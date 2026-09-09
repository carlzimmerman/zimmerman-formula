"""Actual conserved dust in IC17, without substituting vacuum envelope jets."""
import importlib.util
import unittest
import mpmath as mp
import ic17_pole_clock as action


class BaryonBackgroundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps=70

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic17_baryon_background'))
        return __import__('ic17_baryon_background')

    def test_same_action_dust_root_and_positive_expansion_at_requested_points(self):
        model=self.model()
        for S in ('.1','.01','1e-4','1e-8'):
            bg=model.state(S)
            self.assertLess(abs(bg['constraint']),mp.mpf('1e-35'))
            self.assertLess(abs(bg['b']/bg['clock_charge_density']-mp.mpf('.2')),mp.mpf('1e-60'))
            self.assertTrue(0<bg['u']<1)
            self.assertGreater(bg['FX'],0)
            self.assertGreater(bg['Qbare'],0)
            self.assertGreater(bg['Q'],bg['FX'])
            self.assertGreater(abs(mp.det(bg['auxiliary_bracket'])),1)
            self.assertGreater(bg['physical_H'],0)
            self.assertEqual(bg['eta'],1)
            self.assertFalse(bg['full_dust_characteristics_checked'])

    def test_vacuum_limit_recovers_ic17_background(self):
        bg=self.model().state('.1',k=0)
        ref=action.state('.1')
        for left,right in (('w','w'),('Q','kinetic'),('physical_H','physical_H')):
            self.assertLess(abs(bg[left]-ref[right]),mp.mpf('1e-45'))

    def test_clock_charge_dust_continuity_and_auxiliary_preservation(self):
        for S in ('.1','.01','1e-4','1e-8'):
            bg=self.model().state(S)
            self.assertLess(abs(bg['clock_charge_flow_residual'])/(1+bg['H']*bg['clock_charge_density']),mp.mpf('1e-55'))
            self.assertLess(abs(bg['auxiliary_flow_residual'])/(1+bg['H']*bg['b']),mp.mpf('1e-55'))
            self.assertLess(abs(bg['canonical_identity_residual'])/(1+abs(bg['auxiliary_schur'])),mp.mpf('1e-55'))
            self.assertLess(abs(bg['wdot']-bg['wS']*bg['Sdot']),mp.mpf('1e-55'))

    def test_fixed_b_velocity_hessian_matches_clock_schur(self):
        model=self.model()
        bg=model.state('.1')
        point=(mp.exp(-bg['S']),bg['w'])
        density=lambda v,w:model.raw(-mp.log(v),w,bg['b'])
        M=mp.diff(density,point,(2,0))
        mixed=mp.diff(density,point,(1,1))
        B=mp.diff(density,point,(0,2))
        self.assertLess(abs(bg['Q']-(M-mixed*mixed/B)),mp.mpf('1e-50'))

    def test_fixed_charge_ratio_branch_derivative_matches_finite_difference(self):
        model=self.model()
        S,h=mp.mpf('.01'),mp.mpf('1e-6')
        w=lambda s:model.state(s)['w']
        derivative=(-w(S+2*h)+8*w(S+h)-8*w(S-h)+w(S-2*h))/(12*h)
        self.assertLess(abs(derivative-model.state(S)['wS']),mp.mpf('1e-13'))

    def test_grid_reports_finite_scope_and_cli_status(self):
        model=self.model()
        result=model.report(samples=51)
        self.assertEqual(result['scan']['samples'],51)
        self.assertEqual(result['scan']['unhealthy_clock_probes'],0)
        self.assertFalse(result['scan']['interval_certified'])
        self.assertEqual(model.completion_status(result),0)
        self.assertEqual(model.completion_status(result,True),2)
        bad=dict(result,scan=dict(result['scan'],unhealthy_clock_probes=1))
        self.assertEqual(model.completion_status(bad),1)

    def test_invalid_initial_data_are_rejected(self):
        model=self.model()
        for S,k in ((0,'.2'),('.1',-1)):
            with self.assertRaises(ValueError):model.state(S,k=k)


if __name__=='__main__':
    unittest.main()
