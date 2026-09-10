import unittest
import numpy as np
import quadratic_flow as f


class QuadraticContinuation(unittest.TestCase):
    def test_affine_boundary_recovered(self):
        a=f.integrate(j0=0,log_span=1.)
        self.assertTrue(a['event'])
        self.assertAlmostEqual(a['final']['y'],.1404169525918055,places=8)
        self.assertLess(a['max_metric_residual'],1e-8)

    def test_nonaffine_refinement_preserves_equations(self):
        runs=[f.integrate(j0=-25000,log_span=.02,max_step=h) for h in (.005,.0025)]
        for r in runs:
            self.assertTrue(r['success'])
            self.assertLess(r['max_metric_residual'],1e-8)
        np.testing.assert_allclose(runs[0]['final_state'],runs[1]['final_state'],rtol=1e-7,atol=1e-10)


if __name__=='__main__':unittest.main()
