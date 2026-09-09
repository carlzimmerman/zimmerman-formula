import unittest

from alc_ppn_stability import build_audit


class ALCPreferredFrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build_audit()

    def test_ppn_is_not_assumed_in_singular_corner(self):
        self.assertFalse(self.data["ppn_corner_is_regular"])
        self.assertIn("c1", self.data["standard_aether_alpha1"])
        self.assertTrue(self.data["alpha1_path_dependence"])

    def test_constitutive_hessian_sign_change_is_derived(self):
        self.assertIn("1", self.data["longitudinal_sign_crossing"])
        self.assertEqual(self.data["deep_mond_sign"], "1")
        self.assertEqual(self.data["high_acceleration_sign"], "-1")


if __name__ == "__main__":
    unittest.main()
