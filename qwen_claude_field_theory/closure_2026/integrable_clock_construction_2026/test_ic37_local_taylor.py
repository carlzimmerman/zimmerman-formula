"""Local analytic continuation tests; numerical fitting is not a Taylor proof."""
import importlib.util
import unittest
import mpmath as mp


class LocalTaylorTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic37_local_taylor'))
        return __import__('ic37_local_taylor')

    def test_ode_recurrence_on_hand_solved_equation(self):
        m=self.module()
        # y'=r+y, y(0)=1 gives y=2 exp(r)-r-1.
        with mp.workdps(50):
            coeff=m.ode_series(lambda r,y:[r+y[0]],mp.mpf(0),[mp.mpf(1)],6)
            want=[mp.mpf(1),mp.mpf(1),mp.mpf(1),mp.mpf(1)/3,mp.mpf(1)/12,mp.mpf(1)/60,mp.mpf(1)/360]
            for got,expected in zip(coeff[0],want):self.assertLess(abs(got-expected),mp.mpf('1e-45'))

    def test_local_field_rhs_matches_independent_float_first_jet(self):
        m=self.module()
        out=m.rhs_audit()
        self.assertLess(out['max_relative_rhs_error'],1e-9)
        self.assertLess(out['max_initial_constraint'],1e-30)

    def test_high_precision_boundary_elimination_retains_next_jet(self):
        m=self.module()
        self.assertTrue(callable(getattr(m,'boundary_from_coefficients',None)))
        with mp.workdps(50):
            zero=[mp.mpf(0)]*4;one=[mp.mpf(1),*zero[1:]]
            out=m.boundary_from_coefficients([zero,zero,one],[one,zero,zero],zero,[0,0,1,0],3)
            for got,want in zip(out['edge_jets'],[0,0,2,0]):self.assertLess(abs(got-want),mp.mpf('1e-40'))

    def test_field_curvature_stable_under_precision_and_order_change(self):
        m=self.module();lo=m.local_result(dps=40,order=2);hi=m.local_result(dps=60,order=3)
        with mp.workdps(70):
            a=mp.mpf(lo['edge_jets'][2]);b=mp.mpf(hi['edge_jets'][2])
            self.assertLess(abs(a-b)/max(1,abs(b)),mp.mpf('1e-20'))
            self.assertLess(mp.mpf(hi['independent_Qdot_spatial_jet_error']),mp.mpf('1e-40'))
            self.assertLess(mp.mpf(hi['initial_constraint_error']),mp.mpf('1e-40'))

    def test_coupled_refinement_uses_the_actual_jacobian(self):
        m=self.module();self.assertTrue(callable(getattr(m,'newton_refine',None)))
        with mp.workdps(50):
            fn=lambda x:[x[0]**2-2,x[1]-x[0]]
            x,history=m.newton_refine(fn,[mp.mpf('1.4'),mp.mpf('1.4')])
            self.assertLess(abs(x[0]-mp.sqrt(2)),mp.mpf('1e-30'))
            self.assertLess(abs(x[1]-mp.sqrt(2)),mp.mpf('1e-30'))
            self.assertTrue(history)


if __name__=='__main__':unittest.main()
