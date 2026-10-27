"""Admission checks for native binary64 full3D falcON Plummer, not defaults."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

HERE = Path(__file__).resolve().parent
if (HERE / 'falcon_native.py').exists():
    spec = importlib.util.spec_from_file_location('falcon_native_tested', HERE / 'falcon_native.py')
    falcon = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(falcon)
else:
    falcon = None


def reference(x, m, eps):
    d = x[None, :, :] - x[:, None, :]
    r2 = np.sum(d * d, axis=2) + eps ** 2
    np.fill_diagonal(r2, np.inf)
    inv = 1 / np.sqrt(r2)
    return .004498638185693768 * np.sum(d * (inv ** 3 * m[None, :])[:, :, None], axis=1), -.004498638185693768 * (inv @ m)


class FalconTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(falcon, 'isolated binary64 falcON interface missing')

    def test_native_metadata_must_be_double_plummer_and_declared_order(self):
        data = falcon.backend_metadata()
        self.assertEqual(data['real_bytes'], 8)
        self.assertEqual(data['kernel'], 'P0 Plummer, hardcoded')
        self.assertIn(data['expansion_order'], (3, 5, 6))

    def test_full3D_unequal_mass_direct_matches_plummer_and_self_exclusion(self):
        rng = np.random.default_rng(71501)
        x, m = rng.normal(size=(37, 3)) * 300., rng.uniform(.2, 3., 37) * 1000.
        a, U, phi = falcon.gravity(x, m, 10., direct=True)
        ar, pr = reference(x, m, 10.)
        np.testing.assert_allclose(a, ar, rtol=2.e-12, atol=1.e-13)
        np.testing.assert_allclose(phi, pr, rtol=2.e-12, atol=1.e-13)
        self.assertEqual(U, .5 * float(m @ phi))

    def test_direct_pair_momentum_torque_and_translation(self):
        rng = np.random.default_rng(71502)
        x, m = rng.normal(size=(71, 3)) * 20., rng.uniform(.1, 3., 71) * 1000.
        a, _, phi = falcon.gravity(x, m, 3., direct=True)
        translated = falcon.gravity(x + [80000., -50000., 1000.], m, 3., direct=True)
        np.testing.assert_allclose(a, translated[0], rtol=2.e-10, atol=1.e-12)
        np.testing.assert_allclose(phi, translated[2], rtol=2.e-11, atol=1.e-12)
        F = m[:, None] * a
        self.assertLess(np.linalg.norm(F.sum(axis=0)) / np.linalg.norm(F, axis=1).sum(), 1.e-13)
        self.assertLess(np.linalg.norm(np.cross(x, F).sum(axis=0)) /
                        np.sum(np.linalg.norm(x, axis=1) * np.linalg.norm(F, axis=1)), 1.e-13)

    def test_approximate_outputs_and_momentum_are_admitted_as_approximation(self):
        rng = np.random.default_rng(71503)
        x, m = rng.normal(size=(257, 3)) * 300., rng.uniform(.1, 3., 257) * 1000.
        a, U, phi = falcon.gravity(x, m, 10., theta=.3)
        ar, pr = reference(x, m, 10.)
        relative_L2 = np.linalg.norm(a - ar) / np.linalg.norm(ar)
        self.assertLess(relative_L2, 1.e-3)
        self.assertLess(np.linalg.norm(phi - pr) / np.linalg.norm(pr), 1.e-3)
        self.assertEqual(U, .5 * float(m @ phi))
        F = m[:, None] * a
        self.assertLess(np.linalg.norm(F.sum(axis=0)) / np.linalg.norm(F, axis=1).sum(), 1.e-13)

    def test_softened_coincident_pair_and_empty_singleton_and_validation(self):
        a, U, p = falcon.gravity(np.zeros((2, 3)), np.array([2., 3.]), .2, direct=True)
        np.testing.assert_array_equal(a, 0.)
        np.testing.assert_allclose(p, -.004498638185693768 * np.array([3., 2.]) / .2, rtol=1.e-14)
        for n in (0, 1):
            a, U, p = falcon.gravity(np.zeros((n, 3)), np.ones(n), 1.)
            self.assertEqual(U, 0.); np.testing.assert_array_equal(a, 0.); np.testing.assert_array_equal(p, 0.)
        with self.assertRaises(ValueError): falcon.gravity(np.zeros((2, 3)), np.array([0., 1.]), 1.)
        with self.assertRaises(ValueError): falcon.gravity(np.zeros((2, 3)), np.ones(2), -1.)


if __name__ == '__main__':
    unittest.main()
