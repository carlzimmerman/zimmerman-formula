#!/usr/bin/env python3
"""Independent behavioral tests for the exponential-AQUAL EFD flyby laws.

The expectations below are hand-derived special cases, direct numerical
quadratures, or invariant statements.  They do not call a second copy of the
production formula to manufacture an expected value.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import unittest

import numpy as np
from scipy.integrate import quad


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "exact_exponential_aqual_efe_flyby_2026.py"
_SUBJECT = None


def subject(case: unittest.TestCase):
    """Load the real module while turning an absent feature into a RED failure."""
    global _SUBJECT
    if not MODULE_PATH.exists():
        case.fail(f"flyby implementation is missing: {MODULE_PATH.name}")
    if _SUBJECT is None:
        spec = importlib.util.spec_from_file_location("efd_flyby_subject", MODULE_PATH)
        if spec is None or spec.loader is None:
            case.fail("could not construct an import specification for the flyby module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _SUBJECT = module
    return _SUBJECT


class ExponentialAqualEfdFlybyTests(unittest.TestCase):
    def test_exponential_external_field_parameters_are_stable(self):
        mod = subject(self)
        row = mod.external_field_parameters(1.0)
        self.assertAlmostEqual(row.mu, 0.6321205588285577, places=15)
        self.assertAlmostEqual(row.L, 0.5819767068693265, places=15)
        self.assertAlmostEqual(row.q, 1.5819767068693265, places=15)
        endpoint = mod.external_field_parameters(0.0)
        self.assertEqual(endpoint.mu, 0.0)
        self.assertEqual(endpoint.L, 1.0)
        self.assertEqual(endpoint.q, 2.0)

    def test_axis_track_matches_hand_integrated_impulse(self):
        mod = subject(self)
        got = mod.born_impulse(
            gm=3.0,
            mu_e=0.5,
            v_inf=4.0,
            direction=[0.0, 0.0, 1.0],
            impact_parameter=[2.0, 0.0, 0.0],
            q=1.6,
        )
        np.testing.assert_allclose(got, [-1.5, 0.0, 0.0], rtol=0.0, atol=2.0e-15)

    def test_closed_impulse_matches_independent_improper_quadrature(self):
        mod = subject(self)
        gm, mu_e, v_inf, q = 0.83, 0.71, 1.37, 1.73
        n = np.array([0.48, -0.36, 0.8])
        n /= np.linalg.norm(n)
        b = np.array([1.11, 0.77, -0.32])
        b -= n * np.dot(n, b)
        A = np.diag([q, q, 1.0])

        def acceleration(t):
            r = b + v_inf * t * n
            return -(gm / mu_e) * (A @ r) / float(r @ A @ r) ** 1.5

        want = np.array(
            [
                quad(lambda t, j=j: acceleration(t)[j], -np.inf, np.inf,
                     epsabs=2.0e-12, epsrel=2.0e-12, limit=300)[0]
                for j in range(3)
            ]
        )
        got = mod.born_impulse(gm, mu_e, v_inf, n, b, q)
        np.testing.assert_allclose(got, want, rtol=3.0e-12, atol=3.0e-12)

    def test_born_impulse_is_transverse_for_generic_geometry(self):
        mod = subject(self)
        n = np.array([0.6, 0.0, 0.8])
        b = np.array([0.3, 0.9, -0.225])
        b -= n * np.dot(n, b)
        got = mod.born_impulse(1.2, 0.63, 2.1, n, b, 1.8)
        self.assertLess(abs(float(np.dot(n, got))), 2.0e-14 * np.linalg.norm(got))

    def test_isotropic_limit_is_textbook_newtonian_impulse(self):
        mod = subject(self)
        n = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 3.0, 4.0])
        got = mod.born_impulse(2.0, 0.8, 5.0, n, b, 1.0)
        want = -2.0 * (2.0 / 0.8) * b / (5.0 * 25.0)
        np.testing.assert_allclose(got, want, rtol=0.0, atol=2.0e-15)

    def test_principal_trajectory_orientation_ratio_is_sqrt_q(self):
        mod = subject(self)
        q = 1.75
        parallel = mod.born_impulse(1.0, 0.7, 2.0, [0, 0, 1], [3, 0, 0], q)
        perpendicular_1 = mod.born_impulse(1.0, 0.7, 2.0, [1, 0, 0], [0, 3, 0], q)
        perpendicular_2 = mod.born_impulse(1.0, 0.7, 2.0, [1, 0, 0], [0, 0, 3], q)
        self.assertAlmostEqual(np.linalg.norm(parallel) / np.linalg.norm(perpendicular_1),
                               math.sqrt(q), places=14)
        self.assertAlmostEqual(np.linalg.norm(parallel) / np.linalg.norm(perpendicular_2),
                               math.sqrt(q), places=14)

    def test_generic_azimuth_factor_prevents_overclaiming_sqrt_q(self):
        mod = subject(self)
        factor = mod.azimuth_magnitude_factor(2.0, math.pi / 4.0)
        self.assertAlmostEqual(factor, math.sqrt(10.0) / 3.0, places=14)
        self.assertGreater(factor, 1.0)
        self.assertLess(factor, 3.0 / (2.0 * math.sqrt(2.0)))
        ratio = mod.parallel_to_perpendicular_impulse_ratio(2.0, math.pi / 4.0)
        self.assertAlmostEqual(ratio, 3.0 / math.sqrt(5.0), places=14)
        self.assertNotAlmostEqual(ratio, math.sqrt(2.0), places=6)

    def test_azimuth_factor_reaches_derived_bound(self):
        mod = subject(self)
        a = 1.63
        phi = math.atan(math.sqrt(a))
        got = mod.azimuth_magnitude_factor(a, phi)
        want = (a + 1.0) / (2.0 * math.sqrt(a))
        self.assertAlmostEqual(got, want, places=14)

    def test_kick_misalignment_has_deep_limit_bound(self):
        mod = subject(self)
        a = 2.0
        phi = math.atan(math.sqrt(a))
        self.assertAlmostEqual(mod.kick_misalignment(a, phi), math.asin(1.0 / 3.0), places=14)
        self.assertAlmostEqual(mod.maximum_kick_misalignment(a), math.asin(1.0 / 3.0), places=14)

    def test_anisotropic_rutherford_reduces_to_small_angle_rutherford(self):
        mod = subject(self)
        got = mod.anisotropic_rutherford_cross_section(
            gm=2.0,
            mu_e=0.5,
            v_inf=4.0,
            deflection_phi=0.02,
            deflection_theta=0.0,
            trajectory_anisotropy=1.7,
        )
        want = 4.0 * (2.0 / 0.5) ** 2 / (4.0**4 * 0.02**4)
        self.assertAlmostEqual(got, want, places=9)

    def test_equatorial_plane_is_an_exact_invariant_submanifold(self):
        mod = subject(self)
        acceleration = mod.efd_acceleration([1.2, -0.7, 0.0], 2.0, 0.8, 1.9)
        self.assertEqual(acceleration[2], 0.0)

    def test_equatorial_bound_conic_and_period_are_exact_kepler(self):
        mod = subject(self)
        k_e = mod.equatorial_kepler_constant(gm=12.0, mu_e=0.75, q=16.0 / 9.0)
        self.assertAlmostEqual(k_e, 12.0, places=14)
        orbit = mod.equatorial_bound_orbit(k_e, semimajor_axis=3.0, eccentricity=0.5)
        self.assertAlmostEqual(orbit.sem_latus_rectum, 2.25, places=14)
        self.assertAlmostEqual(orbit.specific_energy, -2.0, places=14)
        self.assertAlmostEqual(orbit.specific_angular_momentum, 3.0 * math.sqrt(3.0), places=14)
        self.assertAlmostEqual(orbit.period, 3.0 * math.pi, places=14)
        self.assertAlmostEqual(mod.equatorial_conic_radius(orbit.sem_latus_rectum, 0.5, 0.0),
                               1.5, places=14)
        self.assertAlmostEqual(mod.equatorial_conic_radius(orbit.sem_latus_rectum, 0.5, math.pi),
                               4.5, places=14)

    def test_equatorial_hyperbolic_deflection_is_exact(self):
        mod = subject(self)
        row = mod.equatorial_hyperbolic_scattering(k_e=2.0, impact_parameter=3.0, v_inf=2.0)
        self.assertAlmostEqual(math.tan(row.deflection_angle / 2.0), 1.0 / 6.0, places=14)
        self.assertAlmostEqual(row.eccentricity, math.sqrt(37.0), places=14)
        want = 2.0**2 / (
            4.0 * 2.0**4 * math.sin(row.deflection_angle / 2.0) ** 4
        )
        self.assertAlmostEqual(row.differential_cross_section, want, places=11)

    def test_invalid_absolute_zero_field_and_collision_are_rejected(self):
        mod = subject(self)
        with self.assertRaises(ValueError):
            mod.born_impulse(1.0, 0.0, 1.0, [0, 0, 1], [1, 0, 0], 2.0)
        with self.assertRaises(ValueError):
            mod.born_impulse(1.0, 0.5, 1.0, [0, 0, 1], [0, 0, 0], 1.5)
        with self.assertRaises(ValueError):
            mod.born_impulse(1.0, 0.5, 1.0, [0, 0, 1], [1, 0, 1], 1.5)


if __name__ == "__main__":
    unittest.main()
