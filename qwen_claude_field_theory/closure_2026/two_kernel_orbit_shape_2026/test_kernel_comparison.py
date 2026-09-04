import unittest
import numpy as np
from kernel_comparison import compare_profiles


class ProfileTests(unittest.TestCase):
    def test_recovers_noiseless_rar_with_a0_fitted_in_both_models(self):
        # Construct directly from the defining empirical relation.
        gb = np.logspace(-2, 2, 120)
        go = gb / -np.expm1(-np.sqrt(gb))
        gid = np.arange(120) % 6
        result = compare_profiles(gb, go, gid, np.linspace(-.4, .4, 161), 31, 7)
        self.assertLess(result['fit']['nu_rar']['mse_dex2'], 1e-28)
        self.assertGreater(result['fit']['mu_exp']['mse_dex2'], 1e-4)
        self.assertGreater(result['paired_delta_mse_percentiles'][0], 0)

    def test_replication_within_each_galaxy_does_not_change_equal_galaxy_score(self):
        gb = np.array([.1, 1., 10., 20.])
        go = np.array([.4, 1.7, 11., 22.])
        gid = np.array([0, 0, 1, 1])
        grid = np.linspace(-.4, .4, 81)
        one = compare_profiles(gb, go, gid, grid, 31, 11)
        index = np.array([0, 1, 0, 1, 0, 1, 2, 3])
        two = compare_profiles(gb[index], go[index], gid[index], grid, 31, 11)
        for kernel in ('mu_exp', 'nu_rar'):
            self.assertAlmostEqual(one['fit'][kernel]['mse_dex2'], two['fit'][kernel]['mse_dex2'], places=14)
        np.testing.assert_allclose(one['paired_delta_mse_percentiles'],
                                   two['paired_delta_mse_percentiles'], atol=1e-14)


if __name__ == '__main__':
    unittest.main(verbosity=2)
