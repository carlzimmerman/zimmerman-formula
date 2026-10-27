"""Posthoc remnant diagnostic tests; no orbit integration is performed."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np


_path = Path(__file__).with_name("remnant.py")
if _path.exists():
    _spec = importlib.util.spec_from_file_location("dwarf_remnant", _path)
    remnant = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(remnant)
else:
    remnant = None


def remnant_and_tails():
    rng = np.random.default_rng(192)
    # The majority of stars and mass lie in dispersed debris, not the remnant.
    core_x = rng.normal(size=(144, 3)) * 20.
    directions = rng.normal(size=(896, 3))
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    tails_x = directions * rng.uniform(5000., 25000., size=(896, 1)) + [30000., 0., 0.]
    x = np.r_[core_x, tails_x]
    v = np.r_[rng.normal(size=(144, 3)) * .2, rng.normal(size=(896, 3)) * 30.]
    cold = np.r_[np.arange(144) < 128, np.arange(896) < 512]
    m = np.where(cold, 10000., 1000.)
    return x, v, m, cold


class RemnantTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(remnant, "posthoc remnant diagnostic is not implemented")

    def test_recovers_compact_remnant_despite_dominant_dispersed_stellar_tails(self):
        x, v, m, cold = remnant_and_tails()
        shift, boost = np.array([88000., -42000., 3000.]), np.array([21., -13., 4.])
        result = remnant.diagnose_remnant(x + shift, v + boost, m, cold, 40.)
        self.assertLess(np.linalg.norm(np.asarray(result["centre"]) - shift), 20.)
        self.assertEqual(result["M300"], 1280000.)
        self.assertEqual(result["star_count300"], 16)
        self.assertGreater(result["bound_M300"], 1270000.)
        self.assertGreater(result["any_centre_M300_upper_bound_Msun"], result["M300"] - 1.)
        self.assertIn("posthoc", result["interpretation"].lower())

    def test_centre_is_translation_invariant_deterministic_and_does_not_mutate(self):
        x, v, m, cold = remnant_and_tails()
        before = [a.copy() for a in (x, v, m, cold)]
        a = remnant.remnant_centre(x, m, cold, 40.)
        shift = np.array([88000., -42000., 3000.])
        b = remnant.remnant_centre(x + shift, m, cold, 40.)
        np.testing.assert_allclose(b - shift, a, atol=2.e-5, rtol=0.)
        np.testing.assert_array_equal(a, remnant.remnant_centre(x, m, cold, 40.))
        for actual, original in zip((x, v, m, cold), before):
            np.testing.assert_array_equal(actual, original)

    def test_density_peak_can_be_instantaneously_self_unbound(self):
        rng = np.random.default_rng(193)
        x = rng.normal(size=(64, 3)) * 30.
        v = rng.normal(size=(64, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; v *= 100.
        cold, m = np.ones(64, bool), np.full(64, 100.)
        result = remnant.diagnose_remnant(x, v, m, cold, 10.)
        self.assertEqual(result["M300"], 6400.)
        self.assertEqual(result["bound_M300"], 0.)
        self.assertEqual(result["bound_star_count300"], 0)
        self.assertFalse(result["instantaneously_self_bound_remnant"])


if __name__ == "__main__":
    unittest.main()
