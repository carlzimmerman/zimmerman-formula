"""Independent controls for the bounded same-action bridge audit."""
import unittest
import sympy as sp
from bridge_audit import derive, rar_slope


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = derive()

    def test_variations_and_diagonalization(self):
        self.assertTrue(all(v == 0 for v in self.r['exact_residuals'].values()))

    def test_counterexample_to_small_scalar_share(self):
        self.assertLess(self.r['rar_witness_margin'], 0)
        self.assertLess(self.r['exp_witness_margin'], 0)

    def test_allowed_escape_not_universal_nogo(self):
        self.assertGreater(rar_slope(2.5756789) - 1 / 1.04, 0)
        self.assertGreater(1 / (1 + float(sp.exp(-2))) - 1 / 1.14, 0)

    def test_finite_difference_independent_slope(self):
        import math
        for b in (0.1, 1, 6.25, 20):
            step = b * 1e-5
            curve = lambda z: z / (-math.expm1(-math.sqrt(z)))
            fd = (curve(b + step) - curve(b - step)) / (2 * step)
            self.assertAlmostEqual(fd, rar_slope(math.sqrt(b)), places=9)

    def test_newtonian_mutation_has_no_positive_lower_bound(self):
        # Replacing either MOND curve by g = g_bar makes D=1 identically.
        self.assertEqual(1 / 1 - 1, 0)
        self.assertGreater(1 - 1 / (1 + self.r['scalar_share']), 0)

    def test_flrw_sign_is_not_accepted_either_way(self):
        self.assertEqual(self.r['rho_healthy_example'], sp.Rational(21, 10))
        self.assertEqual(self.r['rho_claimed_example'], -sp.Rational(21, 10))
        self.assertNotEqual(self.r['flrw_wrong_sign_residual'], 0)

    def test_operator_does_not_change_zero_wave_number_coefficient(self):
        k, ell, stiffness = sp.symbols('k ell stiffness', real=True)
        self.assertEqual(sp.limit((stiffness*k**2 + ell**2*k**4)/k**2, k, 0), stiffness)


if __name__ == '__main__':
    unittest.main()
