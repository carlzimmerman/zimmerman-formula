"""Independent anisotropic metric variation must survive the isotropic gauge."""
import importlib.util
import unittest
import sympy as s


class FullMetricEvolutionTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic33_full_metric_evolution'))
        import ic33_full_metric_evolution
        return ic33_full_metric_evolution

    def test_full_action_reduces_to_existing_action(self):
        out=self.module().identities()
        self.assertEqual(out['isotropic_action'],0)
        self.assertEqual(out['trace_evolution'],0)
        self.assertEqual(out['trace_formula'],0)

    def test_tracefree_equation_retains_curvature_and_matter_stress(self):
        out=self.module().identities()
        self.assertEqual(out['tracefree_evolution'],0)
        self.assertEqual(out['matter_trace'],0)
        self.assertEqual(out['matter_tracefree'],0)

    def test_curvature_matches_independent_christoffel_calculation(self):
        m=self.module()
        self.assertTrue(hasattr(m,'curvature_check'))
        self.assertEqual(m.curvature_check(),0)

    def test_repaired_tangent_obeys_full_metric_equation(self):
        m=self.module()
        self.assertTrue(hasattr(m,'full_tangent'))
        out=m.full_tangent(amplitude=1.,nodes=3201)
        self.assertTrue(out['solved'])
        self.assertLess(out['full_shear_euler_defect'],1e-7)
        self.assertLess(out['max_preservation_residual'],1e-5)
        for ratios in out['kick_ratios']:
            for name,value in ratios.items():
                self.assertGreater(value,3.2,name)


if __name__=='__main__':
    unittest.main()
