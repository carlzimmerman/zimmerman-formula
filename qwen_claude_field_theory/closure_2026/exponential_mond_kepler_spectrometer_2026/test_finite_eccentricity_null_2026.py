#!/usr/bin/env python3
"""Tests for the finite-eccentricity clock correction and radius null."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import unittest

import sympy as sp


HERE = Path(__file__).resolve().parent
PATH = HERE / "finite_eccentricity_null_2026.py"
SPEC = importlib.util.spec_from_file_location("finite_e_null", PATH)
FEN = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(FEN)


class GenericFiniteAmplitudeTests(unittest.TestCase):
    def test_turning_point_exchange_forces_even_observable_series(self) -> None:
        d = FEN.derive_turning_point_parity()
        self.assertEqual(d["odd_mean_radius_linear"], 0)
        self.assertEqual(d["odd_mean_radius_cubic"], 0)
        self.assertEqual(d["mean_radius_quadratic_residual"], 0)
        self.assertEqual(d["turning_equation_evenness_residual"], 0)
        self.assertEqual(d["radial_frequency_linear"], 0)
        self.assertEqual(d["radial_frequency_cubic"], 0)
        self.assertEqual(d["azimuthal_mean_linear"], 0)
        self.assertEqual(d["azimuthal_mean_cubic"], 0)
        self.assertEqual(d["signed_eccentricity_quadratic"], 0)
        self.assertEqual(d["signed_eccentricity_quartic"], 0)
        self.assertNotEqual(d["radial_frequency_cubic_negative_control"], 0)

    def test_poincare_lindstedt_coefficients_are_generated(self) -> None:
        d = FEN.derive_generic_finite_amplitude()
        q, u3, u4 = d["q"], d["u3"], d["u4"]
        self.assertEqual(sp.simplify(d["order2_constant_residual"]), 0)
        self.assertEqual(sp.simplify(d["order2_second_harmonic_residual"]), 0)
        self.assertEqual(sp.simplify(d["order3_secular_residual"]), 0)
        self.assertEqual(
            sp.simplify(
                d["radial_frequency_squared_correction"]
                - (u4 / (8 * q) - 5 * u3**2 / (24 * q**2))
            ),
            0,
        )

    def test_mean_azimuthal_clock_is_not_omitted(self) -> None:
        d = FEN.derive_generic_finite_amplitude()
        q, u3 = d["q"], d["u3"]
        self.assertEqual(
            sp.simplify(d["azimuthal_frequency_squared_correction"] - (3 + u3 / q)),
            0,
        )
        self.assertEqual(sp.simplify(d["finite_e_correction_residual"]), 0)

    def test_force_derivative_recurrence_generates_u3_u4(self) -> None:
        d = FEN.derive_force_derivative_coefficients()
        self.assertEqual(d["A2_residual"], 0)
        self.assertEqual(d["A3_residual"], 0)
        self.assertEqual(d["u3_residual"], 0)
        self.assertEqual(d["u4_residual"], 0)

    def test_exact_closed_orbit_controls_cancel(self) -> None:
        d = FEN.derive_generic_finite_amplitude()
        Ce = d["finite_e_correction"]
        q, u3, u4 = d["q"], d["u3"], d["u4"]
        self.assertEqual(sp.simplify(Ce.subs({q: 1, u3: -6, u4: 36})), 0)
        self.assertEqual(sp.simplify(Ce.subs({q: 4, u3: -12, u4: 60})), 0)
        self.assertEqual(sp.simplify(Ce.subs({q: 2, u3: -10, u4: 54}) - sp.Rational(1, 6)), 0)

    def test_omitting_azimuthal_clock_gives_wrong_deep_limit(self) -> None:
        d = FEN.derive_generic_finite_amplitude()
        radial_only = d["radial_frequency_squared_correction"]
        self.assertEqual(
            sp.simplify(radial_only.subs({d["q"]: 2, d["u3"]: -10, d["u4"]: 54}) + sp.Rational(11, 6)),
            0,
        )


class ExactExponentialFiniteETests(unittest.TestCase):
    def test_explicit_transition_polynomial_is_derived(self) -> None:
        d = FEN.derive_exact_exponential_correction()
        self.assertEqual(d["D_residual"], 0)
        self.assertEqual(d["E_residual"], 0)
        self.assertEqual(d["explicit_Ce_residual"], 0)

    def test_newton_and_deep_limits(self) -> None:
        d = FEN.derive_exact_exponential_correction()
        self.assertEqual(d["deep_limit"], sp.Rational(1, 6))
        self.assertEqual(d["newton_limit"], 0)

    def test_representative_coefficients(self) -> None:
        expected = {0.1: 0.167129, 1.0: 0.161336, 3.0: 0.220022, 7.0: 0.229078}
        for y, target in expected.items():
            self.assertAlmostEqual(FEN.finite_e_coefficient(y), target, places=6)

    def test_newtonian_tail_is_not_rounded_to_zero(self) -> None:
        coefficient = FEN.finite_e_coefficient(150.0)
        self.assertGreater(coefficient, 0.0)
        self.assertAlmostEqual(
            coefficient / 2.397378942034799e-59,
            1.0,
            places=10,
        )

    def test_implicit_inversion_handles_measured_q_above_two(self) -> None:
        y_true, eccentricity = 1e-3, 0.03
        q0 = FEN.circular_clock_ratio(y_true)
        q_e = q0 * (1 + FEN.finite_e_coefficient(y_true) * eccentricity**2)
        self.assertGreater(q_e, 2.0)
        recovered = FEN.recover_circular_state(q_e, eccentricity)
        self.assertAlmostEqual(recovered["y"] / y_true, 1.0, places=8)
        self.assertAlmostEqual(recovered["q0"] / q0, 1.0, places=10)

    def test_truncation_aware_interval_accepts_deep_physical_q_above_model_endpoint(self) -> None:
        eccentricity = 0.03
        q_e_exact_log = 2.000300148263
        q_model_endpoint = 2 * (1 + eccentricity**2 / 6)
        self.assertGreater(q_e_exact_log, q_model_endpoint)
        with self.assertRaises(FEN.AsymptoticEndpointError):
            FEN.recover_circular_state(q_e_exact_log, eccentricity)
        interval = FEN.recover_circular_state_interval(
            q_e_exact_log,
            eccentricity,
            absolute_q_model_error=1.6e-7,
        )
        self.assertTrue(interval["model_interval_intersects"])
        self.assertTrue(interval["deep_endpoint_unresolved"])
        self.assertEqual(interval["y_min"], 0.0)
        self.assertGreater(interval["y_max"], 0.0)

    def test_corrected_cross_radius_null_cancels_mass_scale_and_distance(self) -> None:
        eccentricity = 0.03
        observations = []
        invariants = []
        for y in (0.2, 1.0, 3.0):
            state = FEN.synthetic_finite_e_observables(y, eccentricity)
            observations.append(
                {
                    "mean_turning_radius": state["mean_turning_radius"],
                    "q_e": state["q_e"],
                    "eccentricity": eccentricity,
                }
            )
            recovered = FEN.corrected_radius_invariant(
                state["mean_turning_radius"], state["q_e"], eccentricity
            )
            invariants.append(recovered["r0_squared_X"])
            self.assertLess(abs(recovered["r0_squared_X"] - 1.0), 5e-5)
        self.assertLess(abs(math.log(invariants[0] / invariants[-1])), 7e-5)
        null = FEN.cross_radius_log_null(observations[0], observations[-1])
        rescaled = [dict(observation) for observation in observations]
        for observation in rescaled:
            observation["mean_turning_radius"] *= 37.0
        rescaled_null = FEN.cross_radius_log_null(rescaled[0], rescaled[-1])
        self.assertAlmostEqual(null, rescaled_null, places=13)

    def test_invalid_finite_e_domain_is_rejected(self) -> None:
        for q_e, eccentricity in ((1.0, 0.01), (2.1, 0.01), (1.5, -0.01), (1.5, 0.031)):
            with self.assertRaises(ValueError):
                FEN.recover_circular_state(q_e, eccentricity)


class RecordedFiniteELedgerTests(unittest.TestCase):
    def test_recorded_ledger_matches_live_derivation(self) -> None:
        recorded = json.loads((HERE / "finite_eccentricity_results.json").read_text())
        self.assertEqual(recorded, FEN.build_results())


if __name__ == "__main__":
    unittest.main(verbosity=2)
