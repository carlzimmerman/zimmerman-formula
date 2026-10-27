"""Whole rebuilt Hamiltonian tests, rather than frozen-coefficient gradients."""
import unittest
import numpy as np
try:
    from scf_backend import gravity,load_agama
except ImportError:
    gravity=load_agama=None


class SCFTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gravity,'candidate SCF wrapper missing')
        self.rng=np.random.default_rng(42391)
        self.x=self.rng.normal(size=(12,3))*300+[120.,-80.,50.]
        self.m=np.exp(self.rng.normal(size=12))*1000

    def test_rebuilt_COM_energy_gradient_and_PJ(self):
        args=dict(nmax=6,lmax=4,r0=300.,eta=1.,self_mode='included')
        a,u,phi=gravity(self.x,self.m,**args)
        for i,axis in [(0,0),(3,1),(7,2),(11,0)]:
            dx=np.zeros_like(self.x);dx[i,axis]=.002
            up=gravity(self.x+dx,self.m,**args)[1];um=gravity(self.x-dx,self.m,**args)[1]
            fd=-(up-um)/.004/self.m[i]
            self.assertAlmostEqual(a[i,axis],fd,delta=2e-7*max(abs(fd),1e-5))
        f=self.m[:,None]*a;y=self.x-np.average(self.x,axis=0,weights=self.m)
        self.assertLess(np.linalg.norm(f.sum(0))/np.linalg.norm(f,axis=1).sum(),2e-13)
        self.assertLess(np.linalg.norm(np.cross(y,f).sum(0))/np.linalg.norm(np.cross(y,f),axis=1).sum(),2e-12)
        self.assertAlmostEqual(u,.5*float(self.m@phi),delta=1e-13*abs(u))

    def test_rotation_translation_full_m_and_no_mutation(self):
        x=self.x.copy();m=self.m.copy();kwargs=dict(nmax=6,lmax=5,r0=300.,eta=.5,self_mode='included')
        a,u,phi=gravity(x,m,**kwargs)
        q,_=np.linalg.qr(self.rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q)
        ar,ur,pr=gravity(x@q.T+[80000.,-20000.,10000.],m,**kwargs)
        np.testing.assert_allclose(ar,a@q.T,rtol=2e-10,atol=1e-12)
        np.testing.assert_allclose(pr,phi,rtol=2e-11,atol=1e-12)
        self.assertAlmostEqual(ur,u,delta=2e-11*abs(u))
        np.testing.assert_array_equal(x,self.x);np.testing.assert_array_equal(m,self.m)

    def test_self_diagonal_matches_single_source_factory(self):
        # A source's finite basis self-field is nonzero. The excluded convention
        # must subtract its matched diagonal potential and half-diagonal gradient.
        from scf_backend import diagonal
        agama=load_agama();r0=300.;G=.004498638185693768
        for eta in (.5,1.,2.):
            for point in self.x[:3]:
                pot=agama.Potential(type='BasisSet',particles=(point[None,:],np.array([G*20.])),
                    symmetry='None',lmax=4,mmax=4,nmax=6,eta=eta,r0=r0)
                phi,a=pot.eval(point[None,:],pot=True,acc=True)
                k,dk=diagonal(np.linalg.norm(point)[None],6,4,eta,r0)
                np.testing.assert_allclose(phi,G*20*k,rtol=2e-12,atol=1e-13)
                expected=-.5*G*20*dk[:,None]*point[None,:]/np.linalg.norm(point)
                np.testing.assert_allclose(a,expected,rtol=2e-11,atol=1e-13)

    def test_excluded_rebuilt_energy_gradient(self):
        args=dict(nmax=6,lmax=4,r0=300.,eta=1.,self_mode='excluded')
        a,u,phi=gravity(self.x,self.m,**args)
        for i,axis in [(0,0),(3,1),(7,2)]:
            dx=np.zeros_like(self.x);dx[i,axis]=.002
            fd=-(gravity(self.x+dx,self.m,**args)[1]-gravity(self.x-dx,self.m,**args)[1])/.004/self.m[i]
            self.assertAlmostEqual(a[i,axis],fd,delta=2e-7*max(abs(fd),1e-5))
        self.assertAlmostEqual(u,.5*float(self.m@phi),delta=1e-13*abs(u))


if __name__=='__main__':unittest.main()
