#!/usr/bin/env python3
import unittest
import mpmath as mp


class ShearTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mp.mp.dps=60

    def model(self):
        return __import__('ic13_shear_repair')

    def test_kinetic_completion_and_boundary_neighborhoods(self):
        m=self.model()
        for r in map(mp.mpf,('0','1','1.17','1.24')):
            xi,u=mp.mpf('.23'),mp.mpf('.63')
            q=[-3*r/mp.exp((4-3*u)*xi),xi,u]
            v=m.coefficients(q)
            self.assertGreater(v['As'],0)
            self.assertGreaterEqual(v['new_UV']-3*v['d']/4,-mp.mpf('1e-45'))
            self.assertLess(abs(v['new_UV']-(v['old_UV']+v['E']*v['deltaA']/6)),mp.mpf('1e-43'))
            if r in (0,1,mp.mpf('1.24')):
                self.assertEqual(v['deltaA'],0)

    def test_homogeneous_hessian_from_actual_action(self):
        m=self.model()
        q=m.witness()['point']
        rho,xi,u=q
        x=[mp.mpf(0),rho/3,rho/3,rho/3,xi,u]
        H=m.homogeneous_hessian(q)
        for i in range(6):
            for j in range(6):
                order=tuple(int(k==i)+int(k==j) for k in range(6))
                direct=mp.diff(m.raw_homogeneous,tuple(x),order)
                self.assertLess(abs(H[i,j]-direct),mp.mpf('1e-37'))

    def test_curvature_response_and_actual_scalar_instability(self):
        m=self.model()
        bg=m.witness()
        c=m.coefficients(bg['point'])
        cr=m.curvature_derivatives(bg['point'])[1]
        self.assertGreater(abs(cr),mp.mpf('1e-8'))
        errors=[]
        for k in (mp.mpf('1e3'),mp.mpf('1e5')):
            p=m.pencil(bg,k)
            self.assertLess(mp.norm(p['auxiliary_EL_residual']),mp.mpf('1e-35'))
            self.assertGreater(p['reduced'][1,1],0)
            self.assertLess(mp.det(p['reduced']),0)
            errors.append(abs(mp.det(p['reduced'])/k**4+cr**2))
        self.assertLess(errors[1],errors[0]/1000)

    def test_curvature_square_cancels_quartic_but_fails_physical_cone(self):
        m=self.model()
        bg=m.witness()
        residuals=[]
        for k in (mp.mpf('1e3'),mp.mpf('1e5')):
            result=m.pencil(bg,k,True)
            self.assertGreater(mp.det(result['reduced']),0)
            residuals.append(abs(mp.det(result['reduced'])/k**4))
            self.assertGreater(m.evolving_scalar(bg,k,True)['speed_squared'],1)
        self.assertLess(residuals[1],residuals[0]/1000)

    def test_background_derivatives_match_centered_difference(self):
        m=self.model()
        bg=m.witness()
        k=mp.mpf('1000')
        actual=m.evolving_scalar(bg,k,True)
        tangent=[bg['rhodot'],*list(bg['qdot'])]
        dt=mp.mpf('1e-9')
        matrices=[]
        for sign in (-1,1):
            point=[q+sign*dt*v for q,v in zip(bg['point'],tangent)]
            matrices.append(m.pencil(dict(point=point),k,True,
                                    sign*dt*bg['logVdot'],sign*dt*bg['logVdot']/3)['reduced'])
        numeric=(matrices[1]-matrices[0])/(2*dt)
        for key,i,j in (('Adot',1,1),('Bdot',0,1)):
            self.assertLess(abs(numeric[i,j]/actual[key]-1),mp.mpf('1e-9'))


if __name__=='__main__':
    unittest.main()
