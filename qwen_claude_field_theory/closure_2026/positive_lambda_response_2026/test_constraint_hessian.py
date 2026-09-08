"""Catch a missing clock-volume term and incomplete homogeneous preservation."""
import importlib.util
import unittest
import sympy as s


class ConstraintHessianTests(unittest.TestCase):
    def data(self):
        self.assertIsNotNone(importlib.util.find_spec('constraint_hessian'))
        import constraint_hessian
        return constraint_hessian.derive()

    def test_canonical_shift_keeps_its_time_dependent_generator(self):
        d=self.data()
        self.assertEqual(s.simplify(d['clock_correction']-2*d['tau_dot']*d['volume']/3),0)
        self.assertEqual(d['canonical_primary_residual'],0)

    def test_actual_mixed_hessian_is_invertible_despite_zero_lapse_diagonal(self):
        d=self.data()
        self.assertEqual(d['weak_hessian'][0,0],0)
        self.assertEqual(s.simplify(d['weak_hessian'].det()
            +9*d['volume']**2*d['rho']**2),0)

    def test_constraints_are_generated_and_all_multipliers_preserved(self):
        d=self.data()
        self.assertEqual(d['poisson_rank'],4)
        self.assertEqual(d['first_class'],0)
        self.assertEqual(d['homogeneous_pairs'],1)
        self.assertTrue(all(s.simplify(x)==0 for x in d['preservation_residuals']))

    def test_expansion_is_derived_not_deleted(self):
        d=self.data()
        self.assertEqual(s.simplify(d['Hubble']+d['tau']/(3*d['m'])),0)
        self.assertEqual(s.simplify(d['lapse']-d['tau_dot']/(3*d['rho'])),0)
        self.assertTrue(all(s.simplify(x)==0 for x in d['background_residuals']))

    def test_same_positive_lambda_background_requires_zero_lapse_drift(self):
        d=self.data()
        self.assertEqual(d['positive_lambda_lapse_drift'],0)
        self.assertGreater(len(d['primary_constraints']),0)
        self.assertGreater(len(d['secondary_constraints']),0)

    def test_exact_vacuum_is_not_counted_from_regular_inverse_density(self):
        d=self.data()
        self.assertEqual(d['vacuum']['raw_constraints'],[0,0])
        self.assertIsNone(d['vacuum']['count_claimed'])


if __name__=='__main__': unittest.main()
