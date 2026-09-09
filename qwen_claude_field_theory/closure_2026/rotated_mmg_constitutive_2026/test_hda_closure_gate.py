import unittest

from hda_closure_gate import derive_bracket


class HDAClosureGateTests(unittest.TestCase):
    def test_exact_bracket_exposes_cubic_obstruction(self):
        result = derive_bracket()
        self.assertTrue(result["cubic_witness_nonzero"])
        self.assertEqual(result["mu_derivative_at_a0"], "exp(-1)/a0")
        self.assertIn("A_required_by_p_linear_term", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
