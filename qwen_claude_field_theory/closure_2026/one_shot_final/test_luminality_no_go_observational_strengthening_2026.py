#!/usr/bin/env python3
"""Regression tests for the finite-shell observational strengthening."""

import unittest

import numpy as np

from luminality_no_go_observational_strengthening_2026 import (
    a0,
    c,
    constant_independent_speed_bound,
    lam_profile,
    solve_mond_y,
)


class ObservationalStrengtheningTests(unittest.TestCase):
    def test_y_solves_the_exact_exponential_mond_law(self):
        x = np.logspace(-8, 8, 65)
        y = solve_mond_y(x)
        residual = y * (1.0 - np.exp(-y)) - x
        self.assertLess(np.max(np.abs(residual) / np.maximum(1.0, x)), 2e-12)
        self.assertGreater(y[32], x[32])

    def test_lambda_derivative_is_generated_by_the_exact_mond_solution(self):
        rs = np.linspace(1.0, 5.0, 20001)
        x = 3.0 / rs**2
        y, lam = lam_profile(x, rs, mond=True)
        expected_delta = -(a0 / c**2) * np.trapz(y * np.exp(-y), rs)
        self.assertAlmostEqual(lam[-1] - lam[0], expected_delta, places=24)

    def test_gr_mutation_control_has_no_profile(self):
        rs = np.linspace(1.0, 5.0, 100)
        _, lam = lam_profile(np.ones_like(rs), rs, mond=False)
        self.assertTrue(np.array_equal(lam, np.zeros_like(lam)))

    def test_endpoint_bound_is_independent_of_additive_lambda_constant(self):
        delta = 2e-7
        bound = constant_independent_speed_bound(delta)
        offsets = np.linspace(-4e-7, 4e-7, 10001)
        endpoint_maxima = np.maximum(
            np.abs(1 / np.sqrt(1 - 2 * offsets) - 1),
            np.abs(1 / np.sqrt(1 - 2 * (offsets + delta)) - 1),
        )
        self.assertLessEqual(bound, np.min(endpoint_maxima) * (1 + 2e-6))
        self.assertGreater(bound, 0)


if __name__ == "__main__":
    unittest.main()
