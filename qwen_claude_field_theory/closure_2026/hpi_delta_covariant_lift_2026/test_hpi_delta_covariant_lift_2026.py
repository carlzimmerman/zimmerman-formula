#!/usr/bin/env python3
"""Adversarial tests for the HPI-Delta configuration/covariant lift gate."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "hpi_delta_covariant_lift_2026.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("hpi_delta_covariant_lift_2026", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load HPI-Delta covariant-lift module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HpiDeltaCovariantLiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = _load_module()
        cls.result = cls.module.derive_covariant_lift_gate()

    def test_exponential_constitutive_law_is_derived(self) -> None:
        kernel = self.result["kernel"]
        y = kernel["y"]
        self.assertEqual(kernel["mu_residual"], 0)
        self.assertEqual(
            sp.simplify(kernel["lambda_perp"] - (1 - sp.exp(-y))), 0
        )
        self.assertEqual(
            sp.simplify(
                kernel["lambda_parallel"] - (1 + (y - 1) * sp.exp(-y))
            ),
            0,
        )
        self.assertEqual(kernel["deep_primitive_ratio"], sp.Rational(2, 3))

    def test_constitutive_map_has_a_rank_zero_degenerate_origin(self) -> None:
        kernel = self.result["kernel"]
        y = kernel["y"]
        self.assertEqual(kernel["zero_perpendicular"], 0)
        self.assertEqual(kernel["zero_parallel"], 0)
        self.assertEqual(
            sp.simplify(
                kernel["positive_y_derivative"]
                - (1 + (y - 1) * sp.exp(-y))
            ),
            0,
        )
        for value in (sp.Rational(1, 100), sp.Rational(1, 3), 1, 3, 20):
            self.assertGreater(float(kernel["lambda_perp"].subs(y, value)), 0.0)
            self.assertGreater(float(kernel["lambda_parallel"].subs(y, value)), 0.0)

    def test_legendre_map_reconstructs_the_first_order_hamiltonian(self) -> None:
        lift = self.result["legendre_lift"]
        self.assertEqual(lift["trace_momentum_residual"], 0)
        self.assertEqual(lift["velocity_inversion_residuals"], (0, 0, 0))
        self.assertEqual(lift["hamiltonian_residual"], 0)
        self.assertNotEqual(lift["constraint_coupling"], 0)
        self.assertTrue(lift["expected_hamiltonian"].has(lift["sqrt_h"]))

    def test_lambda_variation_is_exactly_the_trace_momentum_constraint(self) -> None:
        auxiliary = self.result["auxiliary_equation"]
        self.assertEqual(auxiliary["euler_residual"], 0)
        self.assertEqual(auxiliary["constraint_residual"], 0)
        self.assertEqual(auxiliary["lambda_velocity_hessian"], 0)

    def test_weak_static_phi_and_psi_are_varied_separately(self) -> None:
        weak = self.result["weak_static"]
        self.assertEqual(weak["psi_equation_residual"], 0)
        self.assertEqual(weak["phi_on_slip_aqual_residual"], 0)
        self.assertFalse(weak["slip_inserted_before_variation"])

    def test_finite_k_dirac_matrix_is_inherited_from_the_same_hamiltonian(self) -> None:
        chain = self.result["finite_k_dirac"]
        self.assertEqual(chain["legendre_bridge_residual"], 0)
        self.assertEqual(
            chain["constraint_jacobian_rank"], len(chain["constraints"])
        )
        self.assertEqual(chain["poisson_rank"], chain["poisson_sample_rank"])
        self.assertEqual(
            chain["first_class_count"] + chain["second_class_count"],
            len(chain["constraints"]),
        )
        self.assertEqual(chain["scalar_configuration_dof"], 0)
        self.assertNotEqual(chain["rank_witness_determinant"], 0)

    def test_k_zero_and_nonzero_are_not_conflated(self) -> None:
        sectors = self.result["mode_sectors"]
        self.assertTrue(sectors["finite_k_constraint_active"])
        self.assertEqual(sectors["homogeneous_constraint_symbol"], 0)
        self.assertTrue(sectors["homogeneous_restart_required"])

    def test_sourced_zero_field_core_is_weak_but_not_c2(self) -> None:
        core = self.result["zero_field_core"]
        self.assertEqual(core["flux_identity_residual"], 0)
        self.assertEqual(core["source_equation_residual"], 0)
        self.assertEqual(core["deep_central_ratio"], 1)
        self.assertEqual(core["flux_at_origin"], 0)
        self.assertTrue(core["linearized_source_obstruction_is_not_nonlinear_no_go"])
        self.assertTrue(core["finite_action_weak_solution_exists"])
        self.assertTrue(core["hessian_diverges"])
        self.assertTrue(core["no_slip_ricci_scalar_diverges"])
        self.assertFalse(core["classical_c2_regular_center_exists"])

    def test_flrw_background_is_einstein_and_can_expand(self) -> None:
        flrw = self.result["flrw"]
        self.assertEqual(flrw["acceleration_squared"], 0)
        self.assertEqual(flrw["auxiliary_b"], 0)
        self.assertEqual(flrw["F_background"], 0)
        self.assertEqual(flrw["lambda_equation"], 0)
        self.assertEqual(flrw["friedmann_residual"], 0)
        self.assertNotEqual(flrw["de_sitter_H"], 0)
        self.assertEqual(flrw["primary_preservation_residuals"], (0, 0))
        self.assertEqual(flrw["secondary_preservation_residual"], 0)
        self.assertEqual(
            flrw["first_class_count"] + flrw["second_class_count"],
            len(flrw["constraints"]),
        )
        self.assertEqual(flrw["constraint_jacobian_rank"], len(flrw["constraints"]))
        self.assertEqual(flrw["poisson_rank"], flrw["poisson_matrix"].rank())
        self.assertEqual(flrw["homogeneous_gravitational_configuration_dof"], 0)

    def test_tensor_block_is_luminal_and_positive(self) -> None:
        tensor = self.result["tensor"]
        self.assertEqual(tensor["auxiliary_tt_coupling"], 0)
        self.assertEqual(tensor["mond_tt_coupling"], 0)
        self.assertEqual(tensor["speed_squared"], 1)
        self.assertTrue(tensor["positive_kinetic"])

    def test_high_acceleration_limit_is_gr_plus_a_cosmological_shift(self) -> None:
        high = self.result["high_acceleration"]
        self.assertEqual(high["F_limit"], -2)
        self.assertEqual(high["F_prime_limit"], 0)
        self.assertEqual(high["F_second_limit"], 0)
        self.assertEqual(high["lambda_effective_residual"], 0)
        self.assertTrue(high["cmc_constraint_is_gr_gauge_fixing_only_in_this_limit"])

    def test_minimal_matter_ward_identity_is_separate(self) -> None:
        ward = self.result["ward_identity"]
        self.assertEqual(ward["matter_on_shell_divergence"], 0)
        self.assertEqual(ward["clock_equation_on_other_shells"], 0)
        self.assertFalse(ward["auxiliary_depends_on_matter_fields"])

    def test_action_is_one_metric_and_scope_is_honestly_classified(self) -> None:
        action = self.result["action"]
        scope = self.result["scope"]
        self.assertEqual(action["physical_metric_count"], 1)
        self.assertTrue(action["matter_minimal_to_physical_metric"])
        self.assertTrue(action["clock_gradient_required_timelike"])
        self.assertEqual(
            scope["candidate_status"],
            "DEAD_AS_AN_EXACT_CLASSICAL_REGULAR_CENTER_THEORY",
        )
        self.assertFalse(scope["static_zero_field_c2_regular"])
        self.assertTrue(scope["conditional_regular_center_no_go_proved"])
        self.assertFalse(scope["full_nonlinear_functional_dirac_closed"])
        self.assertFalse(scope["boosted_ppn_closed"])
        self.assertFalse(scope["global_stability_closed"])

    def test_mutations_break_load_bearing_links(self) -> None:
        mutations = self.result["mutations"]
        self.assertNotEqual(mutations["drop_b_square"]["hamiltonian_residual"], 0)
        self.assertNotEqual(mutations["wrong_b_coefficient"]["constraint_residual"], 0)
        self.assertEqual(mutations["newtonian_kernel"]["mu"], 1)
        self.assertNotEqual(mutations["newtonian_kernel"]["mu"], self.result["kernel"]["mu"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
