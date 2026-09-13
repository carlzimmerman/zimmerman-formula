#!/usr/bin/env python3
"""Behavior tests: forcing signs, constrained IC, zero source and linearity."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

PATH = Path(__file__).with_name('evolve.py')


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = None
        if PATH.exists():
            spec = importlib.util.spec_from_file_location('source_evolve', PATH)
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def setUp(self):
        self.assertIsNotNone(self.module, 'finite-time source integrator not implemented')
        self.model = self.module.Model(.3)

    def test_zero_source_zero_data_stays_zero(self):
        e = self.module
        np.testing.assert_array_equal(e.rhs(.1, [0., 0.], self.model, 3., 0.), [0., 0.])

    def test_constrained_initial_data_and_unreduced_euler_equations(self):
        # Dropping the source in lapse variation or the momentum IC fails this.
        e = self.module
        state = e.initial_state(self.model, 3., 1e-7)
        self.assertGreater(abs(state[1]), 0.)
        for t, st in [(0., state), (.1, np.array([2e-8, -3e-7]))]:
            c = e.coefficients(self.model, t, 3., 1e-7)
            fields = e.fields(t, st, self.model, 3., 1e-7)
            v, pdot = e.rhs(t, st, self.model, 3., 1e-7)
            n, sig, lap = (fields[x] for x in ('n', 'sigma', 'LapB'))
            equations = [
                2*(v-c['Theta']*n)+c['W']*sig,
                6*c['Theta']*v+2*c['Sigma']*n-2*c['Theta']*lap
                +2*c['r']*st[0]+c['D']*sig-c['rho'],
                c['D']*n-3*c['W']*v+c['W']*lap+(c['E']-c['C']*c['r'])*sig,
                pdot-2*c['a']**3*c['r']*(st[0]+n),
                st[1]/c['a']**3-2*lap,
            ]
            np.testing.assert_allclose(equations, 0., atol=3e-18, rtol=0.)
        self.assertLess(abs(e.rhs(0., state, self.model, 3., 1e-7)[0]), 1e-20)

    def test_forced_trajectory_scales_with_source(self):
        # Missing or nonlinear source terms/initial data break this identity.
        e = self.module
        s1 = e.integrate(self.model, 3., 1e-7, rtol=1e-10)
        s2 = e.integrate(self.model, 3., 2e-7, rtol=1e-10)
        grid = np.linspace(0., .3, 17)
        np.testing.assert_allclose(s2.sol(grid), 2*s1.sol(grid), rtol=1e-8, atol=1e-18)

    def test_zero_mode_is_not_silently_divided(self):
        with self.assertRaises(ValueError):
            self.module.coefficients(self.model, .1, 0., 1e-7)

    def test_initial_step_stays_inside_supplied_background(self):
        # SciPy 1.11's default initial-step probe can leave the domain when f0
        # is tiny. Never extrapolate the physical background to accommodate it.
        e = self.module
        model = e.Model(4.)
        sol = e.integrate(model, .3, 1e-7)
        self.assertTrue(sol.success)
        self.assertEqual(sol.t[-1], 4.)

    def test_diagnostic_result_serializes_actual_numerical_checks(self):
        import check_response
        import json
        result = check_response.one(3., 1e-6, .1, 1e-7)
        self.assertIn('checks', json.loads(json.dumps(result)))

    def test_shifted_coordinates_reproduce_original_canonical_trajectory(self):
        e = self.module
        self.assertTrue(hasattr(e, 'integrate_shifted'), 'stable canonical transform not implemented')
        original = e.integrate(self.model, 3., 1e-7, rtol=1e-11, max_step=.02)
        shifted = e.integrate_shifted(self.model, 3., 1e-7, rtol=1e-11, max_step=.02)
        tt = np.linspace(0., .3, 17)
        np.testing.assert_allclose(shifted.sol(tt), original.sol(tt), rtol=1e-7, atol=1e-19)


if __name__ == '__main__':
    unittest.main()
