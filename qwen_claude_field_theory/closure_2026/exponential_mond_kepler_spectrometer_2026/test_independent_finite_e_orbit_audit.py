#!/usr/bin/env python3
"""Hostile nonlinear-orbit tests of the finite-e clock/null formula."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
PATH = HERE / "independent_finite_e_orbit_audit.py"
SPEC = importlib.util.spec_from_file_location("independent_finite_e", PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


class IndependentFiniteEOrbitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.live = AUDIT.audit_grid()
        cls.recorded = json.loads(
            (HERE / "independent_finite_e_results.json").read_text()
        )

    def test_audit_does_not_import_production_formula(self) -> None:
        source = PATH.read_text()
        self.assertNotIn("from finite_eccentricity_null_2026", source)
        self.assertNotIn("import finite_eccentricity_null_2026", source)

    def test_small_amplitude_recovers_symbolic_coefficient(self) -> None:
        self.assertLess(self.live["by_apo_offset"]["0.003"]["max_relative_Ce_error"], 4e-5)

    def test_full_finite_e_inversion_recovers_exterior_invariant(self) -> None:
        for offset, bound in (("0.003", 2e-8), ("0.01", 3e-7), ("0.03", 3e-5)):
            self.assertLess(
                self.live["by_apo_offset"][offset]["max_absolute_corrected_null"],
                bound,
            )

    def test_correction_removes_quadratic_radius_bias(self) -> None:
        largest = self.live["by_apo_offset"]["0.03"]
        self.assertLess(
            largest["max_absolute_corrected_null"],
            largest["max_absolute_uncorrected_null"] / 20,
        )

    def test_exact_logarithmic_limit_exceeds_truncated_deep_endpoint(self) -> None:
        deep = self.live["exact_logarithmic_limit"]
        self.assertGreater(deep["q_e"], deep["truncated_q_endpoint"])
        self.assertAlmostEqual(deep["q_e"], 2.0003001482, places=10)
        self.assertGreater(deep["endpoint_excess"], 1e-7)

    def test_recorded_run_exactly_matches_live_summary_projection(self) -> None:
        self.assertEqual(self.recorded["status"], "PASS")
        projected_live = {
            key: self.live[key]
            for key in (
                "apo_offsets",
                "by_apo_offset",
                "exact_logarithmic_limit",
                "sampled_y",
                "status",
                "units",
            )
        }
        self.assertEqual(self.recorded, projected_live)
        for offset, bound in (("0.003", 2e-8), ("0.01", 3e-7), ("0.03", 3e-5)):
            self.assertLess(
                self.recorded["by_apo_offset"][offset]["max_absolute_corrected_null"],
                bound,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
