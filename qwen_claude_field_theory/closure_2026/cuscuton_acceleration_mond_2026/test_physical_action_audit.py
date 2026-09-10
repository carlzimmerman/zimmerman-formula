"""Regression and falsification controls for the physical action audit."""
import unittest
import sympy as s

from physical_action_audit import (
    source_and_coefficients, tensor_redundancy, clock_background,
    scalar_dirac, lapse_ellipticity, cubic_scalar,
)


class PhysicalActionTests(unittest.TestCase):
    def test_real_source_rejects_historical_positive_sigma(self):
        data = source_and_coefficients()
        mu = next(iter(data["historical_counterterm_coefficient"].free_symbols))
        self.assertLess(data["historical_counterterm_coefficient"].subs(mu, s.Rational(1, 2)), 0)
        self.assertEqual(data["matched_coefficients"], {"eta": 1, "sigma": -1})
        eta, sigma = s.symbols("eta sigma", real=True, nonzero=True)
        self.assertEqual(data["flux_coefficient"].subs({eta: 0, sigma: 0}), 1)  # GR control

    def test_constraint_is_redundant_even_for_nonzero_slip(self):
        data = tensor_redundancy()
        self.assertEqual(data["ibp_residual"], 0)
        self.assertTrue(data["constraints_on_no_lapse_nonzero_Psi"].is_zero_matrix)
        self.assertEqual(data["vector_constraint_rank"], data["vector_plus_tensor_rank"])

    def test_lapse_variation_finds_clock_energy(self):
        data = clock_background()
        self.assertEqual(data["claimed_stealth_clock_Euler_residual"], 0)
        self.assertTrue(data["claimed_stealth_energy"].is_positive)

    def test_full_scalar_pair_survives_zero_quadratic_energy(self):
        data = scalar_dirac()
        self.assertEqual(data["constraint_preservation_residuals"], [0]*4)
        self.assertEqual(data["PB_rank"], data["PB_rank_at_eta_1"])
        self.assertEqual(data["scalar_canonical_pairs"], 1)
        self.assertEqual(data["reduced_bracket_z_p"], 1)
        self.assertEqual(data["reduced_H_at_eta_1"], 0)
        self.assertEqual(data["k_zero_secondary_generation"], [0, 0])

    def test_lapse_symbol_changes_type_across_acceleration_scale(self):
        data = lapse_ellipticity()
        yy = next(v for v in data["longitudinal"].free_symbols if str(v) == "y")
        self.assertTrue(data["longitudinal"].subs(yy, s.Rational(1, 2)).is_positive)
        self.assertEqual(data["longitudinal"].subs(yy, 1), 0)
        self.assertTrue(data["longitudinal"].subs(yy, 2).is_negative)
        self.assertEqual(data["nonzero_characteristic_above_y_1"], 0)

    def test_cubic_dynamics_is_not_erased_by_quadratic_degeneracy(self):
        data = cubic_scalar()
        self.assertEqual(data["kinetic_cubic_identity_residual"], 0)
        self.assertEqual(data["periodic_kinetic_witness_residual"], 0)
        self.assertNotEqual(data["periodic_kinetic_witness"], 0)


if __name__ == "__main__":
    unittest.main()
