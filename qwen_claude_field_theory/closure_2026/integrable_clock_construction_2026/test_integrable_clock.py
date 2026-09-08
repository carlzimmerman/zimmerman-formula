"""Tests of derived identities, not certification of the gravity target."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent


class ConstructionTests(unittest.TestCase):
    def model(self):
        path = HERE / 'integrable_clock.py'
        self.assertTrue(path.exists(), 'The action derivation has not been implemented')
        spec = importlib.util.spec_from_file_location('integrable_clock', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_integrable_primary_algebra_from_velocities(self):
        d = self.model().kinetic()
        self.assertEqual(d['primary_residuals'], [0, 0])
        self.assertEqual(d['bracket'], 0)
        self.assertNotEqual(d['missing_term_bracket'], 0)
        self.assertEqual(d['rank'] + len(d['hessian'].nullspace()), 8)
        self.assertEqual(d['null_residuals'], [[0]*8, [0]*8])

    def test_constitutive_equation_and_limits(self):
        d = self.model().constitutive()
        self.assertEqual(d['legendre_residual'], 0)
        self.assertEqual(d['primitive_residual'], 0)
        self.assertEqual(d['deep_limit'], 1)
        self.assertEqual(d['newtonian_limit'], 1)
        self.assertEqual(d['boundary_auxiliary_equation'], 0)

    def test_static_variation_is_independent(self):
        d = self.model().static_sector()
        self.assertEqual(d['poisson_residual'], 0)
        self.assertEqual(d['slip_residual'], 0)
        self.assertNotEqual(d['clock_lapse_source'], 0)
        self.assertNotEqual(d['clock_spatial_source'], 0)

    def test_homogeneous_legendre_and_primary_preservation(self):
        d = self.model().homogeneous()
        self.assertEqual(d['legendre_residual'], 0)
        self.assertEqual(d['preservation_residuals'], [0]*4)
        self.assertEqual(d['omega'] + d['omega'].T, self.model().s.zeros(4))

    def test_regular_expanding_witness_is_computed(self):
        d = self.model().witness()
        self.assertLess(max(abs(x) for x in d['constraint_residuals']), 1e-10)
        self.assertGreater(d['physical_H'], 0)
        self.assertGreater(min(d['singular_values']), 1e-7)
        self.assertEqual(d['count'], 1)  # independent homogeneous Dirac calculation
        self.assertFalse(d['full_theory_closed'])

    def test_tensor_coefficients_come_from_curvature(self):
        d = self.model().tensor_sector()
        self.assertEqual(d['ricci_residual'], 0)
        self.assertEqual(d['physical_speed_squared'], 1)
        self.assertTrue(d['kinetic_hessian'].is_positive)

    def test_exact_expanding_family_and_reduced_kinetic(self):
        module=self.model()
        self.assertTrue(hasattr(module,'homogeneous_family'), 'Missing all-parameter branch derivation')
        d=module.homogeneous_family()
        self.assertEqual(d['constraint_residuals'], [0]*4)
        self.assertEqual(d['flow_residuals'], [0]*4)
        self.assertEqual(d['determinant_residual'], 0)
        self.assertEqual(d['reduced_hessian_residual'], 0)

    def test_spatial_transform_retains_mixed_gradient(self):
        module=self.model()
        self.assertTrue(hasattr(module,'spatial_transform'), 'Missing transformed spatial action')
        d=module.spatial_transform()
        self.assertEqual(d['identity_residual'], 0)
        self.assertNotEqual(d['mixed_coefficient'], 0)

    def test_minimal_matter_ward_identity(self):
        module=self.model()
        self.assertTrue(hasattr(module,'matter_ward'), 'Missing stress-tensor divergence calculation')
        self.assertEqual(module.matter_ward()['residuals'], [0]*4)


if __name__ == '__main__':
    unittest.main()
