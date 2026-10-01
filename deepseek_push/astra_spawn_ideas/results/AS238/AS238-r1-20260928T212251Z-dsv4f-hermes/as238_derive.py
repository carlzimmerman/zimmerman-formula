#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS238 (Tier-0b): Derive the tensor dispersion on homogeneous occupied FLRW.

Cell: CA5-GNC-R (FINAL_ACTION.md sha b8c04d4e..., occupied/RESULT.md sha 6091291f...),
physical metric g, flat compact FRW leaf occupied by the five real carrier fields
(background U=Z=0, z=0, t_c=1, gate inactive Y_h=-theta<0, Lambda=0 on the occupied
branch per occupied/RESULT.md "bare Einstein constant is zero").

Background equations (occupied/RESULT.md):  3 M H^2 = T + V + V0,  M Hdot = -T,
M = M_P^2, T = 1/2 sum_A v_A^2, V = V_mix >= 0, V0 > 0  (rho_d = T+V+V0, P_d = T-V-V0).

Method: one TT mode gamma_ij = q(t) e_ij C(x), C=cos(k.x), with the EXACT TT family
(four equations: e_ii=0 and k_i e_ij = 0 for j=1,2,3, solved as a linear system for
(e13, e23, e33, e12) with parameters (e11, e22); valid for generic k, kx,ky,kz != 0).
Every sector of S_GNC is expanded to quadratic order in the amplitude, box-averaged
(C^2->1/2, S^2->1/2, CS->0), integrated by parts in time, collected as A qdot^2 + D q^2.
The mass-type coefficient D must vanish after the occupied Friedmann pair.  The target:
S_T = (M/8) int a^3 [qdot^2 - a^-2 k^2 q^2] (per polarization), phase speed c.

