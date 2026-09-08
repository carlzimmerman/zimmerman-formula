"""Independent checks of the gradient-dependent lapse primary constraint.

These tests catch normalization errors in velocity momenta, loss of the
lapse-gradient Euler derivative, omission of the lapse term in H_i, and an
incorrect inference that a nonzero first-order symbol is invertible in 3D.
"""

import json
import pathlib
import subprocess
import sys
import unittest

import sympy as s

try:
    import anisotropic_primary as audit
except ModuleNotFoundError:
    audit = None


class AnisotropicPrimaryTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(audit, "The primary-consistency audit is not implemented")

    def test_primary_is_derived_from_velocity_momenta(self):
        result = audit.derive_velocity_primary()
        self.assertEqual(s.expand(result["primary_residual"]), 0)
        self.assertEqual(s.simplify(result["metric_hessian_determinant"]
                                   + result["m"]**6/(256*result["N"]**6)), 0)
        self.assertEqual(result["hessian_null_residual"], s.zeros(7, 1))
        self.assertNotEqual(s.expand(result["p_N"]), 0)

    def test_reported_rank_is_computed_from_actual_hessian(self):
        result = audit.derive_velocity_primary()
        self.assertIn("kinetic_hessian_rank", result)
        self.assertEqual(result["kinetic_hessian_rank"], 6)
        self.assertEqual(result["kinetic_hessian_rank"], result["hessian"].rank())
        self.assertEqual(audit.run()["velocity_primary"]["kinetic_hessian_rank"],
                         result["kinetic_hessian_rank"])

    def test_actual_euler_variation_retains_gradient_term(self):
        result = audit.derive_smeared_bracket()
        N, eta, a0, P = (result[key] for key in ("N", "eta", "a0", "pi"))
        u, v, du, dv, dN = (result[key] for key in ("u", "v", "du", "dv", "dN"))
        expected = 4*eta/(a0**2*N**2)*sum(
            P[i, j]*dN[i]*(v*du[j]-u*dv[j])
            for i in range(3) for j in range(3))
        self.assertEqual(s.expand(result["bracket_density"]-expected), 0)
        self.assertEqual(result["metric_part"], 0)
        self.assertEqual(s.simplify(result["bracket_density"].subs(eta, 0)), 0)

    def test_bracket_is_antisymmetric_with_metric_dependent_control(self):
        result = audit.derive_smeared_bracket()
        pairs = [(result["u"], result["v"]), *zip(result["du"], result["dv"])]
        swap = {left: right for left, right in pairs}
        swap.update({right: left for left, right in pairs})
        bracket = result["bracket_density"]
        self.assertEqual(s.expand(bracket+bracket.xreplace(swap)), 0)
        self.assertFalse(bracket.has(result["omega"]))

    def test_exact_torus_witness_satisfies_full_constraints(self):
        result = audit.torus_witness()
        self.assertEqual(result["primary_residual"], 0)
        self.assertEqual(result["momentum_residuals"], [0, 0, 0])
        self.assertEqual(result["N_min"], 1)
        self.assertTrue(result["positive_bracket_weight_on_support"])
        self.assertAlmostEqual(result["compact_smear_bracket"],
                               -1.1502517577997406, places=10)

    def test_verdict_uses_actual_weak_bracket_and_exact_integrand_sign(self):
        result = audit.torus_witness()
        self.assertIn("signed_integrand_coefficient", result)
        self.assertEqual(result["signed_integrand_coefficient"], -4)
        self.assertTrue(result["exact_nonzero_witness"])
        self.assertEqual(audit.run()["primary_consistency"],
                         not result["exact_nonzero_witness"])

    def test_fourier_symbol_has_longitudinal_and_transverse_cases(self):
        result = audit.derive_smeared_bracket()
        symbol = result["principal_symbol"]
        substitutions = {result["N"]: 2, result["eta"]: 1, result["a0"]: 1}
        substitutions.update(dict(zip(result["dN"], (1, 0, 0))))
        substitutions.update(dict(zip(result["momenta"], (3, 0, 0, 0, 0, 0))))
        longitudinal = dict(zip(result["k"], (1, 0, 0)))
        transverse = dict(zip(result["k"], (0, 1, 0)))
        self.assertEqual(s.simplify(symbol.subs(substitutions).subs(longitudinal)), -6*s.I)
        self.assertEqual(s.simplify(symbol.subs(substitutions).subs(transverse)), 0)

    def test_serializable_result_and_fail_closed_gate(self):
        result = audit.run()
        json.dumps(result, allow_nan=False)
        self.assertTrue(result["algebra_checks_passed"])
        self.assertFalse(result["primary_consistency"])
        self.assertIsNone(result["dof_count"])
        script = pathlib.Path(__file__).with_name("anisotropic_primary.py")
        completed = subprocess.run(
            [sys.executable, "-B", str(script), "--require-primary-consistency"],
            capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertFalse(json.loads(completed.stdout)["primary_consistency"])


if __name__ == "__main__":
    unittest.main()
