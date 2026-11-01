"""Short independent-integrator comparisons for fixed-law warm continuation."""

from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import refinement

try:
    import bdf_continuation
except ModuleNotFoundError:
    bdf_continuation = None


class BDFContinuationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(bdf_continuation, "independent BDF continuation is absent")
        self.params = refinement.convective.baseline.material.MaterialParameters(
            1, np.sqrt(8 * np.pi), 1, 0.5)

    def warm_model(self):
        model = refinement.FloorAuditedCollapse(8, self.params, initial_density=3,
                                               initial_velocity_gradient=-0.2)
        state = model.initial_state()
        state[16:] = np.linspace(0.5, 0.2, 8)
        return model, state

    def test_BDF_agrees_with_Radau_on_active_warm_dynamics(self):
        # A changed RHS, solver-state slicing, or incorrect time origin fails this.
        model, state = self.warm_model()
        settings = dict(initial_state=state, initial_time=2.0, t_end=2.04,
                        samples=5, rtol=2e-9, atol=1e-11, wall_seconds=5)
        bdf = bdf_continuation.simulate(model, **settings)
        radau_model, _ = self.warm_model()
        radau = refinement.simulate(radau_model, **settings)
        self.assertEqual(bdf["status"], "completed")
        self.assertEqual(radau["status"], "completed")
        self.assertEqual(bdf["method"], "BDF")
        np.testing.assert_allclose(bdf["final_state"], radau["final_state"], rtol=2e-7, atol=5e-9)
        self.assertLess(bdf["max_relative_energy_error"], 1e-7)
        self.assertGreaterEqual(bdf["minimum_accepted_K"], 0)
        self.assertLess(bdf["max_single_step_entropy_decrease"], 1e-12)
        self.assertGreater(bdf["final"]["total_entropy"], bdf["initial"]["total_entropy"])
        self.assertGreater(bdf["accepted_step_statistics"]["maximum_order"], 1)

    def test_exactly_cold_start_is_rejected_instead_of_clipped_or_seeded(self):
        model, state = self.warm_model()
        state[16] = 0
        with self.assertRaisesRegex(ValueError, "strictly positive"):
            bdf_continuation.simulate(model, initial_state=state, initial_time=0, t_end=0.1)

    def test_rhs_limit_preserves_last_accepted_state_and_is_serializable(self):
        model, state = self.warm_model()
        result = bdf_continuation.simulate(model, initial_state=state, initial_time=2,
                                           t_end=3, samples=3, max_rhs_calls=1, wall_seconds=5)
        self.assertEqual(result["status"], "rhs_limit")
        self.assertEqual(result["t_reached"], 2)
        np.testing.assert_array_equal(result["final_state"], state)
        json.dumps(result, allow_nan=False)

    def test_restart_reconstruction_preserves_mass_and_rejects_changed_law(self):
        model, state = self.warm_model()
        previous = refinement.simulate(model, initial_state=state, t_end=0.01,
                                        samples=3, wall_seconds=5)
        reconstructed = bdf_continuation.model_from_restart(previous)
        self.assertEqual(reconstructed.dm, model.dm)
        self.assertEqual(asdict(reconstructed.transport), previous["transport_parameters"])
        changed = dict(previous, transport_parameters=dict(previous["transport_parameters"], diffusivity=0.2))
        with self.assertRaisesRegex(ValueError, "fixed"):
            bdf_continuation.model_from_restart(changed)

    def test_cli_reports_actual_BDF_and_resource_failure_exit(self):
        model, state = self.warm_model()
        previous = refinement.simulate(model, initial_state=state, t_end=0.01,
                                        samples=3, wall_seconds=5)
        with tempfile.TemporaryDirectory() as directory:
            restart = Path(directory) / "restart.json"
            output = Path(directory) / "result.json"
            restart.write_text(json.dumps(previous))
            command = [sys.executable, str(HERE / "bdf_continuation.py"), "--restart", str(restart),
                       "--t-end", "0.02", "--samples", "3", "--wall-seconds", "5", "--output", str(output)]
            completed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result["method"], "BDF")
            self.assertEqual(result["closure"], refinement.convective.CLOSURE)
            self.assertEqual(result["initial"]["K_by_cell"], previous["final_profile"]["K"])
            self.assertEqual(result["continuation"]["restart_time"], 0.01)
            limited = subprocess.run(command + ["--max-rhs-calls", "1"], capture_output=True, text=True)
            self.assertNotEqual(limited.returncode, 0)
            self.assertEqual(json.loads(output.read_text())["status"], "rhs_limit")


if __name__ == "__main__":
    unittest.main()
