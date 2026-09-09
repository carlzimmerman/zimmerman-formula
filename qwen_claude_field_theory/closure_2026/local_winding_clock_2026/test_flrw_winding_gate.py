import unittest

import sympy as sp

from flrw_winding_gate import flrw_report
from winding_calibration import calibration_report


class FlrwWindingTests(unittest.TestCase):
    def test_expanding_solution_and_memory_integral_are_derived(self):
        result = flrw_report()
        solution = result["expanding_solution"]
        self.assertNotEqual(solution["H"], 0)
        self.assertTrue(all(
            sp.simplify(value) == 0
            for value in solution["equation_residuals"].values()
        ))
        self.assertEqual(sp.simplify(result["memory_integral_residual"]), 0)

    def test_cold_kinetic_coefficient_is_positive(self):
        result = flrw_report()
        self.assertEqual(result["cold_kinetic_coefficient"],
                         sp.exp(-result["beta"]) / 2)

    def test_assembly_ordering(self):
        result = calibration_report()
        self.assertEqual(result["Q_rec"], 0)
        self.assertEqual(result["Q_gal"], sp.log(3))
        self.assertEqual(result["Q_cl"], sp.log(sp.Rational(17, 10)))
        self.assertGreater(result["eta_cl_at_beta_min"],
                           result["eta_gal_at_beta_min"])
        self.assertGreater(result["beta_min"], 0)


if __name__ == "__main__":
    unittest.main()
