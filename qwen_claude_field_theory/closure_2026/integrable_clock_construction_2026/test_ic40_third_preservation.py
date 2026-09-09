import importlib.util
import unittest
import sympy as s


class ThirdPreservationTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic40_third_preservation'))
        return __import__('ic40_third_preservation')

    def test_moving_interface_term_is_not_omitted(self):
        m=self.module();out=m.identities()
        self.assertEqual(out['third_pin_derivative'],0)
        self.assertEqual(out['moving_cubic_term'],0)

    def test_fluid_gradient_legendre_coefficient_is_derived(self):
        out=self.module().identities()
        self.assertEqual(out['fluid_quadratic_gradient'],0)
        self.assertEqual(out['fluid_pressure_gradient'],0)

    def test_independent_time_engine_reproduces_lower_gate(self):
        m=self.module();self.assertTrue(callable(getattr(m,'field_result',None)))
        out=m.field_result(dps=40,order=2)
        self.assertLess(float(out['second_gate_relative_error']),1e-18)
        self.assertLess(float(out['first_constraint_error']),1e-18)


if __name__=='__main__':unittest.main()
