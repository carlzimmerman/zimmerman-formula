"""Catch sign errors, dropped geometric terms, and nonconservative integration."""
import importlib.util
import unittest

import sympy as s


class StationaryHaloTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.available = importlib.util.find_spec("stationary_halo") is not None
        if cls.available:
            import stationary_halo
            cls.module = stationary_halo

    def require_implementation(self):
        self.assertTrue(self.available, "Action-derived stationary halo implementation is missing")

    def test_bernoulli_derived_before_specializing(self):
        self.require_implementation()
        data = self.module.derive()
        n, v, p = data["symbols"]
        expected = (1-(s.Rational(3, 2)+p*n**(p+1))*v*v)/(1-v*v)**s.Rational(3, 2)
        self.assertEqual(s.simplify(data["H"]-expected), 0)
        self.assertEqual(s.simplify(data["H"].subs(v, 0)), 1)

    def test_geometrical_stress_conservation(self):
        self.require_implementation()
        self.assertEqual(self.module.derive()["ward_residual"], 0)

    def test_refinement_and_first_integrals(self):
        self.require_implementation()
        coarse = self.module.integrate_shell(max_step=0.02)
        fine = self.module.integrate_shell(max_step=0.01)
        self.assertTrue(coarse["solver_success"] and fine["solver_success"])
        self.assertLess(fine["flux_relative_error"], 1e-8)
        self.assertLess(fine["bernoulli_absolute_error"], 1e-10)
        self.assertLess(abs(coarse["log_radius_final"]-fine["log_radius_final"]), 1e-6)
        self.assertGreater(len(fine["samples"]), 5)


if __name__ == "__main__":
    unittest.main()
