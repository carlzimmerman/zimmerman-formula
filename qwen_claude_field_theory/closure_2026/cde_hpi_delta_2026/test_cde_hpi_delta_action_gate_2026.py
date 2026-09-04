#!/usr/bin/env python3
"""Adversarial tests for the CDE-HPI-Delta construction/falsification gate."""

from __future__ import annotations

import unittest

import sympy as sp

from cde_hpi_delta_action_gate_2026 import derive_hpi_delta_gate


class CdeHpiDeltaActionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = derive_hpi_delta_gate()

    def test_exact_exponential_constitutive_law_is_derived(self) -> None:
        kernel = self.result["kernel"]
        self.assertEqual(kernel["modulus_residual"], 0)
        self.assertEqual(kernel["primitive_residual"], 0)
        self.assertEqual(kernel["lambda_parallel_residual"], 0)
        self.assertEqual(kernel["newtonian_limit"], 1)
        self.assertEqual(kernel["deep_ratio"], 1)

    def test_action_contains_only_the_trace_momentum_auxiliary_constraint(self) -> None:
        action = self.result["action"]
        self.assertEqual(action["auxiliary_constraints"], (action["C_pi"],))
        self.assertFalse(action["has_inserted_slip_constraint"])
        self.assertFalse(action["has_lagrangian_K_multiplier"])

    def test_preselected_primaries_are_consistent_with_absent_velocities(self) -> None:
        chain = self.result["finite_k"]["generic_positive_gradient"]
        self.assertEqual(chain["base"]["spatial_reduction_residual"], 0)
        self.assertEqual(chain["base"]["adm_reduction_residual"], 0)
        self.assertEqual(chain["base"]["mond_hessian_residual"], 0)
        self.assertEqual(chain["C_pi_rescaling_residual"], 0)
        self.assertTrue(all(value == 0 for value in chain["primary_velocity_derivatives"]))
        self.assertEqual(
            tuple(chain["primaries"]),
            tuple(chain["derived_primaries"]),
        )
        self.assertTrue(chain["primaries_preselected_by_first_order_canonical_action"])
        self.assertTrue(chain["primary_check_is_velocity_absence_not_hessian_discovery"])

    def test_trace_constraint_preservation_is_no_slip_not_an_input(self) -> None:
        chain = self.result["finite_k"]["generic_positive_gradient"]
        weak = self.result["weak_static"]
        self.assertTrue(weak["one_dimensional_reduction_only"])
        self.assertEqual(chain["trace_preservation_slip_residual"], 0)
        self.assertEqual(chain["trace_preservation_vs_weak_E_Psi_residual"], 0)
        self.assertTrue(chain["trace_preservation_independent_before_closure"])
        self.assertFalse(chain["slip_inserted_as_constraint"])
        self.assertEqual(weak["no_slip_residual"], 0)

    def test_lapse_preservation_becomes_exact_aqual_after_derived_slip(self) -> None:
        weak = self.result["weak_static"]
        self.assertEqual(weak["E_Phi_on_derived_slip_residual"], 0)
        self.assertEqual(weak["aqual_flux_residual"], 0)
        self.assertEqual(weak["spherical_flux_residual"], 0)
        self.assertEqual(weak["deep_mond_residual"], 0)

    def test_constraint_jacobian_and_poisson_ranks_are_computed_and_crosschecked(self) -> None:
        chain = self.result["finite_k"]["generic_positive_gradient"]
        self.assertEqual(
            chain["constraint_jacobian_rank"],
            chain["constraint_jacobian_sample_rank"],
        )
        self.assertEqual(chain["poisson_rank"], chain["poisson_sample_rank"])
        self.assertEqual(chain["rank_witness"]["size"], chain["poisson_rank"])
        self.assertNotEqual(chain["rank_witness"]["determinant"], 0)
        self.assertEqual(chain["poisson_matrix"] + chain["poisson_matrix"].T, sp.zeros(len(chain["constraints"])))
        phase = chain["phase_variables"]
        half = len(phase) // 2
        coordinates, momenta = phase[:half], phase[half:]

        def independent_pb(first: sp.Expr, second: sp.Expr) -> sp.Expr:
            return sp.factor(sum(
                sp.diff(first, q) * sp.diff(second, p)
                - sp.diff(first, p) * sp.diff(second, q)
                for q, p in zip(coordinates, momenta)
            ))

        independently_rebuilt = sp.Matrix([
            [independent_pb(first, second) for second in chain["constraints"]]
            for first in chain["constraints"]
        ])
        self.assertEqual(independently_rebuilt, chain["poisson_matrix"])

    def test_first_class_generators_are_actual_poisson_null_vectors(self) -> None:
        chain = self.result["finite_k"]["generic_positive_gradient"]
        matrix = chain["poisson_matrix_on_constraint_surface"]
        for vector in chain["poisson_nullspace"]:
            self.assertEqual(matrix * vector, sp.zeros(matrix.rows, 1))
        self.assertTrue(all(value == 0 for value in chain["first_class_bracket_residuals"]))

    def test_scalar_count_is_a_consequence_of_computed_classes(self) -> None:
        chain = self.result["finite_k"]["generic_positive_gradient"]
        recomputed = sp.Rational(
            chain["phase_dimension"]
            - 2 * chain["first_class_count"]
            - chain["second_class_count"],
            2,
        )
        self.assertEqual(chain["configuration_dof"], recomputed)
        self.assertEqual(chain["configuration_dof"], 0)
        self.assertFalse(chain["local_scalar_pair_survives"])

    def test_spatial_gauge_fixed_chain_closes_with_the_same_scalar_count(self) -> None:
        restored = self.result["finite_k"]["generic_positive_gradient"]
        fixed = self.result["finite_k"]["spatial_gauge_fixed"]
        self.assertEqual(fixed["tertiary_slip_residual"], 0)
        self.assertEqual(fixed["quaternary_residual"], 0)
        self.assertEqual(fixed["constraint_jacobian_rank"], fixed["phase_dimension"])
        self.assertEqual(fixed["poisson_rank"], fixed["poisson_sample_rank"])
        self.assertEqual(fixed["configuration_dof"], restored["configuration_dof"])
        self.assertTrue(all(value == 0 for value in fixed["final_preservation_residuals"]))

    def test_preservation_reaches_genuine_closure(self) -> None:
        chain = self.result["finite_k"]["generic_positive_gradient"]
        self.assertTrue(chain["lambda_constraint_was_generated"])
        self.assertTrue(all(value == 0 for value in chain["final_preservation_residuals"]))
        self.assertEqual(chain["new_constraints_after_final_stage"], ())
        self.assertIn(chain["shift_primary_multiplier"], chain["unfixed_primary_multipliers"])

    def test_zero_field_branch_is_recomputed_not_generic_rank_substitution(self) -> None:
        generic = self.result["finite_k"]["spatial_gauge_fixed"]
        zero = self.result["finite_k"]["exact_zero_field"]
        self.assertNotEqual(zero["poisson_rank"], generic["poisson_rank"])
        self.assertEqual(zero["trace_preservation_dependence_residual"], 0)
        self.assertEqual(zero["source_obstruction"], zero["source"])
        self.assertTrue(zero["source_obstruction_requires_vacuum"])
        self.assertTrue(zero["vacuum_only"])
        self.assertEqual(zero["configuration_dof"], 0)
        self.assertTrue(zero["rank_bifurcation"])
        self.assertTrue(zero["strong_coupling_not_excluded"])
        self.assertTrue(all(value == 0 for value in zero["final_preservation_residuals"]))
        self.assertEqual(zero["new_constraints_after_final_stage"], ())

    def test_homogeneous_constraint_symbol_does_not_freeze_expansion(self) -> None:
        zero_mode = self.result["k_zero"]
        self.assertEqual(zero_mode["C_pi"], 0)
        self.assertEqual(zero_mode["C_pi_on_flrw"], 0)
        self.assertNotEqual(zero_mode["flrw_trace_momentum"], 0)
        self.assertTrue(zero_mode["expansion_allowed_by_C_pi"])
        self.assertTrue(zero_mode["C_pi_does_not_algebraically_force_H_zero"])
        self.assertFalse(zero_mode["fresh_homogeneous_hessian_dirac_restart_performed"])
        self.assertFalse(zero_mode["viable_flrw_derived"])

    def test_mutations_are_live_and_fail_for_derived_reasons(self) -> None:
        mutations = self.result["mutations"]
        self.assertNotEqual(mutations["no_laplacian"]["constraint_on_flrw"], 0)
        self.assertTrue(mutations["no_laplacian"]["forces_H_zero"])
        self.assertTrue(mutations["lagrangian_lambda_K"]["forces_H_zero"])
        self.assertNotEqual(mutations["remove_mond"]["modulus_residual"], 0)
        self.assertGreater(
            mutations["remove_trace_constraint"]["configuration_dof"],
            self.result["finite_k"]["generic_positive_gradient"]["configuration_dof"],
        )

    def test_conditional_minimal_matter_ward_template(self) -> None:
        ward = self.result["matter_ward"]
        self.assertEqual(ward["on_shell_divergence"], 0)
        self.assertEqual(ward["auxiliary_direct_matter_derivative"], 0)
        self.assertNotEqual(ward["direct_coupling_mutation_defect"], 0)
        self.assertFalse(ward["explicit_matter_action_varied"])
        self.assertTrue(ward["conditional_on_diffeomorphism_invariant_minimal_Sm"])

    def test_conditional_circular_orbit_substitution_is_consistent(self) -> None:
        orbit = self.result["circular_orbit"]
        self.assertEqual(orbit["period_law_residual"], 0)
        self.assertEqual(orbit["newtonian_limit_residual"], 0)
        self.assertEqual(orbit["deep_mond_limit_residual"], 0)
        self.assertTrue(orbit["conditional_corollary_not_radially_varied_here"])

    def test_tensor_principal_block_is_unchanged_but_scope_is_bounded(self) -> None:
        tensor = self.result["tensor"]
        scope = self.result["scope"]
        self.assertTrue(tensor["positive_kinetic"])
        self.assertEqual(tensor["speed_squared"], 1)
        self.assertFalse(tensor["derived_from_displayed_full_action"])
        self.assertFalse(scope["tensor_sector_certified"])
        self.assertFalse(scope["full_nonlinear_functional_dirac_theorem"])
        self.assertFalse(scope["ppn_certified"])
        self.assertFalse(scope["novelty_claimed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
