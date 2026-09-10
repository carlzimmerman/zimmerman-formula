"""Regression identities independent of the solver's reported verdict.

Changing the source sign, omitting the physical z=u-b*n conversion, or
discarding the shift term in Ricci must fail these tests.
"""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class ResponseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name('response_gate.py')
        spec = importlib.util.spec_from_file_location('response_gate', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.module = module
        cls.a = module.derive()

    def test_variation_residuals(self):
        self.assertEqual(self.a['residuals'], [0, 0, 0])

    def test_known_compensator_response(self):
        a = self.a; m,q,mu,b,d,r,w,rho,S = a['symbols']
        actual = s.factor(a['R00'].subs({b:0,d:2,r:-1}))
        self.assertEqual(s.simplify(s.limit(actual,w,s.oo)-(rho-S)/(2*m)),0)
        self.assertEqual(s.factor(a['speed2'].subs({b:0,d:2,r:-1})-2*mu/(3*(1+mu))),0)

    def test_velocity_mixing_source_contact(self):
        a=self.a; m,q,mu,b,d,r,w,rho,S=a['symbols']
        C=r*(1-b)**2-mu
        expected=-3*b*(b*S+(b*r-r+1)*rho)/(2*m*q*C)
        self.assertEqual(s.factor(a['omega2_contact']-expected),0)
        self.assertNotEqual(s.factor(a['omega2_contact'].subs({b:1,S:1,rho:0})),0)

    def test_constant_speed_tuning_does_not_certify_response(self):
        a=self.a; m,q,mu,b,d,r,w,rho,S=a['symbols']
        self.assertEqual(s.factor(a['speed2'].subs({b:0,r:-1,d:1+mu})-s.Rational(1,3)),0)
        expected=((3*mu-1)*rho/(1+mu)-S)/(2*m*mu)
        self.assertEqual(s.factor(a['tuned_contact']-expected),0)
        self.assertNotEqual(s.factor(s.diff(a['tuned_contact'],S,mu)),0)

    def test_static_branch_is_derived(self):
        a=self.a; m,q,mu,b,d,r,w,rho,S=a['symbols']
        self.assertEqual(s.factor(a['static_n']+rho/(2*m*q*mu)),0)
        self.assertEqual(s.factor(a['static_z']+a['static_n']),0)

    def test_GR_contact_matched_family_retains_vacuum_remainder(self):
        self.assertIn('matched_vacuum_remainder',self.a)
        a=self.a; m,q,mu,b,d,r,w,rho,S=a['symbols']
        mt,ml,Z=s.symbols('mu_t mu_l Z',positive=True)
        expected=-d*d*(d-1)**2*(ml-mt)**5*Z**5/(9*(d-1+mt)**5)
        self.assertEqual(s.factor(a['matched_vacuum_remainder']-expected),0)
        self.assertEqual(a['matched_vacuum_R00_residual'],0)
        self.assertEqual(a['matched_division_residual'],0)


if __name__=='__main__':
    unittest.main()
