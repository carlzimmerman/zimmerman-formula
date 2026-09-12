"""Test-first contracts; each expected identity is independently hand-derived."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s

SOURCE=Path(__file__).with_name('current_audit.py')
if SOURCE.exists():
    spec=importlib.util.spec_from_file_location('current_under_test',SOURCE)
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
else:
    audit=None


class CurrentTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(audit,'The same-action current derivation has not been implemented.')

    def test_covariant_current_cubic_sign_and_projector(self):
        # Catches omitting the derivative of X or reversing the shift-current sign.
        z=audit.covariant();symbols=z['symbols']
        gamma,PX,s0,WY=symbols['gamma'],symbols['PX'],symbols['s0'],symbols['WY']
        grad=symbols['gradient'];H=symbols['hessian'];eta=s.diag(-1,1,1,1)
        box=-H[0,0]+H[1,1]+H[2,2]+H[3,3]
        for mu in range(4):
            expected=-2*(PX+gamma*box)*eta[mu,mu]*grad[mu]
            expected+=2*s0*WY*grad[mu] if mu else 0
            expected+=2*gamma*eta[mu,mu]*sum(eta[k,k]*grad[k]*H[mu,k] for k in range(4))
            self.assertEqual(s.expand(z['current'][mu]-expected),0)

    def test_reduced_radial_action_cancels_second_radial_derivative(self):
        # Catches a missing volume derivative, a missing lapse force, or wrong area term.
        z=audit.radial();v=z['symbols']
        F,N,p,Q,gamma,PX,WY,K,Np=(v[k] for k in ('F','N','p','Q','gamma','PX','WY','K','Np'))
        expected=2*F*(-(PX-WY/N)*p+gamma*Q**2*Np/N**3-gamma*F*K*p**2)
        self.assertEqual(s.factor(z['Jr_reduced']-expected),0)
        self.assertEqual(s.factor(z['Jr_covariant']-expected),0)
        self.assertNotIn(v['pp'],z['Jr_reduced'].free_symbols)
        self.assertNotIn(v['Fp'],z['Jr_reduced'].free_symbols)

    def test_charge_density_is_not_automatically_stationary(self):
        # Catches incorrectly dropping explicit tau-dependence on a static geometry.
        z=audit.radial();v=z['symbols']
        self.assertEqual(s.simplify(z['dJt_dt']-2*v['Q']*v['PXtau']/v['N']**2),0)
        self.assertEqual(z['dJt_dt'].subs({v['Q']:2,v['PXtau']:3,v['N']:2}),3)

    def test_plane_and_spherical_cubic_are_different(self):
        # Catches importing the 2/r area term into a plane, or losing it in a sphere.
        z=audit.radial();v=z['symbols']
        common={v['F']:1,v['N']:1,v['Np']:0}
        plane=s.factor(z['Jr_reduced'].subs(common).subs(v['K'],0))
        self.assertEqual(s.expand(plane+2*(v['PX']-v['WY'])*v['p']),0)
        r=s.symbols('r',positive=True)
        sphere=z['Jr_reduced'].subs(common).subs(v['K'],2/r)
        self.assertEqual(s.factor(sphere-plane+4*v['gamma']*v['p']**2/r),0)

    def test_root_polynomial_keeps_unsquared_sign_condition(self):
        # Catches treating every squared polynomial root as an actual current root.
        z=audit.root_algebra();v=z['symbols']
        p,N,d,D,S,H=(v[k] for k in ('p','N','d','D','S','H'))
        self.assertEqual(s.expand(z['polynomial']-(N**2*S*H**2-d**2*p**2*D**2)),0)
        self.assertTrue(audit.accept_squared_candidate(1,1,1))
        self.assertFalse(audit.accept_squared_candidate(-1,1,1))
        self.assertFalse(audit.accept_squared_candidate(1,1,-1))

    def test_regular_center_excludes_stationary_outflow_not_depletion(self):
        # Catches conflating no center source with stationary enclosed charge.
        z=audit.continuity();v=z['symbols']
        self.assertEqual(s.simplify(z['outward_flux']+v['charge_rate']-v['center_flux']),0)
        self.assertEqual(z['outward_flux'].subs({v['charge_rate']:-3,v['center_flux']:0}),3)
        self.assertEqual(z['outward_flux'].subs({v['charge_rate']:0,v['center_flux']:0}),0)
        self.assertEqual(z['regular_center_limit'],0)

    def test_nontrivial_zero_current_branch_can_be_center_regular(self):
        # Catches discarding the cubic branch merely because psi is regular at r=0.
        z=audit.root_algebra()
        self.assertIn('center_symbols',z,'Regular nontrivial center branch not implemented.')
        v=z['center_symbols']
        self.assertEqual(s.simplify(z['center_slope']+v['A0']/(2*v['gamma'])),0)
        self.assertEqual(z['center_slope'].subs({v['A0']:2,v['gamma']:1}),-1)
        self.assertEqual(z['center_cubic'].subs({v['A0']:2,v['AY']:3,v['gamma']:1}),-s.Rational(3,2))
        self.assertEqual(z['center_residual_through_cubic'],0)

    def test_frozen_action_roots_are_exhaustive_for_recorded_slice(self):
        # Catches loss of zero/nonzero branches or failure to reject squared extras.
        z=audit.frozen_slice()
        self.assertGreaterEqual(len(z['accepted_roots']),2)
        self.assertEqual(z['real_polynomial_roots'],len(z['candidates']))
        self.assertTrue(z['all_roots_classified'])
        self.assertTrue(all(row.get('sign_certified',False) for row in z['candidates']))
        self.assertTrue(all(abs(row['current'])<1e-9 for row in z['accepted_roots']))
        self.assertTrue(any(abs(row['p'])>1e-6 for row in z['accepted_roots']))
        self.assertGreater(abs(z['PXtau_at_p_zero']),1e-10)
        self.assertIn('time_dependence_rows',z,'Actual frozen time-dependence range not evaluated.')
        self.assertEqual(len(z['time_dependence_rows']),5)
        self.assertTrue(all(abs(row['P_Xtau'])>1e-10 for row in z['time_dependence_rows']))

    def test_regular_center_branch_has_timelike_original_action_witness(self):
        # Catches presenting only spacelike algebraic roots as a timelike witness.
        z=audit.frozen_slice()
        self.assertIn('small_radius_witness',z,'Timelike original-action witness not computed.')
        row=z['small_radius_witness']
        self.assertTrue(-.00025<row['p']<-.00024)
        self.assertGreater(row['X'],0)
        self.assertLess(abs(row['covariant_original_current']),1e-16)
        self.assertLess(abs(row['reduced_original_current']),1e-16)
        self.assertGreater(abs(row['dJt_dt']),1e-3)
        self.assertIn('Jt',row,'The witness charge sign must be reported, not assumed positive.')
        self.assertLess(row['Jt'],0)


if __name__=='__main__':
    unittest.main()
