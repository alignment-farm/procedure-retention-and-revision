"""Hash-verified component, locality, paired-outcome and cost summaries."""
import argparse,json,hashlib,collections,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();out=a.run.with_name(a.run.name+'-analysis');out.mkdir(exist_ok=False)
for line in (a.run/'SHA256SUMS').read_text().splitlines():
 h,name=line.split('  ',1);assert hashlib.sha256((a.run/name).read_bytes()).hexdigest()==h,name
rows=[json.loads(x) for x in (a.run/'responses.jsonl').read_text().splitlines()];events=[json.loads(x) for x in (a.run/'events.jsonl').read_text().splitlines()]
assert events[-1]['status']=='complete'
groups=collections.defaultdict(list)
for r in rows:
 c=r['case'];scoped=c['channel']=='copper' and c['priority']=='fast';route='marten' if scoped and r['revised'] else {'copper':'kestrel','violet':'marten','amber':'marten','teal':'kestrel'}[c['channel']]
 m=re.fullmatch('(kestrel|marten)\\(text="([^"\\n]*)"\\)',r['raw'].strip());body=m[2] if m else '';suffix=body.endswith('-Q');identifier=body[:-2] if suffix else body
 expected=f'{route}(text="{c["identifier"].upper()}{"-Q" if c["priority"]=="fast" else ""}")';assert expected==r['expected']
 computed=dict(full=r['raw'].strip()==expected,format=m is not None,route=bool(m and m[1]==route),identifier=bool(m and identifier==c['identifier'].upper()),suffix=bool(m and suffix==(c['priority']=='fast')),stale=bool(m and r['revised'] and scoped and m[1]=='kestrel'),overgeneralized=bool(m and r['revised'] and c['channel']=='copper' and c['priority']=='slow' and m[1]=='marten'))
 assert computed==r['scores'],r
 groups[(r['arm'],r['suite'],'all')].append(r)
 if r['suite'].startswith('A-'):groups[(r['arm'],r['suite'],'scope' if scoped else 'unaffected')].append(r)
summary=[]
for (arm,suite,part),rs in groups.items():
 summary.append(dict(arm=arm,suite=suite,part=part,n=len(rs),**{k:sum(r['scores'][k] for r in rs) for k in rs[0]['scores']}))
for e in events:
 if e['kind']=='evaluation':
  for suite,count in e['summary'].items():
   found=next(x for x in summary if x['arm']==e['arm'] and x['suite']==suite and x['part']=='all')
   assert all(found[k]==v for k,v in count.items())
