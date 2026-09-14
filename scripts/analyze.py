"""Hash-verified component, locality, paired-outcome and cost summaries."""
import argparse,json,hashlib,collections,re
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
