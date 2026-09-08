"""Controls for a fixed positive-Lambda conserved-source response screen."""
import contextlib
import importlib.util
import io
import json
import unittest

import sympy as s


class PositiveLambdaTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("positive_lambda"),
                             "The positive-Lambda response is not implemented")
        import positive_lambda
        return positive_lambda

    def test_actual_background_and_pinned_action_inputs(self):
        d = self.module().derive()
        self.assertTrue(d["base_inputs_match"])
        self.assertEqual(d["background_residuals"], [0]*5)
        self.assertEqual(d["action_equation_residual"], 0)
        self.assertEqual(s.simplify(d["matter_speed_squared"]-1/d["K"]), 0)

    def test_moment_operator_retains_positive_lambda_terms(self):
        d = self.module().derive()
        self.assertEqual(d["moment_operator_residual"], 0)
        self.assertEqual(d["positive_lambda_mass_residual"], 0)
        self.assertEqual(d["remainder_source_residual"], 0)
        self.assertEqual(s.simplify(d["contact_coefficient"]-3/d["K"]), 0)

    def test_all_covariant_ward_and_scalar_projection_components(self):
        d = self.module().derive()
        self.assertEqual(d["ward_residuals"], [0]*4)
        self.assertEqual(d["scalar_projection_residuals"], [0]*12)
        self.assertEqual(d["zero_mean_profile"], 0)

    def test_no_past_source_or_initial_metric_tail_supplies_the_witness(self):
        d = self.module().derive()
        self.assertEqual(d["source_onset_jets"], [0]*4)
        self.assertEqual(d["initial_auxiliary_fields"], [0]*3)
        self.assertEqual(d["weyl_identity_residuals"], [0]*9)
        self.assertEqual(d["slicing_variation"], 0)

    def test_every_finite_subluminal_K_has_positive_remainder_weights(self):
        d = self.module().derive()
        self.assertTrue(all(value.is_positive for value in d["positive_certificates"]))
        self.assertTrue(d["mass_upper_slack_certificate"].is_nonnegative)
        self.assertTrue(d["metric_speed_gap_certificate"].is_nonnegative)

    def test_short_time_green_bound_uses_derived_operator_bounds(self):
        d = self.module().derive()
        self.assertEqual(d["normalized_damping_bound"], 9)
        self.assertEqual(d["normalized_mass_bound"], 18)
        self.assertEqual(d["green_derivative_lower_bound"], s.Rational(211, 400))
        self.assertEqual(d["green_comparison_identity"], 0)

    def test_explicit_exterior_pulse_bound_is_strict_and_outside_cone(self):
        d = self.module().derive()
        self.assertEqual(s.simplify(d["weyl_amplitude_lower_bound"]
                                   -120*d["H0"]/(s.E*d["K"])), 0)
        self.assertEqual(s.simplify(d["electric_weyl_abs_lower_bound"]
            -135*d["H0"]/(s.pi*s.E*d["m"]*d["K"]*d["r_event"]**4)), 0)
        self.assertTrue(d["outside_cone_margin_lower_bound"].is_positive)
        self.assertEqual(d["dipole_geometry_residual"], 0)

    def test_bounded_numerics_only_corroborate_the_exact_inequality(self):
        result = self.module().numerical_check()
        self.assertEqual([entry["K"] for entry in result], [1, 9, 100])
        self.assertTrue(all(entry["F"] > entry["rigorous_F_lower_bound"] for entry in result))
        self.assertTrue(all(entry["relative_refinement_change"] < 1e-7 for entry in result))

    def test_cli_distinguishes_computation_from_the_scoped_physics_failure(self):
        mod = self.module()
        result = json.loads(json.dumps(mod.run()))
        self.assertTrue(result["checks_passed"])
        self.assertEqual(result["causal_response_gate"], "FAIL")
        self.assertFalse(result["healthy_positive_energy_matter_realization_claimed"])
        self.assertFalse(result["stiff_background_response_reused"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-causal-response"]), 2)


if __name__ == "__main__":
    unittest.main()
