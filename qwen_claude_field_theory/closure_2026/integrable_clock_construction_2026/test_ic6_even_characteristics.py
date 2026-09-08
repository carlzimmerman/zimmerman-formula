#!/usr/bin/env python3
"""Independent bridges, benchmark failures and repair conditions for IC6."""
import importlib.util
from pathlib import Path
import unittest

import mpmath as mp
import sympy as s

SPEC = importlib.util.spec_from_file_location("ic6_even_checked", Path(__file__).with_name("ic6_even_characteristics.py"))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class EvenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 80
        cls.states = {kind: MODULE.state(kind) for kind in ("isotropic", "isotropic_neighbor", "sheared")}

    def assertSmall(self, value, tolerance="1e-55"):
        magnitude = mp.norm(value, mp.inf) if isinstance(value, mp.matrix) else abs(value)
        self.assertLess(magnitude, mp.mpf(tolerance), mp.nstr(magnitude, 10))

    def test_all_background_auxiliaries_are_actually_solved(self):
        for background in self.states.values():
            self.assertSmall(mp.matrix(background["auxiliary_residual"]))
            self.assertGreater(background["J"], 0)
            self.assertGreater(background["u"], 0)
            self.assertLess(background["u"], 1)
            v, l1, l2, l3, xi, u, _ = background["point"]
            activation = -(l1+l2+l3)*mp.exp((4-3*u)*xi-v)/3
            self.assertLess(abs(activation**2-1), mp.mpf(1)/4)

    def test_constrained_homogeneous_tangent_includes_auxiliary_multipliers(self):
        for background in self.states.values():
            tangent = mp.matrix(MODULE.homogeneous_tangent(background)[:6])
            self.assertSmall(background["H"][4:6, :]*tangent)
        tangent = MODULE.homogeneous_tangent(self.states["isotropic"])
        self.assertSmall(tangent[0]-3)
        self.assertSmall(tangent[4])
        self.assertSmall(tangent[5])
        self.assertSmall(tangent[6]-1)

    def test_auxiliary_elimination_residuals_and_symmetry(self):
        for background in self.states.values():
            for k in (1, 1000):
                result = MODULE.pencil(background, mp.mpf(k), eigenvalues=False)
                self.assertSmall(result["auxiliary_EL_residual"], "1e-60")
                self.assertSmall(result["reduced"]-result["reduced"].T, "1e-60")

    def test_independent_compact_L_variation_eliminates_lapse_u_and_shift(self):
        for background in self.states.values():
            for k in (1, 10, 1000):
                result = MODULE.compact_lagrangian_bridge(background, mp.mpf(k))
                norm = max(1, mp.norm(result["expected"], mp.inf))
                self.assertSmall(result["residual"]/norm, "1e-65")
                self.assertSmall(result["auxiliary_EL_residual"], "1e-60")

    def test_frozen_canonical_scalar_speed_fails_the_witness_benchmark(self):
        background = self.states["isotropic"]
        frozen = MODULE.pencil(background, mp.mpf(10000))
        self.assertLess(min(mp.re(value) for value in frozen["speed_squares"]), 0)

    def test_time_dependent_reduction_restores_exact_isotropic_wave_equations(self):
        background = self.states["isotropic"]
        light = background["physical_light_speed_squared"]
        for k in (1, 1000):
            result = MODULE.evolving_pencil(background, mp.mpf(k))
            self.assertSmall(result["D"]+3*mp.eye(2), "1e-48")
            expected = mp.matrix([[-light*k*k/3, 0], [0, -light*k*k]])
            self.assertSmall((result["E"]-expected)/max(1, light*k*k), "1e-45")

    def test_complex_step_derivative_has_a_precision_control(self):
        background = self.states["sheared"]
        a = MODULE.evolving_pencil(background, mp.mpf(100), mp.mpf("1e-20"))
        b = MODULE.evolving_pencil(background, mp.mpf(100), mp.mpf("1e-30"))
        self.assertSmall((a["E"]-b["E"])/mp.norm(b["E"], mp.inf), "1e-35")
        self.assertSmall((a["D"]-b["D"])/mp.norm(b["D"], mp.inf), "1e-35")

    def test_exact_rank_one_auxiliary_expansion_matches_large_k_blocks(self):
        background = self.states["sheared"]
        asymptotic = MODULE.asymptotic_conditions(background)
        self.assertSmall(asymptotic["auxiliary_gradient_rank_one_residual"])
        k = mp.mpf("1e5")
        reduced = MODULE.pencil(background, k, eigenvalues=False)["reduced"]
        self.assertSmall(reduced[2:4, 2:4]-asymptotic["A0"], "1e-9")
        self.assertSmall(reduced[:2, 2:4]/k**2-asymptotic["B2"], "1e-9")
        # The next coefficient is retained, rather than misclassifying its
        # known O(k^-2) contribution as error in the leading coefficient.
        approximation = asymptotic["quartic_H"]*k**4+asymptotic["quadratic_H"]*k**2+asymptotic["constant_H"]
        self.assertSmall((reduced-approximation)/mp.norm(reduced, mp.inf), "1e-25")

    def test_sheared_quartic_growth_matches_complete_time_dependent_pencil(self):
        background = self.states["sheared"]
        asymptotic = MODULE.asymptotic_conditions(background)
        self.assertGreater(asymptotic["z_squared"], 0)
        predicted = mp.sqrt(asymptotic["z_squared"])
        k = mp.mpf(10000)
        result = MODULE.evolving_pencil(background, k)
        largest = max(mp.re(pole) for pole in result["poles"])/k**2
        self.assertLess(abs(largest-predicted), mp.mpf("1e-6"))

    def test_nonzero_gyro_cannot_be_fixed_by_curvature_squared_alone(self):
        result = MODULE.asymptotic_conditions(self.states["sheared"])
        self.assertGreater(abs(result["G2"][0, 1]), mp.mpf("1e-4"))
        self.assertLess(result["S4"][0, 0], 0)
        self.assertGreater(result["Rbar_squared_density_coefficient"], 0)
        self.assertLess(result["Rbar_squared_only_z_squared"], 0)
        self.assertSmall(result["S4"][1, 1])
        self.assertSmall(result["S4"][0, 1])

    def test_isotropic_neighbor_is_already_quartically_unstable(self):
        result = MODULE.asymptotic_conditions(self.states["isotropic_neighbor"])
        self.assertSmall(result["G2"])
        self.assertLess(result["S4"][0, 0], -mp.mpf("0.07"))
        self.assertGreater(result["z_squared"], 0)
        self.assertSmall(result["Rbar_squared_only_z_squared"])

    def test_symbolic_trace_branch_derivative_is_negative_in_proved_domain(self):
        result = MODULE.exact_trace_branch()
        for expression in result["residuals"].values():
            entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
            self.assertTrue(all(s.simplify(entry) == 0 for entry in entries))
        positive = s.Symbol("positive", positive=True)
        # T=27/4+positive makes every factor in -S4' strictly positive.
        self.assertTrue(s.factor(-result["S4_prime"].subs(result["T"], s.Rational(27, 4)+positive)).is_positive)

    def test_symbolic_trace_derivative_matches_actual_density_directional_check(self):
        witness = self.states["isotropic"]
        symbolic = MODULE.exact_trace_branch()
        Tvalue = -mp.mpf(27)/16+54/(5*mp.log(mp.mpf(9)/5))
        expected = mp.mpf(str(s.N(symbolic["S4_prime"].subs(symbolic["T"], str(Tvalue)), 70)))
        # Solve the actual nonlinear constraints on both sides, independent of
        # the closed derivative's hand-reduced null-auxiliary coefficients.
        values = []
        step = mp.mpf("1e-15")
        for sign in (-1, 1):
            momenta = [x*(1+sign*step) for x in witness["momenta"]]
            qfun = lambda n, u: tuple(MODULE.build()["aux_evaluate"](0, *momenta, n, u))
            q = mp.findroot(qfun, (witness["xi"], witness["u"]), tol=mp.mpf("1e-65"))
            state = MODULE.at_point([mp.mpf(0), *momenta, q[0], q[1], mp.mpf(0)])
            values.append(MODULE.asymptotic_conditions(state)["S4"][0, 0])
        self.assertLess(abs((values[1]-values[0])/(2*step)-expected), mp.mpf("1e-25"))


if __name__ == "__main__":
    unittest.main()
