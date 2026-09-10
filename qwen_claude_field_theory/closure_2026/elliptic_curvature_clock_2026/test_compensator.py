"""Action checks must detect lapse-symbol freezing and dropped zero modes."""
import importlib.util
from pathlib import Path
import unittest


class CompensatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=Path(__file__).with_name('compensator.py')
        if cls.path.exists():
            spec=importlib.util.spec_from_file_location('compensator',cls.path)
            cls.mod=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.mod)

    def result(self):
        self.assertTrue(self.path.exists(),'new action not implemented')
        return self.mod.derive()

    def test_action_identities(self):
        r=self.result()
        self.assertTrue(all(r['checks'].values()),r['checks'])

    def test_scalar_positive_kinetic_and_radial_gradient(self):
        r=self.result()['scalar']
        self.assertGreater(float(r['kinetic_m1']),0)
        self.assertGreater(float(r['radial_cs2_y2']),0)
        self.assertLess(float(r['radial_cs2_y2']),1)

    def test_no_auxiliary_pair_added_in_principal_dirac(self):
        r=self.result()['dirac']
        self.assertEqual(r['generic']['scalar_mode_count'],1)
        self.assertEqual(r['zero_field']['scalar_mode_count'],1)
        self.assertEqual(r['generic']['bracket_rank'],4)
        self.assertEqual(r['zero_field']['bracket_rank'],4)

    def test_zero_mode_does_not_force_static_universe(self):
        r=self.result()['homogeneous']
        self.assertEqual(r['constraint_residuals'],[0,0,0])
        self.assertEqual(r['bracket_rank'],4)
        self.assertEqual(r['matter_inclusive_pairs'],1)

    def test_compact_initial_data_curvature_response(self):
        r=self.result()
        self.assertIn('causal_initial_data',r,'curvature propagation gate missing')
        c=r['causal_initial_data']
        self.assertEqual(c['initial_constraint_residuals'],[0,0])
        self.assertEqual(c['vacuum_R00_identity_residual'],0)
        self.assertEqual(c['isotropic_remainder'],0)
        self.assertLess(float(c['tail_at_y2_R1']),0)


if __name__=='__main__':
    unittest.main()
