import unittest
import mpmath as mp


class ParametricTests(unittest.TestCase):
    def test_original_pair_recovered(self):
        import parametric as p
        with mp.workdps(40):
            theta=[mp.log(mp.mpf(x)) for x in ('4164.89540032022','.1537936934617971','.02600582459994482')]
            new=p.pair(theta,mp.mpf('.03'));old=p.h.pair(theta,mp.mpf('.03'))
            for a,b in zip(new,old):
                for key in ('P','kappa','gamma','w','y','U'):
                    self.assertAlmostEqual(float(a[key]/b[key]),1.,places=13)

    def test_y1_is_physical_target_input_not_per_halo_a0(self):
        import parametric as p
        with mp.workdps(30):
            theta=[mp.log(mp.mpf(x)) for x in ('1.5','.3','.128')]
            a,b=p.pair(theta,mp.mpf('.128'),p.Spec(y1='.2'))
            self.assertEqual(a['y'],mp.mpf('.2'));self.assertEqual(b['y'],mp.mpf('.3'))
            self.assertAlmostEqual(float(a['P']/b['P']),1.,places=13)

    def test_positive_w_pressure_branch(self):
        import parametric as p
        theta=[mp.log(mp.mpf(x)) for x in ('1.5','.2','.128')]
        a,b=p.pair(theta,mp.mpf('.128'),p.Spec(sign_w=1))
        self.assertGreater(a['w'],0);self.assertGreater(b['w'],0)

    def test_original_next_obstruction_recovered(self):
        import parametric as p
        with mp.workdps(40):
            theta=[mp.log(mp.mpf(x)) for x in ('4164.895400320220432828310157','.153793693461797102646484544','.026005824599944823806882655')]
            row=p.gate(theta,mp.mpf('.03'))
            self.assertAlmostEqual(float(row['next_obstruction']),-.000538829413840944,places=13)
            self.assertFalse(row['joint_accepted'])


if __name__=='__main__':unittest.main()
