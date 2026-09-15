"""Separate single-trajectory deployment accounting from experimental work."""
import argparse,json,hashlib,inspect,subprocess
from collections import Counter
from pathlib import Path
import maintenance_task as t
from maintenance_explicit import execute

def main():
 p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 events=[json.loads(l) for l in (a.run/'events.jsonl').read_text().splitlines()]
 rows=[json.loads(l) for l in (a.run/'responses.jsonl').read_text().splitlines()]
 design=json.loads((a.run/'design.json').read_text())
 def training(us):return dict(updates=len(us),input_tokens=sum(u['input_tokens'] for u in us),loss_tokens=sum(u['loss_tokens'] for u in us),seconds=sum(u['seconds'] for u in us),sources=dict(Counter(u['source'] for u in us)))
 def inference(rs):return dict(calls=len(rs),complete=sum(r['scores']['complete'] for r in rs),prompt_tokens=sum(r['prompt_tokens'] for r in rs),completion_tokens=sum(r['completion_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs))
 trajectories=[]
 for seed in design['seeds']:
  name=f'seed{seed}';acq=[e for e in events if e['kind']=='update' and e['state']==name+'-acquisition']
  validation=[r for r in rows if r['state'].startswith(name+'-A')]
  for arm in ['novel','bridged']:
   update=[e for e in events if e['kind']=='update' and e['state'].startswith(name+'-'+arm+'-v')]
   if not update:continue
   calls=[r for r in rows if (r['state']==name+'-no-update' and r['version']==0) or r['state'].startswith(name+'-'+arm+'-v')]
   cps=[e for e in events if e['kind']=='checkpoint' and e['state'].startswith(name+'-'+arm+'-v')]
   archive={}
   for e in acq+update:
    record=dict(case=e['case'],target=t.oracle(e['case'],e['version']))
    archive[json.dumps(record,sort_keys=True)]=record
   data=json.dumps(list(archive.values()),indent=2)+'\n';archive_name=name+'-'+arm+'-training-archive.json';(a.output/archive_name).write_text(data)
   trajectories.append(dict(seed=seed,arm=arm,acquisition=training(acq),acquisition_validation=inference(validation),revision_training=training(update),recurring_use=inference(calls),
      current_adapter_bytes=cps[-1]['bytes'],training_archive_records=len(archive),training_archive_bytes=len(data.encode()),training_archive_file=archive_name,
      history_records_scanned=128,obsolete_records_excluded=16,prior_revision_records_relabelled=8,
      correction_label_updates=sum(u['source']=='correction' for u in update),boundary_updates=sum(u['source']=='boundary' for u in update),rehearsal_updates=sum(u['source']=='history' for u in update)))
 model_path=Path('models/qwen3-4b-instruct')
 result=dict(git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),trajectories=trajectories,
   experimental_training=training([e for e in events if e['kind']=='update']),experimental_inference=inference(rows),
   finish=events[-1],base_weight_bytes=sum(p.stat().st_size for p in model_path.glob('*.safetensors')),
   interpreter_function_bytes=len(inspect.getsource(execute).encode()),paid_experimental_model_calls=0,
   accounting_notes=['A deployed candidate is one seed/arm trajectory; shared acquisitions are attributed to each candidate but counted once in experiment totals.',
    'Recurring use includes two passes at each of versions 0, 1 and 2; duplicate deterministic calls are use events, not independent statistical samples.',
    'Initial acquisition validation is charged separately; base diagnostics and other references are experimental-only.',
    'Archive is an explicit serialization of all unique case/target pairs actually trained on, including obsolete labels. It is a disclosed sufficient representation, not a minimal storage lower bound.',
    '128 scans and 16 exclusions are investigator-known validity operations across two revisions; eight earlier acquired labels are supplied in revised form at the second revision.',
    'Formal-policy construction, correction authority, assistant orchestration and electricity are unpriced; zero paid experimental calls is not zero research cost.',
    'Wall times are observational on shared hardware. Training/inference times exclude recorded resource waits; they do not include every setup/verification overhead.'])
 (a.output/'costs.json').write_text(json.dumps(result,indent=2)+'\n')
 for name in ['maintenance_costs.py','maintenance_task.py','maintenance_explicit.py']:(a.output/name).write_bytes(Path('scripts',name).read_bytes())
 (a.output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
 print(json.dumps(trajectories,indent=2))

if __name__=='__main__':main()
