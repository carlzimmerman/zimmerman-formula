"""Radial action variation, complete static metric components, and matching."""
import importlib.util
import unittest
import sympy as s
import mpmath as mp


class RadialBridgeTests(unittest.TestCase):
    def implementation(self):
        self.assertIsNotNone(importlib.util.find_spec('ic30_radial_bridge'),
                             'Radial bridge variation is not implemented')
        import ic30_radial_bridge
        return ic30_radial_bridge

    def test_radial_shift_equations_follow_from_action(self):
        m=self.implementation()
        for name,value in m.radial_checks().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_static_physical_density_follows_from_barred_action(self):
        m=self.implementation()
        for name,value in m.static_checks().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_full_static_metric_not_only_conformal_trace(self):
        m=self.implementation()
        for name,value in m.metric_checks().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_matching_derivative_is_not_an_assigned_zero(self):
        m=self.implementation()
        with mp.workdps(45):
            for y in (mp.mpf('.001'),mp.mpf('.1'),mp.mpf(1),mp.mpf(10)):
                r=m.matching(y,mp.mpf('1e-6'))
                self.assertLess(r['r_wprime'],0)
                self.assertLess(abs(r['constitutive_residual']),mp.mpf('1e-35'))
                self.assertLess(abs(r['mass_law_derivative_residual']),mp.mpf('1e-35'))
                self.assertEqual(r['w_at_join'],mp.mpf('-0.025'))
                self.assertLess(abs(r['derivative_residual']),mp.mpf('1e-35'))

    def test_constructive_collar_satisfies_momentum_constraint(self):
        m=self.implementation()
        for name,value in m.collar_checks().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_same_action_z_constraint_through_collar(self):
        m=self.implementation()
        with mp.workdps(50):
            rows=m.collar_auxiliary_rows()
            self.assertGreater(len(rows),2)
            for row in rows:
                self.assertLess(abs(row['z_residual']),mp.mpf('1e-40'))
                self.assertLess(abs(row['z_derivative_residual']),mp.mpf('1e-40'))
                self.assertGreater(row['z_jacobian'],0)
                self.assertGreaterEqual(row['z'],0)


if __name__=='__main__':
    unittest.main()
