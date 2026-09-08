"""Independent controls for algebraic elimination and IC6 strong-space bridge."""
import importlib
import importlib.util
import unittest

import numpy as np
import sympy as sp


class StrongAuxiliaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.available = importlib.util.find_spec("ic6_strong_auxiliary") is not None
        cls.module = importlib.import_module("ic6_strong_auxiliary") if cls.available else None

    def result(self):
        self.assertTrue(self.available, "IC6 strong auxiliary derivation is not implemented")
        return self.module.derive()

    def test_elimination_retains_cross_gradient_response(self):
        d = self.result()
        self.assertTrue(all(sp.simplify(v) == 0 for v in d["schur_residual"]))
        self.assertEqual(sp.simplify(d["longitudinal"] - (2*d["A"]-4*d["At"]**2*d["g2"]/d["M"])), 0)

    def test_transverse_and_parallel_response_differ(self):
        d = self.result()
        matrix = d["principal"].subs({d["A"]:2,d["At"]:3,d["M"]:10,
                                     d["grad"][0]:sp.Rational(1,2),d["grad"][1]:0,d["grad"][2]:0})
        self.assertEqual(matrix, sp.diag(sp.Rational(31,10),4,4))

    def test_bad_gradient_is_detected_not_automatically_certified(self):
        d = self.result()
        matrix = d["principal"].subs({d["A"]:2,d["At"]:3,d["M"]:10,
                                     d["grad"][0]:2,d["grad"][1]:0,d["grad"][2]:0})
        self.assertLess(float(min(matrix.eigenvals())),0)

    def test_actual_ic6_mass_before_background_substitution(self):
        d = self.result()
        expected=sp.Matrix([[24,-27],[-27,2*d["T"]+sp.Rational(135,8)]])
        self.assertEqual((d["mass"]-expected).applyfunc(sp.expand),sp.zeros(2))
        self.assertTrue(all(v == 0 for v in d["mass_bridge"]))

    def test_fourier_inverse_includes_zero_mode(self):
        d = self.result()
        self.assertEqual((d["L0"]*d["inverse"]-sp.eye(2)).applyfunc(sp.factor),sp.zeros(2))
        self.assertNotEqual(sp.factor(d["L0"].subs(d["k2"],0).det()),0)

    def test_nonzero_mode_determinant_has_positive_slope(self):
        d = self.result()
        vals = {d["T"]:20,d["h0"]:1}
        determinant = sp.factor(d["L0"].det())
        self.assertGreater(float(determinant.subs(vals).subs(d["k2"],0)),0)
        self.assertGreater(float(sp.diff(determinant,d["k2"]).subs(vals)),0)

    def test_algebraic_coordinate_uses_correct_canonical_map(self):
        d = self.result()
        self.assertEqual(sp.factor(d["coordinate_map"].det()),1)
        self.assertTrue(all(v == 0 for v in d["canonical_residual"]))

    def test_eliminated_positive_form_is_exact(self):
        d = self.result()
        self.assertEqual(sp.factor(d["completion_residual"]),0)

    def test_numerical_fourier_control_is_not_a_rank_assignment(self):
        self.result()
        report = self.module.numerical_controls()
        self.assertLess(report["maximum_inverse_residual"],1e-8)
        self.assertGreater(report["minimum_eigenvalue"],0)
        self.assertEqual(report["tested_k_squared"][0],0)
        self.assertGreater(report["weighted_inverse_norm_max"],0)
        self.assertTrue(np.isfinite(report["weighted_inverse_norm_max"]))


if __name__ == "__main__":
    unittest.main()
