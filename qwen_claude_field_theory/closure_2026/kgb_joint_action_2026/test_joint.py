"""Tests of the shared-action reduction, not tests assuming theory closure."""
import unittest
import numpy as np
import joint_static as j
import third_mass as third


class JointTests(unittest.TestCase):
    def test_symbolic_logarithmic_derivative(self):
        self.assertEqual(j.symbolic_reduction()['log_derivative_residual'], 0)

    def test_both_matching_signs(self):
        for b in (.25, .75, 1.25, 4.):
            state = j.initial(1e-6, 2e-6, 1., 2., b)
            _, a, c = j.shared(.5, state, (1e-6, 2e-6))
            self.assertLess(abs(a['H']/c['H']-1), 3e-14)
            self.assertGreater(a['U'], 0)
            self.assertGreater(c['U'], 0)

    def test_actual_constraint_preservation(self):
        state = j.initial(1e-6, 2e-6, 1., 2., .75)
        px, a, b = j.shared(.5, state, (1e-6, 2e-6))
        lhs = a['H']*(a['a']+px*a['b'])
        rhs = b['H']*(b['a']+px*b['b'])
        self.assertLess(abs(lhs-rhs)/max(abs(lhs), abs(rhs)), 1e-13)

    def test_complex_step_curvature_against_central_difference(self):
        state = j.initial(1e-6, 2e-6, 1., 2., .75)
        px, pxx = j.action_jet(.5, state, (1e-6, 2e-6))
        vector = j.flow(.5, state, (1e-6, 2e-6))
        h = 1e-12
        estimate = (j.shared(.5+h, state+h*vector, (1e-6, 2e-6))[0]
                    - j.shared(.5-h, state-h*vector, (1e-6, 2e-6))[0])/(2*h)
        self.assertAlmostEqual(pxx/estimate, 1, delta=2e-7)

    def test_principal_and_stress_evaluated(self):
        state = j.initial(1e-6, 2e-6, 1., 2., .75)
        rows = j.inspect(.5, state, (1e-6, 2e-6))
        for row in rows['halos']:
            self.assertLess(row['relative_stress_error'], 5e-8)
        self.assertLess(rows['GX_relative_mismatch'], 1e-13)
        self.assertLess(rows['GXX_relative_mismatch'], 1e-13)

    def test_continuation_integrates_one_action(self):
        state=j.initial(1e-6,2e-6,.1,.3,.25)
        run=j.integrate(state,duration=.05)
        self.assertTrue(run['solver_success'])
        self.assertEqual(len(run['rows']),51)
        self.assertTrue(all(r['both_causal'] for r in run['rows']))
        self.assertLess(max(r['H_relative_mismatch'] for r in run['rows']),1e-10)
        # Independent quadrature control for the action's G(X), not assigned GX.
        from scipy.integrate import simpson
        xs=np.array([r['X'] for r in run['rows']])
        slopes=np.array([r['halos'][0]['GX'] for r in run['rows']])
        quadrature=simpson(slopes,x=xs)
        self.assertAlmostEqual(quadrature/run['rows'][-1]['G'],1,delta=1e-9)

    def test_original_second_mass_passes_next_preservation(self):
        found=third.extension(2e-6)['sign_change_roots']
        control=min(found,key=lambda r:abs(r['y']-.3))
        self.assertLess(control['HXX_relative_mismatch'],1e-11)

    def test_third_mass_next_preservation_is_not_automatic(self):
        found=third.extension(1.5e-6)['sign_change_roots']
        self.assertGreater(len(found),0)
        for r in found:
            self.assertLess(r['first_derivative_relative_error'],1e-10)
            self.assertGreater(r['normalized_log_derivative_preservation_residual'],.1)


if __name__ == '__main__': unittest.main()
