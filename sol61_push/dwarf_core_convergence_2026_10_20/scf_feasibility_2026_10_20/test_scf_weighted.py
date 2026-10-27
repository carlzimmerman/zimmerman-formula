import unittest
import numpy as np


class WeightedSCFTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(522761)
        self.x=self.rng.normal(size=(17,3))*[100,80,60]+[1200,-600,300]
        self.m=np.exp(self.rng.normal(size=17))*1000

    def test_centre_jacobian_including_COM_weight_normalization(self):
        from scf_weighted import centre_and_chain
        c,aux=centre_and_chain(self.x,self.m,300.)
        F=np.array([1.2,-2.3,3.4]);correction=aux(F)
        for i,axis in [(0,0),(4,2),(16,1)]:
            dx=np.zeros_like(self.x);dx[i,axis]=.001
            cp=centre_and_chain(self.x+dx,self.m,300.)[0]
            cm=centre_and_chain(self.x-dx,self.m,300.)[0]
            fd=(cp-cm)/.002
            self.assertAlmostEqual(fd@F/self.m[i],correction[i,axis],delta=2e-10*max(1.,abs(correction[i,axis])))

    def test_rebuilt_whole_energy_gradient_selfexcluded(self):
        from scf_weighted import gravity
        opts=dict(nmax=6,lmax=4,r0=100.,eta=1.,Rcent=300.)
        a,U,phi=gravity(self.x,self.m,**opts)
        for i,axis in [(0,0),(4,2),(16,1)]:
            dx=np.zeros_like(self.x);dx[i,axis]=.002
            fd=-(gravity(self.x+dx,self.m,**opts)[1]-gravity(self.x-dx,self.m,**opts)[1])/.004/self.m[i]
            self.assertAlmostEqual(a[i,axis],fd,delta=3e-7*max(1e-5,abs(fd)))
        self.assertEqual(U,.5*float(self.m@phi))

    def test_PJ_rotation_translation(self):
        from scf_weighted import gravity
        opts=dict(nmax=6,lmax=5,r0=100.,eta=.5,Rcent=600.)
        a,U,phi=gravity(self.x,self.m,**opts)
        F=self.m[:,None]*a;y=self.x-np.average(self.x,axis=0,weights=self.m)
        self.assertLess(np.linalg.norm(F.sum(0))/np.linalg.norm(F,axis=1).sum(),3e-13)
        self.assertLess(np.linalg.norm(np.cross(y,F).sum(0))/np.sum(np.linalg.norm(y,axis=1)*np.linalg.norm(F,axis=1)),3e-12)
        q,_=np.linalg.qr(self.rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q)
        b,V,psi=gravity(self.x@q.T+[80000,-30000,2000],self.m,**opts)
        np.testing.assert_allclose(b,a@q.T,rtol=3e-10,atol=2e-12)
        np.testing.assert_allclose(psi,phi,rtol=3e-11,atol=1e-12)
        self.assertLess(abs(V/U-1),3e-11)


if __name__=='__main__':unittest.main()
