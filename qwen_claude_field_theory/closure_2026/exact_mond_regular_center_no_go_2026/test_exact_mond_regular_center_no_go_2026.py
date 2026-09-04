#!/usr/bin/env python3
"""Adversarial tests for the exact-MOND regular-center obstruction."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "exact_mond_regular_center_no_go_2026.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "exact_mond_regular_center_no_go_2026", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load regular-center no-go module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExactMondRegularCenterNoGoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = _load_module()
        cls.result = cls.module.derive_regular_center_no_go()

    def test_exact_exponential_kernel_is_derived(self) -> None:
        kernel = self.result["kernel"]
        y = kernel["y"]
        self.assertEqual(kernel["mu_residual"], 0)
        self.assertEqual(kernel["mu_at_zero"], 0)
        self.assertEqual(kernel["deep_mond_slope"], 1)
        self.assertEqual(kernel["newtonian_limit"], 1)
        self.assertEqual(
            sp.simplify(
                kernel["parallel_eigenvalue"]
                - (1 + (y - 1) * sp.exp(-y))
            ),
            0,
        )

    def test_fitted_rar_nu_is_not_misidentified_as_exact_aqual_inverse(self) -> None:
        translation = self.result["rar_vs_aqual"]
        self.assertNotEqual(translation["rar_in_exact_inverse_residual"], 0)
        self.assertGreater(abs(translation["residual_at_yN_one"]), 0.25)
        self.assertLess(abs(translation["residual_at_yN_one"]), 0.27)
        self.assertNotEqual(translation["nu_rar_at_yN_one"], translation["nu_aqual_at_yN_one"])
        self.assertEqual(translation["shared_deep_leading_ratio"], 1)
        self.assertEqual(translation["nu_rar_newtonian_limit"], 1)

    def test_constitutive_jacobian_is_computed_and_collapses(self) -> None:
        jac = self.result["constitutive_jacobian"]
        self.assertEqual(jac["axis_off_diagonal_residual"], sp.zeros(3))
        self.assertEqual(jac["axis_transverse_residual"], 0)
        self.assertEqual(jac["axis_parallel_residual"], 0)
        self.assertEqual(jac["origin_limit"], sp.zeros(3))
        self.assertEqual(jac["origin_rank"], 0)

    def test_c2_critical_point_forces_zero_source(self) -> None:
        point = self.result["critical_point"]
        self.assertEqual(point["operator_at_critical_point"], 0)
        self.assertEqual(point["required_source_at_critical_point"], 0)
        self.assertTrue(point["positive_density_contradiction"])
        self.assertEqual(point["regularity_threshold"], "C2")

    def test_puiseux_branch_is_solved_not_inserted(self) -> None:
        spherical = self.result["spherical_core"]
        self.assertEqual(spherical["coefficient_equation_residuals"], (0, 0, 0, 0, 0))
        q = spherical["mass_correction_q"]
        expected = (
            sp.Integer(1),
            sp.Rational(1, 4),
            sp.Rational(7, 96),
            sp.Rational(1, 48),
            q / 2 + sp.Rational(491, 92160),
        )
        self.assertEqual(
            tuple(
                sp.simplify(actual - target)
                for actual, target in zip(spherical["coefficients"], expected)
            ),
            (0, 0, 0, 0, 0),
        )
        self.assertEqual(
            spherical["uniform_core_coefficients"][-1], sp.Rational(491, 92160)
        )
        self.assertEqual(spherical["series_residual_through_sixth_order"], 0)
        self.assertEqual(spherical["leading_acceleration_ratio"], 1)

    def test_positive_spherical_branch_is_unique(self) -> None:
        spherical = self.result["spherical_core"]
        self.assertEqual(spherical["flux_map_at_zero"], 0)
        self.assertTrue(spherical["flux_derivative_numerator_derivative_positive"])
        self.assertTrue(spherical["positive_inverse_branch_exists_and_is_unique"])

    def test_spherical_flux_solves_the_source_equation(self) -> None:
        spherical = self.result["spherical_core"]
        self.assertEqual(spherical["integrated_flux_residual"], 0)
        self.assertEqual(spherical["divergence_source_residual"], 0)

    def test_tidal_curvature_diverges_with_derived_coefficients(self) -> None:
        spherical = self.result["spherical_core"]
        self.assertEqual(spherical["radial_hessian_scaled_limit"], sp.Rational(1, 2))
        self.assertEqual(spherical["tangential_hessian_scaled_limit"], 1)
        self.assertEqual(spherical["laplacian_scaled_limit"], sp.Rational(5, 2))
        self.assertEqual(spherical["tidal_norm_squared_scaled_limit"], sp.Rational(9, 4))
        self.assertEqual(spherical["no_slip_ricci_scalar_scaled_limit"], 5)
        self.assertEqual(spherical["full_metric_ricci_scaled_limit"], 5)
        self.assertEqual(spherical["full_to_linear_ricci_ratio_limit"], 1)
        self.assertEqual(spherical["nonlinear_curvature_ratio_limit"], 0)
        self.assertTrue(spherical["hessian_diverges"])
        self.assertTrue(spherical["tidal_norm_squared_diverges"])
        self.assertTrue(spherical["no_slip_ricci_scalar_diverges"])

    def test_weak_solution_has_locally_finite_action(self) -> None:
        energy = self.result["weak_solution"]
        self.assertEqual(energy["primitive_cubic_ratio"], sp.Rational(2, 3))
        self.assertEqual(energy["radial_energy_power"], sp.Rational(7, 2))
        self.assertTrue(energy["radial_energy_integrable"])
        self.assertTrue(energy["weak_solution_exists"])
        self.assertFalse(energy["classical_c2_solution_exists"])

    def test_einstein_phantom_density_route_inherits_the_cusp(self) -> None:
        phantom = self.result["phantom_density"]
        self.assertEqual(phantom["effective_density_scaled_limit"], 5)
        self.assertEqual(phantom["phantom_density_scaled_limit"], 5)
        self.assertEqual(phantom["effective_mass_scaled_limit"], 1)
        self.assertEqual(phantom["effective_density_at_center"], sp.oo)
        self.assertEqual(phantom["effective_mass_at_center"], 0)
        self.assertTrue(phantom["density_cusp_integrable"])
        self.assertFalse(phantom["effective_stress_regular_at_center"])

    def test_central_kepler_law_and_exponential_corrections_are_derived(self) -> None:
        law = self.result["central_kepler_law"]
        t = law["t"]
        self.assertEqual(law["v_fourth_normalized_limit"], 1)
        self.assertEqual(law["period_fourth_normalized_limit"], 1)
        self.assertEqual(
            sp.series(law["v_fourth_correction_series"], t, 0, 4),
            1 + t / 2 + 5 * t**2 / 24 + 5 * t**3 / 64 + sp.Order(t**4),
        )
        self.assertEqual(
            sp.series(law["period_fourth_correction_series"], t, 0, 4),
            1 - t / 2 + t**2 / 24 + t**3 / 192 + sp.Order(t**4),
        )
        self.assertEqual(law["mond_period_log_slope"], sp.Rational(1, 4))
        self.assertEqual(law["newtonian_period_log_slope"], 0)

    def test_central_kepler_series_matches_independent_numeric_roots(self) -> None:
        numeric = self.result["central_kepler_law"]["numeric_audit"]
        errors = numeric["relative_errors"]
        self.assertTrue(all(error > 0 for error in errors))
        self.assertTrue(all(later < earlier for earlier, later in zip(errors, errors[1:])))
        self.assertLess(errors[-1], 1e-10)

    def test_regulator_is_a_real_negative_control(self) -> None:
        mutation = self.result["regulated_kernel"]
        self.assertNotEqual(mutation["mu_at_zero"], 0)
        self.assertEqual(mutation["origin_jacobian_rank"], 3)
        self.assertEqual(mutation["central_radial_hessian"], mutation["C"] / mutation["epsilon"])
        self.assertEqual(mutation["central_tangential_hessian"], mutation["C"] / mutation["epsilon"])
        self.assertTrue(mutation["central_tidal_norm_finite"])
        self.assertTrue(mutation["violates_exact_target"])

    def test_general_power_law_exposes_scope(self) -> None:
        general = self.result["power_law_scope"]
        self.assertEqual(general["acceleration_exponent"], 1 / (general["s"] + 1))
        self.assertEqual(general["hessian_exponent"], -general["s"] / (general["s"] + 1))
        self.assertTrue(general["all_positive_s_have_divergent_hessian"])

    def test_classification_does_not_overclaim_global_novelty(self) -> None:
        scope = self.result["scope"]
        self.assertEqual(scope["theorem_status"], "PROVED_UNDER_STATED_ASSUMPTIONS")
        self.assertEqual(scope["hpi_delta_status"], "DEAD_AS_AN_EXACT_CLASSICAL_REGULAR_CENTER_THEORY")
        self.assertFalse(scope["global_literature_novelty_claimed"])
        self.assertTrue(scope["weak_or_distributional_escape_remains"])
        self.assertTrue(scope["escape_fails_regular_classical_metric_gate"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
