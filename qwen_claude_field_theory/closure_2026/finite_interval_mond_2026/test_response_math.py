"""Exact-law and numerical-domain checks for finite-interval MOND responses."""

import importlib.util
from pathlib import Path
import unittest

import numpy as np
import sympy as sp


MODULE = Path(__file__).with_name("response_math.py")
response = None
if MODULE.exists():
    spec = importlib.util.spec_from_file_location("finite_interval_response_math", MODULE)
    response = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(response)


class ResponseTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(response, "finite-interval response API is not implemented")

    def test_exponential_inverse_recovers_independent_forward_accelerations(self):
        # A swapped exponential argument or inaccurate small root fails.
        y = np.logspace(-8, 12, 91).reshape(7, 13)
        a0 = 1.17e-10
        b = a0 * y * (-np.expm1(-y))
        actual = response.acceleration(b, a0, "mu_exp")
        self.assertEqual(actual.shape, y.shape)
        np.testing.assert_allclose(actual, a0 * y, rtol=5e-13, atol=0)

    def test_other_kernels_have_independent_forward_benchmarks(self):
        # Confusing mu_exp and the RAR nu, or omitting the simple-law factor, fails.
        a0 = 2.3e-10
        t = np.array([1e-8, .2, 1., 5., 1e6])
        b = a0 * t**2
        np.testing.assert_allclose(response.acceleration(b, a0, "nu_rar"),
                                   b / (-np.expm1(-t)), rtol=2e-14)
        true_g = a0 * np.logspace(-8, 12, 21)
        b_simple = true_g**2 / (true_g + a0)
        np.testing.assert_allclose(response.acceleration(b_simple, a0, "simple"),
                                   true_g, rtol=3e-14)
        self.assertEqual(response.acceleration(4., 9., "deep"), 6.)
        self.assertEqual(response.acceleration(4., 9., "newton"), 4.)

    def test_positive_kernels_have_correct_deep_and_newton_limits(self):
        # A wrong branch may fit transition values but miss either asymptote.
        for kernel in ("mu_exp", "nu_rar", "simple"):
            self.assertAlmostEqual(response.acceleration(1e-16, 1., kernel) / 1e-8,
                                   1., delta=1e-7)
            self.assertAlmostEqual(response.acceleration(1e12, 1., kernel) / 1e12,
                                   1., delta=1e-10)

    def test_symbolic_curvature_matches_independent_log_acceleration_differences(self):
        # Missing chain-rule factors or logarithm-base factors fail.
        derived = response.derive()
        self.assertTrue(all(value == 0 for value in derived["residuals"].values()))
        x = derived["x"]
        self.assertEqual(sp.simplify(derived["slope"]["mu_exp"].subs(x, 1)
                                     - (1-sp.exp(-1))), 0)
        h = .001
        s = np.logspace(-2, 1, 8)
        for kernel in ("mu_exp", "nu_rar"):
            values = [np.log(response.acceleration(s*np.exp(shift), 1., kernel))
                      for shift in (-h, 0., h)]
            measured = (values[2] - 2*values[1] + values[0]) / h**2
            coordinate = (response.acceleration(s, 1., kernel)
                          if kernel == "mu_exp" else np.sqrt(s))
            exact = sp.lambdify(x, derived["curvature"][kernel], "numpy")(coordinate)
            np.testing.assert_allclose(measured, exact, rtol=5e-5, atol=3e-8)

    def test_finite_transfer_preserves_endpoints_and_broadcasting(self):
        # Replacing the secant by a derivative at its midpoint fails.
        self.assertAlmostEqual(response.finite_transfer(1., 100., 3., "deep"), 1.)
        self.assertAlmostEqual(response.finite_transfer(1., 100., 3., "newton"), 2.)
        y = np.array([.05, .5, 5.])
        b = y * (-np.expm1(-y))
        expected = np.log10(y[1:] / y[0])
        np.testing.assert_allclose(response.finite_transfer(b[0], b[1:], 1., "mu_exp"),
                                   expected, rtol=3e-14)
        np.testing.assert_allclose(response.finite_transfer(7*b[0], 7*b[1:], 7., "mu_exp"),
                                   expected, rtol=3e-14)

    def test_chord_defect_preserves_violations_and_cancels_uniform_amplitudes(self):
        # Sorting g or imposing g-monotonicity would hide empirical violations.
        b = np.array([1., 10., 100.])
        g = np.array([1., 2., 10.])
        wanted = np.log10(2.) - .5
        self.assertAlmostEqual(response.chord_defect(b, g), wanted)
        self.assertAlmostEqual(response.chord_defect(11*b, 7.3*g), wanted)
        self.assertGreater(response.chord_defect(b, [1., 20., 10.]), 0.)
        self.assertAlmostEqual(response.chord_defect(b, np.sqrt(b)), 0.)

    def test_exact_exponential_and_rar_predictions_obey_common_interval_bounds(self):
        # A reversed Jensen sign or transfer orientation fails for synthetic laws.
        b = np.array([.003, .3, 30.])
        for kernel in ("mu_exp", "nu_rar"):
            g = response.acceleration(b, 1., kernel)
            transfer = response.finite_transfer(b[0], b[2], 1., kernel)
            self.assertGreater(transfer, .5*np.log10(b[2]/b[0]))
            self.assertLess(transfer, np.log10(b[2]/b[0]))
            self.assertLess(response.chord_defect(b, g), 0.)

    def test_invalid_inputs_fail_without_silently_clipping_or_reordering(self):
        for bad in (0., -1., np.inf, np.nan, [], [1., -2.]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                response.acceleration(bad, 1., "mu_exp")
        for bad_a0 in (0., -1., np.inf, np.nan, [1., 2.]):
            with self.subTest(a0=bad_a0), self.assertRaises(ValueError):
                response.acceleration(1., bad_a0, "mu_exp")
        with self.assertRaises(ValueError):
            response.acceleration(1., 1., "unknown")
        for endpoints in ((2., 1.), (1., 1.), ([1., 2.], [2., 1.])):
            with self.assertRaises(ValueError):
                response.finite_transfer(*endpoints, 1., "mu_exp")
        for b, g in (([1., 2.], [1., 2.]), ([2., 1., 3.], [1., 2., 3.]),
                     ([1., 1., 3.], [1., 2., 3.]), ([1., 2., 3.], [1., 0., 3.]),
                     ([[1., 2., 3.]], [1., 2., 3.])):
            with self.assertRaises(ValueError):
                response.chord_defect(b, g)


if __name__ == "__main__":
    unittest.main(verbosity=2)
