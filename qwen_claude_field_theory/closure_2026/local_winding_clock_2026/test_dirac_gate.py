import unittest

import sympy as sp

from dirac_gate import dirac_report


class DiracGateTests(unittest.TestCase):
    def test_actual_memory_constraints_and_brackets_close(self):
        for mode in ("k_nonzero", "k_zero"):
            with self.subTest(mode=mode):
                result = dirac_report(mode)
                self.assertIn("p_lambda", result["primary_names"])
                self.assertIn("C_Q", result["primary_names"])
                matrix = result["poisson_matrix"]
                self.assertEqual(matrix, -matrix.T)
                self.assertGreaterEqual(result["rank"], 0)
                self.assertTrue(all(
                    sp.simplify(value) == 0
                    for value in result["preservation_residuals"]
                ))
                self.assertEqual(
                    result["phase_space_dimension"] % 2,
                    0,
                )

    def test_absolute_winding_is_reported_as_separate_control(self):
        result = dirac_report("k_nonzero")
        control = result["absolute_winding_control"]
        self.assertIn("velocity_hessian_rank", control)
        self.assertIn("epsilon_w", control)
        self.assertNotEqual(result["mode"], control.get("mode"))


if __name__ == "__main__":
    unittest.main()
