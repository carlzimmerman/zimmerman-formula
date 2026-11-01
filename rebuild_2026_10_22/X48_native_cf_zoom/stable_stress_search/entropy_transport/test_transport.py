"""Independent invariants and soluble benchmarks for entropy transport."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import collapse
import material

try:
    import transport
except ModuleNotFoundError:
    transport = None


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(transport, "entropy transport implementation is absent")
        self.params = material.MaterialParameters(rho_q=1, G=1,
                                                  a0=np.sqrt(8 * np.pi), tau=0.5)

    def model(self, n=4, density=3, velocity=0, **transport_options):
        return transport.TransportCollapse(
            n, self.params, transport=transport.TransportParameters(**transport_options),
            initial_density=density, initial_velocity_gradient=velocity,
        )

    def test_conduction_and_expansion_damping_conserve_total_energy(self):
        # Catches flux signs, missing W/dm, or a mismatch between force and heat.
        model = self.model(4, velocity=0.3)
        y = model.initial_state()
        y[8:] = [0.4, 0.1, 0.3, 0.2]
        fields = model.fields(y)
        self.assertTrue(np.any(fields["luminosity"][1:-1] != 0))
        self.assertTrue(np.all(fields["q_damping"] < 0))
        dy = model.rhs(0, y)
        epsilon = 2e-7
        derivative = (model.energy(y + epsilon * dy)["total"] -
                      model.energy(y - epsilon * dy)["total"]) / (2 * epsilon)
        scale = sum(abs(value) for key, value in model.energy(y).items() if key != "total")
        self.assertLess(abs(derivative), 3e-7 * scale)

    def test_isolated_pair_warms_virgin_cell_and_increases_entropy(self):
        # Catches backward heat flow and artificial suppression of first warming.
        model = self.model(2, damping_strength=0)
        fixed = model.initial_state()
        fixed[4:] = [0.6, 0.0]
        fields = model.fields(fixed)
        self.assertLess(fields["dk_conduction"][0], 0)
        self.assertGreater(fields["dk_conduction"][1], 0)
        self.assertEqual(fields["luminosity"][0], 0)
        self.assertEqual(fields["luminosity"][-1], 0)
        def rhs(t, memory):
            y = fixed.copy()
            y[4:] = memory
            return model.fields(y)["dk_conduction"]
        run = solve_ivp(rhs, (0, 0.5), fixed[4:], rtol=1e-10, atol=1e-12)
        self.assertTrue(run.success)
        np.testing.assert_allclose(run.y.sum(axis=0), 0.6, atol=2e-15)
        self.assertGreaterEqual(float(run.y.min()), 0)
        entropy = np.cbrt(run.y).sum(axis=0)
        self.assertTrue(np.all(np.diff(entropy) >= -2e-13))
        self.assertLess(abs(run.y[0, -1] - run.y[1, -1]), 0.6)

    def test_equal_physical_temperature_has_no_flux_at_unequal_density(self):
        # Catches mixing K instead of the thermodynamic temperature.
        model = self.model(3)
        y = model.initial_state()
        rho = np.array([2.5, 4, 6])
        y[:3] = np.cbrt(3 * np.cumsum(model.dm / rho) / (4 * np.pi))
        W = material.density_weight(rho, self.params)
        y[6:] = W**(-1.5)
        np.testing.assert_allclose(model.fields(y)["luminosity"], 0, atol=5e-14)

    def test_dormant_cell_exactly_blocks_heat_and_stress(self):
        # Catches a one-sided or nonzero-floor face gate.
        model = self.model(3)
        y = model.initial_state()
        rho = np.array([3.0, 0.5, 3.0])
        y[:3] = np.cbrt(3 * np.cumsum(model.dm / rho) / (4 * np.pi))
        y[6:] = [0.6, 0.1, 0.2]
        fields = model.fields(y)
        np.testing.assert_array_equal(fields["luminosity"], np.zeros(4))
        self.assertEqual(fields["pressure"][1], 0)
        self.assertEqual(fields["q"][1], 0)
        self.assertEqual(fields["dk"][1], 0)

    def test_expansion_damping_heats_and_virgin_damping_is_zero(self):
        # Catches compression-only damping and spontaneous virgin memory heating.
        model = self.model(3, velocity=0.2, diffusivity=0)
        y = model.initial_state()
        y[6:] = [0, 0.1, 0.2]
        fields = model.fields(y)
        self.assertEqual(fields["q_damping"][0], 0)
        self.assertEqual(fields["dk_damping"][0], 0)
        self.assertTrue(np.all(fields["q_damping"][1:] < 0))
        self.assertTrue(np.all(fields["dk_damping"][1:] > 0))
        np.testing.assert_allclose(fields["rho"] * material.density_weight(fields["rho"], self.params)
                                   * fields["dk_damping"], -fields["q_damping"] * fields["theta"])

    def test_spatial_transport_approaches_fixed_physical_diffusivity(self):
        # A grid-dependent coefficient or missing spherical area breaks this PDE benchmark.
        errors = []
        for n in [32, 64, 128]:
            model = self.model(n, diffusivity=0.1, damping_strength=0)
            y = model.initial_state()
            r = y[:n]
            inner = np.r_[0, r[:-1]]
            # Exact volume average of K=r^2 over each spherical shell.
            y[2 * n:] = 3 / 5 * (r**5 - inner**5) / (r**3 - inner**3)
            fields = model.fields(y)
            # rho=3: W=3 and psi=3^(3/2) K; Laplacian(r^2)=6.
            expected = 0.1 * np.sqrt(3) * 6 / 3
            # Keep the physical annulus fixed. A fixed cell index approaches
            # r=0 with an unchanged relative shell geometry on equal-mass grids.
            annulus = (r > 0.5) & (r < 0.9)
            errors.append(np.max(np.abs(fields["dk_conduction"][annulus] - expected)))
        self.assertLess(errors[-1], errors[0] * 0.7)
        self.assertLess(errors[-1], 0.015)

    def test_sparse_pattern_covers_all_measured_dependencies(self):
        model = self.model(5, density=1.6, velocity=-0.8)
        y = model.initial_state()
        y[10:] = np.linspace(0.1, 0.5, 5)
        pattern = model.jacobian_sparsity().toarray().astype(bool)
        jacobian = np.empty((15, 15))
        for j in range(15):
            direction = np.zeros(15)
            direction[j] = 1e-7
            jacobian[:, j] = (model.rhs(0, y + direction) - model.rhs(0, y - direction)) / 2e-7
        self.assertTrue(np.all(jacobian[~pattern] == 0))

    def test_cold_forest_matches_original_ode_and_restarts(self):
        model = self.model(8, density=0.25, velocity=-0.25)
        original = collapse.SphericalCollapse(8, self.params)
        np.testing.assert_array_equal(model.rhs(0, model.initial_state()),
                                      original.rhs(0, original.initial_state()))
        first = transport.simulate(model, t_end=0.04, samples=3, wall_seconds=5)
        self.assertEqual(first["status"], "completed")
        second = transport.simulate(model, initial_state=first["final_state"], initial_time=0.04,
                                    t_end=0.08, samples=3, wall_seconds=5)
        whole = transport.simulate(self.model(8, density=0.25, velocity=-0.25),
                                   t_end=0.08, samples=3, wall_seconds=5)
        self.assertEqual(second["status"], "completed")
        np.testing.assert_allclose(second["final_state"], whole["final_state"], atol=1e-10)
        self.assertLess(second["max_relative_energy_error"], 1e-7)
        self.assertEqual(second["final"]["inner_5pct_min_K"], 0)

    def test_run_limit_has_noncompleted_status_and_serializable_restart(self):
        model = self.model(4)
        result = transport.simulate(model, t_end=1, samples=3, max_rhs_calls=1, wall_seconds=5)
        self.assertEqual(result["status"], "rhs_limit")
        self.assertEqual(len(result["final_state"]), 12)
        json.dumps(result, allow_nan=False)

    def test_cli_exit_reflects_internal_limit_and_writes_atomic_json(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            run = subprocess.run([sys.executable, str(HERE / "transport.py"), "--shells", "4",
                                  "--t-end", "0.1", "--max-rhs-calls", "1",
                                  "--output", str(output)], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(json.loads(output.read_text())["status"], "rhs_limit")
            self.assertEqual(list(Path(directory).iterdir()), [output])


if __name__ == "__main__":
    unittest.main()
