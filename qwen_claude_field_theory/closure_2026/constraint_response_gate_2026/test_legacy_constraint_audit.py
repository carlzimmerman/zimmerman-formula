"""Regression tests for actual weak constraints and all Bianchi components."""

import json
import pathlib
import subprocess
import sys
import unittest

import sympy as s

try:
    import legacy_constraint_audit as audit
except ModuleNotFoundError:
    audit = None


class LegacyConstraintAuditTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(audit, "The legacy audit has not been implemented")

    def test_poisson_matrix_and_secondary_come_from_canonical_functions(self):
        result = audit.derive_toy()
        K, L, A, pq = (result[key] for key in ("K", "L", "A", "p_q"))
        expected = s.Matrix([[0, -1, -L, 0], [1, 0, 0, K],
                             [L, 0, 0, -K*L], [0, -K, K*L, 0]])
        self.assertEqual(result["dirac_matrix"], expected)
        self.assertEqual(s.factor(result["determinant"]), 4*K**2*L**2)
        self.assertEqual(result["rank"], 4)
        self.assertEqual(result["derived_secondary"], -L*A*pq)

    def test_full_weak_surface_forces_pq_and_multipliers_to_zero(self):
        result = audit.derive_toy()
        surface = result["weak_surface"]
        self.assertEqual(surface[result["p_phi"]], 0)
        self.assertEqual(surface[result["p_q"]], 0)
        self.assertEqual(surface[result["phi"]], result["rho"]/(2*result["L"]))
        self.assertEqual(surface[result["q"]], -result["rho"]/(2*result["L"]))
        self.assertEqual(result["constraint_residuals"], s.zeros(4, 1))
        self.assertEqual(list(result["weak_multipliers"].values()), [0, 0, 0, 0])

    def test_zero_mode_retains_source_equation(self):
        result = audit.derive_toy()
        self.assertEqual(result["zero_mode_constraints"][2], -result["rho"])
        self.assertEqual(result["zero_mode_rank"], 2)
        self.assertEqual(result["zero_mode_source_solution"], [{result["rho"]: 0}])
        self.assertEqual(result["zero_mode_nonzero_source_solutions"], [])

    def test_metric_derivation_and_all_four_bianchi_components(self):
        result = audit.derive_linear_bianchi()
        t, x, y, z = result["coordinates"]
        psi, phi, mu, G = (result[key] for key in ("Psi", "Phi", "mu", "einstein"))
        lap_psi = sum(s.diff(psi, coordinate, 2) for coordinate in (x, y, z))
        self.assertEqual(s.simplify(G[0, 0]-2*lap_psi), 0)
        self.assertEqual(s.simplify(G[0, 1]-2*s.diff(psi, t, x)), 0)
        self.assertEqual(s.simplify(G[1, 1]-G[2, 2]
                                   -(s.diff(psi-phi, x, 2)-s.diff(psi-phi, y, 2))), 0)
        self.assertEqual(result["gr_bianchi"], s.zeros(4, 1))
        expected = s.Matrix([0, *(2*(1-mu)*s.diff(psi, t, 2, coordinate)
                                  for coordinate in (x, y, z))])
        self.assertEqual((result["tandem_bianchi"]-expected).applyfunc(s.simplify), s.zeros(4, 1))
        self.assertEqual(result["tandem_bianchi"].subs(mu, 1), s.zeros(4, 1))
        psi_1d = s.Function("Psi")(t, x)
        self.assertEqual(result["legacy_plus_sign_base"], 4*s.diff(psi_1d, t, x, 2))

    def test_compact_smooth_noslip_witness_has_nonzero_divergence(self):
        result = audit.compact_witness()
        self.assertEqual(result["slip"], 0)
        self.assertEqual(result["origin_divergence"], s.Matrix([0, 1, 0, 0]))
        self.assertTrue(result["compact_support"])

    def test_json_result_and_computed_legacy_closure_gate(self):
        result = audit.run()
        json.dumps(result, allow_nan=False)
        self.assertTrue(result["algebra_checks_passed"])
        self.assertFalse(result["legacy_closure"])
        self.assertTrue(all(result["violations"].values()))
        self.assertIsNone(result["gravitational_dof_count"])
        script = pathlib.Path(__file__).with_name("legacy_constraint_audit.py")
        completed = subprocess.run(
            [sys.executable, "-B", str(script), "--require-legacy-closure"],
            capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertFalse(json.loads(completed.stdout)["legacy_closure"])


if __name__ == "__main__":
    unittest.main()
