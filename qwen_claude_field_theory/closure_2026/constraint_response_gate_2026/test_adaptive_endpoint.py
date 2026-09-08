"""Action, invariant-curvature, and transfer controls for adaptive kernels."""

import json
import unittest

import sympy as s

import adaptive_endpoint as gate


class AdaptiveEndpointTests(unittest.TestCase):
    def test_action_variations_and_connection_identities(self):
        result = gate.derive()
        self.assertIn("connection_pure_time_gauge_Ricci", result["residuals"])
        for name, residual in result["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)

    def test_canonical_matter_kinetic_is_derived_for_general_beta(self):
        result = gate.derive()
        beta = result["beta"]
        self.assertEqual(s.simplify(result["kinetic"]-(9/(2*beta)-15)), 0)
        self.assertEqual(result["kinetic"].subs(beta, s.Rational(1, 4)), 3)

    def test_original_kernel_has_growing_gauge_invariant_curvature(self):
        result = gate.derive()
        coefficient = result["growth_coefficients"]["R_com"].subs(result["beta"], s.Rational(1, 4))
        expected = 20*result["Hd"]*result["k"]**2*result["u_infinity"]/result["q0"]
        self.assertEqual(s.simplify(coefficient-expected), 0)
        self.assertNotEqual(coefficient, 0)

    def test_cancellation_parameter_is_solved_then_checked_in_other_curvature(self):
        result = gate.derive()
        candidate = result["candidate_beta"]
        self.assertEqual(candidate, s.Rational(3, 16))
        self.assertTrue(candidate > 0)
        self.assertTrue(result["kinetic"].subs(result["beta"], candidate) > 0)
        for name, expression in result["candidate_positive_power_terms"].items():
            with self.subTest(curvature=name):
                self.assertEqual(s.simplify(expression), 0)

    def test_exact_background_and_frobenius_coefficients(self):
        result = gate.derive()
        self.assertTrue(all(s.simplify(value) == 0 for value in result["background_residuals"].values()))
        self.assertEqual(result["residuals"]["frobenius_order_two"], 0)
        self.assertEqual(result["residuals"]["frobenius_order_four"], 0)

    def test_two_tolerance_transfers_are_consistent(self):
        result = gate.run()
        json.dumps(result)
        self.assertTrue(result["algebra_checks_passed"])
        self.assertTrue(result["original_endpoint_growing"])
        self.assertTrue(result["candidate_curvature_growth_cancelled"])
        for name, transfer in result["numerical"].items():
            with self.subTest(branch=name):
                self.assertTrue(transfer["coarse"]["success"])
                self.assertTrue(transfer["refined"]["success"])
                self.assertLess(transfer["maximum_scaled_tolerance_difference"], 1e-4)


if __name__ == "__main__":
    unittest.main()
