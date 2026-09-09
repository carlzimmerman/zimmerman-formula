import unittest

from alc_clock_dirac import build_gate


class ALCClockDiracTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build_gate()

    def test_constraints_are_derived_and_second_class(self):
        self.assertNotEqual(self.data["poisson_determinant"], "0")
        self.assertGreater(self.data["poisson_rank_k_nonzero"], 0)
        self.assertGreaterEqual(self.data["constraint_jacobian_rank"],
                                self.data["poisson_rank_k_nonzero"])

    def test_acceleration_term_does_not_create_clock_wave(self):
        self.assertEqual(self.data["tau_dot_on_constraints"], "0")
        self.assertIn("sigma0*k^2", self.data["reduced_H_on_constraints"])

    def test_zero_mode_is_reported(self):
        self.assertEqual(self.data["poisson_rank_k_zero"],
                         self.data["poisson_rank_k_nonzero"])
        self.assertEqual(self.data["status"], "OPEN")


if __name__ == "__main__":
    unittest.main()
