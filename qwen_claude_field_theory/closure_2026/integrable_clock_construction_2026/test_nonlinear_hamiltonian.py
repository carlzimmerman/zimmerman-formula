#!/usr/bin/env python3
"""Tests for the nonlinear IC4 Hamiltonian identities, not an operator count."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest

import sympy as s


class NonlinearHamiltonianTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name("nonlinear_hamiltonian.py")
        cls.module_path = path
        if path.exists():
            spec = importlib.util.spec_from_file_location("ic4_nonlinear_test", path)
            cls.mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.mod)

    def module(self):
        self.assertTrue(self.module_path.exists(), "The nonlinear Hamiltonian implementation is missing")
        return self.mod

    def test_six_component_legendre_map_catches_off_diagonal_factor(self):
        d = self.module().derive_legendre()
        self.assertEqual(d["component_weights"], (1, 1, 1, 2, 2, 2))
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        C, t = d["C"], d["t"]
        self.assertEqual(s.factor(d["orthonormal_hessian"].det()), 3*C**6*t/8)
        self.assertEqual(d["orthonormal_hessian"][3, 3], C)

    def test_trace_degeneracy_is_not_divided_through(self):
        d = self.module().derive_legendre()
        self.assertEqual(d["orthonormal_hessian"].subs(d["t"], 0).rank(), 5)
        self.assertEqual(d["orthonormal_hessian"].subs(d["t"], s.Rational(-2, 3)).rank(), 6)

    def test_barred_point_map_cancels_both_auxiliary_velocities(self):
        mod = self.module()
        self.assertTrue(hasattr(mod, "derive_point_transform"), "Direct barred point-map derivation is missing")
        d = mod.derive_point_transform()
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        self.assertNotEqual(d["omit_auxiliary_velocity_mutation"], s.zeros(3))

    def test_spatial_ibp_includes_derivative_of_the_auxiliary_in_w(self):
        d = self.module().derive_spatial()
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        xi, u = d["xi"], d["u"]
        self.assertEqual(d["gradient_coefficients"], (0, 4*u*xi, 2*xi**2))
        self.assertNotEqual(d["omit_xi_du_mutation"], 0)

    def test_action_exponents_and_canonical_clock_source(self):
        d = self.module().derive_density()
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        xi, u, kap = d["xi"], d["u"], d["kappa"]
        self.assertEqual(s.diff(d["clock"], kap), -s.exp((3*u-4)*xi)/2)
        self.assertNotEqual(s.diff(d["clock"], xi), 0)

    def test_actual_auxiliary_jets_and_gradient_hessian(self):
        d = self.module().derive_auxiliary()
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        self.assertEqual(d["principal_gradient_hessian"].shape, (6, 6))
        self.assertEqual(d["principal_gradient_hessian"], d["principal_gradient_hessian"].T)
        self.assertNotEqual(d["principal_gradient_hessian"][0, 3], 0)
        self.assertTrue(all(s.simplify(v)==0 for v in d["H10"]-d["H01"].T))

    def test_local_variational_operator_catches_divergence_terms(self):
        d = self.module().derive_operator_control()
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        self.assertNotEqual(d["omit_divergence_mutation"], s.zeros(2, 1))

    def test_secondary_bracket_is_actually_computed_and_not_identically_zero(self):
        d = self.module().derive_bracket_control()
        self.assertIn("a0", d, "The fixture must retain the actual positive action scale")
        self.assertEqual(d["off_shell_fixture"], -5*d["a0"]**2*s.log(s.Rational(3, 4))**2/4)
        self.assertEqual(d["antisymmetry_residual"], 0)
        self.assertFalse(d["fixture_satisfies_auxiliary_constraints"])

    def test_curvature_variation_and_symmetric_canonical_pairing(self):
        d = self.module().derive_metric_variation_control()
        self.assertTrue(all(v == 0 for v in d["residuals"].values()))
        self.assertNotEqual(d["omit_curvature_derivatives_mutation"], 0)

    def test_conditional_constraint_matrix_inverse_does_not_drop_omega(self):
        d = self.module().derive_block_control()
        self.assertEqual(d["inverse_residual"], s.zeros(4))
        self.assertNotEqual(d["inverse_without_omega_residual"], s.zeros(4))

    def test_run_serializes_and_refuses_unproved_functional_closure(self):
        mod = self.module()
        d = mod.run()
        json.loads(json.dumps(d))
        self.assertTrue(d["checks_passed"])
        self.assertTrue(d["input_hash_matches"])
        self.assertFalse(d["full_functional_closure_proved"])
        self.assertIn("computation_manifest", d, "Reusable exact checks need a computation contract and provenance")
        self.assertEqual(d["computation_manifest"]["run"]["exit_status"], 0)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-functional-closure"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
