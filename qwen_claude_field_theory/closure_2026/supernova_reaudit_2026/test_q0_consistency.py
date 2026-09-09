"""Consistency of the proposed density tie with explicit GR background assumptions."""
import unittest
import sympy as sp
import q0_consistency as model


class BackgroundConsistencyTests(unittest.TestCase):
    def test_raychaudhuri_and_friedmann_elimination(self):
        d = model.derive()
        self.assertEqual(sp.simplify(d['q_direct'] - d['q_eliminated']), 0)
        self.assertEqual(sp.simplify(d['q_eliminated'].subs(d['a'], 0)), sp.Rational(1, 2))

    def test_deceleration_boundary_is_derived(self):
        d = model.derive()
        self.assertEqual(sp.simplify(d['q_eliminated'].subs(d['a'], d['a_critical'])), 0)
        self.assertEqual(sp.simplify(d['q_eliminated'].subs(d['a'], d['a_critical']/2)), sp.Rational(3, 8))

    def test_non_lambda_fluid_is_not_assigned_the_lambda_answer(self):
        d = model.derive()
        self.assertEqual(sp.simplify(d['q_general'].subs(d['w'], -1) - d['q_eliminated']), 0)
        self.assertEqual(sp.simplify(d['q_general'].subs(d['w'], 0)), sp.Rational(1, 2))


if __name__ == '__main__':
    unittest.main()
