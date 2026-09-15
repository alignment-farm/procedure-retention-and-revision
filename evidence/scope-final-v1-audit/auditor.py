"""Separate-process token and checkpoint persistence audit; no accuracy denominator."""
import argparse
import json
from pathlib import Path
import subprocess
import time
import mlx.core as mx
from runtime import Runtime, sha
from task import prompt, oracle

p=argparse.ArgumentParser(); p.add_argument('run',type=Path); args=p.parse_args()
out=args.run.with_name(args.run.name+'-audit'); out.mkdir(exist_ok=False)
(out/'auditor.py').write_bytes(Path(__file__).read_bytes())
execution_git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for line in (args.run/'SHA256SUMS').read_text().splitlines():
    h,name=line.split('  ',1); assert sha(args.run/name)==h
def others():
    import os
    ps=subprocess.check_output(['ps','-axo','pid,etime,command'],text=True)
    return [l for l in ps.splitlines() if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0])!=os.getpid()]
started=time.monotonic()
while others():
    assert time.monotonic()-started<7200
    time.sleep(15)
rt=Runtime(); checks=[]; maximum=0; started=time.monotonic()
rows=[json.loads(l) for l in (args.run/'responses.jsonl').read_text().splitlines()]
events=[json.loads(l) for l in (args.run/'events.jsonl').read_text().splitlines()]
design=json.loads((args.run/'design.json').read_text())
for r in rows:
    assert rt.encode(prompt(r['case']))==r['prefix']
    assert rt.tokenizer.decode(r['ids'][:-1] if r['ended'] else r['ids'])==r['raw']
    if r['ended']: assert r['ids'][-1] in rt.tokenizer.eos_token_ids
    maximum=max(maximum,len(rt.target(r['prefix'],r['expected'])))
assert maximum<=48
updates=[e for e in events if e['kind']=='update']
for e in updates:
    prefix=rt.encode(prompt(e['case'])); y=rt.target(prefix,oracle(e['case'],design['phase']!='acquisition'))
    assert e['input_tokens']==len(prefix)+len(y)-1 and e['loss_tokens']==len(y)
source_checks=[]
for e in events:
    if e['kind'] not in ('start_state','reused_acquisition'): continue
    source=Path(e['path'])
    source_rows=[json.loads(l) for l in (source.parent/'responses.jsonl').read_text().splitlines()]
    source_rows=[r for r in source_rows if r['arm']==source.stem and r['suite'] in ('A-recall','B-recall','C-recall')]
    arm=e['name']+'-before' if e['kind']=='start_state' else e['arm']+'-128'
    for old in source_rows:
        new=next(r for r in rows if r['arm']==arm and (r['suite'],r['index'])==(old['suite'],old['index']))
        assert new['prefix']==old['prefix'] and new['ids']==old['ids'],(arm,old['suite'],old['index'])
        source_checks.append(dict(arm=arm,suite=old['suite'],index=old['index'],exact=True))
for path in sorted(args.run.glob('*.safetensors')):
    while others(): time.sleep(15)
    rt.restore(list(mx.load(str(path)).items()))
    candidates=[r for r in rows if r['arm']==path.stem]
    for suite,index in [('A-recall',0),('A-recall',1),('B-recall',0)]:
        r=next(r for r in candidates if (r['suite'],r['index'])==(suite,index))
        new=rt.generate(r['prefix']); assert new['ids']==r['ids'],(path.name,suite,index)
        checks.append(dict(checkpoint=path.name,suite=suite,index=index,exact=True))
result=dict(git_revision=execution_git,
            script_sha256=sha(out/'auditor.py'),token_records=len(rows),training_token_records=len(updates),max_answer_tokens=maximum,source_checks=source_checks,
            reload_checks=checks,seconds=time.monotonic()-started)
(out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(dict(token_records=len(rows),reload_checks=len(checks)))