Negative control: diagnostic shear-squared operator (kappa/2) int a^3 sigma_ij sigma^ij,
sigma = trace-free part of the extrinsic curvature (sigma^(1)_ij = (a^2/2) gammadot_ij
for TT); the tensor-speed extraction must detect M/8 -> (M+kappa)/8 (speed^2 = M/(M+kappa))
and the pure-Einstein extraction must FAIL (EOM residual proportional to kappa).
"""
import sympy as sp
import time, sys

t0 = time.time()
M, Lam = sp.symbols('M Lambda')            # M = M_P^2 > 0 ; Lambda bare (0 on occupied)
Tv, Vv, V0 = sp.symbols('T V V0', positive=True)
kap = sp.symbols('kappa', positive=True)
t = sp.Symbol('t')
a = sp.Function('a')(t)
q = sp.Function('q')(t)
C, S = sp.symbols('C S')
kx, ky, kz = sp.symbols('kx ky kz')
e11, e12, e13, e22, e23, e33 = sp.symbols('e11 e12 e13 e22 e23 e33')
eps = sp.Symbol('eps')
k2 = kx**2 + ky**2 + kz**2

# ---- EXACT TT family: solve e_ii=0 and k_i e_ij=0 (all three j) -------------
sol = sp.solve([e11*kx + e12*ky + e13*kz,          # k_i e_i1
                e12*kx + e22*ky + e23*kz,          # k_i e_i2
                e13*kx + e23*ky + e33*kz,          # k_i e_i3
                e11 + e22 + e33],                  # trace
               [e13, e23, e33, e12], dict=True)[0]
tt_subs = {e1: sol[e1] for e1 in [e13, e23, e33, e12]}

# verify all four conditions identically
for expr, name in [(e11*kx + e12*ky + e13*kz, 'k.e row1'),
                   (e12*kx + e22*ky + e23*kz, 'k.e row2'),
                   (e13*kx + e23*ky + e33*kz, 'k.e row3'),
                   (e11 + e22 + e33, 'trace')]:
    print("TT check %s:" % name, sp.simplify(expr.subs(tt_subs)))

e2 = sp.simplify((e11**2 + e22**2 + e33**2 + 2*(e12**2 + e13**2 + e23**2)).subs(tt_subs))
print("e2 = e_ij e_ij (TT):", sp.simplify(e2))

# ---- metric, derivatives, Christoffels (ds^2 = -dt^2 + h_ij dx^i dx^j) ------
def emat(i, j):
    return {(0,0):e11,(1,1):e22,(2,2):e33,
            (0,1):e12,(1,0):e12,(0,2):e13,(2,0):e13,(1,2):e23,(2,1):e23}[(i,j)]

def hij(i, j):
    return a**2*(sp.Integer(1 if i == j else 0) + eps*q*emat(i,j)*C)

def dx(expr, kk):
    """partial_{x^k}: C=cos(k.x), S=sin(k.x) => d_k f = k_k (C dS f - S dC f)"""
    Kk = [kx, ky, kz][kk]
    e = sp.expand(expr)
    return sp.expand(Kk*(C*sp.diff(e, S) - S*sp.diff(e, C)))

def hinv(i, j):
    d = sp.Integer(1 if i == j else 0)
    e2m = sum(emat(i,k)*emat(k,j) for k in range(3))
    return a**-2*(d - eps*q*emat(i,j)*C + eps**2*q**2*e2m*C**2)

def G0_ij(i, j):   # Gamma^0_ij = (1/2) dh_ij/dt
    return sp.Rational(1,2)*sp.diff(hij(i,j), t)

def Gi_0j(i, j):   # Gamma^i_0j = (1/2) h^ik dh_kj/dt
    return sp.Rational(1,2)*sum(hinv(i,k)*sp.diff(hij(k,j), t) for k in range(3))

def Gi_jk(i, j, kk):   # Gamma^i_jk = (1/2) h^il (d_j h_lk + d_k h_jl - d_l h_jk)
    return sp.Rational(1,2)*sum(hinv(i,l)*(dx(hij(l,kk), j) + dx(hij(j,l), kk) - dx(hij(j,kk), l))
                                for l in range(3))

# Ric: R = -R_00 + h^ij R_ij  (g^0i = 0)
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

# measure: sqrt(-det g) = a^3 sqrt(det(I + eps q e C)) = a^3 (1 + d1 + d2 - d1^2/2)
trA = q*C*(e11+e22+e33)
trA2 = q**2*C**2*sum(sum(emat(i,k)*emat(k,i) for k in range(3)) for i in range(3))
d1 = sp.Rational(1,2)*eps*trA
d2 = eps**2*(sp.Rational(1,8)*trA**2 - sp.Rational(1,4)*trA2)
sq = a**3*(1 + d1 + d2 - d1**2/2)

# ---- Lagrangian densities -----------------------------------------------------
L_EH = (M/2)*sq*(Rsc - 2*Lam)
L_car = sq*(Tv - Vv - V0)          # occupied carrier at t_c = 1, z = 0: T - V - V0
L_tot = sp.expand(L_EH + L_car)
Lser = sp.series(L_tot, eps, 0, 3).removeO()
L1 = sp.simplify(Lser.coeff(eps, 1))
L2 = sp.expand(Lser.coeff(eps, 2))

L1 = sp.simplify(L1.subs(tt_subs))
L2 = sp.expand(L2.subs(tt_subs))

# linear piece must vanish identically for TT
lin_c = sp.simplify(L1.subs({C: 1, S: 0}))
lin_s = sp.simplify(L1.subs({C: 0, S: 1}))
print("\nLINEAR PIECE after EXACT TT (C-part, S-part):", lin_c, ",", lin_s)

# box average
L2av = sp.expand(L2.subs({C**2: sp.Rational(1,2), S**2: sp.Rational(1,2),
                          C*S: 0, C: 0, S: 0}))

H_s, Hd_s = sp.symbols('H Hdot')

# ---- coefficients ---------------------------------------------------------------
qd = sp.Derivative(q, t)
qdd = sp.Derivative(q, (t,2))
E = sp.expand(L2av)
c_qddq = sp.simplify(E.coeff(qdd).coeff(q));  E = sp.expand(E - c_qddq*qdd*q)
c_qdq  = sp.simplify(E.coeff(qd).coeff(q));   E = sp.expand(E - c_qdq*qd*q)
c_qd2  = sp.simplify(E.coeff(qd**2));         E = sp.expand(E - c_qd2*qd**2)
c_q2   = sp.simplify(E.coeff(q**2))

# IBP: f qdd q -> -f qd^2 + (1/2) f'' q^2 ;  g qd q -> -(1/2) g' q^2
f, g = c_qddq, c_qdq
f2p = sp.simplify(sp.diff(f, t, 2))
g1p = sp.simplify(sp.diff(g, t))
A = sp.simplify(c_qd2 - f)
D = sp.simplify(c_q2 + f2p/2 - g1p/2)

# substitute adot = a H, addot = a(H^2 + Hdot) AFTER IBP
subs_kin = {sp.diff(a, t): a*H_s, sp.diff(a, t, 2): a*(H_s**2 + Hd_s)}
A = sp.expand(A.subs(subs_kin))
D = sp.expand(D.subs(subs_kin))

print("\n--- extracted coefficients (exact TT, generic k) ---")
An = sp.simplify(A / ((M/8)*a**3))
Dn = sp.simplify(D / ((M/8)*a**3))
print("A / [(M/8) a^3] =", An)
print("D / [(M/8) a^3] =", sp.factor(Dn))
print("e2 =", sp.factor(e2))

# canonical expectation: A = (M/8) a^3 * e2/2 ; D_grad = -(M/8) a^3 (k^2/a^2) (e2/2)
A_canon = (M/8)*a**3*(e2/2)
D_grad = -(M/8)*a**3*(k2/a**2)*(e2/2)
print("\nA / A_canon =", sp.simplify(A/A_canon))
mass = sp.simplify(D - D_grad)
mass_n = sp.simplify(mass/(a**3*(e2/2)))
print("mass / [a^3 e2/2] (pre-Friedmann):", sp.factor(mass_n))

# Friedmann substitution (general Lambda; occupied branch Lambda = 0)
fr = {H_s**2: (M*Lam + Tv + Vv + V0)/(3*M), Hd_s: -Tv/M}
mass_on = sp.simplify(mass_n.subs(fr))
print("mass after Friedmann:", sp.simplify(mass_on))
print("mass after Friedmann, occupied Lambda=0:", sp.simplify(mass_on.subs(Lam, 0)))

# ---- EOM and dispersion ----------------------------------------------------------
A_a = sp.simplify(A/(e2/2))
D_a = sp.simplify(D_grad/(e2/2))
EOM = sp.expand(sp.diff(2*A_a*qd, t) - 2*D_a*q)
EOM = sp.expand(EOM.subs(subs_kin))
print("\nEOM (per polarization):", sp.collect(sp.expand(EOM), [qdd, qd, q]))
cq1 = sp.simplify(EOM.coeff(qdd)); EOMr = sp.expand(EOM - cq1*qdd)
cq2 = sp.simplify(EOMr.coeff(qd));  EOMr = sp.expand(EOMr - cq2*qd)
cq3 = sp.simplify(EOMr.coeff(q));   EOMr = sp.expand(EOMr - cq3*q)
print("coeff qddot / [(M/4) a^3] =", sp.simplify(cq1/((M/4)*a**3)))
print("coeff qdot  / [(M/4) a^3] =", sp.simplify(cq2/((M/4)*a**3)))
print("coeff q     / [(M/4) a^3] =", sp.simplify(cq3/((M/4)*a**3)))
print("residual after extraction:", sp.simplify(EOMr))

# substitution back with the full dispersion relation (friction included)
w = sp.Symbol('w', positive=True)
sym = sp.simplify((cq1*(-w**2) + cq2*(sp.I*w) + cq3)/((M/4)*a**3))
print("frozen-coefficient symbol (q ~ e^{+iwt}):", sp.simplify(sym))
roots = sp.solve(sp.expand(sym), w)
print("dispersion roots:", roots)
back = [sp.simplify(sym.subs(w, r)) for r in roots]
print("substitution-back residual per root:", back)

# ---- negative control: shear-squared diagnostic --------------------------------
# sigma_ij = K_ij - (K/3) h_ij ; K_ij = (1/2) dh_ij/dt (N=1, Ni=0)
# K^(1) = 0 for TT => sigma^(1)_ij = (a^2/2) gammadot_ij ; sigma^2 = (1/4) gammadot^2
A_kin = (M/8)*a**3*(e2/2)
A_shear = sp.simplify(A_kin + (kap/8)*a**3*(e2/2))
print("\n--- shear negative control ---")
print("kinetic clean:", sp.simplify(A_kin), " with shear:", A_shear)
v2 = sp.simplify(A_kin/A_shear)
print("speed^2 ratio:", v2, " (kappa=0 ->", v2.subs(kap, 0), ")")
res_wrong = sp.factor(sp.simplify((-(w**2*(M+kap)/8) + (M/8)*k2/a**2).subs(w**2, k2/a**2)))
print("residual of pure-Einstein w^2 = k^2/a^2 in shear-modified EOM:",
      res_wrong, "  (fires iff kappa != 0)")

print("\nwall time sympy:", round(time.time()-t0, 1), "s")
sys.exit(0)