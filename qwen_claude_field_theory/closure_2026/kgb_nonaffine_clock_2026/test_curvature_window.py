import unittest
import numpy as np
import curvature_window as w


class CurvatureWindow(unittest.TestCase):
    def test_constructive_criterion_samples(self):
        rng=np.random.default_rng(9247)
        for _ in range(200):
            beta=10**rng.uniform(-5,2);r=-10**rng.uniform(-2,2)
            b=rng.normal();I=2*abs(b)-r+10**rng.uniform(-3,2)
            k,t=w.construct(I,r,b,beta)
            self.assertGreater(k,abs(b));self.assertLess(t,0)
            # Minimum of exact quadratic over all directions, not a mesh.
            self.assertGreater(w.light_minimum(k,r,t,b),0)
            self.assertAlmostEqual(k-t/beta,I)

    def test_impossible_and_zero_slope_sectors(self):
        self.assertIsNone(w.construct(2,-1,1,.1))
        self.assertIsNone(w.construct(5,1,1,.1))
        self.assertEqual(w.select_control(4,0,-1,-1,.1,0)['status'],'fixed_healthy')
        self.assertEqual(w.select_control(-4,0,-1,-1,.1,0)['status'],'fixed_unhealthy')

    def test_actual_inverse_correlation_and_repair(self):
        for y in (.1,1.,2.,10.):
            X,U,_=w.n.old.initial(1e-6,y,.1,.25,1.5)
            z=-1.5*w.n.old.metric(1e-6,y)['g']
            row=w.inspect_window(1e-6,y,X,U,z)
            self.assertLess(row['correlation_residual'],2e-8)
            if row['status']=='constructed':
                self.assertTrue(row['selected']['strict_EF'])
                self.assertLess(row['selected']['residual']['metric'],1e-9)


if __name__=='__main__':unittest.main()
