"""Finite signed-source control; no assertion about all higher wall jets."""
import importlib.util
import contextlib
import io
import unittest

import numpy as np

AVAILABLE = importlib.util.find_spec('metric_collar_control') is not None


class ImplementationTest(unittest.TestCase):
    def test_control_implementation_exists(self):
        self.assertTrue(AVAILABLE, 'Full-background signed collar control is missing')


@unittest.skipUnless(AVAILABLE, 'not implemented')
class CollarControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_collar_control as model
        cls.model = model
        cls.result = model.audit()

    def test_basis_avoids_observer_and_wall_collars(self):
        for x in [-1., -.9, -.81, -.1, 0., .1, .81, .9, 1.]:
            self.assertTrue(np.all(self.model.basis_values(x) == 0))
        self.assertEqual(len(self.model.basis_values(.3)), 10)

    def test_nullspace_does_not_depend_on_a_singular_value_cutoff(self):
        for row in self.result['responses']:
            self.assertEqual(row['control_shape'], [5, 10])
            self.assertEqual(row['conservative_nullity'], 5)
            self.assertEqual(len(row['control_singular_values']), 5)
            self.assertLess(row['selected_control_relative_residual'], 1e-10)

    def test_combined_source_is_signed_and_observer_signal_is_resolved(self):
        for row in self.result['responses']:
            self.assertLess(row['source_minimum'], 0)
            self.assertGreater(row['source_maximum'], 0)
            self.assertGreater(row['observer_to_peak_ratio'], 1e-3)
            self.assertGreater(row['observer_resolution_ratio'], 100)

    def test_independently_reintegrated_constraints_and_collars(self):
        for row in self.result['responses']:
            self.assertEqual(len(row['independently_reintegrated_control']), 5)
            self.assertLess(row['reintegrated_control_scaled_residual'], 1e-5)
            self.assertLess(row['boundary_residual'], 1e-9)
            self.assertLess(row['relative_mean_residual'], 1e-6)
            self.assertLess(row['relative_collar_tail'], 1e-5)
            self.assertLess(row['relative_refinement_difference'], 1e-5)
            self.assertLess(row['finite_difference_ODE_residual'], 1e-5)
            self.assertLess(row['wall_fifth_relative_residual'], 1e-5)

    def test_report_numbers_each_finite_gate_and_preserves_scope(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.model.print_report(self.result)
        report = output.getvalue()
        for number in [1, 2]:
            self.assertIn(f'{number}. [ok]', report)
        self.assertIn(self.result['scope'], report)
        for row in self.result['responses']:
            for warning in row['conditioning_warnings']:
                self.assertIn(warning, report)


if __name__ == '__main__':
    unittest.main()
