import unittest
from analyze_results import absolute_window,combine_histories


class WindowTests(unittest.TestCase):
    def test_windows_use_absolute_time_instead_of_each_restart_fraction(self):
        rows=[dict(t=t) for t in (0,8,24,24.023,26,32)]
        selected=absolute_window(rows,24,32)
        self.assertEqual([r['t'] for r in selected],[24,24.023,26,32])

    def test_restart_duplicate_keeps_last_real_sample_without_inventing_times(self):
        a=dict(time_history=[dict(t=8,enclosed_5pct_mean_density=1),
                             dict(t=24.023,enclosed_5pct_mean_density=2)])
        b=dict(time_history=[dict(t=24.023,enclosed_5pct_mean_density=3),
                             dict(t=32,enclosed_5pct_mean_density=4)])
        result=combine_histories([a,b])
        self.assertEqual([r['t'] for r in result],[8,24.023,32])
        self.assertEqual(result[1]['enclosed_5pct_mean_density'],3)


if __name__=='__main__':
    unittest.main()
