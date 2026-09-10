import unittest
import numpy as np
import controlled_flow as c


class ControlledFlow(unittest.TestCase):
    def test_curvature_cancels_from_F_radial_second_derivative(self):
        n=c.w.n;eps,y=1e-6,.1;X,U,_=n.old.initial(eps,y,.1,.25,1.5)
        z=-1.5*n.old.metric(eps,y)['g'];values=[]
        for j in (-1e5,0.,1e5):
            a=n.coefficients(eps,y,X,U,z,j0=j)
            values.append(a['f']*a['zr']+j*z*z)
        np.testing.assert_allclose(values,[values[1]]*3,rtol=2e-12)

    def test_preserved_action_short_interval_and_refinement(self):
        a=c.integrate(log_span=.02,max_step=.005)
        b=c.integrate(log_span=.02,max_step=.0025)
        self.assertTrue(a['reached_target']);self.assertTrue(a['all_healthy'])
        self.assertLess(a['max_metric_residual'],1e-9)
        np.testing.assert_allclose(a['final_state'],b['final_state'],rtol=2e-6,atol=1e-9)


if __name__=='__main__':unittest.main()
