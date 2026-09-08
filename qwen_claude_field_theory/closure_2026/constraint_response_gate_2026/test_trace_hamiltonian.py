"""Independent identities for the trace-constrained Hamiltonian reduction."""

import json
import unittest

import sympy as s

import trace_hamiltonian as gate


class TraceHamiltonianTests(unittest.TestCase):
    def test_six_component_legendre_variations_close(self):
        result = gate.derive_legendre()
        for name, residual in result["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        self.assertEqual(len(result["momentum_solution"]), 6)
        self.assertNotEqual(result["momentum_hessian_determinant"], 0)

    def test_vcdm_difference_is_a_trace_constraint_multiple(self):
        result = gate.derive_legendre()
        self.assertEqual(s.simplify(result["vcdm_hamiltonian_difference"]
                                   - result["trace_constraint"]
                                   * result["hamiltonian_multiplier_shift"]), 0)
        self.assertEqual(result["residuals"]["vcdm_raw_multiplier_map"], 0)

    def test_homogeneous_lapse_is_not_preset(self):
        result = gate.derive_homogeneous()
        for name, residual in result["residuals"].items():
            with self.subTest(identity=name):
                self.assertEqual(s.simplify(residual), 0)
        self.assertEqual(s.simplify(result["regular_lapse"]
                                   - result["tau_dot"]/(3*result["rho"])), 0)
        self.assertEqual(result["regular_trace_multiplier"], 0)

    def test_constant_tau_vacuum_is_a_distinct_global_branch(self):
        result = gate.derive_homogeneous()
        self.assertEqual(result["vacuum_constraints"], [0, 0])
        self.assertEqual(result["vacuum_momentum_drift"], 0)
        self.assertEqual(s.simplify(result["vacuum_volume_velocity"]
                                   - s.Rational(3, 2)*result["lam"]*result["volume"]), 0)
        self.assertNotEqual(result["vacuum_volume_velocity"], 0)

    def test_global_identity_and_scope_are_distinguished(self):
        result = gate.derive_global_scaling()
        self.assertTrue(all(s.simplify(value) == 0 for value in result["residuals"].values()))
        self.assertIn("compact", result["boundary_assumption"])
        self.assertIn("analytic", result["global_equivalence_evidence"])
        self.assertIn("tau_dot", result["monotone_branch"])

    def test_public_run_is_json_safe_and_does_not_assign_a_full_count(self):
        result = gate.run()
        json.dumps(result)
        self.assertTrue(result["algebra_checks_passed"])
        self.assertIn("not a full", result["scope"])
        self.assertNotIn("full_dof", result)


if __name__ == "__main__":
    unittest.main()
