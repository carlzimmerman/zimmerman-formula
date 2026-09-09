import importlib.util
import unittest


class FourthPreservationTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic42_fourth_preservation'))
        return __import__('ic42_fourth_preservation')

    def test_quartic_fluid_term_is_derived_from_fixed_momentum_legendre_transform(self):
        self.assertEqual(self.module().identities()['fluid_Hkk'],0)
        self.assertEqual(self.module().identities()['fluid_clock_trace'],0)

    def test_fourth_pin_equation_keeps_both_lower_multiplier_derivatives(self):
        self.assertEqual(self.module().identities()['fourth_pin'],0)

    def test_quadratic_moving_face_requirement(self):
        self.assertEqual(self.module().identities()['quadratic_face'],0)


if __name__=='__main__':unittest.main()
