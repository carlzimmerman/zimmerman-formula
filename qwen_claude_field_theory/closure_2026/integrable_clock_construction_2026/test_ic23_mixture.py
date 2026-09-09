"""Three coupled scalar modes from one summed matter action."""
import importlib.util
from pathlib import Path
import unittest
import mpmath as mp


class MixtureTests(unittest.TestCase):
    def model(self):
        path=Path(__file__).with_name('ic23_mixture.py')
        self.assertTrue(path.exists(),'Combined radiation/baryon action reduction missing')
        spec=importlib.util.spec_from_file_location('ic23',path)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        mp.mp.dps=60
        return m

    def test_exact_mixed_equations_and_completed_squares(self):
        m=self.model();self.assertTrue(all(x==0 for x in m.identities().values()))

    def test_both_densities_source_the_same_background(self):
        m=self.model();b=m.background()
        self.assertLess(max(map(abs,b['constraints'])),mp.mpf('1e-45'))
        self.assertEqual(len(b['fluids']),2)
        self.assertGreater(b['H_physical'],0)

    def test_three_characteristics_are_derived_from_combined_matrix(self):
        m=self.model();r=m.principal(m.background())
        self.assertEqual(len(r['speeds_squared']),3)
        self.assertTrue(all(0<x<1 for x in r['speeds_squared']))
        self.assertGreater(r['gradient_margin'],0)
        self.assertGreater(r['lightcone_margin'],0)

    def test_full_frequency_equation_agrees_with_principal_formula(self):
        m=self.model();b=m.background();r=m.frequencies(b,'1e14')
        self.assertEqual(len(r['growth_exponents']),6)
        self.assertLess(r['maximum_eigen_residual'],mp.mpf('1e-40'))
        expected=sorted(m.principal(b)['speeds_squared'])
        measured=sorted(x['imag']**2/(mp.exp(2*b['S'])*mp.mpf('1e14')) for x in r['growth_exponents'] if x['imag']>0)
        self.assertEqual(len(expected),len(measured))
        self.assertLess(max(abs(x-y) for x,y in zip(expected,measured)),mp.mpf('1e-7'))

    def test_combined_background_is_actually_continued(self):
        m=self.model();self.assertTrue(hasattr(m,'continuation'))
        r=m.continuation(target_Q='.0001',step='.00001')
        self.assertGreater(len(r['states']),1)
        self.assertLess(r['maximum_constraint_residual'],mp.mpf('1e-40'))
        self.assertLess(r['maximum_charge_residual'],mp.mpf('1e-40'))

    def test_mixed_auxiliary_mode_matrix_is_computed(self):
        m=self.model();self.assertTrue(hasattr(m,'constraint_matrix'));b=m.background()
        for k2 in (0,1,10000):self.assertEqual(m.constraint_matrix(b,k2)['rank'],4)

    def test_potential_controller_is_an_equation_not_an_assigned_multiplier(self):
        m=self.model();self.assertTrue(hasattr(m,'control_diagnostics'))
        b=m.background();r=m.control_diagnostics(b)
        self.assertGreater(abs(r['denominator']),mp.mpf('1e-8'))
        self.assertLess(abs(r['reconstructed_Sdot']-b['Sdot']),mp.mpf('1e-40'))

    def test_potential_second_jet_controls_actual_lapse_curvature(self):
        m=self.model();self.assertTrue(hasattr(m,'lapse_potential_control'))
        r=m.lapse_potential_control(m.background(),target_M='-3')
        self.assertLess(abs(r['computed_lapse_Schur']+3),mp.mpf('1e-40'))
        self.assertTrue(0<r['computed_gravity_diagonal']<1)


if __name__=='__main__':unittest.main()
