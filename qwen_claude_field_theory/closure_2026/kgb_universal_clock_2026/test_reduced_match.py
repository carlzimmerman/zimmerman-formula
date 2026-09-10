import unittest
import numpy as np


class ReducedTests(unittest.TestCase):
    def test_pressure_is_shared_without_residual_projection(self):
        import reduced_match as r
        rows=r.pair(np.log([1.5,.15,.128]))
        self.assertAlmostEqual(rows[0]['P']/rows[1]['P'],1.,places=12)

    def test_closed_curvature_matches_varied_inverse(self):
        import reduced_match as r
        for a in r.pair(np.log([1.5,.15,.128])):
            A,B=r.curvature_parts(a)
            for f in (-.04,.02,.2):
                _,v=r.s.raw_jet(a['eps'],a['y'],a['X'],a['U'],a['w']/f,a['F'],f)
                np.testing.assert_allclose(A+f*B,v[3:]/f,rtol=2e-8)

    def test_curvature_control_is_solved_not_assigned(self):
        import reduced_match as r
        A=np.array([2.,4.]);B=np.array([-1.,-2.])
        f,err=r.control(A,B)
        self.assertAlmostEqual(f,2.);self.assertLess(np.linalg.norm(err),1e-14)
        _,err=r.control(np.array([2.,3.]),B)
        self.assertGreater(np.linalg.norm(err),.1)


if __name__=='__main__':unittest.main()
