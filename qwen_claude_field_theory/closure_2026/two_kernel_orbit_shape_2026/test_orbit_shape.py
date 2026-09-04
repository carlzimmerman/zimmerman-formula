"""Independent falsifiers for the spherical exterior orbit-shape calculation."""
import unittest

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from orbit_shape import (acceleration, derive, inverse_L, q_flow, rar_primitive,
                         qumond_primitive, derive_qumond_action)


class OrbitShapeTests(unittest.TestCase):
    def test_qumond_action_and_constraint_preservation_are_computed(self):
        d = derive_qumond_action()
        for name, residual in d['residuals'].items():
            with self.subTest(name=name):
                self.assertEqual(sp.simplify(residual), 0)
        self.assertEqual(d['finite_k_rank'], 4)
        self.assertEqual(d['zero_k_rank'], 0)
        self.assertEqual(d['finite_k_scalar_dof'], 0)
        self.assertTrue(d['lorentzian_hessian_determinant'].is_negative)
        self.assertNotEqual(d['wrong_primitive_newton_ratio'], 1)

    def test_qumond_primitive_matches_required_action_derivative(self):
        with mp.workdps(45):
            for t in map(mp.mpf, ('.01', '.3', '2', '8')):
                # Standard action argument Z=(g_N/a0)^2=t^4.
                measured = mp.diff(qumond_primitive, t)/(4*t**3)
                self.assertLess(abs(measured*(-mp.expm1(-t))-1), mp.mpf('1e-35'))
                y = t*t/(-mp.expm1(-t))
                self.assertLess(abs(rar_primitive(t)+qumond_primitive(t)-2*t*t*y), mp.mpf('1e-35'))
            self.assertEqual(qumond_primitive(0), 0)

    def test_symbolic_action_and_orbit_residuals(self):
        result = derive()
        for name, residual in result['residuals'].items():
            with self.subTest(name=name):
                self.assertEqual(sp.simplify(residual), 0)

    def test_deep_invariant_has_opposite_signs(self):
        # Independent series inversion gives +4/3 and -1/3 respectively.
        result = derive()
        self.assertEqual(result['deep_invariant']['mu_exp'], sp.Rational(4, 3))
        self.assertEqual(result['deep_invariant']['nu_rar'], -sp.Rational(1, 3))

    def test_lambert_inverse_selects_nonzero_branch(self):
        with mp.workdps(100):
            for x in ('1e-20', '.001', '.5', '3', '50'):
                x = mp.mpf(x)
                ell = x / mp.expm1(x)
                recovered = inverse_L(ell)
                self.assertLess(abs(recovered / x - 1), mp.mpf('1e-45'))
                self.assertGreater(recovered, 0)
        for invalid in (0, 1, -1, 2):
            with self.assertRaises(ValueError):
                inverse_L(invalid)

    def test_acceleration_satisfies_implicit_constitutive_equation(self):
        gb = np.logspace(-16, 6, 221)
        g = acceleration(gb, 1, 'mu_exp')
        np.testing.assert_allclose(g * -np.expm1(-g), gb, rtol=3e-14)
        g = acceleration(gb, 1, 'nu_rar')
        np.testing.assert_allclose(g * -np.expm1(-np.sqrt(gb)), gb, rtol=3e-14)

    def test_flow_matches_force_differentiation_without_epicycle_formula(self):
        # Differentiate the force directly in log radius. This catches an
        # incorrect inversion, sign, or chain factor in the closed q-flow.
        with mp.workdps(50):
            for kernel in ('mu_exp', 'nu_rar'):
                for x in ('.07', '.5', '1.5', '4', '12'):
                    x = mp.mpf(x)
                    s0 = x * -mp.expm1(-x) if kernel == 'mu_exp' else x*x
                    def g(u):
                        s = s0 * mp.exp(-2*u)
                        if kernel == 'nu_rar':
                            return s / -mp.expm1(-mp.sqrt(s))
                        return mp.findroot(lambda y: y * -mp.expm1(-y) - s,
                                           (x * mp.mpf('.9'), x * mp.mpf('1.1')))
                    def q(u):
                        return 3 + mp.diff(g, u) / g(u)
                    q0, d0 = q(mp.mpf(0)), mp.diff(q, mp.mpf(0))
                    self.assertLess(abs(q_flow(kernel, q0) / d0 - 1), mp.mpf('1e-35'))

    def test_direct_orbits_agree_with_predicted_epicycle_ratio(self):
        # Integrate r, rdot, theta; no q expression enters the dynamics.
        for kernel, gb in (('mu_exp', 1.0), ('nu_rar', 1.0)):
            g0 = float(acceleration(gb, 1, kernel))
            angular_momentum = np.sqrt(g0)
            def rhs(t, state):
                r, vr, theta = state
                return (vr, angular_momentum**2/r**3 -
                        float(acceleration(gb/r**2, 1, kernel)),
                        angular_momentum/r**2)
            def pericenter(t, state):
                return state[1]
            pericenter.direction = 1
            solution = solve_ivp(rhs, (0, 70/np.sqrt(g0)), [1+1e-4, 0, 0],
                                 events=pericenter, rtol=2e-11, atol=2e-13,
                                 max_step=.03/np.sqrt(g0), method='DOP853')
            self.assertTrue(solution.success)
            theta = solution.y_events[0][:, 2]
            self.assertGreater(len(theta), 8)
            measured = (2*np.pi/np.mean(np.diff(theta)))**2
            h = 1e-4
            # Expected ratio from independent force derivative, not q_flow.
            gp = float(acceleration(gb/(1+h)**2, 1, kernel))
            gm = float(acceleration(gb/(1-h)**2, 1, kernel))
            expected = 3+(gp-gm)/(2*h*g0)
            self.assertAlmostEqual(measured, expected, delta=2e-7)

    def test_rar_action_primitive_varies_to_required_flux(self):
        with mp.workdps(45):
            for t in map(mp.mpf, ('.001', '.1', '1', '8')):
                y = lambda z: z*z / -mp.expm1(-z)
                derivative = mp.diff(rar_primitive, t) / mp.diff(y, t)
                self.assertLess(abs(derivative/(2*t*t)-1), mp.mpf('1e-35'))
            self.assertEqual(rar_primitive(0), 0)
            t = mp.mpf('1e-8')
            y = t*t / -mp.expm1(-t)
            self.assertLess(abs(rar_primitive(t)/y**3-mp.mpf(2)/3), mp.mpf('1e-8'))

    def test_wrong_kernel_does_not_pass_shape_null(self):
        # Both may fit q at one radius, but the derivative is incompatible.
        mu = float(q_flow('mu_exp', mp.mpf('1.5')))
        rar = float(q_flow('nu_rar', mp.mpf('1.5')))
        self.assertAlmostEqual(mu, .695895203122716, places=13)
        self.assertAlmostEqual(rar, .378215604313085, places=13)
        self.assertGreater(abs(mu-rar), .3)
        for kernel in ('mu_exp', 'nu_rar'):
            for bad in (1, 2, .5, 3):
                with self.assertRaises(ValueError):
                    q_flow(kernel, bad)
        with self.assertRaises(ValueError):
            acceleration(1, 1, 'wrong')


if __name__ == '__main__':
    unittest.main(verbosity=2)
