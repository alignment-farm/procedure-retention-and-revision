"""Compact publication tables from audited follow-up summaries."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args()
analysis=a.run.with_name(a.run.name+'-analysis')
design=json.loads((a.run/'design.json').read_text())
summary=json.loads((analysis/'summary.json').read_text())
paired=json.loads((analysis/'paired.json').read_text())
costs=json.loads((analysis/'costs.json').read_text())
primary=design['blocks']
lines=['# Fresh scope and rehearsal comparison','',f'Primary endpoint: {primary} target blocks. Counts are conditional on this workload.', '',
'| Start | Treatment | Scope route /12 | Unchanged route /84 | Stale /12 | Overbroad /12 | Full /96 |',
'|---|---|---:|---:|---:|---:|---:|']
for start in design['starts']:
 for treatment in ['before',*design['arms']]:
  name=start+'-'+treatment+('' if treatment=='before' else '-'+str(primary))
  g=summary[name]['groups']
  lines.append(f"| {start} | {treatment} | {g['scope']['route']} | {g['unchanged']['route']} | {g['scope']['stale']} | {g['other_old']['overgeneralized']} | {g['all']['full']} |")
lines += ['','## Complete-call preservation on the same 84 unchanged inputs','',
'| Start | Treatment | Before | After | Lost | Gained | Format /96 | Identifier /96 | Suffix /96 |',
'|---|---|---:|---:|---:|---:|---:|---:|---:|']
for start in design['starts']:
 for mode in ['boundary-repeat','boundary-history']:
  name=f'{start}-{mode}-{primary}'; pair=paired[name]['full'];g=summary[name]['groups']['all']
  lines.append(f"| {start} | {mode} | {pair['before']} | {pair['after']} | {pair['lost']} | {pair['gained']} | {g['format']} | {g['identifier']} | {g['suffix']} |")
lines += ['','## Update costs by source','',
'| Start/treatment | Source | Updates | Unique cases | Input tokens | Answer tokens | Seconds |',
'|---|---|---:|---:|---:|---:|---:|']
for arm,by_source in costs.items():
 for source,d in by_source.items():
  lines.append(f"| {arm} | {source} | {d['updates']} | {d['unique_cases']} | {d['input_tokens']} | {d['loss_tokens']} | {d['seconds']:.2f} |")
(analysis/'compact-tables.md').write_text('\n'.join(lines)+'\n')
print(analysis/'compact-tables.md')
