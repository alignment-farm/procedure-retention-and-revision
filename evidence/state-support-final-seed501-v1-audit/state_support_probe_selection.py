"""Add directly supported target and off-scope transfer probes to prior audit."""
import json
import maintenance_task as t
from maintenance_probe_selection import select as original_select

def select(rows):
 selected=original_select(rows);seen={json.dumps(r['case'],sort_keys=True) for r in selected}
 predicates=[lambda r: r['case']['entity'] in t.TARGETS and r['case']['stock']==1 and t.oracle(r['case'],1)!=t.oracle(r['case'],0),
             lambda r: r['case']['entity'] in t.TARGETS and r['case']['stock']==1 and t.oracle(r['case'],2)!=t.oracle(r['case'],1)]
 for channel,priority in [('copper','slow'),('violet','fast')]:
  predicates.append(lambda r,c=channel,p=priority: r['case']['channel']==c and r['case']['priority']==p and r['case']['stock']==1 and not r['case']['certified'] and r['case']['entity'] not in t.ACQUIRED+t.TARGETS)
 for predicate in predicates:
  for r in rows:
   if predicate(r):
    key=json.dumps(r['case'],sort_keys=True)
    if key not in seen:selected.append(r);seen.add(key)
    break
 return selected
