#!/usr/bin/env python3
"""Adversarial tests for the finite-eccentricity exponential-MOND law."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest
import warnings

import sympy as sp


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "hpi_delta_eccentric_kepler_2026.py"
RECORDED_OUTPUT = HERE / "hpi_delta_eccentric_kepler_2026.out"
MANIFEST = HERE / "computation_manifest.json"


def _load_module():
    if not SCRIPT.exists():
        raise AssertionError(f"missing implementation: {SCRIPT.name}")
    spec = importlib.util.spec_from_file_location(
        "hpi_delta_eccentric_kepler_2026", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SymbolicFiniteEccentricLawTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = _load_module()
        cls.result = cls.module.derive_symbolic_law()

    def test_assumed_flux_is_nondimensionalized_without_inserting_an_orbit_law(self) -> None:
        result = self.result
        self.assertEqual(result["flux_residual"], 0)
        self.assertEqual(result["time_scale_residual"], 0)
        self.assertEqual(result["deep_force_residual"], 0)
        self.assertEqual(result["newton_force_residual"], 0)
        self.assertEqual(result["constitutive_slope_residual"], 0)
        self.assertEqual(result["full_force_h_slope_residual"], 0)

    def test_parametric_potential_differentiates_back_to_the_exact_force(self) -> None:
        result = self.result
        self.assertEqual(result["potential_chain_rule_residual"], 0)
        self.assertEqual(result["potential_parametric_derivative_residual"], 0)

    def test_turning_point_energy_and_angular_momentum_are_solved(self) -> None:
        result = self.result
        self.assertEqual(result["turning_point_pericenter_residual"], 0)
        self.assertEqual(result["turning_point_apocenter_residual"], 0)
        self.assertFalse(result["turning_lambda_squared"].has(result["symbols"]["energy"]))

    def test_newton_and_deep_scaling_laws_are_distinct(self) -> None:
        result = self.result
        self.assertEqual(result["newton_kepler_constant"], 4 * sp.pi**2)
        self.assertEqual(result["newton_circular_condition_residual"], 0)
        self.assertEqual(result["deep_circular_condition_residual"], 0)
        self.assertEqual(result["deep_epicycle_frequency_squared_residual"], 0)
        self.assertEqual(result["deep_circular_radial_period_scaled"], sp.sqrt(2) * sp.pi)
        self.assertEqual(result["deep_radial_period_scaled"], 2 * sp.sqrt(2 * sp.pi))
        self.assertEqual(result["deep_near_circular_apsidal_angle"], sp.sqrt(2) * sp.pi)
        self.assertEqual(result["deep_radial_apsidal_angle"], sp.pi)

    def test_deep_test_particle_virial_identity_beyond_circular_orbits(self) -> None:
        result = self.result
        self.assertEqual(result["deep_r_dot_grad_potential_residual"], 0)
        self.assertEqual(result["deep_mean_speed_squared"], 1)
        self.assertEqual(result["test_particle_virial_residual"], 0)

    def test_naive_semimajor_axis_substitution_is_analytically_falsified(self) -> None:
        result = self.result
        self.assertEqual(result["naive_deep_ratio_near_circular"], 4)
        self.assertEqual(result["naive_deep_ratio_radial_limit"], sp.pi**2 / 4)
        self.assertNotEqual(result["naive_deep_ratio_near_circular"], 1)
        self.assertNotEqual(result["naive_deep_ratio_radial_limit"], 1)


class DeepFiniteEccentricQuadratureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = _load_module()

    def test_deep_law_depends_only_on_eccentricity_after_scaling(self) -> None:
        for eccentricity in (0.1, 0.5, 0.9):
            with self.subTest(e=eccentricity):
                result = self.module.deep_log_orbit(eccentricity)
                self.assertLess(result["turning_residual_max"], 2.0e-12)
                self.assertGreater(result["radial_period_scaled"], 0.0)
                self.assertGreater(result["apsidal_angle"], math.pi)
                self.assertLess(result["apsidal_angle"], math.sqrt(2.0) * math.pi)
                self.assertLess(abs(result["mean_speed_squared"] - 1.0), 2.0e-9)

    def test_finite_eccentricity_is_not_the_epicycle_answer(self) -> None:
        result = self.module.deep_log_orbit(0.6)
        epicycle_angle = math.sqrt(2.0) * math.pi
        self.assertGreater(abs(result["apsidal_angle"] - epicycle_angle), 1.0e-2)
        self.assertFalse(result["epicycle_mutation_survives"])

    def test_deep_table_matches_independent_log_force_orbit_events(self) -> None:
        for eccentricity in (0.1, 0.6, 0.9):
            with self.subTest(e=eccentricity):
                result = self.module.validate_deep_log_orbit_ode(eccentricity)
                self.assertLess(result["period_relative_error"], 2.0e-9)
                self.assertLess(result["angle_relative_error"], 2.0e-9)
                self.assertLess(result["apocenter_relative_error"], 2.0e-9)
                self.assertGreaterEqual(result["force_evaluations"], 100)

    def test_near_circular_sequence_converges_to_epicycle_limit(self) -> None:
        errors = []
        for eccentricity in (0.1, 0.03, 0.01):
            result = self.module.deep_log_orbit(eccentricity)
            errors.append(abs(result["apsidal_angle"] - math.sqrt(2.0) * math.pi))
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])
        self.assertLess(errors[2], 1.0e-4)

    def test_extreme_near_circular_sequence_is_finite_and_warning_free(self) -> None:
        target = math.sqrt(2.0) * math.pi
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            for eccentricity in (3.0e-4, 1.0e-6, 1.0e-8):
                with self.subTest(e=eccentricity):
                    result = self.module.deep_log_orbit(eccentricity)
                    self.assertTrue(math.isfinite(result["radial_period_scaled"]))
                    self.assertTrue(math.isfinite(result["apsidal_angle"]))
                    self.assertLess(abs(result["radial_period_scaled"] - target), 1.0e-6)
                    self.assertLess(abs(result["apsidal_angle"] - target), 1.0e-6)
                    self.assertLess(abs(result["mean_speed_squared"] - 1.0), 2.0e-12)

    def test_near_radial_log_sequence_is_controlled_and_warning_free(self) -> None:
        period_limit = 2.0 * math.sqrt(2.0 * math.pi)
        previous_period = self.module.deep_log_orbit(0.9999)[
            "radial_period_scaled"
        ]
        previous_angle = self.module.deep_log_orbit(0.9999)["apsidal_angle"]
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = self.module.deep_log_orbit(0.99999)
        self.assertTrue(math.isfinite(result["radial_period_scaled"]))
        self.assertTrue(math.isfinite(result["apsidal_angle"]))
        self.assertGreater(result["radial_period_scaled"], previous_period)
        self.assertLess(result["radial_period_scaled"], period_limit)
        self.assertLess(result["apsidal_angle"], previous_angle)
        self.assertGreater(result["apsidal_angle"], math.pi)
        self.assertLess(result["precision_crosscheck_error"], 1.0e-20)

    def test_radial_limit_period_has_closed_gamma_integral(self) -> None:
        result = self.module.derive_radial_deep_limit()
        self.assertEqual(result["j_scaling_residual"], 0)
        self.assertEqual(result["energy_limit_residual"], 0)
        self.assertEqual(result["radial_function_scaling_residual"], 0)
        self.assertEqual(result["angular_prefactor_residual"], 0)
        self.assertEqual(result["gamma_integral_residual"], 0)
        self.assertEqual(result["half_angle_integral_residual"], 0)
        self.assertEqual(result["apsidal_angle_limit_residual"], 0)
        self.assertEqual(result["period_scaled"], 2 * sp.sqrt(2 * sp.pi))
        self.assertEqual(result["apsidal_angle_limit"], sp.pi)

    def test_endpoint_integrator_does_not_hide_negative_interior_radicand(self) -> None:
        def radicand(coordinate: float) -> float:
            if 0.49 < coordinate < 0.51:
                return -1.0e-14
            return coordinate * (1.0 - coordinate)

        with self.assertRaises(RuntimeError):
            self.module._endpoint_regularized_integral(
                0.0,
                1.0,
                radicand,
                lambda coordinate: 1.0 - 2.0 * coordinate,
                lambda _coordinate, _value: 1.0,
            )


class FullExponentialTurningPointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = _load_module()

    def test_full_exponential_quadrature_hits_both_supplied_turning_radii(self) -> None:
        result = self.module.full_exponential_orbit(0.7, 2.3)
        self.assertLess(result["turning_residual_max"], 2.0e-10)
        self.assertGreater(result["radial_period_dimensionless"], 0.0)
        self.assertGreater(result["apsidal_angle"], 0.0)

    def test_numerical_force_solver_preserves_exponential_flux_across_scales(self) -> None:
        previous_y = math.inf
        for x in (1.0e-3, 1.0e-2, 0.1, 1.0, 10.0, 1.0e3, 1.0e6):
            with self.subTest(x=x):
                y = self.module.solve_dimensionless_acceleration(x)
                source = x**-2
                relative_residual = abs(
                    y * self.module.mu_exponential(y) - source
                ) / source
                self.assertLess(relative_residual, 5.0e-10)
                self.assertLess(y, previous_y)
                previous_y = y

    def test_transition_quadrature_matches_independent_nonlinear_orbit_events(self) -> None:
        result = self.module.validate_full_orbit_ode(0.7, 2.3)
        self.assertLess(result["period_relative_error"], 2.0e-8)
        self.assertLess(result["angle_relative_error"], 2.0e-8)
        self.assertLess(result["apocenter_relative_error"], 2.0e-8)
        self.assertGreaterEqual(result["force_evaluations"], 100)

    def test_extreme_near_circular_full_force_uses_stable_scaled_quadrature(self) -> None:
        x_p, x_a = 1.0, 1.0 + 1.0e-7
        mean_radius = (x_p + x_a) / 2.0
        y = self.module.solve_dimensionless_acceleration(mean_radius)
        omega = math.sqrt(y / mean_radius)
        kappa_over_omega = math.sqrt(
            (math.exp(y) - 1.0 + 3.0 * y)
            / (math.exp(y) - 1.0 + y)
        )
        expected_period = 2.0 * math.pi / (omega * kappa_over_omega)
        expected_angle = 2.0 * math.pi / kappa_over_omega
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = self.module.full_exponential_orbit(x_p, x_a)
        self.assertTrue(math.isfinite(result["radial_period_dimensionless"]))
        self.assertTrue(math.isfinite(result["apsidal_angle"]))
        self.assertLess(
            abs(result["radial_period_dimensionless"] / expected_period - 1.0),
            2.0e-7,
        )
        self.assertLess(abs(result["apsidal_angle"] / expected_angle - 1.0), 2.0e-7)

    def test_full_force_numeric_branches_are_continuous_at_safe_cutover(self) -> None:
        for mean_radius in (0.02, 1.0, 100.0):
            with self.subTest(mean_radius=mean_radius):
                eccentricity = 0.0201
                x_p = mean_radius * (1.0 - eccentricity)
                x_a = mean_radius * (1.0 + eccentricity)
                dense = self.module.full_exponential_orbit(x_p, x_a)
                scaled = self.module._full_exponential_orbit_near_circular_mp(
                    x_p, x_a
                )
                self.assertEqual(scaled["numerical_branch"], "scaled_mpmath")
                self.assertEqual(dense["numerical_branch"], "dense_potential")
                self.assertLess(
                    abs(
                        scaled["radial_period_dimensionless"]
                        / dense["radial_period_dimensionless"]
                        - 1.0
                    ),
                    2.0e-8,
                )
                self.assertLess(
                    abs(
                        scaled["apsidal_angle"] / dense["apsidal_angle"] - 1.0
                    ),
                    2.0e-8,
                )

    def test_newtonian_limit_recovers_eccentricity_independent_kepler_law(self) -> None:
        result = self.module.full_exponential_orbit(0.01, 0.03)
        self.assertLess(abs(result["newton_period_ratio"] - 1.0), 2.0e-8)
        self.assertLess(abs(result["apsidal_angle"] / (2.0 * math.pi) - 1.0), 2.0e-8)

    def test_deep_limit_collapses_to_universal_eccentric_law(self) -> None:
        eccentricity = 0.5
        deep = self.module.deep_log_orbit(eccentricity)
        full = self.module.full_exponential_orbit(1000.0, 3000.0)
        self.assertLess(
            abs(full["radial_period_over_mean_radius"] / deep["radial_period_scaled"] - 1.0),
            8.0e-4,
        )
        self.assertLess(abs(full["apsidal_angle"] / deep["apsidal_angle"] - 1.0), 8.0e-4)


class AuditAndCliTests(unittest.TestCase):
    def test_full_audit_is_bounded_and_live(self) -> None:
        module = _load_module()
        audit = module.run_full_audit()
        self.assertTrue(audit["passed"])
        self.assertTrue(all(audit["checks"].values()))
        self.assertTrue(audit["checks"]["numerical_exponential_force_solver"])
        self.assertTrue(audit["checks"]["full_transition_retains_scale_dependence"])
        self.assertEqual(len(audit["deep_ode_grid"]), 3)
        self.assertLess(audit["max_deep_ode_error"], 2.0e-9)
        self.assertEqual(len(audit["transition_ode_grid"]), 3)
        self.assertLess(audit["max_transition_ode_error"], 2.0e-8)
        self.assertFalse(audit["scope"]["proves_relativistic_closure"])
        self.assertFalse(audit["scope"]["proves_novelty"])
        self.assertTrue(audit["scope"]["requires_spherical_exterior"])
        self.assertFalse(audit["scope"]["includes_external_field_effect"])

    def test_cli_emits_machine_readable_result(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=HERE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("FINITE-ECCENTRICITY KEPLER LAW", completed.stdout)
        self.assertIn("CERTIFICATE_JSON:", completed.stdout)
        self.assertIn('"status": "PASS_BOUNDED"', completed.stdout)
        self.assertEqual(completed.stdout, RECORDED_OUTPUT.read_text())
        manifest = json.loads(MANIFEST.read_text())
        recorded_hash = hashlib.sha256(RECORDED_OUTPUT.read_bytes()).hexdigest()
        self.assertEqual(recorded_hash, manifest["outputs"][0]["sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
