"""Tests of the covariant operator map, not a full-gravity certificate."""
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


class CurvatureOperatorBridgeTests(unittest.TestCase):
    def model(self):
        global _MODULE
        path = HERE / "curvature_operator_bridge.py"
        self.assertTrue(path.exists(), "Missing covariant source-operator bridge")
        if _MODULE is None:
            spec = importlib.util.spec_from_file_location("curvature_operator_bridge", path)
            _MODULE = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_MODULE)
        return _MODULE

    def test_physical_measure_and_rhat_give_actual_quadratic_map(self):
        d = self.model().geometry()
        expected = 16*d["ell"]**2/3
        self.assertEqual(s.factor(d["map_factor"]-expected), 0)
        self.assertEqual(d["mapping_residual"], 0)
        self.assertEqual(d["ricci_linear_residual"], 0)

    def test_full_density_second_variation_keeps_no_velocity_or_shift(self):
        d = self.model().geometry()
        self.assertEqual(d["quadratic_velocity_residuals"], [0]*4)
        self.assertEqual(d["measure_residual"], 0)

    def test_point_map_removes_both_auxiliary_velocities(self):
        d = self.model().geometry()
        self.assertEqual(d["point_map_residuals"], [0]*9)
        self.assertEqual(d["Q_auxiliary_velocity_residuals"], [0, 0])

    def test_claimed_branch_transfers_are_first_variation_identities(self):
        d = self.model().geometry()
        self.assertEqual(d["static_first_variation"], [0]*4)
        self.assertEqual(d["witness_first_variation"], [0]*4)
        self.assertEqual(d["pure_TT_correction"], 0)

    def test_spatial_integration_by_parts_is_an_actual_divergence(self):
        d = self.model().spatial_ibp()
        self.assertEqual(d["divergence_residual"], 0)
        self.assertEqual(d["auxiliary_velocity_residuals"], [0, 0])

    def test_corrected_raw_action_solves_all_three_constraints(self):
        d = self.model().reduction()
        self.assertEqual(d["constraint_residuals"], [0]*3)
        self.assertEqual(d["source_matching_residual"], 0)
        self.assertEqual(d["bridge_to_action_residual"], 0)

    def test_constructed_local_lapse_and_auxiliary_are_derived(self):
        d = self.model().reduction()
        T,y = d["T"],d["y"]
        self.assertEqual(s.factor(d["lapse"]-(s.Rational(1,2)+27/(16*T))*y), 0)
        self.assertEqual(s.factor(d["auxiliary"]-9*y/(2*T)), 0)
        self.assertEqual(s.factor(d["a"]-(3-81/(4*T))), 0)

    def test_complete_nonzero_mode_frequency_is_polynomial(self):
        d = self.model().reduction()
        self.assertEqual(s.factor(d["frequency_squared"]-d["speed"]*d["x"]), 0)
        self.assertTrue(d["kinetic_positive"])
        self.assertTrue(d["frequency_positive_for_x_positive"])
        self.assertEqual(d["time_IBP_residual"], 0)

    def test_physical_clock_obeys_derived_local_second_order_equation(self):
        d = self.model().reduction()
        self.assertEqual(d["clock_equation_residual"], 0)
        self.assertEqual(d["z_equation_residual"], 0)

    def test_default_json_and_unproved_full_gate_are_separate(self):
        module = self.model()
        result = module.run()
        json.dumps(result, allow_nan=False)
        self.assertTrue(result["checks_passed"])
        self.assertFalse(result["full_theory_closed"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main([]), 0)
            self.assertEqual(module.main(["--require-full-closure"]), 2)

    def test_failed_algebra_returns_one(self):
        module = self.model()
        result = module.run()
        result["checks_passed"] = False
        with patch.object(module, "run", return_value=result):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.main([]), 1)


if __name__ == "__main__":
    unittest.main()
