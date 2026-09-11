"""Independent fixtures catch sign, physical/comoving length, and pole errors."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class FilterTests(unittest.TestCase):
    def implementation(self):
        path = Path(__file__).with_name('derive_length.py')
        if not path.exists():
            self.fail('action constraint filter has not been implemented')
        spec = importlib.util.spec_from_file_location('length', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_physical_length_and_shift(self):
        k = s.Symbol('k', real=True)
        result = self.implementation().extract_filter(-2-3*k*k, 5+7*k*k, k, s.Integer(2))
        self.assertEqual(result['ell2'], 6)
        self.assertEqual(result['shift'], -s.Rational(7,3))  # E2/D2 = 7/(-3).
        self.assertEqual(result['remaining_u'], s.Rational(1,3))

    def test_reject_non_affine_constraint(self):
        k = s.Symbol('k', real=True)
        with self.assertRaises(ValueError):
            self.implementation().extract_filter(-2-k**4, k*k, k, s.Integer(1))

    def test_reject_zero_mass_or_gradient(self):
        k = s.Symbol('k', real=True)
        for D in (-k*k, s.Integer(-2)):
            with self.assertRaises(ValueError):
                self.implementation().extract_filter(D, k*k, k, s.Integer(1))


if __name__ == '__main__':
    unittest.main()
