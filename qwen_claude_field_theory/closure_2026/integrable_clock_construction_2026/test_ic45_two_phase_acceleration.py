"""Test actual inactive-clock response rather than a prescribed multiplier."""
import importlib.util
import unittest


class TwoPhaseAccelerationTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic45_two_phase_acceleration'))
        import ic45_two_phase_acceleration as module
        return module

    def test_matter_frame_factors_follow_from_physical_minimal_coupling(self):
        d=self.module().matter_identities()
        self.assertTrue(all(value==0 for value in d.values()))

    def test_two_phase_second_constraint_response_is_computed_not_pinned(self):
        d=self.module().experiment(dps=40,degree=6)
        self.assertLess(float(d['max_second_constraint_residual']),1e-20)
        self.assertGreater(abs(float(d['inactive_wtt_second_spatial_derivative'])),1e-5)
        self.assertLess(float(d['operator_reference_error']),1e-25)
        # Bulk equations can pass while the moving boundary fails.
        self.assertGreater(float(d['necessary_second_interface_residual']),1e-5)

    def test_compatible_edge_retains_a_nonzero_inactive_clock_response(self):
        d=self.module().experiment(dps=40,degree=6,boundary='compatible')
        self.assertLess(float(d['max_second_constraint_residual']),1e-20)
        self.assertLess(float(d['necessary_second_interface_residual']),1e-20)
        self.assertGreater(abs(float(d['inactive_wtt_sixth_spatial_derivative'])),1e-5)


if __name__=='__main__':unittest.main()
