"""Orbital windows are time-weighted and never silently truncate coverage."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np


path = Path(__file__).with_name("analyse_resolution.py")
if path.exists():
    spec = importlib.util.spec_from_file_location("resolution_analysis_tested", path)
    analysis = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analysis)
else:
    analysis = None


class WindowTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(analysis, "standalone resolution analysis is missing")

    def test_pericentres_exclude_uncompleted_endpoint_and_small_ripples(self):
        t = np.arange(0., 4601., 10.)
        radius = 50000. + 25000. * np.cos(2. * np.pi * t / 1400.)
        radius += 30. * np.sin(2. * np.pi * t / 40.)
        peri = analysis.find_pericentres(t, radius)
        self.assertEqual(len(peri), 3)
        np.testing.assert_allclose([p["time_Myr"] for p in peri], [700., 2100., 3500.], atol=2.)
        self.assertEqual([p["number"] for p in peri], [1, 2, 3])

    def test_irregular_window_mean_interpolates_boundaries_and_integrates_time(self):
        t = np.array([0., 1., 4.])
        result = analysis.window_statistics(t, 2. * t + 1., .5, 3.)
        self.assertTrue(result["complete"])
        self.assertAlmostEqual(result["mean"], 4.5)
        self.assertAlmostEqual(result["temporal_std"], 5. / np.sqrt(12.))
        self.assertFalse(result["temporal_scatter_is_confidence_interval"])
        vectors = analysis.window_statistics(t, np.c_[t, 2. * t], 0., 4.)
        np.testing.assert_allclose(vectors["mean"], [2., 4.])

    def test_incomplete_window_and_large_recording_gap_are_not_averaged(self):
        missing_end = analysis.window_statistics([0., 1., 2.], [2., 2., 2.], 1., 3.)
        self.assertFalse(missing_end["complete"])
        self.assertIsNone(missing_end["mean"])
        self.assertAlmostEqual(missing_end["coverage_fraction"], .5)
        missing_middle = analysis.window_statistics([0., 1., 9., 10.], [1., 1., 1., 1.],
                                                   0., 10., max_gap_Myr=2.)
        self.assertFalse(missing_middle["complete"])
        self.assertIsNone(missing_middle["mean"])
        self.assertEqual(missing_middle["reason"], "recording_gap")

    def test_last_complete_cycle_uses_last_two_observed_pericentres(self):
        t = np.arange(0., 4601., 10.)
        radius = 50000. + 25000. * np.cos(2. * np.pi * t / 1400.)
        mass = 100. - t / 100.
        result = analysis.orbital_windows(t, radius, mass)
        cycle = result["last_complete_cycle"]
        self.assertTrue(cycle["complete"])
        self.assertEqual(cycle["pericentre_numbers"], [2, 3])
        np.testing.assert_allclose(cycle["interval_Myr"], [2100., 3500.], atol=1.e-7)
        self.assertAlmostEqual(cycle["mean"], 72., places=7)
        first_post = result["post_pericentre_windows"][0]
        np.testing.assert_allclose(first_post["interval_Myr"], [800., 1000.], atol=1.e-7)
        self.assertAlmostEqual(first_post["mean"], 91., places=7)
        short = analysis.orbital_windows(t[:101], radius[:101], mass[:101])
        self.assertFalse(short["last_complete_cycle"]["complete"])

    def test_comparison_kind_uses_arguments_and_never_calls_mixed_changes_matched(self):
        a = dict(ncold=4096, eps=10., h=25., dt=.5, seed=87319, host=True,
                 collisionless=False, duration=10000., backend="cpu", threads=4, collision_seed=None)
        b = dict(a, ncold=8192)
        same, kind, changes = analysis.control_difference(a, b)
        self.assertTrue(same)
        self.assertEqual(kind, "ncold")
        self.assertEqual(changes, ["ncold"])
        b["eps"] = 5.
        same, kind, changes = analysis.control_difference(a, b)
        self.assertFalse(same)
        self.assertEqual(kind, "mixed_controls")
        self.assertEqual(set(changes), {"ncold", "eps"})
        method_control = dict(a, collision_method="ctmc")
        same, kind, changes = analysis.control_difference(a, method_control)
        self.assertTrue(same)
        self.assertEqual(kind, "collision_method")

    def common_metadata(self, digest='a'*64, reference_eps=10.):
        return dict(common_initial_state=True, relative_state_sha256=digest,
                    sampling='nested scrambled6D Sobol; independent species streams; antithetic phase pairs',
                    cold_phase_seed=87319,stellar_phase_seed=87320,
                    reference_softening_pc=reference_eps,cold_mass=30804000.,stellar_mass=574272.,
                    cold=dict(virial_ratio=.2,ordered_fraction=.1),
                    stars=dict(virial_ratio=1.,ordered_fraction=0.))

    def case_fixture(self, args, ic):
        return dict(args=args,initial_conditions=ic,
            final=dict(M100=1.,M300=2.,profile=dict(edges=[5.,10.],density=[1.]),
                       screen=dict(r_screen_pc=None)),
            late_window=dict(M300=dict(mean=2.),profile=dict(density=dict(complete=False))))

    def test_same_N_common_controls_require_actual_state_hash_not_initial_path(self):
        # Equal seed/path conventions must not admit different physical arrays.
        a=dict(ncold=16384,eps=10.,h=25.,dt=.5,seed=87319,backend='tile2',initial='one/initial.npz')
        b=dict(a,eps=20.,initial='another/copy.npz')
        ca=self.case_fixture(a,self.common_metadata())
        cb=self.case_fixture(b,self.common_metadata())
        result=analysis.compare_cases(dict(a=ca,b=cb))[0]
        self.assertTrue(result['matched_single_factor'])
        self.assertEqual(result['kind'],'eps')
        self.assertTrue(result['initial_state_admission']['compatible'])
        self.assertNotIn('renormalize',result['initial_state_caveat'])
        cb['initial_conditions']['relative_state_sha256']='b'*64
        result=analysis.compare_cases(dict(a=ca,b=cb))[0]
        self.assertFalse(result['matched_single_factor'])
        self.assertEqual(result['kind'],'incompatible_initial_states')

    def test_N_control_checks_preparation_family_and_reference_epsilon(self):
        # Different N necessarily changes bytes, but not the preparation law.
        a=dict(ncold=16384,eps=10.,h=25.,dt=.5,seed=87319,backend='tile2',initial='N16/initial.npz')
        b=dict(a,ncold=32768,initial='N32/initial.npz')
        ca=self.case_fixture(a,self.common_metadata())
        cb=self.case_fixture(b,self.common_metadata('b'*64))
        result=analysis.compare_cases(dict(a=ca,b=cb))[0]
        self.assertTrue(result['matched_single_factor'])
        self.assertEqual(result['changed_arguments'],['ncold'])
        self.assertEqual(result['initial_state_admission']['mode'],'same_preparation_family_different_N')
        cb['initial_conditions']['reference_softening_pc']=20.
        result=analysis.compare_cases(dict(a=ca,b=cb))[0]
        self.assertFalse(result['matched_single_factor'])
        self.assertIn('reference_softening_pc',result['initial_state_admission']['failed_checks'])
        cb['initial_conditions']=self.common_metadata('b'*64)
        cb['initial_conditions']['cold']['ordered_fraction']=.2
        result=analysis.compare_cases(dict(a=ca,b=cb))[0]
        self.assertFalse(result['matched_single_factor'])
        self.assertIn('cold.ordered_fraction',result['initial_state_admission']['failed_checks'])

    def test_N_and_backend_changes_remain_mixed_and_legends_name_backend(self):
        # A validated candidate backend is not automatically an N-only control.
        a=dict(ncold=8192,eps=10.,h=25.,dt=.5,seed=87319,backend='metal',initial='old/initial.npz')
        b=dict(a,ncold=16384,backend='tile2',initial='new/initial.npz')
        result=analysis.compare_cases(dict(a=self.case_fixture(a,self.common_metadata()),
            b=self.case_fixture(b,self.common_metadata('b'*64))))[0]
        self.assertFalse(result['matched_single_factor'])
        self.assertEqual(result['kind'],'mixed_controls')
        self.assertEqual(set(result['changed_arguments']),{'ncold','backend'})
        self.assertIn('tile2',analysis._label(dict(args=b)))

    def test_failed_conservation_control_is_visible_in_plot_and_comparison(self):
        # A failed coarse elastic case must not look like admitted physical evidence.
        args=dict(ncold=8192,eps=10.,h=25.,dt=.5,seed=87319,backend='metal')
        a=self.case_fixture(args,self.common_metadata())
        b=self.case_fixture(dict(args,collisionless=True),self.common_metadata())
        a['maxima']=dict(E=.0012366,Jint=0.,Jorb=0.,Jtotal=0.,P=0.)
        b['maxima']=dict(E=.00038,Jint=0.,Jorb=0.,Jtotal=0.,P=0.)
        self.assertIn('E FAIL',analysis._label(a))
        result=analysis.compare_cases(dict(a=a,b=b))[0]
        self.assertEqual(result['recorded_conservation_failures']['a'],['E'])


if __name__ == "__main__":
    unittest.main()
