#!/usr/bin/env python3
"""Test the full IC10 switch derivatives, not a plateau extrapolation."""
import importlib.util
import unittest
import mpmath as mp
import ic10_local_clock as plateau


class TransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps = 60

    def model(self):
        self.assertIsNotNone(importlib.util.find_spec("ic10_transition"))
        return __import__("ic10_transition")

    def test_switch_jets_match_independent_numerical_derivatives(self):
        model = self.model()
        for r in map(mp.mpf, ("0", "1", "1.15", "1.19", "1.24")):
            value, first, second = model.activation(r)
            self.assertLess(abs(first-mp.diff(model.activation_value, r)), mp.mpf("1e-45"))
            self.assertLess(abs(second-mp.diff(model.activation_value, r, 2)), mp.mpf("1e-43"))

    def test_activation_complement_survives_boundary_cancellation(self):
        model = self.model()
        r = mp.sqrt(mp.mpf(5)/4)+mp.mpf("1e-8")
        self.assertEqual(model.activation(r)[0],1)
        self.assertGreater(model.activation_complement(r),0)

    def test_actual_hamiltonian_gradient_and_hessian_include_switch_jets(self):
        model = self.model()
        xi, u = mp.mpf("0.18"), mp.mpf("0.6")
        rho = -3*mp.mpf("1.17")/mp.exp((4-3*u)*xi)
        point = [rho, xi, u]
        actual = model.at_point(point)
        for i in range(3):
            order = tuple(int(j == i) for j in range(3))
            self.assertLess(abs(actual["gradient"][i]-mp.diff(model.raw_density, tuple(point), order)), mp.mpf("1e-43"))
            for j in range(3):
                order = tuple(int(k == i)+int(k == j) for k in range(3))
                self.assertLess(abs(actual["hessian"][i, j]-mp.diff(model.raw_density, tuple(point), order)), mp.mpf("1e-40"))

    def test_recovers_the_independent_local_pressure_branch(self):
        model = self.model()
        for S in map(mp.mpf, ("0.1", "0.2")):
            old = plateau.state(S)
            rho = -3*mp.exp(-mp.mpf(1)/6)*old["H"]
            point = [rho, S+old["w"], old["u"]]
            bg = model.at_point(point)
            self.assertLess(mp.norm(bg["gradient"][1:3, :]), mp.mpf("1e-48"))
            self.assertLess(abs(bg["physical_H"]-old["physical_H"]), mp.mpf("1e-45"))
            self.assertLess(abs(bg["tensor_speed_squared"]-1), mp.mpf("1e-45"))

    def test_constraints_preserve_without_projection_at_a_solved_state(self):
        model = self.model()
        old = plateau.state(mp.mpf("0.2"))
        rho = -3*mp.exp(-mp.mpf(1)/6)*old["H"]
        bg = model.solve_rho(rho, [mp.mpf("0.2")+old["w"], old["u"]])
        self.assertLess(mp.norm(bg["preservation_residual"]), mp.mpf("1e-45"))
        self.assertGreater(abs(mp.det(bg["dirac_matrix"])), mp.mpf("1e-10"))
        self.assertLess(abs(bg["energy_preservation"]), mp.mpf("1e-45"))

    def test_full_gradient_matches_direct_second_variation(self):
        model = self.model()
        point = list(map(mp.mpf, ("-2", "0.18", "0.6")))
        point[0] = -3*mp.mpf("1.17")/mp.exp((4-3*point[2])*point[1])
        G = model.spatial_gradient(point)["G"]
        self.assertGreater(mp.norm(G),mp.mpf("1e-8"))
        for i in range(2):
            for j in range(2):
                order = tuple(int(k == i)+int(k == j) for k in range(2))
                direct = mp.diff(lambda x,y: model.raw_spatial_density(point, x, y),
                                 (mp.mpf(0),mp.mpf(0)), order)
                self.assertLess(abs(G[i,j]-direct), mp.mpf("1e-45"))

    def test_continuation_reaches_transition_and_resolves_actual_pole(self):
        model = self.model()
        states = list(model.continuation(500))
        self.assertEqual(len(states), 501)
        self.assertTrue(any(0 < bg["eta"] < 1 for bg in states))
        bg = states[200]
        poles = model.auxiliary_poles(bg)
        self.assertTrue(poles)
        self.assertTrue(all(x > 0 for x in poles))
        G = model.spatial_gradient(bg["point"])["G"]
        for x in poles:
            pencil = bg["auxiliary"]+x*G
            self.assertLess(abs(mp.det(pencil))/(1+mp.norm(pencil)**2), mp.mpf("1e-45"))


if __name__ == "__main__":
    unittest.main()
