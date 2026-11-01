"""Conservation and constitutive tests for the distinct gated-heat hypothesis."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import collapse
import material

try:
    import convective_transport as convective
except ModuleNotFoundError:
    convective = None


class ConvectiveTransportTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(convective, "instability-gated transport implementation is absent")
        self.params = material.MaterialParameters(1, np.sqrt(8 * np.pi), 1, 0.5)

    def model(self, n=4, density=3, velocity=0, **options):
        return convective.ConvectiveCollapse(
            n, self.params, transport=convective.ConvectiveParameters(**options),
            initial_density=density, initial_velocity_gradient=velocity,
        )

    def test_active_exchange_and_expansion_heat_conserve_total_energy(self):
        # A wrong luminosity sign or inconsistent damping work breaks this.
        model = self.model(4, velocity=0.2)
        y = model.initial_state()
        y[8:] = [0.5, 0.3, 0.2, 0.1]
        self.assertTrue(np.all(model.fields(y)["luminosity"][1:-1] > 0))
        dy = model.rhs(0, y)
        epsilon = 2e-7
        derivative = (model.energy(y + epsilon * dy)["total"] -
                      model.energy(y - epsilon * dy)["total"]) / (2 * epsilon)
        energy_scale = sum(abs(value) for key, value in model.energy(y).items() if key != "total")
        self.assertLess(abs(derivative), energy_scale * 3e-7)

    def test_hot_inner_pair_warms_virgin_neighbor_and_increases_entropy(self):
        # Catches a gate that blocks first warming or exchanges energy backward.
        model = self.model(2, damping_strength=0)
        fixed = model.initial_state()
        fixed[4:] = [0.6, 0]
        f = model.fields(fixed)
        self.assertLess(f["dk_conduction"][0], 0)
        self.assertGreater(f["dk_conduction"][1], 0)
        def rhs(t, K):
            y = fixed.copy()
            y[4:] = K
            return model.fields(y)["dk_conduction"]
        run = solve_ivp(rhs, (0, 1), fixed[4:], rtol=1e-10, atol=1e-12)
        self.assertTrue(run.success)
        self.assertGreaterEqual(run.y.min(), 0)
        np.testing.assert_allclose(run.y.sum(axis=0), 0.6, atol=2e-15)
        self.assertTrue(np.all(np.diff(np.cbrt(run.y).sum(axis=0)) >= -2e-13))
        self.assertGreaterEqual(run.y[0, -1], run.y[1, -1])

    def test_stable_entropy_is_exactly_quiet_even_with_hot_inner_temperature(self):
        # Catches an absent entropy gate or a nonzero gate floor.
        model = self.model(3)
        y = model.initial_state()
        rho = np.array([6.0, 4.0, 2.5])
        y[:3] = np.cbrt(3 * np.cumsum(model.dm / rho) / (4 * np.pi))
        y[6:] = [0.2, 0.25, 0.3]
        f = model.fields(y)
        self.assertTrue(np.all(np.diff(f["temperature_bar"]) < 0))
        np.testing.assert_array_equal(f["convective_gate"], np.zeros(2))
        np.testing.assert_array_equal(f["luminosity"], np.zeros(4))
        np.testing.assert_array_equal(f["dk_conduction"], np.zeros(3))

    def test_unstable_entropy_with_cold_inner_temperature_has_no_inward_flux(self):
        # Catches multiplying a negative Fourier flux by a positive instability gate.
        model = self.model(2)
        y = model.initial_state()
        rho = np.array([1.5, 6.0])
        y[:2] = np.cbrt(3 * np.cumsum(model.dm / rho) / (4 * np.pi))
        y[4:] = [0.3, 0.2]
        f = model.fields(y)
        self.assertGreater(f["convective_gate"][0], 0)
        self.assertLess(f["temperature_bar"][0], f["temperature_bar"][1])
        np.testing.assert_array_equal(f["luminosity"], np.zeros(3))
        np.testing.assert_array_equal(f["dk_conduction"], np.zeros(2))

    def test_dormant_interface_and_closed_boundaries_are_exactly_quiet(self):
        # Catches missing two-sided density gates or a ghost-boundary heat sink.
        model = self.model(3)
        y = model.initial_state()
        rho = np.array([3.0, 0.5, 3.0])
        y[:3] = np.cbrt(3 * np.cumsum(model.dm / rho) / (4 * np.pi))
        y[6:] = [0.6, 0.4, 0.1]
        np.testing.assert_array_equal(model.fields(y)["luminosity"], np.zeros(4))

    def test_finite_physical_gradient_does_not_quench_under_refinement(self):
        # Omitting division by center separation would drive the gate to zero.
        for n in [32, 64, 128]:
            model = self.model(n)
            y = model.initial_state()
            centers = model.fields(y)["center_radius"]
            y[2 * n:] = 0.6 - 0.4 * centers
            f = model.fields(y)
            midpoint = 0.5 * (centers[:-1] + centers[1:])
            xi_exact = 0.04 / (0.61 - 0.4 * midpoint)
            np.testing.assert_allclose(f["convective_gate"], xi_exact / (1 + xi_exact), rtol=3e-13)
            self.assertGreater(f["convective_gate"].min(), 0.06)

    def test_face_flux_is_nondecreasing_inner_K_nonincreasing_outer_K(self):
        # Detects a backward parabolic branch at positive K and fixed geometry.
        for density, memory in [([3, 3], [0.6, 0.2]), ([2.5, 6], [1.5, 0.3]),
                                ([2.5, 6], [0.3, 0.2]), ([3, 3], [0.2, 0.6])]:
            model = self.model(2)
            y = model.initial_state()
            y[:2] = np.cbrt(3 * np.cumsum(model.dm / np.array(density)) / (4 * np.pi))
            y[4:] = memory
            for index, expected_sign in [(4, 1), (5, -1)]:
                direction = np.zeros(6)
                direction[index] = 1e-7
                derivative = (model.fields(y + direction)["luminosity"][1] -
                              model.fields(y - direction)["luminosity"][1]) / 2e-7
                self.assertGreaterEqual(expected_sign * derivative, -1e-12)

    def test_sparse_pattern_still_covers_all_dependencies(self):
        model = self.model(5, density=1.6, velocity=-0.8)
        y = model.initial_state()
        y[10:] = np.linspace(0.6, 0.1, 5)
        pattern = model.jacobian_sparsity().toarray().astype(bool)
        for j in range(15):
            direction = np.zeros(15)
            direction[j] = 1e-7
            derivative = (model.rhs(0, y + direction) - model.rhs(0, y - direction)) / 2e-7
            self.assertTrue(np.all(derivative[~pattern[:, j]] == 0))

    def test_cold_forest_matches_original_source_and_fixed_mass_density(self):
        model = self.model(8, density=0.25, velocity=-0.25)
        original = collapse.SphericalCollapse(8, self.params)
        y = model.initial_state()
        np.testing.assert_array_equal(model.rhs(0, y), original.rhs(0, y))
        diagnostics = model.diagnostics(0, y)
        self.assertAlmostEqual(diagnostics["enclosed_1pct_mean_density"], 0.25, places=14)
        self.assertAlmostEqual(diagnostics["enclosed_1pct_radius"], 0.01**(1 / 3), places=14)

    def test_cli_preserves_new_parameters_and_restart(self):
        # Catches silently dropping subclass scales during serialization/restart.
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.json"
            second = Path(directory) / "second.json"
            common = [sys.executable, str(HERE / "convective_transport.py"), "--shells", "4",
                      "--stratification-length", "0.12", "--stratification-scale", "0.02",
                      "--samples", "3", "--wall-seconds", "5"]
            one = subprocess.run(common + ["--t-end", "0.02", "--output", str(first)],
                                 capture_output=True, text=True)
            self.assertEqual(one.returncode, 0, one.stderr)
            two = subprocess.run(common + ["--t-end", "0.04", "--restart", str(first),
                                            "--output", str(second)], capture_output=True, text=True)
            self.assertEqual(two.returncode, 0, two.stderr)
            result = json.loads(second.read_text())
            self.assertEqual(result["transport_parameters"]["stratification_length"], 0.12)
            self.assertEqual(result["transport_parameters"]["stratification_scale"], 0.02)
            self.assertEqual(result["t_initial"], 0.02)
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["closure"], "outward_instability_gated_heat")


if __name__ == "__main__":
    unittest.main()
