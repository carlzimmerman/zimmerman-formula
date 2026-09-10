import unittest
import numpy as np
import conformal_inverse as c
import gradient_inverse as v
import conformal_flow as flow


class GradientChart(unittest.TestCase):
    def test_overlap_with_pressure_chart(self):
        eps,y,sigma=1e-6,.1,.1
        X,U,P=c.initial(eps,y,sigma,.25,1.5)
        a,pxx,gxx=c.action_curvatures(eps,y,X,U,P,sigma)
        b,pxx2,gxx2=v.action_curvatures(eps,y,X,U,a['z'],sigma)
        np.testing.assert_allclose([b[k] for k in ('P','zr','PX','GX')],
                                  [a[k] for k in ('P','zr','PX','GX')],rtol=1e-11)
        np.testing.assert_allclose([pxx2,gxx2],[pxx,gxx],rtol=1e-10)

    def test_pressure_fold_is_not_linear_system_singularity(self):
        eps,y,sigma=1e-6,.1,.1
        X,U,_=c.initial(eps,y,sigma,.25,1.5)
        a=c.metric(eps,y);F=(1+sigma*X)/2;Fx=sigma/2
        z=-2*F*(a['g']+2/a['r'])/(3*Fx)
        b,pxx,gxx=v.action_curvatures(eps,y,X,U,z,sigma)
        self.assertTrue(np.isfinite([b['PX'],b['GX'],pxx,gxx]).all())
        self.assertNotEqual(np.linalg.det(b['matrix']),0)
        row=c.inspect_coefficients(b,pxx,gxx,sigma)
        self.assertLess(row['relative_metric_error'],1e-8)
        self.assertLess(row['relative_total_current_error'],1e-8)

    def test_gradient_and_pressure_flow_same_boundary(self):
        runs=[flow.integrate(log_span=1.,chart=chart,max_step=.01)
              for chart in ('pressure','gradient')]
        self.assertTrue(all(r['health_event'] for r in runs))
        self.assertAlmostEqual(runs[0]['final_y']/runs[1]['final_y'],1,places=8)
        for k in ('X','U','P','PX','GX','z'):
            np.testing.assert_allclose(runs[0]['final'][k],runs[1]['final'][k],rtol=2e-7)

    def test_deep_extension_is_preserved_but_has_a_boundary(self):
        runs=[flow.integrate(log_span=-9.210340371976184,chart='gradient',max_step=h)
              for h in (.02,.01)]
        for r in runs:
            self.assertTrue(r['health_event'])
            self.assertTrue(r['interior_strict_cone'])
            self.assertLess(r['final_y'],.001)
            self.assertGreater(r['final_y'],.00001)
            self.assertLess(r['max_metric_error'],1e-9)
        self.assertAlmostEqual(runs[0]['final_y']/runs[1]['final_y'],1,places=6)


if __name__=='__main__':unittest.main()
