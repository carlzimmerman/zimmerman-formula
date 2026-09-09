"""Same-action three-function design, no phenomenological mass insertion."""
import importlib.util
import unittest
import mpmath as mp


class ThreeFunctionTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic26_three_functions'),'Third coefficient construction missing')
        import ic26_three_functions
        return ic26_three_functions

    def test_independent_multiplier_and_cone_targets(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();r=m.control(b)
            self.assertLess(abs(r['M']-b['target_M']),mp.mpf('1e-28'))
            self.assertLess(abs(r['flow'][0]-m.base.clock_slope(b)*r['Qdot']),mp.mpf('1e-28'))
            self.assertLess(abs(r['principal']['gravity_diagonal']-b['target']),mp.mpf('1e-28'))

    def test_third_function_integrates_its_action_jets(self):
        m=self.module()
        self.assertTrue(hasattr(m,'completed'),'Genuine second action jets missing')
        with mp.workdps(45):
            r=m.completed(m.initial());errors=m.integrability(r)
            self.assertLess(max(map(abs,errors.values())),mp.mpf('1e-30'))

    def test_homogeneous_terms_were_not_omitted(self):
        m=self.module()
        self.assertTrue(all(x==0 for x in m.homogeneous_audit().values()))

    def test_same_action_history(self):
        m=self.module()
        self.assertTrue(hasattr(m,'evolve'),'Three-function evolution missing')
        h=m.evolve(.005)
        self.assertTrue(h['success'])
        self.assertAlmostEqual(h['Q_end'],.005,places=10)
        self.assertLess(h['maximum_charge_drift'],1e-8)

    def test_full_new_action_modes(self):
        m=self.module()
        self.assertTrue(hasattr(m,'frequencies'),'Three-function Taylor variation missing')
        with mp.workdps(60):
            r=m.completed(m.initial());out=m.frequencies(r,mp.mpf('1e14'))
            actual=sorted(mp.im(x)**2/(mp.exp(2*r['S'])*mp.mpf('1e14')) for x in out['roots'] if mp.im(x)>0)
            expected=sorted(mp.re(x) for x in mp.eig(r['principal']['symbol'],left=False,right=False))
            self.assertEqual(len(actual),3)
            self.assertLess(max(abs(x-y) for x,y in zip(actual,expected)),mp.mpf('1e-7'))
            self.assertLess(out['residual'],mp.mpf('1e-40'))

    def test_actual_propagator_volume(self):
        m=self.module()
        self.assertTrue(hasattr(m,'transport'),'Three-function propagator missing')
        h=m.evolve(.005);t=m.transport(h,100,7)
        self.assertLess(t['relative_volume_error'],1e-7)

    def test_clock_band_rational_formula_matches_direct_derivatives(self):
        m=self.module()
        self.assertTrue(hasattr(m,'clock_band'),'Finite-band rational diagnostic missing')
        with mp.workdps(40):
            r=m.completed(m.initial());result=m.clock_band(r)
            self.assertLess(max(abs(x) for x in result['direct_residuals']),mp.mpf('1e-25'))

    def test_high_precision_transport_volume(self):
        m=self.module()
        self.assertTrue(hasattr(m,'precision_transport'),'Independent precision propagation missing')
        h=m.evolve(.005);r=m.precision_transport(h,100,4)
        self.assertLess(float(r['relative_volume_error']),1e-30)

    def test_tensor_coefficients_from_raw_action(self):
        m=self.module()
        with mp.workdps(40):
            r=m.completed(m.initial())
            speed=-r['t']*r['raw']['R']/mp.exp(2*r['S'])
            self.assertLess(abs(speed-1),mp.mpf('1e-30'))
            self.assertGreater(1/(4*r['t']),0)

    def test_quartic_control_slope_is_actually_varied(self):
        m=self.module()
        with mp.workdps(40):
            b=m.initial();alpha=mp.mpf(1)
            def raw(beta):return m.model.raw_jets(b['S'],b['q'],b['z'],0,m.first_jets(b,alpha,beta))
            def cross(beta):
                r=raw(beta);return r['Sq']-r['Sz']*r['qz']/r['zz']
            r=raw(0);expected=2*b['z']**3*r['qz']/r['zz']
            self.assertLess(abs(mp.diff(cross,0)-expected),mp.mpf('1e-28'))


if __name__=='__main__':unittest.main()
