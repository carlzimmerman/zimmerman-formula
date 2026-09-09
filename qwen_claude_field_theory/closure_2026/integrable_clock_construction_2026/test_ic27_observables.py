"""Physical-metric reconstruction tests; no expected slip or PPN is assigned."""
import importlib.util
import unittest
import mpmath as mp
import sympy as s
import ic26_three_functions as action


class ObservableTests(unittest.TestCase):
    def implementation(self):
        self.assertIsNotNone(importlib.util.find_spec('ic27_observables'),
                             'Physical-metric reconstruction is not implemented')
        import ic27_observables
        return ic27_observables

    def test_lie_derivative_gauge_invariance(self):
        m=self.implementation()
        residuals=m.gauge_audit()
        self.assertGreaterEqual(len(residuals),5)
        for name,value in residuals.items():
            self.assertEqual(s.simplify(value),0,name)

    def test_shift_satisfies_momentum_and_tracefree_evolution(self):
        m=self.implementation()
        with mp.workdps(45):
            b=action.completed(action.initial())
            k=mp.mpf('.13');phase=mp.matrix([.2,.3,-.7,.11,-.23,.41])
            r=m.reconstruct(b,k,phase)
            q,rad,mat=phase[3],phase[1],phase[2]
            j=[f['j'] for f in b['entries']]
            source=q-mp.mpf('1.5')*(j[0]*rad+j[1]*mat)
            self.assertLess(abs(2*r['s_TF']+source),mp.mpf('1e-38'))
            self.assertLess(abs(2*b['t']*r['s_TF']-2*k*r['chi']),mp.mpf('1e-38'))

    def test_reconstructed_metric_obeys_both_matter_equations(self):
        m=self.implementation()
        with mp.workdps(45):
            b=action.completed(action.initial())
            for k in (mp.mpf('.001'),mp.mpf(1),mp.mpf(100)):
                phase=mp.matrix([.2,.3,-.7,.11,-.23,.41])
                r=m.reconstruct(b,k,phase)
                dot=action.base.hamiltonian_generator(b,k)*phase
                for i,f in enumerate(b['entries'],1):
                    field=f['u']*(r['delta_S']+f['w']*(phase[i+3]/f['j']-3*phase[0]))
                    charge=-3*b['Qdot']*phase[i+3]-f['j']*k*r['chi']-mp.exp(2*b['S'])*f['j']*k*phase[i]/f['u']
                    self.assertLess(abs(dot[i]-field),mp.mpf('1e-35'))
                    self.assertLess(abs(dot[i+3]-charge),mp.mpf('1e-35'))

    def test_potential_map_equals_evolving_metric_derivative(self):
        m=self.implementation()
        with mp.workdps(45):
            b=action.completed(action.initial());k=mp.mpf('.2')
            phase=mp.matrix([.2,.3,-.7,.11,-.23,.41])
            dot=action.base.hamiltonian_generator(b,k)*phase
            r=m.reconstruct(b,k,phase)
            def shear(dt):
                row=action.completed(action.moved(b,dt))
                return m.constraint_fields(row,k*mp.exp(-2*b['Qdot']*dt),phase+dt*dot)['chi']
            chi_dot=mp.diff(shear,0)
            phi=r['delta_S']+mp.exp(-2*b['S'])*(chi_dot-b['flow'][0]*r['chi'])
            self.assertLess(abs(phi-r['Phi']),mp.mpf('1e-33'))
            mapped=m.observable_matrix(b,k)*phase
            for x,key in zip(mapped,m.OBSERVABLES):
                self.assertLess(abs(x-r[key]),mp.mpf('1e-33'),key)

    def test_zero_mode_not_divided_by_k_squared(self):
        m=self.implementation()
        with mp.workdps(30):
            b=action.completed(action.initial())
            with self.assertRaises(ValueError):
                m.reconstruct(b,0,mp.zeros(6,1))

    def test_auxiliary_dressing_controls_actual_slip(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'dressing_slip'),'Auxiliary dressing identity not implemented')
        with mp.workdps(45):
            b=action.completed(action.initial())
            for k in (mp.mpf('.001'),mp.mpf('.1'),mp.mpf(10)):
                for i in range(6):
                    phase=mp.eye(6)[:,i]
                    r=m.reconstruct(b,k,phase)
                    d=m.dressing_slip(b,k,phase)
                    self.assertLess(abs(r['Phi']-r['Psi']-d['slip']),mp.mpf('1e-34'))
                    self.assertLess(abs(d['auxiliary_residual']),mp.mpf('1e-34'))

    def test_symbolic_slip_from_unreduced_hamiltonian(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'slip_audit'),'Hamiltonian slip reduction not implemented')
        for name,value in m.slip_audit().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_zero_slip_initial_state_is_constructed_not_assumed(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'slip_preservation'),'Slip preservation not implemented')
        with mp.workdps(45):
            b=action.completed(action.initial());k=mp.mpf('.1')
            r=m.slip_preservation(b,k)
            phase=mp.matrix(r['zero_slip_phase'])
            values=m.reconstruct(b,k,phase)
            self.assertLess(abs(values['Phi']-values['Psi']),mp.mpf('1e-33'))
            dot=action.base.hamiltonian_generator(b,k)*phase
            def slip(dt):
                row=action.completed(action.moved(b,dt))
                metric=m.reconstruct(row,k*mp.exp(-2*b['Qdot']*dt),phase+dt*dot)
                return metric['Phi']-metric['Psi']
            actual=mp.diff(slip,0)
            self.assertLess(abs(actual-r['initial_slip_derivative']),mp.mpf('1e-30'))

    def test_slip_equals_variation_of_physical_tensor_kinetic_coupling(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'tensor_mass_variation'),'Physical tensor normalization not implemented')
        with mp.workdps(45):
            b=action.completed(action.initial());k=mp.mpf('.1')
            phase=mp.matrix([.2,.3,-.7,.11,-.23,.41])
            r=m.reconstruct(b,k,phase);d=m.dressing_slip(b,k,phase)
            result=m.tensor_mass_variation(b,k,phase)
            wc=action.model.normalized.constants()['wc']
            def kinetic(S,z):
                v=mp.exp(S+2*wc)/2+z*z
                t=mp.exp(2*S)/v
                return 2*mp.exp(S-2*wc)/t
            perturb=mp.diff(lambda eps:mp.log(kinetic(
                b['S']+eps*r['delta_S'],b['z']+eps*d['delta_z'])),0)
            rate=mp.diff(lambda dt:mp.log(kinetic(
                b['S']+dt*b['flow'][0],b['z']+dt*b['flow'][2])),0)
            self.assertLess(abs(result['delta_log_M2_B']-perturb-rate*r['clock_B']),mp.mpf('1e-34'))
            self.assertLess(abs(r['Phi']-r['Psi']+result['delta_log_M2_B']),mp.mpf('1e-34'))


if __name__=='__main__':
    unittest.main()
