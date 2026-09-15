"""Aggregate the complete follow-up attempt ledger without dropping failed endpoints."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
assert not a.output.exists()
names=['scope-development-v1','scope-acquisition-v1','scope-boundary-diagnosis-v1',
       'scope-acquisition-repair-v1','scope-final-v1']
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
runs={};hashes=set()
for name in names:
    path=Path('evidence')/name
    events=[json.loads(l) for l in (path/'events.jsonl').read_text().splitlines()]
    rows=[json.loads(l) for l in (path/'responses.jsonl').read_text().splitlines()]
    updates=[e for e in events if e['kind']=='update'];end=events[-1]
    assert end['kind']=='complete' and end['status']=='complete'
    audited=json.loads(path.with_name(name+'-analysis').joinpath('audit.json').read_text())
    assert len(rows)==audited['response_records'] and len(updates)==audited['updates']
    checkpoints=list(path.glob('*.safetensors'));hashes.update(sha(p) for p in checkpoints)
    by_source={}
    for source in sorted({u['source'] for u in updates}):
        us=[u for u in updates if u['source']==source]
        by_source[source]=dict(updates=len(us),**{k:sum(u[k] for u in us) for k in ['seconds','input_tokens','loss_tokens']})
    runs[name]=dict(execution_revision=events[0]['git'],manifest_sha256=sha(path/'SHA256SUMS'),
        updates=len(updates),generations=len(rows),checkpoint_files=len(checkpoints),
        checkpoint_bytes=sum(p.stat().st_size for p in checkpoints),
        elapsed_seconds=end['seconds'],wait_seconds=end['resource_wait_seconds'],
        active_seconds=end['seconds']-end['resource_wait_seconds'],peak_mlx_bytes=end['peak_mlx_bytes'],
        training_seconds=sum(u['seconds'] for u in updates),training_input_tokens=sum(u['input_tokens'] for u in updates),
        answer_tokens=sum(u['loss_tokens'] for u in updates),generation_seconds=sum(r['seconds'] for r in rows),
        prompt_tokens=sum(r['prompt_tokens'] for r in rows),completion_tokens=sum(r['completion_tokens'] for r in rows),
        at_limit=sum(r['at_limit'] for r in rows),by_source=by_source)
keys=['updates','generations','checkpoint_files','checkpoint_bytes','elapsed_seconds','wait_seconds','active_seconds',
      'training_seconds','training_input_tokens','answer_tokens','generation_seconds','prompt_tokens','completion_tokens','at_limit']
totals={k:sum(v[k] for v in runs.values()) for k in keys}
totals['unique_checkpoint_hashes']=len(hashes)
result=dict(git_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),runs=runs,totals=totals,
    note='Experimental runs only; reload-audit generations are separate. Duplicated carried states are counted as files, not independent acquisitions. The failed B32 and every early correction endpoint remain included. Inherited acquisition/B preparation costs belong to the accepted source ledger. No energy, investigator-time, or repayment estimate.')
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
