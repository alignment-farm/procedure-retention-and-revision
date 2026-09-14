"""Audit and tabulate scope follow-up runs without loading model weights."""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()

def analyze(run, output):
    output.mkdir(exist_ok=False)
    for line in (run/'SHA256SUMS').read_text().splitlines():
        h, name = line.split('  ', 1); assert sha(run/name) == h, name
    spec = importlib.util.spec_from_file_location('saved_scope', run/'scope_task.py')
    task = importlib.util.module_from_spec(spec); spec.loader.exec_module(task)
    design = json.loads((run/'design.json').read_text())
    rows = [json.loads(line) for line in (run/'responses.jsonl').read_text().splitlines()]
    events = [json.loads(line) for line in (run/'events.jsonl').read_text().splitlines()]
    states = defaultdict(list)
    for row in rows:
        assert row['scores'] == task.components(row['raw'], row['case'], row['revised'])
        assert row['completion_tokens'] == len(row['ids'])
        assert row['prompt_tokens'] == len(row['prefix'])
        assert row['expected'] == task.score.__globals__['oracle'](row['case'], row['revised'])
        states[row['arm']].append(row)
    if design['phase'] == 'acquisition':
        expected_states = {f'seed{seed}-{stage}-{steps}' for seed in (101,202) for stage,steps in [('A',128),('B',32)]}
    else:
        expected_states = {name+'-before' for name in design['starts']}
        for name in design['starts']:
            for mode in task.ARMS:
                endpoints = {design['blocks']}
                if design['phase'] == 'development' or mode in ('narrow','broad'): endpoints.add(32)
                expected_states.update(f'{name}-{mode}-{step}' for step in endpoints)
    assert set(states) == expected_states, (set(states),expected_states)
    def counts(rs):
        return dict(n=len(rs), **{key:sum(r['scores'][key] for r in rs) for key in rows[0]['scores']})
    summaries = {}
    for arm, rs in states.items():
        case_sets = {'A-recall':task.cases(task.A_WORDS), 'B-recall':task.cases(task.B_WORDS,('amber','teal')), 'C-recall':task.TARGETS}
        if design['phase'] != 'acquisition':
            case_sets.update({'A-new':task.cases(design['words']), 'B-new':task.cases(design['words'],('amber','teal'))})
        assert {r['suite'] for r in rs} == set(case_sets)
        for suite,expected in case_sets.items():
            actual = sorted([r for r in rs if r['suite']==suite],key=lambda r:r['index'])
            assert [r['index'] for r in actual] == list(range(len(expected)))
            assert [r['case'] for r in actual] == expected
        by_suite = {s:counts([r for r in rs if r['suite'] == s]) for s in sorted({r['suite'] for r in rs})}
        for event in [e for e in events if e['kind'] == 'evaluation' and e['arm'] == arm]:
            assert event['summary'] == by_suite
        fresh = [r for r in rs if r['suite'].endswith('-new')]
        groups = dict(scope=[r for r in fresh if task.scope(r['case'])],
                      other_old=[r for r in fresh if r['suite'] == 'A-new' and not task.scope(r['case'])],
                      later=[r for r in fresh if r['suite'] == 'B-new'],
                      unchanged=[r for r in fresh if not task.scope(r['case'])], all=fresh,
                      boundary=[r for r in rs if r['suite'].endswith('-recall') and r['case'] in task.NARROW])
        summaries[arm] = dict(suites=by_suite, groups={key:counts(value) for key,value in groups.items()})
        expected_n = 36 if design['phase'] == 'acquisition' else 36+8*len(design['words'])
        assert len(rs) == expected_n, (arm,len(rs),expected_n)
        assert len({(r['suite'],r['index']) for r in rs}) == len(rs)
    checkpoints = [e for e in events if e['kind'] == 'checkpoint']
    assert {e['arm'] for e in checkpoints} == set(states)
    for e in checkpoints: assert sha(run/(e['arm']+'.safetensors')) == e['sha256']
    for e in [e for e in events if e['kind'] == 'start_state']:
        assert e['state_hash'] == next(c['state_hash'] for c in checkpoints if c['arm'] == e['name']+'-before')
    updates = [e for e in events if e['kind'] == 'update']
    starts = [e for e in events if e['kind'] == 'training_start']
    costs = {}
    for e in starts:
        arm = e['arm']; us = [u for u in updates if u['arm'] == arm]
        per_source = {}
        for source in sorted({u['source'] for u in us}):
            subset = [u for u in us if u['source'] == source]
            per_source[source] = dict(updates=len(subset), unique_cases=len({json.dumps(u['case'],sort_keys=True) for u in subset}),
                                      **{k:sum(u[k] for u in subset) for k in ['input_tokens','loss_tokens','seconds']})
        costs[arm] = per_source
        if design['phase'] == 'acquisition':
            import random
            seed=int(arm.split('-')[0][4:]); rng=random.Random(seed)
            a_order=[]; b_order=[]
            for _ in range(8):
                cycle=task.cases(task.A_WORDS); rng.shuffle(cycle); a_order+=cycle
            for _ in range(2):
                cycle=task.cases(task.B_WORDS,('amber','teal')); rng.shuffle(cycle); b_order+=cycle
            order=a_order if arm.endswith('-A') else b_order
            assert [(u['step'],u['case']) for u in us] == list(enumerate(order,1))
            if arm.endswith('-B'):
                assert e['initial_hash'] == next(c['state_hash'] for c in checkpoints if c['arm'] == f'seed{seed}-A-128')
        else:
            name, mode = arm.rsplit('-',1)
            assert e['initial_hash'] == next(s['state_hash'] for s in events if s['kind'] == 'start_state' and s['name'] == name)
            expected = []
            for i,(target,narrow,broad) in enumerate(task.schedule(design['blocks']),1):
                expected.append((i,'target',target))
                if mode != 'only': expected.append((i,'repeat' if mode == 'repeat' else 'replay', {'repeat':target,'narrow':narrow,'broad':broad}[mode]))
            assert [(u['step'],u['source'],u['case']) for u in us] == expected
    for e in events:
        if e['kind'] == 'training_complete': assert e['base_unchanged'] and e['reset_max_logit_delta'] == 0
    paired = {}
    for arm, rs in states.items():
        if '-before' in arm or design['phase'] == 'acquisition': continue
        name = arm.split('-')[0]
        before = {(r['suite'],r['index']):r for r in states[name+'-before'] if r['suite'].endswith('-new') and not task.scope(r['case'])}
        after = {(r['suite'],r['index']):r for r in rs if r['suite'].endswith('-new') and not task.scope(r['case'])}
        assert before.keys() == after.keys()
        assert all(before[k]['case'] == after[k]['case'] and before[k]['expected'] == after[k]['expected'] for k in before)
        paired[arm] = dict(n=len(before))
        for metric in ['route','strict_route','format','identifier','suffix','full']:
            pairs = [(before[k]['scores'][metric],after[k]['scores'][metric]) for k in before]
            paired[arm][metric] = dict(before=sum(a for a,b in pairs),after=sum(b for a,b in pairs),
                                      lost=sum(a and not b for a,b in pairs),gained=sum(not a and b for a,b in pairs))
    completion = events[-1]; assert completion['kind'] == 'complete' and completion['status'] == 'complete'
    audit = dict(analysis_git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                 script_sha256=sha(__file__), run_git=events[0]['git'], response_records=len(rows),
                 updates=len(updates), checkpoints=len(checkpoints), manifest_verified=True,
                 score_and_schedule_verified=True, completion=completion,
                 generation_cost={k:sum(r[k] for r in rows) for k in ['prompt_tokens','completion_tokens','seconds']},
                 acquisition_criteria=[e for e in events if e['kind'] in ['acquisition_criterion','start_criterion']])
    for filename,data in [('summary.json',summaries),('paired.json',paired),('costs.json',costs),('audit.json',audit)]:
        (output/filename).write_text(json.dumps(data,indent=2)+'\n')
    lines = ['# Scope follow-up counts','',
             'Route recognizes an anchored tool name independently of argument syntax. Full requires the exact complete call.', '',
             '| State | C recall route/full /4 | Boundary route /7 | Scope route/full | Other old route | Later route | All full | Unchanged full lost/gained |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for arm,s in summaries.items():
        g=s['groups']; c=s['suites']['C-recall']; pair=paired.get(arm,{}).get('full',{})
        lines.append(f"| {arm} | {c['route']}/{c['full']} | {g['boundary']['route']} | {g['scope']['route']}/{g['scope']['full']} /{g['scope']['n']} | {g['other_old']['route']}/{g['other_old']['n']} | {g['later']['route']}/{g['later']['n']} | {g['all']['full']}/{g['all']['n']} | {pair.get('lost','—')}/{pair.get('gained','—')} |")
    (output/'tables.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(audit,indent=2))

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('run',type=Path); args=p.parse_args()
    analyze(args.run,args.run.with_name(args.run.name+'-analysis'))
