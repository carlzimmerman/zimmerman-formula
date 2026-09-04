#!/usr/bin/env python3
"""Exact regression and mutation controls for the scoped spectral audit."""

import importlib
import unittest

import sympy as sp


class SpectralEscapeTests(unittest.TestCase):
    def setUp(self):
        try:
            module = importlib.import_module("spectral_escape_checks")
        except ModuleNotFoundError as exc:
            if exc.name != "spectral_escape_checks":
                raise
            self.fail("The reproducible spectral derivation has not been implemented")
        self.result = module.derive_spectral_escape_checks()

    def test_lorentz_projector_has_the_correct_signature_and_spectral_rank(self):
        """Catches a Euclidean sign or the wrong spectral eigenline."""
        r = self.result["spectral"]
        self.assertEqual(r["self_adjoint_residual"], sp.zeros(2))
        self.assertEqual(r["minimal_polynomial_residual"], sp.zeros(2))
        self.assertEqual(r["idempotence_residual"], sp.zeros(4))
        self.assertEqual(r["projector_trace"], 1)
        self.assertEqual(r["spatial_determinant"], 0)
        self.assertEqual(r["rest_spatial_tensor"], sp.diag(0, 1, 1, 1))

    def test_scalar_curvature_degeneracy_has_two_distinct_finite_limits(self):
        """Catches normalization that silently selects one approach direction."""
        r = self.result["spectral"]
        self.assertEqual(r["rest_path_limit"], sp.diag(0, 1, 1, 1))
        expected = sp.Matrix([
            [sp.Rational(1, 3), -sp.Rational(2, 3), 0, 0],
            [-sp.Rational(2, 3), sp.Rational(4, 3), 0, 0],
            [0, 0, 1, 0], [0, 0, 0, 1],
        ])
        self.assertEqual(r["boosted_path_limit"], expected)
        self.assertEqual(r["curvature_path_endpoint_residual"], sp.zeros(2))
        self.assertNotEqual(r["path_difference"], sp.zeros(4))

    def test_null_degeneracy_is_nonzero_jordan_with_divergent_projector(self):
        """Catches confusing the null/Jordan boundary with the scalar endpoint."""
        r = self.result["spectral"]
        self.assertEqual(r["jordan_block"], sp.Matrix([[1, 1], [-1, -1]]))
        self.assertEqual(r["jordan_square"], sp.zeros(2))
        self.assertEqual(r["null_boundary_h11_limit"], sp.oo)
        self.assertEqual(set(r["complex_branch_eigenvalues"]),
                         {-sp.sqrt(3) * sp.I, sp.sqrt(3) * sp.I})

    def test_vanishing_weights_soften_only_the_tested_boundary_jets(self):
        """Catches an unqualified no-go for weighted projectors."""
        r = self.result["weighted_boundary"]
        self.assertEqual(r[1]["right_derivative_limits"], (0, sp.oo))
        self.assertEqual(r[2]["right_derivative_limits"], (0, 0, sp.oo))
        self.assertEqual(r[3]["right_derivative_limits"], (0, 0, 0, sp.oo))
        for n in (1, 2, 3):
            self.assertEqual(r[n]["left_derivative_limits"], (0,) * (n + 1))

    def test_euclidean_sign_mutation_fails_lorentz_self_adjointness(self):
        """The symmetric off-diagonal mutation must fail the same invariants."""
        r = self.result["negative_controls"]
        self.assertNotEqual(r["euclidean_self_adjoint_residual"], sp.zeros(2))
        self.assertNotEqual(r["euclidean_idempotence_residual"], sp.zeros(2))

    def test_metric_jets_generate_static_and_flrw_curvature_with_correct_signs(self):
        """Catches a Riemann convention or Christoffel-product omission."""
        r = self.result["curvature_source"]
        p, A, H = (r["symbols"][name] for name in ("p", "A", "H"))
        self.assertEqual(r["static_ricci_mixed"], sp.diag(-p, p, p, p))
        self.assertEqual(r["flrw_ricci_mixed"],
                         sp.diag(3 * (A + H**2), *([A + 3 * H**2] * 3)))
        self.assertEqual(r["static_riemann"][0, 1, 0, 1], p / 3)
        self.assertEqual(r["static_riemann"][1, 2, 1, 2], 2 * p / 3)
        self.assertEqual(r["flrw_riemann"][0, 1, 0, 1], -A - H**2)
        self.assertEqual(r["flrw_riemann"][1, 2, 1, 2], H**2)

    def test_all_riemann_components_match_at_the_dust_flrw_jet(self):
        """Catches checking only Ricci when claiming curvature indistinguishability."""
        r = self.result["curvature_source"]
        self.assertEqual(len(r["matched_riemann_residuals"]), 256)
        self.assertTrue(all(item == 0 for item in r["matched_riemann_residuals"]))
        self.assertTrue(all(item == 0 for item in r["static_weyl_components"]))
        self.assertTrue(all(item == 0 for item in r["riemann_symmetry_residuals"]))

    def test_tidal_anisotropy_is_a_negative_control_for_riemann_matching(self):
        """Equal Ricci does not force equal Riemann away from the isotropic jet."""
        r = self.result["negative_controls"]
        self.assertEqual(r["tidal_ricci_difference"], sp.zeros(4))
        self.assertTrue(any(item != 0 for item in r["tidal_weyl_components"]))
        self.assertTrue(any(item != 0 for item in r["tidal_riemann_difference"]))

    def test_curvature_subtraction_also_removes_the_static_poisson_source(self):
        """Catches retaining a nonzero linear source after all-FLRW subtraction."""
        r = self.result["curvature_source"]
        c1, c2 = (r["symbols"][name] for name in ("c1", "c2"))
        self.assertEqual(r["linear_source_flrw_coefficients"].det(), -18)
        self.assertEqual(r["linear_source_solution"], {c1: 0, c2: 0})
        self.assertEqual(r["spectral_subtraction_static"], 0)

    def test_spectral_action_acceleration_subblock_needs_off_diagonal_ricci(self):
        """Catches freezing the projector before differentiating the action."""
        r = self.result["derivative_trigger"]
        d, b, lam, C = (r["symbols"][name] for name in ("d", "b", "lambda", "C"))
        expected = 3 * lam * C * b**2 * d / (2 * (d**2 - b**2)**sp.Rational(5, 2))
        self.assertEqual(sp.simplify(r["acceleration_hessian"] - expected), 0)
        self.assertEqual(r["diagonal_ricci_control"], 0)
        self.assertNotEqual(r["off_diagonal_numeric_control"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
