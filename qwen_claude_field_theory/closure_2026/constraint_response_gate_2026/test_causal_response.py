"""Controls for a flat, constant-alpha conserved-source response calculation."""
import contextlib
import importlib.util
import io
import json
import unittest

import sympy as s


class CausalResponseTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("causal_response"),
                             "The causal-response derivation is not implemented")
        import causal_response
        return causal_response

    def test_actual_adm_action_retains_both_tt_and_transverse_shift_components(self):
        # Losing symmetric off-diagonal contractions changes these normalizations.
        d = self.module().derive_action()
        self.assertEqual(s.diff(d["L"], d["pd"], 2), d["m"]/2)
        self.assertEqual(s.diff(d["L"], d["cd"], 2), d["m"]/2)
        self.assertEqual(s.diff(d["L"], d["Vx"], 2), d["m"]*d["k"]**2/2)
        self.assertEqual(s.diff(d["L"], d["Vy"], 2), d["m"]*d["k"]**2/2)
        self.assertEqual(s.diff(d["L"], d["zd"]), 0)

    def test_spatial_curvature_is_derived_from_the_metric(self):
        # Wrong Ricci sign or a missed lapse-curvature term changes the source response.
        d = self.module().derive_action()
        self.assertEqual(d["curvature_action_residual"], 0)
        self.assertEqual(d["source_coupling_residual"], 0)

    def test_all_auxiliary_solutions_satisfy_original_action_variations(self):
        d = self.module().derive_action()
        self.assertEqual(d["auxiliary_residuals"], [0]*5)
        self.assertEqual(d["tensor_frequency_residuals"], [0, 0])
        self.assertEqual(d["tensor_wave_operator"], d["k"]**2-d["omega"]**2)

    def test_all_nine_curvature_components_match_retarded_gr_at_alpha_zero(self):
        # Declaring every elliptic potential acausal would fail this actual cancellation.
        d = self.module().derive_curvature()
        self.assertEqual(d["gr_identity_residuals"], [0]*9)
        self.assertEqual(d["fourier_conservation_residuals"], [0]*4)
        self.assertEqual(d["alpha0_trace_K"], 0)

    def test_alpha_dependence_is_a_derived_extra_curvature_tensor(self):
        d = self.module().derive_curvature()
        self.assertEqual(d["extra_identity_residuals"], [0]*9)
        self.assertEqual(d["extra_zeta_plus_n"], 0)
        self.assertNotEqual(d["extra_curvature"], s.zeros(3))

    def test_compact_scalar_fixture_is_conserved_without_using_field_equations(self):
        d = self.module().derive_fixture()
        self.assertEqual(d["conservation_residuals"], [0]*4)
        self.assertEqual(d["trace_combination_residual"], 0)
        self.assertEqual(d["b_second_at_1"], -2/s.E)
        self.assertTrue(d["signed_stress_perturbation"])

    def test_scalar_fixture_has_no_hidden_vector_or_tt_retarded_tail(self):
        d = self.module().derive_fixture()
        self.assertEqual(d["gr_local_curvature_residuals"], [0]*9)
        self.assertEqual(d["vector_tt_source_residuals"], [0]*4)

    def test_scalar_fixture_is_incompatible_with_the_singular_alpha_one_branch(self):
        d = self.module().derive_fixture()
        self.assertEqual(d["alpha_one_integrated_compatibility_at_t1_Q1"], -6/s.E)

    def test_outside_cone_tidal_witness_is_nonzero_at_alpha_half(self):
        # Treating the new scalar term as a gauge potential would erase this curvature.
        d = self.module().derive_fixture()
        self.assertEqual(s.simplify(d["half_alpha_witness"]-1/(24*s.pi*s.E)), 0)
        self.assertEqual(d["outside_cone_margin"], 1)
        self.assertEqual(d["alpha0_exterior_witness"], 0)

    def test_alpha_one_is_reclassified_before_regular_branch_inversion(self):
        d = self.module().derive_action()["alpha_one"]
        self.assertEqual(d["scalar_hessian_determinant"], 0)
        self.assertEqual(s.simplify(d["compatibility"]-d["rho"]-d["tau"]), 0)
        self.assertIsNone(d["regular_solution_inherited"])

    def test_json_result_and_cli_distinguish_execution_from_causal_gate(self):
        mod = self.module()
        data = json.loads(json.dumps(mod.run()))
        self.assertTrue(data["checks_passed"])
        self.assertEqual(data["causal_response_gate"], "FAIL")
        self.assertFalse(data["finite_acceleration_background_claimed"])
        self.assertFalse(data["healthy_positive_energy_matter_realization_claimed"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-causal-response"]), 2)


class AdaptiveResponseTests(unittest.TestCase):
    def module(self):
        import causal_response
        self.assertTrue(callable(getattr(causal_response, "derive_adaptive_action", None)),
                        "The stiff-background adaptive response is not implemented")
        return causal_response

    def test_seed_action_derives_both_regular_kinetic_controls(self):
        d = self.module().derive_adaptive_action()
        self.assertEqual(d["kinetic"].subs(d["b"], s.Rational(1, 4)), 3)
        self.assertEqual(d["kinetic"].subs(d["b"], s.Rational(3, 16)), 9)
        self.assertEqual(d["auxiliary_residuals"], [0]*3)
        self.assertEqual(d["source_coupling_residual"], 0)

    def test_actual_electric_weyl_is_slicing_invariant(self):
        d = self.module().derive_adaptive_weyl()
        self.assertEqual(d["fourier_weyl_residuals"], [0]*9)
        self.assertEqual(d["slicing_variation"], 0)

    def test_stiff_external_stress_obeys_all_four_covariant_ward_equations(self):
        d = self.module().derive_adaptive_fixture()
        self.assertEqual(d["ward_residuals"], [0]*4)
        self.assertEqual(d["zero_mean_profile_symbol"], 0)
        self.assertEqual(d["source_onset_jets"], [0]*4)
        self.assertEqual(d["initial_constraint_fields"], [0]*3)

    def test_time_green_function_has_the_retarded_unit_jump(self):
        d = self.module().derive_adaptive_fixture()
        self.assertEqual(d["green_ode_residual"], 0)
        self.assertEqual(d["green_initial_value"], 0)
        self.assertEqual(d["green_initial_slope"], 1)
        self.assertEqual(d["moment_equation_residual"], 0)
        self.assertEqual(d["contact_subtraction_residual"], 0)

    def test_k9_local_cancellation_does_not_remove_the_retarded_contact(self):
        d = self.module().derive_adaptive_fixture()
        self.assertEqual(d["free_local_weyl_velocity_coefficient"].subs(d["K"], 9), 0)
        self.assertEqual(d["weyl_contact_coefficient"].subs(d["K"], 9), s.Rational(1, 3))
        self.assertEqual(s.simplify(d["weyl_contact_coefficient"]-3/d["K"]), 0)

    def test_exact_kernel_positivity_certifies_a_nonzero_dipole_weyl_tail(self):
        d = self.module().derive_adaptive_fixture()
        self.assertEqual(d["k9_kernel_bracket_lower_bound"], s.Rational(47, 72))
        self.assertEqual(s.simplify(d["k9_exterior_abs_lower_bound"]
                                   -2*s.exp(-4)/(27*s.pi)), 0)
        self.assertTrue(d["outside_metric_light_cone"])
        self.assertEqual(d["dipole_weyl_geometry_residual"], 0)

    def test_entire_finite_subluminal_family_has_a_strict_external_weyl_bound(self):
        d = self.module().derive_adaptive_fixture()
        self.assertIn("general_exterior_abs_lower_bound", d,
                      "The family-wide bound has not been derived")
        self.assertEqual(s.simplify(d["general_exterior_abs_lower_bound"]
                                   -2*s.exp(-4)/(3*s.pi*d["m"]*d["K"])), 0)
        self.assertTrue(all(value.is_positive for value in d["family_positive_certificates"]))
        self.assertTrue(d["family_metric_speed_gap"].is_nonnegative)
        self.assertEqual(d["scalar_vector_tt_projection_residuals"], [0]*12)

    def test_adaptive_cli_reports_only_the_scoped_retarded_response_failure(self):
        mod = self.module()
        data = json.loads(json.dumps(mod.run()))["adaptive_response"]
        self.assertTrue(data["checks_passed"])
        self.assertEqual(data["causal_response_gate"], "FAIL")
        self.assertFalse(data["preexisting_constraint_tail_used"])
        self.assertFalse(data["healthy_positive_energy_matter_realization_claimed"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-adaptive-causal-response"]), 2)


if __name__ == "__main__":
    unittest.main()
