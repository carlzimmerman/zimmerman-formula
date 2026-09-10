"""Regression targets: a frozen coupling, omitted mean variation, or assigned
constraint ranks must not masquerade as a completed action calculation.
"""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class TraceVarianceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name('trace_variance.py')
        cls.module_path = path
        if path.exists():
            spec = importlib.util.spec_from_file_location('trace_variance', path)
            cls.mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.mod)

    def result(self):
        self.assertTrue(self.module_path.exists(), 'action derivation not implemented')
        return self.mod.derive()

    def test_derivation_identities(self):
        r = self.result()
        self.assertTrue(all(r['checks'].values()), r['checks'])

    def test_running_coupling_is_not_its_hessian(self):
        r = self.result()['acceleration']
        self.assertLess(float(r['parallel_at_y2']), 0)
        self.assertGreater(float(r['frozen_at_y2']), 0)
        self.assertNotEqual(r['parallel_at_y2'], r['frozen_at_y2'])

    def test_healthy_kinetic_branch_has_negative_radial_speed(self):
        r = self.result()['scalar']
        for row in r['witnesses']:
            self.assertGreater(float(row['kinetic']), 0)
            self.assertLess(float(row['radial_speed_squared']), 0)

    def test_exceptional_sectors_recomputed(self):
        r = self.result()['dirac']
        self.assertEqual(r['generic']['scalar_mode_count'], 1)
        self.assertEqual(r['trace_degenerate']['scalar_mode_count'], 0)
        self.assertEqual(r['zero_field_trace_degenerate']['bracket_rank'], 2)
        for row in r.values():
            self.assertTrue(row['preservation_closed'])

    def test_mean_subtraction_keeps_homogeneous_kinetic(self):
        r = self.result()['variance']
        self.assertEqual(r['homogeneous_variance'], 0)
        self.assertEqual(r['legendre_identity_residual'], 0)
        self.assertEqual(r['trace_velocity_hessian_rank'], 1)

    def test_unstable_direction_exists_on_constrained_vacuum_seed(self):
        r = self.result()
        self.assertIn('vacuum_seed', r, 'actual background gate missing')
        v = r['vacuum_seed']
        self.assertTrue(all(x == 0 for x in v['variation_residuals']))
        self.assertGreater(float(v['seed_discriminant']), 0)
        self.assertLess(float(v['seed_alpha_radial']), 0)
        self.assertNotEqual(float(v['seed_ode_determinant']), 0)


if __name__ == '__main__':
    unittest.main()
