"""CPU-only completion-limit diagnosis and remaining development token-cost check."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from transformers import AutoTokenizer
from task import prompt, oracle

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
assert not a.output.exists()
tokenizer=AutoTokenizer.from_pretrained('models/qwen3-4b-instruct')
def encode(c):return tokenizer.apply_chat_template([dict(role='user',content=prompt(c))],tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=False)
dev=Path('evidence/scope-development-v1')
dev_rows=[json.loads(l) for l in (dev/'responses.jsonl').read_text().splitlines()]
for r in dev_rows:assert encode(r['case'])==r['prefix']
updates=[json.loads(l) for l in (dev/'events.jsonl').read_text().splitlines() if json.loads(l)['kind']=='update']
for e in updates:
    prefix=encode(e['case']);y=tokenizer.encode(oracle(e['case'],True),add_special_tokens=False)+[tokenizer.eos_token_id]
    assert e['input_tokens']==len(prefix)+len(y)-1 and e['loss_tokens']==len(y)
rows=[json.loads(l) for l in Path('evidence/scope-final-v1/responses.jsonl').read_text().splitlines()]
capped=[r for r in rows if r['at_limit']]
checks=[]
for r in capped:
    divergent=not r['expected'].startswith(r['raw'].lstrip())
    assert divergent and not r['scores']['full']
    checks.append(dict(arm=r['arm'],suite=r['suite'],index=r['index'],prefix_already_diverged=divergent,raw=r['raw'],expected=r['expected']))
unknown=[dict(arm=r['arm'],suite=r['suite'],index=r['index'],raw=r['raw']) for r in rows if not r['scores']['tool_known']]
result=dict(git_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    development_response_prefix_checks=len(dev_rows),development_training_token_checks=len(updates),
    final_limit=48,capped_generations=len(capped),capped_by_arm=dict(Counter(r['arm'] for r in capped)),
    capped_full_correct=sum(r['scores']['full'] for r in capped),capped_syntactically_valid=sum(r['scores']['format'] for r in capped),
    capped_tool_known=sum(r['scores']['tool_known'] for r in capped),capped_checks=checks,unknown_tool_records=unknown,
    interpretation='Every capped prefix already differs from the canonical answer; appending tokens cannot repair its exact-call score. This does not claim the decoder would never stop or recover in a different interaction. No longer-budget generations were selected or added.')
a.output.write_text(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if k not in ('capped_checks','unknown_tool_records')})
