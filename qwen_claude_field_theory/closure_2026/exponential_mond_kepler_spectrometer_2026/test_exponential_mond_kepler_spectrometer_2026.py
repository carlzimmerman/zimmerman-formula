#!/usr/bin/env python3
"""Tests for the exact-exponential MOND two-clock/curvature derivation."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import unittest

import mpmath as mp
import sympy as sp


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "exponential_mond_kepler_spectrometer_2026.py"
SPEC = importlib.util.spec_from_file_location("kepler_spectrometer", MODULE_PATH)
KS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(KS)


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ActionVariationTests(unittest.TestCase):
    def test_primitive_is_derived_not_assigned(self) -> None:
        d = KS.derive_action_and_flux()
        self.assertEqual(sp.simplify(d["mu"] - (1 - sp.exp(-d["y"]))), 0)
        self.assertEqual(sp.simplify(d["primitive_at_zero"]), 0)

    def test_independent_radial_variations_give_slip_and_mond(self) -> None:
        d = KS.derive_action_and_flux()
        self.assertEqual(sp.simplify(d["psi_euler_residual"]), 0)
        self.assertEqual(sp.simplify(d["phi_mond_residual"]), 0)

    def test_action_mutation_is_detected(self) -> None:
        d = KS.derive_action_and_flux(eh_psi_gradient_coefficient=sp.Integer(2))
        self.assertNotEqual(sp.simplify(d["slip_ratio"] - 1), 0)
        self.assertNotEqual(sp.simplify(d["effective_mu"] - (1 - sp.exp(-d["y"]))), 0)


class GeometryDerivationTests(unittest.TestCase):
    def test_curvature_is_generated_from_linearized_riemann(self) -> None:
        d = KS.derive_curvature_from_metric()
        p, t = d["p"], d["t"]
        self.assertEqual(sp.simplify(d["R_noslip"] - 2 * (p + 2 * t)), 0)
        self.assertEqual(
            sp.simplify(d["K_noslip"] - (12 * p**2 + 16 * p * t + 32 * t**2)),
            0,
        )
        self.assertGreater(d["nonzero_riemann_components"], 0)

    def test_phi_and_psi_are_kept_separate_before_noslip(self) -> None:
        d = KS.derive_curvature_from_metric()
        self.assertTrue(d["R_general"].has(d["p_phi"]))
        self.assertTrue(d["R_general"].has(d["p_psi"]))
        self.assertTrue(d["K_general"].has(d["p_phi"]))
        self.assertTrue(d["K_general"].has(d["p_psi"]))

    def test_spatial_metric_sign_mutation_is_detected(self) -> None:
        good = KS.derive_curvature_from_metric(spatial_sign=-1)
        bad = KS.derive_curvature_from_metric(spatial_sign=1)
        self.assertNotEqual(sp.simplify(good["R_noslip"] - bad["R_noslip"]), 0)

    def test_orbit_elimination_gives_two_clock_curvature_law(self) -> None:
        d = KS.derive_orbit_and_clock_relations()
        Om2, kap2 = d["Omega2"], d["kappa2"]
        self.assertEqual(sp.simplify(d["derived_Omega2"] - d["t"]), 0)
        self.assertEqual(
            sp.simplify(d["derived_kappa2"] - (d["p"] + 3 * d["t"])), 0
        )
        self.assertEqual(sp.simplify(d["R_clock"] - 2 * (kap2 - Om2)), 0)
        self.assertEqual(
            sp.simplify(d["K_clock"] - 4 * (3 * kap2**2 - 14 * kap2 * Om2 + 23 * Om2**2)),
            0,
        )

    def test_newton_deep_and_center_curvature_fingerprints(self) -> None:
        fingerprints = KS.curvature_fingerprints()
        self.assertEqual(fingerprints["newton"]["R_over_Omega2"], 0)
        self.assertEqual(fingerprints["newton"]["K_over_Omega4"], 48)
        self.assertEqual(fingerprints["deep_mond"]["R_over_Omega2"], 2)
        self.assertEqual(fingerprints["deep_mond"]["K_over_Omega4"], 28)
        self.assertEqual(fingerprints["regular_center"]["R_over_Omega2"], 5)
        self.assertEqual(fingerprints["regular_center"]["K_over_Omega4"], 43)


class ExactExponentialSpectrometerTests(unittest.TestCase):
    def test_forward_transition_is_derived_from_exterior_flux(self) -> None:
        d = KS.derive_exponential_transition()
        y, L = d["y"], d["L"]
        self.assertEqual(sp.simplify(L - y / (sp.exp(y) - 1)), 0)
        self.assertEqual(
            sp.simplify(d["q"] - (1 + 3 * L) / (1 + L)),
            0,
        )
        self.assertEqual(
            sp.simplify(d["R_over_Omega2"] - 4 * y / (sp.exp(y) - 1 + y)),
            0,
        )

    def test_lambert_minus_one_branch_inverts_forward_map(self) -> None:
        for y in (0.03, 0.2, 1.0, 2.65, 7.0, 20.0):
            q = KS.clock_ratio_from_y(y)
            recovered = KS.y_from_clock_ratio(q)
            self.assertAlmostEqual(recovered / y, 1.0, places=10)

    def test_principal_lambert_branch_is_rejected(self) -> None:
        q = KS.clock_ratio_from_y(1.0)
        principal = KS.y_from_clock_ratio(q, branch=0)
        physical = KS.y_from_clock_ratio(q, branch=-1)
        self.assertLess(abs(principal), 1e-12)
        self.assertGreater(physical, 0.9)

    def test_two_clocks_recover_mass_and_a0_without_mass_input(self) -> None:
        G = 6.67430e-11
        M = 4.2e40
        a0 = 9.4e-11
        for y in (0.25, 1.0, 3.0):
            mu = 1.0 - math.exp(-y)
            # mu*a0*y=GM/r^2 from the varied spherical field equation.
            r = math.sqrt(G * M / (a0 * y * mu))
            omega = math.sqrt(a0 * y / r)
            q = KS.clock_ratio_from_y(y)
            kappa = omega * math.sqrt(q)
            estimate = KS.infer_mass_and_a0(r, omega, kappa, G=G)
            self.assertAlmostEqual(estimate["a0"] / a0, 1.0, places=10)
            self.assertAlmostEqual(estimate["mass"] / M, 1.0, places=10)

    def test_clock_domain_is_falsifiable(self) -> None:
        for y in (-1, 0):
            with self.assertRaisesRegex(ValueError, "requires y>0"):
                KS.clock_ratio_from_y(y)
        for q in (0.99, 1.0, 2.0, 2.01, 2.5):
            with self.assertRaises(ValueError):
                KS.y_from_clock_ratio(q)

    def test_optimal_fractional_conditioning_is_computed(self) -> None:
        optimum = KS.find_best_conditioned_acceleration()
        self.assertTrue(2.5 < optimum["y"] < 3.5)
        self.assertTrue(1.2 < optimum["q"] < 1.35)
        self.assertTrue(2.4 < optimum["fractional_condition"] < 2.7)
        self.assertTrue(optimum["optimizer_no_worse_than_grid"])
        self.assertEqual(optimum["grid_points"], 4001)
        left = KS.fractional_condition_number(optimum["y"] * 0.8)
        right = KS.fractional_condition_number(optimum["y"] * 1.2)
        self.assertLess(optimum["fractional_condition"], left)
        self.assertLess(optimum["fractional_condition"], right)

    def test_high_precision_residual_not_a_circular_formula_check(self) -> None:
        mp.mp.dps = 80
        for y in (mp.mpf("1e-8"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("30")):
            q = KS.clock_ratio_from_y(y)
            yr = KS.y_from_clock_ratio(q, dps=80)
            residual = yr / mp.expm1(yr) - (q - 1) / (3 - q)
            self.assertLess(abs(residual), mp.mpf("1e-60"))

    def test_adaptive_precision_resolves_both_asymptotic_endpoints(self) -> None:
        with mp.workdps(350):
            for y in (mp.mpf("1e-100"), mp.mpf("1e-50"), mp.mpf("200")):
                q = KS.clock_ratio_from_y(y)
                recovered = KS.y_from_clock_ratio(q)
                self.assertLess(abs(recovered / y - 1), mp.mpf("1e-55"))

    def test_parameter_inference_preserves_high_precision_clock_inputs(self) -> None:
        with mp.workdps(350):
            y = mp.mpf("1e-50")
            mu = -mp.expm1(-y)
            radius = mp.sqrt(1 / (y * mu))
            omega = mp.sqrt(y / radius)
            q = KS.clock_ratio_from_y(y)
            kappa = omega * mp.sqrt(q)
            estimate = KS.infer_mass_and_a0(radius, omega, kappa, G=mp.mpf(1))
            self.assertLess(abs(estimate["a0"] - 1), mp.mpf("1e-50"))
            self.assertLess(abs(estimate["mass"] - 1), mp.mpf("1e-50"))


class RecordedArtifactTests(unittest.TestCase):
    def test_primary_result_ledger_matches_live_derivation(self) -> None:
        recorded = json.loads((HERE / "calculation_results.json").read_text())
        live = KS.build_results()
        for section in (
            "action",
            "geometry",
            "fingerprints",
            "certificates",
        ):
            self.assertEqual(recorded[section], live[section])
        recorded_exponential = dict(recorded["exponential_exterior"])
        live_exponential = dict(live["exponential_exterior"])
        recorded_residual = recorded_exponential.pop("inverse_numeric_residual_y_1")
        live_residual = live_exponential.pop("inverse_numeric_residual_y_1")
        self.assertEqual(recorded_exponential, live_exponential)
        self.assertLess(recorded_residual, 1e-60)
        self.assertLess(live_residual, 1e-60)
        self.assertTrue(all(live["certificates"].values()))
        for key in ("y", "q", "kappa_over_omega", "fractional_condition"):
            self.assertAlmostEqual(
                recorded["best_fractional_conditioning"][key],
                live["best_fractional_conditioning"][key],
                places=11,
            )

    def test_independent_metric_ledger_matches_live_exact_metric(self) -> None:
        module = load_module("independent_metric", "independent_metric_audit.py")
        recorded = json.loads((HERE / "independent_metric_results.json").read_text())
        self.assertEqual(recorded, module.audit())

    def test_independent_orbit_summary_matches_live_integrations(self) -> None:
        module = load_module("independent_orbit", "independent_orbit_audit.py")
        recorded = json.loads((HERE / "independent_orbit_results.json").read_text())
        rows = [module.audit_orbit(y) for y in recorded["sampled_y"]]
        live = {
            "max_relative_GM_recovery_error": max(
                abs(row["relative_GM_error"]) for row in rows
            ),
            "max_relative_a0_recovery_error": max(
                abs(row["relative_a0_error"]) for row in rows
            ),
            "max_relative_q_error_direct_orbit": max(
                abs(row["relative_q_error_orbit"]) for row in rows
            ),
            "max_relative_q_error_finite_difference": max(
                abs(row["relative_q_error_finite_difference"]) for row in rows
            ),
        }
        bounds = {
            "max_relative_GM_recovery_error": 2e-6,
            "max_relative_a0_recovery_error": 2e-6,
            "max_relative_q_error_direct_orbit": 5e-8,
            "max_relative_q_error_finite_difference": 5e-8,
        }
        for key, bound in bounds.items():
            self.assertLess(recorded[key], bound)
            self.assertLess(live[key], bound)


if __name__ == "__main__":
    unittest.main(verbosity=2)
