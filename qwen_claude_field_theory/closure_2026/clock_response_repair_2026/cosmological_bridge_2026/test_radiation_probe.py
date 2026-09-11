"""Bounded tests: unchanged coefficient flow, domain guard, sourced constraints."""
import importlib.util
import unittest
import numpy as np
from background_evolve import Model


class RadiationProbe(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('radiation_probe'),
                             'missing backward frozen-history probe')
        import radiation_probe
        return radiation_probe

    def test_same_initial_coefficients_and_backward_flow(self):
        probe = self.module()
        backward = probe.BackwardHistory(1.)
        original = Model(.01)
        np.testing.assert_allclose(backward.background(0.)['raw'],
                                   original.background(0.)['raw'], rtol=1e-13, atol=1e-14)
        tau, h = -.1, 1e-4
        def state(t):
            b = backward.background(t)
            return np.array([b['a'], b['m'], b['v']])
        derivative = (state(tau-2*h)-8*state(tau-h)
                      +8*state(tau+h)-state(tau+2*h))/(12*h)
        np.testing.assert_allclose(derivative, backward.flowfunc(*state(tau)),
                                   rtol=2e-7, atol=2e-9)

    def test_coefficient_dense_output_cannot_extrapolate(self):
        backward = self.module().BackwardHistory(1.)
        for tau in (1e-5, backward.tau_min-1e-5):
            with self.subTest(tau=tau), self.assertRaises(ValueError):
                backward.background(tau)

    def test_short_sourced_probe_preserves_initial_constraints(self):
        result = self.module().probe(efolds=.05, coefficient_efolds=1., step=.025)
        self.assertEqual(result['outcome'], 'physical_efold_bound')
        self.assertLess(result['max_scaled_friedmann_residual'], 1e-8)
        self.assertLess(result['max_scaled_clock_residual'], 1e-8)
        self.assertLess(result['samples'][-1]['tau'], 0.)
        self.assertGreater(result['samples'][-1]['radiation_fraction'],
                           result['samples'][0]['radiation_fraction'])


if __name__ == '__main__':
    unittest.main()
