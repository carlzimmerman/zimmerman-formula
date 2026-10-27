import unittest
import numpy as np
from evolution import initial_conditions,vector_J
from fast_gravity import gravity
from run_resolution import unbind


class ResolutionDriverTests(unittest.TestCase):
    def test_prepared_virials_masses_and_zero_bulk(self):
        # A normalization error can fake a more strongly collapsing dwarf.
        x,v,m,cold,ic=initial_conditions(512,64,87319,20.,gravity)
        a,_,_=gravity(x,m,20.)
        for mask,ratio in [(cold,.2),(~cold,1.)]:
            W=float(np.sum(m[mask,None]*x[mask]*a[mask]))
            K=float(.5*np.sum(m[mask,None]*v[mask]**2))
            self.assertAlmostEqual(2*K/abs(W),ratio,places=13)
        np.testing.assert_allclose(np.sum(m[:,None]*x,axis=0),0.,atol=1e-5)
        np.testing.assert_allclose(np.sum(m[:,None]*v,axis=0),0.,atol=1e-6)
        self.assertAlmostEqual(m[cold].sum()/m[~cold].sum(),53.64,places=12)

    def test_unbinding_keeps_bound_pair_and_rejects_fast_intruder(self):
        # Failing to refit the bulk velocity or including each self potential
        # can retain an arbitrarily fast intruder as a bound remnant member.
        x=np.array([[-1.,0.,0.],[1.,0.,0.],[0.,2.,0.]])
        v=np.array([[0.,.2,0.],[0.,-.2,0.],[100.,0.,0.]])
        m=np.array([1000.,1000.,1.])
        ids,bulk,_=unbind(x,v,m,np.zeros(3),.1,10.,gravity)
        np.testing.assert_array_equal(ids,[0,1])
        np.testing.assert_allclose(bulk,0.,atol=1e-12)


if __name__=='__main__':unittest.main()
