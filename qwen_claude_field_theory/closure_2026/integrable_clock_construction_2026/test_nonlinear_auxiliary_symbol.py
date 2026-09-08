#!/usr/bin/env python3
"""Independent exact controls for the bounded nonlinear IC-4 symbol audit."""
import importlib.util
import json
from pathlib import Path
import unittest

import sympy as s

SOURCE = Path(__file__).with_name("nonlinear_auxiliary_symbol.py")
MODULE = None
if SOURCE.exists():
    spec = importlib.util.spec_from_file_location("nonlinear_auxiliary_symbol_tested", SOURCE)
    MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MODULE)


class NonlinearAuxiliarySymbolTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MODULE, "The nonlinear Hamiltonian derivation is not implemented")
        self.d = MODULE.derive()

    def assertZero(self, value):
        values = list(value) if isinstance(value, s.MatrixBase) else [value]
        self.assertTrue(all(s.simplify(v) == 0 for v in values), str(value))

    def test_actual_rational_hamiltonian_gradient_differentiation(self):
        # Catches a missing 1/t^2 factor, wrong Legendre sign, or TF contamination.
        d = self.d
        A, B, C, xi, u, rho = [d[k] for k in ("A_J", "B_J", "C_J", "xi", "u", "rho")]
        expected = -d["Dplus"] * s.Matrix([[2*rho*A, rho*B+4*u*xi],
                                                [rho*B+4*u*xi, 2*rho*C+4*xi**2]])
        self.assertZero(d["gradient_hessian"]-expected)
        self.assertZero(d["gradient_hessian"].diff(d["piTF2"]))
        self.assertZero(d["gradient_hessian"].diff(d["F_curvature"]))

    def test_witness_normalization_and_square_direction(self):
        # Catches using the Lagrangian symbol with the wrong Hamiltonian sign.
        d = self.d
        T = d["T"]
        expected = s.Matrix([[s.Rational(81,4)/T**2, -9*(8*T+27)/(32*T**2)],
                             [-9*(8*T+27)/(32*T**2), (8*T+27)**2/(256*T**2)]])
        self.assertZero(d["G_witness"]-expected)
        self.assertZero(d["square_slope"]+T/9+s.Rational(3,8))
        self.assertZero(d["G_witness"]*s.Matrix([-d["square_slope"],1]))
        self.assertZero(d["witness_normalization_residual"])

    def test_true_quadratic_auxiliary_hessian_not_only_velocity_block(self):
        # Catches conflating the degenerate spatial symbol with the full matrix.
        d = self.d
        T, x = d["T"], d["x"]
        mass = s.Matrix([[24,-27],[-27,2*T+s.Rational(135,8)]])
        self.assertZero(d["quadratic_M"]-mass-x*d["G_witness"])
        self.assertZero(d["quadratic_bridge_residual"])
        self.assertZero(d["quadratic_M"].det()-3*(4*T-27)*(8*T+x)/(2*T))
        self.assertGreater(float(d["quadratic_M"].det().subs({T:9,x:1})), 0)

    def test_independent_trace_and_field_deviations_break_witness_null(self):
        # These hand-computed T=9 controls include rho's field dependence.
        values = {"trace_ratio":s.Rational(-25,48), "xi":s.Rational(31,48),
                  "u":s.Rational(47,64)}
        for key, expected in values.items():
            self.assertZero(self.d["determinant_derivatives"][key].subs(self.d["T"],9)-expected)

    def test_static_symbol_is_not_a_rank_one_square_generically(self):
        # Catches silently extending the expanding null direction to pi=0.
        d = self.d
        self.assertZero(d["static_normalized_determinant"]+4*d["u"]**2*d["xi"]**2)
        self.assertEqual(d["static_normalized_determinant"].subs({d["u"]:s.Rational(2,3),
                                                                  d["xi"]:s.Rational(1,4)}), -s.Rational(1,9))

    def test_required_coefficient_identity_and_exact_square_completion(self):
        # Catches preserving only a linear-in-Z truncation but calling it exact.
        d = self.d
        A, B, xi, u, rho = [d[k] for k in ("A_J", "B_J", "xi", "u", "rho_symbol")]
        expected = (B+4*u*xi/rho)**2/(4*A)-2*xi**2/rho
        self.assertZero(d["required_C_J"]-expected)
        self.assertZero(d["required_identity_residual"])
        self.assertZero(d["exact_square_completion_residual"])
        self.assertZero(d["exact_completion_linear_jet_residual"])

    def test_square_patch_matches_witness_and_vanishes_on_homogeneous_fields(self):
        # Catches changing the IC-4 quadratic jet or flat homogeneous reduction.
        d = self.d
        self.assertZero(d["square_matching_residual"])
        self.assertZero(d["homogeneous_correction_residual"])
        self.assertZero(d["homogeneous_first_variations"])
        self.assertZero(d["square_principal_determinant"])

    def test_poisson_principal_sign_from_functional_second_variation(self):
        # Catches the extra minus sign between H_qq and {secondary,p}.
        self.assertZero(self.d["secondary_primary_fourier_symbol"]
                        +self.d["wave_number_squared"]*self.d["gradient_hessian"])

    def test_json_result_contains_computed_residuals_not_unproved_count(self):
        result = MODULE.run()
        json.dumps(result)
        self.assertTrue(result["input_hashes_match"])
        self.assertTrue(result["exact_checks_passed"])
        self.assertGreaterEqual(len(result["exact_residuals"]), 12)
        self.assertFalse(result["full_nonlinear_closure_proved"])


if __name__ == "__main__":
    unittest.main()
