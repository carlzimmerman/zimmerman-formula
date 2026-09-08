"""Prevent a favorable result from a different action being inherited."""
import importlib.util
import unittest
import sympy as s


class ResearchGateTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('research_gate'))
        import research_gate
        return research_gate

    def test_all_three_scalar_actions_are_identical_after_dictionary(self):
        d = self.module().same_action_checks()
        self.assertEqual(d['endpoint_residual'], 0)
        self.assertEqual(d['causal_zero_source_residual'], 0)
        self.assertEqual(d['selected_causal_kinetic_residual'], 0)

    def test_curvature_selection_does_not_count_as_full_closure(self):
        d = self.module().run()
        self.assertTrue(d['checks_passed'])
        self.assertEqual(d['selected_b'], '3/16')
        self.assertEqual(d['selected_kinetic'], 9)
        self.assertEqual(d['causal_response']['adaptive_response']['causal_response_gate'], 'FAIL')
        self.assertFalse(d['closure_passed'])
        self.assertEqual(d['full_theory_status'], 'OPEN')
        self.assertGreater(len(d['missing_certificates']), 0)


if __name__ == '__main__':
    unittest.main()
