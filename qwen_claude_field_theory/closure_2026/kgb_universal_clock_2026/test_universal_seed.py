import importlib
import unittest
import numpy as np


def api():
    try:return importlib.import_module('universal_seed')
    except ModuleNotFoundError:raise AssertionError('common-action seed matcher is not implemented')


class UniversalSeedTests(unittest.TestCase):
    def test_equal_mass_diagonal_control(self):
        m=api();spec=m.Spec(eps2=1e-6)
        theta=np.log([.128,1.5,.1,.128,1.5])
        self.assertLess(np.max(abs(m.residual(theta,spec))),1e-13)

    def test_distinct_mass_changes_equations(self):
        m=api();theta=np.log([.128,1.5,.1,.128,1.5])
        self.assertGreater(np.linalg.norm(m.residual(theta,m.Spec())),1e-3)

    def test_curvatures_are_same_action_total_derivatives(self):
        m=api();eps,y,X,U,z=1e-6,.1,.5,1.28e-7,-.15
        a,vec=m.raw_jet(eps,y,X,U,z)
        b,pxx,gxx=m.n.action_curvatures(eps,y,X,U,z,j0=0.)
        np.testing.assert_allclose(vec,[b['P'],b['PX'],b['GX'],pxx,gxx],rtol=1e-12)

    def test_shared_curvature_cancels_at_equal_mass(self):
        m=api();spec=m.Spec(eps2=1e-6)
        theta=np.log([.128,1.5,.1,.128,1.5])
        for j in (-1e5,1e5):
            a,b=m.pair(theta,spec,j=j)
            np.testing.assert_allclose(a[1],b[1],rtol=1e-12)


if __name__=='__main__':unittest.main()
