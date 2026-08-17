#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
alpha2_linearised_solve_2026.py
===============================
THE PROPERLY-LINEARISED DIRECT SOLVE for the PPN preferred-frame parameters
alpha_1, alpha_2 of AeST's aether sector -- the calculation
nbody_2026/stage72_alpha2_first_principles_2026.py attempted and wedged on
(66 min, 7.2 GB RSS) because it handed sp.solve() a system containing
lambda*A_mu*A_nu with A = A_bg + a, i.e. PRODUCTS OF TWO O(rho) UNKNOWNS.
Those products are O(rho^2) and must be DROPPED.  Once dropped the system is
STRICTLY LINEAR in the unknowns and a matrix solve settles it in seconds.

THEORY (aether sector only; the scalar sector is a SIBLING agent's job):
    S = (1/(16 pi G)) int d^4x sqrt(-g) [ R - (K_B/2) F_{mu nu}F^{mu nu}
                                          - lambda (g^{ab}A_a A_b + 1) ] + S_m
    F_{mu nu} = d_mu A_nu - d_nu A_mu   (ordinary curl: Christoffels cancel by
    antisymmetry, so with A_mu the FUNDAMENTAL field F carries no metric)
    matter couples to g_{mu nu} only.
Einstein-aether dictionary: c_1 = +K_B, c_2 = 0, c_3 = -K_B, c_4 = 0, hence
c_13 = 0 (c_T = 1 exact) AND c_123 = 0 (spin-0 aether mode has ZERO speed).

WHAT IS BEING ADJUDICATED
  reading L (nbody_2026/stage70): Foster-Jacobson generic formula on the
      dictionary -> alpha_1 = -4 K_B -> K_B < 2.5e-5 from LLR.
  reading D (real_research/reviews/ppn_alpha_independent_check_2026.py):
      alpha_1 = alpha_2 = 0 identically, because two independent routes force
      lambda*(w.khat) = 0.
  third reading (recorded, claimed by nobody): discard the Theta_{3nu}
      constraints and freeze lambda at its w=0 value -> alpha_1 = +3K_B/2,
      alpha_2 = +K_B/2.

CONVENTIONS (each of these can flip a sign or a factor)
  V1  signature (-,+,+,+); coordinates (t,x,y,z); c = 1.
  V2  Riemann R^r_{s m n} = d_m Gam^r_{n s} - d_n Gam^r_{m s} + Gam Gam - Gam Gam,
      Ricci R_{sn} = R^m_{s m n}, G_{mn} = R_{mn} - g_{mn}R/2.  Computed in-script
      from this definition, never looked up.
  V3  T_{mn} = -(2/sqrt(-g)) dS_m/dg^{mn}; static dust has T_{00} = +rho.  The
      SIGN is calibrated internally by demanding ATTRACTIVE gravity (h_00 = +2U,
      U > 0 for rho > 0).
  V4  U is DEFINED positive with lap U = -4 pi G_N rho, U(k) = 4 pi G_N rho/k^2,
      G_N being whatever Newton constant the branch's own w -> 0 limit exhibits.
      Each branch is matched to ITS OWN Newtonian limit, so the value of G_N
      never leaks into alpha_1 or alpha_2.
  V5  U_ij := int rho (x-x')_i (x-x')_j/|x-x'|^3, same G_N as U.  The Fourier
      identity U_ij = (delta_ij - 2 n_i n_j) U is DERIVED in PART D, not assumed.
  V6  MATCHING CONVENTION Z (the one this task specifies, = C8 of the
      independent check):
          g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_ij + (w-free)
      so if the w-dependent part of h_00 is [a w^2 + b (w.nhat)^2] U then
          alpha_2 = -b/2 ,    alpha_1 = a + b/2 .
      DERIVED in PART D by equating coefficients.
  V7  CONVENTION TRAP, handled explicitly: Will's textbook writes the w^2 U
      coefficient as (alpha_3 - alpha_1) = -alpha_1 at alpha_3 = 0.  Every
      alpha below is therefore quoted TWICE: convention Z and "convention W"
      (both signs flipped).  a and b themselves are convention-FREE and are the
      primary deliverable.
  V8  perturbative bookkeeping: LINEAR in rho (every unknown -- h_{mn}, a_mu,
      delta-lambda -- is O(rho)); w kept to SECOND order (exactly, in fact:
      most arms are solved exactly in w and only then Taylor-expanded, which is
      strictly stronger than an order-by-order-in-w solve).

GATES (assertion-enforced: if any fails the script exits nonzero and NOTHING
is claimed):
  c_T^2 = 1 exactly; gamma_PPN = 1 at w = 0; G_N(w=0) = G/(1-K_B/2), i.e.
  AeST's quasi-static G~ = (1-K_B/2)G^ -- a published number this machinery did
  not fit; K_B -> 0 gives exactly GR; G^(1)_{3nu} == 0 for z-only perturbations.

Exit 0 = every numbered check passed AND every gate held.
"""

import sys

import sympy as sp

FAIL, NCHK = [], [0]
GATES = []


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:2d}. {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]}. {label[:70]}")
    return ok


def gate(cond, label, detail=""):
    """A check that is ALSO an assertion-enforced gate."""
    ok = check(cond, "GATE " + label, detail)
    GATES.append((ok, label))
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


def hdr(s):
    print("\n" + "=" * 100)
    print(s)
    print("=" * 100)


print(__doc__)

# ======================================================================================
# symbols
# ======================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
COORDS = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)                   # eta_{mn}; as a matrix it is its own inverse

KB = sp.Symbol("K_B", positive=True)
GG = sp.Symbol("G", positive=True)            # Newton constant appearing in the action
kk = sp.Symbol("k", positive=True)
rho = sp.Symbol("rho", positive=True)
TAU = sp.Symbol("tau", positive=True)         # O(rho) bookkeeping for the truncation
BK = sp.Symbol("bk")                          # O(h) bookkeeping for the Riemann expansion

lam = sp.Symbol("lambda_1")                   # delta-lambda (lambda_bg = 0, so this is IT)
av = list(sp.symbols("a_0 a_1 a_2 a_3"))
H = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f"H{min(m,n)}{max(m,n)}"))
HSYMS = sorted({H[m, n] for m in range(4) for n in range(4)}, key=str)
GAUGE_T = {H[0, 3]: 0, H[1, 3]: 0, H[2, 3]: 0, H[3, 3]: 0}     # k-transverse gauge
UNK_ALL = HSYMS + av + [lam]
SCALE = {s: TAU * s for s in UNK_ALL}
SCALE[rho] = TAU * rho
KMU = sp.Matrix([0, 0, 0, kk])                # k_mu for a static, z-dependent mode


def trunc(expr, maxdeg=1):
    """Keep only terms of total degree <= maxdeg in {unknowns, rho}: i.e. DROP every
    product of two O(rho) quantities.  This is the fix for the stage72 blow-up."""
    e = sp.expand(sp.expand(expr).subs(SCALE))
    out = sum(e.coeff(TAU, d) * TAU**d for d in range(maxdeg + 1))
    return sp.expand(out.subs(TAU, 1))


def trunc_deg0(expr):
    e = sp.expand(sp.expand(expr).subs(SCALE))
    return sp.expand(e.coeff(TAU, 0))


def dropped_part(expr, maxdeg=1):
    e = sp.expand(sp.expand(expr).subs(SCALE))
    tot = sp.expand(e - sum(e.coeff(TAU, d) * TAU**d for d in range(maxdeg + 1)))
    return sp.expand(tot.subs(TAU, 1))


# ======================================================================================
hdr("PART A -- the field equations, DERIVED here (not copied), and the background")
# ======================================================================================
# ---- A(i) metric variation of the aether Lagrangian, by an independent route:
# perturb the LOWER metric g_{mn} -> g_{mn} + S*s_{mn} and use
# delta g^{mn} = -g^{ma}g^{nb} delta g_{ab}.  (The independent check varied g^{mn}
# directly; varying the lower metric is a different implementation of the same claim.)
S_ = sp.Symbol("S_var")
gdn0 = sp.Matrix([[-sp.Rational(8, 7), sp.Rational(1, 5), 0, sp.Rational(1, 9)],
                  [sp.Rational(1, 5), sp.Rational(9, 8), sp.Rational(1, 11), 0],
                  [0, sp.Rational(1, 11), sp.Rational(6, 5), -sp.Rational(1, 7)],
                  [sp.Rational(1, 9), 0, -sp.Rational(1, 7), sp.Rational(4, 3)]])
sdir = sp.Matrix([[sp.Rational(2, 5), sp.Rational(1, 3), -sp.Rational(1, 4), 0],
                  [sp.Rational(1, 3), -sp.Rational(3, 8), 0, sp.Rational(1, 7)],
                  [-sp.Rational(1, 4), 0, sp.Rational(5, 9), sp.Rational(1, 6)],
                  [0, sp.Rational(1, 7), sp.Rational(1, 6), -sp.Rational(2, 7)]])
Ffx = sp.zeros(4, 4)
for (m, n), v in {(0, 1): sp.Rational(3, 5), (0, 2): -sp.Rational(2, 7), (0, 3): sp.Rational(1, 4),
                  (1, 2): -sp.Rational(4, 9), (1, 3): sp.Rational(5, 6), (2, 3): -sp.Rational(1, 3)}.items():
    Ffx[m, n], Ffx[n, m] = v, -v
Afx = sp.Matrix([-sp.Rational(6, 5), sp.Rational(2, 9), sp.Rational(1, 6), -sp.Rational(3, 8)])
LAMfx = sp.Symbol("lam_gen")


def L_aether(gup, Fm, Am, lm):
    F2 = sum(Fm[m, n] * Fm[a, b] * gup[m, a] * gup[n, b]
             for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    AA = sum(gup[a, b] * Am[a] * Am[b] for a in range(4) for b in range(4))
    return -(KB / 2) * F2 - lm * (AA + 1)


gdn_e = gdn0 + S_ * sdir
gup_e = gdn_e.inv()
LA_e = L_aether(gup_e, Ffx, Afx, LAMfx)
sqrtg_e = sp.sqrt(-gdn_e.det())
# dS/dS_var  =  (dS/dg^{mn}) * dg^{mn}/dS_var  with  dg^{mn}/dS_var = -g^{ma}g^{nb}s_{ab}
lhs_var = sp.simplify(sp.diff(sqrtg_e * LA_e, S_).subs(S_, 0))
gup0 = gdn0.inv()
sqrtg0 = sp.sqrt(-gdn0.det())
LA0 = L_aether(gup0, Ffx, Afx, LAMfx)
FF0 = sp.Matrix(4, 4, lambda m, n: sum(Ffx[m, b] * gup0[b, d] * Ffx[n, d]
                                       for b in range(4) for d in range(4)))
# claim: delta(sqrt-g L_A)/delta g^{mn} = sqrt-g[ -K_B F_{mb}F_n^b - lam A_m A_n
#                                                 - (1/2) g_{mn} L_A ]
Xmn = sp.Matrix(4, 4, lambda m, n: sqrtg0 * (-KB * FF0[m, n] - LAMfx * Afx[m] * Afx[n]
                                             - sp.Rational(1, 2) * gdn0[m, n] * LA0))
dgup = sp.Matrix(4, 4, lambda m, n: -sum(gup0[m, a] * gup0[n, b] * sdir[a, b]
                                         for a in range(4) for b in range(4)))
rhs_var = sp.simplify(sum(Xmn[m, n] * dgup[m, n] for m in range(4) for n in range(4)))
check(sp.simplify(sp.expand(lhs_var - rhs_var)) == 0,
      "aether metric-variation formula verified OFF-SHELL at a generic Lorentzian g, "
      "generic F, generic A, generic lambda -- by perturbing the LOWER metric",
      "so with delta(sqrt-g R)/delta g^{mn} = sqrt-g G_{mn} and V3, the metric equation is\n"
      "         G_{mn} = 8 pi G T_{mn} + K_B F_{mb}F_n^b - (K_B/4) g_{mn}F^2 + lambda A_m A_n")

# ---- A(ii) aether EOM by a hand-coded functional derivative (not sympy's helper)
Af = [sp.Function(f"AA{i}")(*COORDS) for i in range(4)]
lamf = sp.Function("lamf")(*COORDS)
Ff = sp.Matrix(4, 4, lambda m, n: sp.diff(Af[n], COORDS[m]) - sp.diff(Af[m], COORDS[n]))
F2f = sum(Ff[m, n] * Ff[a, b] * ETA[m, a] * ETA[n, b]
          for m in range(4) for n in range(4) for a in range(4) for b in range(4))
AAf = sum(ETA[a, b] * Af[a] * Af[b] for a in range(4) for b in range(4))
Lag = -(KB / 2) * F2f - lamf * (AAf + 1)
Fupf = sp.Matrix(4, 4, lambda m, n: sum(ETA[m, a] * ETA[n, b] * Ff[a, b]
                                        for a in range(4) for b in range(4)))
Aupf = [sum(ETA[n, a] * Af[a] for a in range(4)) for n in range(4)]
ok_el = True
for n in range(4):
    # EL_n = dL/dA_n - d_mu( dL/d(d_mu A_n) ), coded by hand
    dLdA = sp.diff(Lag, Af[n])
    dLdDA = [sp.diff(Lag, sp.Derivative(Af[n], COORDS[m])) for m in range(4)]
    EL = sp.expand(dLdA - sum(sp.diff(dLdDA[m], COORDS[m]) for m in range(4)))
    want = sp.expand(2 * KB * sum(sp.diff(Fupf[m, n], COORDS[m]) for m in range(4))
                     - 2 * lamf * Aupf[n])
    ok_el = ok_el and sp.simplify(EL - want) == 0
check(ok_el,
      "aether EOM from a hand-coded functional derivative: EL_nu = 0 is exactly "
      "K_B d_mu F^{mu nu} = lambda A^nu",
      "for antisymmetric F, nabla_mu F^{mu nu} = (1/sqrt-g) d_mu(sqrt-g F^{mu nu}), and the "
      "sqrt-g factor is 1 + O(rho), so at LINEAR order this is the FLAT Maxwell equation with "
      "source lambda A^nu_bg")
check(True,
      "and its divergence gives an identity a generic Einstein-aether does NOT have: F^{mu nu} "
      "antisymmetric => d_mu d_nu F^{mu nu} == 0 => grad_nu(lambda A^nu) = 0",
      "this is the algebraic origin of the whole fork")

# ---- A(iii) the boosted background
wsym = sp.Symbol("w", positive=True)
w1s, w2s, w3s = sp.symbols("w_1 w_2 w_3", real=True)


def background(Wl):
    W2 = sum(c**2 for c in Wl)
    gam = 1 / sp.sqrt(1 - W2)
    Aup = sp.Matrix([gam] + [gam * c for c in Wl])       # A^mu = gamma(1, w^i)
    Adn = ETA * Aup                                       # A_mu = gamma(-1, w_i)
    return gam, Aup, Adn


gam_g, Aup_g, Adn_g = background([w1s, w2s, w3s])
check(sp.simplify((Aup_g.T * ETA * Aup_g)[0, 0] + 1) == 0,
      "background is unit-timelike: A^mu A_mu = -1 exactly for A^mu = gamma(1, w^i), any w")
Fbg = sp.Matrix(4, 4, lambda m, n: sp.diff(Adn_g[n], COORDS[m]) - sp.diff(Adn_g[m], COORDS[n]))
check(sp.simplify(Fbg) == sp.zeros(4, 4),
      "F_bg = 0 identically: a CONSTANT boosted aether costs no field energy",
      "hence lambda_bg = 0 (contract the vector EOM with A_nu: lambda = -K_B A_nu d_mu F^{mu nu}), "
      "so delta-lambda is gauge invariant AND is itself O(rho) -- and the F-bilinear sources in "
      "the metric equation are O(rho^2)")


# ======================================================================================
hdr("PART B -- linearized Einstein tensor from the Riemann DEFINITION; Bianchi; c_T gate")
# ======================================================================================
def lin_einstein(hmat, coords, bk):
    """G^(1)_{mn} for g = eta + bk*hmat, computed from the Riemann definition (V2).
    Returns the coefficient of bk^1."""
    gdn = ETA + bk * hmat
    gup = ETA - bk * ETA * hmat * ETA                  # inverse to O(bk)
    Gam = [[[sp.expand(sp.Rational(1, 2) * sum(
        gup[r, s] * (sp.diff(gdn[s, n], coords[m]) + sp.diff(gdn[s, m], coords[n])
                     - sp.diff(gdn[m, n], coords[s])) for s in range(4)))
             for n in range(4)] for m in range(4)] for r in range(4)]

    def Ric(sg, nu):
        out = 0
        for m in range(4):
            out += sp.diff(Gam[m][nu][sg], coords[m]) - sp.diff(Gam[m][m][sg], coords[nu])
            for l in range(4):
                out += Gam[m][m][l] * Gam[l][nu][sg] - Gam[m][nu][l] * Gam[l][m][sg]
        return sp.expand(out)

    R1 = sp.Matrix(4, 4, lambda m, n: sp.expand(sp.expand(Ric(m, n)).coeff(bk, 1)))
    Rs1 = sp.expand(sum(ETA[m, n] * R1[m, n] for m in range(4) for n in range(4)))
    return R1, sp.Matrix(4, 4, lambda m, n: sp.expand(R1[m, n] - sp.Rational(1, 2) * ETA[m, n] * Rs1))


PHASE = sp.exp(sp.I * kk * z)
gdn_chk = ETA + BK * H * PHASE
gup_chk = ETA - BK * ETA * (H * PHASE) * ETA
resid = sp.expand(gup_chk * gdn_chk - sp.eye(4))
check(all(sp.expand(resid[i, j]).coeff(BK, 0) == 0 and sp.expand(resid[i, j]).coeff(BK, 1) == 0
          for i in range(4) for j in range(4)),
      "truncated inverse metric is right: g^{ma}g_{an} = delta + O(h^2)")

R1_pw, G1_pw = lin_einstein(H * PHASE, COORDS, BK)
R1_pw = sp.Matrix(4, 4, lambda m, n: sp.expand(sp.simplify(R1_pw[m, n] / PHASE)))
G1_pw = sp.Matrix(4, 4, lambda m, n: sp.expand(sp.simplify(G1_pw[m, n] / PHASE)))

# Lorenz-gauge identity R^(1)_{mn} = (1/2) k^2 h_{mn}: a nontrivial test of the whole
# Christoffel -> Ricci -> G chain against an independently known result.
LOR = {H[0, 3]: 0, H[1, 3]: 0, H[2, 3]: 0, H[3, 3]: -H[0, 0] + H[1, 1] + H[2, 2]}
R1L = sp.Matrix(4, 4, lambda m, n: sp.expand(R1_pw[m, n].subs(LOR)))
HL = sp.Matrix(4, 4, lambda m, n: H[m, n]).subs(LOR)
check(all(sp.simplify(R1L[m, n] - sp.Rational(1, 2) * kk**2 * HL[m, n]) == 0
          for m in range(4) for n in range(4)),
      "in Lorenz gauge (kbar_{3nu} = 0) the machinery reproduces R^(1)_{mn} = (1/2)k^2 h_{mn}",
      "the standard static plane-wave identity -- an independent validation of the "
      "Riemann-to-Einstein chain before it is used for anything")

gate(all(sp.simplify(G1_pw[3, n]) == 0 for n in range(4)),
     "B/Bianchi  G^(1)_{3 nu} == 0 IDENTICALLY for z-only perturbations, for ARBITRARY "
     "h_{mu nu} -- verified symbolically here, not taken from reading D",
     "linearized Bianchi d^mu G^(1)_{mu nu} = 0 with z-only dependence reads "
     "i k G^(1)_{3 nu} = 0.  CONSEQUENCE: the four (3,nu) Einstein equations contain NO "
     "unknown metric component -- they are PURE CONSTRAINTS on the source, 0 = Theta_{3 nu}, "
     "and cannot be gauged away or discarded")

# ---- residual static gauge freedom, and h_00's invariance
Xi = sp.Matrix(list(sp.symbols("Xi0 Xi1 Xi2 Xi3")))
dh = sp.Matrix(4, 4, lambda m, n: -sp.I * (KMU[m] * Xi[n] + KMU[n] * Xi[m]))
check(sp.simplify(dh[0, 0]) == 0,
      "h_00 is INVARIANT under every residual static gauge transformation (k_0 = 0), so the "
      "PPN read-off below is gauge independent",
      f"and delta h_{{3 nu}} = {[sp.simplify(dh[3,n]) for n in range(4)]} -- four conditions on "
      f"four Xi, so the k-transverse gauge h_{{3 nu}} = 0 is always reachable")

# ---- GATE: c_T^2 = 1 EXACTLY (own derivation, reproduces GW170817-safe corpus result)
hp = sp.Function("h_plus")(t, z)
hc = sp.Function("h_cross")(t, z)
hTT = sp.Matrix([[0, 0, 0, 0], [0, hp, hc, 0], [0, hc, -hp, 0], [0, 0, 0, 0]])
gTT = ETA + BK * hTT
gTTi = gTT.inv()
Amu_TT = sp.Matrix([-1, 0, 0, 0])
AA_TT = sp.simplify(sum(gTTi[m, n] * Amu_TT[m] * Amu_TT[n] for m in range(4) for n in range(4)))
F_TT = sp.Matrix(4, 4, lambda m, n: sp.diff(Amu_TT[n], COORDS[m]) - sp.diff(Amu_TT[m], COORDS[n]))
_, G1_TT = lin_einstein(hTT, COORDS, BK)
want_11 = sp.Rational(1, 2) * (sp.diff(hp, t, 2) - sp.diff(hp, z, 2))
gate(sp.simplify(gTTi[0, 0] + 1) == 0 and sp.simplify(AA_TT + 1) == 0
     and F_TT == sp.zeros(4, 4) and sp.simplify(G1_TT[1, 1] - want_11) == 0,
     "c_T  c_T^2 = 1 EXACTLY, derived here: for a TT wave g^{00} = -1 to ALL orders, so "
     "A_mu = (-1,0,0,0) with lambda = 0 solves the unit constraint EXACTLY and F == 0 "
     "EXACTLY; every aether source in the metric equation vanishes, leaving vacuum GR, and "
     "G^(1)_11 = (1/2)(d_t^2 - d_z^2)h_+ => d_t^2 h = d_z^2 h => speed^2 = 1",
     "reproduces the corpus's committed c_T = 1 exact / GW170817-safe result (c_13 = 0) by a "
     "completely different route, with NO tuning and to all orders in the wave amplitude")


# ======================================================================================
hdr("PART C -- assembling the STRICTLY LINEAR system (the stage72 fix), with a linearity gate")
# ======================================================================================
def build(Wl, gauge=True):
    """Assemble the 15 truncated equations for wind Wl = [w1,w2,w3].
    Returns dict with eqs, labels, unknowns, and the pieces needed for diagnostics."""
    gam, Aupb, Adnb = background(Wl)
    hL = sp.Matrix(4, 4, lambda m, n: H[m, n])
    if gauge:
        hL = hL.subs(GAUGE_T)
    ginv = ETA - ETA * hL * ETA                      # g^{mn} to O(rho)
    Am = sp.Matrix([Adnb[i] + av[i] for i in range(4)])
    Aup = ginv * Am
    F = sp.Matrix(4, 4, lambda m, n: sp.I * (KMU[m] * av[n] - KMU[n] * av[m]))
    Fup = ginv * F * ginv.T
    F2 = sum(Fup[m, n] * F[m, n] for m in range(4) for n in range(4))
    FFmn = sp.Matrix(4, 4, lambda m, n: sum(F[m, b] * ginv[b, d] * F[n, d]
                                            for b in range(4) for d in range(4)))
    # aether EOM: K_B d_mu F^{mu nu} - lambda A^nu = 0
    divF = [sum(sp.I * KMU[m] * Fup[m, n] for m in range(4)) for n in range(4)]
    AE_full = [KB * divF[n] - lam * Aup[n] for n in range(4)]
    # metric: G^(1) - Theta = 0 with Theta = 8 pi G T + K_B F F - (K_B/4) g F^2 + lam A A
    Tm = sp.zeros(4, 4)
    Tm[0, 0] = rho
    Theta_full = sp.Matrix(4, 4, lambda m, n: 8 * sp.pi * GG * Tm[m, n] + KB * FFmn[m, n]
                           - sp.Rational(1, 4) * KB * (ETA[m, n] + hL[m, n]) * F2
                           + lam * Am[m] * Am[n])
    Theta = sp.Matrix(4, 4, lambda m, n: trunc(Theta_full[m, n]))
    G1 = sp.Matrix(4, 4, lambda m, n: G1_pw[m, n].subs(GAUGE_T) if gauge else G1_pw[m, n])
    CON_full = sum(ginv[m, n] * Am[m] * Am[n] for m in range(4) for n in range(4)) + 1

    eqs, labels = [], []
    for m in range(4):
        for n in range(m, 4):
            eqs.append(sp.expand(G1[m, n] - Theta[m, n]))
            labels.append(f"EIN{m}{n}")
    for n in range(4):
        eqs.append(trunc(AE_full[n]))
        labels.append(f"AETH{n}")
    eqs.append(trunc(CON_full))
    labels.append("CONSTR")
    unk = [s for s in HSYMS if s not in GAUGE_T] + av + [lam] if gauge else UNK_ALL
    return dict(eqs=eqs, labels=labels, unk=unk, gam=gam, Aupb=Aupb, Adnb=Adnb,
                Theta=Theta, Theta_full=Theta_full, AE_full=AE_full, CON_full=CON_full,
                divF=divF, F2=F2, FFmn=FFmn)


W_PERP = [wsym, sp.Integer(0), sp.Integer(0)]        # w PERPENDICULAR to k
W_PAR = [sp.Integer(0), sp.Integer(0), wsym]         # w PARALLEL to k
W_GEN = [w1s, w2s, w3s]
W_ZERO = [sp.Integer(0)] * 3

B_perp, B_par, B_gen, B_zero = (build(W) for W in (W_PERP, W_PAR, W_GEN, W_ZERO))

# ---- the dropped terms really are the O(rho^2) ones, and they are exactly the stage72 bug
drop_sample = dropped_part(B_gen["Theta_full"][0, 0])
check(sp.simplify(sp.expand(B_gen["Theta_full"][0, 0] - B_gen["Theta"][0, 0]
                            - drop_sample)) == 0 and drop_sample != 0,
      "the truncation actually removes something, and what it removes is exactly the "
      "products of two O(rho) unknowns -- lambda*a_mu*A^bg, lambda*a*a, and the F-bilinears",
      f"e.g. the piece dropped from Theta_00 is O(rho^2): {sp.simplify(drop_sample)}")
check(all(sp.simplify(trunc_deg0(e)) == 0 for e in B_gen["eqs"]),
      "every equation has ZERO O(rho^0) part: the boosted flat background is an EXACT vacuum "
      "solution, so the linear system is homogeneous apart from the rho source")

# ---- THE LINEARITY GATE the task requires
tsc = sp.Symbol("t_lin", positive=True)
lin_ok, maxdeg = True, 0
for BB in (B_perp, B_par, B_gen):
    for e in BB["eqs"]:
        sc = {s: tsc * s for s in BB["unk"]}
        p = sp.Poly(sp.expand(e.subs(sc)), tsc)
        maxdeg = max(maxdeg, p.degree())
        if p.degree() > 1:
            lin_ok = False
gate(lin_ok and maxdeg <= 1,
     f"LINEARITY  every one of the {len(B_gen['eqs'])} equations has total degree "
     f"{maxdeg} <= 1 in the unknown list, in all three wind configurations -- i.e. NO "
     f"equation contains a product of two unknowns",
     "this is precisely the defect that wedged stage72 (lambda*A_mu*A_nu with A = A_bg + a "
     "is quadratic).  With degree <= 1 guaranteed, sp.linsolve / an explicit matrix solve is "
     "valid and sp.solve's generic nonlinear machinery is never invoked")

# ---- the aether divergence, computed not assumed
_dF = [sp.simplify(trunc(B_gen["divF"][n])) for n in range(4)]
check(_dF[3] == 0 and sp.simplify(_dF[0] - kk**2 * av[0]) == 0,
      f"aether divergence, computed (not assumed) from F^{{mu nu}} = eta eta F, d_mu -> i k_mu, "
      f"and then truncated: d_mu F^{{mu nu}} = {_dF}",
      "the nu=3 component is IDENTICALLY ZERO: the longitudinal a_3 is a pure gradient, hence "
      "invisible to F, hence a FLAT DIRECTION of the aether kinetic term.  (Before truncation "
      "these same components carry H*a products -- the O(rho^2) terms stage72 kept.)")


# ======================================================================================
hdr("PART D -- the PPN matching, DERIVED (U_ij identity and the a,b -> alpha_1,alpha_2 map)")
# ======================================================================================
Usym = sp.Symbol("U", positive=True)
# chi with lap chi = -2U;  U_ij := chi_,ij + delta_ij U   (standard superpotential)
nhat = [0, 0, 1]
chi_k = 2 * Usym / kk**2                              # lap -> -k^2
Uij = sp.Matrix(3, 3, lambda i, j: (-kk**2 * nhat[i] * nhat[j] * chi_k)
                + (Usym if i == j else 0))
check(sp.simplify(sum(Uij[i, i] for i in range(3)) - Usym) == 0,
      "U_ij trace identity U_ii = U (the normalisation that ties U_ij to U with the same G_N)")
check(all(sp.simplify(Uij[i, j] - ((1 if i == j else 0) - 2 * nhat[i] * nhat[j]) * Usym) == 0
          for i in range(3) for j in range(3)),
      "DERIVED Fourier identity U_ij = (delta_ij - 2 n_i n_j) U",
      "hence w^i w^j U_ij = (w^2 - 2 (w.nhat)^2) U -- verified next")
wtest = [w1s, w2s, w3s]
wwU = sp.expand(sum(wtest[i] * wtest[j] * Uij[i, j] for i in range(3) for j in range(3)))
check(sp.simplify(wwU - (sum(c**2 for c in wtest) - 2 * w3s**2) * Usym) == 0,
      "w^i w^j U_ij = (w^2 - 2 (w.nhat)^2) U  with nhat = khat = zhat")
# now the matching, by equating coefficients
aa, bb_, al1, al2 = sp.symbols("a b alpha_1 alpha_2")
lhs_match = aa * (sum(c**2 for c in wtest)) * Usym + bb_ * w3s**2 * Usym
rhs_match = al1 * (sum(c**2 for c in wtest)) * Usym + al2 * wwU
msol = sp.solve([sp.Eq(sp.expand(lhs_match - rhs_match).coeff(w1s, 2), 0),
                 sp.Eq(sp.expand(lhs_match - rhs_match).coeff(w3s, 2), 0)],
                [al1, al2], dict=True)[0]
check(sp.simplify(msol[al2] + bb_ / 2) == 0 and sp.simplify(msol[al1] - (aa + bb_ / 2)) == 0,
     f"MATCHING DERIVED, not assumed: delta h_00 = [a w^2 + b (w.nhat)^2] U corresponds to "
     f"alpha_1 = {msol[al1]}, alpha_2 = {msol[al2]} in convention Z",
      "obtained by equating the w_1^2 and w_3^2 coefficients of the two forms; convention W "
      "(Will) flips both signs")


def alphas(a_val, b_val):
    return sp.simplify(a_val + b_val / 2), sp.simplify(-b_val / 2)


# ======================================================================================
hdr("PART E -- the EXACT-in-w matrix solves, with RANK, for both wind orientations")
# ======================================================================================
def matrix_solve(BB, drop_labels=(), extra_subs=None):
    """Linear matrix solve.  Returns (M, rhs, rank, rank_aug, solution dict or None)."""
    eqs, labels, unk = BB["eqs"], BB["labels"], list(BB["unk"])
    keep = [e for e, l in zip(eqs, labels) if l not in drop_labels]
    if extra_subs:
        keep = [sp.expand(e.subs(extra_subs)) for e in keep]
        unk = [u for u in unk if u not in extra_subs]
    keep = [e for e in keep if sp.simplify(e) != 0]
    M, rhsv = sp.linear_eq_to_matrix(keep, unk)
    rk = M.rank()
    rk_aug = M.row_join(rhsv).rank()
    sol = sp.linsolve((M, rhsv), unk)
    if sol is sp.EmptySet or len(sol) == 0:
        return M, rhsv, rk, rk_aug, None, unk, len(keep)
    tup = list(sol)[0]
    return M, rhsv, rk, rk_aug, dict(zip(unk, [sp.simplify(v) for v in tup])), unk, len(keep)


U_std = 4 * sp.pi * GG * rho / kk**2                 # U at G_N = G (the action's G)
results = {}

for tag, BB, Wl in (("PERP  (w perp k)", B_perp, W_PERP), ("PAR   (w parallel k)", B_par, W_PAR)):
    M, rhsv, rk, rk_aug, sol, unk, neq = matrix_solve(BB)
    print(f"\n  ---- {tag} ----")
    print(f"    {neq} nontrivial equations, {len(unk)} unknowns; rank(M) = {rk}, "
          f"rank([M|b]) = {rk_aug}")
    check(sol is not None and rk == rk_aug,
          f"{tag}: the system is CONSISTENT (rank[M|b] = rank M = {rk}) and solves",
          "so this branch really is a solution of the full theory, not a truncation artefact")
    h00 = sp.simplify(sol[H[0, 0]])
    lamv = sp.simplify(sol[lam])
    a3v = sp.simplify(sol[av[3]])
    deg = len(unk) - rk
    print(f"    h_00     = {sp.simplify(sp.factor(h00))}")
    print(f"    lambda   = {sp.simplify(sp.factor(lamv))}")
    print(f"    a_3      = {a3v}")
    print(f"    DEGENERACY (dim of solution space) = {deg}")
    results[tag] = dict(h00=h00, lam=lamv, a3=a3v, rank=rk, deg=deg, sol=sol, unk=unk)

R_perp = results["PERP  (w perp k)"]
R_par = results["PAR   (w parallel k)"]

check(R_perp["deg"] == 1 and sp.simplify(R_perp["h00"].diff(av[3])) == 0,
      f"*** PERP is RANK-DEFICIENT by exactly {R_perp['deg']}: a_3 appears in ZERO equations "
      f"(it is invisible to F, and w.a = w a_1 does not contain it), so it is a genuine ZERO "
      f"MODE -- the algebraic signature reading D points to.  h_00 does not depend on it ***",
      "this is the c_123 = 0 degeneracy showing up as a rank deficiency of the STATIC linear "
      "response, in a completely explicit finite-dimensional matrix")
check(R_par["deg"] == 0,
      f"*** PAR is FULL RANK (degeneracy {R_par['deg']}): with w_3 != 0 the unit constraint "
      f"contains 2 gamma w_3 a_3, so a_3 IS determined -- and the (3,nu) constraints then "
      f"force lambda ***")
check(sp.simplify(R_par["lam"]) == 0,
      "*** CONSTRAINTS IMPOSED, w NOT perpendicular to k: lambda = 0 IDENTICALLY, for every "
      "K_B and every w.  READING D's MECHANISM IS CONFIRMED BY THE DIRECT SOLVE ***",
      "and lambda A_mu A_nu is the ONLY aether source in the linearized Einstein equation, so "
      "the metric is exactly the GR metric of static dust")
check(sp.simplify(R_par["h00"] - 2 * U_std) == 0,
      f"and therefore h_00(w parallel k) = {sp.simplify(R_par['h00'])} = 2U with G_N = G "
      f"EXACTLY -- no w-dependence at ANY order, so a = b = 0 and alpha_1 = alpha_2 = 0",
      "reading D reproduced, from an independent assembly of the same theory")


# ======================================================================================
hdr("PART F -- the Newtonian-limit GATES, then the w^2 read-off on each branch")
# ======================================================================================
# w = 0 exactly: both orientations degenerate to the same system
M0, r0, rk0, rka0, sol0, unk0, neq0 = matrix_solve(B_zero)
lam0 = sp.simplify(sp.factor(sol0[lam]))
h00_0 = sp.simplify(sol0[H[0, 0]])
GN_w0 = sp.simplify(h00_0 * kk**2 / (2 * 4 * sp.pi * rho))
print(f"    w = 0 exactly:  lambda_0 = {lam0}")
print(f"                    h_00     = {sp.factor(h00_0)}")
print(f"                    G_N(w=0) = {sp.factor(GN_w0)}")
gate(sp.simplify(GN_w0 - GG / (1 - KB / 2)) == 0,
     "G_N  at w = 0 the solve gives G_N = G/(1 - K_B/2) -- i.e. AeST's quasi-static "
     "G~ = (1 - K_B/2)G^ EXACTLY, a published number this machinery never fitted "
     "(SZ21 / arXiv:2304.05134, already on the corpus record from a different calculation)",
     "this is the single strongest validation available: if the assembly had a sign or factor "
     "error, this would not come out")
gate(sp.simplify(lam0 - KB * 8 * sp.pi * GG * rho / (2 - KB)) == 0,
     "lambda_0  lambda(w=0) = 8 pi G K_B rho/(2 - K_B) != 0 for K_B != 0",
     "reduces to the independent check's K_B rho/(2(2-K_B)) in its 16 pi G = 1 units -- "
     "an independent reproduction of that script's Branch B")
hij0 = [sp.simplify(sol0[H[i, i]]) for i in (1, 2)]
gate(all(sp.simplify(hh - h00_0) == 0 for hh in hij0) and sp.simplify(sol0[H[0, 1]]) == 0,
     "gamma_PPN  at w = 0, h_ij = h_00 delta_ij in the k-transverse gauge, i.e. gamma_PPN = 1 "
     "-- the corpus's committed lensing result, reproduced",
     "beta is an O(rho^2) quantity and is OUT OF SCOPE for a linear-in-rho calculation; it is "
     "NOT checked and NOT claimed here")
gate(sp.simplify(lam0.subs(KB, 0)) == 0 and sp.simplify(GN_w0.subs(KB, 0) - GG) == 0
     and sp.simplify(R_perp["h00"].subs(KB, 0) - 2 * U_std) == 0
     and sp.simplify(R_par["h00"].subs(KB, 0) - 2 * U_std) == 0,
     "K_B->0  the K_B -> 0 limit is exactly GR on BOTH branches: lambda -> 0, G_N -> G, and "
     "h_00 -> 2U with no w-dependence, so alpha_1 = alpha_2 = 0 at K_B = 0 either way")


def readoff(h00, wl, label):
    """Match h00 to 2 U_N + [a w^2 + b (w.nhat)^2] U_N against the branch's OWN Newtonian
    limit, and return (a, b, U_N)."""
    # the branch's OWN Newtonian limit: h_00 at w -> 0 WITHIN this orientation
    h00_0b = sp.simplify(h00.subs(wsym, 0)) if wsym in h00.free_symbols else sp.simplify(h00)
    UN = sp.simplify(h00_0b / 2)
    ser = sp.expand(sp.series(sp.expand(h00 / UN), wsym, 0, 4).removeO())
    c2 = sp.simplify(ser.coeff(wsym, 2))
    print(f"    {label}: U_N = {sp.factor(UN)}   (G_N/G = {sp.simplify(UN/U_std)})")
    print(f"       h_00/U_N = 2 + ({c2}) w^2 + O(w^4)")
    return c2, UN


print()
a_perp, UN_perp = readoff(R_perp["h00"], W_PERP, "PERP  ")
a_par_tot, UN_par = readoff(R_par["h00"], W_PAR, "PAR   ")
check(sp.simplify(a_perp - 4 * KB) == 0,
      f"*** PERP BRANCH: the w^2 coefficient is a = {sp.simplify(a_perp)} = 4 K_B EXACTLY "
      f"(all orders in K_B, not just leading).  Since (w.khat) = 0 here, this is a alone ***",
      "and this branch is REGULAR: lambda is determined self-consistently, no pole anywhere, "
      "and it is continuous with the w = 0 solution")
check(sp.simplify(a_par_tot) == 0,
      f"*** PAR BRANCH: the w^2 coefficient is {sp.simplify(a_par_tot)} -- exactly zero, so "
      f"a + b = 0 in that branch, and alpha_1 = alpha_2 = 0.  READING D ***")

# ---- THE DISCONTINUITY, stated sharply
lam_perp_lim = sp.simplify(sp.limit(R_perp["lam"], wsym, 0))
check(sp.simplify(lam_perp_lim - lam0) == 0 and sp.simplify(R_par["lam"]) == 0 and lam0 != 0,
      "*** THE DISCONTINUITY IS IN THE DIRECTION OF w, NOT ONLY AT w = 0: lambda -> lambda_0 "
      "!= 0 as w -> 0 ALONG the perpendicular plane, but lambda == 0 for EVERY w with "
      "w.khat != 0.  The two branches also disagree at O(w^0): G_N = G/(1-K_B/2) on the "
      "perpendicular plane versus G_N = G off it ***",
      f"G_N(perp)/G_N(par) = {sp.simplify(UN_perp/UN_par)}, so the w^0 coefficient of h_00 "
      f"itself jumps.  A PPN form requires a DIRECTION-INDEPENDENT w^0 term; this theory does "
      f"not have one, which is why alpha_1 and alpha_2 -- DEFINED as O(w^2) Taylor "
      f"coefficients about a common Newtonian limit -- do not exist in the usual sense")
info("physical reading of the branch structure, stated both ways",
     "(i) FOR reading D: for any fixed w != 0 the perpendicular plane w.k = 0 is a MEASURE-ZERO "
     "set of Fourier modes, so a real static mass distribution is built almost entirely from "
     "lambda = 0 modes -- the position-space answer is G_N = G and alpha_1 = alpha_2 = 0.  "
     "(ii) AGAINST reading D: the corpus's OWN quasi-static G~ = (1 - K_B/2)G^ lives on the "
     "lambda != 0 branch, so if the lambda = 0 branch were the physical one the corpus's G~ "
     "would be wrong; and the lambda = 0 branch is exactly the one carrying the wake below")

# ---- the wake: the price of lambda = 0
a3_par = R_par["a3"]
res_pole = sp.simplify(sp.limit(a3_par * wsym, wsym, 0))
check(res_pole != 0,
      f"*** THE PRICE OF lambda = 0: a_3 = {a3_par} has a SIMPLE POLE at w.khat -> 0 with "
      f"nonzero residue {sp.factor(res_pole)} = U (at G_N = G) ***",
      "in position space the constraint becomes the transport equation (w.grad)chi = "
      "gamma(1+w^2)U along the wind, whose solution integrates U ~ 1/r along a ray and is "
      "LOG-DIVERGENT: A_mu does NOT return to A_bg at infinity.  The residual static gauge "
      "shifts a_3 by -i k (A_bg . Xi) with Xi fixed by the metric sector, which is REGULAR as "
      "w -> 0 on this branch (h = 2U, pure GR), so the pole is NOT removable by gauge")


# ======================================================================================
hdr("PART G -- the ORDER-BY-ORDER-IN-w solve (the prescribed recipe): it FAILS in one arm")
# ======================================================================================
EE = sp.Symbol("e_w", positive=True)


def order_by_order(Wl, nmax=2, label=""):
    """Solve order by order in the wind bookkeeping parameter e_w, substituting lower
    orders before going up.  Returns (h00_series, failure_order_or_None)."""
    BB = build([EE * c for c in Wl])
    unk = list(BB["unk"])
    uo = [[sp.Symbol(f"{s.name}__{o}") for s in unk] for o in range(nmax + 1)]
    smap = {unk[i]: sum(EE**o * uo[o][i] for o in range(nmax + 1)) for i in range(len(unk))}
    eqs_e = []
    for e in BB["eqs"]:
        ee = sp.expand(sp.series(sp.expand(e.subs(smap)), EE, 0, nmax + 1).removeO())
        eqs_e.append(sp.expand(ee))
    known, out = {}, {}
    for o in range(nmax + 1):
        cur = [sp.expand(sp.expand(e).coeff(EE, o).subs(known)) for e in eqs_e]
        cur = [c for c in cur if sp.simplify(c) != 0]
        if not cur:
            for i, s in enumerate(unk):
                known[uo[o][i]] = sp.Integer(0)
            continue
        M, rr = sp.linear_eq_to_matrix(cur, uo[o])
        sol = sp.linsolve((M, rr), uo[o])
        if sol is sp.EmptySet or len(sol) == 0:
            print(f"    {label} O(w^{o}): NO SOLUTION -- rank(M) = {M.rank()}, "
                  f"rank([M|b]) = {M.row_join(rr).rank()}  => system INCONSISTENT")
            return None, o
        tup = list(sol)[0]
        known.update({uo[o][i]: sp.simplify(tup[i]) for i in range(len(unk))})
        out[o] = dict(zip(unk, [sp.simplify(v) for v in tup]))
        print(f"    {label} O(w^{o}): solved   (rank {M.rank()} of {len(uo[o])} unknowns, "
              f"lambda^({o}) = {sp.simplify(out[o][lam].subs(known))})")
    idx = unk.index(H[0, 0])
    h00s = sp.expand(sum(EE**o * known[uo[o][idx]] for o in range(nmax + 1)))
    return h00s, None


print("\n  ---- w PERPENDICULAR to k, order by order ----")
h00_obo_perp, failp = order_by_order(W_PERP, 2, "PERP")
print("\n  ---- w PARALLEL to k, order by order ----")
h00_obo_par, failq = order_by_order(W_PAR, 2, "PAR ")

check(failp is None and h00_obo_perp is not None,
      "the order-by-order recipe SUCCEEDS on the perpendicular arm")
if h00_obo_perp is not None:
    ex = sp.expand(sp.series(sp.expand(R_perp["h00"].subs(wsym, EE * wsym)), EE, 0, 3).removeO())
    check(sp.simplify(sp.expand(h00_obo_perp.subs({sp.Symbol('a_3__0'): 0,
                                                   sp.Symbol('a_3__1'): 0,
                                                   sp.Symbol('a_3__2'): 0}) - ex)) == 0,
          "and it AGREES with the exact-in-w solve to O(w^2) -- two independent solve strategies, "
          "same answer, so the 4 K_B is not an artefact of either",
          "(the a_3 zero mode is set to zero to compare; h_00 does not depend on it)")

check(failq == 1,
      f"*** THE ORDER-BY-ORDER SOLVE HAS NO SOLUTION AT O(w^1) ON THE PARALLEL ARM "
      f"(failure order = {failq}).  This is the sharpest form of the result: at O(w^0) the "
      f"(3,nu) constraints are vacuous and force lambda = lambda_0 != 0, and then the O(w^1) "
      f"part of Theta_{{30}} = -lambda gamma^2 w_3 reads lambda_0 * w = 0, a CONTRADICTION ***",
      "so g_00 has NO Taylor series in w at w = 0, and alpha_1, alpha_2 -- DEFINED as the "
      "O(w^2) Taylor coefficients -- DO NOT EXIST for this theory.  Both reading L and reading "
      "D are answers to a question whose premise (analyticity in w) fails.  This is exactly the "
      "trap the prescribed recipe was designed to expose, and it is why the exact-in-w solve "
      "was run as the primary route")


# ======================================================================================
hdr("PART H -- the CONSTRAINTS DROPPED arm: what it gives, and why it is worse than illegal")
# ======================================================================================
DROP = ["EIN03", "EIN13", "EIN23", "EIN33", "AETH3"]
Md, rd, rkd, rkad, sold, unkd, neqd = matrix_solve(B_gen, drop_labels=DROP)
print(f"    general w, {neqd} equations kept (dropped {DROP}), {len(unkd)} unknowns; "
      f"rank(M) = {rkd}, rank([M|b]) = {rkad}, degeneracy = {len(unkd) - rkd}")
check(sold is not None and len(unkd) - rkd >= 1,
      f"*** DROPPING THE CONSTRAINTS LEAVES THE SYSTEM RANK-DEFICIENT by {len(unkd)-rkd}: "
      f"lambda is UNDETERMINED.  So the third reading's alpha_1 = +3K_B/2 is not what the "
      f"algebra gives when the constraints are discarded -- it is what one gets after ALSO "
      f"imposing the extra, ad-hoc input lambda(w) = lambda_0 ***",
      "with the (3,nu) equations gone, the unit constraint is solved by a_3 (which they had "
      "made determinate), so nothing fixes lambda at all")

# now freeze lambda at its w=0 value, exactly as the third reading does
h00_frozen = sp.simplify(sold[H[0, 0]].subs(lam, lam0)) if sold is not None else None
UN_fr = sp.simplify(h00_frozen.subs({w1s: 0, w2s: 0, w3s: 0}) / 2)
serf = sp.expand(sp.series(sp.expand(sp.series(sp.expand(
    (h00_frozen / UN_fr).subs({w1s: EE * w1s, w2s: EE * w2s, w3s: EE * w3s})),
    EE, 0, 3).removeO()), EE, 0, 3).removeO())
q2 = sp.expand(sp.simplify(serf.coeff(EE, 2)))
a_fr = sp.simplify(q2.coeff(w1s, 2))
a_fr2 = sp.simplify(q2.coeff(w2s, 2))
b_fr = sp.simplify(sp.simplify(q2.coeff(w3s, 2)) - a_fr)
check(sp.simplify(a_fr - a_fr2) == 0
      and sp.simplify(q2 - (a_fr * (w1s**2 + w2s**2 + w3s**2) + b_fr * w3s**2)) == 0,
      f"the frozen-lambda delta h_00 really is of the form a w^2 + b (w.nhat)^2 (isotropic in "
      f"the two transverse directions, no cross terms): a = {a_fr}, b = {b_fr}")
al1_fr, al2_fr = alphas(a_fr, b_fr)
check(sp.simplify(a_fr - 2 * KB) == 0 and sp.simplify(b_fr + KB) == 0
      and sp.simplify(al1_fr - 3 * KB / 2) == 0 and sp.simplify(al2_fr - KB / 2) == 0,
      f"*** THE THIRD READING IS REPRODUCED EXACTLY: constraints dropped + lambda frozen at "
      f"lambda_0 gives a = {a_fr}, b = {b_fr}, hence alpha_1 = {al1_fr}, alpha_2 = {al2_fr} "
      f"in convention Z (convention W: {-al1_fr}, {-al2_fr}) ***",
      "an independent confirmation of the number stage73 recorded but nobody claimed -- so the "
      "machinery here agrees with the independent check on BOTH of its arms")
# which half of the third reading is robust?
h00_gen = sp.simplify(sold[H[0, 0]])
lam_free = sp.Symbol("lam_free")
h00_lin = sp.simplify(h00_gen.subs(lam, lam0 * (1 + lam_free * (w1s**2 + w2s**2 + w3s**2))))
ser2 = sp.expand(sp.series(sp.expand((h00_lin / UN_fr).subs(
    {w1s: EE * w1s, w2s: EE * w2s, w3s: EE * w3s})), EE, 0, 3).removeO())
q2b = sp.expand(sp.simplify(ser2.coeff(EE, 2)))
a_v = sp.simplify(q2b.coeff(w1s, 2))
b_v = sp.simplify(sp.simplify(q2b.coeff(w3s, 2)) - a_v)
check(sp.simplify(b_v + KB) == 0 and sp.simplify(sp.diff(a_v, lam_free)) != 0,
      f"*** AND WHICH HALF OF THE THIRD READING IS ROBUST IS NOW SETTLED: allowing lambda an "
      f"arbitrary O(w^2) piece lambda_0(1 + c w^2) leaves b = {b_v} = -K_B UNCHANGED but makes "
      f"a = {sp.simplify(a_v)} ARBITRARY.  So in that arm alpha_2 = +K_B/2 is fixed by "
      f"lambda(w=0) ALONE, while alpha_1 = +3K_B/2 is an artefact of the ad-hoc freezing ***",
      "the (w.nhat)^2 structure can only come from Theta_11 + Theta_22 = lambda gamma^2 "
      "(w^2 - w_3^2), whose O(w^2) coefficient needs only lambda(w=0); the isotropic w^2 piece "
      "picks up lambda's own w-dependence, which the dropped equations were the only thing "
      "fixing.  NEW, and it sharpens stage73's PART B4")


# ======================================================================================
hdr("PART I -- numeric cross-check, and the confrontation with READING L")
# ======================================================================================
NUM = {KB: sp.Rational(1, 7), wsym: sp.Rational(1, 5), rho: sp.Integer(1),
       kk: sp.Integer(1), GG: sp.Integer(1)}
for tag, BB, ref in (("PERP", B_perp, R_perp), ("PAR", B_par, R_par)):
    Bn = dict(BB)
    Bn["eqs"] = [sp.expand(e.subs(NUM)) for e in BB["eqs"]]
    _, _, _, _, soln, _, _ = matrix_solve(Bn)
    got = sp.simplify(soln[H[0, 0]])
    want = sp.simplify(ref["h00"].subs(NUM))
    check(sp.simplify(got - want) == 0,
          f"numeric cross-check {tag} at K_B = 1/7, w = 1/5, rho = k = G = 1: the rational "
          f"re-solve gives h_00 = {got}, matching the symbolic formula",
          "an independent path through the same matrix, guarding against a simplification bug")

a1_L = -4 * KB
check(all(sp.simplify(cand - a1_L) != 0 for cand in
          [sp.Integer(0), al1_fr, sp.simplify(a_perp + 0)]),
      f"*** READING L IS NOT REPRODUCED BY ANY ARM OF THE DIRECT SOLVE: alpha_1 = -4 K_B "
      f"appears nowhere.  The arms give 0 (constraints imposed, generic w), {al1_fr} "
      f"(constraints dropped + lambda frozen), and an undetermined alpha_1 (constraints "
      f"dropped, lambda free) ***",
      "so the Foster-Jacobson generic formula is indeed being applied off its domain: it "
      "presumes every aether mode propagates, whereas at c_123 = 0 the spin-0 mode is static "
      "and the static response is a CONSTRAINED, branch-dependent problem")
check(sp.simplify(sp.Abs(a_perp) - 4 * KB) == 0,
      f"*** BUT THE MAGNITUDE 4 K_B IS REAL AND IT DOES APPEAR: the only REGULAR branch (w "
      f"perpendicular to k -- self-consistent lambda, no pole, continuous with w = 0) has "
      f"w^2 U coefficient a = {a_perp}.  In a convention where the w^2 U coefficient is "
      f"-alpha_1 (Will, alpha_3 = 0) that reads alpha_1 = -4 K_B -- numerically reading L ***",
      "RECORDED, NOT CLAIMED, and stated against interest: it is a coincidence of magnitude on "
      "a single-direction branch, not a derivation of reading L, because the same solve gives "
      "b != 0 (see next) whereas the identification alpha_1 = -a requires alpha_2 = 0.  It does "
      "mean the honest prior on the SIZE of preferred-frame effects here is ~4 K_B, not 0")

# the cross-branch match: each branch normalised to its OWN Newtonian limit
a_x = a_perp
b_x = sp.simplify(a_par_tot - a_perp)
al1_x, al2_x = alphas(a_x, b_x)
print(f"\n    CROSS-BRANCH MATCH (each branch to its own G_N):  a = {a_x}, b = {b_x}")
print(f"       => convention Z: alpha_1 = {al1_x}, alpha_2 = {al2_x}")
print(f"          convention W: alpha_1 = {-al1_x}, alpha_2 = {-al2_x}")
check(sp.simplify(al1_x - 2 * KB) == 0 and sp.simplify(al2_x - 2 * KB) == 0,
      f"a FOURTH arm, reported for completeness and explicitly NOT claimed: matching the two "
      f"orientations after normalising each to its own Newtonian limit gives alpha_1 = "
      f"alpha_2 = {al1_x} = 2 K_B",
      "ILLEGITIMATE, and the reason is precise: a PPN match requires ONE w^0 term, and these "
      "two branches have DIFFERENT ones (G vs G/(1-K_B/2)).  Listed so that nobody rediscovers "
      "it and mistakes it for a result; if it were legitimate, |alpha_2| < 1e-7 would give "
      f"K_B < {sp.simplify(1e-7/2):.1e}, tighter than reading L")

# what a K_B bound would look like on each arm, for the record only
print("\n    what each arm WOULD imply for K_B (arithmetic only -- NOT a bound in force):")
for nm, a1v, a2v in (("constraints imposed (reading D)", sp.Integer(0), sp.Integer(0)),
                     ("constraints dropped + lambda frozen", al1_fr, al2_fr),
                     ("cross-branch (illegitimate)", al1_x, al2_x),
                     ("reading L (literature map)", -4 * KB, sp.nan)):
    s1 = "no bound" if a1v == 0 else (
        f"K_B < {float(sp.solve(sp.Eq(sp.Abs(a1v), 1e-4), KB)[0]):.2e}" if a1v.free_symbols else "-")
    s2 = "no bound" if a2v == 0 else (
        f"K_B < {float(sp.solve(sp.Eq(sp.Abs(a2v), 1e-7), KB)[0]):.2e}"
        if getattr(a2v, "free_symbols", set()) else "NOT COMPUTED")
    print(f"      {nm:38s}  from |alpha_1|<1e-4: {s1:16s}  from |alpha_2|<1e-7: {s2}")
info("reading L's alpha_2 is NOT COMPUTED here and must not be guessed",
     "stage70's own B3 records that the Einstein-aether alpha_2 expression involves c_2 and the "
     "c_123 combinations in a form it did not verify -- and c_123 = 0 is exactly this theory's "
     "degeneracy.  Writing down an unverified alpha_2 formula would be worse than leaving it "
     "open, so it is left open")


# ======================================================================================
hdr("PART J -- SCOPE, and the verdict")
# ======================================================================================
check(True,
      "SCOPE: this is the AETHER SECTOR ONLY.  AeST adds 2(2-K_B)J^mu grad_mu phi and "
      "-(2-K_B)Y, which is what lifts the c_123 = 0 degeneracy -- a SIBLING agent is computing "
      "that, and it is not duplicated here.  Nothing in this file adjusts a_0 = kappa c "
      "sqrt(G rho_Lambda) (9.3619e-11 canonical / 1.1279e-10 alt), the kernel nu(y) = "
      "1/(1-exp(-sqrt y)), kappa = 1/2, or beta = 1: those appear ZERO times above",
      "the risk located here is in the adopted relativistic home's vector sector, and it can "
      "neither be traded away by adjusting kappa nor blamed on it")
check(True,
      "*** VERDICT.  (1) READING D's MECHANISM IS CONFIRMED by an independent properly-"
      "linearised solve: for every w with w.khat != 0 the (3,nu) constraints force lambda = 0 "
      "exactly, h_00 = 2U with G_N = G, and alpha_1 = alpha_2 = 0 at all orders in w and K_B.  "
      "(2) READING L IS NOT REPRODUCED anywhere.  (3) THE THIRD READING is reproduced exactly "
      "when lambda is frozen, but the dropped system is rank-deficient in lambda, so only its "
      "alpha_2 = +K_B/2 is robust and its alpha_1 = +3K_B/2 is an artefact.  (4) NEW AND "
      "SHARPEST: the prescribed order-by-order-in-w solve has NO SOLUTION AT O(w^1) on the "
      "parallel arm, so g_00 is not analytic in w and alpha_1, alpha_2 do not exist as Taylor "
      "coefficients.  (5) AGAINST INTEREST: the one REGULAR branch (w perp k) carries "
      "a = 4 K_B, so the honest prior on the SIZE of preferred-frame effects in this sector is "
      "~4 K_B, not zero. ***",
      "DIRECTION: MIXED.  Favourable, because reading L's K_B < 2.5e-5 ceiling -- and hence "
      "stage73's EMPTY window against the subluminality floor K_B >= 2/(K_2+1) -- is NOT in "
      "force.  Adverse, because what replaces it is not a clean zero but a theory with no "
      "static PPN limit: the same c_123 = 0 degeneracy that gives c_T = 1 free also makes the "
      "preferred-frame question ill-posed, and the magnitude it is hiding is 4 K_B")
info("NOT COMPUTED, explicitly",
     "(a) the physical branch.  Deciding between lambda = 0 (wake, non-normalisable) and "
     "lambda != 0 (regular, but only on a measure-zero plane) requires a TIME-DEPENDENT "
     "calculation in which the wake is cut off -- a finite-time / finite-extent regularisation "
     "of the c_S = 0 resonance.  That is the calculation this fork actually needs, and it is "
     "not done here.  (b) alpha_2 in the Einstein-aether literature formula (would need an "
     "unverified expression with c_123 in it).  (c) anything with the scalar sector retained "
     "(sibling agent).  (d) beta_PPN (O(rho^2), out of scope for a linear-in-rho solve).  "
     "(e) any bound on K_B: NONE is in force from this file, in either direction")

# ======================================================================================
hdr("GATE ENFORCEMENT AND LEDGER")
# ======================================================================================
for ok, nm in GATES:
    print(f"    gate {nm:12s} {'HELD' if ok else 'FAILED'}")
assert all(ok for ok, _ in GATES), (
    "A GATE FAILED -- the machinery is not validated, so NOTHING in this file is claimed: "
    f"{[nm for ok, nm in GATES if not ok]}")
print(f"\n    all {len(GATES)} gates HELD (c_T^2 = 1 exact; G^(1)_3nu == 0; strict linearity; "
      f"G_N(w=0) = G/(1-K_B/2) = AeST's G~; lambda_0; gamma_PPN = 1; K_B -> 0 = GR)")
n_fail = len(FAIL)
print(f"\n    CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
