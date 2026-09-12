import unittest
import numpy as np
from tracking_audit import original, exact, invasion


class TrackingTests(unittest.TestCase):
    def test_exact_signed_invasion_and_drag_identities(self):
        self.assertTrue(all(exact()['checks'].values()))

    def test_original_root_is_signed_negative(self):
        ns,row=original()
        Y,c=ns['fixed_point'](row,1000.)
        self.assertTrue(np.isfinite(Y))
        self.assertLess(c,0.)
        self.assertAlmostEqual(-c*1000.**2,1.,places=8)

    def test_original_root_can_report_no_balance(self):
        ns,row=original();Y,c=ns['fixed_point'](row,1.)
        self.assertTrue(np.isnan(Y) and np.isnan(c))

    def test_higher_mode_invades_old_balance(self):
        result=invasion()
        self.assertAlmostEqual(result['infinitesimal_invader_rate'],2.,places=8)
        self.assertGreater(result['initial_log_variance_rates'][1],1.9)
        self.assertGreater(result['final_fractions'][1],.99)
        self.assertLess(abs(result['new_balance_ratio']-1),.01)

    def test_lower_mode_does_not_fake_positive_invasion(self):
        result=invasion(ratio=.5,Nmax=.05)
        self.assertLess(result['infinitesimal_invader_rate'],0.)
        self.assertLess(result['final_fractions'][1],1e-6)


if __name__=='__main__':unittest.main()
