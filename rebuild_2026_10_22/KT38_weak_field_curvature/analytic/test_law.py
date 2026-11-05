import importlib.util
from pathlib import Path
import unittest
import numpy as np


class ActionTests(unittest.TestCase):
    def setUp(self):
        path=Path(__file__).with_name('law.py')
        self.assertTrue(path.exists(),'KT38 law implementation absent')
        spec=importlib.util.spec_from_file_location('kt38_test_law',path)
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)

    def test_full_energy_first_variation(self):
        m=self.m;g=np.array([.3,-.6,.8]);H=np.array([[.2,.1,-.1],[.1,-.3,.2],[-.1,.2,.4]])
        v=np.array([.2,.5,-.4]);K=np.array([[.7,-.4,.3],[-.4,.5,.6],[.3,.6,-.2]])
        t=m.tensor_terms(g,H,.7,a0=1.2);h=1e-5
        fd=(m.tensor_terms(g+h*v,H+h*K,.7,a0=1.2)['energy']-m.tensor_terms(g-h*v,H-h*K,.7,a0=1.2)['energy'])/(2*h)
        exact=2*np.sum((t['A']+g)*v)+2*np.sum(t['B']*K)
        np.testing.assert_allclose(fd,exact,rtol=2e-8,atol=1e-10)

    def test_newton_ell0_origin(self):
        m=self.m;g=np.array([.4,.3,0.]);H=np.eye(3)
        t=m.tensor_terms(g,H,.7,newtonian=True)
        np.testing.assert_array_equal(t['A'],np.zeros(3));np.testing.assert_array_equal(t['B'],np.zeros((3,3)))
        q=m.tensor_terms(g,H,0.)
        np.testing.assert_allclose(q['A'],(m.Qprime(.25)-1)*g,rtol=1e-13)
        np.testing.assert_array_equal(q['B'],np.zeros((3,3)))
        o=m.tensor_terms(np.zeros(3),np.zeros((3,3)),1.)
        self.assertEqual(float(o['energy']),0.);np.testing.assert_array_equal(o['A'],np.zeros(3));np.testing.assert_array_equal(o['B'],np.zeros((3,3)))

    def test_weak_scaling_away_from_saddle(self):
        m=self.m;g=np.array([.3,-.4,.5]);H=np.diag([.2,-.3,.4]);lam=1e-10
        t=m.tensor_terms(lam*g,lam*H,.8)
        np.testing.assert_allclose((t['A']+lam*g)/np.sqrt(lam),g/np.sqrt(np.linalg.norm(g)),rtol=1e-5)
        one=m.tensor_terms(1e-4*g,1e-4*H,.8)['B'];two=m.tensor_terms(5e-5*g,5e-5*H,.8)['B']
        np.testing.assert_allclose(np.linalg.norm(one)/np.linalg.norm(two),2**2.5,rtol=1e-4)

    def test_uniform_background_first_variation(self):
        m=self.m;eta=2.48;g=np.array([0.,0.,eta]);v=np.array([.7,.2,-.5]);H=np.diag([.3,-.2,.8]);h=1e-5
        plus=m.tensor_terms(g+h*v,h*H,3.);minus=m.tensor_terms(g-h*v,-h*H,3.)
        dA=(plus['A']-minus['A'])/(2*h);dB=(plus['B']-minus['B'])/(2*h)
        nu=float(m.Qprime(eta**2));nud=-1/(eta**2*np.sqrt(1+4/eta))
        expected=(nu-1)*v;expected[2]+=eta*nud*v[2]
        np.testing.assert_allclose(dA,expected,rtol=1e-8,atol=1e-10)
        self.assertLess(np.linalg.norm(dB),1e-7)


if __name__=='__main__':unittest.main()
