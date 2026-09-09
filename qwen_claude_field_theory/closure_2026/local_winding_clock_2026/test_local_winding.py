import unittest

import sympy as sp

from run_local_winding import build_results


class LocalWindingIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = build_results()

    def test_all_implemented_exact_gates_close(self):
        r = self.results
        self.assertEqual(sp.simplify(r["action"]["primitive_residual"]), 0)
        self.assertEqual(sp.simplify(r["action"]["memory_residual"]), 0)
        self.assertEqual(sp.simplify(r["action"]["memory_adjoint_residual"]), 0)
        self.assertEqual(sp.simplify(r["action"]["cold_scalar_residual"]), 0)
        self.assertEqual(sp.simplify(r["action"]["static"]["mond_residual"]), 0)
        for mode in ("k_nonzero", "k_zero"):
            self.assertTrue(all(
                sp.simplify(v) == 0
                for v in r["dirac"][mode]["preservation_residuals"]
            ))
        self.assertEqual(sp.simplify(r["weak_field"]["mond_residual"]), 0)
        self.assertEqual(sp.simplify(r["ward"]["baryon_ward_residual"]), 0)
        self.assertEqual(sp.simplify(r["ward"]["baryon_divergence_on_shell"]), 0)
        self.assertEqual(sp.simplify(r["flrw"]["memory_integral_residual"]), 0)
        self.assertTrue(r["stability"]["zero_gradient_flag"])
        self.assertEqual(sp.simplify(sp.diff(
            r["stability"]["memory_characteristic_determinant"],
            r["stability"]["k"],
        )), 0)
        self.assertEqual(r["status"], "OPEN")
        self.assertIn("DEAD_FOR_SEPARATE_COLD_TRANSMISSION", r["route_verdict"])
        self.assertTrue(r["no_go"]["escape_requires_changing_constraint"])

    def test_report_explicitly_keeps_unimplemented_gates_open(self):
        open_gates = set(self.results["open_gates"])
        for gate in ("full_ADM_DOF", "PPN_alpha", "nonlinear_stability", "causal_propagation"):
            self.assertIn(gate, open_gates)


if __name__ == "__main__":
    unittest.main()
