import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import maintenance_task as t

class Maintenance(unittest.TestCase):
 def test_environment(self):
  for v in range(3):
   for c in t.cases(['sample']):
    answer=t.oracle(c,v)
    self.assertTrue(t.check(answer,c,v)['complete'])
    for i,opts in enumerate([['PASS','FAIL'],['RESERVE','SKIP'],['SHIP','SKIP'],['0','1'],['SENT','HELD','WAIT']]):
     for o in opts:
      f=answer.split()
      if f[i]==o: continue
      f[i]=o
      self.assertFalse(t.check(' '.join(f),c,v)['complete'],(c,v,f))
 def test_matched_schedules(self):
  for v in [1,2]:
   a=t.schedule('novel',v);b=t.schedule('bridged',v)
   self.assertEqual(len(a),192)
   for (sa,ca),(sb,cb) in zip(a,b):
    self.assertEqual(sa,sb)
    self.assertEqual({k:x for k,x in ca.items() if k!='entity'},{k:x for k,x in cb.items() if k!='entity'})
    self.assertEqual(t.oracle(ca,v),t.oracle(cb,v))
    if sa=='history': self.assertEqual(ca,cb)
    if sa=='correction': self.assertNotEqual(t.oracle(ca,v),t.oracle(ca,v-1))
    else: self.assertEqual(t.oracle(ca,v),t.oracle(ca,v-1))
 def test_stale_is_obligation(self):
  for v in (1,2):
   changed=[c for c in t.cases(t.ACQUIRED) if t.oracle(c,v)!=t.oracle(c,v-1)]
   self.assertEqual(len(changed),8)
   for c in changed:
    self.assertTrue(t.check(t.oracle(c,v-1),c,v)['stale'])
    self.assertFalse(t.check(t.oracle(c,v-1),c,v)['complete'])

class ExplicitPolicy(unittest.TestCase):
 def test_state_conservation_and_revision(self):
  from maintenance_explicit import execute, INITIAL, ADDITIONS
  import copy
  policy=copy.deepcopy(INITIAL)
  for v in range(3):
   if v:policy['eligible_any'].append(ADDITIONS[v-1])
   for c in t.cases(['unseen']):
    raw,trace=execute(c,policy)
    self.assertTrue(t.check(raw,c,v)['complete'])
    for state in trace:
     self.assertEqual(state['stock']+state['reserved']+state['shipped'],c['stock'])
  c=dict(entity='unseen',channel='copper',priority='slow',certified=0,stock=1)
  wrong=copy.deepcopy(policy);wrong['eligible_any'].append({'channel':'copper'})
  raw,_=execute(c,wrong)
  self.assertFalse(t.check(raw,c,2)['complete'])
