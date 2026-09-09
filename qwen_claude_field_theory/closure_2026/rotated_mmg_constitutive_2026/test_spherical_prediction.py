import unittest

from spherical_prediction import derive_series


class SphericalPredictionTests(unittest.TestCase):
    def test_exact_deep_mond_series_coefficients(self):
        result = derive_series()
        self.assertEqual(result["coefficients"]["a"], "1/4")
        self.assertEqual(result["coefficients"]["b"], "7/96")
        self.assertIn("v^4 = G*M*a0", result["leading_BTFR"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
