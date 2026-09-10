import unittest
import numpy as np
import mpmath as mp


class JointSearchTests(unittest.TestCase):
    def test_seed_is_not_jointly_matched(self):
        import search
        theta=np.log([4164.89540032022,.1537936934617971,.02600582459994482,.1])
        row=search.inspect(theta,.03)
        self.assertFalse(row['accepted_numerical_joint'])
        self.assertGreater(abs(row['residual'][3]),1e-4)

    def test_fast_and_independent_first_control(self):
        import search
        import parametric as p
        theta=np.log([4164.89540032022,.1537936934617971,.02600582459994482,.1])
        row=search.inspect(theta,.03)
        with mp.workdps(40):
            reference=p.gate([mp.mpf(float(t)) for t in theta[:3]],mp.mpf('.03'))
        self.assertAlmostEqual(row['f']/float(reference['f']),1.,places=8)

    def test_changed_halo_target_does_not_change_scale(self):
        import search
        rows=search.pair(np.log([2.,.3,.1,.2]),.03)
        self.assertEqual([r['geometry']['eps'] for r in rows],[1e-6,2e-6])
        self.assertAlmostEqual(rows[0]['P']/rows[1]['P'],1.,places=13)


if __name__=='__main__':unittest.main()
