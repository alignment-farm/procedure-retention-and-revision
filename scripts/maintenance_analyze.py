"""Recompute maintenance endpoints, paired preservation and native-unit costs."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import random
import subprocess
from pathlib import Path
import maintenance_task as t


def main():
 p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 a.output.mkdir(parents=True,exist_ok=False)
 for name in ['maintenance_analyze.py','maintenance_task.py']:(a.output/name).write_bytes(Path('scripts',name).read_bytes())
 (a.output/'revision.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True))
 def write(n,d): (a.output/n).write_text(json.dumps(d,indent=2)+'\n')
 for line in (a.run/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);assert hashlib.sha256((a.run/n).read_bytes()).hexdigest()==h,n
 events=[json.loads(l) for l in (a.run/'events.jsonl').read_text().splitlines()]
 rows=[json.loads(l) for l in (a.run/'responses.jsonl').read_text().splitlines()]
 assert events[-1]['kind']=='finish' and events[-1]['status']=='complete'
 design=json.loads((a.run/'design.json').read_text())
 grouped=defaultdict(list)
 for r in rows:
  assert r['scores']==t.check(r['raw'],r['case'],r['version'])
  assert r['expected']==t.oracle(r['case'],r['version'])
  assert r['prompt_tokens']==len(r['prefix']) and r['completion_tokens']==len(r['ids'])
  grouped[(r['state'],r['version'],r['repeat'])].append(r)
 summary=[]
 for (state,v,repeat),rs in grouped.items():
  keys=[json.dumps(r['case'],sort_keys=True) for r in rs];assert len(keys)==len(set(keys))
  summary.append(dict(state=state,version=v,repeat=repeat,n=len(rs),**{k:sum(r['scores'][k] for r in rs) for k in rs[0]['scores']}))
 for e in events:
  if e['kind']=='evaluation':
   found=next(s for s in summary if (s['state'],s['version'],s['repeat'])==(e['state'],e['version'],e['repeat']))
   assert e['summary']=={k:v for k,v in found.items() if k not in ['state','version','repeat']}
 updates=defaultdict(list)
 for e in events:
  if e['kind']=='update':
   assert math.isfinite(e['loss']) and math.isfinite(e['gradient_norm'])
   updates[e['state']].append(e)
 for state,us in updates.items():
  if state.endswith('-acquisition'):
   rng=random.Random(int(state.split('-')[0][4:]));order=[]
   for _ in range(16):
    cycle=t.cases(t.ACQUIRED);rng.shuffle(cycle);order+=cycle
   for i,u in enumerate(us):assert (u['index'],u['case'],u['version'])==(i+1,order[i],0)
  if '-v' in state:
   arm=state.split('-')[1];v=int(state[-1]);schedule=t.schedule(arm,v,design['blocks'],design.get('boundary_mode','all'))
   assert len(us)==len(schedule)
   for i,(u,(source,c)) in enumerate(zip(us,schedule),1):
    assert (u['index'],u['source'],u['case'],u['version'])==(i,source,c,v)
 for seed in design['seeds']:
  starts=[e['state_hash'] for e in events if e['kind']=='paired_start' and e['state'].startswith(f'seed{seed}-')]
  assert not starts or len(starts)==2 and len(set(starts))==1
  selected=[e for e in events if e['kind']=='acquisition_criterion' and e['state'].startswith(f'seed{seed}-') and e['passed']]
  if selected:
   assert len(selected)==1
   cp=next(e for e in events if e['kind']=='checkpoint' and e['state']==selected[0]['state'])
   assert starts and starts[0]==cp['state_hash']
  reused=[e for e in events if e['kind']=='reused_acquisition']
  if reused:assert starts[0]==reused[0]['state_hash']
  inv=[e for e in events if e['kind']=='invariants' and e['seed']==seed]
  assert not starts or len(inv)==1 and inv[0]['base_unchanged'] and inv[0]['reset_max_logit_delta']==0
 paired=[];obligations=[];repeats=[]
 def key(r):return json.dumps(r['case'],sort_keys=True)
 for (state,v,repeat),rs in grouped.items():
  if repeat==1:
   before={key(r):r for r in grouped[(state,v,0)]}
   repeats.append(dict(state=state,version=v,n=len(rs),identical=sum(r['ids']==before[key(r)]['ids'] for r in rs)))
  if repeat!=0 or not ('-novel-v' in state or '-bridged-v' in state):continue
  seed,arm,_=state.split('-')
  prior=(seed+'-no-update',0,0) if v==1 else (seed+'-'+arm+f'-v{v-1}',v-1,0)
  before={key(r):r for r in grouped[prior]}
  unchanged=[r for r in rs if t.oracle(r['case'],v)==t.oracle(r['case'],v-1)]
  for subgroup,subset in [('all',unchanged),('acquired',[r for r in unchanged if r['case']['entity'] in t.ACQUIRED]),('fresh',[r for r in unchanged if r['case']['entity'] in design['fresh']]),('earlier-revision',[r for r in unchanged if v>1 and t.oracle(r['case'],v-1)!=t.oracle(r['case'],0)])]:
   paired.append(dict(state=state,version=v,group=subgroup,n=len(subset),
     before=sum(before[key(r)]['scores']['complete'] for r in subset),after=sum(r['scores']['complete'] for r in subset),
     lost=sum(before[key(r)]['scores']['complete'] and not r['scores']['complete'] for r in subset),
     gained=sum(not before[key(r)]['scores']['complete'] and r['scores']['complete'] for r in subset)))
  changed=[r for r in rs if t.oracle(r['case'],v)!=t.oracle(r['case'],v-1)]
  for label,entities in [('familiar-first-two',t.ACQUIRED[:2]),('familiar-withheld',t.ACQUIRED[2:]),('correction-new',t.TARGETS),('fresh',design['fresh'])]:
   sub=[r for r in changed if r['case']['entity'] in entities]
   direct_entities=t.TARGETS if arm=='novel' else t.ACQUIRED[:2]+t.TARGETS[:2]
   direct=[r for r in sub if r['case']['entity'] in direct_entities]
   obligations.append(dict(state=state,version=v,group=label,n=len(sub),directly_relabelled_n=len(direct),directly_relabelled_complete=sum(r['scores']['complete'] for r in direct),complete=sum(r['scores']['complete'] for r in sub),stale=sum(r['scores']['stale'] for r in sub),
                           downstream_n=sum(r['case']['stock']==1 for r in sub),downstream_complete=sum(r['case']['stock']==1 and r['scores']['complete'] for r in sub)))
 costs=[]
 for state,us in updates.items():
  costs.append(dict(state=state,updates=len(us),input_tokens=sum(u['input_tokens'] for u in us),loss_tokens=sum(u['loss_tokens'] for u in us),seconds=sum(u['seconds'] for u in us),sources=dict(Counter(u['source'] for u in us))))
 inference=[]
 for (state,v,repeat),rs in grouped.items():
  inference.append(dict(state=state,version=v,repeat=repeat,n=len(rs),complete=sum(r['scores']['complete'] for r in rs),prompt_tokens=sum(r['prompt_tokens'] for r in rs),completion_tokens=sum(r['completion_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs)))
 counterfactual=[]
 for (state,v,repeat),rs in grouped.items():
  if state.endswith('-no-update') and v==0:
   for version in (1,2):
    counterfactual.append(dict(state=state,version=version,repeat=repeat,n=len(rs),complete=sum(t.check(r['raw'],r['case'],version)['complete'] for r in rs),stale=sum(t.check(r['raw'],r['case'],version)['stale'] for r in rs),reuses_generation=True))
 write('no-update-rescored.json',counterfactual)
 write('summary.json',summary);write('paired.json',paired);write('obligations.json',obligations);write('repeatability.json',repeats)
 write('costs.json',dict(training=costs,inference=inference,finish=events[-1],maintenance=[e for e in events if e['kind']=='maintenance'],checkpoints=[e for e in events if e['kind']=='checkpoint']))
 write('audit.json',dict(responses=len(rows),updates=sum(map(len,updates.values())),hashes_verified=True,score_recomputed=True,schedules_verified=True,paired_starts_verified=True))
 lines=['# Complete work-order maintenance','', '| State | Version | Complete | Eligibility | Shipment | Stock |','|---|---:|---:|---:|---:|---:|']
 for s in summary:
  if s['repeat']==0:lines.append(f"| {s['state']} | {s['version']} | {s['complete']}/{s['n']} | {s['eligibility']} | {s['shipment']} | {s['stock']} |")
 lines+=['','## Paired unchanged tasks','','| State | Group | n | Before | After | Lost | Gained |','|---|---|---:|---:|---:|---:|---:|']
 for r in paired:lines.append('| '+' | '.join(str(r[k]) for k in ['state','group','n','before','after','lost','gained'])+' |')
 lines+=['','## Changed obligations','','| State | Group | Complete | Stale | Downstream complete |','|---|---|---:|---:|---:|']
 for r in obligations:lines.append(f"| {r['state']} | {r['group']} | {r['complete']}/{r['n']} | {r['stale']} | {r['downstream_complete']}/{r['downstream_n']} |")
 (a.output/'tables.md').write_text('\n'.join(lines)+'\n')
 (a.output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
 print(json.dumps(dict(responses=len(rows),updates=sum(map(len,updates.values())),finish=events[-1]),indent=2))

if __name__=='__main__': main()
