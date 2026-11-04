import unittest
import numpy as np


class RadialTests(unittest.TestCase):
    def test_core_and_point_limits(self):
        import law
        from radial_reference import radial_force
        for p in (1.25,1.5,1.75):
            k=.7;ell=.8;r=np.array([1e-6,2e-6]);g=k*r;z0=(3*ell**2*k**2)**p
            t=radial_force(r,g,np.full_like(r,k),np.zeros_like(r),ell,p=p)
            np.testing.assert_allclose(t['total']/r,k*(law.R(z0)-(2*p/3)*law.zRprime(z0)),rtol=3e-10)
            r=np.array([1e-4,2e-4]);g=1/r**2
            t=radial_force(r,g,-2/r**3,6/r**4,1.,p=p)
            expected=(2-p*(2+3*p)/3)*6**(-p/2)*r**(3*p-2)
            np.testing.assert_allclose(t['phantom'],expected,rtol=3e-6)

    def test_radial_plain_control(self):
        import law
        from radial_reference import radial_force,plummer_fields
        r=np.geomspace(1e-4,1e3,200);g,gp,gpp=plummer_fields(r,1.3,.8)
        for p in (1.25,1.5,1.75):
            t=radial_force(r,g,gp,gpp,0.,p=p)
            np.testing.assert_allclose(t['total'],g*law.Qprime(g*g),rtol=1e-12)


if __name__=='__main__':unittest.main()
