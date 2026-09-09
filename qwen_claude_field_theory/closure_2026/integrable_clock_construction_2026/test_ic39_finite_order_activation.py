"""A finite-order switch must expose both its benefit and regularity cost."""
import importlib.util
import unittest
import sympy as s


class ActivationTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic39_finite_order_activation'))
        return __import__('ic39_finite_order_activation')

    def test_endpoint_smoothness_is_derived_not_assigned(self):
        out=self.module().derive()
        self.assertEqual(out['left_jets'],[0,0,0,0,6144])
        self.assertEqual(out['right_jets'],[1,0,0,0,-6144])

    def test_quartic_source_has_finite_limit_but_lower_order_leaks(self):
        out=self.module().derive()
        self.assertEqual(out['limit_identity'],0)
        self.assertEqual(out['quadratic_leak_limit'],-s.oo)
        self.assertEqual(out['quartic_example_limit'],-s.Rational(1,256))

    def test_action_variation_preserves_pin_equation_not_just_force_law(self):
        out=self.module().derive()
        self.assertTrue(all(v==0 for v in out['variation_checks'].values()))
        self.assertEqual(out['monotonicity_identity'],0)


if __name__=='__main__':unittest.main()
