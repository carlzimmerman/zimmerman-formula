import unittest
import numpy as np
import sympy as sy
from principal_audit import derive,principal,proxy_function,jets


class PrincipalAuditTests(unittest.TestCase):
    def test_explicit_invariant_hessian_and_schur(self):
        result=derive()
        self.assertTrue(all(result['checks'].values()))

    def test_nontrivial_zero_gradient_baseline(self):
        # Negative clock speed recovered from actual Hessian/Schur formulas,
        # at rational values not tied to the source numerical test fixture.
        U,d,ell,Q,s=2.,3/7,1/5,4/5,5/4
        result=principal(U,d,ell,Q,s,0.,0.)
        margin=(U-2*d*Q*Q)/U
        expected=(1-s)*margin/(2-margin)
        self.assertAlmostEqual(result['G']/result['K'],expected,places=14)
        self.assertLess(result['quarter_discriminant'],0.)

    def test_exact_proxy_zero_counterexample(self):
        # Source tau=0 coefficient values exactly rational, with finite Y.
        # Choose s by the proxy marginal condition, rather than numerically
        # solving it, so this is an exact algebraic counterexample family.
        d=sy.Rational(1,200);U=sy.Rational(1,110);ell=sy.Rational(5,121)
        Q=sy.Rational(10,11);Y=sy.Rational(1,12000)
        WY=d/sy.sqrt(1+Y/ell)
        WYY=-d/(2*ell)*(1+Y/ell)**sy.Rational(-3,2)
        W=U+2*d*ell*(sy.sqrt(1+Y/ell)-1)
        PX=U*d/(U-2*d*(Q*Q-Y));PXX=2*U*d*d/(U-2*d*(Q*Q-Y))**2
        C=WY+2*Y*WYY;F=W-2*Q*Q*C-2*Y*WY;K=2*PX+4*Q*Q*PXX
        negative=-8*PX*Y*(PXX+K*Q*Q*C*WY/(W*F))
        for value in (PX,PXX,C,F,W,WY,K):
            self.assertTrue(bool(value>0))
        self.assertTrue(bool(negative<0))
        s=PX*(W-2*Q*Q*C)/(W*C)
        result=principal(float(U),float(d),float(ell),float(Q),float(s),float(Y),1.)
        self.assertAlmostEqual(result['quarter_discriminant'],float(negative),places=14)
        self.assertLess(result['quarter_discriminant'],0.)
        self.assertGreater(max(abs(x) for x in result['phase_speeds_imag']),1e-3)
        self.assertLess(abs(proxy_function()(float(U),float(d),float(ell),float(Q),float(s),float(Y),'L')),1e-14)

    def test_orientation_reverses_drift_not_discriminant(self):
        args=(1/110,1/200,5/121,10/11,1.031781,1/4000)
        plus=principal(*args,1.)
        minus=principal(*args,-1.)
        self.assertAlmostEqual(plus['quarter_discriminant'],minus['quarter_discriminant'],places=14)
        np.testing.assert_allclose(plus['phase_speeds_real'],[-x for x in reversed(minus['phase_speeds_real'])],atol=1e-13)


if __name__=='__main__':
    unittest.main()
