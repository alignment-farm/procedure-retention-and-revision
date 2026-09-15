import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import maintenance_task as t

class CrossingSchedule(unittest.TestCase):
 def test_identity_is_only_schedule_difference(self):
  novel=t.schedule('novel',2,64,'negative');bridged=t.schedule('bridged',2,64,'negative')
  self.assertEqual(len(novel),192)
  for (sn,cn),(sb,cb) in zip(novel,bridged):
   self.assertEqual(sn,sb)
   self.assertEqual({k:v for k,v in cn.items() if k!='entity'},{k:v for k,v in cb.items() if k!='entity'})
   self.assertEqual(t.oracle(cn,2),t.oracle(cb,2))
   if sn=='history':self.assertEqual(cn,cb)
  history=[c for s,c in novel if s=='history']
  self.assertEqual(sum(t.oracle(c,1)!=t.oracle(c,0) for c in history),10)
  self.assertTrue(all(t.oracle(c,2)==t.oracle(c,1) for c in history))

class ReloadCoverage(unittest.TestCase):
 def test_direct_target_and_fresh_negative_boundaries(self):
  from state_support_probe_selection import select
  rows=[dict(case=c,version=2,expected=t.oracle(c,2),scores=t.check(t.oracle(c,2),c,2)) for c in t.cases(t.ACQUIRED+t.TARGETS+['fresh'])]
  selected=select(rows)
  for v in [1,2]:
   self.assertTrue(any(r['case']['entity'] in t.TARGETS and r['case']['stock']==1 and t.oracle(r['case'],v)!=t.oracle(r['case'],v-1) for r in selected))
  for channel,priority in [('copper','slow'),('violet','fast')]:
   self.assertTrue(any(r['case']==dict(entity='fresh',channel=channel,priority=priority,certified=0,stock=1) for r in selected))
