#!/usr/bin/env python3
"""Nontrivial controls: formal polynomial linkage, physical path, and Hilbert variation."""
import re
from pathlib import Path
import unittest

import sympy as s

from current_action import calculate
from variation import derive


class CurrentActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = calculate()

    def test_lean_polynomial_is_the_derived_polynomial(self):
        source = Path(__file__).with_name("CounterflowCone.lean").read_text()
        extract = lambda name: re.search(r"def "+name+r"(?: \(t : ℝ\))? : ℝ := (.*)", source)[1]
        u, t = s.symbols("u t")
        formal = (s.sympify(extract("A"))*u*u+s.sympify(extract("B"))*u
                  +s.sympify(extract("C")))
        actual = s.sympify(self.result["healthy_witness"]["polynomial_in_speed_squared"])
        self.assertEqual(s.expand(formal-actual), 0)

    def test_lean_small_velocity_expression_matches_variation(self):
        v, t = s.symbols("v t")
        formal = t*(717*t**3-1753*t**2+235*t+1)/((3*t*t-2*t+1)*(239*t*t-374*t-9))
        actual = s.sympify(self.result["small_velocity_branch"]["exact_squared_speed"])
        self.assertEqual(s.factor(formal.subs(t, v*v)-actual), 0)

    def test_boundary_and_mode_count_are_not_skipped(self):
        for branch in ("coflow", "healthy_witness"):
            for sector in ("dirac_k0", "dirac_k1"):
                d = self.result[branch][sector]
                matrix = s.Matrix([[s.sympify(x) for x in row] for row in d["poisson_matrix"]])
                self.assertEqual(matrix+matrix.T, s.zeros(matrix.rows))
                self.assertEqual(d["poisson_rank"], matrix.rows)
                self.assertTrue(d["closure_residual_zero"])
                self.assertEqual(d["free_multiplier_parameters"], 0)
        self.assertEqual(self.result["coflow"]["dirac_k1"]["phase_dimension"],
                         2*self.result["coflow"]["dirac_k0"]["phase_dimension"])

    def test_healthy_witness_does_not_hide_bad_path(self):
        self.assertTrue(any(x < 0 for x in self.result["same_action_path"][0]["transverse_numeric"]))
        self.assertLess(s.sympify(self.result["small_velocity_branch"]["limit_speed_squared_over_v_squared"]), 0)

    def test_metric_variation_independent_of_current_derivative(self):
        result = derive()
        self.assertEqual(set(result["ten_hilbert_variation_residuals"]), {"0"})


if __name__ == "__main__":
    unittest.main()
