"""Independent controls: fail if Maxwell signs or metric-shift signs change."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s


class ConeTests(unittest.TestCase):
    def test_action_derived_cones_and_shift_controls(self):
        path = Path(__file__).with_name('derive_cone.py')
        self.assertTrue(path.exists(), 'action-derived cone implementation missing')
        spec = importlib.util.spec_from_file_location('derive_cone', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        C, lapse2 = s.symbols('C lapse2', positive=True)
        kinetic, gradient = mod.maxwell_coefficients(C, lapse2)
        self.assertEqual(s.simplify(gradient/kinetic-lapse2/C), 0)
        self.assertEqual(kinetic.subs({C: 3, lapse2: 3}), 1)
        self.assertEqual(gradient.subs({C: 3, lapse2: 3}), 1)
        self.assertEqual(s.simplify((gradient/kinetic).subs({C: 2, lapse2: 1})), s.Rational(1, 2))
        self.assertEqual(mod.potential_shifts(-1, -2), (1, 1))
        self.assertEqual(mod.potential_shifts(1, 0), (1, -1))
        self.assertEqual(mod.potential_shifts(0, 0), (0, 0))


if __name__ == '__main__':
    unittest.main()
