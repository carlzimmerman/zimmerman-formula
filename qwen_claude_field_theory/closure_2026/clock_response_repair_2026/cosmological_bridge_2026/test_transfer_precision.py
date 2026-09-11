"""Precision checks do not turn a stored double trajectory into an exact one."""
import unittest
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from transfer_evolve import Background, metric_fields, mode_system
from transfer_precision import dense_mp, PrecisionEvaluator, precision_sweep


class PrecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bg = Background(.02)
        cls.k = .3
        cls.sol = solve_ivp(lambda t, u: (mode_system(cls.bg.at(float(t))[0], cls.k)[0]
                            @ u.reshape(6, 6)).ravel(), [0, .02], np.eye(6).ravel(),
                            method='DOP853', rtol=2e-10, atol=2e-12, dense_output=True)

    def test_dense_replays_same_polynomial_and_rejects_extrapolation(self):
        with mp.workdps(40):
            for t in np.linspace(0, .02, 13):
                np.testing.assert_allclose(np.asarray(dense_mp(self.sol.sol, mp.mpf(t)), float),
                                           self.sol.sol(t), rtol=2e-15, atol=2e-15)
            with self.assertRaises(ValueError):
                dense_mp(self.sol.sol, mp.mpf(-.01))

    def test_reconstructed_fields_match_original(self):
        evaluator = PrecisionEvaluator(self.bg, self.sol, self.k)
        with mp.workdps(40):
            for t in (.004, .01, .016):
                actual, _ = evaluator.fields(mp.mpf(t))
                expected, _ = metric_fields(self.bg, self.sol, self.k, t)
                np.testing.assert_allclose(np.asarray(actual, float), expected,
                                           rtol=3e-12, atol=3e-12)

    def test_higher_precision_resolves_small_step_growth(self):
        result = precision_sweep(self.bg, self.sol, self.k,
                                 steps=(.001, .0005, .000125), dps=(30, 50))
        low, high = result['precision_runs']
        for a, b in zip(low['diagnostics'], high['diagnostics']):
            self.assertLess(abs(a['max_scaled_euler']-b['max_scaled_euler']), 1e-13)
        self.assertLess(high['diagnostics'][-1]['max_scaled_euler'], 3e-8)
        self.assertLess(high['diagnostics'][-1]['max_scaled_euler'],
                        result['float64'][-1]['max_scaled_euler']/10)


if __name__ == '__main__':
    unittest.main()
