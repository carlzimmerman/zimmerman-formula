#!/usr/bin/env python3
"""Compare as238_derive.Rsc vs pin_R_bug.Rsc at identical points; determine R^(2) kinetic sign."""
import sympy as sp

t = sp.Symbol('t')
a = sp.Function('a')(t)
q = sp.Function('q')(t)
C, S = sp.symbols('C S')
kx, ky, kz = sp.symbols('kx ky kz')
e11, e12, e13, e22, e23, e33 = sp.symbols('e11 e12 e13 e22 e23 e33')
eps = sp.Symbol('eps')

def emat(i, j):
    return {(0,0):e11,(1,1):e22,(2,2):e33,
            (0,1):e12,(1,0):e12,(0,2):e13,(2,0):e13,(1,2):e23,(2,1):e23}[(i,j)]

def hij(i, j):
    return a**2*(sp.Integer(1 if i == j else 0) + eps*q*emat(i,j)*C)

def dx(expr, kk):
    Kk = [kx, ky, kz][kk]
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

# 1) generic k, eps series to eps^2, no TT assumptions yet:
R2_raw = sp.expand(sp.series(sp.expand(Rsc), eps, 0, 3).removeO().coeff(eps, 2))

# 2) e=diag(1,-1,0), k=(0,0,kz): substitute GENERIC kz (no division anywhere)
subs_pol = {e11: 1, e22: -1, e33: 0, e12: 0, e13: 0, e23: 0, kx: 0, ky: 0}
R2 = sp.simplify(R2_raw.subs(subs_pol))
print("R^(2) for e=diag(1,-1,0), k=(0,0,kz):")
print(sp.factor(R2))

# coefficients of qd^2 and kz^2 q^2  (q..qdd->0 check)
qd = sp.Derivative(q, t)
qdd = sp.Derivative(q, (t,2))
E = sp.expand(R2)
coef_qd2 = sp.simplify(E.coeff(qd**2))
E2 = sp.expand(E - coef_qd2*qd**2)
coef_q2 = sp.simplify(E2.coeff(q**2))
coef_qddq = sp.simplify(E2.coeff(qdd).coeff(q)) if False else None
print("coeff of qd^2 in R^(2):", sp.simplify(coef_qd2))
print("coeff of q^2 in R^(2):", sp.factor(sp.simplify(coef_q2)))

# evaluate at a point to compare with the numeric run (a=1, q0=q1=0.01, C=1,S=0)... 
# NOTE: eps-series form; evaluate eps=1, q=q0+q1*t:
val = sp.simplify(R2.subs({a: 1, eps: 1, q: sp.Rational(1,100) + sp.Rational(1,100)*t,
                           qd: sp.Rational(1,100), qdd: 0, kz: 1, C: 1, S: 0}))
val = float(val.subs(t, 0))
print("R^(2) at (a=1,q=0.01,qd=0.01,kz=1,C=1,S=0):", val)
print("NOTE: numeric exact R at the same point: -3.50005e-4")