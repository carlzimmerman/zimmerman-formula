import unittest

from sparc_exact_exponential_fit import fit, invert_exponential


class SPARCExactExponentialTests(unittest.TestCase):
    def test_inverse_residual_is_small(self):
        import numpy as np

        gb = np.logspace(-13, -9, 8)
        g = invert_exponential(gb)
        self.assertLess(float(np.max(np.abs(g * (1 - np.exp(-g / 9.36e-11)) - gb) / gb)), 1e-9)

    def test_catalogue_fit_is_finite(self):
        result = fit()
        self.assertGreater(result["n_galaxies"], 100)
        self.assertGreater(result["n_points"], 1000)
        self.assertTrue(0.3 <= result["best_disk_ml"] <= 1.2)
        self.assertTrue(result["best_scatter_dex"] > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
