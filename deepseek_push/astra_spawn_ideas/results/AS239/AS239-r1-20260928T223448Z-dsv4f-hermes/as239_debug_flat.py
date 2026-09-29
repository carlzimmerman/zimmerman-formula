#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AS239 debug: validate the Ricci engine for the quadratic tensor Lagrangian
against a NUMERIC finite-difference of the full Einstein Lagrangian density
L_EH(eps) = (M/2) sqrt(-g)(R(g) - 2*Lambda) in FLAT space with a TT probe."""
import sympy as sp
import numpy as np

x, t = sp.symbols('x t')
eps = sp.Symbol('eps')
M = sp.Rational(1, 1)
e_diag = [0, 1, -1]

q0, k, w = sp.symbols('q0 k w')
qx = q0*sp.cos(k*x)*sp.cos(w*t)          # concrete probe (no slow modulation)

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

def Rsc_expr():
    out = sp.Integer(0)
    for mu in range(4):
        for nu in range(4):
            r = sp.Integer(0)
            for lam in range(4):
                r += (sp.diff(Gam(lam,mu,nu), t) if lam==0 else sp.diff(Gam(lam,mu,nu), x))
                r -= (sp.diff(Gam(lam,mu,lam), t) if nu==0 else sp.diff(Gam(lam,mu,lam), x))
            for alp in range(4):
                for bet in range(4):
                    r += Gam(alp,bet,alp)*Gam(bet,mu,nu) - Gam(alp,bet,nu)*Gam(bet,mu,alp)
            out += ginv(mu,nu)*sp.expand(r)
    return sp.expand(out)

def sdet():
    trA  = sum(eps*qx*e for e in e_diag)
    trA2 = sum((eps*qx*e)**2 for e in e_diag)
    return sp.Integer(1) + trA + (trA**2 - trA2)/2     # det_3 = 1 + trA + (tr^2-tr2)/2

Rsc = sp.expand(Rsc_expr())
L = sp.expand(sp.Rational(1,2)*sp.sqrt(sdet())*Rsc)    # (M=1, Lambda=0)
print("engine Rsc ep^0:", sp.simplify(Rsc.coeff(eps,0)))
print("engine Rsc ep^1:", sp.simplify(Rsc.coeff(eps,1)))
print("engine Rsc ep^2:", sp.simplify(Rsc.coeff(eps,2)))

# ---- numeric truth: second finite difference of L(eps) at fixed (x,t) -------
Lf = sp.lambdify((x,t,eps), L, 'numpy')
R0f = sp.lambdify((x,t,eps), Rsc, 'numpy')
import numpy as np
xs = np.linspace(0.3, 2.1, 7); ts = np.linspace(0.2, 1.3, 7)
k0, w0, q00 = 1.7, 2.3, 0.4
pts = [(xx, tt, k0, w0, q00) for xx in xs for tt in ts]
h = 1e-3
maxres = 0.0
for (xx, tt, kk, ww, q0v) in pts:
    Lm = float(Lf(xx, tt, -2*h)); L0 = float(Lf(xx, tt, 0)); Lp = float(Lf(xx, tt, 2*h))
    d2 = (Lp - 2*L0 + Lm)/(4*h*h)
    # engine second-order prediction at (xx,tt):
    qval = q0v*np.cos(kk*xx)*np.cos(ww*tt)
    qt = -q0v*np.cos(kk*xx)*ww*np.sin(ww*tt)
    qx = -q0v*kk*np.sin(kk*xx)*np.cos(ww*tt)
    qtt = -q0v*np.cos(kk*xx)*ww**2*np.cos(ww*tt)
    qxx = -q0v*kk**2*np.cos(kk*xx)*np.cos(ww*tt)
    qtx = q0v*kk*ww*np.sin(kk*xx)*np.sin(ww*tt)
    # engine density quadratic form evaluated from sympy at the point:
    val = float(Lf(xx, tt, 0) + (h**2*0))  # placeholder
    # direct: L(eps) ~ L0 + eps^2 * L2val
    L2v = (float(Lf(xx, tt, h)) + float(Lf(xx, tt, -h)) - 2*float(Lf(xx, tt, 0)))/(h*h)
    res = abs(L2v - d2)
    maxres = max(maxres, res)
print("numeric second-difference consistency (symmetric vs one-sided):", maxres)

# now compare engine eps^2 coeff vs numeric L2v
L2sym = sp.lambdify((x,t), sp.expand(L.coeff(eps,2)), 'numpy')
maxrel = 0.0
for (xx, tt, kk, ww, q0v) in pts:
    L2num = (float(Lf(xx,tt,h)) + float(Lf(xx,tt,-h)) - 2*float(Lf(xx,tt,0)))/(h*h)
    L2symv = float(L2sym(xx, tt))
    rel = abs(L2num - L2symv)/(abs(L2symv)+1e-30)
    maxrel = max(maxrel, rel)
print("max |L2_numeric - L2_engine|/|L2_engine| over 49 points:", maxrel)