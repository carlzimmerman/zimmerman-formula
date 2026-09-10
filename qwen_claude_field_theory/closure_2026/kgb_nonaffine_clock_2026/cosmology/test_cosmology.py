#!/usr/bin/env python3
import importlib
import unittest
import sympy as s


def calculation():
    try:return importlib.import_module('cosmology_checks')
    except ModuleNotFoundError:raise AssertionError('same-action cosmology calculation is not yet implemented')


class CosmologyTests(unittest.TestCase):
    def test_mapped_fluid_lapse_pressure_and_current(self):
        self.assertTrue(all(value==0 for value in calculation().fluid_variation()['residuals'].values()))

    def test_KGB_homogeneous_action_and_kinetic_coefficient(self):
        self.assertTrue(all(value==0 for value in calculation().homogeneous_action()['residuals'].values()))

    def test_dust_is_not_EF_minimal_but_radiation_is_trace_free(self):
        a=calculation().matter_map(s.Rational(1,2),s.Rational(21,20),s.Rational(1,10),0,10,0,1)
        self.assertEqual(a['rho_EF'],s.Rational(200,21))
        self.assertNotEqual(a['rho_EF'],s.Rational(4000,441))
        self.assertEqual(a['homogeneous_matter_kinetic'],s.Rational(1,2))
        r=calculation().matter_map(s.Rational(1,2),s.Rational(21,20),s.Rational(1,10),0,10,s.Rational(10,3),1)
        self.assertEqual(r['current_EF'],0)
        self.assertEqual(r['rho_EF'],s.Rational(4000,441))

    def test_quadratic_positive_curvature_field_barrier(self):
        X,j=s.symbols('X j',positive=True)
        a=calculation().quadratic_F(X,j)
        self.assertEqual(s.factor(a['Dfield']-(1+j*(s.Rational(1,4)-X*X))),0)
        self.assertEqual(s.factor(a['Dfield'].subs(X,s.sqrt(s.Rational(1,4)+1/j))),0)

    def test_negative_curvature_Ricci_barrier(self):
        j=-s.Integer(100000)
        boundary=calculation().first_upper_barrier(j)
        self.assertEqual(boundary['kind'],'F_zero')
        self.assertEqual(s.simplify(calculation().quadratic_F(boundary['X'],j)['F']),0)

    def test_galaxy_two_jet_does_not_fix_early_energy(self):
        a=calculation().jet_ambiguity()
        self.assertEqual(a['same_seed_2jet'],[0,0,0])
        self.assertNotEqual(a['early_EF_energy_lambda_coefficient'],0)

    def test_horizon_ratio_does_not_determine_mode_acceleration(self):
        a=calculation().l121_recheck()
        self.assertAlmostEqual(a['ratio_constant'],6.155600671402932e-6,delta=1e-18)
        self.assertGreater(a['mode_examples'][0]['g_over_global_a0'],a['mode_examples'][1]['g_over_global_a0'])
        self.assertAlmostEqual(a['ratio_constant']*a['Hrec_over_H0'],a['ratio_today'])

    def test_physical_to_EF_FLRW_time_and_expansion(self):
        t=s.Symbol('t',real=True);X=s.Function('X')(t);a=s.Function('a')(t);C=s.Function('C')(X)
        out=calculation().flrw_map(s.diff(a,t)/a,s.diff(X,t),X,C,s.diff(C,X))
        expected=s.diff(s.sqrt(C)*a,t)/(C*a)
        self.assertEqual(s.simplify(out['H_EF']-expected),0)


if __name__=='__main__':unittest.main(verbosity=2)
