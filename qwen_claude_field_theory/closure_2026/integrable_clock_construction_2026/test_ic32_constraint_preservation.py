"""Action-derived time tangent, with a finite-kick test that does not reproject."""
import importlib.util
import unittest
import sympy as s
import numpy as np


class PreservationTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('ic32_constraint_preservation'))
        import ic32_constraint_preservation
        return ic32_constraint_preservation

    def test_inhomogeneous_evolution_and_curvature_jets(self):
        for name,value in self.module().identities().items():
            self.assertEqual(s.simplify(value),0,name)

    def test_unprojected_kicks_improve_quadratically(self):
        out=self.module().experiment(amplitude=1,nodes=1601)
        self.assertTrue(out['solved'])
        self.assertLess(out['max_preservation_residual'],1e-5)
        for key,ratio in out['kick_ratios'].items():
            self.assertGreater(ratio,3.2,key)
        self.assertGreater(out['frozen_auxiliary_violation'],out['kicks'][0]['lapse'])

    def test_radiation_legendre_transform_against_original_action(self):
        m=self.module()
        j,grad,S,Q=.7,.2,.1,.15
        f=m.fluid(j,grad,S,Q,1/3,3/4)
        k2=np.exp(-2*Q)*grad**2
        X=(f['v']**2-k2)/2
        self.assertLess(abs(j-2*X*f['v']),1e-12)
        self.assertLess(abs(f['h']-np.exp(S)*(j*f['v']-X**2)),1e-12)
        self.assertLess(abs(f['pw']),1e-12)

    def test_mesh_merges_roundoff_duplicates(self):
        mesh=self.module().merge_mesh([2.,np.nextafter(2.,3.),3.,3.+1e-8])
        self.assertEqual(len(mesh),3)
        self.assertTrue(np.all(np.diff(mesh)>0))


if __name__=='__main__':
    unittest.main()
