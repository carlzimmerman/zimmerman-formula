import unittest

import sympy as sp

from stability_causality_gate import stability_report


class StabilityCausalityTests(unittest.TestCase):
    def test_memory_principal_symbol_has_no_spatial_gradient(self):
        result = stability_report()
        omega = result["omega"]
        k = result["k"]
        det = result["memory_characteristic_determinant"]
        self.assertEqual(sp.simplify(sp.diff(det, k)), 0)
        self.assertEqual(sp.simplify(det.subs(omega, 0)), 0)
        self.assertGreater(result["memory_velocity_hessian_rank"], -1)
        self.assertTrue(result["zero_gradient_flag"])

    def test_cold_scalar_has_healthy_principal_sign(self):
        result = stability_report()
        self.assertGreater(result["cold_kinetic_coefficient"], 0)
        self.assertNotEqual(
            sp.simplify(result["cold_characteristic_determinant"]), 0
        )


if __name__ == "__main__":
    unittest.main()
