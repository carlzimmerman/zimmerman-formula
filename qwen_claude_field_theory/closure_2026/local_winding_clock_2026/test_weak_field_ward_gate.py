import unittest

import sympy as sp

from weak_field_ward_gate import weak_field_report, ward_report


class WeakFieldWardTests(unittest.TestCase):
    def test_potentials_are_varied_independently_and_mond_branch_is_exact(self):
        result = weak_field_report()
        self.assertNotEqual(result["phi_equation"], result["psi_equation"])
        self.assertEqual(sp.simplify(result["mond_residual"]), 0)
        self.assertEqual(sp.simplify(result["measured_G"] - 1 / (8 * sp.pi * result["m"])), 0)

    def test_baryon_ward_is_exact_but_cold_exchange_is_not_zero(self):
        result = ward_report()
        self.assertEqual(sp.simplify(result["baryon_ward_residual"]), 0)
        self.assertEqual(sp.simplify(result["baryon_divergence_on_shell"]), 0)
        self.assertNotEqual(sp.simplify(result["cold_exchange_residual"]), 0)
        self.assertNotEqual(sp.simplify(result["q_equation_source_term"]), 0)


if __name__ == "__main__":
    unittest.main()
