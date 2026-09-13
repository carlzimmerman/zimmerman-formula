"""Regression tests for a screened spatial kernel, not a full gravity certificate."""
import contextlib
import importlib.util
import io
import json
import unittest
from unittest.mock import patch

import sympy as s


class ScreenedKernelTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("screened_kernel"))
        import screened_kernel
        return screened_kernel

    def test_screened_kernel_is_inserted_before_auxiliary_variation(self):
        d = self.module().derive_action()
        self.assertTrue(all(value == 0 for value in d["constraint_residuals"]))
        self.assertEqual(s.factor(d["solution"][d["n"]]-4*d["ud"]/d["q"]), 0)
        self.assertEqual(s.factor(d["kinetic"]-d["K0"]-3*d["mass2"]/(d["k"]**2/d["a"]**2)), 0)

    def test_volume_and_time_dependent_kinetic_are_varied_in_the_actual_action(self):
        d = self.module().derive_action()
        self.assertEqual(d["time_EL_residual"], 0)
        self.assertNotEqual(d["kinetic_drift"], 0)
        self.assertEqual(s.factor(d["kinetic_drift"]+12*d["H"]*d["mass2"]*d["a"]**2/d["k"]**2), 0)

    def test_only_one_healthy_frozen_coefficient_removes_the_dispersion_pole(self):
        d = self.module().derive_action()
        self.assertEqual(d["frozen_cancellation_K0"], [3])
        self.assertEqual(d["frozen_cancellation_b"], [s.Rational(1, 4)])
        self.assertEqual(s.factor(d["frozen_pole_residue"]
            +3*d["mu2_symbol"]**2*(d["K0"]-3)/d["K0"]**3), 0)

    def test_frozen_wave_speed_does_not_delete_the_expanding_yukawa_drag(self):
        d = self.module().derive_action()
        self.assertEqual(d["selected_speed_squared"], s.Rational(1, 3))
        self.assertEqual(d["selected_drag_residual"], 0)
        self.assertNotEqual(d["selected_drag_pole_residue"], 0)

    def test_actual_metric_weyl_cancels_only_the_velocity_inverse_laplacian(self):
        d = self.module().derive_geometry()
        self.assertTrue(all(value == 0 for value in d["geometry_residuals"]))
        self.assertEqual(d["required_inverse_Q_laplacian_coefficient"], [-1])
        self.assertEqual(d["Weyl_canonical_residual"], 0)
        self.assertNotEqual(d["Weyl_canonical_tracefree_term"], 0)

    def test_physical_scalar_stress_obeys_full_linear_not_separate_external_ward(self):
        d = self.module().derive_geometry()
        self.assertEqual(d["physical_KG_action_residual"], 0)
        self.assertTrue(all(value == 0 for value in d["physical_ward_residuals"]))
        self.assertFalse(d["external_stress_used"])
        self.assertEqual(d["relational_gauge_variation"], 0)

    def test_all_original_canonical_initial_fields_have_annular_support(self):
        d = self.module().derive_geometry()
        self.assertTrue(all(value == 0 for value in d["initial_reconstruction_residuals"]))
        self.assertTrue(all(value == 0 for value in d["initial_inner_ball_fields"].values()))
        self.assertIn("gravity_tracefree_momentum", d["initial_local_fields"])
        self.assertIn("matter_momentum", d["initial_local_fields"])
        self.assertEqual(d["initial_I_linear"], 0)

    def test_canonical_matter_momentum_is_derived_not_assigned(self):
        d = self.module().derive_geometry()
        a = self.module().derive_action()
        self.assertEqual(s.factor(d["matter_momentum"]-a["a"]**3*a["kinetic"]*a["ud"]), 0)
        self.assertEqual(d["trace_momentum_constraint_residual"], 0)

    def test_hole_jerk_has_a_strictly_positive_yukawa_coefficient(self):
        d = self.module().derive_tail()
        self.assertEqual(d["jerk_decomposition_residual"], 0)
        self.assertEqual(d["primitive_division_residual"], 0)
        self.assertTrue(d["hole_jerk_coefficient"].is_positive)
        self.assertTrue(d["strict_jerk_origin_lower_bound"].is_positive)

    def test_yukawa_kernel_has_the_correct_operator_and_unit_flux(self):
        d = self.module().derive_tail()
        self.assertEqual(d["green_ODE_residual"], 0)
        self.assertEqual(d["green_unit_flux_residual"], 0)
        self.assertTrue(d["green_kernel"].is_positive)
        self.assertEqual(d["physical_mean_zero_symbol"], 0)

    def test_relational_matter_observable_detects_the_tail_without_lapse_inference(self):
        d = self.module().derive_tail()
        self.assertEqual(d["relational_second_derivative_residual"], 0)
        self.assertTrue(d["strict_abs_relational_second_derivative_lower_bound"].is_positive)

    def test_full_kernel_normalization_is_checked_using_the_actual_I_mode(self):
        d = self.module().derive_kernel_realizer()
        self.assertEqual(d["quadratic_matching_residual"], 0)
        self.assertEqual(d["clock_mass_matching_residual"], 0)
        self.assertFalse(d["full_nonlinear_field_variation_completed"])

    def test_json_does_not_promote_a_linear_gate_to_nonlinear_closure(self):
        result = json.loads(json.dumps(self.module().run(), allow_nan=False))
        self.assertTrue(result["checks_passed"])
        self.assertEqual(result["expanding_linear_Cauchy_gate"], "FAIL")
        self.assertIsNone(result["full_gravitational_count"])
        self.assertFalse(result["zero_past_actuator_realization_claimed"])
        self.assertFalse(result["nonlinear_initial_data_lift_claimed"])
        self.assertFalse(result["exact_zero_mode_inverse_assigned"])

    def test_cli_distinguishes_algebra_failure_from_unmet_causal_requirement(self):
        module = self.module()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main([]), 0)
            self.assertEqual(module.main(["--require-causal-screen"]), 2)
        failed = {"checks_passed": False, "expanding_linear_Cauchy_gate": "INCONCLUSIVE"}
        with patch.object(module, "run", return_value=failed), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main([]), 1)
            self.assertEqual(module.main(["--require-causal-screen"]), 1)


if __name__ == "__main__":
    unittest.main()
