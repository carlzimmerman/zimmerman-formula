"""Same-action radiation, constraint reduction, and coupled principal modes."""
import importlib.util
from pathlib import Path
import unittest
import mpmath as mp


class RadiationTests(unittest.TestCase):
    def model(self):
        path=Path(__file__).with_name('ic21_radiation.py')
        self.assertTrue(path.exists(),'Explicit radiation reduction missing')
        spec=importlib.util.spec_from_file_location('ic21',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        mp.mp.dps=60
        return module

    def test_exact_matter_legendre_and_quadratic_identities(self):
        m=self.model();self.assertTrue(all(x==0 for x in m.identities().values()))

    def test_background_uses_actual_radiation_lapse_source(self):
        m=self.model();b=m.background('1e-6')
        self.assertLess(max(map(abs,b['constraints'])),mp.mpf('1e-45'))
        self.assertGreater(b['H_physical'],0)

    def test_coupled_modes_are_computed_from_two_field_matrix(self):
        m=self.model();b=m.background('1e-6');r=m.principal(b,'1e10')
        self.assertEqual(len(r['speeds_squared']),2)
        self.assertGreater(min(r['kinetic_eigenvalues']),0)
        self.assertTrue(all(0<x<1 for x in r['speeds_squared']))

    def test_dilute_radiation_limit_recovers_both_independent_sectors(self):
        m=self.model();r=m.principal(m.background('1e-12'),'1e12')
        observed=sorted(r['speeds_squared'])
        self.assertLess(abs(observed[0]-mp.mpf('.2')),mp.mpf('1e-6'))
        self.assertLess(abs(observed[1]-mp.mpf(1)/3),mp.mpf('1e-6'))

    def test_principal_limit_is_derived_and_matches_full_time_dependent_reduction(self):
        m=self.model();b=m.background('1e-4')
        self.assertTrue(hasattr(m,'principal_limit'))
        exact=m.principal_limit(b);finite=m.principal(b,'1e12')
        self.assertLess(max(abs(x-y) for x,y in zip(sorted(exact['speeds_squared']),sorted(finite['speeds_squared']))),mp.mpf('1e-8'))
        self.assertGreater(exact['gradient_determinant'],0)
        self.assertGreater(exact['lightcone_margin_determinant'],0)

    def test_matter_auxiliary_brackets_are_computed_in_both_sectors(self):
        m=self.model();b=m.background('1e-6')
        self.assertTrue(hasattr(m,'constraint_matrix'))
        for k in (0,1,10000):
            row=m.constraint_matrix(b,k)
            self.assertEqual(row['rank'],4)
            self.assertGreater(row['determinant'],0)


if __name__=='__main__':unittest.main()
