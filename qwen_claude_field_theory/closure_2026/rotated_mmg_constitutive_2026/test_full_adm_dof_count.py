import unittest

from full_adm_dof_count import count_for_mode


class FullADMDofCountTests(unittest.TestCase):
    def test_local_two_and_homogeneous_rank_jump(self):
        local = count_for_mode(1.0)
        homogeneous = count_for_mode(0.0)
        self.assertEqual(local["gravitational_dof_count"], 2.0)
        self.assertGreater(homogeneous["gravitational_dof_count"], local["gravitational_dof_count"])
        self.assertEqual(local["second_class_scalar_constraints"], local["scalar_matrix_rank"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
