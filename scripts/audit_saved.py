"""Separate-process persistence and token audit; replays are excluded from scores."""
import argparse,json,hashlib,sys,time,importlib.util,subprocess
from pathlib import Path
import mlx.core as mx
from runtime import Runtime,sha
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();out=a.run.with_name(a.run.name+'-audit');out.mkdir(exist_ok=False)
for line in (a.run/'SHA256SUMS').read_text().splitlines():
 h,name=line.split('  ',1);assert sha(a.run/name)==h
rows=[json.loads(x) for x in (a.run/'responses.jsonl').read_text().splitlines()]
spec=importlib.util.spec_from_file_location('saved_task',a.run/'task.py');task=importlib.util.module_from_spec(spec);spec.loader.exec_module(task)
rt=Runtime();start=time.monotonic();checks=[]
max_target_tokens=0
for r in rows:
 target_tokens=len(rt.target(r['prefix'],r['expected']));max_target_tokens=max(max_target_tokens,target_tokens);assert target_tokens<=48
 kwargs={'clean':r['clean_evidence']} if 'clean_evidence' in r else {}
 if 'rules' in r:kwargs['rules']=r['rules']
 assert rt.encode(task.prompt(r['case'],r['evidence'],r['revised'],**kwargs))==r['prefix']
 ids=r['ids'];assert rt.tokenizer.decode(ids[:-1] if r['ended'] else ids)==r['raw']
 assert len(ids)==r['completion_tokens'] and len(r['prefix'])==r['prompt_tokens']
 if r['ended']:assert ids[-1] in rt.tokenizer.eos_token_ids
for checkpoint in sorted(a.run.glob('*.safetensors')):
 arm=checkpoint.stem;rt.restore(list(mx.load(str(checkpoint)).items()))
 selected=[next(r for r in rows if r['arm']==arm and r['suite']==suite and r['index']==index) for suite,index in [('A-recall',0),('A-recall',1),('B-new',0)]]
 for r in selected:
  gen=rt.generate(r['prefix']);assert gen['ids']==r['ids'],(arm,r['suite'],r['index'])
  checks.append(dict(arm=arm,suite=r['suite'],index=r['index'],ids=gen['ids'],exact=True))
prior=json.loads(Path('sources/checkpoints/recall.json').read_text());inherited=[]
for r in rows:
 if r['arm'].endswith('-acquired') and r['suite']=='A-recall':
  method=r['arm'].split('-')[0];old=next(x for x in prior if x['arm']==method+'-0.0005' and x['case']==r['case']);assert old['ids']==r['ids'];inherited.append(dict(arm=r['arm'],index=r['index'],exact=True))
result=dict(audit_git_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),audit_script_sha256=sha(__file__),token_records=len(rows),max_canonical_answer_tokens=max_target_tokens,generation_limit=48,reload_checks=checks,inherited_acquisition_replays=inherited,seconds=time.monotonic()-start)
(out/'audit.json').write_text(json.dumps(result,indent=2));print(dict(token_records=len(rows),reload_checks=len(checks),inherited_replays=len(inherited)))
