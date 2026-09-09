"""Distinct constant-tensor candidate, no inherited IC26 certification."""
import importlib.util
import unittest
import mpmath as mp
import sympy as s


class ConstantTensorTests(unittest.TestCase):
    def implementation(self):
        self.assertIsNotNone(importlib.util.find_spec('ic28_constant_tensor'),
                             'Constant-tensor branch is not implemented')
        import ic28_constant_tensor
        return ic28_constant_tensor

    def test_raw_action_compatibility_identities(self):
        m=self.implementation()
        for name,value in m.identities().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_actual_varied_background_constraints_and_preservation(self):
        m=self.implementation()
        with mp.workdps(50):
            b=m.witness()
            self.assertLess(max(abs(x) for x in b['constraints']+b['preservation']),mp.mpf('1e-35'))
            self.assertGreater(b['H_physical'],0)
            self.assertGreater(b['a'],0)
            self.assertLess(b['M'],0)
            self.assertGreater(b['principal']['gravity_diagonal'],0)
            self.assertLess(b['principal']['gravity_diagonal'],1)

    def test_independently_reconstructed_potentials_have_no_slip(self):
        m=self.implementation()
        with mp.workdps(50):
            b=m.witness()
            for k in (mp.mpf('.001'),mp.mpf(1),mp.mpf(100)):
                for i in range(6):
                    metric=m.physical_fields(b,k,mp.eye(6)[:,i])
                    self.assertLess(abs(metric['Phi']-metric['Psi']),mp.mpf('1e-35'))

    def test_lapse_and_shear_agree_with_matter_equations(self):
        m=self.implementation()
        with mp.workdps(50):
            b=m.witness();k=mp.mpf('.1');phase=mp.matrix([.2,.3,-.7,.11,-.23,.41])
            f=m.physical_fields(b,k,phase);dot=m.generator(b,k)*phase
            for i,row in enumerate(b['entries'],1):
                expect=row['u']*(f['delta_S']+row['w']*(phase[i+3]/row['j']-3*phase[0]))
                self.assertLess(abs(dot[i]-expect),mp.mpf('1e-35'))

    def test_fixed_functions_evolve_with_conserved_charge(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'evolve'),'Same-action evolution missing')
        h=m.evolve(target_Q=.0001,max_step=.00001)
        self.assertTrue(h['success'],h['reason'])
        self.assertLess(h['maximum_charge_drift'],1e-8)

    def test_full_euler_spectrum_keeps_all_modes(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'frequencies'),'Full nonautonomous spectrum missing')
        with mp.workdps(45):
            b=m.witness();r=m.frequencies(b,mp.mpf('1e14'))
            self.assertEqual(len(r['roots']),6)
            self.assertLess(r['residual'],mp.mpf('1e-30'))
            values=sorted(float(abs(mp.im(x))**2/(mp.exp(2*b['S'])*mp.mpf('1e14'))) for x in r['roots'])
            expected=sorted([float(x) for x in mp.eig(b['principal']['symbol'],left=False,right=False)]*2)
            for a,c in zip(values,expected):
                self.assertLess(abs(a-c)/max(c,1e-15),.002)

    def test_integrated_potential_has_genuine_derivative_jets(self):
        m=self.implementation()
        self.assertTrue(hasattr(m,'integrated_state'),'Integrated potential construction missing')
        with mp.workdps(45):
            b=m.witness();r=m.integrated_state(b['S'],b['q'],b['z'],b['Q'],b['fluids'],b['parameters'])
            for value in m.integrability(r).values():
                self.assertLess(abs(value),mp.mpf('1e-32'))

    def test_integrated_positive_auxiliary_chart_cannot_jump_across_zero(self):
        m=self.implementation()
        with mp.workdps(30):
            b=m.witness()
            with self.assertRaises(ValueError):
                m.integrated_state(b['S'],b['q'],-b['z'],b['Q'],b['fluids'],b['parameters'])


if __name__=='__main__':
    unittest.main()
