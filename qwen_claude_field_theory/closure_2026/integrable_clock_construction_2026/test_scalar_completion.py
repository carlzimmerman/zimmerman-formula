"""Regression checks for the IC-2 quadratic calculation, not full closure."""
import importlib.util
import json
from pathlib import Path
import unittest

import sympy as s

HERE = Path(__file__).resolve().parent
_MODULE = None


class ScalarCompletionTests(unittest.TestCase):
    def model(self):
        global _MODULE
        path = HERE / "scalar_completion.py"
        self.assertTrue(path.exists(), "The scalar action calculation is not implemented")
        if _MODULE is None:
            spec = importlib.util.spec_from_file_location("scalar_completion", path)
            _MODULE = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_MODULE)
        return _MODULE

    def test_raw_adm_keeps_the_mixed_spatial_term(self):
        d = self.model().derive()
        n, v, z = (d[j] for j in ("n", "v", "z"))
        expected = z*z + 4*n*z/3 + v*z/2 + n*v/3 + v*v/16
        self.assertEqual(s.expand(d["spatial_polynomial"] - expected), 0)
        self.assertEqual(d["residuals"]["raw_ricci"], 0)
        self.assertEqual(d["residuals"]["raw_kinetic"], 0)

    def test_correction_is_normalized_from_physical_volume(self):
        d = self.model().derive()
        self.assertEqual(s.simplify(d["correction_factor"] - 4*d["ell"]**2/3), 0)
        self.assertEqual(d["residuals"]["correction_quadratic"], 0)

    def test_eliminated_fields_solve_all_three_actual_equations(self):
        d = self.model().derive()
        self.assertEqual(d["constraint_residuals"], [0, 0, 0])
        self.assertEqual(d["residuals"]["momentum_constraint"], 0)
        self.assertEqual(d["residuals"]["reduced_action"], 0)

    def test_kinetic_polynomial_is_not_a_prescribed_rank(self):
        d = self.model().derive()
        x, T, alpha, dv, ev = (d[j] for j in ("x", "Tcal", "alpha", "d", "e"))
        expected = 12*T-81 + (12*ev+alpha*T+18*dv)*x + (alpha*ev-dv*dv)*x*x
        self.assertEqual(s.factor(d["kinetic_numerator"]-expected), 0)
        self.assertEqual(d["baseline_uv_kinetic_over_x"], -s.Rational(1, 27))

    def test_time_dependent_cross_term_is_integrated_with_the_measure(self):
        d = self.model().derive()
        x = d["x"]
        expected = d["c"] - 3*d["bcoef"]/2 + x*s.diff(d["bcoef"], x)
        self.assertEqual(s.factor(d["g"]-expected), 0)
        self.assertEqual(d["residuals"]["time_boundary"], 0)

    def test_selected_repair_has_positive_kinetic_and_uv_speed(self):
        d = self.model().repair()
        self.assertEqual(d["residuals"]["kinetic_positive_decomposition"], 0)
        self.assertEqual(d["residuals"]["auxiliary_positive_decomposition"], 0)
        self.assertEqual(d["uv_physical_speed_squared"], s.Rational(4, 9))
        self.assertGreater(float(d["T_exact"]), s.Rational(27, 4))
        self.assertGreater(d["transition_x_numeric"], 0)

    def test_ir_sign_is_not_mislabeled_as_all_wavelength_stability(self):
        d = self.model().repair()
        self.assertGreater(float(d["ir_g_over_x"]), 0)
        self.assertFalse(d["all_wavelength_frequency_nonnegative"])
        self.assertEqual(d["future_indicial_roots"], [0, s.Rational(3, 2)])
        self.assertEqual(d["residuals"]["transition_root"], 0)
        self.assertEqual(d["residuals"]["future_series"], 0)

    def test_sign_flags_have_exact_inequality_witnesses(self):
        d = self.model().repair()
        self.assertIn("kinetic_sign_expression", d, "Missing exact sign certificate")
        self.assertTrue(d["kinetic_sign_expression"].is_positive)
        self.assertTrue(d["ir_sign_expression"].is_positive)
        self.assertTrue(d["T_gap_lower_bound"].is_positive)
        self.assertFalse(self.model().run()["unmodified"]["positive_all_x_kinetic"])

    def test_correction_first_variation_vanishes_on_claimed_branches(self):
        d = self.model().derive()
        self.assertIn("static_correction_first_variation", d, "Missing branch-transfer variation")
        self.assertEqual(d["static_correction_first_variation"], [0, 0, 0])
        self.assertEqual(d["homogeneous_correction_first_variation"], [0, 0, 0])
        self.assertEqual(d["residuals"]["pure_tensor_correction"], 0)

    def test_exact_zero_mode_does_not_inherit_a_divided_shift_constraint(self):
        d = self.model().derive()
        T = d["Tcal"]
        self.assertEqual(s.factor(d["zero_mode_kinetic"]-(4*T/9-3)), 0)
        self.assertEqual(d["zero_mode_residuals"], [0, 0])
        self.assertNotEqual(s.factor(d["zero_mode_kinetic"]-d["a"].subs(d["x"], 0)), 0)

    def test_json_report_separates_the_proved_and_open_gates(self):
        d = self.model().run()
        json.dumps(d, allow_nan=False)
        self.assertTrue(d["exact_checks_passed"])
        self.assertFalse(d["full_theory_closed"])
        self.assertFalse(d["repair"]["all_wavelength_frequency_nonnegative"])
        self.assertFalse(d["repair"]["causality_proved"])


if __name__ == "__main__":
    unittest.main()
