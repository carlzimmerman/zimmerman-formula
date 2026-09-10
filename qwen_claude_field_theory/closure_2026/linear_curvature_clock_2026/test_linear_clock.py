"""Independent controls for a changed auxiliary action, not a success counter."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class LinearClockTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).with_name('linear_clock.py')
        cls.present=path.exists()
        if cls.present:
            spec=importlib.util.spec_from_file_location('linear_clock',path)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            cls.a=module.derive()

    def setUp(self):
        self.assertTrue(self.present,'new action computation missing')

    def test_independent_static_fields(self):
        self.assertEqual(self.a['static']['slip_residual'],0)
        self.assertEqual(self.a['static']['chi_gradient'],0)
        self.assertEqual(self.a['static']['MOND_residual'],0)

    def test_local_wave_not_old_elliptic_dispersion(self):
        a=self.a['principal']; m,q,alpha=a['symbols']
        self.assertEqual(s.factor(a['speed_squared']-2*(1-alpha)/3),0)
        self.assertEqual(a['kinetic'],3*m/2)
        self.assertNotEqual(s.factor(a['speed_squared']-2*(1-alpha)/(3*(2-alpha))),0)

    def test_actual_constraints_preserved_in_exceptional_sectors(self):
        for dc in self.a['dirac'].values():
            self.assertTrue(dc['preservation_closed'])
            self.assertEqual(s.Matrix(dc['poisson_matrix']).rank(),dc['bracket_rank'])

    def test_physical_vacuum_fields_have_local_time_evolution(self):
        a=self.a['vacuum']
        self.assertTrue(all(x==0 for x in a['constraint_residuals']))
        self.assertEqual(a['fourth_derivative_denominator'],1)
        self.assertEqual(a['curvature_identity_residual'],0)
        self.assertIn('first_order_residuals',a)
        self.assertTrue(all(x==0 for x in a['first_order_residuals']))

    def test_conserved_source_is_not_assigned_GR_response(self):
        a=self.a['response']; m,q,alpha,w,rho,S=a['symbols']
        self.assertEqual(a['residuals'],[0,0,0,0])
        self.assertEqual(s.factor(a['high_frequency_R00']-((1-alpha)*rho-S)/(2*m)),0)
        self.assertNotEqual(s.factor(a['high_frequency_R00']-(rho-S)/(2*m)),0)

    def test_same_expanding_homogeneous_action(self):
        a=self.a['homogeneous']
        self.assertTrue(all(x==0 for x in a['preservation_residuals']))
        self.assertTrue(all(x==0 for x in a['constraint_residuals']))

    def test_positive_null_beams_supply_conserved_matter_witness(self):
        self.assertIn('null_beams',self.a)
        a=self.a['null_beams']
        self.assertTrue(all(x==0 for x in a['ward_residuals']))
        self.assertTrue(all(x==0 for x in a['initial_source_differences']))
        self.assertEqual(a['response_equation_residual'],0)
        self.assertEqual(a['tail_symbol_residual'],0)
        self.assertTrue(a['exterior_tail'].is_positive)
        self.assertIn('particle_variation',a)
        self.assertTrue(all(x==0 for x in a['particle_variation']['null_constraints']))


if __name__=='__main__':
    unittest.main()
