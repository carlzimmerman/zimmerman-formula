#!/usr/bin/env python3
"""Bounded IC11 action-pressure checks, not a full-theory certificate."""
import importlib.util
import unittest
import mpmath as mp
import sympy as s


class PressureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 55

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec("ic11_clock_pressure"))
        return __import__("ic11_clock_pressure")

    def test_action_lift_and_exact_derivative_identities(self):
        for residual in self.model().identities().values():
            self.assertEqual(s.simplify(residual), 0)

    def test_static_value_and_first_jets_vanish(self):
        model = self.model()
        self.assertTrue(hasattr(model, "phase_delta"))
        self.assertEqual(model.phase_delta(mp.mpf(".4"), mp.mpf("-.1"), 0), 0)
        for index in range(3):
            point = [mp.mpf(".4"), mp.mpf("-.1"), mp.mpf(0)]
            def vary(value):
                arguments = list(point)
                arguments[index] = value
                return model.phase_delta(*arguments)
            self.assertEqual(mp.diff(vary, point[index]), 0)

    def test_repair_preserves_auxiliary_root_but_changes_expansion(self):
        import ic10_local_clock as old
        model = self.model()
        a, b = old.state(".03"), model.state(".03")
        self.assertLess(abs(a["w"]-b["w"]), mp.mpf("1e-45"))
        self.assertGreater(a["speed_squared"], 1)
        self.assertTrue(b["admissible"])
        self.assertGreater(b["energy"], a["energy"])
        self.assertGreater(abs(b["physical_H"]-a["physical_H"]), mp.mpf(".01"))

    def test_eliminated_pressure_derivatives_independently(self):
        model = self.model()
        S, step = mp.mpf(".03"), mp.mpf("1e-11")
        a, b, c = [model.state(S+k*step) for k in (-1, 0, 1)]
        self.assertLess(abs((c["P"]-a["P"])/(2*step)-b["PS"]), mp.mpf("1e-17"))
        self.assertLess(abs((c["PS"]-a["PS"])/(2*step)-b["PSS_effective"]), mp.mpf("1e-16"))
        self.assertLess(abs(b["constraint_schur_identity"]), mp.mpf("1e-40"))

    def test_domain_does_not_reuse_old_activation(self):
        model = self.model()
        for S in (".0001", ".001", ".01", ".24"):
            self.assertFalse(model.state(S)["inside_eta_one"])
        for S in (".03", ".05", ".1", ".2"):
            self.assertTrue(model.state(S)["admissible"])

    def test_both_plateau_endpoints_and_interior(self):
        model = self.model()
        lo, hi = model.plateau_boundaries()
        self.assertTrue(mp.mpf(".01") < lo["S"] < mp.mpf(".03"))
        self.assertTrue(mp.mpf(".2") < hi["S"] < mp.mpf(".24"))
        for bg in (lo, hi):
            self.assertLess(abs(bg["activation_r"]**2-mp.mpf(5)/4), mp.mpf("1e-40"))
        for i in range(101):
            bg = model.state(mp.mpf(".03")+mp.mpf(".17")*i/100)
            self.assertTrue(bg["admissible"])

    def test_actual_flrw_charge_conservation(self):
        result = self.model().evolve(".03", ".1")
        self.assertGreater(result["physical_efolds"], 0)
        self.assertLess(abs(result["charge_ratio"]-1), mp.mpf("1e-40"))


if __name__ == "__main__":
    unittest.main()
