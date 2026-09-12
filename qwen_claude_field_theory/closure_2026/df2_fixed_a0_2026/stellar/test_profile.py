"""Independent normalization and Jeans controls, not observational fit tests."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from scipy.integrate import quad
from scipy.special import erf

PATH = Path(__file__).with_name('profile.py')


class ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if PATH.exists():
            spec = importlib.util.spec_from_file_location('df2_profile', PATH)
            cls.code = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.code)
        else:
            cls.code = None

    def require_code(self):
        self.assertIsNotNone(self.code, 'The normalized stellar profile is not implemented')
        return self.code

    def test_gaussian_abel_and_enclosed_mass(self):
        c = self.require_code()
        p = c.Sersic(n=.5)
        r = np.array([0., .001, .1, .5, 1., 2., 4.])
        b = np.log(2.)
        rho = (b / np.pi)**1.5 * np.exp(-b*r*r)
        mass = erf(np.sqrt(b)*r)-2*np.sqrt(b/np.pi)*r*np.exp(-b*r*r)
        np.testing.assert_allclose(p.density(r), rho, rtol=2e-5, atol=1e-12)
        np.testing.assert_allclose(p.mass(r), mass, rtol=2e-5, atol=1e-11)

    def test_df2_mass_and_reprojection(self):
        p = self.require_code().Sersic()
        self.assertAlmostEqual(p.projected_mass(1.), .5, places=13)
        self.assertAlmostEqual(quad(lambda r: 4*np.pi*r*r*p.density(r), 0, 20,
                                    epsabs=1e-8)[0], 1., places=6)
        for R in [.05, .5, 1., 3.]:
            reprojection = 2*quad(lambda z: p.density(np.hypot(R,z)), 0, 20,
                                  epsabs=1e-9)[0]
            self.assertAlmostEqual(reprojection/p.surface_density(R), 1., places=5)
        self.assertEqual(p.mass(0.), 0.)
        self.assertAlmostEqual(p.mass(50.), 1., places=8)
        self.assertTrue(np.all(np.diff(p.mass(np.geomspace(1e-7,50,500))) >= 0))

    def test_inverse_aqual_has_both_limits_and_small_residual(self):
        c = self.require_code()
        y = np.geomspace(1e-14,1e4,300)
        x = c.spherical_acceleration(y)
        np.testing.assert_allclose(x*(-np.expm1(-x)), y, rtol=1e-11)
        self.assertAlmostEqual(x[0]/np.sqrt(y[0]),1.,places=6)
        self.assertAlmostEqual(x[-1]/y[-1],1.,places=12)
        self.assertEqual(c.spherical_acceleration(0.),0.)

    def test_newtonian_plummer_apertures_and_global(self):
        c = self.require_code()
        class Plummer:
            def density(self,r): return 3/(4*np.pi)*(1+np.asarray(r)**2)**-2.5
            def mass(self,r): return np.asarray(r)**3/(1+np.asarray(r)**2)**1.5
            def projected_mass(self,R): return R*R/(1+R*R)
        p = Plummer()
        for R in [.1, 1., 5., np.inf]:
            expected = np.pi/32 if np.isinf(R) else (np.pi/32)*(
                1-(1+R*R)**-1.5)/(R*R/(1+R*R))
            got = c.aperture_second_moment(p, eta=1., aperture=R, law='newtonian')
            self.assertAlmostEqual(got/expected,1.,places=7)

    def test_aqual_deep_global_virial_coefficient(self):
        c = self.require_code()
        p = c.Sersic()
        # Independent deep-MOND virial identity for continuous spherical mass:
        # sigma_los² = (2/9) sqrt(G M a0), neglecting the O(g/a0) correction.
        got = c.aperture_second_moment(p, eta=1e-10, aperture=np.inf)
        self.assertLess(abs(got/((2/9)*1e-5)-1), 1e-4)


if __name__ == '__main__':
    unittest.main()
