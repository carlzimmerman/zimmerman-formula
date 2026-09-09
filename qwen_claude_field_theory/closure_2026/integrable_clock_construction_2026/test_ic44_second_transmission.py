"""Catch missing time Euler terms, shift terms, and singular-sector erasure."""
import importlib.util
import unittest
import sympy as s


class SecondTransmissionTests(unittest.TestCase):
    def model(self):
        self.assertIsNotNone(importlib.util.find_spec('ic44_second_transmission'),
                             'Second-derivative action transmission is absent')
        import ic44_second_transmission as module
        return module.derive()

    def test_constructed_jumps_satisfy_every_varied_transmission_equation(self):
        d=self.model()
        self.assertEqual(d['residual'], s.zeros(6,1))
        self.assertNotEqual(d['determinant'], 0)

    def test_finite_clock_reaction_is_carried_by_a_trace_gradient_jump(self):
        d=self.model()
        self.assertEqual(s.simplify(d['jumps']['q_r']+
            d['reaction']/(2*(d['speed']+d['beta']))), 0)
        self.assertEqual(d['zero_reaction_jumps'], s.zeros(6,1))

    def test_exceptional_sectors_are_not_covered_by_generic_inverse(self):
        d=self.model()
        self.assertEqual(s.simplify(d['determinant'].subs(d['speed'],-d['beta'])), 0)
        self.assertEqual(s.simplify(d['determinant'].subs(d['w'],-d['S']/2)), 0)

    def test_actual_activation_distinguishes_allowed_and_wrong_side_jets(self):
        d=self.model()
        self.assertIn('activation_gradient_off', d)
        common={d['q_boundary']:-1,d['qprime_on']:-1,d['speed']:1,d['beta']:0}
        self.assertEqual(d['activation_gradient_off'].subs(common).subs(d['reaction'],0), 1)
        self.assertEqual(d['activation_gradient_off'].subs(common).subs(d['reaction'],-3), -s.Rational(1,2))


if __name__=='__main__':unittest.main()
