"""Regressions for the physical projection and the closure obstruction."""
import unittest

import sympy as s

from derive_geometry import (constrained_obstruction, frozen_action_map, projected_geometry,
                             unitary_adm, variance_transport)


class ClockGeometryTests(unittest.TestCase):
    def test_arbitrary_metric_second_order_projection(self):
        result = projected_geometry()
        self.assertTrue(all(result["checks"].values()))
        self.assertFalse(result["expression"].free_symbols & result["metric_symbols"])
        self.assertFalse(result["expression"].free_symbols & result["second_order_symbols"])

    def test_comoving_fields_have_zero_projected_gradient(self):
        result = projected_geometry()
        q, sbar = result["symbols"]["q"], result["symbols"]["sbar"]
        substitutions = {s.Symbol("sigma_"+axis,real=True):q/sbar*s.Symbol("pi_"+axis,real=True)
                         for axis in "xyz"}
        self.assertEqual(s.simplify(result["expression"].subs(substitutions)),0)

    def test_unitary_gauge_preserves_all_three_spatial_components(self):
        result = projected_geometry()
        expr = result["expression"].subs({s.Symbol("pi_"+axis,real=True):0 for axis in "xyz"})
        expected = sum(s.Symbol("sigma_"+axis,real=True)**2 for axis in "xyz")/result["symbols"]["a"]**2
        self.assertEqual(s.expand(expr-expected),0)

    def test_exact_adm_identity_and_cosine_normalization(self):
        self.assertTrue(all(unitary_adm()["checks"].values()))

    def test_action_matrix_density_correlation_witness(self):
        self.assertTrue(all(constrained_obstruction()["checks"].values()))

    def test_covariance_transport_and_all_hidden_directions(self):
        self.assertTrue(all(variance_transport()["checks"].values()))

    def test_frozen_action_matches_geometric_observable_and_state_map(self):
        self.assertTrue(all(frozen_action_map()["checks"].values()))

    def test_scalar_closure_failure_at_an_exact_regular_matrix(self):
        # Rational matrix fixture verifies signs/scaling only; it is not
        # asserted to be a physical constitutive/background sample.
        M = s.Matrix([[2,0,0,3],[0,5,0,7],[0,0,1,11],[13,0,0,17]])
        source = s.Matrix([0,0,s.Rational(3,10),s.Rational(1,2)])
        lapse_density = (-M.inv()*source)[3]
        self.assertEqual(lapse_density,s.Rational(1,5))
        p,q,x,r = s.Rational(9,4),s.Rational(2,3),s.Rational(1,7),s.Rational(1,11)
        gap = 4*p*q*x*r*lapse_density
        self.assertEqual(gap,s.Rational(6,385))
        self.assertNotEqual(gap,0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
