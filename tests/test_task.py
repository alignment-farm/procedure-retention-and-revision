import sys,unittest
sys.path.insert(0,'scripts')
from task import *
class Contract(unittest.TestCase):
 def test_scoped_revision(self):
  rows=cases(['az'],('copper','violet','amber','teal'))
  self.assertEqual(sum(oracle(c)!=oracle(c,True) for c in rows),1)
  c=dict(channel='copper',priority='fast',identifier='az')
  self.assertEqual(oracle(c,True),'marten(text="AZ-Q")')
  self.assertTrue(score('kestrel(text="AZ-Q")',c,True)['stale'])
  c['priority']='slow'
  self.assertTrue(score('marten(text="AZ")',c,True)['overgeneralized'])
 def test_component_independence(self):
  c=dict(channel='copper',priority='fast',identifier='az')
  s=score('marten(text="WRONG-Q")',c,True)
  self.assertTrue(s['route']);self.assertTrue(s['suffix']);self.assertFalse(s['identifier']);self.assertFalse(s['full'])
  self.assertFalse(score('marten(text="AZ-Q") trailing',c,True)['route'])
 def test_explicit_evidence_access(self):
  c=cases(['unseen'])[0];text=prompt(c,True,True,clean=True)
  self.assertEqual(text.count(' -> '),32)
  for old in cases(A_WORDS):
   if scope(old):self.assertNotIn(query(old)+' -> ',text)
  for revised in cases(C_WORDS):
   if scope(revised):self.assertIn(query(revised)+' -> '+oracle(revised,True),text)
 def test_no_stale_replay(self):
  replay=[x for x in cases(A_WORDS)+cases(B_WORDS,('amber','teal')) if not scope(x)]
  self.assertEqual(len(replay),28)
  self.assertTrue(all(oracle(c)==oracle(c,True) for c in replay))
  self.assertFalse(set(fresh(2026091417))&set(A_WORDS+B_WORDS+C_WORDS+DEV_WORDS))
if __name__=='__main__':unittest.main()
