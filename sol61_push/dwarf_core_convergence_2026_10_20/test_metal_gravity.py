"""Optional GPU contract: explicitly emulated precision, never plain FP32."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
from pathlib import Path
import unittest

import numpy as np
from fast_gravity import gravity as cpu_gravity


HERE = Path(__file__).resolve().parent
if (HERE / 'metal_gravity.py').exists():
    spec = importlib.util.spec_from_file_location('tested_metal_gravity', HERE / 'metal_gravity.py')
    gpu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gpu)
else:
    gpu = None


class MetalGravityTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gpu, 'optional Metal gravity has not been implemented')

    def test_actual_library_metadata_and_three_component_coordinates(self):
        metadata = gpu.backend_metadata()
        self.assertEqual(metadata.get('abi_version'), 2)
        self.assertIn(metadata.get('newton_corrections'), (1, 2))
        self.assertEqual(len(metadata.get('library_sha256', '')), 64)
        self.assertTrue(callable(getattr(gpu, '_pack_particles', None)))
        x = np.array([[80000.123456789, -30000.987654321, 2000.123456789]])
        packed = gpu._pack_particles(x, np.array([3000.123456789]))
        recovered = (packed[:, [0, 2, 4]].astype(np.float64)
                     + packed[:, [1, 3, 5]].astype(np.float64) + packed[:, 8:11].astype(np.float64))
        np.testing.assert_array_equal(recovered, x)
        self.assertGreater(np.count_nonzero(packed[:, 8:11]), 0)

    def compare(self, x, m, eps):
        a, U, phi = gpu.gravity(x, m, eps)
        reference = cpu_gravity(x, m, eps)
        relative = np.linalg.norm(a - reference[0], axis=1) / np.maximum(np.linalg.norm(reference[0], axis=1), 1.e-100)
        self.assertLess(float(np.max(relative)), 1.e-11)
        self.assertLess(float(np.max(np.abs((phi - reference[2]) / reference[2]))), 1.e-11)
        self.assertLess(abs(U / reference[1] - 1.), 1.e-11)
        self.assertEqual(U, .5 * float(m @ phi))
        return a, U, phi

    def test_three_dimensional_unequal_mass_precision(self):
        rng = np.random.default_rng(99171)
        x = rng.normal(size=(193, 3)) * [900., 400., 200.]
        m = rng.uniform(.2, 5., len(x)) * 4000.
        self.compare(x, m, 7.)

    def test_dense_remnant_with_distant_tails_and_large_translation(self):
        rng = np.random.default_rng(99172)
        x = np.r_[rng.normal(size=(157, 3)) * 50., rng.normal(size=(90, 3)) * 100000.]
        x = x[rng.permutation(len(x))] + [80000., -30000., 2000.]
        m = rng.uniform(.5, 3., len(x)) * 2000.
        self.compare(x, m, 5.)

    def test_first_particle_far_from_a_dense_remnant(self):
        # The reference origin must not lose close-pair information when that
        # identity becomes an escaped tail particle at late times.
        rng = np.random.default_rng(99176)
        compact = rng.normal(size=(63, 3)) * [2., 3., 1.] + [80000.12345, -30000.9876, 2000.42]
        x = np.r_[[[-400000.87654, 500000.12346, -200000.35]], compact]
        m = rng.uniform(.5, 3., len(x)) * 2000.
        self.compare(x, m, 2.)

    def test_two_body_softened_force_and_self_exclusion(self):
        x = np.array([[1., 2., 3.], [-5., 7., 2.]])
        m = np.array([2., 3.])
        a, U, phi = self.compare(x, m, .3)
        np.testing.assert_allclose(m[0] * a[0], -m[1] * a[1], rtol=1.e-11, atol=1.e-14)
        self.assertLess(U, 0.); self.assertTrue(np.all(phi < 0.))

    def test_vector_momentum_torque_and_translation(self):
        rng = np.random.default_rng(99173)
        x = rng.normal(size=(129, 3)) * 100.
        m = rng.uniform(.3, 4., len(x)) * 1000.
        a, U, phi = self.compare(x, m, 5.)
        shifted = gpu.gravity(x + [80000., -40000., 9000.], m, 5.)
        np.testing.assert_allclose(a, shifted[0], rtol=1.e-11, atol=1.e-13)
        f = m[:, None] * a
        self.assertLess(np.linalg.norm(f.sum(axis=0)) / np.linalg.norm(f, axis=1).sum(), 1.e-11)
        self.assertLess(np.linalg.norm(np.cross(x, f).sum(axis=0)) /
                        np.sum(np.linalg.norm(x, axis=1) * np.linalg.norm(f, axis=1)), 1.e-11)

    def test_concurrent_calls_have_separate_buffers(self):
        rng = np.random.default_rng(99174)
        cases = [(rng.normal(size=(81 + k, 3)) * 80., rng.uniform(.3, 2., 81 + k)) for k in range(2)]
        reference = [gpu.gravity(x, m, 3.) for x, m in cases]
        with ThreadPoolExecutor(max_workers=2) as pool:
            actual = list(pool.map(lambda pair: gpu.gravity(*pair, 3.), cases))
        for one, two in zip(actual, reference):
            for a, b in zip(one, two): np.testing.assert_array_equal(a, b)

    def test_invalid_inputs_and_zero_or_singleton(self):
        a, U, phi = gpu.gravity(np.empty((0, 3)), np.empty(0), 1.)
        self.assertEqual(a.shape, (0, 3)); self.assertEqual(U, 0.); self.assertEqual(phi.size, 0)
        a, U, phi = gpu.gravity(np.zeros((1, 3)), np.ones(1), 1.)
        np.testing.assert_array_equal(a, 0.); self.assertEqual(U, 0.); np.testing.assert_array_equal(phi, 0.)
        with self.assertRaises(ValueError): gpu.gravity(np.zeros((2, 3)), np.ones(2), -1.)
        with self.assertRaises(ValueError): gpu.gravity(np.zeros((2, 3)) + np.nan, np.ones(2), 1.)
        with self.assertRaises(ValueError): gpu.gravity(np.zeros((2, 3)), [1., -1.], 1.)


if __name__ == '__main__':
    unittest.main()
