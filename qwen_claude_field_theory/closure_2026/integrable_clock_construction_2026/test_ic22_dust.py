"""Varied pressureless matter: no radiation-limit shortcut."""
import importlib.util
from pathlib import Path
import unittest
import mpmath as mp


class DustTests(unittest.TestCase):
    def model(self):
        path=Path(__file__).with_name('ic22_dust.py')
        self.assertTrue(path.exists(),'Dust constrained action is missing')
        spec=importlib.util.spec_from_file_location('ic22',path)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        mp.mp.dps=60
        return m

    def test_dust_action_and_frequency_polynomial_are_varied(self):
        m=self.model();self.assertTrue(all(x==0 for x in m.identities().values()))

    def test_dust_background_satisfies_actual_constraints(self):
        m=self.model();b=m.background('1e-6')
        self.assertLess(max(map(abs,b['constraints'])),mp.mpf('1e-45'))
        self.assertGreater(b['H_physical'],0)

    def test_finite_momentum_matrix_is_not_set_to_radiation_zero_sound_speed(self):
        m=self.model();b=m.background('1e-6');q=m.quadratic(b,'1e6')
        self.assertGreater(mp.det(q['K']),0)
        self.assertGreater(min(mp.eigsy(q['A'],eigvals_only=True)),0)
        self.assertNotEqual(q['B'][0,1]-q['B'][1,0],0)

    def test_full_frequency_problem_retains_four_roots(self):
        m=self.model();r=m.frequencies(m.background('1e-6'),'1e6')
        self.assertEqual(len(r['growth_exponents']),4)
        self.assertLess(r['maximum_eigen_residual'],mp.mpf('1e-40'))

    def test_principal_frequency_polynomial_matches_fast_root(self):
        m=self.model();b=m.background('1e-6');r=m.frequencies(b,'1e10')
        principal=m.principal_symbol(b)
        self.assertTrue(0<principal['nonzero_speed_squared']<1)
        self.assertLess(abs(r['fastest_oscillatory_speed_squared']-principal['nonzero_speed_squared']),mp.mpf('1e-7'))

    def test_dust_norm_and_density_current_follow_the_hamiltonian(self):
        m=self.model()
        self.assertIn('dust_norm_equation',m.identities())
        self.assertIn('dust_density_current',m.identities())
        self.assertEqual(m.identities()['dust_norm_equation'],0)
        self.assertEqual(m.identities()['dust_density_current'],0)

    def test_exact_dust_zero_mode_is_not_mistaken_for_strong_hyperbolicity(self):
        m=self.model();r=m.principal_symbol(m.background('1e-6'))
        self.assertIn('zero_eigenspace_dimension',r)
        self.assertLess(r['zero_eigenspace_dimension'],r['zero_frequency_multiplicity'])

    def test_positive_pressure_completion_comes_from_the_same_gravity_action(self):
        m=self.model();b=m.background('1e-6',pressure='.001')
        r=m.pressure_principal(b)
        self.assertTrue(all(0<x<1 for x in r['speeds_squared']))
        self.assertGreater(r['gradient_determinant'],0)
        finite=m.frequencies(b,'1e10')
        observed=sorted(x['imag']**2/(mp.exp(2*b['S'])*mp.mpf('1e10')) for x in finite['growth_exponents'] if x['imag']>0)
        self.assertEqual(len(observed),2)
        self.assertLess(max(abs(x-y) for x,y in zip(observed,sorted(r['speeds_squared']))),mp.mpf('1e-7'))

    def test_full_dust_auxiliary_matrix_includes_density_multiplier(self):
        m=self.model();b=m.background('1e-6')
        self.assertTrue(hasattr(m,'auxiliary_matrix'))
        for k in (0,1,10000):self.assertEqual(m.auxiliary_matrix(b,k)['rank'],6)


if __name__=='__main__':unittest.main()
