"""Tests catch inconsistent prolongation, lost matter response, and fake closure."""
import importlib.util
import unittest
import numpy as np


class SecondPreservationTests(unittest.TestCase):
    def module(self):
        spec=importlib.util.find_spec('ic36_second_preservation')
        self.assertIsNotNone(spec, 'Second-preservation implementation is missing')
        import ic36_second_preservation
        return ic36_second_preservation

    def test_polynomial_differentiation_and_centered_integral(self):
        m=self.module(); r=np.linspace(1,2,17)
        p=m.fit(r,r**4,8)
        np.testing.assert_allclose(p.deriv(2)(r),12*r*r,atol=1e-9)
        a=p.integ()
        self.assertAlmostEqual(float(a(2)-a(1)),31/5,places=10)

    def test_grid_does_not_round_beyond_integrated_endpoints(self):
        m=self.module()
        self.assertTrue(callable(getattr(m,'grid',None)))
        lo,hi=2.-.006/2,2.+.006/2
        r=m.grid(lo,hi,65)
        self.assertEqual(r[0],lo);self.assertEqual(r[-1],hi)
        self.assertTrue(np.all((r>=lo)&(r<=hi)))

    def test_compatible_and_incompatible_sources_are_distinguished(self):
        m=self.module(); r=np.linspace(1,2,49)
        C=np.tile([-1.,2.,1.],(len(r),1))
        W=np.tile([2.,-1.,3.],(len(r),1))
        f=r**3; f1=3*r*r; f2=6*r
        FC=-(-f+2*f1+f2); FW=-(2*f-f1+3*f2)
        good=m.compatibility(r,C,W,FC,FW,12)
        self.assertLess(good['max_W_residual'],1e-7)
        bad=m.compatibility(r,C,W,FC,FW+r**4,12)
        self.assertGreater(bad['max_W_residual'],1e-4)

    def test_second_matter_jet_includes_generated_flux(self):
        m=self.module()
        # At a point with HQ=HQdot=beta=0, j=2, e^(S-2Q)/v=1,
        # gdot'=3 and gdot=0, the second density rate is 6, not 0.
        got=m.matter_second(2.,0.,0.,0.,0.,0.,0.,0.,2.,1.,0.,3.)
        self.assertAlmostEqual(float(got),6.)

    def test_canonical_flux_second_derivative_identity(self):
        m=self.module()
        self.assertTrue(callable(getattr(m,'identities',None)))
        for name,value in m.identities().items():
            self.assertEqual(value,0,name)

    def test_actual_collar_second_response_without_projection(self):
        m=self.module(); report=m.FirstJet().experiment(degree=8,nodes=33,step=1e-4)
        self.assertLess(report['initial_constraint'],1e-8)
        self.assertLess(report['first_preservation'],1e-7)
        self.assertLess(report['independent_momentum_first'],1e-4)
        self.assertLess(report['independent_second_response_error'],1e-4*report['W_source_scale'])
        self.assertLess(report['corrected_C_second'],1e-4*report['W_source_scale'])
        # No assertion of a desired compatibility verdict, rank, or DOF count.


if __name__=='__main__':unittest.main()
