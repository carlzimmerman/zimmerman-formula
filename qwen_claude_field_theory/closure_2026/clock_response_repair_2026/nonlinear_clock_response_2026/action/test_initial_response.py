"""Nonlinear initial-constraint response regression, not evolution tests."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent


class InitialResponseTests(unittest.TestCase):
    def test_generated_mean_and_second_harmonic_cancel_constraints(self):
        path = HERE/'initial_response.py'
        self.assertTrue(path.exists(), 'The nonlinear initial response solve is missing')
        spec = importlib.util.spec_from_file_location('initial_response',path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        result = module.run()
        self.assertLess(result['linear_constraint_max'], 1e-11)
        self.assertLess(result['quadratic_constraint_max_after_response'], 1e-10)
        self.assertGreater(result['quadratic_constraint_max_before_response'], 1e-3)
        self.assertGreater(abs(result['response']['mean_deltaQ2']), 1e-4)
        self.assertLess(result['exact_even_residual_order_min_error'], .15)
        self.assertLess(result['exact_full_residual_order_min_error'], .15)


if __name__ == '__main__':
    unittest.main()
