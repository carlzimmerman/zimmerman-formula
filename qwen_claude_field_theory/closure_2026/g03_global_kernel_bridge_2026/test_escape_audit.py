"""Controls for reconstructing an allowed scalar branch before its next gate."""
import importlib.util
import unittest

AVAILABLE = importlib.util.find_spec('escape_audit') is not None


class ImplementationTest(unittest.TestCase):
    def test_escape_calculation_exists(self):
        self.assertTrue(AVAILABLE, 'The proposed escape has not been implemented')


@unittest.skipUnless(AVAILABLE, 'implementation not present yet')
class EscapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import escape_audit
        cls.module = escape_audit
        cls.result = escape_audit.derive()

    def test_both_variational_reconstructions(self):
        for row in self.result['curves'].values():
            self.assertTrue(all(v == 0 for v in row['exact_residuals'].values()))

    def test_newtonian_coefficient_and_monotonicity(self):
        for row in self.result['curves'].values():
            self.assertEqual(row['j_newtonian'], 3)
            self.assertGreater(row['minimum_slope_margin'], 0)

    def test_independent_numerical_primitive(self):
        for kernel in ('mu_exp', 'nu_RAR'):
            for u in (0.1, 0.5, 1.0, 3.0, 10.0):
                step = u*1e-5
                L = self.module.point(kernel,u-step)
                R = self.module.point(kernel,u+step)
                fd = (R['J']-L['J'])/(R['X']-L['X'])
                self.assertAlmostEqual(fd,self.module.point(kernel,u)['j'],places=7)

    def test_deep_mond_forces_negative_inside_coefficient(self):
        self.assertLess(self.result['j_zero'], 0)
        self.assertLess(self.result['inside_static_k4'], 0)
        self.assertGreater(self.result['outside_static_k4'], 0)

    def test_wavelength_term_is_varied(self):
        self.assertEqual(self.result['fourth_order_variation_residual'],0)

    def test_no_silent_newton_constant_identification(self):
        self.assertGreater(self.result['G_infinity_over_G_local'],1.2)
        self.assertFalse(self.result['local_G_exact_asymptote'])


class SourceDynamicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from zero_field_source_audit import derive
        cls.result=derive()

    def test_source_and_independent_ADM_agree(self):
        self.assertTrue(self.result['internal_validity'])
        self.assertFalse(self.result['source']['cache_io'])

    def test_actual_poles_change_with_operator_placement(self):
        self.assertTrue(self.result['inside_rejected_at_witness'])
        self.assertTrue(self.result['outside_positive_at_witness'])

    def test_stiffness_sign_and_kinetic_energy(self):
        import sympy as sp
        inside=self.result['variants']['inside']
        outside=self.result['variants']['outside']
        self.assertLess(sp.sympify(inside['stiffness_determinant']),0)
        self.assertGreater(sp.sympify(outside['stiffness_determinant']),0)
        self.assertTrue(all(sp.sympify(v)>0 for v in self.result['kinetic_eigenvalues_at_witness']))


if __name__ == '__main__':
    unittest.main()
