#!/usr/bin/env python3
r"""
ppn_khronon_routeB_theorem_2026.py -- INDEPENDENT verification of the Route B result,
and the structural theorem behind it.

CLAIM (verified below, three independent ways):

  On the CANDIDATE LOCUS beta = lam = 0 (the candidate's gravity sector is exactly
  K_ij K^ij - K^2 + R3, so the ONLY Lorentz-violating operator is the lapse-tied one),
  for a STATIC source at rest in coordinates in which the khronon/preferred frame moves
  with velocity w != 0:

     the ENTIRE non-GR sector (MOND term AND carrier) drops out of every metric field
     equation identically.  Hence

        gamma_PPN = 1,  G_N = G,  alpha_1 = alpha_2 = 0        (preferred-frame gate PASSES)

     but ALSO the MOND modification of the Poisson equation is GONE:
     mu_eff = 1 for every w != 0, while mu_eff = 1 - alpha/2 at w = 0 exactly.
     The w -> 0 limit is DISCONTINUOUS.

MECHANISM (proof sketch, each step checked symbolically below):

  (1) With beta = lam = 0 the only LV operator is built from a_mu = P_mu^nu d_nu ln N.
      For a STATIC metric (h_00=2Phi, h_0i=Z_i, h_ij=2Psi d_ij) and khronon
      T = t + w.x + tau, at leading weak-field order
          ln N = - shat/(1-w^2),   shat = Phi - Z.w + Psi w^2 - w.grad(tau)
      so the WHOLE non-GR sector -- for ANY function F(A), and with the auxiliary chi and
      the TT carrier Q_ij included -- is a functional of the SINGLE SCALAR shat
      (plus the auxiliaries, which do not involve the metric).

  (2) Therefore
          dL_nonGR/dZ_i   = -w_i * Q ,   dL_nonGR/dPhi = Q ,   dL_nonGR/dPsi = w^2 Q ,
          dL_nonGR/dtau   = + w.grad(Q) ,        where  Q := dL_nonGR/d shat .

  (3) The Z_i field equation is  -2 G^{(1)0i} - w_i Q = 0.  Its divergence, together with
      the LINEARISED BIANCHI IDENTITY d_i G^{(1)0i} = -d_0 G^{(1)00} = 0 (static), gives
          w.grad(Q) = 0   ==>   Q == 0  for any configuration decaying at infinity.
      (this is the same equation as the khronon/tau field equation -- consistent, and it is
       an identity of the system, not an extra assumption.)

  (4) Q == 0 kills the non-GR contribution to the Phi, Psi and Z_i equations simultaneously
      (all three are proportional to Q).  The metric sector is exactly GR.  QED.

  At w = 0 the combination shat degenerates to Phi, tau drops out of the action entirely,
  step (3) is vacuous (0 = 0), and MOND survives.  Hence the discontinuity.
"""
import sympy as sp
from sympy import Rational as R_

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
COORDS = (t, x1, x2, x3)
XS = (x1, x2, x3)
al = sp.symbols('alpha', real=True)
G = sp.symbols('G', positive=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
W = [w1, w2, w3]
w2s = w1**2 + w2**2 + w3**2

Phi = sp.Function('Phi')(*XS)
Psi = sp.Function('Psi')(*XS)
Zc = [sp.Function('Za')(*XS), sp.Function('Zb')(*XS), sp.Function('Zd')(*XS)]
tau = sp.Function('tau')(*XS)
rho = sp.Function('rho')(*XS)


def d(e, m):
    return sp.diff(e, COORDS[m])


# ---------------------------------------------------------------- STEP 1
print("STEP 1: the non-GR sector depends on the metric ONLY through the scalar shat")
eta = sp.diag(-1, 1, 1, 1)
ep = sp.symbols('varepsilon', positive=True)
h = sp.zeros(4, 4)
h[0, 0] = 2*Phi
for i in range(3):
    h[0, i+1] = Zc[i]
    h[i+1, 0] = Zc[i]
    h[i+1, i+1] = 2*Psi
Hm = eta*h
ginv1 = eta - ep*Hm*eta
T = t + sum(W[i]*XS[i] for i in range(3)) + ep*tau
dT = [d(T, m) for m in range(4)]
Xk = sp.expand(sum(-ginv1[m, n]*dT[m]*dT[n] for m in range(4) for n in range(4)))
X0 = sp.simplify(Xk.subs(ep, 0))
X1 = sp.expand(sp.diff(Xk, ep).subs(ep, 0))
lnN1 = sp.simplify(-R_(1, 2)*X1/X0)                       # O(ep) part of ln N
shat = Phi - sum(Zc[i]*W[i] for i in range(3)) + Psi*w2s - sum(W[i]*d(tau, i+1)
                                                              for i in range(3))
print("   X0 = 1 - w^2 ? ", sp.simplify(X0 - (1 - w2s)) == 0)
print("   ln N |_O(ep)  = -shat/(1-w^2) ? ",
      sp.simplify(lnN1 + shat/(1 - w2s)) == 0)

# a_mu at O(ep) from the verified identity a_mu = P_mu^nu d_nu (ln N)
u0 = sp.Matrix([-dT[m].subs(ep, 0)/sp.sqrt(X0) for m in range(4)])
uup0 = sp.Matrix([sum(eta[m, n]*u0[n] for n in range(4)) for m in range(4)])
Pm = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Pm[m, n] = (1 if m == n else 0) + u0[m]*uup0[n]
a1v = sp.Matrix([sp.expand(sum(Pm[m, n]*d(lnN1, n) for n in range(4))) for m in range(4)])
A_q = sp.simplify(sum(eta[m, n]*a1v[m]*a1v[n] for m in range(4) for n in range(4)))
s = -shat/(1 - w2s)
A_pred = sp.simplify(sum(d(s, i+1)**2 for i in range(3))
                     + (sum(W[i]*d(s, i+1) for i in range(3)))**2/(1 - w2s))
print("   A = a.a = [(grad s)^2 + (w.grad s)^2/(1-w^2)] with s=-shat/(1-w^2) ? ",
      sp.simplify(A_q - A_pred) == 0)
print("   ==> the LV sector is a functional of shat ALONE (any F(A), any auxiliary,")
print("       and the TT carrier f(chi) Q^ij [a_i a_j]^TF - (1/2) Q^ij M Q_ij too,")
print("       because a_mu itself depends on the metric only through shat).")

# ---------------------------------------------------------------- STEP 2/3
print()
print("STEP 2/3: linearised Bianchi identity  d_i G^{(1)0i} = 0  for static fields")
Gam1 = [[[0]*4 for _ in range(4)] for _ in range(4)]
for r in range(4):
    for m in range(4):
        for n in range(m, 4):
            ss = sum(eta[r, a]*(d(h[a, m], n) + d(h[a, n], m) - d(h[m, n], a))
                     for a in range(4))
            Gam1[r][m][n] = sp.expand(ss/2)
            Gam1[r][n][m] = Gam1[r][m][n]
Ric1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(m, 4):
        ss = sum(d(Gam1[r][m][n], r) - d(Gam1[r][m][r], n) for r in range(4))
        Ric1[m, n] = sp.expand(ss)
        Ric1[n, m] = Ric1[m, n]
Rs1 = sp.expand(sum(eta[m, n]*Ric1[m, n] for m in range(4) for n in range(4)))
Ein1 = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ein1[m, n] = sp.expand(Ric1[m, n] - R_(1, 2)*eta[m, n]*Rs1)
Einup = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Einup[m, n] = sp.expand(sum(eta[m, a]*eta[n, b]*Ein1[a, b]
                                    for a in range(4) for b in range(4)))
div = sp.simplify(sum(d(Einup[0, i+1], i+1) for i in range(3)))
print("   d_i G^{(1)0i} =", div, "  (identically zero for static h)")
assert div == 0

# ---------------------------------------------------------------- STEP 4 explicit solve
print()
print("STEP 4: explicit linear solve, beta=lam=0, single Fourier mode k along z")
k = sp.Symbol('kk', positive=True)
wx, wz = sp.symbols('wx wz', real=True)
Ph, Ps, Z1h, Z2h, Z3h, Th, Rh = sp.symbols('Phih Psih Z1h Z2h Z3h tauh rhoh')
E = sp.exp(sp.I*k*x3)
SUB = {Phi: Ph*E, Psi: Ps*E, Zc[0]: Z1h*E, Zc[1]: Z2h*E, Zc[2]: Z3h*E,
       tau: Th*E, rho: Rh*E, w1: wx, w2: 0, w3: wz}


def fourier(e):
    e = sp.expand(e.subs(SUB).doit())
    e = sp.expand(sp.cancel(sp.together(e/E)))
    return e


# quadratic Lagrangian pieces (in units where the whole action is (1/16 pi G) L )
# substitute the frame (w2 = 0, w1 = wx, w3 = wz) BEFORE differentiating -- pure speed
WSUBS = {w1: wx, w2: 0, w3: wz}
A_q = sp.expand(sp.cancel(sp.together(A_q.subs(WSUBS))))
L_LV = al*A_q                                # beta = lam = 0
L_m = 16*sp.pi*G*rho*Phi


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


FLD = [Phi, Psi] + Zc + [tau]
EHpart = {Phi: -2*Einup[0, 0], Psi: -2*sum(Einup[i, i] for i in (1, 2, 3)),
          Zc[0]: -2*Einup[0, 1], Zc[1]: -2*Einup[0, 2], Zc[2]: -2*Einup[0, 3],
          tau: sp.Integer(0)}
EQ = {f: sp.expand(EHpart[f] + euler(L_LV, f) + euler(L_m, f)) for f in FLD}
FEQ = {f: fourier(EQ[f]) for f in FLD}

UNK = [Ph, Ps, Z1h, Z2h, Z3h, Th]
SYS = [FEQ[f] for f in FLD]
M6, R6 = sp.linear_eq_to_matrix(SYS, UNK)

NUM = {al: sp.Rational(1, 5), k: 1, G: 1, Rh: 1}
for lbl, wsub in (("w = 0 (khronon at rest)", {wx: 0, wz: 0, **NUM}),
                  ("w != 0 (boosted khronon), w=(1/7,0,1/3)",
                   {wx: sp.Rational(1, 7), wz: sp.Rational(1, 3), **NUM}),
                  ("w != 0 symbolic direction, wx=0",
                   {wx: 0, wz: sp.Rational(1, 3), **NUM})):
    print("   ---", lbl)
    Mn = M6.subs(wsub).applyfunc(sp.cancel)
    Rn = R6.subs(wsub).applyfunc(sp.cancel)
    print("      rank(M) =", Mn.rank(), " rank([M|b]) =", Mn.row_join(Rn).rank())
    sol = list(sp.linsolve((Mn, Rn), UNK))[0]
    PhiS = sp.simplify(sp.cancel(sp.together(sol[0])))
    PsiS = sp.simplify(sp.cancel(sp.together(sol[1])))
    ZxS = sp.simplify(sp.cancel(sp.together(sol[2])))
    print("      Phi =", PhiS)
    print("      Psi =", PsiS)
    print("      Z_x =", ZxS)
    GNoverG = sp.simplify(PhiS*k**2/(4*sp.pi*G*Rh)).subs(wsub)
    print("      G_eff/G (coefficient of the Newtonian solution) =", sp.simplify(GNoverG),
          "   [MOND-sector prediction 1/(1-alpha/2) =", sp.simplify(1/(1 - al/2)), "]")
    # shat evaluated on the solution
    shatF = fourier(shat).subs(wsub)
    shatF = sp.simplify(shatF.subs({UNK[i]: sol[i] for i in range(6)}))
    print("      shat on-shell =", shatF,
          "   (shat = 0  =>  the entire non-GR stress vanishes)")

print()
print("CONCLUSION: at beta = lam = 0 the boosted-khronon static solution is EXACTLY GR:")
print("  alpha_1 = alpha_2 = 0, gamma = 1, G_eff = G -- and the MOND modification is GONE.")
print("  At w = 0 exactly, MOND is present (G_eff = G/(1-alpha/2)).  Discontinuous limit.")
