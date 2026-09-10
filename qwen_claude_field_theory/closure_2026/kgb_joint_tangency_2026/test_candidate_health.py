import unittest


class CandidateHealthTests(unittest.TestCase):
    def test_joint_control_has_angular_instability(self):
        from candidate_health import screen
        from refine_joint import SEED
        row=screen(SEED)
        self.assertTrue(row['seven_equations_numerically_matched'])
        self.assertTrue(all(row['angular_gradient_instability']))
        self.assertFalse(row['needs_high_precision'])

    def test_modified_shared_curvature_is_not_promoted(self):
        from candidate_health import screen
        from refine_joint import SEED
        row=screen(dict(SEED,j=SEED['j']*2))
        self.assertFalse(row['seven_equations_numerically_matched'])
        self.assertFalse(row['needs_high_precision'])


if __name__=='__main__':unittest.main()
