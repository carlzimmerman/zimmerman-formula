"""Discrete conservation and independently soluble cold-collapse checks."""

import unittest

import numpy as np
from scipy.integrate import solve_ivp

import material

import collapse


class CollapseTests(unittest.TestCase):
    def setUp(self):
        self.params = material.MaterialParameters(rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=0.5)

    def test_uniform_virgin_sphere_has_exactly_zero_stress_and_heating(self):
        model = collapse.SphericalCollapse(8, self.params)
        y = model.initial_state()
        fields = model.fields(y)
        np.testing.assert_allclose(fields["rho"], 0.25, rtol=3e-15)
        np.testing.assert_allclose(fields["theta"], -0.75, rtol=3e-15)
        np.testing.assert_array_equal(fields["pressure"], np.zeros(8))
        np.testing.assert_array_equal(fields["q"], np.zeros(8))
        np.testing.assert_array_equal(model.rhs(0, y)[16:], np.zeros(8))
        np.testing.assert_allclose(
            model.rhs(0, y)[8:16], -np.pi * y[:8] / 3,
            rtol=3e-15,
        )

    def test_semidiscrete_energy_derivative_vanishes_during_dissipation(self):
        # A missing interface area, endpoint half-weight, or pressure-work term
        # breaks this independent directional derivative of total energy.
        model = collapse.SphericalCollapse(4, self.params)
        y = np.array([0.3, 0.5, 0.8, 1.0, -1, -2, -3, -4, 0.3, 0.4, 0.2, 0.1])
        dy = model.rhs(0, y)
        self.assertTrue(np.any(model.fields(y)["q"] > 0))
        eps = 2e-7
        derivative = (model.energy(y + eps * dy)["total"] - model.energy(y - eps * dy)["total"]) / (2 * eps)
        scale = sum(abs(v) for k, v in model.energy(y).items() if k != "total")
        self.assertLess(abs(derivative), 2e-7 * scale)
        self.assertTrue(np.all(dy[8:] >= 0))

    def test_cold_short_run_matches_independent_homologous_solution(self):
        model = collapse.SphericalCollapse(8, self.params)
        run = collapse.simulate(model, t_end=0.08, samples=9, wall_seconds=5)
        self.assertEqual(run["status"], "completed")
        reference = solve_ivp(
            lambda t, a: [a[1], -np.pi / (3 * a[0]**2)],
            (0, 0.08), [1, -0.25], rtol=1e-11, atol=1e-13,
        )
        expected_r = model.initial_state()[:8] * reference.y[0, -1]
        np.testing.assert_allclose(run["final_profile"]["r"], expected_r, rtol=2e-8)
        np.testing.assert_array_equal(run["final_profile"]["K"], np.zeros(8))
        self.assertLess(run["max_relative_energy_error"], 1e-7)

    def test_inverted_or_coincident_shells_are_rejected_before_density_evaluation(self):
        model = collapse.SphericalCollapse(4, self.params)
        for inner in [0.5, 0.8]:
            y = model.initial_state()
            y[:4] = [0.3, inner, 0.5, 1]
            with self.assertRaises(collapse.ShellOrderingError):
                model.rhs(0, y)

    def test_enclosed_density_estimator_interpolates_fixed_mass(self):
        model = collapse.SphericalCollapse(8, self.params)
        for fraction in [0.01, 0.05, 0.1, 0.5, 1.0]:
            radius, density = model.enclosed_estimator(model.initial_state(), fraction)
            self.assertAlmostEqual(radius, fraction**(1 / 3), places=13)
            self.assertAlmostEqual(density, 0.25, places=13)

    def test_resource_bound_is_reported_as_inconclusive(self):
        model = collapse.SphericalCollapse(8, self.params)
        run = collapse.simulate(model, t_end=8, samples=3, max_rhs_calls=1, wall_seconds=5)
        self.assertEqual(run["status"], "rhs_limit")
        self.assertLess(run["t_reached"], 8)

    def test_gate_crossing_rejects_invalid_trials_and_heats_without_state_projection(self):
        model = collapse.SphericalCollapse(64, self.params)
        run = collapse.simulate(model, t_end=0.66, samples=9, wall_seconds=5)
        self.assertEqual(run["status"], "completed")
        self.assertGreater(run["final"]["max_K"], 0)
        self.assertGreaterEqual(run["minimum_accepted_K"], 0)
        self.assertLess(run["max_relative_energy_error"], 2e-6)

    def test_stiff_integrator_crosses_the_same_gate_without_projection(self):
        model = collapse.SphericalCollapse(16, self.params)
        run = collapse.simulate(model, t_end=0.7, samples=8, wall_seconds=5, method="Radau")
        self.assertEqual(run["status"], "completed")
        self.assertGreater(run["final"]["max_K"], 0)
        self.assertGreaterEqual(run["minimum_accepted_K"], 0)
        self.assertLess(run["max_relative_energy_error"], 2e-6)

    def test_sparse_jacobian_pattern_contains_all_measured_dependencies(self):
        model = collapse.SphericalCollapse(5, self.params, initial_density=1.5,
                                           initial_velocity_gradient=-2)
        y = model.initial_state()
        y[10:] = np.linspace(0.2, 0.6, 5)
        pattern = model.jacobian_sparsity().toarray().astype(bool)
        jacobian = np.empty((15, 15))
        for j in range(15):
            direction = np.zeros(15)
            direction[j] = 1e-7
            jacobian[:, j] = (model.rhs(0, y + direction) - model.rhs(0, y - direction)) / 2e-7
        self.assertTrue(np.all(jacobian[~pattern] == 0))


if __name__ == "__main__":
    unittest.main()
