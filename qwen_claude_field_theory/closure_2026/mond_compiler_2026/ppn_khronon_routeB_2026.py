#!/usr/bin/env python3
r"""
ppn_khronon_routeB_2026.py  --  ROUTE B (COVARIANT KHRONON) 1PN preferred-frame gate.

Independent of any ADM-route script.  Everything below is derived, not assumed.

METHOD
------
1. Khronon:  u_mu = -d_mu T / sqrt(X),  X = -g^{ab} d_a T d_b T,  N = 1/sqrt(X),
   a_mu = u^n nabla_n u_mu.  We VERIFY the dictionary identity a_mu = P_mu^n d_n ln N
   (P = delta + u u) at the order used, so that in unitary gauge T=t the candidate's
   MOND operator chi (D phi)^2 with phi = ln N IS chi * a_mu a^mu.

2. Covariant family (contains the candidate at beta = lam = 0):
      S = (1/16 pi G) Int sqrt(-g) [ R + alpha a_mu a^mu
                                       + beta nabla_mu u_nu nabla^nu u^mu
                                       + lam (nabla_mu u^mu)^2 ]
          - Int rho_c sqrt(-g_00)                      (static dust at rest)
   GR <=> alpha = beta = lam = 0.  The candidate's GR sector K_ij K^ij - K^2 + R3 is
   exactly beta = lam = 0.

3. Background: flat metric + KHRONON BOOSTED with velocity w:  Tbar = t + w.x.
   (exact flat solution: a_mu = 0, nabla u = 0).  Source static and at rest.
   Perturbations Phi, Psi, Z_i, tau; gauge: h_ij = 2 Psi delta_ij and tau = 0
   (xi^i and xi^0, all static).  tau's equation is then redundant -- CHECKED.

4. Field equations (derived, see notes in code):
      -2 G^{(1)00}   + EL_Phi(L_LV) + 16 pi G rho = 0
      -2 sum_i G^{(1)ii} + EL_Psi(L_LV)           = 0
      -2 G^{(1)0j}   + EL_Zj(L_LV)                = 0
      EL_tau(L_LV) = 0                            (redundancy check)

5. PPN readout (Will TEGP 4.46), static source, preferred frame moving at w:
      g_00 = -1 + 2U - (a1 - a2 - a3) w^2 U - a2 w^i w^j U_ij
      g_0i = -(1/2) a1 w_i U + (1/2) a2 w^j U_ij
      g_ij = (1 + 2 gamma U) delta_ij
   Fourier:  U_ij(k) = -2 k_i k_j U/k^2 + delta_ij U.  Hence with Phi := h_00/2,
      Phi/U = 1 - (1/2)(a1 - a3) w^2 + a2 (k.w)^2/k^2
   ==> a2 = coeff of (k.w)^2/k^2 ;  a1 - a3 = -2 * coeff of w^2.
   h_00 and h_ij are INVARIANT under the residual static xi^0 freedom (the only freedom
   that can shuffle weight between a1 and a2 in g_0i), so this readout is gauge-safe.
   g_0i is used only as a cross-check on the invariant combination a1 - a2.
"""
import sympy as sp
import sys
from sympy import Rational as R_

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
COORDS = (t, x1, x2, x3)
XS = (x1, x2, x3)
ep = sp.symbols('varepsilon', positive=True)
G = sp.symbols('G', positive=True)
al, be, lm = sp.symbols('alpha beta lambda_', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
W = [w1, w2, w3]

Phi = sp.Function('Phi')(*XS)
Psi = sp.Function('Psi')(*XS)
Za = sp.Function('Za')(*XS)
Zb = sp.Function('Zb')(*XS)
Zd = sp.Function('Zd')(*XS)
Zc = [Za, Zb, Zd]
tau = sp.Function('tau')(*XS)
rho = sp.Function('rho')(*XS)

FIELDS = [Phi, Psi] + Zc + [tau]


def lin(e):
    """keep O(ep^1) coefficient (i.e. linearise)"""
    return sp.expand(sp.diff(sp.expand(e), ep).subs(ep, 0))


def order0(e):
    return sp.expand(sp.expand(e).subs(ep, 0))


eta = sp.diag(-1, 1, 1, 1)
h = sp.zeros(4, 4)
h[0, 0] = 2*Phi
for i in range(3):
    h[0, i+1] = Zc[i]
    h[i+1, 0] = Zc[i]
    h[i+1, i+1] = 2*Psi

g = eta + ep*h
Hm = eta*h                                   # H^mu_nu = eta^{mu a} h_{a nu}
ginv = eta - ep*Hm*eta + ep**2*(Hm*Hm*eta)   # O(ep^2) inverse


def d(e, mu):
    return sp.diff(e, COORDS[mu])


print("[1] linearised Christoffel / Ricci / Einstein ...", flush=True)
Gam1 = [[[0]*4 for _ in range(4)] for _ in range(4)]
for r in range(4):
    for m in range(4):
        for n in range(m, 4):
            s = 0
            for a in range(4):
                s += eta[r, a]*(d(h[a, m], n) + d(h[a, n], m) - d(h[m, n], a))
            s = sp.expand(s/2)
            Gam1[r][m][n] = s
            Gam1[r][n][m] = s

Ric1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(m, 4):
        s = 0
        for r in range(4):
            s += d(Gam1[r][m][n], r) - d(Gam1[r][m][r], n)
        s = sp.expand(s)                      # GG terms are O(ep^2), dropped
        Ric1[m, n] = s
        Ric1[n, m] = s

Rs1 = sp.expand(sum(eta[m, n]*Ric1[m, n] for m in range(4) for n in range(4)))
Ein1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ein1[m, n] = sp.expand(Ric1[m, n] - R_(1, 2)*eta[m, n]*Rs1)
# raise indices with eta (background G vanishes)
Einup = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Einup[m, n] = sp.expand(sum(eta[m, a]*eta[n, b]*Ein1[a, b]
                                    for a in range(4) for b in range(4)))

print("[2] khronon sector ...", flush=True)
ginv1 = eta - ep*Hm*eta                       # inverse metric to O(ep) -- all we need
T = t + sum(W[i]*XS[i] for i in range(3)) + ep*tau
dT = [d(T, m) for m in range(4)]

Xk = sp.expand(sum(-ginv1[m, n]*dT[m]*dT[n] for m in range(4) for n in range(4)))
X0 = sp.simplify(order0(Xk))
X1 = lin(Xk)
invsq = 1/sp.sqrt(X0) - ep*X1/(2*X0**R_(3, 2))
u_lo = sp.Matrix([sp.expand(-dT[m]*invsq) for m in range(4)])
u0 = u_lo.applyfunc(order0)
u1 = u_lo.applyfunc(lin)

# nabla_mu u_nu at O(ep) : d_mu u^{(1)}_nu - Gamma^{(1)r}_{mu nu} u^{(0)}_r
nab1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        nab1[m, n] = sp.expand(d(u1[n], m) - sum(Gam1[r][m][n]*u0[r] for r in range(4)))
# background nabla u vanishes because u0 is constant and Gamma^{(0)}=0
assert all(sp.simplify(d(u0[n], m)) == 0 for m in range(4) for n in range(4))

uup0 = sp.Matrix([sp.expand(sum(eta[m, n]*u0[n] for n in range(4))) for m in range(4)])
a1v = sp.Matrix([sp.expand(sum(uup0[n]*nab1[n, m] for n in range(4))) for m in range(4)])
print("    u.u check:", sp.simplify(sum(eta[m, n]*u0[m]*u0[n]
                                        for m in range(4) for n in range(4))), flush=True)

# --- verify the khronometric dictionary identity a_mu = P_mu^nu d_nu ln N at O(ep) ---
sN = sp.expand(-R_(1, 2)*(X1/X0))            # O(ep) part of ln N = -(1/2) ln X
Pm = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Pm[m, n] = (1 if m == n else 0) + u0[m]*uup0[n]
ident = [sp.simplify(sp.expand(sum(Pm[m, n]*d(sN, n) for n in range(4)) - a1v[m]))
         for m in range(4)]
print("    identity a_mu = P_mu^n d_n ln N  residuals:", ident, flush=True)
assert all(v == 0 for v in ident)

A_q = sp.expand(sum(eta[m, n]*a1v[m]*a1v[n] for m in range(4) for n in range(4)))
B_q = sp.expand(sum(eta[m, p]*eta[n, q]*nab1[m, n]*nab1[q, p]
                    for m in range(4) for n in range(4)
                    for p in range(4) for q in range(4)))
Th_q = sp.expand(sum(eta[m, n]*nab1[m, n] for m in range(4) for n in range(4)))
L_LV = sp.expand(al*A_q + be*B_q + lm*Th_q**2)


def euler(L, f):
    L = sp.expand(L)
    e = sp.diff(L, f)
    for m in range(1, 4):
        e -= sp.diff(sp.diff(L, sp.diff(f, COORDS[m])), COORDS[m])
    for m in range(1, 4):
        for n in range(m, 4):
            e += sp.diff(sp.diff(L, sp.diff(f, COORDS[m], COORDS[n])),
                         COORDS[m], COORDS[n])
    return sp.expand(e)


print("[3] field equations ...", flush=True)
EQ = {}
EQ['Phi'] = sp.expand(-2*Einup[0, 0] + euler(L_LV, Phi) + 16*sp.pi*G*rho)
EQ['Psi'] = sp.expand(-2*sum(Einup[i, i] for i in (1, 2, 3)) + euler(L_LV, Psi))
for j in range(3):
    EQ['Z%d' % j] = sp.expand(-2*Einup[0, j+1] + euler(L_LV, Zc[j]))
EQ['tau'] = sp.expand(euler(L_LV, tau))

print("[4] Fourier reduction ...", flush=True)
k1, k2, k3 = sp.symbols('k1 k2 k3', real=True)
K = [k1, k2, k3]
E = sp.exp(sp.I*(k1*x1 + k2*x2 + k3*x3))
Ph, Ps, Z1h, Z2h, Z3h, Th, Rh = sp.symbols('Phih Psih Z1h Z2h Z3h tauh rhoh')
SUB = {Phi: Ph*E, Psi: Ps*E, Za: Z1h*E, Zb: Z2h*E, Zd: Z3h*E, tau: Th*E, rho: Rh*E}

FEQ = {}
for key, e in EQ.items():
    ee = sp.expand(e.subs(SUB).doit())
    ee = sp.expand(ee.subs(E, 1))
    # remove any residual exponentials (all terms carry exactly one factor E)
    ee = sp.expand(sp.powsimp(ee))
    ee = ee.replace(sp.exp, lambda a: 1)
    FEQ[key] = sp.expand(ee)

import pickle
import os
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, '_routeB_feq.pkl'), 'wb') as fh:
    pickle.dump({'FEQ': {k: sp.srepr(v) for k, v in FEQ.items()}}, fh)
print("    saved Fourier equations", flush=True)
for kk in FEQ:
    print("   ", kk, ":", sp.count_ops(FEQ[kk]), "ops", flush=True)
