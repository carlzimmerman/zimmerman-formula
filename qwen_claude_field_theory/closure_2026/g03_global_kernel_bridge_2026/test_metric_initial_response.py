"""Test the physical initial-jet response, including the global trace mode."""
import importlib.util
import unittest

AVAILABLE=importlib.util.find_spec('metric_initial_response') is not None


class ImplementationTest(unittest.TestCase):
    def test_initial_response_exists(self):
        self.assertTrue(AVAILABLE,'Curved-background gravitational response missing')


@unittest.skipUnless(AVAILABLE,'not implemented')
class InitialResponseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_initial_response as model
        cls.r=model.audit()

    def test_curvature_not_lapse_acceleration_is_the_observable(self):
        self.assertEqual(self.r['Ricci_initial_jet_identity_residual'],'0')
        self.assertEqual(self.r['GR_lapse_response_to_v'],'0')
        self.assertIn('GR_Rindler_lapse_equation',self.r)
        self.assertEqual(self.r['GR_Rindler_lapse_equation'],'-4*wpp')

    def test_global_constraint_and_walls_are_not_omitted(self):
        for row in self.r['responses']:
            self.assertTrue(row['success'])
            self.assertLess(row['maximum_boundary_residual'],1e-9)
            self.assertLess(row['relative_mean_w_residual'],1e-6)
            self.assertLess(row['maximum_ODE_residual'],1e-5)

    def test_refined_response_is_nonzero_outside_source(self):
        for row in self.r['responses']:
            self.assertGreater(row['outside_to_peak_curvature_ratio'],1e-4)
            self.assertLess(row['relative_refinement_difference'],1e-4)
            self.assertTrue(row['source_and_initial_matter_difference_zero_at_probe'])


if __name__=='__main__':
    unittest.main()
