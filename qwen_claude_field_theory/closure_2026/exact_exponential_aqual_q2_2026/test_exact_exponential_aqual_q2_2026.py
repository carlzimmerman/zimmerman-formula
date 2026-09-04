#!/usr/bin/env python3
"""Regression tests for the exact-exponential AQUAL quadrupole audit."""

import math
import unittest

import numpy as np

import exact_exponential_aqual_q2_2026 as q2


class KernelTests(unittest.TestCase):
    def test_mu_is_stable_and_has_required_limits(self):
        self.assertEqual(q2.mu_exp(0.0), 0.0)
        self.assertAlmostEqual(q2.mu_exp(1.0), 1.0 - math.exp(-1.0), places=15)
        self.assertAlmostEqual(q2.mu_exp(1.0e-12) / 1.0e-12, 1.0, places=11)
        grid = np.logspace(-12, 3, 3000)
        self.assertTrue(np.all(np.diff(q2.mu_exp(grid)) >= 0.0))

    def test_exact_aqual_branch_is_not_the_rar_shortcut(self):
        y_newton = 1.0
        nu_aqual = q2.nu_aqual_exp(y_newton)
        nu_rar = q2.nu_rar(y_newton)
        self.assertAlmostEqual(
            y_newton * nu_aqual * q2.mu_exp(y_newton * nu_aqual),
            y_newton,
            places=12,
        )
        self.assertGreater(abs(nu_aqual - nu_rar), 0.20)

    def test_regular_variable_inner_boundary_reconstructs_newtonian_phi(self):
        eta, radius, cosine = 2.5, 1.0e-6, 0.37
        u_inner = q2.inner_u_boundary(eta, radius, cosine)
        external_piece = -eta * radius * cosine
        self.assertAlmostEqual(u_inner + external_piece, -1.0 / radius, places=9)

    def test_exclusion_classification_is_computed_and_mutatable(self):
        excluded, label = q2.classify_against_ceiling(
            values=[2.0e-26, 2.1e-26],
            errors=[3.0e-28, 3.0e-28],
            ceiling=5.2e-27,
        )
        self.assertTrue(excluded)
        self.assertIn("EXCLUDED", label)
        mutated, mutated_label = q2.classify_against_ceiling(
            values=[4.0e-27], errors=[1.0e-28], ceiling=5.2e-27
        )
        self.assertFalse(mutated)
        self.assertNotIn("EXCLUDED", mutated_label)


class SolverTests(unittest.TestCase):
    def test_published_anchor_is_approached_under_refinement(self):
        # Blanchet--Novak: eta=1.9/1.2 and q2=0.26, hence |qzz|=2 q2/3.
        target_qzz = 2.0 * 0.26 / 3.0
        coarse = q2.solve_dimensionless_qzz(1.9 / 1.2, ns=96, nt=32)
        fine = q2.solve_dimensionless_qzz(1.9 / 1.2, ns=160, nt=48)
        self.assertTrue(coarse.converged)
        self.assertTrue(fine.converged)
        self.assertLess(abs(fine.qzz_abs - target_qzz), abs(coarse.qzz_abs - target_qzz))
        self.assertLess(abs(fine.qzz_abs / target_qzz - 1.0), 0.12)

    def test_dimensional_conversion_matches_definition(self):
        qzz = 0.18
        a0 = 9.3619e-11
        gm = 6.67430e-11 * 1.98892e30
        expected = 1.5 * qzz * a0 ** 1.5 / math.sqrt(gm)
        self.assertAlmostEqual(q2.q2_si_from_qzz(qzz, a0, gm), expected, places=40)

    def test_inner_boundary_location_is_stable_at_matched_log_resolution(self):
        eta = q2.G_EXT_CENTRAL_SI / q2.A0_FROZEN_SI
        check = q2.inner_boundary_sensitivity(eta)
        self.assertTrue(all(item.converged for item in check["solves"]))
        self.assertLess(check["fractional_span"], 1.0e-3)

    def test_outer_boundary_location_is_stable_at_matched_log_resolution(self):
        eta = q2.G_EXT_CENTRAL_SI / q2.A0_FROZEN_SI
        check = q2.outer_boundary_sensitivity(eta)
        self.assertTrue(all(item.converged for item in check["solves"]))
        self.assertLess(check["fractional_span"], 1.0e-2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
