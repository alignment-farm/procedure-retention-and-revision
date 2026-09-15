"""Whole-phase counts and exact matching of deployed neural/formal use workloads."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import maintenance_task as t

def main():
 p=argparse.ArgumentParser();p.add_argument('--runs',type=Path,nargs='+',required=True);p.add_argument('--final-run',type=Path,required=True);p.add_argument('--formal',type=Path,required=True);p.add_argument('--audits',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 def lines(p):return [json.loads(l) for l in p.read_text().splitlines()]
 def verify(p):
  for line in (p/'SHA256SUMS').read_text().splitlines():
   h,n=line.split('  ',1);assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h
 run_totals=[]
 for path in a.runs:
  verify(path);ev=lines(path/'events.jsonl');rs=lines(path/'responses.jsonl');assert ev[-1]['status']=='complete'
  us=[e for e in ev if e['kind']=='update'];calibration=json.loads((path/'routing-calibration.json').read_text())['responses'] if (path/'routing-calibration.json').exists() else []
  run_totals.append(dict(path=str(path),git=ev[0]['git'],generations=len(rs),calibration_generations=len(calibration),updates=len(us),training_input_tokens=sum(e['input_tokens'] for e in us),training_loss_tokens=sum(e['loss_tokens'] for e in us),inference_prompt_tokens=sum(r['prompt_tokens'] for r in rs+calibration),inference_completion_tokens=sum(r['completion_tokens'] for r in rs+calibration),wall_seconds=ev[-1]['wall_seconds'],wait_seconds=ev[-1]['wait_seconds'],active_seconds=ev[-1]['wall_seconds']-ev[-1]['wait_seconds'],peak_mlx_bytes=ev[-1]['peak_mlx_bytes'],acquisition_attempts=[dict(state=e['state'],passed=e['passed'],recall=e['recall']['complete'],recall_n=e['recall']['n'],transfer=e['transfer']['complete'],transfer_n=e['transfer']['n']) for e in ev if e['kind']=='acquisition_criterion']))
 verify(a.formal);formal=lines(a.formal/'responses.jsonl');rs=lines(a.final_run/'responses.jsonl');design=json.loads((a.final_run/'design.json').read_text())
 def key(r):return (r['version'],r['repeat'],json.dumps(r['case'],sort_keys=True))
 fk=[key(r) for r in formal];assert len(set(fk))==len(fk)
 for r in formal:assert t.check(r['raw'],r['case'],r['version'])['complete']
 comparisons=[]
 for seed in design['seeds']:
  for arm in ['novel','bridged']:
   trajectory=[r for r in rs if (r['state']==f'seed{seed}-no-update' and r['version']==0) or r['state'].startswith(f'seed{seed}-{arm}-v')]
   if not trajectory:continue
   assert sorted(key(r) for r in trajectory)==sorted(fk)
   comparisons.append(dict(seed=seed,arm=arm,calls=len(trajectory),complete=sum(r['scores']['complete'] for r in trajectory),formal_complete=len(formal),identical_inputs=True))
 audits=[]
 for path in a.audits:
  verify(path);d=json.loads((path/'audit.json').read_text());audits.append(dict(path=str(path),rows_verified=d['rows_verified'],updates_verified=d['updates_verified'],reload_probes=len(d['probes']),calibration_rows_verified=d['calibration_rows_verified'],calibration_probes=len(d['calibration_probes']),seconds=d['seconds'],wait_seconds=d['wait_seconds']))
 assert sum(d['rows_verified'] for d in audits)==sum(d['generations'] for d in run_totals)
 assert sum(d['calibration_rows_verified'] for d in audits)==sum(d['calibration_generations'] for d in run_totals)
 assert sum(d['updates_verified'] for d in audits)==sum(d['updates'] for d in run_totals)
 report=dict(git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),runs=run_totals,audits=audits,matched_workloads=comparisons,formal=json.loads((a.formal/'summary.json').read_text()),totals={k:sum(d[k] for d in run_totals) for k in ['generations','calibration_generations','updates','training_input_tokens','training_loss_tokens','inference_prompt_tokens','inference_completion_tokens','wall_seconds','wait_seconds','active_seconds']})
 (a.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 for name in ['maintenance_phase_audit.py','maintenance_task.py']:(a.output/name).write_bytes(Path('scripts',name).read_bytes())
 (a.output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
 print(json.dumps(report,indent=2))

if __name__=='__main__':main()
