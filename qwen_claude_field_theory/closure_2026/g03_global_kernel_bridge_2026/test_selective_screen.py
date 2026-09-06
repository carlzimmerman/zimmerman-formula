"""Regression controls: source mismatch, false pole kill, and hidden constraints."""
import importlib.util
import unittest

AVAILABLE = importlib.util.find_spec('selective_screen') is not None


class ImplementationTest(unittest.TestCase):
    def test_selective_screen_is_implemented(self):
        self.assertTrue(AVAILABLE, 'Selective-screen action calculation is missing')


@unittest.skipUnless(AVAILABLE, 'calculation not implemented')
class ScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import selective_screen
        cls.result = selective_screen.derive()

    def test_source_action_and_exact_identities(self):
        self.assertTrue(all(self.result['checks'].values()))

    def test_no_fake_ghost_from_lapse_sign(self):
        self.assertTrue(all(v > 0 for v in self.result['kinetic_eigenvalues']))
        self.assertLess(min(self.result['above_threshold_omega_squared']), 0)
        self.assertGreater(min(self.result['below_threshold_omega_squared']), 0)

    def test_crossing_is_not_silently_divided_out(self):
        self.assertEqual(self.result['crossing_frequency_polynomial_degree'], 1)
        self.assertGreater(self.result['crossing_finite_omega_squared'], 0)

    def test_dirac_chain_preserved_until_closure(self):
        for row in self.result['dirac'].values():
            self.assertTrue(row['preservation_closed'])
            self.assertEqual(row['bracket_rank'], row['constraint_count'])
        self.assertGreater(self.result['dirac']['crossing']['constraint_count'],
                           self.result['dirac']['above']['constraint_count'])

    def test_zero_mode_not_counted_by_cancelling_k(self):
        self.assertFalse(self.result['homogeneous']['nonlinear_count_claimed'])
        self.assertEqual(self.result['homogeneous']['screen_contribution'], '0')


if __name__ == '__main__':
    unittest.main()
