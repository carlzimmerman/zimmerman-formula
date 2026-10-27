"""Frozen-snapshot finite-support rate and reciprocal receipt checks."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent
if (HERE / 'hazard_resolution.py').exists():
    spec = importlib.util.spec_from_file_location('hazard_audited', HERE / 'hazard_resolution.py')
    hazard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hazard)
else:
    hazard = None


class HazardTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(hazard, 'frozen-snapshot hazard audit has not been implemented')

    def test_analytic_pair_rate_and_reciprocal_aperture_energy_and_vector_J(self):
        # A wrong rate factor, energy sign, source mass, or omitted lever arm fails.
        x = np.array([[.2, .1, 0.], [.8, .1, 0.]])
        v = np.array([[2., 1., 0.], [-1., 0., 0.]])
        m, mask = np.full(2, 1000.), np.ones(2, bool)
        result, arrays = hazard.audit_snapshot(x, v, m, mask, np.zeros(3), np.zeros(3),
            supports=[1., 2.], apertures=[.5], radial_edges=[0., .5, 1.])
        z = 10. / (2 * .02 * 306601.39378555055) ** 2
        ratio = ((2 - z / (1 - z)) / 2) ** 2 / (1 + .02 ** 2 * z)
        rate = 1000. * .3 * .0002088420524663771 * 3 / np.pi * ratio * 3.
        self.assertAlmostEqual(result['supports'][0]['total_pair_rate_per_Myr'], rate, delta=rate * 1.e-13)
        self.assertAlmostEqual(result['supports'][1]['total_pair_rate_per_Myr'], rate / 8, delta=rate * 1.e-13)
        np.testing.assert_allclose(arrays['particle_hazard_per_Myr'][0], [rate, rate], rtol=1.e-13)
        np.testing.assert_array_equal(arrays['neighbor_count'][0], [1, 1])
        flux = result['supports'][0]['aperture_exchange'][0]
        self.assertAlmostEqual(flux['energy_into_inside_Msun_pc2_Myr3'], -1500. * rate, delta=rate * 1.e-9)
        self.assertAlmostEqual(flux['energy_into_outside_Msun_pc2_Myr3'], 1500. * rate, delta=rate * 1.e-9)
        np.testing.assert_allclose(flux['J_into_inside_Msun_pc2_Myr2'], [0., 0., 300. * rate], atol=1.e-10)
        self.assertLess(result['supports'][0]['relative_pair_energy_closure'], 1.e-14)
        self.assertLess(result['supports'][0]['relative_pair_vector_J_closure'], 1.e-14)

    def test_strict_support_zero_incoming_and_star_exclusion(self):
        # Boundary/coincident pairs have zero physical rate; stars never collide.
        x = np.array([[0., 0., 0.], [1., 0., 0.], [0., 0., 0.], [.5, 0., 0.]])
        v = np.array([[1., 0., 0.], [-1., 0., 0.], [1., 0., 0.], [-2., 0., 0.]])
        m, mask = np.full(4, 1000.), np.array([True, True, True, False])
        result, arrays = hazard.audit_snapshot(x, v, m, mask, np.zeros(3), np.zeros(3),
            supports=[1.], apertures=[.5], radial_edges=[0., .5, 2.])
        self.assertEqual(result['supports'][0]['strict_neighbor_pairs'], 0)
        np.testing.assert_array_equal(arrays['neighbor_count'], 0)
        np.testing.assert_array_equal(arrays['particle_hazard_per_Myr'], 0)
        v = -v
        result, _ = hazard.audit_snapshot(x[:2], v[:2], m[:2], np.ones(2, bool), np.zeros(3), np.zeros(3),
            supports=[2.], apertures=[.5], radial_edges=[0., .5, 2.])
        self.assertEqual(result['supports'][0]['strict_neighbor_pairs'], 1)
        self.assertEqual(result['supports'][0]['active_incoming_pairs'], 0)
        self.assertEqual(result['supports'][0]['total_pair_rate_per_Myr'], 0.)

    def test_independent_direct_hazard_and_receipts_translation_frame_and_batching(self):
        rng = np.random.default_rng(71106)
        x, v = rng.normal(size=(12, 3)), rng.normal(size=(12, 3))
        m, mask = np.full(12, 50.), np.ones(12, bool)
        centre, bulk = np.array([.2, -.1, .3]), np.array([.1, -.4, .6])
        result, arrays = hazard.audit_snapshot(x, v, m, mask, centre, bulk,
            supports=[.8, 1.6], apertures=[1.], radial_edges=[0., 1., 10.], batch_size=3)
        direct = np.zeros((2, 12))
        for k, h in enumerate([.8, 1.6]):
            for i in range(12):
                for j in range(i + 1, 12):
                    d, w = x[i] - x[j], v[i] - v[j]
                    r = np.linalg.norm(d)
                    if not 0 < r < h:
                        continue
                    z = np.dot(w, w) / (2 * .02 * 306601.39378555055) ** 2
                    ratio = ((2 - z / (1 - z)) / 2) ** 2 / (1 + .02 ** 2 * z)
                    rate = 50. * .3 * .0002088420524663771 * 3 / (np.pi * h ** 3) * ratio * max(-np.dot(w, d / r), 0.)
                    direct[k, i] += rate
                    direct[k, j] += rate
            self.assertAlmostEqual(result['supports'][k]['total_pair_rate_per_Myr'], .5 * direct[k].sum(), delta=1.e-16)
        np.testing.assert_allclose(arrays['particle_hazard_per_Myr'], direct, rtol=1.e-13, atol=1.e-17)
        shifted, shifted_arrays = hazard.audit_snapshot(x + [80000., -40000., 1000.], v + [100., 20., -40.],
            m, mask, centre + [80000., -40000., 1000.], bulk + [100., 20., -40.],
            supports=[.8, 1.6], apertures=[1.], radial_edges=[0., 1., 10.], batch_size=5)
        np.testing.assert_allclose(shifted_arrays['particle_hazard_per_Myr'], direct, rtol=3.e-10, atol=1.e-14)
        for a, b in zip(result['supports'], shifted['supports']):
            np.testing.assert_allclose(a['aperture_exchange'][0]['J_into_inside_Msun_pc2_Myr2'],
                                       b['aperture_exchange'][0]['J_into_inside_Msun_pc2_Myr2'], atol=1.e-12, rtol=3.e-9)
            self.assertAlmostEqual(a['aperture_exchange'][0]['energy_into_inside_Msun_pc2_Myr3'],
                                   b['aperture_exchange'][0]['energy_into_inside_Msun_pc2_Myr3'], delta=1.e-12)
        self.assertEqual(result['supports'][0]['radial'][0]['count'] + result['supports'][0]['radial'][1]['count'], 12)

    def test_domain_and_resource_limits_fail_without_partial_claim(self):
        x, v, m = np.array([[0., 0., 0.], [.2, 0., 0.], [.4, 0., 0.]]), np.ones((3, 3)), np.ones(3)
        with self.assertRaises(RuntimeError):
            hazard.audit_snapshot(x, v, m, np.ones(3, bool), np.zeros(3), np.zeros(3), supports=[1.], max_pairs=1)
        with self.assertRaises(RuntimeError):
            hazard.audit_snapshot(x, v * np.array([[1.e5], [-1.e5], [1.e5]]), m, np.ones(3, bool),
                                  np.zeros(3), np.zeros(3), supports=[1.])


if __name__ == '__main__':
    unittest.main()
