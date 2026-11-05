from pathlib import Path
import unittest
import numpy as np


class RadialTests(unittest.TestCase):
    def test_radial_reference_exists_and_ell_zero(self):
        self.assertTrue(Path(__file__).with_name('radial_reference.py').exists(),'radial reference absent')
        from radial_reference import plummer_fields,radial_force
        r=np.geomspace(1e-4,1e3,200);g,gp,gpp=plummer_fields(r,1.,.7)
        q=radial_force(r,g,gp,gpp,0.)
        target=(.5+np.sqrt(.25+1/g))*g
        np.testing.assert_allclose(q['total'],target,rtol=2e-14)

    def test_point_origin_and_far_field(self):
        from radial_reference import radial_force
        r=np.array([1e-4,1e5]);g=1/r**2;gp=-2/r**3;gpp=6/r**4
        q=radial_force(r,g,gp,gpp,1.)
        self.assertAlmostEqual(q['phantom'][0]/r[0],1/(3*np.sqrt(6)),delta=2e-8)
        self.assertAlmostEqual(q['total'][1]*r[1],1.,delta=1e-5)

    def test_smooth_core(self):
        import law
        from radial_reference import plummer_fields,radial_force
        r=np.array([1e-6]);g,gp,gpp=plummer_fields(r,1.,1.)
        ell=.3;z0=3*ell**2
        expected=law.R(z0)-(2/3)*law.zRprime(z0)
        actual=radial_force(r,g,gp,gpp,ell)['total']/r
        np.testing.assert_allclose(actual,expected,rtol=1e-10)


if __name__=='__main__':unittest.main()
