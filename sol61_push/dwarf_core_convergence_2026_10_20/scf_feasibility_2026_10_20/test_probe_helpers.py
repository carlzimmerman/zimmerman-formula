import unittest
import numpy as np


class ProbeHelpersTest(unittest.TestCase):
    def test_sample_direct_unequal_mass(self):
        from probe_helpers import direct_sample,G
        x=np.array([[0.,0.,0.],[3.,4.,0.]]);m=np.array([2.,7.])
        a,p=direct_sample(x,m,np.array([0,1]),0.)
        np.testing.assert_allclose(a[0],G*7*x[1]/125,rtol=2e-15)
        np.testing.assert_allclose(a[1],-G*2*x[1]/125,rtol=2e-15)
        np.testing.assert_allclose(p,-G*np.array([7.,2.])/5,rtol=2e-15)

    def test_uniform_sphere_matches_analytic_inside_outside(self):
        from probe_helpers import ellipsoid_field,G
        x=np.array([[1.,2.,0.],[12.,-5.,0.],[0.,0.,0.]])
        a,p=ellipsoid_field(x,3.,np.array([10.,10.,10.]))
        r=np.linalg.norm(x,axis=1)
        expected=-G*3*x/np.maximum(r,10.)[:,None]**3
        phi=np.where(r<=10.,-G*3*(3*100-r*r)/2000.,-G*3/np.maximum(r,1.))
        np.testing.assert_allclose(a,expected,rtol=2e-12,atol=1e-17)
        np.testing.assert_allclose(p,phi,rtol=2e-12)


if __name__=='__main__':unittest.main()
