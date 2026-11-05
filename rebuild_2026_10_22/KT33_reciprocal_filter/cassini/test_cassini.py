"""Independent invariants and archived benchmark tests for the Cassini operator."""
import importlib.util
import math
from pathlib import Path
import unittest
import numpy as np
from scipy.integrate import quad
from scipy.special import erf

MODULE = Path(__file__).with_name('cassini.py')


class CassiniTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if MODULE.exists():
            spec = importlib.util.spec_from_file_location('cassini', MODULE)
            cls.model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.model)
        else:
            cls.model = None

    def require_model(self):
        self.assertIsNotNone(self.model, 'Corrected Cassini implementation is required')
        return self.model

    def test_gaussian_kernel_is_hessian_of_smoothed_green(self):
        m = self.require_model()
        # Independent centered finite differences of erf(r/sqrt(2)s)/r.
        s = 0.5
        for r in [0.15, 0.4, 1.0, 3.0]:
            h = 1e-4 * s
            f = lambda z: erf(z / (math.sqrt(2) * s)) / z
            first = (f(r+h)-f(r-h))/(2*h)
            second = (f(r+h)-2*f(r)+f(r-h))/(h*h)
            actual = (second-first/r) * r**3/3
            self.assertAlmostEqual(m.kernel_weight(np.array([r]), s)[0], actual, delta=2e-7)

    def test_gaussian_normalization_and_field(self):
        m = self.require_model()
        s = 0.5
        density = lambda r: math.sqrt(2/math.pi)*r*r/s**3*math.exp(-r*r/(2*s*s))
        self.assertAlmostEqual(quad(density, 0, np.inf)[0], 1., places=12)
        for r in [1e-5, 0.1, 1.0, 5.0]:
            enclosed = quad(density, 0, r, epsabs=1e-16)[0]
            self.assertAlmostEqual(m.gaussian_field(np.array([r]), s)[0]*r*r, enclosed, delta=2e-13)

    def test_zero_width_and_newtonian_limits(self):
        m = self.require_model()
        np.testing.assert_array_equal(m.kernel_weight(np.array([.01,1.,100.]), 0), 1.)
        np.testing.assert_array_equal(m.kernel_weight_prime(np.array([.01,1.,100.]), 0), 0.)
        for source, outer in [(0.,0.),(.5,0.),(.5,.5)]:
            self.assertEqual(m.quadrupole(2.32e-10/9.3603e-11, source, outer, nr=1000, nm=40, newtonian=True)['q_signed'], 0.)

    def test_source_only_reproduces_archive(self):
        m = self.require_model()
        for a0, archived in [(9.3603e-11,.021196656767700273),(1.1312e-10,.0350820450127879)]:
            q = m.quadrupole(2.32e-10/a0,.5,0.,nr=20000,nm=200)['q_signed']
            self.assertAlmostEqual(abs(q),archived,delta=2e-8)

    def test_density_and_flux_agree_with_surface_term(self):
        m = self.require_model()
        for source, outer in [(0.,0.),(.5,0.),(.5,.5)]:
            out = m.quadrupole(2.32e-10/9.3603e-11,source,outer,nr=8000,nm=200,rmin=1e-5,rmax=1000.)
            self.assertAlmostEqual(out['q_signed']-out['boundary_term'],out['q_density_signed'],delta=2e-5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
