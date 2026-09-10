import unittest
import numpy as np

try:
    import signed_search as search
except ImportError:
    search=None


class SignedSearchTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(search,'signed-f search is required')

    def test_fast_jets_match_original_for_both_f_signs(self):
        for f in (.05,-.05):
            for eps,y,U,w in ((1e-6,.1,1.28e-7,-.0075),(2e-6,.3,2e-7,-.03),(1e-6,.1,1.28e-7,-100.)):
                fast=search.normalized_jet(eps,y,.5,U,w,.525,f)
                _,original=search.s.raw_jet(eps,y,.5,U,w/f,.525,f)
                original[1:]/=f
                relative=abs(fast-original)/np.maximum(np.maximum(abs(fast),abs(original)),1.)
                self.assertLess(max(relative),2e-7)

    def test_negative_w_chart_keeps_Dcoord_positive(self):
        for value in (-20,-3,0,3,13):
            theta=np.array([np.log(.05),value,np.log(.2),np.log(.128),value])
            rows=search.pair(theta,-1)
            for a,_ in rows:
                self.assertLess(a['w'],0)
                self.assertGreater(a['Dcoord'],0)
                self.assertLess(a['Dcoord'],1)
                self.assertLess(a['f'],0)

    def test_equal_mass_control_has_zero_five_jet_residual(self):
        spec=search.s.Spec(eps2=1e-6)
        theta=np.array([np.log(.05),-10,np.log(.1),np.log(.128),-10])
        self.assertLess(max(abs(search.residual(theta,-1,spec))),1e-14)

    def test_high_precision_matched_seed_and_same_shared_health_control(self):
        try:
            import matched_seed_audit as audit
        except ImportError:
            audit=None
        self.assertIsNotNone(audit,'matched-seed audit is required')
        out=audit.run(70)
        self.assertLess(float(out['five_jet_relative_error']),1e-55)
        self.assertLess(float(out['shared_curvature_five_jet_relative_error']),1e-55)
        self.assertEqual(out['common']['status'],'nonempty')
        for row in out['halos']:
            self.assertTrue(row['strict_EF'])
            self.assertLess(float(row['Einstein_relative_error']),1e-50)
            self.assertLess(float(row['current_relative_error']),1e-50)
            self.assertLess(float(row['Dfield']),0)
            self.assertGreater(float(row['Dcoord']),0)

    def test_three_seed_next_obstructions_and_original_raw_finite_difference(self):
        import matched_seed_audit as audit
        expected=(-.000538829413840944,-.000262477518649397,-.000135746899087186)
        for u,obstruction in zip(('.03','.128','.5'),expected):
            out=audit.run(70,u)
            self.assertAlmostEqual(float(out['normalized_next_obstruction']),obstruction,places=14)
            self.assertLess(float(out['pivot_j']),0)
            self.assertGreater(float(out['common']['lower']),0)
            self.assertTrue(all(not row['strict_EF'] for row in out['required_j_health']))
            self.assertGreater(abs(float(out['pivot_remaining'])),1e13)
            # The nonzero gamma discrepancy survives an independent raw-jet finite difference.
            self.assertLess(min(row['scaled_error'][1] for row in out['finite_original_raw_checks']),1e-6)


if __name__=='__main__':unittest.main(verbosity=2)
