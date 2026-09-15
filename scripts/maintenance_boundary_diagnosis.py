"""One bounded matched-budget diagnostic, using acquired development weights."""
import argparse,json,os,subprocess,time
from pathlib import Path
import mlx.core as mx
from runtime import Runtime,resource,sha,digest
import maintenance_task as t

def main():
 p=argparse.ArgumentParser();p.add_argument('start_run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();wait=0.;last=0.;status='failed'
 for n in ['maintenance_boundary_diagnosis.py','maintenance_task.py','runtime.py']:(out/n).write_bytes(Path('scripts',n).read_bytes())
 (out/'protocol.md').write_bytes(Path('protocol/maintenance-boundary-diagnosis-v1.md').read_bytes())
 def save(n,d):(out/n).write_text(json.dumps(d,indent=2)+'\n')
 ev=(out/'events.jsonl').open('x');rs=(out/'responses.jsonl').open('x')
 def emit(kind,**d):ev.write(json.dumps(dict(kind=kind,elapsed=time.monotonic()-start,**d))+'\n');ev.flush()
 def guard():
  nonlocal wait,last
  if time.monotonic()-last>5:
   while True:
    ps=subprocess.check_output(['ps','-axo','pid,etime,rss,command'],text=True).splitlines()
    jobs=[l for l in ps if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0])!=os.getpid()]
    emit('resource_check',jobs=jobs)
    if not jobs:break
    tick=time.monotonic();time.sleep(10);wait+=time.monotonic()-tick;assert wait<7200
   last=time.monotonic()
  assert time.monotonic()-start-wait<3600 and mx.get_peak_memory()<40e9
 save('design.json',dict(phase='boundary-diagnosis',seeds=[311],blocks=64,boundary_mode='negative',fresh=t.DEV,acquired=t.ACQUIRED,targets=t.TARGETS))
 try:
  emit('revision',git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),dirty=subprocess.check_output(['git','status','--short'],text=True))
  guard()
  for line in (a.start_run/'SHA256SUMS').read_text().splitlines():
   h,n=line.split('  ',1);assert sha(a.start_run/n)==h
  save('resource.json',resource());rt=Runtime();path=a.start_run/'seed311-A256.safetensors';acquired=list(mx.load(str(path)).items());rt.restore(acquired)
  emit('reused_acquisition',path=str(path),sha256=sha(path),state_hash=digest(rt.snapshot()))
  def evaluate(state,v):
   counts={};n=0
   for c in t.cases(t.ACQUIRED+t.TARGETS+t.DEV):
    guard();prefix=rt.encode(t.prompt(c));r=rt.generate(prefix,limit=40);scores=t.check(r['raw'],c,v);n+=1
    for k,value in scores.items():counts[k]=counts.get(k,0)+int(value)
    rs.write(json.dumps(dict(state=state,version=v,repeat=0,case=c,rule=False,prefix=prefix,expected=t.oracle(c,v),scores=scores,**r))+'\n');rs.flush()
   summary=dict(n=n,**counts);emit('evaluation',state=state,version=v,repeat=0,summary=summary);print(state,summary,flush=True)
  evaluate('seed311-no-update',0)
  for arm in ['novel','bridged']:
   rt.restore(acquired);name=f'seed311-{arm}-v1';emit('paired_start',state=f'seed311-{arm}',state_hash=digest(rt.snapshot()));opt=rt.optimizer()
   emit('maintenance',state=name,scanned=64,excluded=8,authority='investigator')
   for i,(source,c) in enumerate(t.schedule(arm,1,64,'negative'),1):
    guard();prefix=rt.encode(t.prompt(c));y=rt.target(prefix,t.oracle(c,1));emit('update',state=name,index=i,source=source,case=c,version=1,**rt.step(prefix,y,opt))
   path=out/(name+'.safetensors');mx.save_safetensors(str(path),dict(rt.snapshot()));emit('checkpoint',state=name,sha256=sha(path),state_hash=digest(rt.snapshot()),bytes=path.stat().st_size)
   evaluate(name,1)
  emit('invariants',seed=311,**rt.invariants());status='complete'
 finally:
  emit('finish',status=status,wall_seconds=time.monotonic()-start,wait_seconds=wait,peak_mlx_bytes=mx.get_peak_memory());ev.close();rs.close()
  (out/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))

if __name__=='__main__':main()
