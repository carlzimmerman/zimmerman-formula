import unittest

from laplacian_multiplier_gate import laplacian_scaled


class LaplacianMultiplierGateTests(unittest.TestCase):
    def test_local_constraints_are_preserved_and_zero_mode_is_separate(self):
        for k in (0.5, 1.0, 2.0):
            local = laplacian_scaled(k, 2.0, 1.0)
            self.assertTrue(local["nonzero_equivalent_to_direct_relay"])
            self.assertGreater(local["dirac_rank"], 0)
        homogeneous = laplacian_scaled(0.0, 2.0, 1.0)
        self.assertTrue(homogeneous["homogeneous_constraints_vanish"])
        self.assertLess(homogeneous["dirac_rank"], laplacian_scaled(1.0, 2.0, 1.0)["dirac_rank"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
