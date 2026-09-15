"""CPU-only verification, paired contrasts, and native-unit costs."""
import argparse,collections,hashlib,json,subprocess
from pathlib import Path
import maintenance_task as t

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 for line in (a.run/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);assert sha(a.run/n)==h,n
 rows=[json.loads(l) for l in (a.run/'responses.jsonl').read_text().splitlines()];ev=[json.loads(l) for l in (a.run/'events.jsonl').read_text().splitlines()]
 assert ev[-1]['status']=='complete'
 groups=collections.defaultdict(list)
 for r in rows:
  assert t.check(r['raw'],r['case'],r['version'])==r['scores'];groups[r['state']].append(r)
 def key(c):return json.dumps(c,sort_keys=True)
 summaries={}
 for state,rr in groups.items():
  assert len(rr)==len({key(r['case']) for r in rr})
  inherited,support=state.split('--') if '--' in state else (None,None)
  subsets=dict(all=rr,earlier_waiver=[r for r in rr if t.oracle(r['case'],1)!=t.oracle(r['case'],0)],newest_waiver=[r for r in rr if t.oracle(r['case'],2)!=t.oracle(r['case'],1)])
  for label,entities in [('acquired',t.ACQUIRED),('target',t.TARGETS),('fresh',sorted({r['case']['entity'] for r in rr}-set(t.ACQUIRED+t.TARGETS)))]:subsets[label]=[r for r in rr if r['case']['entity'] in entities]
  if support:
   trained=t.TARGETS if support=='novel' else t.ACQUIRED[:2]+t.TARGETS[:2]
   subsets['current_support_identities']=[r for r in rr if r['case']['entity'] in trained]
   subsets['additional_familiar']=[r for r in rr if r['case']['entity'] in t.ACQUIRED and r['case']['entity'] not in trained]
  report={n:dict(n=len(ss),**{k:sum(r['scores'][k] for r in ss) for k in rr[0]['scores']}) for n,ss in subsets.items()}
  if inherited:
   before={key(r['case']):r for r in groups[inherited+'-start']}
   unchanged=[r for r in rr if t.oracle(r['case'],1)==t.oracle(r['case'],2)]
   report['unchanged']=dict(n=len(unchanged),lost=sum(before[key(r['case'])]['scores']['complete'] and not r['scores']['complete'] for r in unchanged),gained=sum(not before[key(r['case'])]['scores']['complete'] and r['scores']['complete'] for r in unchanged))
   for label in ['acquired','target','fresh','current_support_identities','additional_familiar']:
    subset=[r for r in subsets[label] if t.oracle(r['case'],1)==t.oracle(r['case'],2)]
    report['unchanged_'+label]=dict(n=len(subset),lost=sum(before[key(r['case'])]['scores']['complete'] and not r['scores']['complete'] for r in subset),gained=sum(not before[key(r['case'])]['scores']['complete'] and r['scores']['complete'] for r in subset))
   updates=[e for e in ev if e['kind']=='update' and e['state']==state]
   expected=t.schedule(support,2,64,'negative');assert len(updates)==len(expected)
   for i,(u,(source,c)) in enumerate(zip(updates,expected),1):assert (u['index'],u['source'],u['case'],u['version'])==(i,source,c,2)
   report['costs']=dict(updates=len(updates),input_tokens=sum(u['input_tokens'] for u in updates),loss_tokens=sum(u['loss_tokens'] for u in updates),update_seconds=sum(u['seconds'] for u in updates))
  summaries[state]=report
 starts={e['state']:e for e in ev if e['kind']=='paired_start'}
 for inherited in ['novel','bridged']:assert starts[inherited+'--novel']['state_hash']==starts[inherited+'--bridged']['state_hash']
 costs=dict(updates=sum(e['kind']=='update' for e in ev),generations=len(rows),prompt_tokens=sum(r['prompt_tokens'] for r in rows),completion_tokens=sum(r['completion_tokens'] for r in rows),generation_seconds=sum(r['seconds'] for r in rows),update_seconds=sum(e['seconds'] for e in ev if e['kind']=='update'),finish=ev[-1])
 result=dict(summaries=summaries,costs=costs)
 (a.output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['# State/support comparison','', '| Inherited state | Current support | Complete | Earlier waiver | Newest waiver | Unchanged lost/gained |','|---|---|---|---|---|---|']
 for state,s in summaries.items():
  if '--' not in state:continue
  h,c=state.split('--');fraction=lambda k:f"{s[k]['complete']}/{s[k]['n']}"
  lines.append(f"| {h} | {c} | {fraction('all')} | {fraction('earlier_waiver')} | {fraction('newest_waiver')} | {s['unchanged']['lost']}/{s['unchanged']['gained']} |")
 (a.output/'tables.md').write_text('\n'.join(lines)+'\n');(a.output/'state_support_analyze.py').write_bytes(Path(__file__).read_bytes());(a.output/'revision.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True));print('\n'.join(lines))
if __name__=='__main__':main()
