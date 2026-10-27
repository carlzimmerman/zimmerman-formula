"""Independent invariants and a statistical angular-law test for the kernel."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np


_path = Path(__file__).with_name("dynamics.py")
if _path.exists():
    _spec = importlib.util.spec_from_file_location("dwarf_dynamics", _path)
    dynamics = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(dynamics)
else:
    dynamics = None


class DynamicsTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(dynamics, "dynamics kernel has not been implemented")

    def test_pair_gravity_matches_potential_gradient_and_central_torque(self):
        # A wrong force sign, mass factor, or origin monopole fails this check.
        x = np.array([[1.3, -2., .7], [-.8, .4, 2.1], [2., 1., -.3]])
        m = np.array([2.3, 4.1, 1.7])
        a, potential = dynamics.gravity(x, m, .17)
        self.assertLess(potential, 0.)
        for i in range(len(x)):
            for axis in range(3):
                plus, minus = x.copy(), x.copy()
                plus[i, axis] += 1.e-5
                minus[i, axis] -= 1.e-5
                derivative = (dynamics.gravity(plus, m, .17)[1]
                              - dynamics.gravity(minus, m, .17)[1]) / 2.e-5
                self.assertAlmostEqual(a[i, axis], -derivative / m[i], delta=2.e-12)
        np.testing.assert_allclose(np.sum(m[:, None] * a, axis=0), 0., atol=1.e-16)
        np.testing.assert_allclose(np.sum(np.cross(x, m[:, None] * a), axis=0),
                                   0., atol=1.e-16)

    def test_pair_gravity_is_translation_invariant_and_has_no_self_force(self):
        x = np.array([[1., 2., 3.], [-2., 1., .5]])
        m = np.array([3., 5.])
        a, potential = dynamics.gravity(x, m, .2)
        shifted_a, shifted_potential = dynamics.gravity(x + [8., -9., 2.], m, .2)
        np.testing.assert_allclose(a, shifted_a, rtol=1.e-14, atol=1.e-17)
        self.assertAlmostEqual(potential, shifted_potential, delta=1.e-16)
        np.testing.assert_array_equal(dynamics.gravity(x[:1], m[:1], .2)[0], [[0., 0., 0.]])
        self.assertEqual(dynamics.gravity(x[:1], m[:1], .2)[1], 0.)

    def test_compiled_gravity_matches_independent_numpy_for_unequal_masses(self):
        self.assertEqual(getattr(dynamics, "GRAVITY_BACKEND", None), "c")
        rng = np.random.default_rng(874)
        x = rng.normal(size=(43, 3))
        m = rng.uniform(.4, 3., size=len(x))
        actual_a, actual_u = dynamics.gravity(x, m, .14)
        reference_a, reference_u = dynamics._gravity_numpy(x, m, .14)
        np.testing.assert_allclose(actual_a, reference_a, rtol=4.e-14, atol=2.e-17)
        self.assertAlmostEqual(actual_u, reference_u, delta=2.e-14)

    def test_host_gradient_zero_switch_and_spherical_torque(self):
        x = np.array([[12000., -3000., 7000.], [0., 0., 0.]])
        a, phi = dynamics.host(x)
        np.testing.assert_allclose(np.cross(x, a), 0., atol=1.e-11)
        for axis in range(3):
            plus, minus = x.copy(), x.copy()
            plus[0, axis] += .01
            minus[0, axis] -= .01
            derivative = (dynamics.host(plus)[1][0] - dynamics.host(minus)[1][0]) / .02
            self.assertAlmostEqual(a[0, axis], -derivative, delta=3.e-9)
        self.assertTrue(np.all(phi < 0.))
        azero, phizero = dynamics.host(x, enabled=False)
        np.testing.assert_array_equal(azero, np.zeros_like(x))
        np.testing.assert_array_equal(phizero, np.zeros(len(x)))

    def test_scatter_central_impulses_conserve_energy_momentum_and_vector_J(self):
        x = np.array([[3., .5, -1.], [2., -.2, -.6], [2.5, 0., 0.]])
        initial = np.array([[-2., .4, .8], [1., -.2, .1], [12., -9., 3.]])
        m = np.array([1.e8, 1.e8, 3.e7])
        cold = np.array([True, True, False])
        rng = np.random.default_rng(123)
        total_hits = 0
        for _ in range(256):
            v = initial.copy()
            report = dynamics.scatter(x, v, m, cold, .00002, 2., rng)
            total_hits += report["n"]
            np.testing.assert_allclose(np.sum(m[:, None] * v, axis=0),
                                       np.sum(m[:, None] * initial, axis=0), atol=2.e-7, rtol=0.)
            self.assertAlmostEqual(np.sum(m[:, None] * v * v),
                                   np.sum(m[:, None] * initial * initial), delta=3.e-6)
            before_J = np.sum(np.cross(x, m[:, None] * initial), axis=0)
            after_J = np.sum(np.cross(x, m[:, None] * v), axis=0)
            np.testing.assert_allclose(after_J, before_J, atol=3.e-7, rtol=0.)
            np.testing.assert_array_equal(v[2], initial[2])
            self.assertLess(abs(report["delta_energy"]), 3.e-7)
            np.testing.assert_allclose(report["delta_J"], 0., atol=3.e-7)
        self.assertGreater(total_hits, 0)

    def test_compiled_scatter_matches_python_sequential_reference(self):
        self.assertTrue(hasattr(dynamics._C_BACKEND, "scatter_kernel"))
        rng = np.random.default_rng(875)
        x = rng.normal(size=(192, 3)) * 2.
        v = rng.normal(size=x.shape)
        m, cold = np.full(len(x), 1.e8), np.ones(len(x), bool)
        actual_v, reference_v = v.copy(), v.copy()
        actual = dynamics.scatter(x, actual_v, m, cold, .0001, 5., np.random.default_rng(876))
        reference = dynamics._scatter_python(x, reference_v, m, cold, .0001, 5.,
                                             np.random.default_rng(876))
        self.assertGreater(actual["n"], 1)
        self.assertEqual(actual["n"], reference["n"])
        np.testing.assert_allclose(actual_v, reference_v, atol=3.e-14, rtol=3.e-14)
        self.assertAlmostEqual(actual["max_prob"], reference["max_prob"], delta=3.e-15)

    def test_flux_weighted_central_scatter_has_isotropic_outgoing_angle(self):
        # Uniform unweighted pair directions require incoming-cosine weighting.
        # Removing that weighting biases cos(theta) and fails these moments.
        rng_geometry = np.random.default_rng(715)
        count = 40000
        q = rng_geometry.random(count)
        azimuth = rng_geometry.uniform(0., 2. * np.pi, count)
        radial = np.sqrt(1. - q * q)
        normal = np.column_stack((radial * np.cos(azimuth), radial * np.sin(azimuth), -q))
        x = np.zeros((2 * count, 3))
        x[1::2, 0] = np.arange(count) * 3.
        x[::2] = x[1::2] + .4 * normal
        v = np.zeros_like(x)
        v[::2, 2], v[1::2, 2] = .5, -.5
        m = np.full(len(x), 1.e8)
        sigma_unit = .1 * 1.98847e30 / (3.085677581491367e16 ** 2)
        weight = 3. / (4. * np.pi)
        dt = .04 / (4. * m[0] * .3 * sigma_unit * weight)
        report = dynamics.scatter(x, v, m, np.ones(len(x), dtype=bool), dt, 1.,
                                  np.random.default_rng(716))
        hit = np.any(v[::2] != np.array([0., 0., .5]), axis=1)
        cos_theta = (v[::2, 2] - v[1::2, 2])[hit]
        self.assertEqual(int(np.sum(hit)), report["n"])
        self.assertGreater(report["n"], 650)
        self.assertLess(report["n"], 950)
        self.assertLess(abs(float(np.mean(cos_theta))), .08)
        self.assertLess(abs(float(np.mean(cos_theta ** 2)) - 1. / 3.), .05)
        self.assertLess(report["max_prob"], .040000001)

    def test_scatter_refuses_unequal_cold_masses_and_unresolved_probability(self):
        x = np.array([[0., 0., 0.], [.4, 0., 0.]])
        v = np.array([[1., 0., 0.], [-1., 0., 0.]])
        cold = np.array([True, True])
        with self.assertRaisesRegex(ValueError, "equal.mass"):
            dynamics.scatter(x, v.copy(), np.array([1., 2.]), cold, .01, 1., np.random.default_rng(1))
        with self.assertRaisesRegex(RuntimeError, "probability"):
            dynamics.scatter(x, v.copy(), np.full(2, 1.e8), cold, 1., 1., np.random.default_rng(1))

    def test_scatter_refuses_resonance_domain_and_has_zero_rate_limit(self):
        x = np.array([[0., 0., 0.], [.4, 0., 0.]])
        v = np.array([[3000., 0., 0.], [-3000., 0., 0.]])
        cold, m = np.array([True, True]), np.full(2, 1.e8)
        with self.assertRaisesRegex(RuntimeError, "resonance"):
            dynamics.scatter(x, v.copy(), m, cold, .00001, 1., np.random.default_rng(1))
        before = v.copy()
        report = dynamics.scatter(x, v, m, cold, .01, 1., np.random.default_rng(1), sigma_cm2_g=0.)
        self.assertEqual(report["n"], 0)
        np.testing.assert_array_equal(v, before)


if __name__ == "__main__":
    unittest.main()
