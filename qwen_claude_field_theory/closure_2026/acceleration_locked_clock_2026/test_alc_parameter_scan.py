import unittest

from alc_parameter_scan import scan


class ALCParameterScanTests(unittest.TestCase):
    def test_exact_curve_selects_unique_coefficient(self):
        result = scan(etas=[0.0, 0.5, 1.0, 1.5, 2.0])
        self.assertEqual(result["best"]["eta"], 1.0)
        self.assertLess(result["best"]["max_abs_mu_error"], 1e-12)
        passing = [row for row in result["rows"] if row["passes_exact_grid"]]
        self.assertEqual(len(passing), 1)

    def test_zero_field_and_high_field_limits_are_computed(self):
        rows = scan(etas=[1.0])["rows"]
        self.assertEqual(rows[0]["mu_at_zero_limit"], 0.0)
        self.assertEqual(rows[0]["high_y_limit"], 1.0)


if __name__ == "__main__":
    unittest.main()
