"""Behavioral tests for frozen-position continuous-time central elastic C22."""
import importlib.util
from pathlib import Path
import time
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent
if (HERE / 'null_scatter.py').exists():
    spec = importlib.util.spec_from_file_location('null_scatter_tested', HERE / 'null_scatter.py')
    null = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(null)
else:
    null = None


class NullScatterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(null, 'continuous-time thinning C22 has not been implemented')

    def test_two_particle_first_event_probability_is_exponential(self):
        # Omitting thinning, doubling the unordered rate, or retaining the old
        # Bernoulli rule changes this independently known first-jump law.
        x = np.array([[-.25, 0., 0.], [.25, 0., 0.]])
        initial = np.array([[1., 0., 0.], [-1., 0., 0.]])
        m, mask = np.full(2, 1000.), np.ones(2, bool)
        sigma, dt, h = .3, 2., 1.
        z = 4. / (2 * .02 * 306601.39378555055) ** 2
        ratio = ((2 - z / (1 - z)) / 2) ** 2 / (1 + .02 ** 2 * z)
        hazard = 1000. * sigma * .0002088420524663771 * 3 / np.pi * ratio * 2
        expected = -np.expm1(-hazard * dt)
        rng = np.random.default_rng(72101)
        trials, hit = 5000, 0
        for _ in range(trials):
            v = initial.copy()
            result = null.scatter(x, v, m, mask, dt, h, rng, sigma)
            self.assertIn(result['n'], (0, 1))  # A reflected pair is outgoing.
            hit += result['n']
        tolerance = 5 * np.sqrt(expected * (1 - expected) / trials) + 1 / trials
        self.assertAlmostEqual(hit / trials, expected, delta=tolerance)

    def test_nonuniform_degree_graph_proposes_each_unordered_pair_uniformly(self):
        # Uniform choice of first particle would bias edges with low-degree ends.
        x = np.array([[0., 0., 0.], [.4, 0., 0.], [.8, 0., 0.], [1.7, 0., 0.]])
        graph = null.NeighborProposal(x, 1.)
        expected = {(0, 1), (0, 2), (1, 2), (2, 3)}
        self.assertEqual(graph.oriented_count, 8)
        rng = np.random.default_rng(72102)
        counts = {edge: 0 for edge in expected}
        for _ in range(20000):
            i, j = graph.draw(rng)
            self.assertNotEqual(i, j)
            edge = tuple(sorted((i, j)))
            self.assertIn(edge, expected)
            counts[edge] += 1
        for count in counts.values():
            self.assertAlmostEqual(count / 20000., .25, delta=.02)

    def test_zero_outgoing_rate_boundary_and_coincident_pairs(self):
        mask, m = np.ones(2, bool), np.full(2, 1000.)
        for x, v in (([[-.25, 0., 0.], [.25, 0., 0.]], [[-1., 0., 0.], [1., 0., 0.]]),
                     ([[0., 0., 0.], [1., 0., 0.]], [[1., 0., 0.], [-1., 0., 0.]]),
                     ([[0., 0., 0.], [0., 0., 0.]], [[1., 0., 0.], [-1., 0., 0.]])):
            x, v = np.array(x), np.array(v)
            before = v.copy()
            result = null.scatter(x, v, m, mask, 4., 1., np.random.default_rng(72103))
            self.assertEqual(result['n'], 0)
            np.testing.assert_array_equal(v, before)

    def test_energy_momentum_vector_angular_momentum_and_stars(self):
        rng = np.random.default_rng(72104)
        x, v = rng.normal(size=(15, 3)) * .2, rng.normal(size=(15, 3)) * .2
        mask = np.arange(15) < 12
        m = np.where(mask, 1.e5, 2.e4)
        before = v.copy()
        energy = lambda w: .5 * np.sum(m[:, None] * w * w)
        momentum = lambda w: np.sum(m[:, None] * w, axis=0)
        angular = lambda w: np.sum(np.cross(x, m[:, None] * w), axis=0)
        result = null.scatter(x, v, m, mask, .1, 1., rng)
        self.assertGreater(result['n'], 2)
        self.assertAlmostEqual(energy(v) / energy(before), 1., delta=2.e-14)
        np.testing.assert_allclose(momentum(v), momentum(before), rtol=0., atol=1.e-9)
        np.testing.assert_allclose(angular(v), angular(before), rtol=0., atol=1.e-9)
        np.testing.assert_array_equal(v[~mask], before[~mask])
        self.assertLess(abs(result['delta_energy']) / energy(before), 2.e-14)
        self.assertLess(np.linalg.norm(result['delta_J']), 1.e-8)
        self.assertEqual(result['method'], 'frozen-position-CTMC-thinning')
        self.assertGreaterEqual(result['proposals'], result['n'])
        self.assertEqual(result['elapsed_Myr'], .1)

    def test_galilean_and_translation_invariance(self):
        rng = np.random.default_rng(72105)
        x, v = rng.normal(size=(8, 3)) * .1, rng.normal(size=(8, 3))
        m, mask = np.full(8, 1.e5), np.ones(8, bool)
        w = v.copy(); moved = v + [100., -30., 20.]
        first = null.scatter(x, w, m, mask, .1, 1., np.random.default_rng(23))
        second = null.scatter(x + [80000., 0., -30000.], moved, m, mask,
                              .1, 1., np.random.default_rng(23))
        self.assertEqual(first['n'], second['n'])
        self.assertEqual(first['proposals'], second['proposals'])
        np.testing.assert_allclose(w, moved - [100., -30., 20.], atol=3.e-9, rtol=0.)

    def test_first_jump_rate_agrees_with_independent_bruteforce_hazard(self):
        # First-event survival is exp(-sum(lambda_ij)*dt), independently of
        # changed rates after later jumps. This catches weighting/rate errors.
        rng = np.random.default_rng(72106)
        x, v = rng.normal(size=(5, 3)) * .15, rng.normal(size=(5, 3)) * .2
        m, mask, h, sigma = np.full(5, 2.e4), np.ones(5, bool), 1., .3
        hazard = 0.
        for i in range(5):
            for j in range(i + 1, 5):
                q, w = x[i] - x[j], v[i] - v[j]
                radius = np.linalg.norm(q)
                if not 0 < radius < h:
                    continue
                z = np.dot(w, w) / (2 * .02 * 306601.39378555055) ** 2
                ratio = ((2 - z / (1 - z)) / 2) ** 2 / (1 + .02 ** 2 * z)
                hazard += m[i] * sigma * .0002088420524663771 * 3 / (np.pi * h ** 3) * ratio * max(-np.dot(w, q / radius), 0.)
        dt = .12 / hazard
        expected, trials, hits = -np.expm1(-hazard * dt), 5000, 0
        for _ in range(trials):
            result = null.scatter(x, v.copy(), m, mask, dt, h, rng, sigma)
            hits += result['n'] > 0
        tolerance = 5 * np.sqrt(expected * (1 - expected) / trials) + 1 / trials
        self.assertAlmostEqual(hits / trials, expected, delta=tolerance)

    def test_inactive_inputs_and_fail_closed_caps_and_resonance(self):
        x = np.array([[-.25, 0., 0.], [.25, 0., 0.]])
        v, m, mask = np.array([[-1., 0., 0.], [1., 0., 0.]]), np.full(2, 1000.), np.ones(2, bool)
        self.assertEqual(null.scatter(x, v.copy(), m, mask, 0., 1., np.random.default_rng(24))['n'], 0)
        with self.assertRaises(RuntimeError):
            null.scatter(x, v.copy(), m, mask, 1000., 1., np.random.default_rng(24), max_proposals=1)
        with self.assertRaises(RuntimeError):
            null.scatter(x, v * 1.e5, m, mask, 1., 1., np.random.default_rng(24))
        with self.assertRaises(ValueError):
            null.scatter(x, v.copy(), [1000., 2000.], mask, 1., 1., np.random.default_rng(24))
        for bad in (np.nan, np.inf, -1.):
            with self.assertRaises(ValueError):
                null.scatter(x, v.copy(), m, mask, bad, 1., np.random.default_rng(24))


if __name__ == '__main__':
    unittest.main()
