import unittest
import numpy as np


class RadialTests(unittest.TestCase):
    def test_core_and_point_limits(self):
        import law
        from radial_reference import radial_force
        k=.7;ell=.8;r=np.array([1e-6,2e-6]);g=k*r
        t=radial_force(r,g,np.full_like(r,k),np.zeros_like(r),ell)
        z0=(3*ell**2*k**2)**2
        expected=k*(law.R(z0)-4/3*law.zRprime(z0))
        np.testing.assert_allclose(t['total']/r,expected,rtol=2e-10)
        r=np.array([.001,.002]);g=1/r**2
        p=radial_force(r,g,-2/r**3,6/r**4,1.)
        np.testing.assert_allclose(p['phantom'],(-5/9)*r**4,rtol=1e-9)

    def test_plummer_newton_and_plain(self):
        import law
        from radial_reference import radial_force,plummer_fields
        r=np.geomspace(1e-4,1e3,200);g,gp,gpp=plummer_fields(r,1.3,.8)
        n=radial_force(r,g,gp,gpp,3.,newtonian=True)
        np.testing.assert_array_equal(n['total'],g)
        p=radial_force(r,g,gp,gpp,0.)
        np.testing.assert_allclose(p['total'],g*law.Qprime(g*g),rtol=1e-12)


if __name__=='__main__':unittest.main()
