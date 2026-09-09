#!/usr/bin/env python3
"""Tests of the optical auxiliary variable and its SAME-action propagation."""
import importlib.util
import unittest
import mpmath as mp
import sympy as s
import ic6_even_characteristics as old


class LightconeAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 80

    def model(self):
        spec = importlib.util.find_spec("ic9_lightcone_alignment")
        self.assertIsNotNone(spec, "The optical-alignment action is missing")
        return __import__("ic9_lightcone_alignment")

    def small(self, value, tol="1e-55"):
        size = mp.norm(value, mp.inf) if isinstance(value, mp.matrix) else abs(value)
        self.assertLess(size, mp.mpf(tol))

    def test_symbolic_optical_alignment_and_conformal_action(self):
        for value in self.model().symbolic_identities().values():
            self.assertEqual(s.simplify(value), 0)

    def test_actual_isotropic_and_sheared_auxiliary_solutions(self):
        model = self.model()
        for kind in ("isotropic", "isotropic_neighbor", "sheared"):
            bg = model.state(kind)
            self.small(mp.matrix(bg["auxiliary_residual"]))
            self.assertGreater(bg["J"], 0)

    def test_no_quartic_counterterm_is_needed_for_either_condition(self):
        model = self.model()
        for permutation in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
            bg = model.state("sheared", permutation=permutation)
            conditions = old.asymptotic_conditions(bg)
            self.small(conditions["G2"])
            self.small(conditions["S4"])
            self.small(conditions["B2"])

    def test_derived_principal_coefficients_match_constrained_phase_Hessian(self):
        model = self.model()
        for kind in ("isotropic", "isotropic_neighbor", "sheared"):
            bg = model.state(kind)
            values = model.principal(bg)
            actual = old.asymptotic_conditions(bg)
            self.small(actual["A0"]-values["A0"])
            self.small(actual["quadratic_H"][:2, :2]-values["C2"])

    def test_all_sampled_principal_axes_have_a_physical_null_tensor(self):
        model = self.model()
        for permutation in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
            bg = model.state("sheared", permutation=permutation)
            values = model.principal(bg)
            self.small(values["tensor_speed_squared"]-1)
            self.assertGreater(values["scalar_speed_squared"], 0)
            self.assertLess(values["scalar_speed_squared"], 1)
            result = model.evolution(bg, mp.mpf(10000))
            nearest = min(result["speed_squares"], key=lambda x:abs(mp.re(x)-1))
            self.assertLess(abs(mp.re(nearest)-1), mp.mpf("1e-6"))

    def test_background_evolution_remains_in_the_lower_order_terms(self):
        model = self.model()
        bg = model.state("sheared")
        a = model.evolution(bg, mp.mpf(100), step=mp.mpf("1e-20"))
        b = model.evolution(bg, mp.mpf(100), step=mp.mpf("1e-30"))
        self.small((a["E"]-b["E"])/mp.norm(b["E"]), "1e-35")

    def test_independent_exact_plateau_Lagrangian_bridge(self):
        model = self.model()
        for kind in ("isotropic", "sheared"):
            for k in (1, 100):
                self.small(model.lagrangian_bridge(model.state(kind), mp.mpf(k)), "1e-60")

    def test_exact_finite_wave_equation_matches_actual_background_evolution(self):
        model = self.model()
        self.assertTrue(hasattr(model, "witness_reduction"), "The finite-wave equation is not derived")
        result = model.witness_reduction()
        bg = model.state("isotropic")
        T = -mp.mpf(27)/16+54/(5*mp.log(mp.mpf(9)/5))
        alpha = 81/(8*T*T)
        evaluate = s.lambdify((result["x"], result["T"], result["alpha"]),
                             (result["a"], result["D"], result["E"]), "mpmath")
        for k in (mp.mpf("0.1"), mp.mpf(1), mp.mpf(100)):
            a, D, E = evaluate(bg["physical_light_speed_squared"]*k*k, T, alpha)
            actual = model.evolution(bg, k)
            H = old.pencil(bg, k, eigenvalues=False)["reduced"]
            self.small(a-H[2, 2]*mp.exp(-mp.mpf(1)/2))
            self.small(D-actual["D"][0, 0], "1e-45")
            self.small(E-actual["E"][0, 0], "1e-43")

    def test_finite_wave_kinetic_has_no_real_positive_wavenumber_pole(self):
        model = self.model()
        self.assertTrue(hasattr(model, "witness_reduction"))
        result = model.witness_reduction()
        positive = s.Symbol("positive", positive=True)
        a = s.factor(result["a"].subs(result["T"], s.Rational(27, 4)+positive))
        self.assertTrue(a.is_positive)

    def test_uv_cone_is_not_misreported_as_full_wave_locality(self):
        model = self.model()
        self.assertTrue(hasattr(model, "witness_reduction"))
        result = model.witness_reduction()
        self.assertNotEqual(s.factor(s.diff(result["D"], result["x"])), 0)
        self.assertGreater(s.degree(s.denom(s.cancel(result["E"])), result["x"]), 0)

    def test_potential_only_orthogonal_repair_is_derived(self):
        model = self.model()
        self.assertTrue(hasattr(model, "potential_repair"))
        result = model.potential_repair()
        self.assertGreater(result["mass"].det(), 0)
        self.assertGreater(result["mass"][0, 0], 0)
        self.assertEqual(result["orthogonality"], 0)
        self.assertEqual(s.diff(result["a"], result["x"]), 0)
        self.assertEqual(s.factor(result["locality_identity"]), 0)
        self.assertNotEqual(result["uncancelled_pole_residue"], 0)

    def test_clock_response_is_not_hidden_by_the_metric_variable(self):
        model = self.model()
        self.assertTrue(hasattr(model, "clock_response"))
        result = model.clock_response()
        self.assertEqual(s.simplify(result["constraint_residual"]), s.zeros(2, 2))
        self.assertGreater(s.degree(s.denom(s.cancel(result["bracket"])), result["x"]), 0)


if __name__ == "__main__":
    unittest.main()
