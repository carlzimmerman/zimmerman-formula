"""Regression controls: omission of constraint preservation must fail these."""
import importlib.util
from pathlib import Path
import unittest
import sympy as S


class PrincipalTests(unittest.TestCase):
    def test_derived_chain_closes_and_preserves(self):
        path = Path(__file__).with_name('principal_gate.py')
        self.assertTrue(path.exists(), 'the constraint derivation has not been implemented')
        spec = importlib.util.spec_from_file_location('principal_gate', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for case in module.constraint_cases().values():
            self.assertTrue(all(S.simplify(x) == 0 for x in case['preservation']))
            matrix = case['bracket_matrix']
            self.assertEqual(matrix + matrix.T, S.zeros(matrix.rows))
            self.assertEqual(case['first_class'] + case['second_class'], len(case['constraints']))
        # A false MOND=linear-response identity must be rejected by the actual law.
        self.assertGreater(abs(module.mond_residual(0.01, 0.01, 1.0)), 0.009)


if __name__ == '__main__':
    unittest.main()
