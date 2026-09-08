"""Tests of the IC-2 finite-band bound and numerical fundamental matrix."""
import importlib.util
import json
from pathlib import Path
import unittest

import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
_MODEL = None


class IRGrowthTests(unittest.TestCase):
    def model(self):
        global _MODEL
        path = HERE / "ir_growth.py"
        self.assertTrue(path.exists(), "The finite-growth calculation is not implemented")
        if _MODEL is None:
            spec = importlib.util.spec_from_file_location("ir_growth", path)
            _MODEL = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_MODEL)
        return _MODEL

    def test_damping_comes_from_the_imported_kinetic_coefficient(self):
        d = self.model().derive()
        x, D = d["x"], d["d0"]
        expected = 3-108*x/((D+x)*(D+x-54))
        self.assertEqual(s.factor(d["damping"]-expected), 0)
        self.assertEqual(d["residuals"]["damping_square"], 0)

    def test_growth_primitive_differentiates_to_the_actual_force(self):
        d = self.model().derive()
        self.assertIn("stable_growth_primitive",d["residuals"],"The numerical log1p form needs an exact control")
        self.assertEqual(s.factor(s.diff(d["Gamma"],d["x"])-d["force"]/(4*d["x"])), 0)
        self.assertEqual(s.simplify(d["Gamma"].subs(d["x"],0)), 0)
        self.assertEqual(d["residuals"]["stable_growth_primitive"],0)

    def test_uniform_bound_has_exact_positive_certificates(self):
        d = self.model().derive()
        self.assertTrue(d["damping_positive_expression"].is_positive)
        self.assertTrue(d["force_upper_difference"].is_positive)
        self.assertGreater(d["uniform_bound_numeric"], 1)
        self.assertLess(d["uniform_bound_numeric"], 4.24)

    def test_physical_fields_are_reconstructed_from_the_same_constraints(self):
        d = self.model().derive()
        self.assertEqual(d["residuals"]["lapse_constraint"], 0)
        self.assertEqual(d["residuals"]["auxiliary_constraint"], 0)
        self.assertEqual(d["residuals"]["physical_curvature"], 0)
        self.assertEqual(d["residuals"]["physical_zeta"], 0)

    def test_future_velocity_bound_is_a_supersolution(self):
        d = self.model().derive()
        self.assertEqual(d["residuals"]["velocity_envelope"], 0)
        self.assertEqual(d["residuals"]["position_tail"], 0)

    def test_zero_x_control_is_not_a_claim_about_the_genuine_zero_mode(self):
        model = self.model()
        result = model.fundamental(0.0, tau_end=4.0, samples=81)
        t = result["times"]
        expected = np.zeros_like(result["matrices"])
        expected[:,0,0] = 1
        expected[:,0,1] = -np.expm1(-3*t)/3
        expected[:,1,1] = np.exp(-3*t)
        self.assertLess(np.max(np.abs(result["matrices"]-expected)), 1e-9)

    def test_numerical_inputs_do_not_silently_leave_the_proved_band(self):
        model = self.model()
        with self.assertRaises(ValueError):
            model.fundamental(-1)
        with self.assertRaises(ValueError):
            model.fundamental(2*model.derive()["x_star_numeric"])
        with self.assertRaises(ValueError):
            model.fundamental(1,tau_end=0)

    def test_fundamental_matrix_refinement_respects_the_uniform_bound(self):
        d = self.model().numerical()
        self.assertTrue(d["all_integrations_succeeded"])
        self.assertLess(d["max_refinement_difference"], 1e-7)
        self.assertLess(d["max_envelope_excess"], 1e-7)
        self.assertLess(d["max_early_wronskian_error"], 1e-7)
        self.assertGreater(d["max_weighted_transfer_norm"], 1)

    def test_report_is_json_safe_and_does_not_certify_full_closure(self):
        d = self.model().run()
        json.dumps(d,allow_nan=False)
        self.assertTrue(d["exact_checks_passed"])
        self.assertTrue(d["input_hash_matches"])
        self.assertIn("numerical_consistency_passed",d,"Finite numerical tolerances need an executed status")
        self.assertTrue(d["numerical_consistency_passed"])
        self.assertFalse(d["full_theory_closed"])
        self.assertFalse(d["physical_causality_proved"])


if __name__ == "__main__":
    unittest.main()
