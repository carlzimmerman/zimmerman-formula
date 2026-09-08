"""IC-3 repair identities: tests do not certify nonlinear gravity."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import sympy as s

HERE = Path(__file__).resolve().parent
_MODULE = None


class ClockLocalityCompletionTests(unittest.TestCase):
    def model(self):
        global _MODULE
        path = HERE / "clock_locality_completion.py"
        self.assertTrue(path.exists(), "Missing constructive clock-locality calculation")
        if _MODULE is None:
            spec = importlib.util.spec_from_file_location("clock_locality_completion", path)
            _MODULE = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_MODULE)
        return _MODULE

    def test_actual_raw_action_eliminates_all_auxiliary_fields(self):
        d = self.model().derive()
        self.assertEqual(d["constraint_residuals"], [0, 0, 0])
        self.assertEqual(d["raw_reduction_residuals"], [0, 0, 0, 0])

    def test_matching_families_come_from_clock_pole_divisibility(self):
        d = self.model().derive()
        T, r = d["T"], d["ratio"]
        expected = (T*r+9)*((8*T+27)*r+108)
        self.assertEqual(s.factor(d["matching_polynomial"]-expected), 0)
        self.assertEqual(set(d["matching_roots"]), {-9/T, -108/(8*T+27)})

    def test_constructed_action_has_constant_positive_scalar_kinetic(self):
        d = self.model().candidate()
        T, x = d["T"], d["x"]
        self.assertEqual(s.factor(d["a"]-(3-81/(4*T))), 0)
        self.assertEqual(s.diff(d["a"], x), 0)
        self.assertTrue(d["kinetic_positive"])
        self.assertTrue(d["e_positive"])
        self.assertEqual(d["uv_physical_speed_squared"], s.Rational(1, 3))

    def test_action_coefficients_reproduce_selected_alpha_d_e(self):
        d = self.model().candidate()
        self.assertEqual(d["action_mapping_residuals"], [0, 0, 0])
        self.assertEqual(d["constitutive_matching_residuals"], [0, 0])

    def test_velocity_data_clock_slope_is_now_polynomial(self):
        d = self.model().candidate()
        self.assertTrue(d["velocity_slope_local"])
        self.assertEqual(d["velocity_pole_residual"], 0)
        self.assertTrue(d["velocity_initial_data_local"])

    def test_complete_clock_readout_retains_position_data_pole(self):
        d = self.model().candidate()
        T, x, D = d["T"], d["x"], d["D"]
        self.assertEqual(s.factor(d["position_tail"]-3*T*x*x/(8*D)), 0)
        self.assertFalse(d["position_slope_local"])
        self.assertTrue(d["position_initial_data_local"])
        self.assertTrue(d["position_tail_coefficient_positive"])

    def test_initial_momenta_restore_the_local_time_boundary_term(self):
        d = self.model().candidate()
        expected = (d["b"]-18)*d["D"]*d["x"]
        self.assertEqual(s.factor(d["position_initial_data"]["trace_momentum"]-expected), 0)

    def test_second_family_repairs_both_initial_clock_slopes(self):
        module = self.model()
        self.assertTrue(hasattr(module, "second_family"), "Missing second constructive family")
        d = module.second_family()
        self.assertTrue(d["velocity_first_local"])
        self.assertTrue(d["position_first_local"])
        self.assertTrue(d["kinetic_positive"])

    def test_second_family_next_condition_is_computed_not_assumed(self):
        module = self.model()
        self.assertTrue(hasattr(module, "second_family"), "Missing complete clock differentiation")
        d = module.second_family()
        self.assertFalse(d["velocity_second_local"])
        self.assertTrue(d["velocity_second_residue_positive"])
        self.assertEqual(d["compatible_e_for_both_second_slopes"], [])

    def test_exact_zero_mode_is_reported_separately(self):
        d = self.model().run()
        self.assertIn("uniform", d)
        self.assertFalse(d["full_theory_closed"])
        self.assertFalse(d["clock_locality_completed"])
        json.dumps(d, allow_nan=False)
        self.assertTrue(d["checks_passed"])

    def test_cli_is_fail_closed_for_missing_full_locality(self):
        module = self.model()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main([]), 0)
            self.assertEqual(module.main(["--require-clock-locality"]), 2)
            self.assertEqual(module.main(["--require-full-closure"]), 2)

    def test_cli_returns_one_for_failed_algebra(self):
        module = self.model()
        result = module.run()
        result["checks_passed"] = False
        with patch.object(module, "run", return_value=result):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.main([]), 1)


if __name__ == "__main__":
    unittest.main()
