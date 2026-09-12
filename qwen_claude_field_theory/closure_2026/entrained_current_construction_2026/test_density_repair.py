import re
from pathlib import Path
import unittest

import sympy as s

from density_repair import calculate


class DensityRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = calculate()

    def test_lean_matches_derived_polynomial(self):
        source = Path(__file__).with_name("DensityRepair.lean").read_text()
        extract = lambda name: re.search(r"def "+name+r"(?: \(t : ℝ\))? : ℝ := (.*)", source)[1]
        u, t = s.symbols("u t")
        formal = s.sympify(extract("A"))*u*u+s.sympify(extract("B"))*u+s.sympify(extract("C"))
        derived = s.sympify(self.result["exact_equal_density_witnesses"]["1/10"]["polynomial"])
        self.assertEqual(s.expand(formal-derived), 0)

    def test_actual_health_and_failed_domain_both_retained(self):
        for item in self.result["exact_equal_density_witnesses"].values():
            self.assertTrue(item["positive_energy"])
            self.assertTrue(item["all_angle_squared_speeds_between_zero_and_one"])
        self.assertTrue(any(not item["positive_energy"] for item in self.result["finite_domain"]))
        self.assertFalse(self.result["high_velocity_test"]["all_angle_squared_speeds_between_zero_and_one"])

    def test_two_field_modes_not_hidden_auxiliaries(self):
        for sector in ("dirac_repaired_k0", "dirac_repaired_k1"):
            item = self.result[sector]
            self.assertEqual(s.sympify(item["physical_canonical_pairs"])/item["quadratures"], 2)
            self.assertTrue(item["closure_residual_zero"])

    def test_positive_energy_is_not_positive_isotropic_kick_pressure(self):
        item = self.result["stress_redistribution_gate"]
        d, p = s.symbols("d p", positive=True)
        trace = s.sympify(item["leading_coefficients_divided_by_v_squared"]["pressure_trace"], locals={"d": d, "p": p})
        self.assertEqual(s.simplify(trace-(-2-6*p)*d**(p+2)), 0)
        self.assertLess(trace.subs({p: s.Rational(1, 2), d: 1}), 0)


if __name__ == "__main__":
    unittest.main()
