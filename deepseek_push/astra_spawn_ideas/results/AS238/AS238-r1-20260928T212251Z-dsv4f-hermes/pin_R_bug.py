#!/usr/bin/env python3
"""Pin down the numeric-R bug: compare numeric R at one cell with the validated sympy Rsc."""
import numpy as np
import sympy as sp
import importlib.util

spec = importlib.util.spec_from_file_location('dc', 'debug_curvature.py')
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)

# ---- sympy side: reuse the exact expression builder from as238_derive.py -------
src = open('as238_derive.py').read()
# extract only the parts we need by exec'ing and grabbing Rsc via a stub
import types, sys
# Instead: rebuild minimal sympy R for the flat single-mode case
t = sp.Symbol('t')
a = sp.Function('a')(t)
q = sp.Function('q')(t)
C, S = sp.symbols('C S')
kz = sp.Symbol('kz')
e11, e12, e13, e22, e23, e33 = sp.symbols('e11 e12 e13 e22 e23 e33')
eps = sp.Symbol('eps')

def emat(i, j):
    return {(0,0):e11,(1,1):e22,(2,2):e33,
            (0,1):e12,(1,0):e12,(0,2):e13,(2,0):e13,(1,2):e23,(2,1):e23}[(i,j)]

def hij(i, j):
    return a**2*(sp.Integer(1 if i == j else 0) + eps*q*emat(i,j)*C)

def dx(expr, kk):
    Kk = [0, 0, kz][kk]
    e = sp.expand(expr)
    return sp.expand(Kk*(C*sp.diff(e, S) - S*sp.diff(e, C)))

def hinv(i, j):
    d = sp.Integer(1 if i == j else 0)
    e2m = sum(emat(i,k)*emat(k,j) for k in range(3))
    return a**-2*(d - eps*q*emat(i,j)*C + eps**2*q**2*e2m*C**2)

def G0_ij(i, j):
    return sp.Rational(1,2)*sp.diff(hij(i,j), t)

def Gi_0j(i, j):
    return sp.Rational(1,2)*sum(hinv(i,k)*sp.diff(hij(k,j), t) for k in range(3))

def Gi_jk(i, j, kk):
    return sp.Rational(1,2)*sum(hinv(i,l)*(dx(hij(l,kk), j) + dx(hij(j,l), kk) - dx(hij(j,kk), l))
                                for l in range(3))

R00 = -sp.diff(sum(Gi_0j(i,i) for i in range(3)), t) \
      - sum(Gi_0j(i,j)*Gi_0j(j,i) for i in range(3) for j in range(3))

def R_ij(i, j):
    t1 = sp.diff(G0_ij(i,j), t) + sum(dx(Gi_jk(kk,i,j), kk) for kk in range(3))
    t2 = -dx(sum(Gi_jk(kl,i,kl) for kl in range(3)), j)
    t3 = sum(Gi_0j(kk,kk) for kk in range(3))*G0_ij(i,j) \
         + sum(sum(Gi_jk(l,kk,l) for l in range(3))*Gi_jk(kk,i,j) for kk in range(3))
    t4 = 0
    for kk in range(3):
        t4 -= G0_ij(i,kk)*Gi_0j(kk,j)
        t4 -= Gi_0j(kk,i)*G0_ij(j,kk)
        for ll in range(3):
            t4 -= Gi_jk(ll,i,kk)*Gi_jk(kk,j,ll)
    return sp.expand(t1 + t2 + t3 + t4)

Rsc = sp.expand(-R00 + sum(hinv(i,j)*R_ij(i,j) for i in range(3) for j in range(3)))

# flat space, single mode e = diag(1,-1,0), k = (0,0,1)
subs = {a: sp.Integer(1),          # a=1, H=0, Hdot=0
        e11: 1, e22: -1, e33: 0, e12: 0, e13: 0, e23: 0,
        kz: 1, eps: 1}
qd = sp.Derivative(q, t); qdd = sp.Derivative(q, (t,2))
q0v, q1v = 0.01, 0.01
R_expr = sp.simplify(Rsc.subs(subs)).subs({C: 1, S: 0})
R_expr = sp.expand(R_expr.subs({q: q0v + q1v*t, qd: q1v, qdd: 0}))
R_at = float(R_expr.subs(t, 0.0))
print("sympy R at cell (t=0, C=1, S=0), q0=q1=0.01:", R_at)

# ---- numeric side: R at the same cell ----
Rc, sg, L, g, gi = dc.R_num((24, 24, 24, 9), 2*np.pi, 1.0, 0.0, q0v, q1v, 0.0, wrap_t=False)
# cell (t=4th slice? time axis: t = (arange(9)-4)*0.05 -> slice i has t=(i-4)*dtv)
dtv_n = 0.05
for i, tt in enumerate((np.arange(9)-4)*dtv_n):
    if abs(tt) < 1e-12:
        tslice = i
        break
# spatial cell where z = 0 (cos(0)=1): z grid: (arange(24)-12)*dx, dx = 2pi/24
zgrid = (np.arange(24)-12)*(2*np.pi/24)
zc = int(np.argmin(np.abs(zgrid)))
x = (np.arange(24)-12)*(2*np.pi/24)
R_num_cell = Rc[tslice, 12, 12, zc]
# also C=1 cell: z=0 -> gam = q*e -> R should match sympy
print("numeric R at t=0, z=0:", R_num_cell, " (expect", R_at, ")")
print("numeric R at t=0, all z: min/max", Rc[tslice].min(), Rc[tslice].max(),
      "mean", Rc[tslice].mean())