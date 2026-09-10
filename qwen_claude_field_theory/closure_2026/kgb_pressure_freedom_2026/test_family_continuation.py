import unittest
import family_continuation as f


class FamilyTests(unittest.TestCase):
    def test_joint_control_is_recovered_but_not_health_certified(self):
        start=f.SEED['parameters'][:3]+[f.SEED['u1']]
        row=f.solve(start,.1,max_nfev=1)
        self.assertTrue(row['accepted_numerical_joint'])
        self.assertLess(max(map(abs,row['first_relative']+row['next_relative'])),1e-8)
        self.assertFalse(row['health']['needs_high_precision'])

    def test_one_actual_continuation_step(self):
        start=f.SEED['parameters'][:3]+[f.SEED['u1']]
        start[1]*=.8
        row=f.solve(start,.08,max_nfev=25)
        self.assertTrue(row['accepted_numerical_joint'])
        self.assertLess(max(map(abs,row['five_jet_relative'])),1e-8)
        self.assertLess(row['u1']*1e-6,.01)
        self.assertLess(row['parameters'][2]*2e-6,.01)

    def test_incomplete_step_is_not_a_match(self):
        start=f.SEED['parameters'][:3]+[f.SEED['u1']]
        start[1]*=.8
        row=f.solve(start,.08,max_nfev=1)
        self.assertFalse(row['accepted_numerical_joint'])
        self.assertNotIn('health',row)


if __name__=='__main__':unittest.main(verbosity=2)
