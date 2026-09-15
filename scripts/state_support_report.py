"""Assemble complete phase costs and finite-state contrasts without model calls."""
import argparse,collections,hashlib,json,random,subprocess
from pathlib import Path
import maintenance_task as t

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return [json.loads(l) for l in p.read_text().splitlines()]
def verify(root):
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);assert sha(root/n)==h,(root,n)
def main():
 p=argparse.ArgumentParser();p.add_argument('--runs',nargs='+',type=Path,required=True);p.add_argument('--analyses',nargs='+',type=Path,required=True);p.add_argument('--audits',nargs='+',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 runs={};attempts=[]
 for root in a.runs:
  verify(root);ev=read(root/'events.jsonl');rr=read(root/'responses.jsonl');assert ev[-1]['status']=='complete'
  for r in rr:assert r['scores']==t.check(r['raw'],r['case'],r['version'])
  updates=[e for e in ev if e['kind']=='update']
  costs=dict(updates=len(updates),training_input_tokens=sum(u['input_tokens'] for u in updates),training_loss_tokens=sum(u['loss_tokens'] for u in updates),update_seconds=sum(u['seconds'] for u in updates),generations=len(rr),prompt_tokens=sum(r['prompt_tokens'] for r in rr),completion_tokens=sum(r['completion_tokens'] for r in rr),generation_seconds=sum(r['seconds'] for r in rr),wall_seconds=ev[-1]['wall_seconds'],wait_seconds=ev[-1]['wait_seconds'],peak_mlx_bytes=ev[-1]['peak_mlx_bytes'],checkpoint_bytes=sum(e['bytes'] for e in ev if e['kind']=='checkpoint'))
  costs['active_seconds']=costs['wall_seconds']-costs['wait_seconds'];runs[str(root)]=costs
  attempts.extend(dict(run=str(root),**e) for e in ev if e['kind'] in ['acquisition_criterion','acquisition_failed'])
  if 'acquisition' in root.name:
   for seed in json.loads((root/'design.json').read_text())['seeds']:
    actual=[u for u in updates if u['state']==f'seed{seed}-acquisition'];rng=random.Random(seed);order=[]
    for _ in range(16):
     cycle=t.cases(t.ACQUIRED);rng.shuffle(cycle);order+=cycle
    assert [u['case'] for u in actual]==order[:len(actual)]
    checkpoints=[e for e in ev if e['kind']=='acquisition_criterion' and e['state'].startswith(f'seed{seed}-')]
    assert len(actual) in (256,512,1024)
    for e in checkpoints:
     assert e['passed']==(e['recall']['complete']>=60 and e['transfer']['complete']>=28)
    assert not any(e['passed'] for e in checkpoints[:-1])
    for arm in ['novel','bridged']:
     us=[u for u in updates if u['state']==f'seed{seed}-{arm}-v1']
     if not checkpoints[-1]['passed']:assert not us;continue
     assert [(u['source'],u['case']) for u in us]==t.schedule(arm,1,64,'negative')
   for r in rr:
    if r['repeat']==1:
     original=next(x for x in rr if x['state']==r['state'] and x['repeat']==0 and x['case']==r['case']);assert original['ids']==r['ids']
 interactions={}
 for root in a.analyses:
  ss=json.loads((root/'analysis.json').read_text())['summaries']
  count=lambda h,c:ss[h+'--'+c]['all']['complete']
  nn,nb,bn,bb=[count(h,c) for h,c in [('novel','novel'),('novel','bridged'),('bridged','novel'),('bridged','bridged')]]
  interactions[str(root)]=dict(nn=nn,nb=nb,bn=bn,bb=bb,novel_history_support_effect=nn-nb,bridged_history_support_effect=bn-bb,novel_support_history_effect=nn-bn,bridged_support_history_effect=nb-bb,interaction=(nn-nb)-(bn-bb),starts={h:ss[h+'-start']['all']['complete'] for h in ['novel','bridged']})
 audits={}
 for root in a.audits:
  verify(root);d=json.loads((root/'audit.json').read_text());audits[str(root)]={k:v for k,v in d.items() if k not in ['probes','calibration_probes']};audits[str(root)]['probes']=len(d['probes']);assert all(p['exact_match'] for p in d['probes'])
 assert sum(x['rows_verified'] for x in audits.values())==sum(x['generations'] for x in runs.values())
 assert sum(x['updates_verified'] for x in audits.values())==sum(x['updates'] for x in runs.values())
 result=dict(runs=runs,acquisition_attempts=attempts,interactions=interactions,audits=audits,totals={k:sum(r[k] for r in runs.values()) for k in next(iter(runs.values())) if k!='peak_mlx_bytes'})
 (a.output/'report.json').write_text(json.dumps(result,indent=2)+'\n');(a.output/'revision.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True));(a.output/'state_support_report.py').write_bytes(Path(__file__).read_bytes());(a.output/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'));print(json.dumps(dict(interactions=interactions,totals=result['totals']),indent=2))
if __name__=='__main__':main()
