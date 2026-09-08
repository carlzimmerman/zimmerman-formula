"""General finite-K canonical Cauchy-support and action-derived branch gates."""

import contextlib
import importlib
import importlib.util
import io
import json
import unittest

import sympy as s


class GeneralFamilyTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("general_family"),
                             "The general-family derivation is not implemented")
        return importlib.import_module("general_family")

    def test_free_action_is_varied_before_the_family_is_parameterized(self):
        d = self.module().derive_action()
        self.assertTrue(d["pinned_inputs_match"])
        self.assertEqual(s.simplify(d["kinetic_b"]-9/(2*d["b"])+15), 0)
        self.assertEqual(s.simplify(d["b_of_K"]-9/(2*(d["K"]+15))), 0)
        self.assertEqual(d["residuals"]["kinetic_parameterization"], 0)
        self.assertEqual(s.simplify(d["matter_momentum"]-d["K"]*d["a"]**3*d["ud"]), 0)

    def test_actual_general_geometry_has_local_and_nonlocal_weyl_parts(self):
        d = self.module().derive_geometry()
        self.assertNotEqual(d["local_slip_coefficient"], 0)
        self.assertEqual(d["local_slip_coefficient"].subs(d["K"], 9), 0)
        for name, residual in d["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)

    def test_annular_initial_canonical_data_match_for_every_finite_K(self):
        d = self.module().derive_annular()
        for field in d["inner_initial_fields"].values():
            entries = list(field) if isinstance(field, s.MatrixBase) else [field]
            self.assertTrue(all(s.simplify(entry) == 0 for entry in entries))
        self.assertTrue(d["torus_mean_zero_by_parity"])
        self.assertTrue(d["epsilon_may_depend_on_K"])
        self.assertFalse(d["localized_auxiliary_values_claimed_equal"])

    def test_uniform_green_bound_and_metric_cone_for_K_at_least_one(self):
        d = self.module().derive_green()
        self.assertEqual(d["green_lower"], s.Rational(211, 400))
        self.assertTrue(d["mass_upper_slack"].is_nonnegative)
        self.assertTrue(d["mass_positive_certificate"].is_positive)
        self.assertTrue(d["metric_speed_gap_certificate"].is_nonnegative)
        self.assertTrue(d["Weyl_abs_lower"].is_positive)
        self.assertEqual(d["matter_cone_margin"], s.Rational(3, 4))

    def test_positive_b_classification_is_computed_from_the_kinetic(self):
        d = self.module().derive_action()
        branches = d["positive_b_classification"]
        self.assertEqual(branches["K_ge_one"], s.Interval.Lopen(0, s.Rational(9, 32)))
        self.assertEqual(branches["zero_lt_K_lt_one"], s.Interval.open(s.Rational(9, 32), s.Rational(3, 10)))
        self.assertEqual(branches["K_zero"], s.FiniteSet(s.Rational(3, 10)))
        self.assertEqual(branches["K_negative"], s.Interval.open(s.Rational(3, 10), s.oo))
        self.assertEqual(s.Union(*branches.values()), s.Interval.open(0, s.oo))

    def test_every_computed_identity_and_scoped_cli_status(self):
        mod = self.module()
        result = mod.run()
        json.dumps(result)
        self.assertTrue(result["checks_passed"])
        self.assertEqual(result["healthy_linear_cauchy_gate"], "FAIL")
        self.assertFalse(result["zero_past_actuator_realization_claimed"])
        self.assertFalse(result["nonlinear_initial_data_lift_claimed"])
        self.assertFalse(result["infinite_K_or_b_zero_claimed"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-cauchy-locality"]), 2)


if __name__ == "__main__":
    unittest.main()
