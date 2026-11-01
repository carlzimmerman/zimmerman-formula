"""The sampled energy diagnostic must not inherit an accepted-step bound."""
import unittest

from analyze_results_v2 import sampled_energy_error


class EnergyScopeTests(unittest.TestCase):
    def test_dense_sample_error_can_exceed_accepted_step_diagnostic(self):
        first = dict(initial=dict(total=-2), max_relative_energy_error=1e-12,
                     time_history=[dict(total=-2),dict(total=-2.00000004)])
        second = dict(initial=dict(total=-2.000000000001),
                      time_history=[dict(total=-2.000000000001)])
        self.assertAlmostEqual(sampled_energy_error([first,second]),2e-8,places=15)
        self.assertGreater(sampled_energy_error([first,second]),
                           first['max_relative_energy_error'])

    def test_all_segments_use_the_original_reference(self):
        runs = [dict(initial=dict(total=-2),time_history=[dict(total=-2.1)]),
                dict(initial=dict(total=-2.1),time_history=[dict(total=-2.2)])]
        self.assertAlmostEqual(sampled_energy_error(runs),.1)


if __name__ == '__main__':
    unittest.main()
