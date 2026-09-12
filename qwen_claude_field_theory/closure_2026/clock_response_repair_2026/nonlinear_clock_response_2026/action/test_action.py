"""Regression targets for the full ADM polynomial generator.

Removing a cubic ADM term, a matter velocity, or using qbar in place of Q
must fail these checks. No benchmark assumes the nonlinear constraints solved.
"""
from pathlib import Path
import importlib.util
import unittest

HERE = Path(__file__).resolve().parent


class ActionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((HERE/'adm_action.py').exists(),
                        'The unrestricted higher-order ADM generator is missing')
        spec = importlib.util.spec_from_file_location('adm_action', HERE/'adm_action.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_series_matches_exact_differentiation(self):
        self.assertTrue(self.module.series_check())

    def test_quadratic_action_matches_original_bridge(self):
        self.assertTrue(all(self.module.quadratic_regression().values()))

    def test_full_braiding_matches_covariant_divergence_with_shift(self):
        self.assertTrue(hasattr(self.module, 'covariant_braiding_check'),
                        'Full shifted covariant/ADM boundary check is missing')
        self.assertTrue(self.module.covariant_braiding_check())

    def test_linear_constraint_seed_generates_second_order_sources(self):
        self.assertTrue(hasattr(self.module, 'linear_seed_sources'),
                        'Constraint-compatible linear seed is missing')
        result = self.module.linear_seed_sources()
        self.assertLess(result['linear_lapse_shift_max'], 1e-11)
        self.assertLess(result['clock_linear_residual'], 1e-11)
        self.assertGreater(abs(result['sources']['lapse']['2']['constant']), 1e-5)
        self.assertGreater(abs(result['sources']['lapse']['2']['cos2']), 1e-5)
        self.assertGreater(abs(result['sources']['shift']['2']['sin2']), 1e-5)
        self.assertLess(result['source_projection_max_error'], 1e-10)

    def test_constraints_match_independent_variation(self):
        result = self.module.numerical_checks()
        self.assertLess(result['independent_variation_max_error'], 2e-10)
        self.assertLess(result['source2_relative_error'], 3e-4)
        self.assertLess(result['source3_relative_error'], 3e-4)
        self.assertLess(result['action4_relative_error'], 3e-4)
        self.assertGreater(result['physical_Q_qbar_separation'], 1e-4)
        self.assertEqual(result['gamma'], 1e-6)
        self.assertEqual(result['forbidden_harmonics_max'], 0)


if __name__ == '__main__':
    unittest.main()
