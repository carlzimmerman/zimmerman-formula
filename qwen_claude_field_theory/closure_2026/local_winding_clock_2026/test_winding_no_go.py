import unittest

import sympy as sp

from winding_no_go import no_go_report


class WindingNoGoTests(unittest.TestCase):
    def test_exact_transport_is_degenerate_for_all_spatial_modes(self):
        r = no_go_report()
        self.assertEqual(r["momentum_hessian_rank"], 0)
        self.assertEqual(sp.simplify(r["dirac_bracket_p_lambda_CQ"] - r["area"]), 0)
        self.assertEqual(sp.simplify(sp.diff(r["principal_determinant"], r["k"])), 0)
        self.assertIn("cannot", r["strict_architecture_conclusion"])

    def test_removing_the_multiplier_constraint_is_the_required_escape(self):
        r = no_go_report()
        self.assertGreater(r["kinetic_regulator_rank"], r["momentum_hessian_rank"])
        self.assertTrue(r["escape_requires_changing_constraint"])


if __name__ == "__main__":
    unittest.main()
