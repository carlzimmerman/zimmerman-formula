"""Controls for retarded variation, kinetic sign, and pole cancellation."""
import importlib.util
import unittest

AVAILABLE = importlib.util.find_spec('causal_screen') is not None


class ImplementationTest(unittest.TestCase):
    def test_causal_gate_exists(self):
        self.assertTrue(AVAILABLE, 'Causal-screen calculation missing')


@unittest.skipUnless(AVAILABLE, 'not implemented')
class CausalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import causal_screen
        cls.r = causal_screen.derive()

    def test_variation_is_not_silently_replaced_by_retarded_rule(self):
        self.assertTrue(self.r['checks']['retarded_action_varies_to_symmetric_kernel'])
        self.assertFalse(self.r['retarded_gradient_equals_retarded_equation'])

    def test_healthy_and_ghost_signs_are_distinguished(self):
        self.assertGreater(self.r['healthy']['static_response_correction'], 0)
        self.assertLess(self.r['ghost']['static_response_correction'], 0)
        self.assertEqual(self.r['healthy']['negative_kinetic_count'], 0)
        self.assertGreater(self.r['ghost']['negative_kinetic_count'], 0)

    def test_hidden_pole_is_not_cancelled(self):
        self.assertGreater(self.r['healthy']['propagator_pole_count'], 1)
        self.assertEqual(self.r['healthy']['common_polynomial_factor_degree'], 0)
        self.assertGreater(self.r['healthy']['velocity_Hessian_rank'], 1)

    def test_healthy_oscillator_does_not_automatically_fail(self):
        self.assertTrue(all(v > 0 for v in self.r['healthy']['omega_squared']))

    def test_completed_square_and_negative_witness(self):
        self.assertTrue(all(self.r['checks'].values()))
        self.assertLess(self.r['negative_direction_before'], 0)
        self.assertLessEqual(self.r['negative_direction_after'], self.r['negative_direction_before'])

    def test_elliptic_escape_is_counted_and_tests_physical_tail(self):
        self.assertIn('elliptic',self.r,'Nondynamical elliptic escape has not been tested')
        self.assertEqual(self.r['elliptic']['physical_mode_count'],1)
        self.assertLess(self.r['elliptic']['off_source_initial_acceleration'],0)
        self.assertTrue(self.r['elliptic']['constraint_preservation_closed'])


if __name__ == '__main__':
    unittest.main()
