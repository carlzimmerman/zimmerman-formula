from __future__ import annotations

import unittest

import fourform_a0_promotion_gate as gate


class FourFormA0PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = gate.derive()

    def test_algebraic_promotion_checks_pass(self):
        self.assertTrue(all(self.result["checks"].values()))

    def test_half_kappa_is_marked_calibration(self):
        self.assertEqual(self.result["status"], "A0_PROMOTION_ALIGNED_BUT_KAPPA_FITTED")
        self.assertIn("kappa=1/2 is derived", self.result["non_claims"])

    def test_energy_relation_is_exact(self):
        self.assertEqual(self.result["derived"]["a0_squared_minus_kappa_squared_G_epsilon"], "0")


if __name__ == "__main__":
    unittest.main()
