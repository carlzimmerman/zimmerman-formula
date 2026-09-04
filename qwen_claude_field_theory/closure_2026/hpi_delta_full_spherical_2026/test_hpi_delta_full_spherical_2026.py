#!/usr/bin/env python3
"""Tests for the full static-spherical HPI-Delta action audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "hpi_delta_full_spherical_2026.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "hpi_delta_full_spherical_2026", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load full-action spherical audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HpiDeltaFullSphericalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = _load_module()
        cls.result = cls.module.derive_full_spherical_audit()

    def test_derivation_module_exists(self) -> None:
        self.assertTrue(
            MODULE_PATH.is_file(),
            "the full-action spherical derivation module has not been implemented",
        )

    def test_reduction_retains_every_load_bearing_radial_field(self) -> None:
        geometry = self.result["geometry"]
        self.assertEqual(
            geometry["field_names"], ("N", "A", "R", "beta", "lambda")
        )
        self.assertEqual(geometry["kinetic_expansion_residual"], 0)
        self.assertEqual(geometry["flat_spatial_curvature"], 0)
        self.assertEqual(geometry["unit_three_sphere_curvature"], 6)
        self.assertEqual(geometry["flat_lambda_laplacian_residual"], 0)

    def test_lambda_and_shift_equations_are_actual_variations(self) -> None:
        auxiliary = self.result["auxiliary_equations"]
        self.assertEqual(auxiliary["lambda_equation_residual"], 0)
        self.assertEqual(auxiliary["shift_equation_residual"], 0)
        self.assertNotEqual(auxiliary["lambda_equation"], 0)
        self.assertNotEqual(auxiliary["shift_equation"], 0)
        self.assertEqual(auxiliary["lambda_velocity_hessian"], 0)

    def test_isolated_regular_branch_eliminates_shift_and_multiplier(self) -> None:
        branch = self.result["isolated_branch"]
        self.assertEqual(branch["harmonic_solution_residual"], 0)
        self.assertEqual(branch["momentum_solution_residual"], 0)
        self.assertEqual(branch["isotropic_barred_curvature_residual"], 0)
        self.assertEqual(branch["central_auxiliary_charge_solution"], 0)
        self.assertTrue(branch["traceless_mode_action_diverges"])
        self.assertEqual(branch["shift_solution_residual"], 0)
        self.assertEqual(branch["isolated_shift_constant"], 0)
        self.assertEqual(branch["regular_lambda_flux_constant"], 0)

    def test_exact_metric_equations_follow_from_the_reduced_action(self) -> None:
        equations = self.result["metric_equations"]
        noether = self.result["radial_noether_identity"]
        self.assertEqual(equations["raw_vs_first_order_boundary_residual"], 0)
        self.assertEqual(equations["lapse_equation_residual"], 0)
        self.assertEqual(equations["radial_equation_residual"], 0)
        self.assertEqual(equations["angular_equation_residual"], 0)
        self.assertTrue(
            all(
                residual == 0
                for residual in noether[
                    "zero_branch_full_kinetic_metric_variation_residuals"
                ]
            )
        )

    def test_radial_diffeomorphism_identity_survives_the_reduction(self) -> None:
        noether = self.result["radial_noether_identity"]
        self.assertEqual(noether["static_metric_residual"], 0)
        self.assertEqual(noether["full_kinetic_residual"], 0)

    def test_classical_center_requires_a_fine_tuned_active_density(self) -> None:
        smooth = self.result["center"]["smooth"]
        G, rho, pressure, Lambda = (
            smooth["G"], smooth["rho"], smooth["pressure"], smooth["Lambda"]
        )
        self.assertEqual(smooth["radial_coefficient_residual"], 0)
        self.assertEqual(smooth["lapse_coefficient_residual"], 0)
        self.assertEqual(
            sp.simplify(
                smooth["required_active_density"] - Lambda / (4 * sp.pi * G)
            ),
            0,
        )
        self.assertNotEqual(
            smooth["compatibility_residual"].subs(
                {G: 1, rho: 1, pressure: 0, Lambda: 0}
            ),
            0,
        )

    def test_puiseux_coefficients_are_solved_from_both_metric_equations(self) -> None:
        puiseux = self.result["center"]["puiseux"]
        self.assertEqual(puiseux["radial_solution_residual"], 0)
        self.assertEqual(puiseux["lapse_solution_residual"], 0)
        self.assertEqual(
            sp.simplify(
                puiseux["c_squared"]
                - (
                    4 * sp.pi * puiseux["G"]
                    * (puiseux["rho"] + 3 * puiseux["pressure"])
                    - puiseux["Lambda"]
                )
                / (3 * puiseux["ell"])
            ),
            0,
        )

    def test_curvature_is_derived_directly_and_benchmarked(self) -> None:
        curvature = self.result["curvature"]
        self.assertEqual(curvature["ricci_formula_residual"], 0)
        self.assertEqual(curvature["kretschmann_formula_residual"], 0)
        self.assertEqual(curvature["core_ricci_scaled_limit"], 5 * curvature["c"])
        self.assertEqual(
            curvature["core_kretschmann_scaled_limit"], 43 * curvature["c"] ** 2
        )
        self.assertEqual(curvature["minkowski"], (0, 0))
        self.assertEqual(curvature["schwarzschild_ricci"], 0)
        self.assertEqual(
            curvature["schwarzschild_kretschmann"],
            48 * curvature["mass"] ** 2 / curvature["r"] ** 6,
        )
        self.assertEqual(curvature["de_sitter_ricci"], 12 * curvature["H"] ** 2)
        self.assertEqual(
            curvature["de_sitter_kretschmann"], 24 * curvature["H"] ** 4
        )

    def test_mutations_identify_the_exact_degenerate_coefficient(self) -> None:
        mutations = self.result["mutations"]
        self.assertEqual(mutations["gr_center_radial_residual"], 0)
        self.assertEqual(mutations["gr_center_lapse_residual"], 0)
        self.assertEqual(mutations["regulated_center_residual"], 0)
        self.assertTrue(mutations["regulated_center_is_finite"])
        self.assertNotEqual(mutations["coordinate_laplacian_noether_defect"], 0)
        self.assertNotEqual(mutations["wrong_b_square_constraint_residual"], 0)
        self.assertEqual(mutations["premature_shift_equation"], 0)
        self.assertNotEqual(
            mutations["premature_shift_equation"],
            self.result["auxiliary_equations"]["shift_equation"],
        )

    def test_verdict_is_scoped_to_the_action_and_branch_actually_computed(self) -> None:
        scope = self.result["scope"]
        self.assertEqual(
            scope["candidate_status"],
            "DEAD_UNDER_ISOLATED_STATIC_CLASSICAL_REGULAR_CENTER_REQUIREMENTS",
        )
        self.assertTrue(scope["full_static_spherical_action_varied"])
        self.assertTrue(scope["radial_shift_and_lambda_varied_before_branching"])
        self.assertFalse(scope["full_nonlinear_dirac_completed"])
        self.assertFalse(scope["boosted_ppn_completed"])
        self.assertFalse(scope["cosmological_cmc_branch_excluded"])
        self.assertFalse(scope["global_novelty_claimed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
