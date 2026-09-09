"""Elimination must reject incompatible sources and retain singular cases."""
import importlib.util
import unittest
import sympy as s


class FunctionalCompatibilityTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic38_functional_compatibility'))
        return __import__('ic38_functional_compatibility')

    def test_identically_zero_b1_does_not_hide_second_residual(self):
        m=self.module();x=s.Symbol('x',real=True)
        out=m.reduce_exact(x,[0,0,1],[1,0,0],0,x*x)
        self.assertEqual(out['R1'],0)
        self.assertEqual(out['R2'],-2)
        self.assertEqual(out['A'],-x*x)

    def test_compatible_nonconstant_pair_recovers_actual_solution(self):
        m=self.module();x=s.Symbol('x',real=True)
        # A=exp(x), A''+x A'+A=-( -(x+2)exp(x) ).
        C=[1,x,1];W=[2,3+x,2]
        out=m.reduce_exact(x,C,W,-(x+2)*s.exp(x),-(7+x)*s.exp(x))
        self.assertEqual(s.simplify(out['A']-s.exp(x)),0)
        self.assertEqual(out['R1'],0);self.assertEqual(out['R2'],0)

    def test_singular_pair_is_not_certified_or_divided(self):
        m=self.module();x=s.Symbol('x',real=True)
        out=m.reduce_exact(x,[0,0,1],[0,0,2],0,1)
        self.assertEqual(out['determinant'],0)
        self.assertEqual(out['status'],'singular_reduction')
        self.assertNotIn('A',out)

    def test_generic_elimination_identities(self):
        m=self.module()
        self.assertTrue(all(v==0 for v in m.identities().values()))

    def test_numeric_reduction_keeps_an_incompatible_source(self):
        m=self.module();self.assertTrue(callable(getattr(m,'reduce_series',None)))
        import mpmath as mp
        with mp.workdps(50):
            zero=[0]*5;one=[1,0,0,0,0]
            out=m.reduce_series([zero,zero,one],[one,zero,zero],zero,[0,0,1,0,0],2)
            for got,want in zip(out['R2_jets'],[-2,0,0]):self.assertLess(abs(got-want),mp.mpf('1e-40'))

    def test_real_field_operator_recovers_independent_boundary_solution(self):
        m=self.module()
        import mpmath as mp
        out=m.field_result(dps=50)['operator']
        self.assertLess(mp.mpf(out['boundary_A_agreement']),mp.mpf('1e-25'))
        self.assertLess(mp.mpf(out['boundary_V_agreement']),mp.mpf('1e-25'))

    def test_numeric_reduction_with_variable_coefficients(self):
        m=self.module()
        import mpmath as mp
        with mp.workdps(50):
            C=[[1,0,0,0,0],[0,1,0,0,0],[1,0,0,0,0]]
            W=[[2,0,0,0,0],[3,1,0,0,0],[2,0,0,0,0]]
            f=[-mp.mpf(n+2)/mp.factorial(n) for n in range(5)]
            g=[-mp.mpf(n+7)/mp.factorial(n) for n in range(5)]
            out=m.reduce_series(C,W,f,g,2)
            self.assertLess(abs(out['A']-1),mp.mpf('1e-40'))
            for key in ('R1_jets','R2_jets'):
                self.assertLess(max(abs(v) for v in out[key]),mp.mpf('1e-40'))


if __name__=='__main__':unittest.main()