updates=[e for e in events if e['kind']=='update'];costs=dict(updates=len(updates),update_seconds=sum(e['seconds'] for e in updates),update_input_tokens=sum(e['input_tokens'] for e in updates),update_loss_tokens=sum(e['loss_tokens'] for e in updates),generations=len(rows),generation_seconds=sum(r['seconds'] for r in rows),prompt_tokens=sum(r['prompt_tokens'] for r in rows),completion_tokens=sum(r['completion_tokens'] for r in rows),run_seconds=events[-1]['seconds'],peak_mlx_bytes=events[-1]['peak_mlx_bytes'],checkpoint_bytes=sum(f.stat().st_size for f in a.run.glob('*.safetensors')))
(out/'summary.json').write_text(json.dumps(summary,indent=2));(out/'costs.json').write_text(json.dumps(costs,indent=2))
lines=['| State | Suite | Part | n | Route | Full | Identifier | Suffix | Stale | Overgeneralized |','|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
for r in summary:lines.append('| '+' | '.join(str(r[k]) for k in ['arm','suite','part','n','route','full','identifier','suffix','stale','overgeneralized'])+' |')
(out/'tables.md').write_text('\n'.join(lines)+'\n');print(json.dumps(costs,indent=2))

# Check denominators and record identity, not just aggregate totals.
design=json.loads((a.run/'design.json').read_text());nwords=len(design['words'])
assert len({(r['arm'],r['suite'],r['index']) for r in rows})==len(rows)
for e in events:
 if e['kind']=='evaluation':
  assert {k:v['n'] for k,v in e['summary'].items()}=={'A-recall':16,'B-recall':16,'C-recall':4,'A-new':4*nwords,'B-new':4*nwords}
for e in events:
 if e['kind']=='training_start':
  us=[u for u in updates if u['arm']==e['arm']]
  expected=128*(1+bool(e['replay'])+bool(e.get('double',False)));assert len(us)==expected
  for step,index in enumerate(e['order'],1):
   actual=[u for u in us if u['step']==step]
   wanted=[('target',e['targets'][index])]
   if e.get('double',False):wanted.append(('repeat',e['targets'][index]))
   if e['replay']:wanted.append(('replay',e['replay'][e['replay_order'][step-1]]))
   assert [(u['source'],u['case']) for u in actual]==wanted
   assert all(u['gradient_norm']>=0 for u in actual)
lookup={(r['arm'],r['suite'],r['index']):r for r in rows};paired=[]
for method in ['ce','forward']:
 for state in ['B-only','B-double','B-replay','C-only','C-double','C-replay']:
  after=method+'-'+state+'-128';before=method+'-acquired' if state.startswith('B') else method+'-B-replay-128'
  for suite in (['A-new'] if state.startswith('B') else ['A-new','B-new']):
   rs=[r for r in rows if r['arm']==after and r['suite']==suite and not (state.startswith('C') and r['case']['channel']=='copper' and r['case']['priority']=='fast')]
   if not rs:continue
   for metric in ['route','full']:
    transitions=collections.Counter()
    for r in rs:
     old=lookup[(before,suite,r['index'])]['scores'][metric];new=r['scores'][metric];transitions[str(int(old))+str(int(new))]+=1
    paired.append(dict(before=before,after=after,suite=suite,metric=metric,n=len(rs),both_correct=transitions['11'],lost=transitions['10'],gained=transitions['01'],both_wrong=transitions['00']))
(out/'paired.json').write_text(json.dumps(paired,indent=2))
(out/'audit.json').write_text(json.dumps(dict(hash_checks=True,score_records=len(rows),unique_records=True,denominators=True,training_order_checks=True),indent=2))

arm_costs=[]
for arm in sorted({u['arm'] for u in updates}):
 us=[u for u in updates if u['arm']==arm]
 arm_costs.append(dict(arm=arm,updates=len(us),target_updates=sum(u['source']=='target' for u in us),repeat_updates=sum(u['source']=='repeat' for u in us),replay_updates=sum(u['source']=='replay' for u in us),input_tokens=sum(u['input_tokens'] for u in us),loss_tokens=sum(u['loss_tokens'] for u in us),seconds=sum(u['seconds'] for u in us)))
generation_costs=[]
for arm in sorted({r['arm'] for r in rows}):
 rs=[r for r in rows if r['arm']==arm]
 generation_costs.append(dict(arm=arm,n=len(rs),prompt_tokens=sum(r['prompt_tokens'] for r in rs),completion_tokens=sum(r['completion_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs)))
(out/'arm-costs.json').write_text(json.dumps(dict(training=arm_costs,inference=generation_costs,resource_wait_seconds=events[-1].get('resource_wait_seconds',0)),indent=2))

# Early-budget alternatives added prospectively after B development.
for method in ['ce','forward']:
 for state in ['B-only','C-only']:
  after=method+'-'+state+'-32';before=method+'-acquired' if state.startswith('B') else method+'-B-replay-128'
  for suite in (['A-new'] if state.startswith('B') else ['A-new','B-new']):
   rs=[r for r in rows if r['arm']==after and r['suite']==suite and not (state.startswith('C') and r['case']['channel']=='copper' and r['case']['priority']=='fast')]
   if not rs:continue
   for metric in ['route','full']:
    transitions=collections.Counter()
    for r in rs:
     old=lookup[(before,suite,r['index'])]['scores'][metric];new=r['scores'][metric];transitions[str(int(old))+str(int(new))]+=1
    paired.append(dict(before=before,after=after,suite=suite,metric=metric,n=len(rs),both_correct=transitions['11'],lost=transitions['10'],gained=transitions['01'],both_wrong=transitions['00']))
(out/'paired.json').write_text(json.dumps(paired,indent=2))

starts=[e for e in events if e['kind']=='training_start']
for method in ['ce','forward']:
 for stage in ['B','C']:
  subset=[e for e in starts if e['arm'].startswith(method+'-'+stage+'-')]
  if subset:
   assert len({e['initial_hash'] for e in subset})==1,(method,stage,'unequal starting weights')
   assert all(e['order']==subset[0]['order'] for e in subset),(method,stage,'unequal target order')
assert all(e['base_unchanged'] and e['reset_max_logit_delta']==0 for e in events if e['kind']=='training_complete')
checks=json.loads((out/'audit.json').read_text());checks.update(equal_stage_starts=True,equal_target_orders=True,frozen_base_and_reset=True)
(out/'audit.json').write_text(json.dumps(checks,indent=2))

# Descriptive format/length accounting; does not replace any primary metric.
strata=[]
for arm in sorted({r['arm'] for r in rows}):
 for suite in ['A-new','B-new']:
  for length in sorted({len(r['case']['identifier']) for r in rows if r['suite']==suite}):
   rs=[r for r in rows if r['arm']==arm and r['suite']==suite and len(r['case']['identifier'])==length]
   strata.append(dict(arm=arm,suite=suite,length=length,n=len(rs),at_limit=sum(r['at_limit'] for r in rs),**{k:sum(r['scores'][k] for r in rs) for k in ['format','route','identifier','suffix','full']}))
(out/'length-and-format.json').write_text(json.dumps(strata,indent=2))

checks=json.loads((out/'audit.json').read_text());checks.update(analysis_git_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),analysis_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(out/'audit.json').write_text(json.dumps(checks,indent=2))
