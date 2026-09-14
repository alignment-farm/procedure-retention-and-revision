import sys
import unittest
sys.path.insert(0, 'scripts')
from scope_task import *

class ScopeContract(unittest.TestCase):
    def test_routing_survives_argument_syntax_failure(self):
        c = TARGETS[0]
        s = components('marten(text="BROKEN', c)
        self.assertTrue(s['route'])
        self.assertFalse(s['format'])
        self.assertFalse(s['strict_route'])
        self.assertFalse(components('martenish(text="X")', c)['tool_known'])
        self.assertFalse(components('I choose marten', c)['tool_known'])
        self.assertTrue(components('kestrel(text="BROKEN', c)['stale'])
        self.assertTrue(components('marten(text="BROKEN', NARROW[0])['overgeneralized'])

    def test_matched_boundary_schedule(self):
        rows = schedule(128)
        self.assertEqual(len(rows), 128)
        self.assertTrue(all(scope(t) and not scope(n) and not scope(b) for t, n, b in rows))
        self.assertTrue(all((n['channel'], n['priority']) == (b['channel'], b['priority']) for _, n, b in rows))
        self.assertTrue(all(n == b for _, n, b in rows[:7]))
        key = lambda c: tuple(sorted(c.items()))
        self.assertEqual({key(n) for _, n, _ in rows}, {key(c) for c in NARROW})
        self.assertEqual({key(b) for _, _, b in rows[:28]}, {key(c) for c in BROAD})

    def test_crossed_boundary_and_matched_history(self):
        from task import oracle
        self.assertEqual(len(BOUNDARY),7)
        self.assertEqual({c['identifier'] for c in BOUNDARY},{TARGETS[0]['identifier']})
        self.assertTrue(all(oracle(c)==oracle(c,True) for c in BOUNDARY))
        for t,n,b in schedule(128):
            left=block_updates('boundary-repeat',t,n,b)
            right=block_updates('boundary-history',t,n,b)
            self.assertEqual(len(left),3)
            self.assertEqual(left[:2],right[:2])
            self.assertEqual(left[2][1]['channel'],right[2][1]['channel'])
            self.assertEqual(left[2][1]['priority'],right[2][1]['priority'])

if __name__ == '__main__': unittest.main()
