"""Regression tests for the literal rotated-MMG lapse variation."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import sympy as sp

import rmmg_lapse_variation_gate as gate


HERE = Path(__file__).resolve().parent


class RMMGLapseVariationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = gate.derive()

    def test_symbolic_variation_checks_pass(self):
        self.assertTrue(all(self.result["checks"].values()))

    def test_affine_advertised_constraint_vanishes(self):
        self.assertEqual(self.result["affine"]["advertised_Q"], "0")

    def test_affine_extra_term_has_positive_exact_factor(self):
        extra = self.result["affine"]["extra_term"]
        factor = self.result["affine"]["positive_factor"]
        self.assertIn("exp", extra)
        self.assertEqual(factor, "beta*k + exp(beta*k) - 1")

        # This is only a numerical sanity check on the exact symbolic
        # factorization; the report supplies the analytic positivity proof.
        Y = sp.symbols("Y", positive=True)
        fn = sp.lambdify(Y, sp.exp(Y) + Y - 1, "math")
        self.assertTrue(all(fn(value) > 0 for value in (1e-8, 0.1, 1.0, 8.0)))

    def test_strict_advertised_constraint_gate_is_rejected(self):
        command = [
            sys.executable,
            "-B",
            str(HERE / "rmmg_lapse_variation_gate.py"),
            "--require-advertised-lapse-constraint",
        ]
        completed = subprocess.run(command, cwd=HERE.parents[2], check=False)
        self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
