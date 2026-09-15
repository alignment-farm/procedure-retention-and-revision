"""Maintained formal policy + fixed transition interpreter. No oracle at execution."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time
import maintenance_task as t

INITIAL={'eligible_any':[{'certified':1}], 'units_per_order':1}
ADDITIONS=[{'channel':'copper','priority':'fast'}, {'channel':'violet','priority':'slow'}]

def execute(c,policy):
 eligible=any(all(c.get(field)==value for field,value in clause.items()) for clause in policy['eligible_any'])
 state={'stock':c['stock'],'reserved':0,'shipped':0,'status':'HELD'}
 trace=[dict(state)];actions=[]
 if eligible:
  if state['stock']>=policy['units_per_order']:
   state['stock']-=policy['units_per_order'];state['reserved']+=policy['units_per_order'];actions.append('RESERVE');trace.append(dict(state))
   state['reserved']-=policy['units_per_order'];state['shipped']+=policy['units_per_order'];state['status']='SENT';actions.append('SHIP');trace.append(dict(state))
  else:state['status']='WAIT';actions=['SKIP','SKIP'];trace.append(dict(state))
 else:actions=['SKIP','SKIP']
 return ' '.join(['PASS' if eligible else 'FAIL',*actions,str(state['stock']),state['status']]),trace

def main():
 p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 design=json.loads((a.run/'design.json').read_text());entities=design['acquired']+design['targets']+design['fresh'];policy=copy.deepcopy(INITIAL)
 start=time.monotonic();rows=[];maintenance=[]
 for v in range(3):
  tick=time.perf_counter()
  if v:policy['eligible_any'].append(dict(ADDITIONS[v-1]))
  data=json.dumps(policy,sort_keys=True,indent=2)+'\n';(a.output/f'policy-v{v}.json').write_text(data)
  policy=json.loads((a.output/f'policy-v{v}.json').read_text())
  maintenance.append(dict(version=v,seconds=time.perf_counter()-tick,bytes=len(data.encode()),clauses_added=1 if v else 0,records_scanned=0,authority='investigator-supplied formal rule'))
  for repeat in range(2):
   for c in t.cases(entities):
    tick=time.perf_counter();raw,trace=execute(c,policy);elapsed=time.perf_counter()-tick
    scores=t.check(raw,c,v);assert scores['complete']
    for state in trace:assert state['stock']>=0 and state['reserved']>=0 and state['stock']+state['reserved']+state['shipped']==c['stock']
    rows.append(dict(version=v,repeat=repeat,case=c,raw=raw,trace=trace,scores=scores,seconds=elapsed))
 (a.output/'responses.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
 report=dict(git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),python=platform.python_version(),n=len(rows),complete=sum(r['scores']['complete'] for r in rows),inference_seconds=sum(r['seconds'] for r in rows),maintenance=maintenance,wall_seconds=time.monotonic()-start,model_tokens=0,updates=0,paid_cost=0,information='privileged executable rules; manual construction and authority')
 (a.output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
 for name in ['maintenance_explicit.py','maintenance_task.py']:(a.output/name).write_bytes(Path('scripts',name).read_bytes())
 (a.output/'protocol.md').write_bytes(Path('protocol/maintenance-reference-diagnosis-v1.md').read_bytes())
 (a.output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
 print(json.dumps(report,indent=2))

if __name__=='__main__':main()
