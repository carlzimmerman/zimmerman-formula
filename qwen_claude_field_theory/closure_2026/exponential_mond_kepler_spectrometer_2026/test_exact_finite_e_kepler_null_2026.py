#!/usr/bin/env python3
"""Tests for the all-orders eccentric exponential-MOND Kepler null."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "exact_finite_e_kepler_null_2026.py"
SPEC = importlib.util.spec_from_file_location("exact_finite_e", PATH)
EXACT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(EXACT)

PRIOR_PATH = (
    HERE.parent
    / "hpi_delta_eccentric_kepler_2026"
    / "hpi_delta_eccentric_kepler_2026.py"
)
PRIOR_SPEC = importlib.util.spec_from_file_location("prior_exact_eccentric", PRIOR_PATH)
PRIOR = importlib.util.module_from_spec(PRIOR_SPEC)
assert PRIOR_SPEC.loader is not None
PRIOR_SPEC.loader.exec_module(PRIOR)


class ExactFiniteEKeplerNullTests(unittest.TestCase):
    def test_cached_forward_result_cannot_be_poisoned_by_a_caller(self) -> None:
        first = EXACT.exact_apsidal_map(0.7, 0.19)
        expected = first["q_e"]
        first["q_e"] = -123.0
        second = EXACT.exact_apsidal_map(0.7, 0.19)
        self.assertIsNot(first, second)
        self.assertEqual(second["q_e"], expected)

    def test_unresolved_near_circular_quadrature_fails_loudly(self) -> None:
        with self.assertRaises(ValueError):
            EXACT.exact_apsidal_map(1.0, 2e-6)

    def test_forward_solver_rejects_unaudited_zero_field_corner(self) -> None:
        with self.assertRaises(ValueError):
            EXACT.exact_apsidal_map(1e-12, 0.03)

    def test_dimensionless_reduction_and_turning_energy_residuals(self) -> None:
        symbolic = EXACT.derive_exact_turning_law()
        self.assertEqual(symbolic["field_scale_residual"], 0)
        self.assertEqual(symbolic["eccentricity_X_residual"], 0)
        self.assertEqual(symbolic["turning_energy_residual"], 0)
        self.assertEqual(symbolic["invariant_pericenter_residual"], 0)
        self.assertEqual(symbolic["invariant_apocenter_residual"], 0)
        self.assertEqual(symbolic["cycle_factor_mutation"], 4)

    def test_deep_and_newtonian_finite_e_limits(self) -> None:
        eccentricity = 0.03
        deep = EXACT.exact_apsidal_map(1e-6, eccentricity)
        self.assertAlmostEqual(deep["q_e"], 2.0003001482, places=5)
        newton = EXACT.exact_apsidal_map(25.0, 0.2)
        self.assertLess(abs(newton["q_e"] - 1.0), 3e-5)

    def test_exact_forward_agrees_with_prior_independent_radius_quadrature(self) -> None:
        for y_peri, eccentricity in ((0.2, 0.12), (1.0, 0.2), (5.0, 0.35)):
            forward = EXACT.exact_apsidal_map(y_peri, eccentricity)
            x_peri = 1 / math.sqrt(EXACT.constitutive_X(y_peri))
            x_apo = x_peri * (1 + eccentricity) / (1 - eccentricity)
            prior = PRIOR.full_exponential_orbit(x_peri, x_apo)
            relative_error = abs(
                forward["apsidal_angle"] / prior["apsidal_angle"] - 1
            )
            self.assertLess(relative_error, 1e-8)

    def test_endpoint_guard_exceeds_bounded_independent_disagreement_audit(self) -> None:
        eccentricities = [0.01 + 0.001 * index for index in range(21)] + [
            0.04,
            0.05,
            0.075,
            0.1,
            0.15,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
        ]
        disagreements = []
        for y_peri in (EXACT.MIN_INVERSE_Y_PERI, EXACT.MAX_INVERSE_Y_PERI):
            x_peri = 1 / math.sqrt(EXACT.constitutive_X(y_peri))
            for eccentricity in eccentricities:
                x_apo = x_peri * (1 + eccentricity) / (1 - eccentricity)
                production_q = EXACT.exact_apsidal_map(y_peri, eccentricity)["q_e"]
                prior_theta = PRIOR.full_exponential_orbit(x_peri, x_apo)[
                    "apsidal_angle"
                ]
                prior_q = (2 * math.pi / prior_theta) ** 2
                disagreements.append(abs(production_q - prior_q))
        self.assertEqual(len(disagreements), 64)
        self.assertGreater(
            EXACT.INVERSE_ENDPOINT_Q_UNCERTAINTY,
            4 * max(disagreements),
        )

    def test_exact_inverse_round_trip_at_finite_eccentricity(self) -> None:
        for y_peri, eccentricity in ((0.2, 0.1), (1.0, 0.2), (5.0, 0.35)):
            forward = EXACT.exact_apsidal_map(y_peri, eccentricity)
            recovered = EXACT.recover_exact_pericenter_state(
                forward["q_e"], eccentricity
            )
            self.assertAlmostEqual(recovered["y_peri"] / y_peri, 1.0, places=6)

    def test_inverse_accepts_an_exact_search_endpoint(self) -> None:
        eccentricity = 0.2
        forward = EXACT.exact_apsidal_map(EXACT.MIN_INVERSE_Y_PERI, eccentricity)
        recovered = EXACT.recover_exact_pericenter_state(
            forward["q_e"], eccentricity
        )
        self.assertAlmostEqual(
            recovered["y_peri"] / EXACT.MIN_INVERSE_Y_PERI, 1.0, places=10
        )

    def test_inverse_accepts_a_root_on_an_interior_scan_node(self) -> None:
        segments = EXACT.DEFAULT_INVERSE_LOG_GRID_SEGMENTS
        log_min = math.log(EXACT.MIN_INVERSE_Y_PERI)
        log_max = math.log(EXACT.MAX_INVERSE_Y_PERI)
        y_peri = math.exp(log_min + (log_max - log_min) * 16 / segments)
        eccentricity = 0.2
        forward = EXACT.exact_apsidal_map(y_peri, eccentricity)
        branches = EXACT.recover_exact_pericenter_states(
            forward["q_e"], eccentricity, log_grid_segments=segments
        )
        self.assertEqual(len(branches["roots"]), 1)
        self.assertAlmostEqual(branches["roots"][0]["y_peri"] / y_peri, 1.0)

    def test_endpoint_near_values_do_not_create_false_root_records(self) -> None:
        eccentricity = 0.2
        q_low_y = EXACT.exact_apsidal_map(
            EXACT.MIN_INVERSE_Y_PERI, eccentricity
        )["q_e"]
        q_high_y = EXACT.exact_apsidal_map(
            EXACT.MAX_INVERSE_Y_PERI, eccentricity
        )["q_e"]
        delta = 2.5e-11
        above_image = EXACT.recover_exact_pericenter_states(
            q_low_y + delta, eccentricity
        )
        just_inside = EXACT.recover_exact_pericenter_states(
            q_low_y - delta, eccentricity
        )
        below_image = EXACT.recover_exact_pericenter_states(
            q_high_y - delta, eccentricity
        )
        self.assertEqual(above_image["roots"], [])
        self.assertEqual(just_inside["roots"], [])
        self.assertEqual(below_image["roots"], [])
        self.assertEqual(above_image["status"], "ENDPOINT_NUMERICALLY_UNRESOLVED")
        self.assertEqual(just_inside["status"], "ENDPOINT_NUMERICALLY_UNRESOLVED")
        self.assertEqual(below_image["status"], "ENDPOINT_NUMERICALLY_UNRESOLVED")
        inward_low = EXACT.recover_exact_pericenter_states(
            math.nextafter(q_low_y, -math.inf), eccentricity
        )
        inward_high = EXACT.recover_exact_pericenter_states(
            math.nextafter(q_high_y, math.inf), eccentricity
        )
        self.assertEqual(inward_low["roots"], [])
        self.assertEqual(inward_high["roots"], [])
        self.assertEqual(inward_low["status"], "ENDPOINT_NUMERICALLY_UNRESOLVED")
        self.assertEqual(inward_high["status"], "ENDPOINT_NUMERICALLY_UNRESOLVED")
        with self.assertRaises(ValueError):
            EXACT.recover_exact_pericenter_states(0.99999999995, 0.01)

    def test_inverse_rejects_custom_bounds_outside_audited_window(self) -> None:
        with self.assertRaises(ValueError):
            EXACT.recover_exact_pericenter_states(
                1.5,
                0.2,
                y_peri_min=EXACT.MIN_FORWARD_Y_PERI,
                y_peri_max=EXACT.MAX_FORWARD_Y_PERI,
            )

    def test_inverse_enumerates_detected_multiple_branches(self) -> None:
        def artificial_forward(y_peri: float, eccentricity: float) -> dict[str, float]:
            del eccentricity
            log_y = math.log(y_peri)
            return {
                "y_peri": y_peri,
                "q_e": 2.0 + (log_y + 0.73) * (log_y - 1.17),
            }

        with mock.patch.object(EXACT, "exact_apsidal_map", side_effect=artificial_forward):
            branches = EXACT.recover_exact_pericenter_states(
                2.0,
                0.2,
                y_peri_min=math.exp(-2),
                y_peri_max=math.exp(2),
                log_grid_segments=32,
            )
            self.assertEqual(len(branches["roots"]), 2)
            self.assertAlmostEqual(math.log(branches["roots"][0]["y_peri"]), -0.73)
            self.assertAlmostEqual(math.log(branches["roots"][1]["y_peri"]), 1.17)
            with self.assertRaises(ValueError):
                EXACT.recover_exact_pericenter_state(
                    2.0,
                    0.2,
                    y_peri_min=math.exp(-2),
                    y_peri_max=math.exp(2),
                    log_grid_segments=32,
                )

    def test_scalar_inverse_refuses_an_interior_root_with_endpoint_ambiguity(self) -> None:
        lower = math.log(EXACT.MIN_INVERSE_Y_PERI)
        upper = math.log(EXACT.MAX_INVERSE_Y_PERI)
        root_log_y = (lower + upper) / 2
        coefficient = 5e-10 / (root_log_y - lower)

        def shallow_forward(y_peri: float, eccentricity: float) -> dict[str, float]:
            del eccentricity
            return {
                "y_peri": y_peri,
                "q_e": 2.0 + coefficient * (root_log_y - math.log(y_peri)),
                "X_peri": y_peri,
            }

        with mock.patch.object(EXACT, "exact_apsidal_map", side_effect=shallow_forward):
            branches = EXACT.recover_exact_pericenter_states(
                2.0,
                0.2,
                log_grid_segments=32,
            )
            self.assertEqual(len(branches["roots"]), 1)
            self.assertTrue(branches["endpoint_ambiguities"])
            with self.assertRaises(ValueError):
                EXACT.recover_exact_pericenter_state(
                    2.0,
                    0.2,
                    log_grid_segments=32,
                )
            nulls = EXACT.exact_cross_radius_null_candidates(
                {"mean_turning_radius": 1.0, "q_e": 2.0, "eccentricity": 0.2},
                {"mean_turning_radius": 2.0, "q_e": 2.0, "eccentricity": 0.2},
            )
            self.assertEqual(nulls["status"], "ENDPOINT_NUMERICALLY_UNRESOLVED")
            self.assertTrue(nulls["orbit_i_endpoint_ambiguities"])
            self.assertTrue(nulls["orbit_j_endpoint_ambiguities"])

    def test_exact_cross_radius_null_cancels_mass_a0_distance_and_clock(self) -> None:
        r_m = 5.0
        observations = []
        invariants = []
        for y_peri, eccentricity in ((0.3, 0.12), (2.0, 0.28)):
            forward = EXACT.exact_apsidal_map(y_peri, eccentricity)
            mean_radius = r_m * forward["mean_dimensionless_radius"]
            recovered = EXACT.exact_radius_invariant(
                mean_radius, forward["q_e"], eccentricity
            )
            invariants.append(recovered["r_M_squared"])
            observations.append(
                {
                    "mean_turning_radius": mean_radius,
                    "q_e": forward["q_e"],
                    "eccentricity": eccentricity,
                }
            )
            self.assertAlmostEqual(recovered["r_M_squared"], r_m**2, places=5)
        self.assertLess(abs(math.log(invariants[0] / invariants[1])), 2e-6)
        null = EXACT.exact_cross_radius_log_null(observations[0], observations[1])
        scaled = [dict(observation) for observation in observations]
        for observation in scaled:
            observation["mean_turning_radius"] *= 37.0
        self.assertAlmostEqual(
            null,
            EXACT.exact_cross_radius_log_null(scaled[0], scaled[1]),
            places=11,
        )
        candidates = EXACT.exact_cross_radius_null_candidates(
            observations[0], observations[1]
        )
        self.assertEqual(len(candidates["pairwise_log_nulls"]), 1)
        self.assertAlmostEqual(
            candidates["minimum_absolute_log_null"], abs(null), places=11
        )

    def test_recorded_exact_ledger_matches_live_calculation(self) -> None:
        result_path = HERE / "exact_finite_e_results.json"
        recorded = json.loads(result_path.read_text())
        live = EXACT.build_results()
        self.assertEqual(recorded, live)
        canonical = json.dumps(live, indent=2, sort_keys=True, allow_nan=False) + "\n"
        self.assertEqual(result_path.read_text(), canonical)


if __name__ == "__main__":
    unittest.main(verbosity=2)
