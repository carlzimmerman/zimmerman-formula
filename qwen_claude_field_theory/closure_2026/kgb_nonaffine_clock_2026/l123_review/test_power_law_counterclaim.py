#!/usr/bin/env python3
"""Exact counterclaim certificate; no CMB fit or full-theory health claim.

Signature (-+++), X=phidot^2/2>0, P=X^N, N>=2, expanding homogeneous
background, and conserved shift density n=P_X sqrt(2X), a^3 n=constant.
All checks use exact SymPy arithmetic. Symbolic identities cover the stated
family; explicit N=1 and N=2 cases are controls, not a finite scan proof.
"""
import sys
import unittest
import sympy as s


def family():
    X = s.Symbol('X', positive=True)
    N = s.Symbol('N', positive=True)
    P = X**N
    PX = s.diff(P, X)
    D = s.diff(2*X*PX-P, X)
    rho = 2*X*PX-P
    n = PX*s.sqrt(2*X)
    return dict(X=X, N=N, P=P, PX=PX, D=D, rho=rho, n=n)


class PowerLawCounterclaimTests(unittest.TestCase):
    def assert_zero(self, expr):
        self.assertEqual(s.simplify(s.expand_power_base(expr, force=False)), 0)

    def test_homogeneous_lapse_action_variation_derives_density_and_current(self):
        f=family(); X,N=[f[k] for k in ('X','N')]
        lapse,a,v=s.symbols('lapse a v',positive=True)
        lagrangian=lapse*a**3*(v*v/(2*lapse*lapse))**N
        rho_variation=(-s.diff(lagrangian,lapse)/a**3).subs(lapse,1)
        n_variation=(s.diff(lagrangian,v)/a**3).subs(lapse,1)
        self.assert_zero(rho_variation-f['rho'].subs(X,v*v/2))
        self.assert_zero(n_variation-f['n'].subs(X,v*v/2))

    def test_exact_density_current_and_hessian(self):
        f=family(); X,N,PX,D,rho,n=[f[k] for k in ('X','N','PX','D','rho','n')]
        self.assert_zero(rho-(2*N-1)*X**N)
        self.assert_zero(n-s.sqrt(2)*N*X**(N-s.Rational(1,2)))
        self.assert_zero(D-N*(2*N-1)*X**(N-1))
        self.assert_zero(s.diff(n,X)-D/s.sqrt(2*X))

    def test_charge_density_curvature_is_not_constant_in_general(self):
        f=family(); X,D,rho,n=[f[k] for k in ('X','D','rho','n')]
        rho_n=s.simplify(s.diff(rho,X)/s.diff(n,X))
        rho_nn=s.simplify(s.diff(rho_n,X)/s.diff(n,X))
        self.assert_zero(rho_n-s.sqrt(2*X))
        self.assert_zero(rho_nn-1/D)
        self.assertNotEqual(s.diff(rho_nn.subs(f['N'],2),X),0)

    def test_positive_standard_kessence_coefficients_and_sound_speed(self):
        f=family(); X,N=[f[k] for k in ('X','N')]
        t=s.Symbol('t', nonnegative=True)
        self.assert_zero(f['PX']/f['D']-1/(2*N-1))
        self.assertTrue(((2+t)*X**(1+t)).is_positive)
        self.assertTrue(((2+t)*(3+2*t)*X**(1+t)).is_positive)
        self.assertTrue((1/(3+2*t)).is_positive)
        self.assertTrue((1-1/(3+2*t)).is_positive)

    def test_conserved_shift_charge_fixes_exact_redshift_exponent(self):
        f=family(); X,N,P,rho,n=[f[k] for k in ('X','N','P','rho','n')]
        # n_dot+3Hn=0. These logarithmic slopes avoid inverting fractional powers.
        X_dot_over_H=-3*n/s.diff(n,X)
        exponent=s.simplify(-s.diff(rho,X)*X_dot_over_H/rho)
        self.assert_zero(exponent-6*N/(2*N-1))
        self.assert_zero(s.diff(rho,X)*X_dot_over_H+3*(rho+P))
        self.assert_zero(exponent-3*(1+P/rho))

    def test_all_N_at_least_two_have_exponent_strictly_between_three_and_six(self):
        t=s.Symbol('t', nonnegative=True); N=2+t
        exponent=6*N/(2*N-1)
        self.assert_zero(exponent-3-3/(3+2*t))
        self.assert_zero(4-exponent-2*t/(3+2*t))
        self.assertTrue((3/(3+2*t)).is_positive)
        self.assertTrue((2*t/(3+2*t)).is_nonnegative)
        self.assert_zero(6-exponent-(6+6*t)/(3+2*t))
        self.assertTrue(((6+6*t)/(3+2*t)).is_positive)

    def test_N_two_is_exact_nonstiff_counterexample(self):
        f=family(); X=f['X']
        rho=s.simplify(f['rho'].subs(f['N'],2)); n=s.simplify(f['n'].subs(f['N'],2))
        self.assert_zero(rho-3*X**2)
        self.assert_zero(n-2*s.sqrt(2)*X**s.Rational(3,2))
        self.assert_zero(rho**3-s.Rational(27,64)*n**4)
        self.assertEqual(s.Rational(6*2,2*2-1),4)
        self.assertEqual(s.simplify((f['PX']/f['D']).subs(f['N'],2)),s.Rational(1,3))

    def test_canonical_N_one_recovers_stiff_control(self):
        f=family(); rho=f['rho'].subs(f['N'],1); n=f['n'].subs(f['N'],1)
        self.assert_zero(rho-n*n/2)
        self.assertEqual(s.Rational(6,2-1),6)
        self.assertEqual(s.simplify((f['PX']/f['D']).subs(f['N'],1)),1)

    def test_arbitrarily_small_positive_sound_speed_bound(self):
        delta,gap=s.symbols('delta gap', positive=True)
        # Any N at least 2+1/(2 delta) works; arbitrarily large integers qualify.
        N=2+1/(2*delta)+gap
        cs2=s.factor(1/(2*N-1))
        self.assert_zero(cs2-delta/(1+3*delta+2*delta*gap))
        self.assertTrue(cs2.is_positive)
        self.assertTrue(s.factor(delta-cs2).is_positive)
        self.assert_zero(6*N/(2*N-1)-3-3*cs2)


if __name__=='__main__':
    print('EXACT_CERTIFICATE Python='+sys.version.split()[0]+' SymPy='+s.__version__,flush=True)
    print('SCOPE: P=X^N, X>0, N>=2, conserved a^3*n; no CMB, clustering, strong-coupling or full MOND certificate.',flush=True)
    unittest.main(verbosity=2)
