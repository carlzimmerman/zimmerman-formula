"""Observation-only floor sampling and explicitly prepared restart states."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import convective_transport as convective

try:
    import refinement
except ModuleNotFoundError:
    refinement = None


class RefinementTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(refinement, "fixed-mass floor observer is absent")
        self.params = convective.baseline.material.MaterialParameters(1, np.sqrt(8 * np.pi), 1, 0.5)

    def test_observer_leaves_rhs_and_energy_exactly_unchanged(self):
        # An unintended force/source override would break bitwise equality.
        observer = refinement.FloorAuditedCollapse(8, self.params, initial_density=3,
                                                  initial_velocity_gradient=-0.8)
        baseline = convective.ConvectiveCollapse(8, self.params, initial_density=3,
                                                 initial_velocity_gradient=-0.8)
        y = observer.initial_state()
        y[16:] = np.linspace(0.5, 0.1, 8)
        np.testing.assert_array_equal(observer.rhs(0, y), baseline.rhs(0, y))
        self.assertEqual(observer.energy(y), baseline.energy(y))
        observer.diagnostics(0, y)
        np.testing.assert_array_equal(observer.rhs(0, y), baseline.rhs(0, y))

    def test_guard_mapping_distinguishes_partial_cells_and_exact_boundaries(self):
        # Catches selecting the partially included cell itself as its own guard.
        partial = refinement.prefix_mapping(32, 0.05)
        self.assertEqual(partial["included_cell_count"], 2)
        self.assertEqual(partial["last_included_cell_index"], 1)
        self.assertEqual(partial["guard_cell_index"], 2)
        self.assertFalse(partial["exact_cell_boundary"])
        self.assertAlmostEqual(partial["last_included_cell_fraction"], 0.6)
        self.assertEqual(partial["guard_inner_mass_fraction"], 2 / 32)
        exact = refinement.prefix_mapping(100, 0.05)
        self.assertEqual(exact["included_cell_count"], 5)
        self.assertEqual(exact["guard_cell_index"], 5)
        self.assertTrue(exact["exact_cell_boundary"])
        self.assertEqual(exact["last_included_cell_fraction"], 1)
        # Binary multiplication gives 7.000000000000001 for this decimal pair.
        self.assertEqual(refinement.prefix_mapping(50, 0.14)["guard_cell_index"], 7)

    def test_sample_arrays_and_prefix_minima_include_zeros(self):
        # Catches dropping zero K or averaging a guard instead of sampling it.
        model = refinement.FloorAuditedCollapse(32, self.params, initial_density=3,
                                               initial_velocity_gradient=0)
        y = model.initial_state()
        y[64:] = np.arange(32) / 100
        row = model.diagnostics(0, y)
        self.assertEqual(row["K_by_cell"], y[64:].tolist())
        self.assertEqual(row["r_by_cell"], y[:32].tolist())
        np.testing.assert_allclose(row["rho_by_cell"], 3, rtol=1e-13)
        self.assertEqual(row["min_all_K"], 0)
        self.assertEqual(row["prefix_5pct_min_K"], 0)
        self.assertEqual(row["K_guard_5pct"], 0.02)
        self.assertEqual(row["floor_prefixes"]["5pct"]["guard_cell_index"], 2)
        self.assertEqual(row["K_guard_25pct"], 0.08)

    def test_prepared_restart_preserves_K_and_accounts_for_all_energy_changes(self):
        # Catches hidden energy injection or changing mass/K during a radius kick.
        model = refinement.FloorAuditedCollapse(8, self.params, initial_density=3,
                                               initial_velocity_gradient=0)
        y = model.initial_state()
        y[16:] = 0.2
        original = y.copy()
        radius_factor, gradient = 1.1, 0.1
        before = model.energy(y)
        prepared, audit = refinement.prepare_restart_state(
            model, y, radius_factor=radius_factor, velocity_gradient=gradient)
        np.testing.assert_array_equal(y, original)
        np.testing.assert_array_equal(prepared[16:], original[16:])
        np.testing.assert_allclose(prepared[:8], radius_factor * original[:8])
        np.testing.assert_allclose(prepared[8:16], gradient * prepared[:8])
        expected_kinetic = float(np.sum(0.5 * model.mu * (gradient * radius_factor * original[:8])**2))
        self.assertAlmostEqual(audit["delta_energy"]["kinetic"], expected_kinetic, places=13)
        self.assertAlmostEqual(audit["delta_energy"]["gravitational"],
                               before["gravitational"] * (1 / radius_factor - 1), places=12)
        self.assertAlmostEqual(audit["delta_energy"]["internal"],
                               before["internal"] * (1 / radius_factor**3 - 1), places=12)
        self.assertAlmostEqual(audit["delta_total_energy"], sum(audit["delta_energy"][key]
                               for key in ("internal", "kinetic", "gravitational")), places=12)
        self.assertTrue(audit["K_preserved_exactly"])

    def test_observer_serialization_keeps_closure_and_every_sample_array(self):
        model = refinement.FloorAuditedCollapse(4, self.params)
        result = refinement.simulate(model, t_end=0.01, samples=3, wall_seconds=5)
        self.assertEqual(result["closure"], convective.CLOSURE)
        self.assertEqual(result["observer"]["name"], "fixed_mass_prefix_floor")
        self.assertEqual(result["status"], "completed")
        for row in result["time_history"]:
            self.assertEqual(len(row["K_by_cell"]), 4)
            self.assertEqual(len(row["rho_by_cell"]), 4)
            self.assertEqual(len(row["r_by_cell"]), 4)
        json.dumps(result, allow_nan=False)

    def test_unheated_dense_expansion_keeps_exact_cold_invariant(self):
        # The coupled 3N sparse LU leaks roundoff into K even when Kdot=0.
        model = refinement.FloorAuditedCollapse(24, self.params, initial_density=1.5,
                                               initial_velocity_gradient=2)
        y = model.initial_state()
        y[:24] *= 1 + 0.01 * np.sin(np.pi * y[:24])
        y[24:48] = 2 * y[:24]
        result = refinement.simulate(model, initial_state=y, t_end=0.05,
                                     samples=6, wall_seconds=5)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["cold_phase"]["status"], "completed_without_activation")
        self.assertEqual(result["accepted_negative_memory_rejections"], 0)
        np.testing.assert_array_equal(result["final_profile"]["K"], np.zeros(24))
        for row in result["time_history"]:
            np.testing.assert_array_equal(row["K_by_cell"], np.zeros(24))

    def test_cold_subspace_hands_off_at_physical_activation_without_K_seed(self):
        model = refinement.FloorAuditedCollapse(8, self.params)
        result = refinement.simulate(model, t_end=0.7, samples=9, wall_seconds=5)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["cold_phase"]["status"], "activation_handoff")
        self.assertTrue(result["cold_phase"]["handoff_K_exactly_zero"])
        self.assertLess(abs(result["cold_phase"]["activation_indicator_at_handoff"]), 1e-10)
        self.assertGreater(result["final"]["max_K"], 0)
        self.assertLess(result["max_relative_energy_error"], 2e-6)
        self.assertEqual(result["t_initial"], 0)
        self.assertEqual(result["time_history"][0]["t"], 0)
        self.assertEqual(result["time_history"][-1]["t"], 0.7)
        self.assertTrue(np.all(np.diff([row["t"] for row in result["time_history"]]) > 0))

    def test_cold_phase_respects_total_rhs_limit(self):
        model = refinement.FloorAuditedCollapse(4, self.params)
        result = refinement.simulate(model, t_end=1, samples=3, wall_seconds=5, max_rhs_calls=1)
        self.assertEqual(result["status"], "rhs_limit")
        self.assertLess(result["t_reached"], 1)
        self.assertEqual(result["rhs_cap"], 1)
        np.testing.assert_array_equal(result["final_profile"]["K"], np.zeros(4))

    def test_cli_logs_preparation_and_rejects_perturbation_without_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / "original.json"
            output = Path(directory) / "prepared.json"
            base_model = convective.ConvectiveCollapse(4, self.params)
            base_result = convective.simulate(base_model, t_end=0.01, samples=3, wall_seconds=5)
            original.write_text(json.dumps(base_result))
            common = [sys.executable, str(HERE / "refinement.py"), "--shells", "4",
                      "--t-end", "0.02", "--samples", "3", "--wall-seconds", "5",
                      "--perturb-radius-factor", "1.01", "--perturb-velocity-gradient", "0.02"]
            run = subprocess.run(common + ["--restart", str(original), "--output", str(output)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result["closure"], convective.CLOSURE)
            self.assertEqual(result["transport_parameters"], base_result["transport_parameters"])
            self.assertEqual(result["preparation"]["radius_factor"], 1.01)
            self.assertEqual(result["preparation"]["velocity_gradient_added"], 0.02)
            self.assertEqual(result["preparation"]["prepared_energy"]["total"], result["initial"]["total"])
            self.assertEqual(result["t_initial"], 0.01)
            rejected_output = Path(directory) / "rejected.json"
            rejected = subprocess.run(common + ["--output", str(rejected_output)],
                                      capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertFalse(rejected_output.exists())


if __name__ == "__main__":
    unittest.main()
