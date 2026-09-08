#!/usr/bin/env python3
"""Action-level isotropic repair; tests deliberately retain the shear gap."""
import unittest
import mpmath as mp
import sympy as s
import ic6_even_characteristics as old
import ic7_curvature_square as new


class CurvatureSquareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 80
        cls.states = [new.trace_state(j) for j in ("0.998", "1", "1.002", "1.007")]

    def small(self, value, tolerance="1e-55"):
        magnitude = mp.norm(value, mp.inf) if isinstance(value, mp.matrix) else abs(value)
        self.assertLess(magnitude, mp.mpf(tolerance))

    def test_symbolic_coefficient_and_metric_measure_bridges(self):
        for value in new.symbolic_bridges().values():
            self.assertEqual(s.simplify(value), 0)

    def test_actual_auxiliary_roots_and_regular_denominator(self):
        for bg in self.states:
            self.small(mp.matrix(bg["auxiliary_residual"]))
            self.assertGreater(abs(mp.det(new.coefficient(bg)["M"])), 1)
            self.assertEqual(new.coefficient(bg)["cutoff"], 1)

    def test_zero_extension_does_not_invert_a_singular_static_matrix(self):
        bg = old.at_point([mp.mpf(0)]*4+[mp.mpf(1)/4, mp.mpf(2)/3, mp.mpf(0)])
        result = new.coefficient(bg)
        self.small(mp.det(result["M"]))
        self.assertEqual(result["c7"], 0)
        self.assertEqual(result["cutoff"], 0)

    def test_determinant_cutoff_support_and_transition(self):
        for ratio in (0, mp.mpf("0.5"), mp.mpf("1.5"), 2):
            self.assertEqual(new.determinant_cutoff(ratio), 0)
        for ratio in (mp.mpf("0.75"), 1, mp.mpf("1.25")):
            self.assertEqual(new.determinant_cutoff(ratio), 1)
        for ratio in (mp.mpf("0.625"), mp.mpf("1.375")):
            self.small(new.determinant_cutoff(ratio)-mp.mpf(1)/2)

    def test_invariant_derivatives_match_full_metric_momentum_Hessian(self):
        for bg in self.states:
            result = new.coefficient_bridge(bg)
            self.small(result["mass_residual"])
            self.small(result["source_residual"])

    def test_volume_and_wave_coordinate_factors_are_not_assumed_unity(self):
        bg = new.trace_state("1.004", volume="1.7", zscale="0.13")
        result = new.coefficient_bridge(bg)
        self.small(result["mass_residual"])
        self.small(result["source_residual"])
        self.small(new.repair_conditions(bg)["S4"])

    def test_witness_quadratic_action_is_unchanged(self):
        self.small(new.coefficient(self.states[1])["c7"])
        self.small(new.repaired_pencil(self.states[1], mp.mpf(20))["correction"])

    def test_isotropic_quartic_and_gyro_conditions_cancel(self):
        for bg in self.states:
            conditions = new.repair_conditions(bg)
            self.small(conditions["S4"])
            self.small(conditions["G2"])

    def test_removed_repair_and_wrong_coefficient_are_detected(self):
        bg = self.states[-1]
        for factor in (0, mp.mpf("0.9"), -1):
            conditions = new.repair_conditions(bg, factor=factor)
            self.assertGreater(mp.norm(conditions["S4"], mp.inf), mp.mpf("0.001"))

    def test_independent_quadratic_Legendre_bridge(self):
        for bg in (self.states[1], self.states[-1], old.state("sheared")):
            for k in (1, 100):
                self.small(new.lagrangian_bridge(bg, mp.mpf(k)), "1e-60")

    def test_repaired_neighbor_has_positive_mass_and_bounded_wave_speeds(self):
        bg = self.states[-1]
        for k in (mp.mpf(1000), mp.mpf(10000)):
            result = new.evolving_pencil(bg, k)
            mass = new.repaired_pencil(bg, k)["reduced"][2:4, 2:4]**-1
            self.assertGreater(mass[0, 0], 0)
            self.assertGreater(mp.det(mass), 0)
            speeds = sorted(mp.re(c) for c in result["speed_squares"])
            self.assertGreater(speeds[0], mp.mpf("0.3"))
            self.assertLess(speeds[1], mp.mpf("0.5"))
            self.assertLess(abs(speeds[-1]-1), mp.mpf("0.000003"))
            self.assertLess(max(abs(mp.im(c)) for c in result["speed_squares"]), mp.mpf("0.003"))

    def test_evolving_background_terms_still_matter(self):
        bg = self.states[1]
        result = new.evolving_pencil(bg, mp.mpf(1000))
        light = bg["physical_light_speed_squared"]
        self.small(result["D"]+3*mp.eye(2), "1e-48")
        self.small(result["E"]/1000000+light*mp.matrix([[mp.mpf(1)/3, 0], [0, 1]]), "1e-45")

    def test_shear_gyro_is_not_misreported_as_repaired(self):
        bg = old.state("sheared")
        before = old.asymptotic_conditions(bg)
        after = new.repair_conditions(bg)
        self.small(after["G2"]-before["G2"])
        self.assertGreater(abs(after["G2"][0, 1]), mp.mpf("0.0001"))


if __name__ == "__main__":
    unittest.main()
