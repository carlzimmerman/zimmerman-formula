import unittest

import sympy as sp

from action_variation import derive_action, static_branch


class ActionVariationTests(unittest.TestCase):
    def test_exact_action_residuals_vanish(self):
        result = derive_action()
        self.assertEqual(sp.simplify(result["primitive_residual"]), 0)
        for name in ("memory_residual", "memory_adjoint_residual",
                     "cold_scalar_residual"):
            self.assertEqual(sp.simplify(result[name]), 0)

    def test_static_baryon_branch_keeps_exponential_mond(self):
        result = static_branch()
        self.assertEqual(sp.simplify(result["mond_residual"]), 0)
        self.assertEqual(sp.simplify(result["slip_residual"]), 0)
        self.assertTrue(result["measured_G"] != 0)


if __name__ == "__main__":
    unittest.main()
