import unittest

from ward_covariance_gate import derive_residual


class WardCovarianceGateTests(unittest.TestCase):
    def test_adm_residual_is_explicitly_nonzero(self):
        result = derive_residual()
        self.assertTrue(result["residual_nonzero"])
        self.assertIn("d_x d_t xi", result["delta_grad_u"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
