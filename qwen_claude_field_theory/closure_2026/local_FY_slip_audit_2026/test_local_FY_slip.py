#!/usr/bin/env python3
"""Regression tests for the local F(Y) action-level slip audit."""

from __future__ import annotations

import importlib.util
import pathlib
import unittest


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("local_fy", HERE / "derive_local_FY_slip.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LocalFYSlipTests(unittest.TestCase):
    def test_live_symbolic_certificate(self) -> None:
        result = MODULE.derive()
        self.assertTrue(result["passed"])
        self.assertTrue(all(result["checks"].values()))

    def test_zero_mode_is_distinguished_from_finite_wavelength(self) -> None:
        result = MODULE.derive()
        dirac = result["dirac"]
        self.assertEqual(dirac["k0_symbol"], "0")
        self.assertNotEqual(dirac["k_nonzero_transverse_symbol"], "0")
        self.assertNotEqual(dirac["k_nonzero_longitudinal_symbol"], "0")

    def test_exact_exponential_symbols_are_not_hard_coded_in_verdict(self) -> None:
        result = MODULE.derive()
        exponential = result["exponential"]
        self.assertEqual(exponential["lambda_perp"], exponential["mu"])
        self.assertIn("exp(-y)", exponential["lambda_parallel"])
        self.assertNotEqual(exponential["aligned_TF_difference"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
