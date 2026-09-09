#!/usr/bin/env python3
"""Structural repair tests; wrong tensor/auxiliary derivatives must fail."""
import importlib.util
from pathlib import Path
import unittest
import mpmath as mp
import sympy as s
import ic6_even_characteristics as old


class ShearIntegrabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 80

    def model(self):
        name = "ic8_shear_integrability"
        spec = importlib.util.find_spec(name)
        self.assertIsNotNone(spec, "The new action construction has not been implemented")
        return __import__(name)

    def small(self, expression, tol="1e-55"):
        value = mp.norm(expression, mp.inf) if isinstance(expression, mp.matrix) else abs(expression)
        self.assertLess(value, mp.mpf(tol))

    def test_passive_auxiliary_and_trace_kinetic_derivatives_vanish(self):
        model = self.model()
        for value in model.symbolic_identities().values():
            self.assertEqual(s.simplify(value), 0)

    def test_isotropic_background_equations_are_the_same(self):
        model = self.model()
        for kind in ("isotropic", "isotropic_neighbor"):
            a, b = old.state(kind), model.state(kind)
            self.small(a["xi"]-b["xi"])
            self.small(a["u"]-b["u"])

    def test_sheared_background_is_resolved_not_borrowed(self):
        model = self.model()
        oldbg, bg = old.state("sheared"), model.state("sheared")
        self.small(mp.matrix(bg["auxiliary_residual"]))
        self.assertGreater(abs(oldbg["xi"]-bg["xi"]), mp.mpf("1e-5"))

    def test_both_higher_order_conditions_cancel_on_three_principal_axes(self):
        model = self.model()
        for permutation in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
            bg = model.state("sheared", permutation=permutation)
            out = model.conditions(bg)
            self.small(out["G2"])
            self.small(out["S4"])

    def test_scalar_is_not_certified_by_the_quartic_cancellation(self):
        model = self.model()
        # Same action family, deliberately poor slope: principal orders cancel
        # but the computed scalar speed is superluminal.
        bg = model.state("isotropic", slope=mp.mpf(1))
        self.small(model.conditions(bg)["S4"])
        result = model.evolution(bg, mp.mpf(10000))
        self.assertGreater(max(mp.re(x) for x in result["speed_squares"]), 2)

    def test_default_isotropic_scalar_has_positive_mass_and_subluminal_uv_ratio(self):
        model = self.model()
        bg = model.state("isotropic")
        result = model.evolution(bg, mp.mpf(10000))
        mass = model.conditions(bg)["M0"]
        self.assertGreater(mass[0, 0], 0)
        self.assertGreater(mp.det(mass), 0)
        values = sorted(mp.re(x) for x in result["speed_squares"])
        self.assertGreater(values[0], 0)
        self.assertLess(values[1], 1)

    def test_independent_compact_action_bridge(self):
        model = self.model()
        for kind in ("isotropic", "sheared"):
            for k in (1, 100):
                self.small(model.lagrangian_bridge(model.state(kind), mp.mpf(k)), "1e-60")


if __name__ == "__main__":
    unittest.main()
