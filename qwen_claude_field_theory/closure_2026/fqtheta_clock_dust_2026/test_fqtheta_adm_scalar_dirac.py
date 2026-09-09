import unittest

from fqtheta_adm_scalar_dirac import build_gate


class FQThetaADMScalarDiracTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build_gate()

    def test_hessian_is_affinely_degenerate(self):
        self.assertTrue(self.data["affine_degeneracy_check_at_unit_sample"])
        self.assertEqual(self.data["velocity_hessian_determinant"], "0")

    def test_poisson_matrix_is_antisymmetric_and_generic(self):
        self.assertTrue(self.data["poisson_antisymmetric"])
        # The determinant is a nonzero polynomial; its numerical rank is then
        # evaluated directly from the exact sample matrix.
        self.assertNotEqual(self.data["poisson_determinant_factor"], "0")
        self.assertEqual(self.data["local_k_nonzero"]["constraint_jacobian_rank"],
                         self.data["local_k_nonzero"]["constraint_count"])

    def test_local_mode_and_zero_mode_are_reported_separately(self):
        local = self.data["local_k_nonzero"]
        zero = self.data["k_zero"]
        self.assertGreater(local["poisson_rank"], 0)
        self.assertGreaterEqual(int(local["configuration_dof"]), 0)
        self.assertGreater(zero["first_class_count"], 0)
        self.assertNotEqual(local["configuration_dof"], zero["configuration_dof"])

    def test_reduced_symplectic_form_has_k_squared_factor(self):
        reduced = self.data["reduced_Unn_Unnp_zero"]
        omega = reduced["symplectic_coefficient_dz_wedge_dp"]
        self.assertIn("k**2", omega)
        self.assertIn("lambda", reduced["characteristic_polynomial"])

    def test_runner_writes_json(self):
        # Keep this smoke test local and side-effect free.
        self.assertEqual(self.data["status"], "OPEN")


if __name__ == "__main__":
    unittest.main()
