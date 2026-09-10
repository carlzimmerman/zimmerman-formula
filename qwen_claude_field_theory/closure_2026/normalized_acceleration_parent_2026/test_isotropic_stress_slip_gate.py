import unittest

from isotropic_stress_slip_gate import class_no_go, nonlinear_slip_source


class IsotropicStressSlipGateTests(unittest.TestCase):
    def test_exponential_scalar_norm_no_go(self):
        result = class_no_go()
        self.assertTrue(result["not_identically_zero"])
        self.assertTrue(result["positive_for_y_positive"])

    def test_metric_variation_generates_slip_source(self):
        result = nonlinear_slip_source()
        self.assertFalse(result["exact_slip_source_vanishes_identically"])
        self.assertEqual(result["high_acceleration_gradient_source"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
