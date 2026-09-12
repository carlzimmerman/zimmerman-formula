import unittest
import numpy as np
from cubic_debraiding import derive,corrected,gamma0_jets


class CubicDebraidingTests(unittest.TestCase):
    def test_covariant_tensor_and_discriminant_identities(self):
        self.assertTrue(all(derive()['checks'].values()))

    def test_zero_gamma_is_nontrivial_previous_symbol(self):
        j=gamma0_jets(1/110,1/200,5/121,10/11,1/12000)
        result=corrected(j,10/11,1.031781,1/12000,1.,gamma=0.)
        self.assertLess(result['quarter_finite_gamma'],0.)
        self.assertEqual(result['quarter_finite_gamma'],result['quarter_gamma0'])
        self.assertEqual(result['deltaK'],0.)

    def test_finite_gamma_feedback_can_be_large(self):
        # This guards against a blanket 'gamma is irrelevant' implementation.
        j=gamma0_jets(1/110,1/200,5/121,10/11,1/12000)
        Q,Y=10/11,1/12000
        C=j['WY']+2*Y*j['WYY']
        s=j['PX']*(j['W']-2*Q*Q*C)/(j['W']*C)
        zero=corrected(j,Q,s,Y,1.,gamma=0.)
        finite=corrected(j,Q,s,Y,1.,gamma=1.)
        self.assertGreater(finite['deltaK'],1.)
        self.assertLess(finite['quarter_finite_gamma'],100*zero['quarter_finite_gamma'])
        self.assertLess(finite['linear_correction_coefficient'],0.)
        self.assertLess(finite['quadratic_correction_coefficient'],0.)

    def test_homogeneous_known_metric_feedback(self):
        Q=3/4;g=1/7;M2=2.
        j=gamma0_jets(2.,1/4,1/3,Q,0.)
        result=corrected(j,Q,1.2,0.,0.,gamma=g,M2=M2)
        self.assertAlmostEqual(result['deltaK'],6*g*g*Q**4/M2,places=14)
        self.assertAlmostEqual(result['deltaG'],-2*g*g*Q**4/M2,places=14)
        self.assertEqual(result['deltaB'],0.)

    def test_gamma_sign_does_not_change_explicit_affine_feedback(self):
        j=gamma0_jets(2.,1/4,1/3,3/4,1/100)
        a=corrected(j,3/4,1.2,1/100,.6,gamma=1/7)
        b=corrected(j,3/4,1.2,1/100,.6,gamma=-1/7)
        for key in ('deltaK','deltaB','deltaG','quarter_finite_gamma'):
            self.assertEqual(a[key],b[key])

    def test_nonzero_hessian_flrw_direct_cubic_control(self):
        Q,Y,H,qd,g=3/4,1/100,2/3,-1/5,1/7
        j=gamma0_jets(2.,1/4,1/3,Q,Y)
        hessian=np.diag([qd,-H*Q,-H*Q,-H*Q])
        hessian[0,1]=hessian[1,0]=-H*np.sqrt(Y)
        point=corrected(j,Q,1.2,Y,1.,gamma=g,hessian_cov=hessian)
        self.assertAlmostEqual(point['hessian_deltaK'],-12*g*H*Q,places=14)
        self.assertAlmostEqual(point['hessian_deltaB'],-8*g*H*np.sqrt(Y),places=14)
        self.assertAlmostEqual(point['hessian_deltaG'],-4*g*(qd+2*H*Q),places=14)


if __name__=='__main__':
    unittest.main()
