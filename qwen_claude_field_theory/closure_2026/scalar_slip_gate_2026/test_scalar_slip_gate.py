#!/usr/bin/env python3
"""Tests for the conditional local-single-scalar slip obstruction."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "scalar_slip_gate.py"


class ScalarSlipGateTests(unittest.TestCase):
    def test_derivation_suite_passes_and_reports_scope(self) -> None:
        proc = subprocess.run(
            [sys.executable, "-B", str(SCRIPT)],
            cwd=HERE,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        record = json.loads(proc.stdout.split("CERTIFICATE_JSON:", 1)[1])
        self.assertEqual(record["status"], "CONDITIONAL_OBSTRUCTION")
        self.assertTrue(record["checks"]["traceless_sum_of_squares"])
        self.assertTrue(record["checks"]["mond_coefficient_nonzero"])
        self.assertTrue(record["checks"]["obstruction"])
        self.assertIn("not a universal", record["scope"])

    def test_strict_compatibility_mode_fails_for_the_derived_obstruction(self) -> None:
        proc = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--require-compatible"],
            cwd=HERE,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
