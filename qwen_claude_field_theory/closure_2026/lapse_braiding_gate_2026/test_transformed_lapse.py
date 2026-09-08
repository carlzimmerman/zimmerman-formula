"""Independent controls for a transformed physical lapse potential."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

import sympy as s


class TransformedLapseTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec("transformed_lapse"),
                             "The transformed lapse screen is not implemented")
        import transformed_lapse
        return transformed_lapse

    def test_full_symmetric_symplectic_form_fixes_primary_momentum_sign(self):
        # Omitting doubled off-diagonal contractions or reversing w_N fails.
        d = self.module().derive_point_transformation()
        self.assertEqual(d["symplectic_residual"], 0)
        self.assertEqual(d["primary_relation_residual"], 0)
        fixture = {**dict.fromkeys(d["h_components"], 0),
                   **dict.fromkeys(d["pi_components"], 0)}
        fixture[d["h_components"][3]] = 3
        fixture[d["pi_components"][3]] = 5
        self.assertEqual(d["pi_trace"].subs(fixture), 30)

    def test_physical_metric_pullback_fixes_both_conformal_weights(self):
        # Using the seed inverse metric for the physical acceleration fails.
        d = self.module().derive_potential()
        self.assertEqual(d["pullback_residual"], 0)
        self.assertEqual(d["acceleration_pullback_residual"], 0)
        self.assertEqual(d["volume_pullback_residual"], 0)

    def test_actual_potential_gradient_hessian_matches_all_tensor_components(self):
        # Wrong prefactors, a dropped radial term, or diagonal truncation fails.
        d = self.module().derive_potential()
        self.assertEqual(d["gradient_hessian_residuals"], [0]*9)
        self.assertEqual(d["gradient_hessian"], d["gradient_hessian"].T)
        self.assertNotEqual(d["gradient_hessian"][0, 1], 0)

    def test_homogeneous_symbol_uses_finite_first_derivative_not_singular_fss(self):
        d = self.module().derive_homogeneous()
        fixture = {d["M"]: 2, d["N"]: 3, d["a"]: 5,
                   d["w0"]: 0, d["alpha"]: 1, d["k"]: 7}
        self.assertEqual(d["hamiltonian_symbol"].subs(fixture), -s.Rational(1960, 3))
        self.assertEqual(d["hamiltonian_symbol"].subs(d["alpha"], 0), 0)
        self.assertEqual(d["hamiltonian_symbol"].subs(d["k"], 0), 0)
        self.assertEqual(d["mode_functional_residual"], 0)
        self.assertFalse(d["hamiltonian_symbol"].has(s.zoo, s.nan, s.oo))

    def test_exact_kernel_radial_eigenvalue_has_the_only_finite_positive_zero(self):
        d = self.module().derive_anisotropy()
        y = d["y"]
        self.assertEqual(s.simplify(d["tangential_normalized"]-s.exp(-y)), 0)
        self.assertEqual(s.simplify(d["longitudinal_normalized"]-(1-y)*s.exp(-y)), 0)
        self.assertEqual(d["longitudinal_positive_roots"], [1])
        self.assertEqual(d["tangential_positive_roots"], [])
        self.assertEqual(d["potential_hessian_rank_at_y1"], 2)
        self.assertEqual(d["potential_hessian_determinant_at_y1"], 0)
        self.assertLess(d["longitudinal_normalized"].subs(y, 2), 0)

    def test_mond_operator_does_not_share_the_lapse_hessian_zero(self):
        # Confusing f_s+2s f_ss with mu+y mu_y would falsely kill static ellipticity.
        d = self.module().derive_anisotropy()
        self.assertEqual(d["mond_radial"].subs(d["y"], 1), 1)
        self.assertEqual(s.limit(d["longitudinal_normalized"], d["y"], 0, dir="+"), 1)
        self.assertEqual(d["anisotropic_hessian_residuals"], [0]*9)

    def test_matter_legendre_transform_has_no_gradient_lapse_principal_term(self):
        d = self.module().derive_matter()
        self.assertEqual(d["matter_momentum_residual"], 0)
        self.assertEqual(d["matter_velocity_residual"], 0)
        self.assertEqual(d["gradient_lapse_hessian"], s.zeros(3))
        self.assertNotEqual(d["algebraic_lapse_hessian"], 0)

    def test_run_serializes_failed_gate_and_keeps_source_caveats(self):
        result = self.module().run()
        data = json.loads(json.dumps(result))
        self.assertTrue(data["checks_passed"])
        self.assertEqual(data["two_tensor_gate"], "FAIL")
        self.assertFalse(data["full_constraint_count_claimed"])
        self.assertEqual(data["source"]["verification_scope"],
                         "restriction_equations_and_point_transformation_not_dof_certification")
        self.assertGreaterEqual(len(data["source"]["caveats"]), 2)

    def test_cli_gate_exit_and_output_are_independent_and_non_overwriting(self):
        mod = self.module()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(mod.main([]), 0)
            self.assertEqual(mod.main(["--require-two-tensor"]), 2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"result.json"
            self.assertEqual(mod.main(["--output", str(output)]), 0)
            original = output.read_bytes()
            self.assertTrue(json.loads(original)["checks_passed"])
            with self.assertRaises(FileExistsError):
                mod.main(["--output", str(output)])
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
