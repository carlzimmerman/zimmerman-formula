"""Nontrivial normalization, variational, limit and regularity controls."""
from pathlib import Path
import unittest
import numpy as np
from scipy.integrate import quad


class LawTests(unittest.TestCase):
    def test_implementation_and_Q_normalization(self):
        self.assertTrue(Path(__file__).with_name('law.py').exists(),'analytic law module absent')
        import law
        self.assertEqual(float(law.Q(0)),0.)
        for z in np.geomspace(1e-24,1e24,25):
            u=z**.25
            independent=quad(lambda v:4*v*v*np.sqrt(1+v*v/4)+2*v**3,0,u,epsabs=1e-100,epsrel=3e-13)[0]
            self.assertAlmostEqual(float(law.Q(z))/independent,1.,delta=3e-12)

    def test_scalar_derivatives(self):
        import law
        z=np.geomspace(1e-16,1e16,161);h=2e-5
        qp=(law.Q(z*np.exp(h))-law.Q(z*np.exp(-h)))/(2*h*z)
        rp=(law.Rminus1(z*np.exp(h))-law.Rminus1(z*np.exp(-h)))/(2*h*z)
        np.testing.assert_allclose(qp,law.Qprime(z),rtol=2e-8)
        np.testing.assert_allclose(rp,law.Rprime(z),rtol=2e-8)
        np.testing.assert_allclose(law.R(z)+law.zRprime(z),law.Qprime(z),rtol=2e-15)

    def test_energy_gradient_hessian_partials(self):
        import law
        g=np.array([.8,-.3,.5]);H=np.array([[.2,.1,-.04],[.1,-.4,.07],[-.04,.07,.3]])
        dg=np.array([.11,.2,-.07]);dH=np.array([[.03,-.05,.02],[-.05,.07,.08],[.02,.08,-.09]])
        for ell,a0 in [(0.,1.),(.4,1.),(3.,.2)]:
            out=law.tensor_terms(g,H,ell,a0)
            dx=1e-5
            ep=law.tensor_terms(g+dx*dg,H+dx*dH,ell,a0)['energy']
            em=law.tensor_terms(g-dx*dg,H-dx*dH,ell,a0)['energy']
            exact=2*np.sum((out['A']+g)*dg)+2*np.sum(out['B']*dH)
            self.assertAlmostEqual(float((ep-em)/(2*dx)),float(exact),delta=2e-8)

    def test_controls_and_origin(self):
        import law
        g=np.array([.3,.4,0.]);H=np.eye(3)*.1
        newton=law.tensor_terms(g,H,3.,newtonian=True)
        np.testing.assert_array_equal(newton['A'],np.zeros(3));np.testing.assert_array_equal(newton['B'],np.zeros((3,3)))
        ordinary=law.tensor_terms(g,H,0.)
        nu=.5+np.sqrt(.25+1/np.linalg.norm(g))
        np.testing.assert_allclose(ordinary['A'],(nu-1)*g,rtol=2e-15)
        np.testing.assert_array_equal(ordinary['B'],np.zeros((3,3)))
        origin=law.tensor_terms(np.zeros(3),np.zeros((3,3)),1.)
        self.assertEqual(float(origin['energy']),0.);np.testing.assert_array_equal(origin['A'],np.zeros(3));np.testing.assert_array_equal(origin['B'],np.zeros((3,3)))
        tiny=law.tensor_terms(g*1e-100,H*1e-100,1.)
        self.assertTrue(np.all(np.isfinite(tiny['A'])));self.assertTrue(np.all(np.isfinite(tiny['B'])))


if __name__=='__main__':unittest.main()
