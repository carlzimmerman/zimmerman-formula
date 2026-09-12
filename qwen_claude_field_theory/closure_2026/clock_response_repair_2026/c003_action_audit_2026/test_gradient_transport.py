"""Exact regressions for the necessary gradient-tracking identity."""
import unittest
import sympy as s
from gradient_transport import derive


class TransportTests(unittest.TestCase):
    def test_raw_metric_derivative_matches_projected_identity(self):
        self.assertEqual(derive()["transport_residual"], 0)

    def test_uniform_clock_gradient_dilutes(self):
        self.assertEqual(derive()["uniform_gradient_residual"], 0)

    def test_nonzero_critical_gradient_needs_a_source(self):
        r = derive()
        H, Y, rate = r["tracking_symbols"]
        self.assertEqual(s.expand(r["required_source"] - (2*H*Y + rate)), 0)


if __name__ == "__main__":
    unittest.main()
