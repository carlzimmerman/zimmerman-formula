#!/usr/bin/env python3
"""Regression tests for the executable Fable 5.1 comparison audit."""

import unittest

import sympy as sp

from fable_5_1_comparison_gate_2026 import (
    c2_convention_residual,
    clock_current_scaling_residual,
    dbi_vacuum_diagnostics,
)


class FableComparisonTests(unittest.TestCase):
    def test_literal_minus_two_dbi_has_wrong_vacuum_and_kinetic_signs(self):
        rho0, kinetic = dbi_vacuum_diagnostics(sp.Integer(-2))
        self.assertEqual(sp.sign(rho0), -1)
        self.assertEqual(sp.sign(kinetic), -1)
        healthy_rho, healthy_kinetic = dbi_vacuum_diagnostics(sp.Integer(1))
        self.assertEqual(sp.sign(healthy_rho), 1)
        self.assertEqual(sp.sign(healthy_kinetic), 1)

    def test_document_c2_sign_does_not_match_fj_formula(self):
        residual = c2_convention_residual()
        self.assertNotEqual(sp.simplify(residual), 0)
        self.assertNotEqual(sp.simplify(residual.subs({"c2_doc": sp.Rational(1, 10), "c14": sp.Rational(1, 5)})), 0)

    def test_clock_current_metric_source_has_linear_not_mond_scaling(self):
        linear_residual, mond_residual = clock_current_scaling_residual()
        self.assertEqual(linear_residual, 0)
        self.assertNotEqual(mond_residual, 0)


if __name__ == "__main__":
    unittest.main()
