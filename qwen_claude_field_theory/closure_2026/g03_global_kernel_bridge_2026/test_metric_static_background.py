"""Break-sensitive checks of the ungauged static action and solved backgrounds."""
import importlib.util
import unittest

AVAILABLE = importlib.util.find_spec('metric_static_background') is not None


class ImplementationTest(unittest.TestCase):
    def test_background_solver_exists(self):
        self.assertTrue(AVAILABLE, 'The nonlinear background has not been implemented')


@unittest.skipUnless(AVAILABLE, 'not implemented')
class BackgroundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_static_background as model
        cls.model = model
        cls.r = model.audit()

    def test_radial_lapse_was_varied_and_constraint_is_preserved(self):
        # Deleting the B equation, or fixing B before variation, breaks this.
        self.assertEqual(len(self.r['Euler_Lagrange_equations']), 3)
        self.assertEqual(self.r['radial_Noether_identity_residual'], '0')
        self.assertEqual(self.r['constraint_propagation_residual'], '0')

    def test_reduced_EH_density_has_the_correct_boundary_term(self):
        self.assertEqual(self.r['EH_integration_by_parts_residual'], '0')

    def test_vanishing_kernel_recovers_rindler(self):
        # A constant, N linear and Lambda=0 is a hand-checkable GR solution.
        self.assertEqual(self.r['GR_Rindler_residuals'], ['0', '0', '0'])

    def test_highest_derivative_matrix_tracks_loss_of_ellipticity(self):
        self.assertEqual(self.r['determinant_identity_residual'], '0')
        self.assertEqual(self.r['zero_field_determinant'], '0')
        self.assertNotEqual(self.r['unit_field_determinant'], '0')

    def test_nonlinear_backgrounds_satisfy_all_equations_at_two_tolerances(self):
        for row in self.r['backgrounds']:
            with self.subTest(row=row['label']):
                self.assertTrue(row['integration_success'])
                self.assertLess(row['max_scaled_EL_residual'], 1e-8)
                self.assertLess(row['max_constraint_drift'], 1e-8)
                self.assertLess(row['refinement_relative_difference'], 1e-7)
                self.assertGreater(row['minimum_y'], 0)
                self.assertGreater(row['minimum_N'], 0)
                self.assertGreater(row['minimum_A'], 0)

    def test_solved_background_does_not_accidentally_restore_causal_GR_symbol(self):
        for row in self.r['backgrounds']:
            self.assertLess(row['transverse_C4_at_unit_k'], 0)
        self.assertTrue(self.r['principal_crosscheck'])

    def test_no_real_seed_and_zero_field_are_not_silently_certified(self):
        with self.assertRaises(ValueError):
            self.model.solve_background(1., 100., span=.01)
        with self.assertRaises(ValueError):
            self.model.solve_background(0., 0., span=.01)

    def test_local_solution_is_not_mistaken_for_a_compact_static_vacuum(self):
        self.assertIn('compact_static_obstruction', self.r)
        row = self.r['compact_static_obstruction']
        self.assertEqual(row['plane_identity_residual'], '0')
        self.assertEqual(row['full_trace_identity_residual'], '0')
        self.assertTrue(row['framework_ratio_excluded'])
        self.assertEqual(row['kernel_bound_remainder'], '(y**2 + 2*y + 2)*exp(-y)')

    def test_regulated_boundary_variation_cancels(self):
        self.assertIn('Dirichlet_boundary_variation_residual',self.r)
        self.assertEqual(self.r['Dirichlet_boundary_variation_residual'],'0')

    def test_physical_matter_stress_jets_on_curved_background(self):
        self.assertIn('curved_matter_jets',self.r)
        row=self.r['curved_matter_jets']
        self.assertTrue(row['initial_stress_and_first_derivative_equal'])
        self.assertEqual(row['proper_time_stress_acceleration_coefficient'],'-24')
        self.assertTrue(row['covariant_Ward_residuals_zero'])
        self.assertEqual(row['initial_energy_difference'],'0')


if __name__ == '__main__':
    unittest.main()
