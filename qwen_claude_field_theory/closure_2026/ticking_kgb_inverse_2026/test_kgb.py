"""Action-level and independent limiting controls for the ticking KGB route."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class KGBTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).with_name('kgb_inverse.py');cls.present=path.exists()
        if cls.present:
            spec=importlib.util.spec_from_file_location('kgb_inverse',path)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            cls.a=module.derive()

    def setUp(self):
        self.assertTrue(self.present,'new ticking-clock action calculation missing')

    def test_radial_metric_variation_and_current(self):
        self.assertTrue(all(x==0 for x in self.a['variation']['identity_residuals']))

    def test_static_scalar_limit_does_not_cover_ticking_scalar(self):
        a=self.a['variation']
        self.assertEqual(a['static_clock_limit'],0)
        self.assertNotEqual(a['ticking_rho_plus_pt'],0)

    def test_exact_halo_einstein_equations(self):
        self.assertTrue(all(x==0 for x in self.a['halo']['Einstein_residuals']))
        self.assertEqual(self.a['halo']['current_residual'],0)

    def test_derived_halo_principal_metric(self):
        a=self.a['halo'];w,m=a['symbols']
        self.assertEqual(s.factor(a['radial_speed2']-3*w/(w+2)),0)
        self.assertEqual(s.factor(a['angular_speed2']-3*w*w/(w+2)),0)
        self.assertTrue(a['kinetic'].is_positive)

    def test_same_action_cosmology(self):
        a=self.a['cosmology'];n=s.Symbol('n',positive=True)
        self.assertEqual(s.factor(a['equation_of_state']-1/(4*n+1)),0)
        self.assertEqual(s.factor(a['speed2']-(16*n+7)/(3*(4*n+1)**2)),0)
        self.assertTrue(all(x==0 for x in a['background_residuals']))

    def test_one_power_is_not_a_mass_dependent_btfr(self):
        a=self.a['halo'];w,m=a['symbols']
        self.assertEqual(s.factor(a['power_index']-(1-w)/(2*w)),0)
        self.assertEqual(a['fixed_action_velocity_mass_derivative'],0)

    def test_preferred_kernel_inverse_has_small_field_residuals(self):
        path=Path(__file__).with_name('mond_profile.py')
        self.assertTrue(path.exists(),'full exponential-profile inverse not implemented')
        spec=importlib.util.spec_from_file_location('mond_profile',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        a=module.sample('0.000001','1')
        self.assertLess(float(a['max_relative_field_residual']),1e-35)
        self.assertGreater(float(a['rho']),0)
        self.assertLess(float(a['X_log_derivative']),0)

    def test_canonical_scalar_principal_benchmark(self):
        path=Path(__file__).with_name('kgb_inverse.py')
        spec=importlib.util.spec_from_file_location('kgb_benchmark',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        a=module.principal_template()
        M=a['M'].subs({a['G1']:0,a['G2']:0,a['P1']:1,a['P2']:0})
        self.assertEqual(M,s.diag(1,-1,-1,-1))

    def test_general_inverse_current_is_radial_ward_identity(self):
        self.assertEqual(self.a['general_inverse']['current_ward_residual'],0)
        self.assertTrue(all(x==0 for x in self.a['general_inverse']['stress_residuals']))


if __name__=='__main__':
    unittest.main()
