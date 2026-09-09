"""Break-sensitive tests for two-function action reconstruction."""
import importlib.util
import unittest
import mpmath as mp


class CoupledTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic25_coupled'),'Two-function reconstruction missing')
        import ic25_coupled
        return ic25_coupled

    def test_characteristic_polynomial_predicts_unused_slope(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();p=m.polynomial(b)
            x=mp.mpf('.37');r=m.trial(b,x)
            self.assertLess(abs(r['principal']['gravity_diagonal']-(p[0]*x*x+p[1]*x+p[2])),mp.mpf('1e-28'))

    def test_actual_variation_recovers_designed_history(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();r=m.control(b)
            self.assertLess(abs(r['flow'][0]-b['kappa']*r['Qdot']),mp.mpf('1e-28'))
            self.assertLess(abs(r['principal']['gravity_diagonal']-b['target']),mp.mpf('1e-28'))
            self.assertLess(max(map(abs,r['constraints'])),mp.mpf('1e-28'))
            self.assertLess(r['M'],0)

    def test_two_function_integrability(self):
        m=self.module()
        self.assertTrue(hasattr(m,'completed'),'Second action jets missing')
        with mp.workdps(45):
            r=m.completed(m.initial());errors=m.integrability(r)
            self.assertLess(max(map(abs,errors.values())),mp.mpf('1e-30'))

    def test_integrator_recovers_monotonic_history(self):
        m=self.module()
        self.assertTrue(hasattr(m,'evolve'),'Two-function integrator missing')
        out=m.evolve(.005)
        self.assertTrue(out['success'])
        self.assertAlmostEqual(out['Q_end'],.005,places=10)
        self.assertLess(out['maximum_charge_drift'],1e-8)
        self.assertLess(out['maximum_target_error'],1e-10)

    def test_full_roots_and_computed_constraint_matrix(self):
        m=self.module()
        self.assertTrue(hasattr(m,'frequencies'),'Frozen S-only higher-jet variation missing')
        with mp.workdps(60):
            r=m.completed(m.initial());f=m.frequencies(r,mp.mpf('1e14'))
            actual=sorted(mp.im(x)**2/(mp.exp(2*r['S'])*mp.mpf('1e14')) for x in f['roots'] if mp.im(x)>0)
            expected=sorted(mp.re(x) for x in mp.eig(r['principal']['symbol'],left=False,right=False))
            self.assertEqual(len(actual),3)
            self.assertLess(max(abs(x-y) for x,y in zip(actual,expected)),mp.mpf('1e-7'))
            self.assertLess(f['residual'],mp.mpf('1e-40'))
            for k2 in (0,1,10000):self.assertEqual(m.prior.brackets(r,k2)['rank'],4)

    def test_hamiltonian_flow_preserves_weighted_symplectic_form(self):
        m=self.module()
        self.assertTrue(hasattr(m,'hamiltonian_generator'),'Nonautonomous Hamiltonian generator missing')
        with mp.workdps(40):
            r=m.completed(m.initial());G=m.hamiltonian_generator(r,7)
            D=mp.diag([2,1,1]);Omega=mp.zeros(6)
            for i in range(3):Omega[i,i+3]=D[i,i];Omega[i+3,i]=-D[i,i]
            self.assertLess(mp.norm(G.T*Omega+Omega*G+3*r['Qdot']*Omega),mp.mpf('1e-25'))

    def test_time_transport_not_just_frozen_roots(self):
        m=self.module()
        self.assertTrue(hasattr(m,'transport'),'Perturbation propagator missing')
        h=m.evolve(.005);out=m.transport(h,k2_initial=1,nodes=7)
        self.assertLess(out['relative_volume_error'],1e-7)
        self.assertGreater(out['weighted_singular_values'][0],0)

    def test_exact_slope_and_hamiltonian_identities(self):
        m=self.module()
        self.assertTrue(hasattr(m,'identities'),'Exact designer identities missing')
        self.assertTrue(all(x==0 for x in m.identities().values()))

    def test_pin_off_stratum_is_not_silently_continued(self):
        m=self.module()
        with mp.workdps(35):
            b=m.initial();b['q']=mp.mpf('-1')
            with self.assertRaisesRegex(ValueError,'pin'):m.trial(b,1)

    def test_charge_scaled_clock_derives_consistent_jets(self):
        m=self.module()
        self.assertTrue(hasattr(m,'clock_slope'),'Charge-scaled history missing')
        with mp.workdps(40):
            b=m.initial(profile='charge');r=m.completed(b)
            self.assertLess(max(map(abs,m.integrability(r).values())),mp.mpf('1e-27'))
            self.assertGreater(r['pin_activation'],0)
            shifted=dict(b);shifted['Q']=mp.mpf(2)
            self.assertLess(abs(m.clock_slope(shifted)/m.clock_slope(b)-mp.exp(-6)),mp.mpf('1e-30'))


if __name__=='__main__':unittest.main()
