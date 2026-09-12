"""Orthogonal checks of the clock-frame / dispersion distinction.

Mutations caught: replacing central covariance with raw second moment;
omitting the antisymmetric derivative in n wedge dn; zeroing recoil stress.
"""
import importlib.util
from pathlib import Path
import unittest

import sympy as s


class TriggerTests(unittest.TestCase):
    def module(self):
        path = Path(__file__).with_name("trigger.py")
        self.assertTrue(path.exists(), "the exact trigger/action computation is missing")
        spec = importlib.util.spec_from_file_location("trigger", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_single_stream_bulk_motion_has_no_dispersion(self):
        mod = self.module()
        mean, covariance = mod.moments([s.Rational(1)], [s.Matrix([2, -1, 3])])
        self.assertEqual(mean, s.Matrix([2, -1, 3]))
        self.assertEqual(covariance, s.zeros(3))

    def test_counterstreams_and_boost_invariant_covariance(self):
        mod = self.module()
        weights = [s.Rational(1, 2)] * 2
        velocities = [s.Matrix([1, 0, 0]), s.Matrix([-1, 0, 0])]
        mean, covariance = mod.moments(weights, velocities)
        _, shifted = mod.moments(weights, [v + s.Matrix([4, 3, 2]) for v in velocities])
        self.assertEqual(mean, s.zeros(3, 1))
        self.assertEqual(covariance, s.diag(1, 0, 0))
        self.assertEqual(covariance, shifted)

    def test_exact_clock_one_form_has_zero_frobenius(self):
        mod = self.module()
        t, x, y = s.symbols("t x y", real=True)
        clock = t + x*y
        normal = s.Matrix([s.diff(clock, c) * (1 + x*x) for c in (t, x, y)])
        self.assertEqual(mod.wedge_derivative(normal, (t, x, y)), 0)

    def test_rotating_flow_is_not_a_clock_gradient(self):
        mod = self.module()
        t, x, y, omega = s.symbols("t x y omega", real=True)
        normal = s.Matrix([-1, -omega*y, omega*x])
        self.assertEqual(mod.wedge_derivative(normal, (t, x, y)), -2*omega)

    def test_angular_kick_moments_preserve_number_momentum_not_dust(self):
        mod = self.module()
        v = s.Matrix(s.symbols("vx vy vz", real=True))
        kick = s.Symbol("kick", positive=True)
        mean, second = mod.isotropic_kick_moments(v, kick)
        self.assertEqual(mean, v)
        self.assertEqual(second - v*v.T, s.eye(3)*kick**2/3)


if __name__ == "__main__":
    unittest.main()
