"""Controls for the extended-cuscuton lapse-constraint discriminator."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

import sympy as s


class CuscutonScreenTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("cuscuton_screen"),
                             "The cuscuton discriminator has not been implemented")
        import cuscuton_screen
        return cuscuton_screen

    def test_off_diagonal_metric_coordinate_has_twice_tensor_momentum(self):
        # Dropping either symmetric K12 entry changes this hand-computed fixture.
        d = self.module().derive_seed()
        fixture = {d["N"]: 3, d["A4"]: -2,
                   **dict(zip(d["scales"], [2, 3, 5])),
                   **dict.fromkeys(d["velocities"], 0)}
        fixture[d["velocities"][3]] = 7
        self.assertEqual(d["raw_momenta"][3].subs(fixture), s.Rational(35, 9))
        self.assertEqual(d["momentum_tensor_from_velocities"][0, 1].subs(fixture),
                         s.Rational(35, 18))
        self.assertEqual(d["tensor_momentum_residuals"], [0]*9)

    def test_legendre_transform_reconstructs_every_symmetric_metric_velocity(self):
        # An erroneous trace or off-diagonal inverse fails Hamilton's equations.
        d = self.module().derive_seed()
        self.assertEqual(d["inverse_momentum_residuals"], [0]*6)
        self.assertEqual(d["hamilton_velocity_residuals"], [0]*6)
        self.assertEqual(d["contracted_hamiltonian_residual"], 0)
        self.assertNotEqual(d["raw_velocity_hessian_determinant"], 0)

    def test_published_seed_is_lapse_affine_with_nonzero_trace_hessian(self):
        # A missing correlated A2 term destroys affinity; trace deletion is separate.
        d = self.module().derive_seed()
        self.assertEqual(d["seed_lapse_hessian"], 0)
        self.assertNotEqual(d["seed_trace_hessian"], 0)
        self.assertNotEqual(d["uncorrelated_lapse_hessian"], 0)

    def test_mond_coefficient_is_derived_from_exact_kernel(self):
        # Wrong normalization of the MOND potential changes the zero-field slope.
        d = self.module().derive_lapse_variation()
        self.assertEqual(d["mond_alpha"], 1)
        self.assertEqual(d["kernel_slope_residual"], 0)

    def test_functional_derivative_and_mode_hessian_agree_with_gradient_sign(self):
        # Treating DiN as independent of N or losing the Hamiltonian minus sign fails.
        d = self.module().derive_lapse_variation()
        self.assertEqual(d["mode_variation_residual"], 0)
        fixture = {d["M"]: 2, d["alpha"]: 1, d["a"]: 3,
                   d["Nbar"]: 5, d["k"]: 7}
        self.assertEqual(d["mode_hessian"].subs(fixture), -s.Rational(1176, 5))
        self.assertEqual(d["mode_hessian"].subs(d["alpha"], 0), 0)

    def test_lapse_secondary_bracket_and_multiplier_close_without_new_constraint(self):
        # Assigning a bracket by hand or deleting remaining Hamiltonian drift fails.
        mod = self.module()
        d = mod.derive_constraint_symbol()
        self.assertEqual(d["secondary_definition_residual"], 0)
        self.assertEqual(d["primary_secondary_hessian_residual"], 0)
        self.assertEqual(d["poisson_matrix"], -d["poisson_matrix"].T)
        self.assertNotEqual(d["poisson_matrix"].det(), 0)
        self.assertEqual(d["multiplier_preservation_residual"], 0)
        self.assertTrue(d["drift"].has(s.Derivative))

    def test_homogeneous_and_unmodified_controls_are_rebuilt_before_division(self):
        # Substituting k=0 after dividing by k^2 would give an invalid rank claim.
        d = self.module().derive_constraint_symbol()
        for key in ("homogeneous", "unmodified"):
            c = d[key]
            self.assertEqual(c["primary_secondary_bracket"], 0)
            self.assertEqual(c["multiplier_coefficient"], 0)
            self.assertNotEqual(c["preservation_condition"], 0)
            self.assertIsNone(c["solved_multiplier"])

    def test_result_serializes_a_failed_scientific_gate_without_claiming_full_rank(self):
        result = self.module().run()
        self.assertEqual(json.loads(json.dumps(result))["two_tensor_gate"], "FAIL")
        self.assertTrue(result["checks_passed"])
        self.assertFalse(result["full_nonlinear_dof_count_claimed"])

    def test_cli_normal_and_required_gate_exit_codes_and_exclusive_output(self):
        # Conflating successful execution with a passing physics gate is a bug.
        mod = self.module()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-two-tensor"]), 2)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/"result.json"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(mod.main(["--output", str(output)]), 0)
            original = output.read_bytes()
            self.assertEqual(json.loads(original)["two_tensor_gate"], "FAIL")
            with self.assertRaises(FileExistsError):
                mod.main(["--output", str(output)])
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
