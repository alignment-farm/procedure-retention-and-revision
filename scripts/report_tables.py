"""Compact tables from the independently checked summaries; no model selection."""
import json,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('analysis',type=Path);a=p.parse_args()
rows=json.loads((a.analysis/'summary.json').read_text())
def get(arm,suite,part='all'):return next(x for x in rows if (x['arm'],x['suite'],x['part'])==(arm,suite,part))
lines=['| Acquired state | Later learning | Old route /48 | New route /48 | Old call /48 | New call /48 |','|---|---|---:|---:|---:|---:|']
for method in ['ce','forward']:
 for suffix,label in [('acquired','None'),('B-only-32','32 new'),('B-only-128','128 new'),('B-double-128','256 new'),('B-replay-128','128 new +128 replay')]:
  arm=method+'-'+suffix;x=get(arm,'A-new');y=get(arm,'B-new');lines.append(f'| {method} | {label} | {x["route"]} | {y["route"]} | {x["full"]} | {y["full"]} |')
lines+=['','| Acquired state | Correction updates | Scope route /12 | Other old route /36 | New-channel route /48 | Full calls /96 | Stale /12 | Overbroad /12 |','|---|---|---:|---:|---:|---:|---:|---:|']
for method in ['ce','forward']:
 for suffix,label in [('C-only-32','32 corrections'),('C-only-128','128 corrections'),('C-double-128','256 corrections'),('C-replay-128','128 corrections +128 replay')]:
  arm=method+'-'+suffix;x=get(arm,'A-new','scope');y=get(arm,'A-new','unaffected');z=get(arm,'B-new');lines.append(f'| {method} | {label} | {x["route"]} | {y["route"]} | {z["route"]} | {x["full"]+y["full"]+z["full"]} | {x["stale"]} | {y["overgeneralized"]} |')
lines+=['','| Context reference | Old/current route /48 | New-channel route /48 | Full calls /96 |','|---|---:|---:|---:|']
for arm in ['base','explicit-original','explicit-revised','rule-original','rule-revised']:
 x=get(arm,'A-new');y=get(arm,'B-new');lines.append(f'| {arm} | {x["route"]} | {y["route"]} | {x["full"]+y["full"]} |')
(a.analysis/'compact-tables.md').write_text('\n'.join(lines)+'\n')
