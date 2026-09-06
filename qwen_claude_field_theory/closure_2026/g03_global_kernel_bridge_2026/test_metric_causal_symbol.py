"""Full metric symbol tests: no preset determinant or causal certificate."""
import importlib.util
import unittest

AVAILABLE=importlib.util.find_spec('metric_causal_symbol') is not None


class ImplementationTest(unittest.TestCase):
    def test_full_metric_response_exists(self):
        self.assertTrue(AVAILABLE,'Full metric/source response is not implemented')


@unittest.skipUnless(AVAILABLE,'not implemented')
class MetricSymbolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_causal_symbol
        cls.r=metric_causal_symbol.derive()

    def test_all_metric_equations_and_constraints_satisfied(self):
        self.assertTrue(all(self.r['checks'].values()))
        self.assertEqual(len(self.r['canonical_metric_coordinates']),6)
        self.assertEqual(len(self.r['shift_coordinates']),3)
        self.assertTrue(self.r['all_equation_residuals_zero'])

    def test_all_metric_Dirac_chain_closes_without_a_hidden_polarization(self):
        self.assertTrue('all_metric_dirac' in self.r,'Full canonical constraint calculation missing')
        row=self.r['all_metric_dirac']
        self.assertTrue(row['preservation_closed'])
        self.assertEqual(row['physical_gravitational_pairs'],2)
        self.assertGreater(len(row['generations']),2)

    def test_GR_control_cancels_nonlocal_Ricci_response(self):
        self.assertEqual(self.r['GR_Ricci_identity_residual'],'0')
        self.assertTrue(self.r['GR_locality'])

    def test_tensor_poles_not_discarded_from_metric_solution(self):
        self.assertTrue(self.r['tensor_wave_pole_present'])
        self.assertTrue(self.r['Ricci_trace_independent_of_tensor_source'])

    def test_exponential_principal_response_is_not_local(self):
        self.assertFalse(self.r['exponential_locality'])
        self.assertNotEqual(self.r['exponential_time_jet_multiplier'],'0')
        self.assertEqual(self.r['locality_solutions'],[{'mu_l':'1','mu_t':'1'}])

    def test_principal_order_comes_from_full_auxiliary_density(self):
        self.assertTrue(self.r['checks']['full_auxiliary_order_two_matches_lapse_Hessian'])
        self.assertEqual(self.r['auxiliary_mixed_derivative_degree'],1)
        self.assertEqual(self.r['auxiliary_metric_derivative_degree'],0)

    def test_healthy_matter_can_have_equal_initial_stress_but_different_stress_acceleration(self):
        self.assertIn('healthy_matter_jets',self.r,'Physical matter jet calculation missing')
        row=self.r['healthy_matter_jets']
        self.assertTrue(row['both_initial_energies_positive'])
        self.assertEqual(row['initial_energy_difference'],'0')
        self.assertEqual(row['initial_stress_difference'],'0')
        self.assertEqual(row['stress_trace_second_time_derivative'],'-24')
        self.assertTrue(row['conservation_to_computed_order'])


if __name__=='__main__':
    unittest.main()
