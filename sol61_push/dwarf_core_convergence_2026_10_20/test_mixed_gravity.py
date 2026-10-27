"""Independent gates for a separately declared compensated mixed GPU candidate.

This candidate is not admitted by the existing DS precision contract. Its
empirical error must be much smaller than physical convergence tolerances,
and trajectory/conservation controls are still required.
"""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from fast_gravity import gravity as reference

path=Path(__file__).with_name('mixed_gravity.py')
if path.exists():
    spec=importlib.util.spec_from_file_location('mixed_candidate',path)
    candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
else:candidate=None


class MixedCandidateTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(candidate,'mixed candidate not implemented')

    def compare(self,x,m,eps):
        a,U,phi=candidate.gravity(x,m,eps);b,V,psi=reference(x,m,eps)
        self.assertLess(np.linalg.norm(a-b)/np.linalg.norm(b),5e-7)
        self.assertLess(np.max(np.linalg.norm(a-b,axis=1)/np.maximum(np.linalg.norm(b,axis=1),1e-100)),2e-6)
        self.assertLess(np.max(abs((phi-psi)/psi)),5e-7)
        self.assertLess(abs(U/V-1),5e-7)
        return a,U,phi

    def test_unequal_mass_and_coincident_distinct_sources(self):
        rng=np.random.default_rng(19873);x=rng.normal(size=(513,3))*[500,100,30]
        x[1]=x[0];m=rng.uniform(.1,5,len(x))*1000
        self.compare(x,m,5.)

    def test_close_remnant_with_far_first_tail_and_translation(self):
        rng=np.random.default_rng(19874)
        x=np.r_[[[-4e5,5e5,-2e5]],rng.normal(size=(256,3))*[2,3,1]+[80000.12345,-30000.9876,2000.42]]
        m=rng.uniform(.1,5,len(x))*1000
        a,U,phi=self.compare(x,m,2.)
        b,V,psi=candidate.gravity(x+[200000.,-300000.,100000.],m,2.)
        np.testing.assert_allclose(a,b,rtol=2e-6,atol=1e-9)
        self.assertLess(abs(V/U-1),5e-7)

    def test_accumulation_and_vector_invariants(self):
        rng=np.random.default_rng(19875);x=rng.normal(size=(4097,3))*100
        m=rng.uniform(.1,5,len(x))*1000
        a,U,phi=self.compare(x,m,5.);f=m[:,None]*a
        self.assertLess(np.linalg.norm(f.sum(0))/np.linalg.norm(f,axis=1).sum(),1e-8)
        self.assertLess(np.linalg.norm(np.cross(x,f).sum(0))/np.sum(np.linalg.norm(x,axis=1)*np.linalg.norm(f,axis=1)),1e-8)


if __name__=='__main__':unittest.main()
