#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AS239 debug 2: component-level validation of the Ricci engine at FLAT.
Hand-derived (diagonal family g = diag(-1,1,1+eq,1-eq), q=q(x,t)):
  R_tt = eps^2 (q q_tt + q_t^2/2)
  R_xx = eps^2 (q q_xx + q_x^2/2)
  R_yy = (1/2) eps (q_tt - q_xx) + (1/2) eps^2 (q_t^2 + q_x^2)
  R_zz = (1/2) eps (q_xx - q_tt) + (1/2) eps^2 (q_t^2 + q_x^2)
  scalar R = -R_tt + R_xx + (1- eq) R_yy + (1+eq) R_zz
Engine prints its own R_00..R_33; compare both ways numerically at several points."""
import sympy as sp
import numpy as np

x, t = sp.symbols('x t')
eps = sp.Symbol('eps')
M = sp.Rational(1, 1)
e_diag = [0, 1, -1]
q0, k, w = sp.symbols('q0 k w')
qx = q0*sp.cos(k*x)*sp.cos(w*t)

g = {}
g[(0,0)] = sp.Integer(-1)
for i in range(1,4):
    g[(0,i)] = 0; g[(i,0)] = 0
for i in range(1,4):
    for j in range(1,4):
        g[(i,j)] = sp.Integer(1 if i==j else 0) + eps*qx*sp.Integer(e_diag[i-1] if i==j else 0)

def ginv(mu, nu):
    if mu==0 and nu==0: return sp.Integer(-1)
    if mu==0 or nu==0: return sp.Integer(0)
    i, j = mu-1, nu-1
    if i==j:
        return 1 - eps*qx*e_diag[i] + eps**2*qx**2*e_diag[i]**2
    return sp.Integer(0)

def Gam(mu, nu, rho):
    terms = []
    for sig in range(4):
        dnu  = sp.diff(g[(sig,rho)], t) if nu==0 else sp.diff(g[(sig,rho)], x)
        drho = sp.diff(g[(sig,nu)], t) if rho==0 else sp.diff(g[(sig,nu)], x)
        dsig = sp.diff(g[(nu,rho)], t) if sig==0 else sp.diff(g[(nu,rho)], x)
        terms.append(ginv(mu,sig)*(dnu + drho - dsig))
    return sp.expand(sp.Rational(1,2)*sum(terms))

def RicciE(mu, nu):
    def deriv(expr, v): return sp.diff(expr, t) if v==0 else sp.diff(expr, x)
    out = sp.Integer(0)
    for lam in range(4):
        out += deriv(Gam(lam, mu, nu), lam) - deriv(Gam(lam, mu, lam), nu)
    for alp in range(4):
        for bet in range(4):
            out += Gam(alp, bet, alp)*Gam(bet, mu, nu) - Gam(alp, bet, nu)*Gam(bet, mu, alp)
    return sp.expand(out)

def coeff2(expr):
    E = sp.expand(expr)
    return E.coeff(eps, 0) + 0, E.coeff(eps, 1), E.coeff(eps, 2)

R00e = RicciE(0,0); R11e = RicciE(1,1); R22e = RicciE(2,2); R33e = RicciE(3,3)
R01e = RicciE(0,1); R12e = RicciE(1,2)
print("symmetry check R01 =", sp.simplify(R01e), " R12 =", sp.simplify(R12e))

q = qx
# hand forms (symbolic):
Rtt_h = eps**2*(q*sp.diff(q, t, 2) + sp.diff(q, t)**2/2)
Rxx_h = eps**2*(q*sp.diff(q, x, 2) + sp.diff(q, x)**2/2)
Ryy_h = sp.Rational(1,2)*eps*(sp.diff(q, t, 2) - sp.diff(q, x, 2)) + sp.Rational(1,2)*eps**2*(sp.diff(q,t)**2 + sp.diff(q,x)**2)
Rzz_h = sp.Rational(1,2)*eps*(sp.diff(q, x, 2) - sp.diff(q, t, 2)) + sp.Rational(1,2)*eps**2*(sp.diff(q,t)**2 + sp.diff(q,x)**2)

def repoint(E, xx, tt, kk, ww, q0v):
    sub = {x: xx, t: tt, k: kk, w: ww, q0: q0v}
    return float(sp.N(sp.expand(E).subs(sub)))

for (xx, tt, kk, ww, q0v) in [(0.7, 0.4, 1.7, 2.3, 0.4), (1.9, 1.1, 0.9, 0.6, 0.25),
                              (0.3, 2.0, 2.5, 2.5, 0.5)]:
    print("\npoint", (xx, tt, kk, ww, q0v), "(last one on-shell k=w)")
    for lab, He, Hh in [("R00", R00e, Rtt_h), ("R11", R11e, Rxx_h),
                        ("R22", R22e, Ryy_h), ("R33", R33e, Rzz_h)]:
        for o in (1, 2):
            e_ = repoint(He.coeff(eps, o), xx, tt, kk, ww, q0v)
            h_ = repoint(Hh.coeff(eps, o), xx, tt, kk, ww, q0v)
            print(f"  {lab} eps^{o}: engine {e_:+.8e}  hand {h_:+.8e}  diff {e_-h_:+.3e}")
    # scalar (full inverse series to O(eps^2)):
    ginv22 = 1 - eps*qx + eps**2*qx**2        # g^yy = 1/(1+eps q)
    ginv33 = 1 + eps*qx + eps**2*qx**2        # g^zz = 1/(1-eps q)
    Re = repoint(sp.expand(-R00e + R11e + ginv22*R22e + ginv33*R33e), xx, tt, kk, ww, q0v)
    Rh = repoint(sp.expand(-Rtt_h + Rxx_h + (1-eps*qx)*Ryy_h + (1+eps*qx)*Rzz_h), xx, tt, kk, ww, q0v)
    print(f"  Rsc eps^2: engine {Re:+.8e}  hand {Rh:+.8e}  diff {Re-Rh:+.3e}")