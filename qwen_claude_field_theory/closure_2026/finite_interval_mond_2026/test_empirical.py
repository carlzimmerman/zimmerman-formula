"""Tests designed to catch selection leakage, covariance and pairing errors."""
import importlib.util
import json
from pathlib import Path
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent


class EmpiricalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = HERE / 'empirical.py'
        cls.module = None
        if cls.path.exists():
            spec = importlib.util.spec_from_file_location('empirical', cls.path)
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def impl(self):
        self.assertIsNotNone(self.module, 'empirical implementation is missing')
        return self.module

    def test_selection_uses_baryons_and_has_no_velocity_argument(self):
        m = self.impl()
        b = np.array([100., 1., 10., 8., 2., 70.])
        self.assertEqual(m.select_triple(b), (1, 2, 0))

    def test_narrow_and_degenerate_triples_are_rejected(self):
        m = self.impl()
        self.assertIsNone(m.select_triple(np.ones(6)))
        self.assertIsNone(m.select_triple(np.geomspace(1, 2, 6)))
        self.assertIsNone(m.select_triple(np.array([1., 1.01, 1.02, 90., 95., 100.])))

    def test_contrast_and_covariance_have_shared_middle_point(self):
        m = self.impl()
        # At b=(1,10,100), C rows are (-1,0,1),(-1/2,1,-1/2).
        val, cov = m.contrasts(np.array([1., 10., 100.]),
                               np.array([2., 20., 200.]), np.diag([1., 2., 9.]))
        np.testing.assert_allclose(val, [2., 0.], atol=1e-14)
        np.testing.assert_allclose(cov, [[10., -4.], [-4., 4.5]], atol=1e-14)

    def test_global_acceleration_normalization_and_common_noise_cancel(self):
        m = self.impl()
        b, g = np.array([1., 4., 100.]), np.array([3., 8., 40.])
        v, c = m.contrasts(b, g, np.eye(3))
        vv, cc = m.contrasts(b, 23*g, np.eye(3)+19*np.ones((3, 3)))
        np.testing.assert_allclose(vv, v, atol=1e-13)
        np.testing.assert_allclose(cc, c, atol=1e-13)

    def test_covariance_rejects_non_psd_or_wrong_shape(self):
        m = self.impl()
        for bad in (np.eye(2), np.diag([1., -1., 1.])):
            with self.assertRaises(ValueError):
                m.contrasts([1., 2., 4.], [1., 2., 4.], bad)

    def test_bootstrap_resamples_whole_rows_and_is_reproducible(self):
        m = self.impl()
        values = np.array([[1., 2.], [4., 8.], [7., 14.]])
        aa = m.bootstrap_means(values, 99, 8)
        bb = m.bootstrap_means(values, 99, 8)
        np.testing.assert_array_equal(aa, bb)
        np.testing.assert_allclose(aa[:, 1], 2*aa[:, 0])
        self.assertTrue(np.all((aa[:, 0]>=1) & (aa[:, 0]<=7)))

    def test_wrong_empty_input_not_a_vacuous_success(self):
        m = self.impl()
        with self.assertRaises(ValueError):
            m.bootstrap_means(np.zeros((0, 2)), 99, 1)

    def test_signed_negative_gas_is_not_a_primary_sample_exclusion(self):
        m = self.impl()
        r = np.arange(1., 7.)
        b = np.geomspace(1., 100., 6)
        d = np.column_stack([r, np.full(6, 20.), np.ones(6), -np.ones(6),
                             np.sqrt(2*(r*b+1)), np.zeros((6, 3))])
        sample = [{'name': 'signed-gas', 'data': d,
                   'master': {'Q': 1, 'inc': 60., 'Rdisk': 1.}}]
        rows, excluded = m.make_rows(sample)
        self.assertEqual(len(rows), 1, excluded)
        self.assertTrue(all(f < 0 for f in rows[0]['gas_fraction']))
        gas_rows, _ = m.make_rows(sample, gas_min=.8)
        self.assertEqual(gas_rows, [])

    def test_complete_controls_serialize_as_strict_json(self):
        m = self.impl()
        r = np.arange(1., 7.)
        b = np.geomspace(1., 100., 6)
        d = np.column_stack([r, np.full(6, 20.), np.ones(6), np.ones(6),
                             np.sqrt(2*r*b), np.zeros((6, 3))])
        sample = [{'name': 'serialization-control', 'data': d,
                   'master': {'Q': 1, 'inc': 60., 'Rdisk': 1.}}]
        rows, _ = m.make_rows(sample)
        result = m.controls(rows)
        encoded = json.dumps(result, allow_nan=False)
        self.assertEqual(json.loads(encoded)['checks'], result['checks'])

    def test_single_galaxy_does_not_get_zero_width_population_intervals(self):
        m = self.impl()
        one = [{'observed_D_J_dex': [.3, .02], 'span_dex': .6,
                'covariance_D_J_dex2': [[.01, 0.], [0., .01]],
                'predicted_D_J_dex': {k: [.4, -.01] for k in m.KERNELS}}]
        summary = m.summarize(one)
        self.assertEqual(summary['status'], 'single_galaxy_no_population_inference')
        self.assertNotIn('observed_mean_percentiles_2p5_50_97p5', summary)
        with self.assertRaises(ValueError):
            m.bootstrap_means([[.3, .02]], 99, 1)


if __name__ == '__main__':
    unittest.main()
