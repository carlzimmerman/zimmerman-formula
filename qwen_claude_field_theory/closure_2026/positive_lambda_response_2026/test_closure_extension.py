"""Cross-check the same-action extension without turning arithmetic into closure."""
import contextlib
import importlib
import io
import unittest
from unittest.mock import patch


class ExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = importlib.import_module('closure_extension')
        cls.result = cls.module.run()

    def test_all_six_computations_ran(self):
        self.assertEqual(set(self.result['evidence']), {
            'positive_lambda_external', 'physical_cauchy', 'homogeneous_dirac',
            'auxiliary_localization', 'infrared_domain', 'general_family'})
        self.assertTrue(self.result['checks_passed'])
        for result in self.result['evidence'].values():
            self.assertTrue(result['checks_passed'])

    def test_healthy_cauchy_witness_is_not_an_external_realization(self):
        physical = self.result['evidence']['physical_cauchy']
        self.assertEqual(physical['healthy_linear_cauchy_gate'], 'FAIL')
        self.assertFalse(physical['external_signed_probe_identified_with_canonical_delta_T'])
        self.assertFalse(physical['nonlinear_constraint_completion_claimed'])

    def test_general_family_does_not_borrow_the_K9_weyl_formula(self):
        family = self.result['evidence']['general_family']
        self.assertEqual(family['healthy_linear_cauchy_gate'], 'FAIL')
        self.assertFalse(family['infinite_K_or_b_zero_claimed'])
        self.assertFalse(family['nonlinear_initial_data_lift_claimed'])

    def test_partial_constraint_counts_never_promote_to_full_count(self):
        self.assertTrue(self.result['evidence']['auxiliary_localization']['nonzero_mode_auxiliary_closure'])
        self.assertFalse(self.result['evidence']['homogeneous_dirac']['full_field_count_proved'])
        self.assertIsNone(self.result['full_theory_gates']['full_nonlinear_gravitational_count'])
        self.assertFalse(self.result['full_closure_proved'])

    def test_default_and_acceptance_have_different_exit_status(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.module.main([]), 0)
            self.assertEqual(self.module.main(['--require-closure']), 2)

    def test_computation_failure_is_exit_one(self):
        failed = dict(self.result, checks_passed=False)
        with patch.object(self.module, 'run', return_value=failed), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.module.main([]), 1)
            self.assertEqual(self.module.main(['--require-closure']), 1)

    def test_corroboration_is_checked_but_not_called_proof(self):
        self.assertTrue(self.result['numerical_corroboration_consistent'])
        external = self.result['evidence']['positive_lambda_external']
        self.assertTrue(external['numerics_are_not_the_inequality_proof'])
        for row in external['numerical_corroboration']:
            self.assertGreater(row['F'], row['rigorous_F_lower_bound'])
            self.assertLess(row['relative_refinement_change'], 1e-8)


if __name__ == '__main__':
    unittest.main()
