"""Bounded branch checks; positive high-k c^2 is not a no-ghost certificate."""
import importlib.util
import unittest
from background_evolve import Model


class BranchContinuation(unittest.TestCase):
    def run_branch(self, H, q, direction, **kwargs):
        self.assertIsNotNone(importlib.util.find_spec('branch_continuation'),
                             'missing same-action alternate-branch continuation')
        from branch_continuation import continue_branch
        return continue_branch(H, q, direction, **kwargs)

    def test_small_steps_keep_fixed_coefficients_and_constraints(self):
        for H, q in ((.6967532055475008, .9477017173736229),
                     (.6967560366493584, -.9477017537279459)):
            for direction in (-1, 1):
                with self.subTest(q=q, direction=direction):
                    result = self.run_branch(H, q, direction, efolds=.001)
                    self.assertEqual(result['outcome'], 'requested_loga_bound')
                    first, last = result['samples'][0], result['samples'][-1]
                    self.assertAlmostEqual(first['coefficient_q'], Model(.01).background(0.)['q'])
                    self.assertGreater(abs(first['q']-first['coefficient_q']), .01)
                    self.assertGreater(direction*last['tau'], 0.)
                    self.assertLess(result['max_scaled_constraint'], 1e-8)
                    self.assertGreater(first['clock_cs2'], 0.)
                    self.assertAlmostEqual(first['high_k'][1]['radiation_cs2'], 1/3, delta=1e-5)

    def test_known_low_q_branch_is_not_reported_as_healthy(self):
        result = self.run_branch(.5191118192004086, .9078321505772312, 1, efolds=.001)
        self.assertEqual(result['outcome'], 'high_k_negative_clock')
        self.assertFalse(result['full_health_established'])

    def test_direction_is_explicit(self):
        with self.assertRaises(ValueError):
            self.run_branch(.6967532055475008, .9477017173736229, 0)


if __name__ == '__main__':
    unittest.main()
