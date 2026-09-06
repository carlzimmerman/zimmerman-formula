"""Regression breaks: radial units, substituted kernel, extrapolation, pressure sign."""
import importlib.util
import unittest
from pathlib import Path

import numpy as np


class ClusterAuditTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.find_spec('cluster_audit')
        self.assertIsNotNone(spec, 'The independent cluster audit is not implemented yet')
        import cluster_audit
        self.a = cluster_audit

    def test_exact_inverse_not_rar_substitution(self):
        # Construct gbar from known g, independently of the inverse under test.
        y = np.geomspace(1e-6, 100, 90)
        b = y * (-np.expm1(-y))
        np.testing.assert_allclose(self.a.exact_y(b), y, rtol=2e-11)
        self.assertGreater(abs(self.a.route_a_y(b[45])/y[45]-1), .001)

    def test_zero_and_negative_field(self):
        self.assertEqual(self.a.exact_y(0.), 0.)
        with self.assertRaises(ValueError):
            self.a.exact_y(-1.)

    def test_radius_uses_own_fits_header(self):
        # 2.5% of a 1.2-Mpc aperture is 30 kpc, not 25 kpc.
        np.testing.assert_allclose(self.a.radius_kpc([.025], 'R/R500', {'R500':1200}), [30])
        np.testing.assert_allclose(self.a.radius_kpc([.025], 'Mpc', {}), [25])
        with self.assertRaises(ValueError):
            self.a.radius_kpc([.025], 'R/R500', {})

    def test_no_extrapolation(self):
        got = self.a.loginterp([1, 2, 4, 8, 16], [2, 8], [4, 64])
        self.assertTrue(np.isnan(got[[0,4]]).all())
        np.testing.assert_allclose(got[1:4], [4,16,64])

    def test_gas_radius_crossvalidates_independent_mass_column(self):
        c = self.a.load_cluster('A2029')
        good = self.a.mass_alignment(c, legacy=False)
        bad = self.a.mass_alignment(c, legacy=True)
        self.assertLess(good, .005)
        self.assertGreater(bad, .1)

    def test_exact_source_mass_differs_from_effective_mass(self):
        # yobs=ln2 -> mu=1/2. M_HSE=6 and Mb=2 -> required-source ratio=1.5.
        got = self.a.source_ratio(np.log(2), 6., 2.)
        self.assertAlmostEqual(got, 1.5)
        self.assertNotEqual(got, 3.)

    def test_pressure_increases_gravity_if_it_decreases_outward(self):
        # gH=3, rho=2, dPnt/dr=-4 -> true g=5 in static equilibrium.
        self.assertEqual(self.a.static_gravity(3., -4., 2.), 5.)
        self.assertEqual(self.a.static_gravity(3., 4., 2.), 1.)

    def test_integrated_pressure_requires_outer_confinement(self):
        r=np.array([0.,1.,2.]); rho=np.ones(3)*2
        # gH=3, gmodel=1, deficit integral=8; zero outer pressure makes Pnt(0)=-8.
        z=self.a.pressure_boundary(r, rho, np.ones(3)*3, np.ones(3))
        self.assertAlmostEqual(z['required_outer_pressure'], 8.)
        self.assertAlmostEqual(z['inner_pressure_if_outer_zero'], -8.)
        self.assertAlmostEqual(z['fraction_of_thermal_pressure_drop'], 2/3)

    def test_cosmic_average_is_not_local_ceiling(self):
        # 2% of a mass inventory has local baryon fraction .5; global fraction .16.
        other=self.a.rest_baryon_fraction(.02, .5, .16)
        self.assertGreater(other,0.)
        self.assertLess(other,1.)
        self.assertAlmostEqual(.02*.5+.98*other, .16)


if __name__ == '__main__':
    unittest.main()
