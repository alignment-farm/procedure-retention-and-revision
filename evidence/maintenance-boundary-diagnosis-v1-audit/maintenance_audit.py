"""Separate-process saved-adapter and token audit; excluded from accuracy counts."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
import mlx.core as mx
from runtime import Runtime, resource, sha
import maintenance_task as t
from maintenance_probe_selection import select


def main():
 p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 a.output.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();wait=0.
 for n in ['maintenance_audit.py','maintenance_probe_selection.py','maintenance_task.py','runtime.py','task.py']:(a.output/n).write_bytes(Path('scripts',n).read_bytes())
 (a.output/'revision.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True))
 def guard():
  nonlocal wait
  while True:
   ps=subprocess.check_output(['ps','-axo','pid,command'],text=True).splitlines()
   jobs=[l for l in ps if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0])!=os.getpid()]
   if not jobs:return
   tick=time.monotonic();time.sleep(10);wait+=time.monotonic()-tick
   assert wait<7200
 guard()
 for line in (a.run/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);assert sha(a.run/n)==h
 resource();guard();rt=Runtime()
 rows=[json.loads(l) for l in (a.run/'responses.jsonl').read_text().splitlines()]
 events=[json.loads(l) for l in (a.run/'events.jsonl').read_text().splitlines()]
 for r in rows:
  prefix=rt.encode(t.prompt(r['case'],r['version'] if r['rule'] else None))
  assert prefix==r['prefix']
  ids=r['ids'][:-1] if r['ended'] else r['ids']
  assert rt.tokenizer.decode(ids)==r['raw']
 updates=[e for e in events if e['kind']=='update']
 for u in updates:
  prefix=rt.encode(t.prompt(u['case']));y=rt.target(prefix,t.oracle(u['case'],u['version']))
  assert u['input_tokens']==len(prefix)+len(y)-1 and u['loss_tokens']==len(y)
 calibration=[];calibration_probes=[]
 if (a.run/'routing-calibration.json').exists():
  from task import prompt as routing_prompt, score as routing_score
  reference=json.loads((a.run/'routing-calibration.json').read_text());calibration=reference['responses']
  path=Path(reference['path']);assert sha(path)==reference['sha256'];rt.restore(list(mx.load(str(path)).items()))
  for r in calibration:
   assert rt.encode(routing_prompt(r['case']))==r['prefix']
   assert rt.tokenizer.decode(r['ids'][:-1] if r['ended'] else r['ids'])==r['raw']
   assert routing_score(r['raw'],r['case'])==r['scores']
  for r in calibration[:3]:
   guard();actual=rt.generate(r['prefix']);assert actual['ids']==r['ids']
   calibration_probes.append(dict(case=r['case'],ids=actual['ids'],exact_match=True))
 probes=[]
 for e in events:
  if e['kind']!='checkpoint':continue
  guard();path=a.run/(e['state']+'.safetensors');assert sha(path)==e['sha256'];rt.restore(list(mx.load(str(path)).items()))
  candidates=[r for r in rows if r['state'] in (e['state'],e['state']+'-new') and r['repeat']==0]
  selected=select(candidates)
  for r in selected:
   guard();result=rt.generate(r['prefix'],limit=40);assert result['ids']==r['ids'],e['state']
   probes.append(dict(state=e['state'],version=r['version'],case=r['case'],ids=result['ids'],expected=r['expected'],recorded_raw=r['raw'],exact_match=True))
 result=dict(rows_verified=len(rows),updates_verified=len(updates),probes=probes,calibration_rows_verified=len(calibration),calibration_probes=calibration_probes,seconds=time.monotonic()-start,wait_seconds=wait)
 (a.output/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.output/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
 print(json.dumps({k:v for k,v in result.items() if k!='probes'}));print('probes',len(probes))

if __name__=='__main__':main()
