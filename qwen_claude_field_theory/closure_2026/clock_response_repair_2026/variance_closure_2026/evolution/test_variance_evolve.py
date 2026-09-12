"""Orthogonal, cheap checks of variance differentiation and normalization."""
import unittest
import numpy as np
from scipy.linalg import expm
from variance_evolve import covariance_rhs, variance_jets, initial_states, forward_rate, forward_curvature


class VarianceAlgebraTests(unittest.TestCase):
    def test_constant_operator_against_exponential(self):
        # Noncommuting, nonsymmetric A and a PSD covariance with correlations.
        A = np.array([[.1, 2.], [-3., -.4]])
        C = np.array([[2., -.3], [-.3, .7]])
        H = .6
        jets = variance_jets(4., H, 0., A, np.zeros((2, 2)), C)
        def exact_y(t):
            fundamental = expm(A * t)
            return 4 * np.exp(-2 * H * t) * (fundamental @ C @ fundamental.T)[0, 0]
        self.assertAlmostEqual(jets[0], exact_y(0.))
        self.assertAlmostEqual(jets[1], forward_rate(exact_y, 1e-4), places=8)
        coarse_error = abs(jets[2] - forward_curvature(exact_y, 1e-3))
        fine_error = abs(jets[2] - forward_curvature(exact_y, 5e-4))
        self.assertLess(fine_error, coarse_error)
        self.assertLess(fine_error, 3e-6)

    def test_pure_expansion_and_inertial_mode(self):
        # sigma=s+v*t, a=exp(H*t) gives an elementary independent benchmark.
        A = np.array([[0., 1.], [0., 0.]])
        state = np.array([2., 3.])
        C = np.outer(state, state)
        H = .4
        jets = variance_jets(5., H, 0., A, np.zeros((2, 2)), C)
        np.testing.assert_allclose(jets, [20., 44., 6.8], atol=1e-12)

    def test_same_variance_opposite_rates(self):
        A = np.zeros((6, 6))
        A[0, 0] = .3
        A[0, 1] = 2.
        states = initial_states(A, .5)
        for index, state in enumerate(states):
            C = np.outer(state, state)
            jet = variance_jets(9., .5, 0., A, np.zeros_like(A), C)
            self.assertAlmostEqual(jet[0], 9.)
            self.assertAlmostEqual(jet[1], [-18., 0., 18.][index])
            self.assertGreaterEqual(np.linalg.eigvalsh(C).min(), -1e-14)

    def test_forward_stencils_and_k0_observable(self):
        self.assertAlmostEqual(forward_rate(lambda t: 2 + 3*t - 7*t**4, .001), 3., places=9)
        self.assertAlmostEqual(forward_curvature(lambda t: 2 + 3*t + 4*t*t + 5*t**4, .01), 8., places=8)
        np.testing.assert_array_equal(variance_jets(0., 2., 3., np.eye(2),
            np.eye(2), np.eye(2)), np.zeros(3))


if __name__ == "__main__":
    unittest.main()
