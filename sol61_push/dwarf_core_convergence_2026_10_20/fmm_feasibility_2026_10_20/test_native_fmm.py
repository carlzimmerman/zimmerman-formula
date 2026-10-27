"""Tests of the native ABI/conventions; these do not certify FMM truncation."""
from pathlib import Path
import unittest
import numpy as np

try:
    from native_fmm import gravity
except ImportError:
    gravity = None


class NativeFMMTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gravity, 'native ctypes binding is missing')

    def test_two_body_sign_normalization_and_self_exclusion(self):
        x=np.array([[0.,0.,0.],[2.,0.,0.]])
        m=np.array([3.,7.]); g=.004498638185693768
        a,u,phi=gravity(x,m,tolerance=1e-12)
        np.testing.assert_allclose(phi,-g*np.array([7.,3.])/2,rtol=3e-14,atol=0.)
        np.testing.assert_allclose(a,g*np.array([[7./4,0,0],[-3./4,0,0]]),rtol=3e-14,atol=0.)
        self.assertAlmostEqual(u,-g*21/2,delta=3e-14*abs(u))

    def test_unequal_mass_translation_and_no_input_mutation(self):
        rng=np.random.default_rng(8162); x=rng.normal(size=(128,3))*100
        m=np.exp(rng.normal(size=128)); xx=x.copy(); mm=m.copy()
        a,u,phi=gravity(x,m,tolerance=1e-12)
        delta=x[None,:,:]-x[:,None,:]
        r2=np.einsum('ijk,ijk->ij',delta,delta); np.fill_diagonal(r2,np.inf)
        invr=1/np.sqrt(r2); g=.004498638185693768
        ar=g*np.sum((m[None,:]*invr**3)[:,:,None]*delta,axis=1)
        phir=-g*np.sum(m[None,:]*invr,axis=1)
        np.testing.assert_allclose(a,ar,rtol=1e-11,atol=1e-15)
        np.testing.assert_allclose(phi,phir,rtol=1e-12,atol=0.)
        shifted=gravity(x+[20000,-10000,30000],m,tolerance=1e-12)
        np.testing.assert_allclose(shifted[0],a,rtol=1e-10,atol=1e-15)
        np.testing.assert_array_equal(x,xx); np.testing.assert_array_equal(m,mm)


if __name__=='__main__': unittest.main()
