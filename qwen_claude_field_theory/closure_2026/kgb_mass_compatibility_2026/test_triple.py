import unittest
import numpy as np
import triple_seed as t
import triple_flow as flow


class TripleTests(unittest.TestCase):
    def test_previous_root_matches_value_and_slope_not_next_derivative(self):
        a=t.jet(.1,.3,.1603985047412938,.25)
        self.assertLess(abs(a['residual'][0]),1e-8)
        self.assertGreater(abs(a['residual'][1]),1e-3)

    def test_original_mass_is_an_exact_control(self):
        a=t.jet(.1,.3,.3,.25,eps3=2e-6)
        np.testing.assert_allclose(a['residual'],[0,0],atol=1e-7)

    def test_triple_seed_is_compatible_and_healthy(self):
        fit,state=flow.initial()
        self.assertLess(fit['max_scaled_residual'],1e-8)
        self.assertTrue(fit['all_causal'])
        observation=flow.observe(0,state)
        for halo in observation['halos']:
            self.assertLess(halo['common_action_stress_error'],1e-12)
            self.assertLess(halo['common_action_current_error'],1e-12)

    def test_next_lie_derivative_does_not_close_at_that_seed(self):
        coarse=flow.next_preservation(.25,1e-4)['next_scaled_preservation']
        fine=flow.next_preservation(.25,1e-5)['next_scaled_preservation']
        self.assertGreater(abs(fine),1.)
        self.assertAlmostEqual(coarse/fine,1,delta=1e-5)

    def test_third_mass_uses_shared_action_and_detects_real_defect(self):
        first=flow.integrate(max_step=.0005)
        fine=flow.integrate(max_step=.00025)
        self.assertTrue(first['solver_success'] and fine['solver_success'])
        a,b=first['rows'][-1],fine['rows'][-1]
        for row in (a,b):
            for halo in row['halos'][:2]:
                self.assertLess(halo['common_action_stress_error'],1e-10)
            self.assertGreater(row['halos'][2]['common_action_stress_error'],1e-6)
        self.assertAlmostEqual(a['value_mismatch']/b['value_mismatch'],1,delta=1e-7)


if __name__=='__main__':unittest.main()
