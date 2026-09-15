"""Factor inherited revision-1 weights from current revision-2 evidence."""
import argparse,json,os,subprocess,time
from pathlib import Path
import mlx.core as mx
from runtime import Runtime,resource,sha,digest
import maintenance_task as t

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--start-run',type=Path,default=Path('evidence/maintenance-final-v1'));p.add_argument('--seed',type=int,default=401);a=p.parse_args()
 out=a.output;out.mkdir(parents=True,exist_ok=False);start=time.monotonic();wait=0.;last=0.;status='failed'
 for n in ['state_support_experiment.py','maintenance_task.py','runtime.py']:(out/n).write_bytes(Path('scripts',n).read_bytes())
 (out/'protocol.md').write_bytes(Path('protocol/state-support-development-v1.md').read_bytes())
 ev=(out/'events.jsonl').open('x');rs=(out/'responses.jsonl').open('x')
 def save(n,d):(out/n).write_text(json.dumps(d,indent=2)+'\n')
 def emit(kind,**d):ev.write(json.dumps(dict(kind=kind,elapsed=time.monotonic()-start,**d))+'\n');ev.flush()
 def guard():
  nonlocal wait,last
  if time.monotonic()-last>5:
   while True:
    lines=subprocess.check_output(['ps','-axo','pid,etime,rss,command'],text=True).splitlines()
    jobs=[l for l in lines if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0])!=os.getpid()]
    emit('resource_check',jobs=jobs)
    if not jobs:break
    tick=time.monotonic();time.sleep(10);wait+=time.monotonic()-tick;assert wait<7200
   last=time.monotonic()
  assert time.monotonic()-start-wait<3600 and mx.get_peak_memory()<40e9
 try:
  emit('revision',git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),dirty=subprocess.check_output(['git','status','--short'],text=True))
  for line in (a.start_run/'SHA256SUMS').read_text().splitlines():
   h,n=line.split('  ',1);assert sha(a.start_run/n)==h,n
  design=json.loads((a.start_run/'design.json').read_text());entities=t.ACQUIRED+t.TARGETS+design['fresh']
  save('design.json',dict(seed=a.seed,entities=entities,start_run=str(a.start_run),blocks=64,boundary_mode='negative',phase='diagnostic'))
  old=[json.loads(l) for l in (a.start_run/'responses.jsonl').read_text().splitlines()]
  def published(arm,v):return {json.dumps(r['case'],sort_keys=True):r['raw'] for r in old if r['state']==f'seed{a.seed}-{arm}-v{v}' and r['repeat']==0}
  guard();save('resource.json',resource());rt=Runtime()
  def evaluate(state,v,reference=None):
   counts={};raws={}
   for c in t.cases(entities):
    guard();prefix=rt.encode(t.prompt(c));r=rt.generate(prefix,limit=40);scores=t.check(r['raw'],c,v)
    for k,value in scores.items():counts[k]=counts.get(k,0)+int(value)
    raws[json.dumps(c,sort_keys=True)]=r['raw']
    rs.write(json.dumps(dict(state=state,version=v,repeat=0,case=c,prefix=prefix,scores=scores,**r))+'\n');rs.flush()
   emit('evaluation',state=state,summary=dict(n=len(raws),**counts));print(state,counts['complete'],len(raws),flush=True)
   if reference is not None:
    diffs=[k for k in raws if raws[k]!=reference.get(k)];emit('reproduction',state=state,differences=diffs);assert not diffs,(state,diffs)
  for inherited in ['novel','bridged']:
   path=a.start_run/f'seed{a.seed}-{inherited}-v1.safetensors';weights=list(mx.load(str(path)).items());rt.restore(weights)
   emit('reused_state',inherited=inherited,path=str(path),sha256=sha(path),bytes=path.stat().st_size,state_hash=digest(rt.snapshot()))
   evaluate(inherited+'-start',1,published(inherited,1))
   for support in ['novel','bridged']:
    rt.restore(weights);name=inherited+'--'+support;opt=rt.optimizer();emit('paired_start',state=name,inherited=inherited,support=support,state_hash=digest(rt.snapshot()))
    for i,(source,c) in enumerate(t.schedule(support,2,64,'negative'),1):
     guard();prefix=rt.encode(t.prompt(c));y=rt.target(prefix,t.oracle(c,2));emit('update',state=name,index=i,source=source,case=c,version=2,**rt.step(prefix,y,opt))
    path=out/(name+'.safetensors');mx.save_safetensors(str(path),dict(rt.snapshot()));h=sha(path)
    emit('checkpoint',state=name,sha256=h,state_hash=digest(rt.snapshot()),bytes=path.stat().st_size)
    evaluate(name,2,published(inherited,2) if inherited==support else None)
    if inherited==support:
     same=h==sha(a.start_run/f'seed{a.seed}-{inherited}-v2.safetensors');emit('diagonal_checkpoint',state=name,identical=same);assert same
  emit('invariants',**rt.invariants());status='complete'
 finally:
  emit('finish',status=status,wall_seconds=time.monotonic()-start,wait_seconds=wait,peak_mlx_bytes=mx.get_peak_memory());ev.close();rs.close()
  (out/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
if __name__=='__main__':main()
