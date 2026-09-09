import unittest

from spatial_diffeo_gate import density_residuals


class SpatialDiffeoGateTests(unittest.TestCase):
    def test_constraint_density_identities(self):
        result = density_residuals()
        self.assertTrue(result["mond_density_identity"])
        self.assertTrue(result["slip_density_identity"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
