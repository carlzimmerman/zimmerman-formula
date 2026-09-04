"""Exact benchmarks: each test names an error it must detect."""

import importlib.util
from pathlib import Path
import unittest

import sympy as sp

MODULE = Path(__file__).with_name("connection_checks.py")
checks = None
if MODULE.exists():
    spec = importlib.util.spec_from_file_location("connection_checks", MODULE)
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(checks, "full connection computation is not implemented")

    def test_vector_restriction_of_full_tensor_matches_hand_contraction(self):
        # A swapped contraction or wrong lower-index symmetry changes 3*A^2.
        data = checks.distortion(4)
        a = sp.symbols("A0:4", real=True)
        replacement = {data["C"](i, j, k): (a[k] if i == j else 0)
                       + (a[j] if i == k else 0)
                       for i, j, k in data["indices"]}
        actual = data["B"].subs(data["flat_metric"]).subs(replacement)
        self.assertEqual(sp.expand(actual - 3 * (-a[0]**2 + sum(v**2 for v in a[1:]))), 0)

    def test_general_frame_identities_include_metric_variation(self):
        # Omitting a covariant-index term or the metric variation breaks GL.
        data = checks.frame_audit(4)
        self.assertTrue(all(value == 0 for value in data["B_residuals"]))
        self.assertTrue(all(value == 0 for value in data["trace_residuals"]))
        self.assertTrue(any(value != 0 for value in data["C_only_B_variations"]))
        self.assertEqual(data["metric_map_rank"], len(checks.distortion(4)["gvars"]))

    def test_connection_hessian_not_assumed_invertible_in_all_dimensions(self):
        # Replacing the Hessian by an identity would miss the 2D degeneracy.
        two, four = checks.hessian_audit(2), checks.hessian_audit(4)
        self.assertEqual(two["determinant"], 0)
        self.assertNotEqual(four["determinant"], 0)
        self.assertEqual(four["euler_residual"], 0)
        self.assertEqual(four["hessian"], four["hessian"].T)
        self.assertEqual(checks.distortion(1)["B"], 0)

    def test_poisson_matrix_is_derived_from_primary_and_secondary_functions(self):
        # Wrong symplectic sign, duplicated constraints, or an inserted rank fails.
        data = checks.canonical_audit()
        matrix = data["poisson_matrix"]
        n = len(data["q"])
        self.assertEqual(checks.poisson(data["q"][0], data["p"][0], data["q"], data["p"]), 1)
        # Differentiate the actual constraint functions independently of the
        # symplectic-matrix multiplication, fixing the otherwise invisible sign.
        cross = matrix.extract(range(n), range(n, 2 * n))
        self.assertEqual(cross + sp.Matrix(data["secondary"]).jacobian(data["q"]).T,
                         sp.zeros(n))
        self.assertEqual(matrix + matrix.T, sp.zeros(matrix.rows))
        self.assertEqual(data["preservation_residual"], sp.zeros(len(data["q"]), 1))
        self.assertNotEqual(matrix.det(), 0)
        self.assertEqual(matrix.rank(), data["constraint_jacobian"].rank())
        self.assertEqual(data["auxiliary_phase_dimension_after_reduction"],
                         len(data["q"]) * 2 - matrix.rank())
        self.assertTrue(all(not v.has(data["k"]) for v in matrix))

    def test_exponential_branch_retains_nonzero_null_distortions(self):
        # Declaring C=0 uniquely would discard actual stationary null branches.
        data = checks.exponential_audit()
        self.assertEqual(data["primitive_residual"], 0)
        self.assertEqual(data["U_B_positive"], 1 - sp.exp(-sp.sqrt(data["b"]) / data["a0"]))
        self.assertEqual(data["U_B_negative_magnitude"], -data["U_B_positive"])
        self.assertEqual(data["derivative_limit_at_zero"], 0)
        self.assertEqual(data["null_B"], 0)
        self.assertTrue(any(v != 0 for v in data["null_gradient_B"]))
        self.assertEqual(data["U_BB_limit_at_zero"], sp.oo)
        self.assertEqual(data["origin_directional_second_derivative"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
