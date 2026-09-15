"""Scope/rehearsal follow-up. All attempts append evidence in a new directory."""
import argparse
import json
import os
from pathlib import Path
import random
import subprocess
import time
import mlx.core as mx
from runtime import Runtime, resource, sha, digest
from task import cases, A_WORDS, B_WORDS, DEV_WORDS, fresh, prompt, oracle
from scope_task import ARMS, ANCHORED_ARMS, TARGETS, NARROW, BROAD, BOUNDARY, components, schedule, block_updates

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--phase', choices=['development', 'acquisition', 'final'], default='development')
    p.add_argument('--blocks', type=int, default=128)
    p.add_argument('--starts', nargs='+', default=['ce'])
    p.add_argument('--acquisition-run', type=Path)
    p.add_argument('--anchored', action='store_true')
    p.add_argument('--arms', nargs='+')
    p.add_argument('--seeds', nargs='+', type=int, default=[101,202])
    p.add_argument('--later-blocks', type=int, default=32)
    p.add_argument('--later-replay', action='store_true')
    p.add_argument('--reuse-acquisition', type=Path)
    p.add_argument('--start-manifest', type=Path)
    args = p.parse_args()
    out = args.output; out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); wait_seconds = 0.; last_check = 0.
    for name in ['scope_experiment.py', 'scope_task.py', 'runtime.py', 'task.py']:
        (out / name).write_bytes(Path('scripts', name).read_bytes())
    protocol = Path('protocol/scope-anchored-final-v1.md' if args.phase == 'final' and args.anchored else
                    'protocol/scope-boundary-diagnosis-v1.md' if args.anchored else
                    'protocol/scope-final-v1.md' if args.phase == 'final' else 'protocol/scope-development-v1.md')
    (out / 'protocol.md').write_bytes(protocol.read_bytes())
    if args.reuse_acquisition:
        (out / 'acquisition-repair-protocol.md').write_bytes(Path('protocol/scope-acquisition-repair-v1.md').read_bytes())
    if args.start_manifest: (out / 'start-manifest.json').write_bytes(args.start_manifest.read_bytes())
    ev = (out / 'events.jsonl').open('x'); responses = (out / 'responses.jsonl').open('x')
    def save(name, data): (out / name).write_text(json.dumps(data, indent=2) + '\n')
    def emit(kind, **data):
        ev.write(json.dumps(dict(kind=kind, elapsed=time.monotonic()-start, **data)) + '\n'); ev.flush()
    def check():
        nonlocal wait_seconds, last_check
        if time.monotonic() - last_check > 5:
            while True:
                ps = subprocess.check_output(['ps', '-axo', 'pid,etime,rss,command'], text=True)
                jobs = [line for line in ps.splitlines() if '/bin/python' in line and 'scripts/' in line
                        and 'monitor.py' not in line and int(line.split()[0]) != os.getpid()]
                emit('resource_check', jobs=jobs)
                if not jobs: break
                print('Yielding shared hardware:', jobs, flush=True)
                before = time.monotonic(); time.sleep(15); wait_seconds += time.monotonic()-before
                assert wait_seconds < 7200, 'two-hour resource wait ceiling'
            last_check = time.monotonic()
        assert time.monotonic()-start-wait_seconds < (3600 if args.phase == 'final' else 1500), 'active budget'
        assert mx.get_peak_memory() < 40e9, '40 GB MLX ceiling'
    def verify_manifest(path):
        for line in (path / 'SHA256SUMS').read_text().splitlines():
            h, name = line.split('  ', 1); assert sha(path / name) == h
    words = DEV_WORDS if args.phase != 'final' else fresh(2026091429, 12)
    excluded = set(json.loads(Path('sources/prior-evaluation-identifiers.json').read_text()))
    excluded.update(json.loads(Path('evidence/final-v1/design.json').read_text())['words'])
    if args.phase == 'final': assert not set(words) & excluded
    arms = args.arms or (ANCHORED_ARMS if args.anchored else ARMS)
    assert all(arm in (ANCHORED_ARMS if args.anchored else ARMS) for arm in arms)
    save('design.json', dict(phase=args.phase, blocks=args.blocks, starts=args.starts, arms=arms, anchored=args.anchored,
         seeds=args.seeds, later_blocks=args.later_blocks, later_replay=args.later_replay, reuse_acquisition=str(args.reuse_acquisition) if args.reuse_acquisition else None,
         words=words, fresh_seed=2026091429 if args.phase == 'final' else None,
         targets=TARGETS, narrow=NARROW, broad=BROAD, boundary=BOUNDARY if args.anchored else [], schedule=schedule(args.blocks),
         acquisition_run=str(args.acquisition_run), args={k:str(v) for k,v in vars(args).items()}))
    status = 'failed'
    try:
        emit('revision', git=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
             dirty=subprocess.check_output(['git', 'status', '--short'], text=True))
        check(); save('resource.json', resource()); rt = Runtime()
        def evaluate(arm, revised=True, recall_only=False):
            suites = [('A-recall', cases(A_WORDS)), ('B-recall', cases(B_WORDS, ('amber', 'teal'))),
                      ('C-recall', TARGETS)]
            if args.anchored: suites += [('boundary-recall', BOUNDARY)]
            if not recall_only:
                suites += [('A-new', cases(words)), ('B-new', cases(words, ('amber', 'teal')))]
            summary = {}
            for suite, cs in suites:
                counts = {k:0 for k in components('', cs[0], revised)}
                for i, c in enumerate(cs):
                    check(); prefix = rt.encode(prompt(c)); r = rt.generate(prefix)
                    s = components(r['raw'], c, revised)
                    for k,v in s.items(): counts[k] += int(v)
                    responses.write(json.dumps(dict(arm=arm, suite=suite, index=i, case=c,
                                    revised=revised, prefix=prefix, expected=oracle(c, revised), scores=s, **r))+'\n')
                    responses.flush()
                summary[suite] = dict(n=len(cs), **counts)
            emit('evaluation', arm=arm, summary=summary)
            print(arm, {s:(d['route'],d['full'],d['n']) for s,d in summary.items()}, flush=True)
            return summary
        def checkpoint(name):
            path = out / (name + '.safetensors'); mx.save_safetensors(str(path), dict(rt.snapshot()))
            emit('checkpoint', arm=name, sha256=sha(path), state_hash=digest(rt.snapshot()))
        def update(arm, step, source, case, opt, revised):
            check(); prefix = rt.encode(prompt(case)); y = rt.target(prefix, oracle(case, revised))
            emit('update', arm=arm, step=step, source=source, case=case, **rt.step(prefix, y, opt))
        if args.phase == 'acquisition':
            if args.reuse_acquisition: verify_manifest(args.reuse_acquisition)
            for seed in args.seeds:
                rt.reinitialize(seed); opt = rt.optimizer(); rng = random.Random(seed)
                arm = f'seed{seed}-A'
                if not args.reuse_acquisition: emit('training_start', arm=arm, seed=seed, initial_hash=digest(rt.snapshot()))
                order = []
                while len(order) < 128:
                    cycle = cases(A_WORDS); rng.shuffle(cycle); order += cycle
                if args.reuse_acquisition:
                    path=args.reuse_acquisition/(arm+'-128.safetensors')
                    rt.restore(list(mx.load(str(path)).items()))
                    emit('reused_acquisition', arm=arm, path=str(path), sha256=sha(path), state_hash=digest(rt.snapshot()))
                else:
                    for i,c in enumerate(order, 1): update(arm, i, 'acquisition', c, opt, False)
                checkpoint(arm+'-128'); a = evaluate(arm+'-128', False, True)
                emit('acquisition_criterion', arm=arm, passed=a['A-recall']['route'] >= 15,
                     route=a['A-recall']['route'], full=a['A-recall']['full'], n=16)
                opt = rt.optimizer(); arm = f'seed{seed}-B'; emit('training_start', arm=arm, initial_hash=digest(rt.snapshot()))
                order = []
                while len(order) < args.later_blocks:
                    cycle = cases(B_WORDS, ('amber', 'teal')); rng.shuffle(cycle); order += cycle
                replay_order=[]; replay_rng=random.Random(73)
                while len(replay_order) < args.later_blocks:
                    cycle=cases(A_WORDS); replay_rng.shuffle(cycle); replay_order+=cycle
                for i,c in enumerate(order[:args.later_blocks], 1):
                    update(arm, i, 'later', c, opt, False)
                    if args.later_replay: update(arm,i,'old-replay',replay_order[i-1],opt,False)
                    if i in (32,args.later_blocks):
                        checkpoint(arm+f'-{i}'); b=evaluate(arm+f'-{i}',False,True)
                        emit('start_criterion', arm=arm, step=i, passed=a['A-recall']['route'] >= 15 and b['A-recall']['route'] >= 15 and b['B-recall']['route'] >= 15,
                             A_route=b['A-recall']['route'], B_route=b['B-recall']['route'], A_full=b['A-recall']['full'], B_full=b['B-recall']['full'])
                emit('training_complete', arm=arm, **rt.invariants())
        else:
            verify_manifest(Path('evidence/final-v1'))
            if args.acquisition_run: verify_manifest(args.acquisition_run)
            for name in args.starts:
                overrides=json.loads(args.start_manifest.read_text()) if args.start_manifest else {}
                path = (Path(overrides[name]) if name in overrides else
                        args.acquisition_run / f'{name}-B-32.safetensors' if name.startswith('seed')
                        else Path('evidence/final-v1') / f'{name}-B-replay-128.safetensors')
                verify_manifest(path.parent)
                rt.restore(list(mx.load(str(path)).items())); initial = rt.snapshot()
                emit('start_state', name=name, path=str(path), sha256=sha(path), state_hash=digest(initial))
                checkpoint(name+'-before'); evaluate(name+'-before')
                for arm in arms:
                    label = name+'-'+arm; rt.restore(initial); opt = rt.optimizer()
                    emit('training_start', arm=label, initial_hash=digest(rt.snapshot()))
                    for i,(target,narrow,broad) in enumerate(schedule(args.blocks),1):
                        for source,c in block_updates(arm,target,narrow,broad): update(label,i,source,c,opt,True)
                        if i == args.blocks or (i == 32 and (args.phase == 'development' or arm in ('narrow', 'broad', 'boundary-repeat', 'boundary-history'))):
                            checkpoint(label+f'-{i}'); evaluate(label+f'-{i}')
                    emit('training_complete', arm=label, **rt.invariants())
        status = 'complete'
    finally:
        emit('complete', status=status, seconds=time.monotonic()-start, resource_wait_seconds=wait_seconds,
             peak_mlx_bytes=mx.get_peak_memory())
        ev.close(); responses.close()
        (out / 'SHA256SUMS').write_text('\n'.join(sha(f)+'  '+f.name for f in sorted(out.iterdir())
                                      if f.is_file() and f.name != 'SHA256SUMS')+'\n')

if __name__ == '__main__': main()
