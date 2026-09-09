#!/usr/bin/env python3
"""Tests for the trace-aligned, local expanding plateau; not full closure."""
import importlib.util
import unittest
import mpmath as mp
import sympy as s


class LocalClockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 60

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec("ic10_local_clock"))
        return __import__("ic10_local_clock")

    def test_full_trace_and_tensor_legendre_identity(self):
        for residual in self.model().identities().values():
            self.assertEqual(s.simplify(residual), 0)

    def test_actual_algebraic_constraint_and_healthy_clock(self):
        model = self.model()
        for S in ("0.1", "0.15", "0.2"):
            bg = model.state(mp.mpf(S))
            self.assertLess(abs(bg["constraint"]), mp.mpf("1e-50"))
            self.assertGreater(bg["PX"], 0)
            self.assertGreater(bg["kinetic"], 0)
            self.assertGreater(bg["speed_squared"], 0)
            self.assertLess(bg["speed_squared"], 1)
            self.assertGreater(bg["energy"], 0)
            self.assertGreater(bg["physical_H"], 0)
            self.assertLess(abs(bg["activation_r"]**2-1), mp.mpf(1)/4)

    def test_auxiliary_pair_is_nondegenerate_from_actual_potential(self):
        model = self.model()
        for S in ("0.1", "0.2"):
            result = model.state(mp.mpf(S))
            self.assertGreater(abs(mp.det(result["auxiliary_bracket"])), mp.mpf("1e-10"))
            self.assertLess(abs(result["constraint_schur_identity"]), mp.mpf("1e-45"))

    def test_eliminated_clock_derivatives_against_finite_difference(self):
        model = self.model()
        S, step = mp.mpf("0.15"), mp.mpf("1e-12")
        a, b, c = model.state(S-step), model.state(S), model.state(S+step)
        self.assertLess(abs((c["P"]-a["P"])/(2*step)-b["PS"]), mp.mpf("1e-20"))
        self.assertLess(abs((c["PS"]-a["PS"])/(2*step)-b["PSS_effective"]), mp.mpf("1e-20"))

    def test_flrw_charge_conservation_and_friedmann_equation(self):
        result = self.model().evolve()
        self.assertGreater(result["barred_efolds"], 0)
        self.assertGreater(result["physical_efolds"], 0)
        self.assertGreater(result["proper_time"], 0)
        self.assertLess(abs(result["charge_ratio"]-1), mp.mpf("1e-45"))
        self.assertLess(abs(result["friedmann_residual"]), mp.mpf("1e-45"))

    def test_unhealthy_other_branch_is_not_discarded(self):
        bg = self.model().state(mp.mpf(1))
        self.assertLess(bg["speed_squared"], 0)
        self.assertGreater(abs(bg["activation_r"]**2-1), mp.mpf(1)/4)

    def test_next_transition_is_located_on_the_derived_evolution(self):
        model = self.model()
        self.assertTrue(hasattr(model, "plateau_boundary"))
        result = model.plateau_boundary()
        self.assertGreater(result["S"], mp.mpf("0.2"))
        self.assertLess(abs(result["activation_r"]**2-mp.mpf(5)/4), mp.mpf("1e-45"))
        self.assertGreater(result["speed_squared"], 0)


if __name__ == "__main__":
    unittest.main()
