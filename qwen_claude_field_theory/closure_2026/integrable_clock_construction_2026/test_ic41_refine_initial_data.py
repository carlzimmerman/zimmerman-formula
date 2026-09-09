import importlib.util
import unittest
import mpmath as mp


class RefinementTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic41_refine_initial_data'))
        return __import__('ic41_refine_initial_data')

    def test_step_solves_coupled_linear_system_without_assigned_rank(self):
        m=self.module()
        with mp.workdps(50):
            fn=lambda x:[2*x[0]+x[1]-5,x[0]-3*x[1]+1]
            out=m.newton_step(fn,[mp.mpf(0),mp.mpf(0)],mp.mpf('1e-12'))
            self.assertLess(abs(out['delta'][0]-2),mp.mpf('1e-35'))
            self.assertLess(abs(out['delta'][1]-1),mp.mpf('1e-35'))
            self.assertLess(abs(out['determinant']+7),mp.mpf('1e-35'))

    def test_singular_response_is_not_reported_as_solved(self):
        m=self.module()
        with mp.workdps(50):
            with self.assertRaises(ZeroDivisionError):
                m.newton_step(lambda x:[x[0]+x[1],2*x[0]+2*x[1]],
                              [mp.mpf(1),mp.mpf(1)],mp.mpf('0.125'))


if __name__=='__main__':unittest.main()
