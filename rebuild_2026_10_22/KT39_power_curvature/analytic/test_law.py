import importlib.util
from pathlib import Path
import unittest
import numpy as np


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


class ActionTests(unittest.TestCase):
    def setUp(self):
        path=Path(__file__).with_name('law.py')
        self.assertTrue(path.exists(),'KT39 implementation absent')
        self.m=module(path,'kt39_test_law')

    def test_full_tensor_variation(self):
        m=self.m;g=np.array([.3,-.6,.8]);H=np.array([[.2,.1,-.1],[.1,-.3,.2],[-.1,.2,.4]])
        v=np.array([.2,.5,-.4]);K=np.array([[.7,-.4,.3],[-.4,.5,.6],[.3,.6,-.2]])
        for p in (1.25,1.5,1.75):
            t=m.tensor_terms(g,H,.7,a0=1.2,p=p);h=1e-5
            fd=(m.tensor_terms(g+h*v,H+h*K,.7,a0=1.2,p=p)['energy']-m.tensor_terms(g-h*v,H-h*K,.7,a0=1.2,p=p)['energy'])/(2*h)
            exact=2*np.sum((t['A']+g)*v)+2*np.sum(t['B']*K)
            np.testing.assert_allclose(fd,exact,rtol=3e-8,atol=1e-10)

    def test_legacy_power_controls(self):
        root=Path(__file__).resolve().parents[2]
        g=np.array([[.3,.4,.7],[.2,-.4,.9]]);H=np.array([np.diag([.2,-.3,.4]),np.diag([.1,.5,-.7])])
        for p,folder in [(1.,'KT37_generalized_action'),(2.,'KT38_weak_field_curvature')]:
            old=module(root/folder/'analytic/law.py',f'legacy_{p}')
            a=self.m.tensor_terms(g,H,.8,p=p);b=old.tensor_terms(g,H,.8)
            for key in ('A','B','energy','z'):np.testing.assert_allclose(a[key],b[key],rtol=2e-14,atol=1e-15)

    def test_newton_zero_and_weak_scaling(self):
        m=self.m;g=np.array([.3,-.4,.5]);H=np.diag([.2,-.3,.4]);lam=1e-12
        for p in (1.25,1.5,1.75):
            t=m.tensor_terms(g,H,.8,newtonian=True,p=p)
            np.testing.assert_array_equal(t['A'],np.zeros(3));np.testing.assert_array_equal(t['B'],np.zeros((3,3)))
            t=m.tensor_terms(np.zeros(3),np.zeros((3,3)),.8,p=p)
            self.assertEqual(float(t['energy']),0.);np.testing.assert_array_equal(t['A'],np.zeros(3));np.testing.assert_array_equal(t['B'],np.zeros((3,3)))
            t=m.tensor_terms(lam*g,lam*H,.8,p=p)
            np.testing.assert_allclose((t['A']+lam*g)/np.sqrt(lam),g/np.sqrt(np.linalg.norm(g)),rtol=2e-6)

    def test_uniform_Hzero_variation(self):
        m=self.m;eta=2.48;g=np.array([0.,0.,eta]);v=np.array([.7,.2,-.5]);H=np.diag([.3,-.2,.8]);h=1e-10
        nu=float(m.Qprime(eta**2));nud=-1/(eta**2*np.sqrt(1+4/eta));expected=(nu-1)*v;expected[2]+=eta*nud*v[2]
        for p in (1.25,1.5,1.75):
            plus=m.tensor_terms(g+h*v,h*H,1.,p=p);minus=m.tensor_terms(g-h*v,-h*H,1.,p=p)
            np.testing.assert_allclose((plus['A']-minus['A'])/(2*h),expected,rtol=2e-5,atol=3e-6)
            self.assertLess(np.linalg.norm((plus['B']-minus['B'])/(2*h)),1e-5)


if __name__=='__main__':unittest.main()
