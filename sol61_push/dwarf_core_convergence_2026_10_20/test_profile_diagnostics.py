"""Analytic count fixtures test profile diagnostics without N-body evolution."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np


path = Path(__file__).with_name("profile_diagnostics.py")
if path.exists():
    spec = importlib.util.spec_from_file_location("profile_diagnostics_tested", path)
    diagnostics = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(diagnostics)
else:
    diagnostics = None


def analytic_fixture(gamma, count=16384):
    # Inverse CDF for rho proportional to r^-gamma inside R=400 pc.
    # Quantiles make the expected shape independent of random counting noise.
    u = (np.arange(count) + .5) / count
    radius = 400. * u ** (1. / (3. - gamma))
    rng = np.random.default_rng(201)
    direction = rng.normal(size=(count, 3))
    direction /= np.linalg.norm(direction, axis=1)[:, None]
    return radius[:, None] * direction, np.full(count, .01)


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(diagnostics, "profile diagnostic implementation is missing")

    def test_shell_counts_include_unresolved_inner_mass_and_all_gravitating_species(self):
        # Omitting inner mass, wrong edge inclusion, or using only cold gravity fails.
        x = np.array([[1., 0., 0.], [2., 0., 0.], [3., 0., 0.]]) + [70., -2., 5.]
        p = diagnostics.shell_profile(x, [2., 3., 5.], [70., -2., 5.], [1., 2., 4.],
                                      cold=np.array([True, False, True]))
        np.testing.assert_array_equal(p["count"], [0, 1])
        np.testing.assert_allclose(p["mass"], [0., 5.])
        np.testing.assert_array_equal(p["cumulative_count"], [1, 2])
        np.testing.assert_allclose(p["cumulative_mass"], [2., 7.])
        np.testing.assert_allclose(p["gravitating_cumulative_mass"], [5., 10.])
        np.testing.assert_allclose(p["gravitating_cumulative_Neff"], [25. / 13., 100. / 38.])
        self.assertAlmostEqual(p["density"][1], 5. / (4. * np.pi / 3. * 56.))

    def test_softened_relaxation_screen_uses_orbital_time_and_documented_formula(self):
        x = np.zeros((10, 3)); x[:, 0] = np.linspace(1., 99., 10)
        p = diagnostics.shell_profile(x, np.full(10, 10.), [0., 0., 0.], [1., 100.])
        s = diagnostics.relaxation_screen(p, eps=10., G=1., age_Myr=10000.)
        self.assertAlmostEqual(s["torb_Myr"][-1], 628.3185307179587, places=9)
        self.assertAlmostEqual(s["t_relax_Myr"][-1], 442.11795051616116, places=8)
        self.assertFalse(s["pass_age"][-1])
        self.assertTrue(s["heuristic_screen_only"])

    def test_count_likelihood_recovers_uniform_density_and_r_inverse_cusp(self):
        for truth in (0., 1.):
            x, m = analytic_fixture(truth)
            p = diagnostics.shell_profile(x, m, [0., 0., 0.], np.geomspace(100., 400., 9))
            f = diagnostics.fit_powerlaw(p, 100., 400.)
            self.assertAlmostEqual(f["gamma"], truth, delta=.005)
            self.assertLess(f["gamma_ci95"][0], truth)
            self.assertGreater(f["gamma_ci95"][1], truth)
            self.assertTrue(f["conditional_Poisson_only"])
            self.assertEqual(f["fit_bin_count"], 8)

    def test_flatness_is_inconclusive_when_force_or_relaxation_screen_fails(self):
        x, m = analytic_fixture(0.)
        p = diagnostics.shell_profile(x, m, [0., 0., 0.], np.geomspace(100., 400., 9))
        f = diagnostics.fit_powerlaw(p, 100., 400.)
        s = diagnostics.relaxation_screen(p, 10.)
        result = diagnostics.classify_flatness(p, f, s, eps=10.)
        self.assertTrue(result["flat_candidate"])
        self.assertFalse(result["core_established"])
        self.assertTrue(result["temporal_and_ensemble_uncertainty_missing"])
        unresolved = diagnostics.classify_flatness(p, f, s, eps=50.)
        self.assertFalse(unresolved["flat_candidate"])
        self.assertIn("force_resolution", unresolved["failed_gates"])
        dense_p = diagnostics.shell_profile(x, m * 1.e8, [0., 0., 0.], p["edges"])
        dense_s = diagnostics.relaxation_screen(dense_p, 10.)
        relaxation_limited = diagnostics.classify_flatness(dense_p, f, dense_s, eps=10.)
        self.assertFalse(relaxation_limited["flat_candidate"])
        self.assertIn("relaxation_age", relaxation_limited["failed_gates"])

    def test_cusp_is_not_classified_flat_even_with_ample_numerical_resolution(self):
        x, m = analytic_fixture(1.)
        p = diagnostics.shell_profile(x, m, [0., 0., 0.], np.geomspace(100., 400., 9))
        f = diagnostics.fit_powerlaw(p, 100., 400.)
        s = diagnostics.relaxation_screen(p, 10.)
        c = diagnostics.classify_flatness(p, f, s, eps=10.)
        self.assertFalse(c["flat_candidate"])
        self.assertEqual(c["sampling_flatness"], "nonflat")

    def test_hollow_profile_cannot_pass_an_upper_slope_bound_as_flat(self):
        x, m = analytic_fixture(-1., count=65536)
        p = diagnostics.shell_profile(x, m, [0., 0., 0.], np.geomspace(100., 400., 9))
        f = diagnostics.fit_powerlaw(p, 100., 400.)
        self.assertLess(f["gamma_ci95"][1], .3)
        c = diagnostics.classify_flatness(p, f, diagnostics.relaxation_screen(p, 10.), eps=10.)
        self.assertFalse(c["flat_candidate"])
        self.assertEqual(c["sampling_flatness"], "nonflat")

    def test_near_zero_fitted_slope_does_not_hide_nonmonotonic_shell_model_misfit(self):
        x, m = analytic_fixture(0.)
        p = diagnostics.shell_profile(x, m, [0., 0., 0.], np.geomspace(100., 400., 9))
        counts = np.asarray(p["count"]).copy()
        # On geometric bins this zero-sum second difference also preserves
        # sum(n_j log(r_lo,j)), hence the powerlaw MLE slope stays near zero.
        counts[3:6] += [300, -600, 300]
        p["count"] = counts.tolist()
        f = diagnostics.fit_powerlaw(p, 100., 400.)
        self.assertAlmostEqual(f["gamma"], 0., delta=.005)
        self.assertLess(f["gamma_ci95"][1], .3)
        self.assertIn("gof_pvalue", f)
        self.assertLess(f["gof_pvalue"], 1.e-10)
        result = diagnostics.classify_flatness(p, f, diagnostics.relaxation_screen(p, 10.), eps=10.)
        self.assertFalse(result["flat_candidate"])
        self.assertIn("powerlaw_model_misfit", result["failed_gates"])

    def test_comparison_does_not_discard_failing_bins_or_unmatched_coverage(self):
        x, m = analytic_fixture(0.)
        a = diagnostics.shell_profile(x, m, [0., 0., 0.], [100., 200., 400.])
        b = dict(a); b["density"] = [a["density"][0], 1.5 * a["density"][1]]
        c = diagnostics.compare_profiles(a, b, tolerance=.1)
        self.assertEqual(c["within_tolerance"], [True, False])
        self.assertFalse(c["all_within_tolerance"])
        np.testing.assert_allclose(c["relative_difference"], [0., .5])
        changed_edges = dict(b); changed_edges["edges"] = [100., 250., 400.]
        c = diagnostics.compare_profiles(a, changed_edges, tolerance=.1)
        self.assertFalse(c["coverage_match"])
        self.assertFalse(c["all_within_tolerance"])

    def test_fit_refuses_partial_shell_assignment_and_unequal_mass_poisson_claim(self):
        x, m = analytic_fixture(0., count=4096)
        p = diagnostics.shell_profile(x, m, [0., 0., 0.], [100., 200., 400.])
        with self.assertRaisesRegex(ValueError, "edge"):
            diagnostics.fit_powerlaw(p, 101., 400.)
        m[::2] *= 2.
        p = diagnostics.shell_profile(x, m, [0., 0., 0.], [100., 200., 400.])
        with self.assertRaisesRegex(ValueError, "equal.mass"):
            diagnostics.fit_powerlaw(p, 100., 400.)


if __name__ == "__main__":
    unittest.main()
