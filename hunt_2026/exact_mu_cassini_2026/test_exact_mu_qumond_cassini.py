#!/usr/bin/env python3
"""Regression and falsification tests for the exact-mu QUMOND Cassini audit."""

from __future__ import annotations

import math
import unittest

import numpy as np

from exact_mu_qumond_cassini import (
    A0_ALTERNATE,
    A0_CANONICAL,
    G_EXTERNAL,
    GM_SUN,
    PARK_Q2_2SIGMA_CEILING,
    exact_inverse_total_acceleration,
    mu_exponential,
    newtonian_external_from_true_eta,
    nu_exponential_exact,
    q2_from_q,
    q_direct_adaptive,
    q_split_gauss,
    radial_tail_bound,
)


class ExactMuInverseTests(unittest.TestCase):
    def test_inverse_closes_defining_flux_equation(self) -> None:
        for x in np.logspace(-14, 6, 81):
            y = exact_inverse_total_acceleration(float(x))
            reconstructed = y * mu_exponential(y)
            self.assertLessEqual(
                abs(reconstructed - x),
                3.0e-12 * max(x, 1.0e-14),
            )
            self.assertAlmostEqual(nu_exponential_exact(float(x)), y / x, places=13)

    def test_external_field_is_transformed_before_qumond_integral(self) -> None:
        eta_true = G_EXTERNAL / A0_CANONICAL
        e_newtonian = newtonian_external_from_true_eta(eta_true)
        self.assertAlmostEqual(
            e_newtonian,
            eta_true * (1.0 - math.exp(-eta_true)),
            places=15,
        )


class QuadratureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.eta = G_EXTERNAL / A0_CANONICAL

    def test_independent_direct_and_split_forms_agree(self) -> None:
        direct = q_direct_adaptive(
            self.eta,
            radial_max=6.0,
            absolute_tolerance=1.0e-12,
            relative_tolerance=1.0e-10,
        )
        split32 = q_split_gauss(self.eta, radial_max=6.0, order=32)
        split64 = q_split_gauss(self.eta, radial_max=6.0, order=64)
        split128 = q_split_gauss(self.eta, radial_max=6.0, order=128)
        split256 = q_split_gauss(self.eta, radial_max=6.0, order=256)

        delta_32_64 = abs(split32.q - split64.q)
        delta_64_128 = abs(split64.q - split128.q)
        delta_128_256 = abs(split128.q - split256.q)
        self.assertLess(delta_64_128, delta_32_64)
        self.assertLess(delta_128_256, delta_64_128)
        self.assertLess(delta_128_256, 5.0e-9)
        self.assertLess(abs(direct.q - split256.q), 5.0e-10)
        self.assertGreater(direct.q, 0.0)
        self.assertLess(direct.reported_error, 5.0e-10)

    def test_domain_change_is_covered_by_analytic_tail_bound(self) -> None:
        at_six = q_split_gauss(self.eta, radial_max=6.0, order=96)
        at_ten = q_split_gauss(self.eta, radial_max=10.0, order=96)
        bound = radial_tail_bound(self.eta, radial_min=6.0)
        # Product-rule roundoff is allowed in addition to the rigorous omitted tail.
        self.assertLess(abs(at_six.q - at_ten.q), bound + 3.0e-10)
        self.assertLess(bound, 1.0e-12)

    def test_newtonian_and_zero_external_field_mutations_collapse_q(self) -> None:
        def newtonian_nu_minus_one(value):
            return np.zeros_like(np.asarray(value, dtype=float))

        newtonian = q_split_gauss(
            self.eta,
            radial_max=6.0,
            order=32,
            nu_minus_one=newtonian_nu_minus_one,
        )
        zero_external = q_split_gauss(0.0, radial_max=6.0, order=32)
        self.assertEqual(newtonian.q, 0.0)
        self.assertEqual(zero_external.q, 0.0)

    def test_both_a0_footings_exceed_park_ceiling(self) -> None:
        for a0 in (A0_CANONICAL, A0_ALTERNATE):
            eta = G_EXTERNAL / a0
            q = q_split_gauss(eta, radial_max=6.0, order=256).q
            q2 = q2_from_q(q, a0=a0, central_mass_parameter=GM_SUN)
            self.assertGreater(q2, PARK_Q2_2SIGMA_CEILING)


if __name__ == "__main__":
    unittest.main(verbosity=2)
