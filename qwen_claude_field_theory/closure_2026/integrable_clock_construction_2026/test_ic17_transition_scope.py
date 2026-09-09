"""Exact scope controls; no IC17 constraint solution is asserted."""
import importlib
import importlib.util
import subprocess
import sys
import unittest
import sympy as s


class TransitionScopeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('ic17_transition_scope'),
                             'Missing independently computed transition scope audit')
        self.m = importlib.import_module('ic17_transition_scope')

    def test_hessian_identity_includes_pressure_and_switch_derivatives(self):
        self.assertTrue(all(v == 0 for v in self.m.fixed_q_checks().values()))

    def test_rising_switch_and_strict_positive_interior_coefficient(self):
        c = self.m.counterexample()
        r = c['r']
        self.assertEqual(s.factor(c['eta_prime']), 30*(r-1)**2*(r-2)**2)
        self.assertEqual(s.simplify(c['aUV']-c['eta_prime']-c['eta_second']**2/100), 0)
        self.assertEqual([c['eta'].subs(r,k) for k in (1,2)], [0,1])
        for k in (1,2):
            self.assertEqual(c['eta_prime'].subs(r,k), 0)
            self.assertEqual(c['eta_second'].subs(r,k), 0)

    def test_isolated_zero_and_divergent_integrating_factor(self):
        c = self.m.counterexample()
        self.assertEqual(s.solve(c['b'],c['r']), [1,s.Rational(3,2),2])
        self.assertEqual(c['integrating_factor_residue'], -s.Rational(10,3))

    def test_positive_pressure_bound_and_chart_sample_scope(self):
        c = self.m.counterexample()
        self.assertEqual(c['second_derivative_bound'], 10/s.sqrt(3))
        self.assertTrue(c['B_numerator_lower_bound'] > 0)
        self.assertTrue(all(self.m.chart_checks().values()))

    def test_failure_gate_and_strict_cli(self):
        self.assertEqual(self.m.exit_status({'x':False}), 1)
        self.assertEqual(self.m.exit_status({'x':False},True), 1)
        self.assertEqual(self.m.exit_status({'x':True},True), 2)
        result=subprocess.run([sys.executable,self.m.__file__,'--require-full-closure'],
                              capture_output=True,text=True)
        self.assertEqual(result.returncode,2,result.stderr)


if __name__ == '__main__':
    unittest.main()
