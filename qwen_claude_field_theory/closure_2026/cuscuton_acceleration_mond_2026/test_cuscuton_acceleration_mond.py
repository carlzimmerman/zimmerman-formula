"""Regression tests for the constructive cuscuton/acceleration branch."""

import unittest
import sympy as sp

from cuscuton_acceleration_mond_gate import (
    CHECKS,
    dirac_auxiliary,
    static_variation,
    tensor_compensator_variation,
)
from kepler_prediction_gate import derive_prediction
from clock_principal_gate import derive_clock_symbol
from eh_static_reduction_gate import derive_eh_static


class CuscutonAccelerationMondTests(unittest.TestCase):
    def test_static_action_variation(self):
        data = static_variation()
        self.assertEqual(data["q_identity"], 0)
        self.assertEqual(data["flux_residual"], 0)
        self.assertEqual(data["aqual_residual"], 0)
        self.assertEqual(
            data["slip_equation"],
            sp.diff(data["fields"]["Phi"], data["coordinate"], 2)
            - sp.diff(data["fields"]["Psi"], data["coordinate"], 2),
        )

    def test_finite_k_auxiliary_dirac(self):
        result = dirac_auxiliary("k_nonzero")
        self.assertEqual(result.bracket.rank(), result.second_class)
        self.assertEqual(float(result.physical_dof), 0.0)
        self.assertGreaterEqual(len(result.constraints), len(result.primaries))

    def test_zero_mode_is_separate(self):
        result = dirac_auxiliary("k_zero")
        self.assertEqual(result.mode, "k_zero")
        self.assertNotEqual(result.mode, "k_nonzero")

    def test_trace_free_compensator(self):
        data = tensor_compensator_variation()
        self.assertEqual(data["constraint_residual"], 0)
        self.assertEqual(data["metric_residual"], 0)

    def test_circular_orbit_prediction(self):
        data = derive_prediction()
        self.assertIn("exp", str(data["implicit_circular_law"]))
        self.assertEqual(
            sp.expand(data["v4_over_GMa0_series"]).coeff(
                next(iter(data["v4_over_GMa0_series"].free_symbols)), 1
            ),
            sp.Rational(1, 2),
        )

    def test_clock_principal_symbol(self):
        data = derive_clock_symbol()
        self.assertEqual(
            data["delta_acceleration"],
            -sp.diff(data["symbols"]["pi"],
                     next(v for v in data["delta_acceleration"].free_symbols
                          if str(v) == "t"),
                     next(v for v in data["delta_acceleration"].free_symbols
                          if str(v) == "x")),
        )
        self.assertEqual(data["cuscuton_quadratic"].has(
            sp.diff(data["symbols"]["pi"], next(
                v for v in data["cuscuton_quadratic"].free_symbols
                if str(v) == "t"))), False)

    def test_eh_static_reduction_is_a_real_obstruction(self):
        data = derive_eh_static()
        M2 = data["symbols"]["M2"]
        Phi = data["symbols"]["Phi"]
        x = data["symbols"]["x"]
        self.assertEqual(
            sp.simplify(data["discrepancy"] - M2 * sp.diff(Phi, x) ** 2), 0
        )
        self.assertNotEqual(data["cam_eh_density"], data["eh_density_ibp"])


if __name__ == "__main__":
    unittest.main()
