"""Record visible shared-hardware activity; observational, no scheduler or lock."""
import subprocess,time,json,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--seconds',type=int,default=1200);a=p.parse_args()
with a.output.open('x') as f:
 for _ in range(a.seconds//15):
  s=subprocess.check_output(['ps','-axo','pid,etime,command'],text=True)
  lines=[l for l in s.splitlines() if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l]
  f.write(json.dumps(dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),jobs=lines))+'\n');f.flush()
  if not lines:break
  time.sleep(15)
