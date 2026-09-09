"""Check independent physical combinations and degenerate transmission sources."""
import importlib.util
import unittest


class PhysicalLimitTests(unittest.TestCase):
    def result(self):
        self.assertIsNotNone(importlib.util.find_spec('ic44_physical_limits'))
        import ic44_physical_limits as module
        return module.derive()

    def test_compact_physical_jumps_match_the_action_solution(self):
        d=self.result()
        self.assertTrue(all(v==0 for v in d['compact_identity_errors'].values()))

    def test_zero_field_and_shift_characteristic_require_zero_reaction(self):
        d=self.result()
        self.assertEqual(d['zero_u_reaction_coefficient'], 1)
        self.assertEqual(d['zero_V_reaction_coefficient'], 1)

    def test_joint_scaling_controls_the_computed_jump_family(self):
        d=self.result()
        self.assertEqual(d['scaled_physical_lapse_limit_error'], 0)
        self.assertEqual(d['scaled_spatial_metric_limit_error'], 0)


if __name__=='__main__':unittest.main()
