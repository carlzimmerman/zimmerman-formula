import importlib.util
import unittest
import sympy as s


class ActionBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.find_spec('derive')
        cls.available=spec is not None
        if cls.available:
            import derive
            cls.result=derive.construct()

    def data(self):
        self.assertTrue(self.available,'missing unrestricted cosmological action bridge')
        return self.result

    def test_independent_density_and_momentum(self):
        d=self.data()
        self.assertEqual(s.expand(d['rho_delta']-d['rho_target']),0)
        self.assertEqual(s.expand(d['momentum']-d['momentum_target']),0)

    def test_independent_pressure(self):
        d=self.data()
        self.assertEqual(s.expand(d['pressure_delta']-d['pressure_target']),0)

    def test_shear_equation_derives_no_slip(self):
        d=self.data();v=d['s']
        self.assertEqual(s.expand(d['euler']['e']+v['M2']*v['a']*v['k']**2*d['slip']),0)

    def test_matter_clock_separation(self):
        d=self.data();v=d['s']
        self.assertEqual(s.diff(d['radiation'],v['n'],2),6*v['a']**3*v['Cr']*v['qr']**4)
        self.assertEqual(s.diff(d['dust'],v['drho'],v['td']),v['a']**3/2)
        self.assertEqual(s.diff(d['clock'],v['e']),0)

    def test_homogeneous_shift_disappears(self):
        d=self.data();v=d['s']
        self.assertEqual(s.expand(d['euler']['b'].subs(v['k'],0)),0)

    def test_general_clock_rate_not_reconstructed_lapse_one(self):
        d=self.data();v=d['s']
        self.assertIn('sbar',v,'clock rate must respond on a matter-containing background')
        self.assertEqual(s.diff(d['pressure_delta'],v['W']),-v['n']*v['sbar'])

    def test_both_offshell_ward_identities(self):
        d=self.data()
        self.assertIn('ward',d,'finite-k off-shell conservation bridge missing')
        for name,expr in d['ward'].items():
            self.assertEqual(s.expand(expr),0,name)

    def test_fixed_action_background_preservation(self):
        d=self.data()
        self.assertIn('background',d,'same-action sourced homogeneous system missing')
        for expr in d['background']['checks'].values():
            self.assertEqual(s.expand(expr),0)

    def test_true_homogeneous_mode_normalization(self):
        d=self.data();v=d['s']
        self.assertEqual(s.expand(d['homogeneous_action']-2*d['action'].subs(
            {v['k']:0,v['e']:0,v['ed']:0})),0)


if __name__=='__main__':unittest.main()
