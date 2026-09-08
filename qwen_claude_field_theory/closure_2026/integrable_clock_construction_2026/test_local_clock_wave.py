"""Behavior tests of a same-action scalar-wave construction, not full gravity."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest

import sympy as s

MODEL = None


class LocalClockWaveTests(unittest.TestCase):
    def model(self):
        global MODEL
        path = Path(__file__).with_name("local_clock_wave.py")
        self.assertTrue(path.exists(), "The action-derived local-wave calculation is missing")
        if MODEL is None:
            spec = importlib.util.spec_from_file_location("tested_local_clock_wave", path)
            MODEL = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(MODEL)
        return MODEL

    def test_full_density_derivative_gives_the_curvature_coupling(self):
        d = self.model().derive()
        self.assertEqual(s.factor(d["coupling_factor"]-16*d["ell"]**2/3), 0)
        self.assertEqual(d["density_residual"], 0)

    def test_compatibility_is_solved_from_both_field_equations(self):
        d = self.model().derive()
        self.assertEqual(d["constraint_residuals"], [0, 0, 0])
        self.assertEqual(s.factor(d["selected_q"]+1+3*d["selected_p"]/8), 0)
        self.assertEqual(s.diff(d["solutions"][d["v"]], d["z"]), 0)

    def test_positive_constant_kinetic_is_derived_from_reduced_action(self):
        d = self.model().derive()
        self.assertEqual(s.factor(d["a"]-3+81/(4*d["T"])), 0)
        self.assertEqual(s.diff(d["a"], d["x"]), 0)
        self.assertTrue(d["kinetic_positive"])

    def test_wave_speed_uses_physical_time_and_scale(self):
        d = self.model().derive()
        self.assertEqual(s.factor(d["physical_speed_squared"]-d["target_speed_squared"]), 0)
        self.assertEqual(s.factor(d["g"]+d["a"]*d["target_speed_squared"]*d["x"]), 0)
        self.assertEqual(d["friction"], 3)

    def test_lapse_and_auxiliary_are_local_in_reduced_canonical_data(self):
        d = self.model().derive()
        self.assertTrue(all(d["canonical_readouts_local"].values()))
        self.assertEqual(d["clock_wave_residual"], 0)
        self.assertEqual(d["energy_residual"], 0)

    def test_zero_mode_is_varied_separately_and_not_silently_identified(self):
        d = self.model().derive()
        self.assertNotEqual(s.factor(d["zero_a"]-d["a"]), 0)
        self.assertEqual(d["zero_lapse_canonical_match"], 0)
        self.assertEqual(d["zero_aux_canonical_match"], 0)

    def test_static_homogeneous_and_tensor_transfers_have_zero_jets(self):
        d = self.model().derive()
        self.assertTrue(all(v == 0 for v in d["bridge_residuals"].values()))

    def test_exact_mode_functions_satisfy_the_derived_evolution(self):
        d = self.model().derive()
        self.assertEqual(d["mode_function_residuals"], [0, 0])

    def test_wave_packet_map_reconstructs_shift_without_a_spatial_inverse(self):
        d = self.model().derive()
        self.assertIn("packet", d, "Missing local physical wave-packet reconstruction")
        self.assertTrue(all(value == 0 for value in d["packet"]["residuals"].values()))
        self.assertTrue(all(d["packet"]["differential_readouts"].values()))

    def test_numerical_transfer_has_independent_analytic_and_refinement_controls(self):
        d = self.model().numerical()
        self.assertTrue(d["all_integrations_succeeded"])
        self.assertLess(d["maximum_scaled_analytic_error"], 1e-7)
        self.assertLess(d["maximum_scaled_refinement_error"], 1e-7)
        self.assertLess(d["maximum_relative_energy_increase"], 1e-8)

    def test_full_theory_gate_stays_open_despite_a_verified_linear_wave(self):
        model = self.model()
        d = model.run()
        json.dumps(d, allow_nan=False)
        self.assertTrue(d["exact_checks_passed"])
        self.assertFalse(d["full_theory_closed"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(model.main([]), 0)
            self.assertEqual(model.main(["--require-full-closure"]), 2)


if __name__ == "__main__":
    unittest.main()
