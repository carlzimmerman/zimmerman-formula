"""Scientific controls: a wrong derivative, normalization or action primitive fails."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np


class ResponseTests(unittest.TestCase):
    def test_response_exists_and_exact_simple_control(self):
        path=Path(__file__).with_name('response.py')
        self.assertTrue(path.exists(), 'new response implementation is absent')
        from response import Response
        y=np.geomspace(1e-10,1e10,101)
        np.testing.assert_allclose(Response('simple').nu(y), .5+np.sqrt(.25+1/y),rtol=2e-15)
        np.testing.assert_allclose(Response('power',power=1).nu(y),Response('simple').nu(y),rtol=3e-14)

    def test_analytic_derivative_and_energy_primitive(self):
        from response import Response
        cases=[Response('power',power=2),Response('cutoff',scale=3,power=4),Response('rational',scale=3,power=4)]
        y=np.geomspace(1e-5,30,31); h=2e-5
        for response in cases:
            fd=(response.excess(y*np.exp(h))-response.excess(y*np.exp(-h)))/(2*h*y)
            np.testing.assert_allclose(response.nud(y),fd,rtol=2e-6,atol=2e-10)
            for point in [.01,.3,1.,3.,10.]:
                dx=point*2e-4
                slope=(response.primitive(point+dx)-response.primitive(point-dx))/(2*dx)
                expected=point*response.excess(point)
                self.assertAlmostEqual(slope,expected,delta=max(1e-8,3e-6*abs(expected)))

    def test_limits_and_shapes(self):
        from response import candidates
        for response in candidates():
            self.assertLess(abs(np.sqrt(1e-14)*response.nu(1e-14)-1),2e-7)
            self.assertLess(abs(response.nu(1e14)-1),2e-7)
            self.assertEqual(response.nu(np.ones((2,3))).shape,(2,3))
            self.assertTrue(np.isfinite(response.nud(1.)).all())

    def test_cassini_control_and_zero_external_field(self):
        from response import Response
        from cassini_response import quadrupole, baseline
        old=baseline.quadrupole(2.32e-10/9.3603e-11,.5,.5,nr=3000,nm=80)
        new=quadrupole(Response('simple'),2.32e-10/9.3603e-11,.5,nr=3000,nm=80)
        self.assertAlmostEqual(old['q_hessian_signed'],new['q_hessian_signed'],delta=1e-12)
        self.assertLess(abs(new['flux_density_difference']),1e-8)
        zero=quadrupole(Response('cutoff',scale=3,power=4),0.,.3,nr=1000,nm=40)
        self.assertLess(abs(zero['q_hessian_signed']),1e-12)


if __name__=='__main__': unittest.main()
