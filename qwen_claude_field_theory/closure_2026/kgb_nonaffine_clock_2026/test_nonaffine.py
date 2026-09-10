import unittest
import numpy as np
import nonaffine_inverse as n


class NonaffineInverse(unittest.TestCase):
    def test_affine_equation_and_curvature_control(self):
        eps,y=1e-6,.1;X,U,P=n.old.initial(eps,y,.1,.25,1.5)
        a=n.old.coefficients(eps,y,X,U,P,.1)
        b,pxx,gxx=n.action_curvatures(eps,y,X,U,a['z'],j0=0)
        old,opxx,ogxx=n.old.action_curvatures(eps,y,X,U,P,.1)
        np.testing.assert_allclose([b[k] for k in ('P','PX','GX','zr')],[old[k] for k in ('P','PX','GX','zr')],rtol=1e-10)
        np.testing.assert_allclose([pxx,gxx],[opxx,ogxx],rtol=1e-9)

    def test_nonzero_coupling_curvature_metric_and_current(self):
        for y in (.1,1.,5.):
            X,U,_=n.old.initial(1e-6,y,.1,.25,1.5)
            z=-1.5*n.old.metric(1e-6,y)['g']
            for j in (-1e5,1e5):
                a=n.coefficients(1e-6,y,X,U,z,j0=j)
                residual=n.physical_residual(a)
                self.assertLess(residual['metric'],1e-9)
                self.assertLess(residual['current'],1e-9)

    def test_radial_pressure_is_preserved(self):
        eps,y,X=1e-6,.1,.5;_,U,_=n.old.initial(eps,y,.1,.25,1.5)
        z=-1.5*n.old.metric(eps,y)['g'];j=1e5
        a=n.coefficients(eps,y,X,U,z,j0=j)
        point=np.array([y,X,U,z]);v=np.array([1/a['ry'],z,-2*a['g']*(2*X+U)-2*z,a['zr']])
        h=1e-25;b=n.coefficients(eps,*(point+1j*h*v),j0=j)
        self.assertAlmostEqual(np.imag(b['P'])/h/(a['PX']*z),1,places=8)


if __name__=='__main__':unittest.main()
