"""Tests-first contract for a conservative full-3D gravity accelerator."""
from concurrent.futures import ThreadPoolExecutor
import ctypes
import importlib.util
from pathlib import Path
import subprocess
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent
if (HERE / 'fast_gravity.py').exists():
    spec = importlib.util.spec_from_file_location('fast_gravity_tested', HERE / 'fast_gravity.py')
    fast = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fast)
else:
    fast = None


def independent_reference(x, m, eps):
    displacement = x[None, :, :] - x[:, None, :]
    distance2 = np.sum(displacement * displacement, axis=2) + eps * eps
    np.fill_diagonal(distance2, np.inf)
    inverse = 1. / np.sqrt(distance2)
    phi = -.004498638185693768 * (inverse @ m)
    acceleration = .004498638185693768 * np.sum(
        displacement * (inverse ** 3 * m[None, :])[:, :, None], axis=1)
    return acceleration, .5 * float(m @ phi), phi


class FastGravityTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(fast, 'fast conservative backend has not been implemented')

    def test_build_refuses_unsafe_fast_math(self):
        built = subprocess.run(['clang', '-ffast-math', '-fsyntax-only', str(HERE / 'fast_gravity.c')],
                               capture_output=True, text=True, timeout=10)
        self.assertNotEqual(built.returncode, 0, 'unsafe fast-math must be refused explicitly')
        self.assertIn('fast-math', built.stderr)

    def test_unequal_mass_three_dimensional_force_and_per_particle_potential(self):
        # Wrong source masses, signs, omitted phi, or softened monopoles fail.
        rng = np.random.default_rng(9541)
        x = rng.normal(size=(137, 3)) * 1100.
        m = rng.uniform(.3, 8., len(x)) * 1000.
        reference = independent_reference(x, m, 27.)
        for threads in (1, 2, 4):
            a, U, phi = fast.gravity(x, m, 27., threads=threads)
            np.testing.assert_allclose(a, reference[0], rtol=1.e-12,
                                       atol=1.e-13 * np.max(np.abs(reference[0])))
            np.testing.assert_allclose(phi, reference[2], rtol=1.e-12, atol=0.)
            self.assertAlmostEqual(U / reference[1], 1., delta=1.e-12)
            self.assertEqual(U, .5 * float(m @ phi))

    def test_old_compiled_reference_force_and_total_potential(self):
        old = ctypes.CDLL(str(HERE.parent / 'isolated_host_dwarf_2026_10_19' / 'direct_gravity.dylib'))
        array = np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')
        old.gravity_kernel.argtypes = [array, array, ctypes.c_size_t, ctypes.c_double,
                                      ctypes.c_double, array, ctypes.POINTER(ctypes.c_double)]
        old.gravity_kernel.restype = ctypes.c_int
        rng = np.random.default_rng(9542)
        x = rng.normal(size=(301, 3)) * 300.
        m = rng.uniform(.7, 4., len(x)) * 6000.
        aold, Uold = np.zeros_like(x), ctypes.c_double()
        self.assertEqual(old.gravity_kernel(x, m, len(m), 15., .004498638185693768,
                                            aold, ctypes.byref(Uold)), 0)
        a, U, _ = fast.gravity(x, m, 15., threads=4)
        np.testing.assert_allclose(a, aold, rtol=1.e-12, atol=1.e-14)
        self.assertAlmostEqual(U / Uold.value, 1., delta=1.e-12)

    def test_momentum_and_vector_torque_cancel_for_central_pair_forces(self):
        rng = np.random.default_rng(9543)
        x = rng.normal(size=(193, 3)) * 300.
        m = rng.uniform(.1, 9., len(x)) * 7000.
        a, _, _ = fast.gravity(x, m, 12., threads=4)
        forces = m[:, None] * a
        force_scale = np.sum(np.linalg.norm(forces, axis=1))
        torque_scale = np.sum(np.linalg.norm(x, axis=1) * np.linalg.norm(forces, axis=1))
        self.assertLess(np.linalg.norm(np.sum(forces, axis=0)) / force_scale, 1.e-13)
        self.assertLess(np.linalg.norm(np.sum(np.cross(x, forces), axis=0)) / torque_scale, 1.e-13)

    def test_force_matches_hamiltonian_gradient(self):
        rng = np.random.default_rng(9544)
        x = rng.normal(size=(17, 3)) * 30.
        m = rng.uniform(.5, 5., len(x))
        a, _, _ = fast.gravity(x, m, 3., threads=4)
        step = 1.e-3
        for index, axis in ((0, 0), (3, 1), (11, 2)):
            plus, minus = x.copy(), x.copy()
            plus[index, axis] += step
            minus[index, axis] -= step
            derivative = (fast.gravity(plus, m, 3., threads=4)[1]
                          - fast.gravity(minus, m, 3., threads=4)[1]) / (2 * step)
            self.assertAlmostEqual(-derivative / m[index], a[index, axis],
                                   delta=max(1.e-13, abs(a[index, axis]) * 2.e-8))

    def test_translation_and_noncontiguous_inputs(self):
        rng = np.random.default_rng(9545)
        raw = rng.normal(size=(96, 6)) * 1500.
        x = raw[:, ::2]
        m = np.linspace(100., 10000., len(x))
        actual = fast.gravity(x, m, 20., threads=4)
        translated = fast.gravity(x + [80000., -50000., 3000.], m, 20., threads=4)
        np.testing.assert_allclose(actual[0], translated[0], rtol=1.e-12, atol=1.e-14)
        np.testing.assert_allclose(actual[2], translated[2], rtol=1.e-12, atol=1.e-14)
        self.assertAlmostEqual(actual[1] / translated[1], 1., delta=1.e-12)

    def test_calls_are_reentrant_and_thread_partition_is_repeatable(self):
        rng = np.random.default_rng(9546)
        inputs = [(rng.normal(size=(127 + k, 3)) * 40., rng.uniform(.2, 5., 127 + k))
                  for k in range(4)]
        references = [fast.gravity(x, m, 1., threads=2) for x, m in inputs]
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda pair: fast.gravity(*pair, 1., threads=2), inputs))
        for actual, reference in zip(results, references):
            for a, b in zip(actual, reference):
                np.testing.assert_array_equal(a, b)

    def test_empty_singleton_and_softened_coincident_pair(self):
        a, U, phi = fast.gravity(np.empty((0, 3)), np.empty(0), .2)
        self.assertEqual(a.shape, (0, 3)); self.assertEqual(U, 0.); self.assertEqual(phi.shape, (0,))
        a, U, phi = fast.gravity(np.array([[9., 4., -1.]]), np.array([2.]), .2)
        np.testing.assert_array_equal(a, 0.); np.testing.assert_array_equal(phi, 0.); self.assertEqual(U, 0.)
        a, U, phi = fast.gravity(np.zeros((2, 3)), np.array([2., 3.]), .2)
        np.testing.assert_array_equal(a, 0.)
        np.testing.assert_allclose(phi, -.004498638185693768 * np.array([3., 2.]) / .2)
        self.assertAlmostEqual(U, -.004498638185693768 * 6. / .2)

    def test_invalid_inputs_and_singular_unsoftened_pair_are_rejected(self):
        x, m = np.zeros((2, 3)), np.ones(2)
        for bad in (-1, 0, 1.5, 65):
            with self.assertRaises(ValueError):
                fast.gravity(x, m, .2, threads=bad)
        for eps in (-1., np.nan, np.inf):
            with self.assertRaises(ValueError):
                fast.gravity(x, m, eps)
        with self.assertRaises(ValueError): fast.gravity(x, [1., -1.], .2)
        with self.assertRaises(ValueError): fast.gravity(x + np.nan, m, .2)
        with self.assertRaises(ValueError): fast.gravity(x, [1., np.inf], .2)
        with self.assertRaises(ValueError): fast.gravity(x, m, 0.)


if __name__ == '__main__':
    unittest.main()
