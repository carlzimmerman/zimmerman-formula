"""Field equations and preserved action derivatives, not a theory certificate."""
import unittest
import numpy as np
import conformal_inverse as c
import conformal_flow as f


class ConformalInverse(unittest.TestCase):
    def test_independent_metric_equations_and_total_current(self):
        for sigma in (1e-6, .1, 1.):
            for y in (.1, 1., 10.):
                row = c.inspect(1e-6, y, *c.initial(1e-6,y,sigma,.25,1.5), sigma)
                self.assertLess(row['relative_metric_error'], 1e-8)
                self.assertLess(row['relative_total_current_error'], 2e-8)

    def test_curvatures_are_total_derivatives(self):
        eps,y,sigma=1e-6,.1,.1
        X,U,P=c.initial(eps,y,sigma,.25,1.5)
        a,pxx,gxx=c.action_curvatures(eps,y,X,U,P,sigma)
        tangent=np.array([1/a['ry'],a['z'],-2*a['g']*(2*X+U)-2*a['z'],a['PX']*a['z']])
        v=np.array([y,X,U,P]);h=1e-11
        lo=c.coefficients(eps,*(v-h*tangent),sigma)
        hi=c.coefficients(eps,*(v+h*tangent),sigma)
        numeric=np.array([hi['PX']-lo['PX'],hi['GX']-lo['GX']])/(2*h*a['z'])
        np.testing.assert_allclose(numeric,[pxx,gxx],rtol=2e-5)

    def test_radial_constraint_preservation(self):
        eps,y,sigma=1e-6,.1,.1
        X,U,P=c.initial(eps,y,sigma,.25,1.5)
        # 1e-11 loses precision by subtracting nearly equal large pressures;
        # a step scan (1e-8...1e-12) places 1e-10 in the converged window.
        a=c.coefficients(eps,y,X,U,P,sigma);h=1e-10
        ps=[]
        for sign in (-1,1):
            ps.append(c.pressure_from_gradient(eps,y+sign*h/a['ry'],
                       X+sign*h*a['z'],a['z']+sign*h*a['zr'],sigma))
        self.assertAlmostEqual((ps[1]-ps[0])/(2*h)/(a['PX']*a['z']),1,places=5)

    def test_short_same_action_continuation_and_refinement(self):
        runs=[f.integrate(sigma=.1,b=.25,d=1.5,log_span=.02,max_step=h)
              for h in (.005,.0025)]
        for run in runs:
            self.assertTrue(run['solver_success'])
            self.assertLess(run['max_metric_error'],1e-8)
            self.assertGreater(run['accepted_points'],2)
        np.testing.assert_allclose(runs[0]['final_state'],runs[1]['final_state'],rtol=2e-7,atol=1e-9)


if __name__=='__main__':unittest.main()
