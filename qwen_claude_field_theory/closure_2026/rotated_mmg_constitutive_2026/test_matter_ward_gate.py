import unittest

from matter_ward_gate import ward_identity


class MatterWardGateTests(unittest.TestCase):
    def test_minimal_matter_identity(self):
        result = ward_identity()
        self.assertTrue(result["ward_identity"])
        self.assertEqual(result["residual_t"], "0")
        self.assertEqual(result["residual_x"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
