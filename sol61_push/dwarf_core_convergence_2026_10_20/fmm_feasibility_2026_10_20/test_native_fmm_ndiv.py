import unittest
import numpy as np
try:
    from native_fmm_ndiv import gravity
except ImportError:
    gravity=None


class NdivTests(unittest.TestCase):
    def test_nondefault_leaf_analytic_and_direct(self):
        self.assertIsNotNone(gravity,'ndiv ABI binding missing')
        rng=np.random.default_rng(8191);x=rng.normal(size=(256,3))*100.;m=np.exp(rng.normal(size=256))
        dr=x[None,:,:]-x[:,None,:];r2=np.einsum('ijk,ijk->ij',dr,dr);np.fill_diagonal(r2,np.inf)
        inv=1/np.sqrt(r2);g=.004498638185693768
        ar=g*np.sum((m[None,:]*inv**3)[:,:,None]*dr,axis=1);pr=-g*np.sum(m[None,:]*inv,axis=1)
        for ndiv in (16,1000,4000):
            a,u,phi=gravity(x,m,1e-12,ndiv)
            np.testing.assert_allclose(a,ar,rtol=1e-10,atol=1e-14)
            np.testing.assert_allclose(phi,pr,rtol=1e-12,atol=0.)
            self.assertAlmostEqual(u,.5*float(m@pr),delta=1e-12*abs(u))


if __name__=='__main__':unittest.main()
