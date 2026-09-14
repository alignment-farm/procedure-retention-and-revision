"""Separate-process token and checkpoint persistence audit; no accuracy denominator."""
import argparse
import json
from pathlib import Path
import subprocess
import time
import mlx.core as mx
from runtime import Runtime, sha
from task import prompt

p=argparse.ArgumentParser(); p.add_argument('run',type=Path); args=p.parse_args()
out=args.run.with_name(args.run.name+'-audit'); out.mkdir(exist_ok=False)
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
for r in rows:
    assert rt.encode(prompt(r['case']))==r['prefix']
    assert rt.tokenizer.decode(r['ids'][:-1] if r['ended'] else r['ids'])==r['raw']
    if r['ended']: assert r['ids'][-1] in rt.tokenizer.eos_token_ids
    maximum=max(maximum,len(rt.target(r['prefix'],r['expected'])))
assert maximum<=48
for path in sorted(args.run.glob('*.safetensors')):
    while others(): time.sleep(15)
    rt.restore(list(mx.load(str(path)).items()))
    candidates=[r for r in rows if r['arm']==path.stem]
    for suite,index in [('A-recall',0),('A-recall',1),('B-recall',0)]:
        r=next(r for r in candidates if (r['suite'],r['index'])==(suite,index))
        new=rt.generate(r['prefix']); assert new['ids']==r['ids'],(path.name,suite,index)
        checks.append(dict(checkpoint=path.name,suite=suite,index=index,exact=True))
result=dict(git_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            script_sha256=sha(__file__),token_records=len(rows),max_answer_tokens=maximum,
            reload_checks=checks,seconds=time.monotonic()-started)
(out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(dict(token_records=len(rows),reload_checks=len(checks)))
