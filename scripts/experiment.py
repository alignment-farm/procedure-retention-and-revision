"""Bounded sequential CE adaptation; raw generations, all attempts and checkpoints."""
import argparse,json,time,random,subprocess,os
from pathlib import Path
import mlx.core as mx
from runtime import Runtime,resource,sha,digest
from task import *
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',choices=['development','final'],default='development');a=p.parse_args()
out=a.output;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
for name in ['experiment.py','runtime.py','task.py']:(out/name).write_bytes(Path('scripts',name).read_bytes())
(out/'protocol.md').write_bytes(Path('protocol',a.phase+'-v1.md').read_bytes())
ev=(out/'events.jsonl').open('x');responses=(out/'responses.jsonl').open('x')
def save(name,data):(out/name).write_text(json.dumps(data,indent=2))
def emit(kind,**d):ev.write(json.dumps(dict(kind=kind,elapsed=time.monotonic()-start,**d))+'\n');ev.flush()
def processes():return subprocess.check_output(['ps','-axo','pid,etime,command'],text=True)
last_resource_check=0.
wait_seconds=0.
def check():
 global last_resource_check,wait_seconds
 now=time.monotonic()
 if now-last_resource_check>5:
  while True:
   active=[line for line in processes().splitlines() if '/bin/python' in line and ('scripts/experiment.py' in line or 'scripts/run_confirmatory.py' in line) and int(line.split()[0])!=os.getpid()]
   if not active:break
   emit('resource_wait',jobs=active);before=time.monotonic();time.sleep(15);wait_seconds+=time.monotonic()-before
   assert wait_seconds<3600,'one-hour resource wait ceiling'
  last_resource_check=time.monotonic()
 assert time.monotonic()-start-wait_seconds<(1800 if a.phase=='final' else 1200),'active execution budget'
 assert mx.get_peak_memory()<40e9,'40 GB ceiling'
words=DEV_WORDS if a.phase=='development' else fresh(2026091417,12)
if a.phase=='final':assert not set(words)&set(json.loads(Path('sources/prior-evaluation-identifiers.json').read_text()))
save('design.json',dict(phase=a.phase,evaluation_seed=2026091417 if a.phase=='final' else None,words=words,A=cases(A_WORDS),B=cases(B_WORDS,('amber','teal')),C=[c for c in cases(C_WORDS) if scope(c)]))
status='failed'
try:
 check();(out/'processes-before.txt').write_text(processes());save('resource.json',resource());emit('revision',git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
 rt=Runtime();base=rt.snapshot()
 def evaluate(arm,revised=False,evidence=False,rules=False):
  suites=[('A-recall',cases(A_WORDS)),('B-recall',cases(B_WORDS,('amber','teal'))),('C-recall',[c for c in cases(C_WORDS) if scope(c)]),('A-new',cases(words)),('B-new',cases(words,('amber','teal')))]
  summary={}
  for suite,cs in suites:
   counts={k:0 for k in score('',cs[0])}
   for i,c in enumerate(cs):
    check();prefix=rt.encode(prompt(c,evidence,revised,clean=a.phase=='final',rules=rules));r=rt.generate(prefix);s=score(r['raw'],c,revised)
    for k,v in s.items():counts[k]+=int(v)
    responses.write(json.dumps(dict(arm=arm,suite=suite,index=i,case=c,revised=revised,evidence=evidence,clean_evidence=a.phase=='final',rules=rules,prefix=prefix,expected=oracle(c,revised),scores=s,**r))+'\n');responses.flush()
   summary[suite]=dict(n=len(cs),**counts)
  emit('evaluation',arm=arm,summary=summary);print(arm,{s:(d['route'],d['full'],d['n']) for s,d in summary.items()},flush=True)
 def train(arm,initial,targets,replay,revised,double=False):
  rt.restore(initial);opt=rt.optimizer();rng=random.Random(73);order=[];replay_order=[]
  while len(order)<128:
   indices=list(range(len(targets)));rng.shuffle(indices);order+=indices
  while replay and len(replay_order)<128:
   indices=list(range(len(replay)));rng.shuffle(indices);replay_order+=indices
  emit('training_start',arm=arm,initial_hash=digest(rt.snapshot()),targets=targets,replay=replay,order=order[:128],replay_order=replay_order[:128],revised=revised,double=double)
  for step,index in enumerate(order[:128],1):
   for source,c in [('target',targets[index])]+([('repeat',targets[index])] if double else [])+([('replay',replay[replay_order[step-1]])] if replay else []):
    check();prefix=rt.encode(prompt(c));y=rt.target(prefix,oracle(c,revised));r=rt.step(prefix,y,opt);emit('update',arm=arm,step=step,source=source,case=c,**r)
   if step==128 or (step==32 and (a.phase=='development' or arm.endswith('-only'))):
    checkpoint=f'{arm}-{step}.safetensors';mx.save_safetensors(str(out/checkpoint),dict(rt.snapshot()));evaluate(f'{arm}-{step}',revised)
  emit('training_complete',arm=arm,**rt.invariants());return rt.snapshot()
 evaluate('base')
 methods=['ce'] if a.phase=='development' else ['ce','forward']
 for method in methods:
  checkpoint=Path('sources/checkpoints',f'acquired-{method}128.safetensors');acquired=list(mx.load(str(checkpoint)).items());rt.restore(acquired)
  emit('acquired',method=method,checkpoint_sha256=sha(checkpoint),state_hash=digest(rt.snapshot()));evaluate(method+'-acquired')
  b=cases(B_WORDS,('amber','teal'));old=cases(A_WORDS);c=[x for x in cases(C_WORDS) if scope(x)]
  train(method+'-B-only',acquired,b,[],False)
  if a.phase=='final':train(method+'-B-double',acquired,b,[],False,double=True)
  retained=train(method+'-B-replay',acquired,b,old,False)
  train(method+'-C-only',retained,c,[],True)
  if a.phase=='final':train(method+'-C-double',retained,c,[],True,double=True)
  train(method+'-C-replay',retained,c,[x for x in old+b if not scope(x)],True)
 rt.restore(base);evaluate('explicit-original',evidence=True);evaluate('explicit-revised',revised=True,evidence=True)
 if a.phase=='final':evaluate('rule-original',rules=True);evaluate('rule-revised',revised=True,rules=True)
 status='complete'
finally:
 (out/'processes-after.txt').write_text(processes());emit('complete',status=status,seconds=time.monotonic()-start,resource_wait_seconds=wait_seconds,peak_mlx_bytes=mx.get_peak_memory());ev.close();responses.close()
 (out/'SHA256SUMS').write_text('\n'.join(sha(f)+'  '+f.name for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
