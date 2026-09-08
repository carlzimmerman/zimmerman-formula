"""Catch wrong signs, fixed-k claims, and skipped exceptional reductions."""
import importlib.util
import unittest
import sympy as s


class SpatialKernelTests(unittest.TestCase):
    def data(self):
        self.assertIsNotNone(importlib.util.find_spec('spatial_kernel_gate'),
                             'Missing action-derived general spatial-kernel gate')
        import spatial_kernel_gate as gate
        return gate.derive()

    def test_static_law_and_slip_fix_matrix_not_its_stiffness(self):
        d = self.data()
        self.assertEqual(d['static']['cross'], d['Q'])
        self.assertEqual(s.simplify(d['static']['lapse']-d['Q']
                                   -d['M']**2*d['k']**2/d['a']**2*(d['alpha']-1)), 0)

    def test_general_kernel_kinetic_from_eliminating_auxiliaries(self):
        d = self.data()
        Q,Z,D,q = [d[x] for x in ('Q','Z','D','q')]
        expected = -6*Z-9*Z**2/D-9*Z**2*q**2/(2*Q)
        self.assertEqual(s.factor(d['kinetic']-expected), 0)
        self.assertTrue(all(r == 0 for r in d['residuals']))

    def test_unbounded_kernel_has_wrong_kinetic_either_sign(self):
        d = self.data()
        expected = -6*d['Z']-9*d['Z']**2/d['D']
        self.assertEqual(s.simplify(d['large_positive_Q_kinetic']-expected), 0)
        self.assertEqual(s.simplify(d['large_negative_Q_kinetic']-expected), 0)

    def test_negative_bounded_kernel_really_passes_one_gate(self):
        d = self.data()
        self.assertEqual(d['canonical_negative']['kinetic'], 3)
        self.assertEqual(d['canonical_negative']['UV_speed2'], s.Rational(1,3))
        self.assertEqual(d['canonical_negative']['gravity_scalar_pairs_claimed'], None)

    def test_spatial_realizer_retains_inverse_laplacian_terms(self):
        d = self.data()
        self.assertEqual(s.simplify(d['realizer']['I_linear']
                         -4*d['k']**2/d['a']**2*(d['n']+d['z'])), 0)
        self.assertEqual(s.factor(d['realizer']['reconstructed_Q']-d['Q']), 0)

    def test_zero_stiffness_not_substituted_into_inverse_Q(self):
        d = self.data()['zero_stiffness']
        self.assertEqual(d['rank'], 6)
        self.assertEqual(d['matter_pairs'], 1)
        self.assertEqual(d['matter_velocity'], 0)
        self.assertEqual(len(d['explicit_constraint_time_derivatives']), 3)

    def test_existing_action_is_exact_positive_kernel_control(self):
        d = self.data()
        self.assertEqual(d['old_action_residual'], 0)

    def test_fixed_clock_kernel_fails_on_constant_potential_matter(self):
        c = self.data()['constant_potential']
        self.assertEqual(c['fixed_fixture_kinetic'], -6)
        self.assertTrue(all(r == 0 for r in c['background_residuals']))

    def test_proper_clock_derivative_changes_that_same_counterexample(self):
        d = self.data()
        self.assertEqual(d['constant_potential']['adaptive_fixture_kinetic'], 3)
        self.assertEqual(s.simplify(d['adaptive']['kinetic']
                                   -(12*d['Z']-9*d['Z']**2/d['D'])), 0)
        self.assertEqual(d['adaptive']['source_coefficient_residual'], 0)
        self.assertEqual(d['adaptive']['density'], -3*d['q']*d['Z']*d['ud'])

    def test_clock_coefficient_is_a_computed_family_not_a_fixed_answer(self):
        d = self.data()
        f = d['adaptive_family']
        b = f['b']
        self.assertEqual(s.simplify(f['kinetic']
            -d['Z']*(9/(2*b)-6-9*d['Z']/d['D'])), 0)
        self.assertEqual(s.factor(f['proper_Q']+2*b*f['tau_T']/(3*f['Nbar'])), 0)

    def test_zero_enthalpy_is_rebuilt_from_canonical_action(self):
        d = self.data()['zero_enthalpy']
        self.assertEqual(d['matter_speed2'], 1)
        self.assertEqual(d['lapse_variation'], 0)
        self.assertEqual(d['trace_variation'], 0)
        self.assertEqual(d['speed_matching_b'], [s.Rational(9,32)])


if __name__ == '__main__':
    unittest.main()
