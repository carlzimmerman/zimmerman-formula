"""Independent identities and finite residuals for common constraint data."""
import importlib.util
import unittest
import sympy as s

AVAILABLE=importlib.util.find_spec('metric_shared_data') is not None


class ImplementationTest(unittest.TestCase):
    def test_shared_data_construction_exists(self):
        self.assertTrue(AVAILABLE,'Nonlinear common initial-data calculation missing')


@unittest.skipUnless(AVAILABLE,'not implemented')
class SharedDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import metric_shared_data as model
        cls.r=model.audit()

    def test_boundary_map_is_computed_and_degeneracy_not_ignored(self):
        chi=s.symbols('chi',real=True)
        det=s.sympify(self.r['limit']['computed_determinant'],locals={'chi':chi})
        self.assertEqual(s.factor(det+4*chi/(3*(1-chi))),0)
        self.assertEqual(self.r['limit']['chi_zero_boundary_rank'],2)
        self.assertTrue(self.r['limit']['derived_principal_matrix_agrees'])

    def test_exterior_tail_and_positive_source_bound_are_exact(self):
        r=self.r['limit']
        self.assertEqual(r['exterior_solution_identity_residual'],'0')
        self.assertEqual(r['uniform_exterior_bound_coefficient'],'1/8')
        self.assertEqual(r['mean_constraint_residual'],'0')

    def test_shared_sources_come_from_same_positive_KG_action(self):
        r=self.r['matter']
        self.assertEqual(r['rho_difference'],'0')
        self.assertEqual(r['trace_difference'],'0')
        self.assertEqual(r['momentum_difference'],'0')
        self.assertTrue(r['first_stress_derivatives_agree'])

    def test_nonlinear_operator_linearizes_to_published_operator(self):
        self.assertEqual(self.r['linearization_residuals'],['0']*12)

    def test_actual_nonlinear_shared_constraints_and_volume(self):
        for row in self.r['common_data']:
            self.assertTrue(row['success'])
            self.assertLess(row['boundary_residual'],1e-8)
            self.assertLess(row['volume_relative_residual'],1e-7)
            self.assertLess(row['max_constraint_residual'],1e-6)
            self.assertLess(row['refinement_difference'],1e-6)
            self.assertGreater(row['minimum_y'],0)
            self.assertGreater(row['minimum_N'],0)

    def test_fixed_canonical_matter_preservation(self):
        for row in self.r['common_data']:
            p=row['preservation']
            self.assertEqual(p['computed_boundary_rank'],3)
            self.assertLess(p['boundary_residual'],1e-9)
            self.assertLess(p['current_volume_mean_residual'],1e-7)
            self.assertLess(p['finite_difference_ODE_residual'],1e-6)
            self.assertLess(p['refinement_difference'],1e-6)
            self.assertLess(p['fixed_p_directional_derivative_residual'],1e-6)
            self.assertTrue(p['same_for_both_matter_states'])


if __name__=='__main__':
    unittest.main()
