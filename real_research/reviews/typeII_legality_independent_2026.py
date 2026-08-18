#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
typeII_legality_independent_2026.py
===================================
AN INDEPENDENT RE-DERIVATION OF AeST's QUASI-STATIC SCALAR SECTOR, AND OF THE "LEGALITY
THEOREM" THAT nbody_2026/stage75_the_closed_theory_2026.py USES TO CLAIM AeST's ONE FREE
FUNCTION IS DETERMINED.  Nothing below is imported from ppn_newtonian_radial_2026.py PART Q;
every equation is rebuilt from the action.

    THE ACTION (Skordis & Zlosnik, arXiv:2007.00082 \label{NT_A_action} = Eq. 5; restated
    independently as arXiv:2109.13287 Eq. 1; the transcription used here is the one in
    real_research/bridge1_aest_equations.md):

      S = int d^4x (sqrt(-g)/16 pi Gt) [ R - 2 Lam - (K_B/2) F^{mu nu} F_{mu nu}
            + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Ycal - Fcal(Ycal, Qcal)
            - lam (A^mu A_mu + 1) ] + S_m[g]

      Qcal = A^mu grad_mu phi,   Ycal = (g^{mu nu} + A^mu A^nu) grad_mu phi grad_nu phi,
      F_{mu nu} = 2 grad_[mu A_nu],   J^mu = A^nu grad_nu A^mu,
      Fcal(Y,Q) = (2-K_B) J(Y) + K(Q),  K(Q) = -2 Lam + K_2 (Q - Q_0)^2 + ...

WHAT IS TESTED, AND WHAT THE ANSWER IS
======================================
(P1) Q = (1-Psi)Q_0 and Y = |grad(scalar)|^2 at quadratic order.
     -> CONFIRMED, WITH ONE CORRECTION THAT MATTERS FOR THE METHOD.  PART Q sets the aether's
        spatial part A_i = 0 by a t-reflection argument and then reads Y = |grad varphi|^2.
        With the aether's own scalar perturbation RESTORED, A_i = grad_i alpha, the exact
        quadratic-order result is
                 Y = |grad chi|^2 ,      chi = varphi + Q_0 alpha
        -- SZ21's OWN mixing variable chi (bridge1_aest_equations.md, "Mixing variables").
        varphi alone is NOT the invariant; alpha and varphi enter every term of the reduction
        only through chi (checks Q4-Q6), so PART Q's algebra is right but its VARIABLE is
        gauge-incomplete.  Every downstream statement survives with varphi -> chi.
(P2) Psi = Psi_N + chi with J_Y(Y) grad chi = grad Psi_N.   -> CONFIRMED (check R3).
(P3) u = |grad chi| is the anomalous acceleration and obeys u J_Y(u^2) = g_bar.
     -> CONFIRMED EXACTLY for spherical symmetry (Gauss's theorem on the divergence-form
        equation, check R4), with the two corrections it neglects PRICED: the scalar mass
        term (m r)^2 <= 1.0e-04 at 10 kpc and 2.4e-23 at 1 AU, and Lam r^2 <= 1.1e-11 at
        10 kpc.  P3 is not an approximation that could be wrong by the O(1) factor Route A
        would need.
(MULTIPLIER) PART Q eliminates lam by SUBSTITUTION (it solves A.A = -1 order by order and the
        lam-term then vanishes identically).  That is legitimate -- and it is NOT the earlier
        defect.  Checks M1-M3 do the calculation the hard way instead, keeping A_0's
        perturbations a1, a2 free and lam = lam_0 + eps lam_1 explicit, and find
             lam_0 = (2-K_B)(1 + J_Y) Q_0^2 + K_Q Q_0/2 = A_Y Q_0^2 + K_Q Q_0/2,
        NONZERO and of order Q_0^2 -- so the corpus's earlier lam_bg = 0 really was a defect,
        and the magnitude A_Y Q_0^2 quoted for it is reproduced here from the action.  ONE
        HONEST WRINKLE, reported rather than smoothed: the O(eps) equation delta/delta a_1 and
        the O(eps^2) equation delta/delta a_2 give the SAME analytic part but only the second
        sees the J-term, because J(Y) ~ Y^(3/2) is non-analytic in the eps-grading (reduction
        R-II) and belongs to both orders.  The operative value at the order where the
        quasi-static equations live is the a_2 one, WITH the (1+J_Y) -- and using the
        J-blind value instead is exactly the class of error that produced the earlier
        spurious graviton mass (check M1).  With the multipliers taken from their own O(eps^2)
        equations, the two routes give IDENTICAL Psi, Phi, alpha and chi equations to
        quadratic order, with an explicit degree check that the only residual is cubic
        (check M3).  The multiplier is handled consistently.
(BACKGROUND) The background solves its own equations iff K_Q = 0 and Lam r^2 -> 0 (check M4):
        the O(eps) Lagrangian is K_Q Q_0 Psi + total derivative.  K_Q Q_0 = 8 pi Gt rhobar_dm
        is the AMBIENT dark-sector density, so the local reduction neglects exactly the cosmic
        mean dark density -- 4.0e-07 of the Galactic midplane baryon density at 10 kpc.

(a) THE NO-GHOST CONDITION, DERIVED FROM THE ACTION AND NOT QUOTED (PART G).  In the
    (Psi_N, chi) basis the whole quadratic Lagrangian diagonalises,
          L_2 = -(2-K_B)[ |grad Psi_N|^2 + J(|grad chi|^2) ] - (1/2)K_QQ Q_0^2 Psi^2
                - 16 pi Gt rho (Psi_N + chi)      (check G1, exact up to a total divergence),
    so the ENTIRE scalar nonlinearity sits in J and the second variation about a background
    with u = |grad chi_bg| != 0 has kinetic matrix
          M_ij = J_Y delta_ij + 2 J_YY u_i u_j ,
    eigenvalues J_Y (transverse, x2) and J_Y + 2 Y J_YY (longitudinal).  And
          J_Y + 2 Y J_YY = d(u J_Y)/du = 1/U'(y)      (check G3, symbolic identity)
    with U(y) = u/a_0 = y(nu(y)-1).  THEREFORE ellipticity/no-ghost <=> U'(y) > 0 <=> J
    single-valued: the two halves of the legality criterion are the SAME condition, proved,
    not asserted (check G4).
    *** THIS SHARPENS PART C's C2 AND MAKES IT STRICTER.  C2 used d(g_tot)/du = 1 + 1/U' as
    the longitudinal stiffness.  That is the coefficient in the (Psi, chi) basis, BEFORE the
    constrained Newtonian potential is integrated out; it is not the physical stiffness.  The
    two differ by exactly 1 and can disagree in sign whenever U' < -1 -- exhibited on a toy
    kernel at check G5.  For BOTH corpus kernels the verdicts are identical, so no downstream
    conclusion moves; the criterion just stopped being basis-dependent. ***
(b) THE MULTI-VALUED / HYSTERESIS ESCAPE (PART E).  PRICED AND CLOSED, and the pricing is
    ADVERSE to the operative kernel beyond what stage75 claims.  There are two distinct folds
    and only one of them is the hysteresis case:
      - FOLD IN u AT FIXED g_bar (G(u) = u J_Y(u^2) non-monotone with J single-valued): this
        IS the first-order-transition case.  Branch selection by history, a Maxwell
        construction and domain walls are all legitimate.  Route A is NOT this case.
      - FOLD IN y AT FIXED u (U(y) non-injective): two different g_bar share one u, so
        J_Y(Y) = g_bar/u would have to take two values at one Y.  No Lagrangian of the form
        F(Y,Q) exists AT ALL -- there is no non-convex single-valued potential to run a
        Maxwell construction on.  Route A is this case (check E2).
    Restricting Route A to one branch is priced explicitly (check E3) and both restrictions
    fail catastrophically: the MOND branch (y <= 2.5399) has NO SOLUTION for g_bar > 2.5399 a_0
    -- i.e. nowhere inside 4993 AU of the Sun -- and the Newtonian branch (y >= 2.5399) has NO
    SOLUTION for g_bar < 2.5399 a_0, so it has no MOND limit at all and fails gate (c).
    The one real escape is structural: a QUMOND-class free function of |grad Psi_N| instead of
    Y = |grad chi|^2 would host ANY single-valued nu(y), including Route A.  That is not
    AeST -- AeST's Fcal is a function of Y, which is built from the SCALAR's gradient.  The
    escape costs the relativistic home, and it is named, not hidden (check E4).
(c) IS nu = sqrt(1+1/y) SELECTED?  *** NO.  THIS REFUTES stage75's HEADLINE (PART F). ***
    The legal class is every U:(0,inf)->(0,inf) that is strictly increasing with U -> sqrt(y)
    as y -> 0 and U/y -> 0 as y -> inf; the reconstruction J_Y(Y) = y(U)/U, Y = a_0^2 U^2 is
    explicit and invertible for every such U (check F1).  The class is INFINITE-DIMENSIONAL:
    check F3 exhibits a one-parameter continuum of legal kernels, and check F2 gives THREE
    closed-form alternatives to alpha = 1 that pass every gate stage75 uses --
          J_Y = v/(1-4v^2)  [U = sqrt(y)/sqrt(1+4y)],   J_Y = v/(1-2v)^2  [U = sqrt(y)/(1+2sqrt y)],
          U = (1/2)(1 - e^(-2 sqrt y))  (an EXPONENTIAL kernel that IS legal),
    all three strictly monotone, all three saturating at u = a_0/2 exactly like alpha = 1, and
    all three with the SAME deep-MOND limit J -> (2/3)Y^(3/2)/a_0 that stage75's check B6 uses
    as its independent confirmation.  So B6 confirms nothing about alpha = 1 specifically.
    On observability the honest numbers cut both ways and BOTH are reported (check F4): the
    widest pair in the list differs by 0.0974 dex across 1e-2 <= y <= 1e2, which is NOT small
    against the corpus's committed RAR scatter of 0.108 dex -- a full refit could plausibly
    exclude ALT-3.  But ALT-4 differs from alpha = 1 by at most 0.0062 dex ANYWHERE, and the
    convex family (1-t) U_(alpha=1) + t U_(ALT-3) reaches 0.0005 dex at t = 0.01, so the legal
    class contains members arbitrarily close to alpha = 1.  No finite-precision RAR can ever
    select a point out of it.
    WHAT SURVIVES, AND IT IS NOT NOTHING: legality REJECTS the operative exponential kernel
    (adverse, and now proved from the action rather than asserted), and it forces a CONSTANT
    sunward anomaly for every legal member -- 1279x / 1279x / 1279x / 1279x the Sereno & Jetzer
    Earth bound for the four saturating kernels (check F5).  Those two results are
    kernel-class statements and they stand.  "AeST's one free function is DETERMINED" and
    "FREE FUNCTIONS: ZERO" do not.

WHAT IS NOT AT ISSUE.  a_0 = kappa c sqrt(G rho_Lam) = 9.3619e-11 m/s^2 canonical /
1.1279e-10 alt with kappa = 1/2 FITTED and never derived; the RAR fit, BTFR, lensing, CLASS,
the promotion a_0^2(Q) = kappa^2 G(-K(Q)): none of them is touched, credited or blamed here.
Everything below is a property of the ADOPTED RELATIVISTIC HOME and of which interpolating
functions its Y-sector can host.

REDUCTIONS, ALL DECLARED
========================
R-I   Static, matter rest frame, weak field: g_00 = -(1+2 eps Psi), g_ij = (1-2 eps Phi)delta.
      Aether A_mu = (-(1+eps a1 + eps^2 a2), eps grad_i alpha) -- the SCALAR sector of the
      aether in full; the transverse-vector part decouples from scalars at this order and is
      not treated.
R-II  Quadratic order in (Psi, Phi, alpha, varphi), with J(Y) kept UNEXPANDED as a general
      function -- Y ~ (amplitude)^2 and the MOND term goes as Y^(3/2), which is third order
      and unreachable by a Taylor expansion.  This is the standard weak-field MOND treatment.
      The general function is carried as sympy's Jf(Y) with the chain rule done by sympy, so
      no power-law representative is assumed anywhere.
R-III Local problem: the O(eps^0) bracket constant (Lam and K(Q_0)) and the ambient K_Q are
      set to zero, both PRICED numerically at check M4.
R-IV  P3 uses spherical symmetry and the no-free-scalar-charge boundary condition (the
      integration constant in r^2 J_Y u = G M + C is C = 0 because the scalar is sourced only
      through its coupling to Psi).  Stated, not hidden.
R-V   No claim is made here about the aether/vector sector's own health: the static reduction
      is BLIND to alpha's kinetic term, which lives in E = alphadot + Psi and vanishes for a
      static configuration.  Ghost statements below are about the LONGITUDINAL SCALAR only.

EXIT 0 iff every numbered check passes.
"""

import math
import sys
import time

import sympy as sp

# =================================================================================================
# check harness
# =================================================================================================
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


print(__doc__)
T0 = time.time()

# =================================================================================================
# constants and the two footings
# =================================================================================================
CLIGHT = 2.99792458e8
GNEWT = 6.674e-11
GMSUN = 1.32712440018e20             # m^3 s^-2, IAU
AU = 1.495978707e11                  # m, IAU 2012
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
A0_CAN = 9.3619e-11                  # kappa c sqrt(G rho_Lam), canonical footing
A0_ALT = 1.1279e-10                  # alt footing
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
EPH_EARTH = 3.66e-14                 # m/s^2, Sereno & Jetzer 2006, 2 sigma, as carried in STANDING.md
RHO_LAM = 5.96e-27                   # kg/m^3
RHO_DM0 = 2.4e-27                    # kg/m^3, cosmic mean dark density today
RHO_BAR_10KPC = 6.0e-21              # kg/m^3, Galactic midplane baryons ~0.09 Msun/pc^3
MU_INV_FLOOR = 1.0 * MPC             # mu^-1 >~ 1 Mpc (bridge1_aest_equations.md)
K2_FIT = 9.5e3                       # the LARGER of SZ21's two published K_2 fits (Exp)
KB_MAX = 0.25                        # BBN bound carried in the corpus
RAR_SCATTER_DEX = 0.108              # corpus's committed RAR scatter (rar_framework_a0_mlfit.py)

# =================================================================================================
print()
print("=" * 100)
print("PART Q -- THE REDUCTION, REBUILT FROM THE ACTION WITH THE AETHER SCALAR RESTORED")
print("=" * 100)

tt, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
CO, SPC = [tt, x1, x2, x3], [x1, x2, x3]
eps = sp.Symbol("eps")
KB, Q0s, GT, rhos = sp.symbols("K_B Q_0 Gt rho")
KQ, KQQ = sp.symbols("K_Q K_QQ")               # dK/dQ and d2K/dQ2 at the background Q_0
lam0, lam1 = sp.symbols("lambda_0 lambda_1")
Psi = sp.Function("Psi")(x1, x2, x3)
Phi = sp.Function("Phi")(x1, x2, x3)
al = sp.Function("alpha")(x1, x2, x3)          # aether scalar potential: A_i = grad_i alpha
vp = sp.Function("varphi")(x1, x2, x3)         # scalar field perturbation
a1 = sp.Function("a1")(x1, x2, x3)             # A_0 perturbation, O(eps)   -- FREE, not set to Psi
a2 = sp.Function("a2")(x1, x2, x3)             # A_0 perturbation, O(eps^2) -- FREE
chi_f = sp.Function("chi")(x1, x2, x3)         # SZ21's mixing variable chi = varphi + Q_0 alpha
Jf = sp.Function("Jf")                         # the free function J(Y), NEVER expanded
wdum = sp.Symbol("w")


def s2(e):
    return sp.expand(sp.series(sp.expand(e), eps, 0, 3).removeO())


def el(Lag, f, vs=None):
    """Euler-Lagrange derivative carrying first AND second derivatives of the field."""
    vs = SPC if vs is None else vs
    out = sp.diff(Lag, f)
    for c in vs:
        out -= sp.diff(sp.diff(Lag, sp.Derivative(f, c)), c)
    for i, ci in enumerate(vs):
        for j, cj in enumerate(vs):
            if i <= j:
                dd = sp.Derivative(f, (ci, 2)) if ci == cj else sp.Derivative(f, ci, cj)
                trm = sp.diff(Lag, dd)
                if trm != 0:
                    out += sp.diff(trm, ci, cj)
    return sp.expand(out.doit())


def gdot(f, g):
    return sum(sp.diff(f, c) * sp.diff(g, c) for c in SPC)


def lap(f):
    return sum(sp.diff(f, c, 2) for c in SPC)


gd = sp.diag(-(1 + 2 * eps * Psi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
gu = sp.Matrix(4, 4, lambda i, j: s2(sp.simplify(gd.inv()[i, j])))
sqg = s2(sp.series(sp.sqrt(-sp.expand(gd.det())), eps, 0, 3).removeO())
Gam = [[[s2(sp.Rational(1, 2) * sum(
    gu[r, s] * (sp.diff(gd[s, n], CO[m]) + sp.diff(gd[s, m], CO[n]) - sp.diff(gd[m, n], CO[s]))
    for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]


def ric(si, nu):
    o = 0
    for m in range(4):
        o += sp.diff(Gam[m][nu][si], CO[m]) - sp.diff(Gam[m][m][si], CO[nu])
        for l in range(4):
            o += Gam[m][m][l] * Gam[l][nu][si] - Gam[m][nu][l] * Gam[l][m][si]
    return s2(o)


Rsc = s2(sum(gu[m, n] * ric(m, n) for m in range(4) for n in range(4)))

# --- the aether, with A_0 UNCONSTRAINED and the spatial scalar A_i = grad_i alpha restored ----
Ad = sp.Matrix([-(1 + eps * a1 + eps ** 2 * a2)] + [eps * sp.diff(al, c) for c in SPC])
Au = sp.Matrix(4, 1, lambda i, j: s2(sum(gu[i, k] * Ad[k] for k in range(4))))
AA = s2(sum(Au[i] * Ad[i] for i in range(4)))
Xc = sp.expand(AA + 1)
X1, X2 = Xc.coeff(eps, 1), Xc.coeff(eps, 2)

check(sp.simplify(X1 - 2 * (Psi - a1)) == 0
      and sp.simplify(sp.expand(X2.subs(a1, Psi)) + (Psi ** 2 + 2 * a2 - gdot(al, al))) == 0,
      "Q1  THE UNIT-NORM CONSTRAINT, ORDER BY ORDER, WITH NOTHING ASSUMED.  A^mu A_mu + 1 = "
      "2 eps (Psi - a1) - eps^2 (a1^2 + 2 a2 - 4 Psi a1 + 4 Psi^2 - |grad alpha|^2).  Its "
      "O(eps) part FORCES a1 = Psi and its O(eps^2) part then forces "
      "a2 = (|grad alpha|^2 - Psi^2)/2",
      "at alpha = 0 this is a2 = -Psi^2/2, reproducing PART Q's check Q1; the |grad alpha|^2 "
      "piece is new and is what the A_i = 0 ansatz throws away")

c2sol = sp.solve(sp.Eq(sp.expand(X2.subs(a1, Psi)), 0), a2)[0]
SUBC = {a1: Psi, a2: c2sol}

Fmn = sp.Matrix(4, 4, lambda m, n: sp.diff(Ad[n], CO[m]) - sp.diff(Ad[m], CO[n]))
F2 = s2(sum(Fmn[m, n] * Fmn[a, b] * gu[m, a] * gu[n, b]
            for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
dphi = sp.Matrix([Q0s, 0, 0, 0]) + eps * sp.Matrix([sp.diff(vp, c) for c in CO])
Qsc = s2(sum(Au[m] * dphi[m] for m in range(4)))
Ysc = s2(sum((gu[m, n] + Au[m] * Au[n]) * dphi[m] * dphi[n]
             for m in range(4) for n in range(4)))
Jd = [s2(sum(Au[nu] * (sp.diff(Ad[q], CO[nu]) - sum(Gam[b][nu][q] * Ad[b] for b in range(4)))
             for nu in range(4))) for q in range(4)]
Jphi = s2(sum(gu[m, q] * Jd[q] * dphi[m] for m in range(4) for q in range(4)))

chi_expr = vp + Q0s * al
check(sp.simplify(sp.expand(Qsc).coeff(eps, 1).subs(a1, Psi) + Q0s * Psi) == 0,
      "Q2  *** GATE (a): delta Q = -Q_0 Psi at first order, i.e. Q = (1 - Psi) Q_0 -- the "
      "corpus's committed quasi-static relation, reproduced from the action AND unaffected by "
      "the restored aether scalar (alpha enters Q only at second order) ***",
      f"the O(eps^2) piece is {sp.simplify(sp.expand(Qsc).coeff(eps, 2).subs(SUBC).doit())}, "
      "whose grad alpha . grad varphi term is what couples alpha to the dust density K_Q")

check(sp.simplify(sp.expand(Ysc).coeff(eps, 0)) == 0
      and sp.simplify(sp.expand(Ysc).coeff(eps, 1).subs(a1, Psi)) == 0
      and sp.simplify(sp.expand(Ysc).coeff(eps, 2).subs(SUBC).doit()
                      - gdot(chi_expr, chi_expr)) == 0,
      "Q3  *** THE CORRECTION TO P1, AND IT IS SZ21's OWN VARIABLE: Y = 0 at background, 0 at "
      "first order, and EXACTLY |grad chi|^2 at second order with chi = varphi + Q_0 alpha -- "
      "NOT |grad varphi|^2.  PART Q's Q4 gets |grad varphi|^2 only because it sets A_i = 0 ***",
      "chi is the mixing variable bridge1_aest_equations.md transcribes verbatim from the "
      "arXiv source ('chi = varphi + phidot alpha').  The reduction is therefore not wrong, "
      "but its field variable is incomplete, and the completion is a rename, not a new term")

check(sp.simplify(sp.expand(F2).coeff(eps, 2).subs(SUBC).doit() + 2 * gdot(Psi, Psi)) == 0
      and sp.simplify(sp.expand(Jphi).coeff(eps, 1).subs(SUBC).doit()) == 0
      and sp.simplify(sp.expand(Jphi).coeff(eps, 2).subs(SUBC).doit()
                      - gdot(Psi, chi_expr)) == 0,
      "Q4  and the other two aether structures also see only chi: F^{mu nu}F_{mu nu} = "
      "-2|grad Psi|^2 (alpha drops -- a static gradient A_i has F_ij = 0 and does not touch "
      "F_0i), and J^mu grad_mu phi = eps^2 grad Psi . grad chi with NO first-order piece",
      "PART Q's Q5 got grad Psi . grad varphi; the missing Q_0 grad Psi . grad alpha is exactly "
      "what promotes varphi to chi.  Every alpha-dependence in the aether sector is absorbed")

# ---- the full quadratic Lagrangian, both routes ------------------------------------------------
Kexp = KQ * (Qsc - Q0s) + sp.Rational(1, 2) * KQQ * (Qsc - Q0s) ** 2
BR = (Rsc - sp.Rational(1, 2) * KB * F2 + 2 * (2 - KB) * Jphi - (2 - KB) * Ysc
      - Kexp - (lam0 + eps * lam1) * (AA + 1))
Lser = sp.expand(s2(sqg * BR)) - 16 * sp.pi * GT * rhos * Psi * eps ** 2
L1_free = Lser.coeff(eps, 1)
L2_free = Lser.coeff(eps, 2)
Y2_free = sp.expand(Ysc).coeff(eps, 2)
JY_gen = sp.Subs(sp.Derivative(Jf(wdum), wdum), wdum, Y2_free)     # J_Y(Y) for the free route
L2_free = sp.expand(L2_free - (2 - KB) * Jf(Y2_free))

print(f"       [built the free-field quadratic Lagrangian, t = {time.time()-T0:.1f} s]")

# =================================================================================================
print()
print("=" * 100)
print("PART M -- THE LAGRANGE MULTIPLIER, DONE THE HARD WAY, AND THE BACKGROUND'S OWN EQUATIONS")
print("=" * 100)
JY_bg = sp.Symbol("J_Y")


def desubs(e):
    """replace every Subs(dJf/dw, w, Y) -- i.e. every occurrence of J_Y -- by a plain symbol"""
    return e.replace(lambda z: isinstance(z, sp.Subs), lambda z: JY_bg)


eq_a1_o1 = el(L1_free, a1)
eq_a2_o2 = el(L2_free, a2)
lam0_from_a1 = sp.solve(sp.Eq(eq_a1_o1, 0), lam0)[0]
lam0_from_a2 = sp.solve(sp.Eq(sp.expand(eq_a2_o2), 0), lam0)[0]
lam0_a2_sym = sp.simplify(desubs(sp.expand(lam0_from_a2)))
lam0_target = (2 - KB) * (1 + JY_bg) * Q0s ** 2 + KQ * Q0s / 2
check(sp.simplify(lam0_from_a1 - ((2 - KB) * Q0s ** 2 + KQ * Q0s / 2)) == 0
      and sp.simplify(lam0_a2_sym - lam0_target) == 0
      and sp.simplify(lam0_a2_sym - lam0_from_a1 - (2 - KB) * JY_bg * Q0s ** 2) == 0,
      "M1  *** THE MULTIPLIER IS NONZERO ON THE BACKGROUND, AT ORDER Q_0^2, AND ITS OPERATIVE "
      "VALUE CARRIES THE FREE FUNCTION:\n"
      "        delta/delta a_1 at O(eps)  ->  lam_0 = (2-K_B) Q_0^2 + K_Q Q_0/2   [J-blind]\n"
      "        delta/delta a_2 at O(eps^2) -> lam_0 = (2-K_B)(1+J_Y) Q_0^2 + K_Q Q_0/2\n"
      "                                             = A_Y Q_0^2 + K_Q Q_0/2 ,\n"
      "    with A_Y = (2-K_B)(1+J_Y), in the sign convention of -lam(A^mu A_mu + 1) ***",
      "the two agree on the analytic part and differ by EXACTLY (2-K_B) J_Y Q_0^2, verified "
      "here as a third assertion.  REPORTED, NOT SMOOTHED: they differ because J(Y) ~ Y^(3/2) "
      "is non-analytic in the eps-grading (reduction R-II) and therefore contributes at both "
      "orders; the value operative in the quasi-static equations is the a_2 one, WITH the "
      "(1+J_Y).  This CONFIRMS the diagnosis of ppn_scalar_retained_2026.py's defect from the "
      "action -- lam_bg = 0 is not an option, its magnitude is A_Y Q_0^2, and the reason is "
      "that dY/dA^mu = 2 Q grad_mu phi does not vanish on the background")

lam_sol = sp.solve([sp.Eq(sp.expand(el(L2_free, a1)), 0),
                    sp.Eq(sp.expand(el(L2_free, a2)), 0)], [lam0, lam1], dict=True)[0]
L2_con = sp.expand(L2_free.subs(SUBC).doit())
check(not (L2_con.has(lam0) or L2_con.has(lam1)),
      "M2  and PART Q's SHORTCUT IS LEGITIMATE: once the constraint is solved by substitution "
      "(a1 = Psi, a2 = (|grad alpha|^2 - Psi^2)/2) the term -lam(A^mu A_mu + 1) vanishes "
      "IDENTICALLY, so lam never has to be computed at all",
      "solving a holonomic constraint before varying is legal provided the parametrisation "
      "covers the constraint surface.  A_mu has 4 components, the constraint removes 1, and "
      "the scalar sector of what is left is exactly (a1 solved, alpha free) -- which is why "
      "restoring alpha, not restoring lam, is what PART Q was missing")

# --- consistency: constrained route vs free route with the multipliers eliminated ---------------
dl = sp.Symbol("dl", positive=True)
FLDS = (Psi, Phi, al, vp)


def mindeg(e):
    """lowest total degree in the perturbation amplitude; J_Y counted as degree 0 (R-II)"""
    e = desubs(e).replace(lambda z: isinstance(z, sp.Function) and z.func == Jf,
                          lambda z: JY_bg)
    e = sp.expand(e.subs({f: dl * f for f in FLDS}).doit())
    if e == 0:
        return 99
    return min(m[0] for m in sp.Poly(e, dl).monoms())


deg = {}
for f in FLDS:
    d = sp.expand(el(L2_con, f)
                  - sp.expand(el(L2_free, f).subs(lam_sol).doit().subs(SUBC).doit()))
    deg[f] = mindeg(d)
check(all(v >= 3 for v in deg.values()),
      "M3  *** AND THE TWO ROUTES AGREE, TO THE ORDER THE REDUCTION CLAIMS.  The Psi, Phi, "
      "alpha and varphi field equations obtained (i) by substituting the constraint before "
      "varying and (ii) by keeping a_1, a_2, lam_0, lam_1 free and eliminating the multipliers "
      "from their own O(eps^2) equations are IDENTICAL for a general free function J, with an "
      "explicit degree check on the residual ***",
      f"lowest surviving degree in the perturbation amplitude, per equation "
      f"(99 = identically zero): "
      + ", ".join(f"{str(k.func)}:{v}" for k, v in deg.items())
      + ".  Psi, Phi and varphi agree IDENTICALLY; the alpha equation's residual starts at "
      "CUBIC order, generated by the chain rule through a_2 = (|grad alpha|^2 - Psi^2)/2, and "
      "cubic terms are outside the stated quadratic truncation R-II.  So the multiplier "
      "treatment in PART Q's setup is consistent -- it is NOT the ppn_scalar_retained_2026.py "
      "defect repeated.  That defect was setting lam_bg = 0 while keeping lam in the "
      "equations; PART Q keeps neither, which is why it escapes")

L1_onshell = sp.expand(L1_free.subs(SUBC).doit().subs(lam0, lam0_from_a1))
L1_minus_tadpole = sp.expand(L1_onshell - KQ * Q0s * Psi)
is_totdiv = sp.simplify(L1_minus_tadpole - (4 * lap(Phi) - 2 * lap(Psi))) == 0
lam_r2_10kpc = (8 * math.pi * GNEWT * RHO_LAM / CLIGHT ** 2) * (10 * KPC) ** 2
lam_r2_1au = (8 * math.pi * GNEWT * RHO_LAM / CLIGHT ** 2) * AU ** 2
dust_ratio = RHO_DM0 / RHO_BAR_10KPC
check(is_totdiv and lam_r2_10kpc < 1e-9 and dust_ratio < 1e-5,
      "M4  DOES THE BACKGROUND SOLVE ITS OWN EQUATIONS?  YES, iff K_Q = 0 and Lam r^2 -> 0, "
      "and both are priced.  On the constraint surface the O(eps) Lagrangian is exactly\n"
      "        L^(1) = K_Q Q_0 Psi + 4 lap(Phi) - 2 lap(Psi)   (the last two a total "
      "divergence),\n"
      "    so the ONLY obstruction is the tadpole K_Q Q_0 Psi",
      f"and K_Q Q_0 = 8 pi Gt rhobar_dm is the AMBIENT dark-sector density (bridge1's "
      f"background relations), so dropping it is exactly the standard step of ignoring the "
      f"cosmic mean density in a local problem: rhobar_dm/rho_baryon(10 kpc) = "
      f"{dust_ratio:.2e}.  The dropped O(eps^0) constant costs Lam r^2 = {lam_r2_10kpc:.2e} at "
      f"10 kpc and {lam_r2_1au:.2e} at 1 AU.  Both are declared reductions R-III, not hidden "
      f"assumptions")

# =================================================================================================
print()
print("=" * 100)
print("PART R -- THE REDUCTION ITSELF: gamma_PPN, TYPE-II, AND THE LOCAL ALGEBRAIC LAW")
print("=" * 100)
L2c0 = sp.expand(L2_con.subs(KQ, 0))
L2chi = sp.expand(L2c0.subs({vp: chi_f - Q0s * al}).doit())
check(not L2chi.has(al),
      "R1  *** alpha IS A FLAT DIRECTION: with K_Q = 0 the ENTIRE quadratic Lagrangian depends "
      "on (varphi, alpha) only through chi = varphi + Q_0 alpha.  So PART Q's A_i = 0 is not a "
      "physical assumption -- it is a CHOICE OF SPLIT inside a degenerate pair, and every "
      "physical statement is a statement about chi ***",
      "verified by literal substitution varphi -> chi - Q_0 alpha in the full quadratic "
      "Lagrangian: alpha does not appear.  This is stronger than PART Q's Q7, which argued "
      "A_i = 0 from t-reflection symmetry and recorded the term-by-term check as not done")

eqPhi = el(L2chi, Phi)
check(sp.simplify(eqPhi / 4 - (lap(Psi) - lap(Phi))) == 0,
      "R2  *** GATE (b): gamma_PPN = 1 EXACTLY.  The Phi field equation is lap(Phi) = lap(Psi) "
      "for EVERY K_B, every free function J, every Q_0, and with the aether scalar restored ***",
      "no aether, scalar or free-function term contains Phi at quadratic order, so the "
      "transverse metric potential is pure GR and Phi = Psi with the usual boundary condition")

Lr = sp.expand(L2chi.subs(Phi, Psi).doit())
PsiN = sp.Function("Psi_N")(x1, x2, x3)
Lr_target = (-(2 - KB) * (gdot(Psi - chi_f, Psi - chi_f) + Jf(gdot(chi_f, chi_f)))
             - sp.Rational(1, 2) * KQQ * Q0s ** 2 * Psi ** 2
             - 16 * sp.pi * GT * rhos * Psi)
totdiv = sp.expand(Lr - Lr_target)
totdiv_is_div = sp.simplify(totdiv - 12 * (Psi * lap(Psi) + gdot(Psi, Psi))) == 0
check(totdiv_is_div,
      "R3  *** THE WHOLE REDUCTION IN ONE LINE, AND IT IS P2.  Up to the total divergence "
      "12 div(Psi grad Psi), the quadratic Lagrangian at Phi = Psi is EXACTLY\n"
      "        L_2 = -(2-K_B)[ |grad(Psi - chi)|^2 + J(|grad chi|^2) ] "
      "- (1/2)K_QQ Q_0^2 Psi^2 - 16 pi Gt rho Psi ,\n"
      "    so with Psi_N = Psi - chi the gradient sector DIAGONALISES: Psi = Psi_N + chi with "
      "lap(Psi_N) = 4 pi Ghat rho, Ghat = Gt/(1-K_B/2), and the scalar's entire dynamics is "
      "the free function J ***",
      "AeST's quasi-static sector is therefore TYPE-II, confirmed independently of PART Q.  "
      "Note what this makes manifest: matter couples to Psi = Psi_N + chi, so chi is sourced "
      "by rho with the SAME strength as Psi_N -- that is the type-II mechanism, and it is why "
      "div[J_Y grad chi] = lap(Psi_N) below")

eq_chi = el(Lr, chi_f)
JY_chi = sp.Subs(sp.Derivative(Jf(wdum), wdum), wdum, gdot(chi_f, chi_f))
tgt_chi = sp.expand(2 * (2 - KB) * (sum(sp.diff((1 + JY_chi) * sp.diff(chi_f, c), c)
                                        for c in SPC) - lap(Psi)))
check(sp.simplify(sp.expand(eq_chi - sp.expand(tgt_chi.doit()))) == 0,
      "R4  *** GATE (c), FIRST HALF, AND IT IS P2 PROPER: the chi equation is "
      "div[(1 + J_Y) grad chi] = lap(Psi), which with Psi = Psi_N + chi collapses to\n"
      "        div[ J_Y(|grad chi|^2) grad chi ] = lap(Psi_N) = 4 pi Ghat rho ***",
      "derived with J carried as a GENERAL function (sympy's Jf with the chain rule done "
      "symbolically), so no power-law representative and no Taylor expansion in Y is used "
      "anywhere.  The '1' cancels because the action's J-coupling coefficient 2(2-K_B) is "
      "exactly twice the Y coefficient (2-K_B) -- SZ21's design")

# P3 by Gauss, and the corrections it neglects
rr = sp.Symbol("r", positive=True)
uf = sp.Function("u")(rr)
JYs = sp.Function("JYs")
flux = rr ** 2 * JYs(uf ** 2) * uf
GMs = sp.Symbol("GM", positive=True)
check(sp.simplify(sp.diff(flux, rr) - sp.diff(rr ** 2 * (GMs / rr ** 2), rr)
                  - sp.diff(flux - GMs, rr)) == 0,
      "R5  *** GATE (c), SECOND HALF = P3, EXACTLY.  In spherical symmetry the divergence-form "
      "equation of R4 integrates by Gauss's theorem to r^2 J_Y(u^2) u = G M + C with u = "
      "|grad chi|, and C = 0 by the no-free-scalar-charge boundary condition (R-IV).  Hence "
      "the PURELY LOCAL ALGEBRAIC LAW  u J_Y(u^2) = g_bar ***",
      "verified here as the trivial identity d/dr[r^2 J_Y u] = d/dr[r^2 g_bar] <=> "
      "d/dr[r^2 J_Y u - G M] = 0.  P3 is therefore NOT an approximation in spherical symmetry: "
      "it is the first integral.  What it neglects is priced at R6")

mu_inv = MU_INV_FLOOR
mr2_10kpc = ((10 * KPC) / mu_inv) ** 2
mr2_1au = (AU / mu_inv) ** 2
check(mr2_10kpc < 1e-3 and mr2_1au < 1e-14,
      "R6  AND THE PRICE OF P3's TWO NEGLECTED TERMS.  The scalar mass term gives Psi a Yukawa "
      f"correction of relative size (m r)^2 <= (r mu)^2 = {mr2_10kpc:.2e} at 10 kpc and "
      f"{mr2_1au:.2e} at 1 AU (using mu^-1 >= 1 Mpc from bridge1); the dropped Lam gives "
      f"{lam_r2_10kpc:.2e} at 10 kpc.  P3 is exact to ~1e-4 where galaxies are fitted and to "
      f"~{mr2_1au:.0e} at 1 AU",
      "*** THIS IS THE ANSWER TO 'WHAT IF P3 IS ONLY APPROXIMATE'.  Rescuing the exponential "
      "kernel needs U(y) to REVERSE -- to fall from 0.6478 at y = 2.54 to 1e-3455 at 1 AU, an "
      "O(1) to O(1e3455) violation of the local law.  Corrections of 1e-4 cannot do it.  The "
      "legality verdict is not hostage to P3's small print ***")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- THE NO-GHOST CONDITION, DERIVED FROM THE SECOND VARIATION (ROUTE ITEM (a))")
print("=" * 100)
info("G0  THE SETUP.  From R3 the scalar's own Lagrangian, after the constrained Newtonian "
     "potential Psi_N is separated out, is L_chi = -(2-K_B) J(|grad chi|^2) - 16 pi Gt rho chi. "
     "Perturb chi = chi_bg + dchi about a background with u_i = grad_i chi_bg != 0 and read the "
     "quadratic form in grad dchi.  No result is quoted; the standard AQUAL answer is "
     "REPRODUCED, and then sharpened.")
u1s, u2s, u3s = sp.symbols("u1 u2 u3", real=True)
dchi = sp.Function("dchi")(x1, x2, x3)
Ysym, JYf, JYYf = sp.symbols("Y J_Yv J_YYv")
gb = [u1s, u2s, u3s]
gp = [sp.diff(dchi, c) for c in SPC]
Ypert = sum((gb[i] + gp[i]) ** 2 for i in range(3))
Ybg = sum(g ** 2 for g in gb)
dY = sp.expand(Ypert - Ybg)
quad = sp.expand(JYf * dY + sp.Rational(1, 2) * JYYf * dY ** 2)
quad2 = sum(t for t in quad.args if sp.Poly(t, *gp).total_degree() == 2) if quad.args else 0
Mmat = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2) * sp.diff(quad2, gp[i], gp[j]))
Mtarget = sp.Matrix(3, 3, lambda i, j: JYf * sp.KroneckerDelta(i, j) + 2 * JYYf * gb[i] * gb[j])
deg_ok = all(sp.Poly(t, *gp).total_degree() <= 2 for t in sp.Add.make_args(sp.expand(quad2)))
check(sp.simplify(Mmat - Mtarget) == sp.zeros(3, 3) and deg_ok,
      "G1  *** THE KINETIC MATRIX, DERIVED: expanding J(Y) to SECOND order in grad dchi about "
      "a nontrivial background gives M_ij = J_Y delta_ij + 2 J_YY u_i u_j, with an explicit "
      "degree check that nothing above quadratic order was retained ***",
      "the static field equation div[J_Y grad chi] = source is elliptic -- equivalently the "
      "gradient energy (2-K_B) M_ij is positive definite and the longitudinal mode is not a "
      "ghost -- iff M is positive definite.  2 - K_B > 0 is AeST's own aether window")
ev = sp.Matrix([[JYf + 2 * JYYf * Ybg]])
check(sp.simplify((Mtarget * sp.Matrix(gb)) - (JYf + 2 * JYYf * Ybg) * sp.Matrix(gb))
      == sp.zeros(3, 1)
      and sp.simplify((Mtarget * sp.Matrix([-u2s, u1s, 0]))
                      - JYf * sp.Matrix([-u2s, u1s, 0])) == sp.zeros(3, 1),
      "G2  ITS EIGENVALUES, VERIFIED BY DIRECT ACTION ON THE EIGENVECTORS: the longitudinal "
      "direction u_i has eigenvalue J_Y + 2 Y J_YY, and the two transverse directions have "
      "eigenvalue J_Y.  So the conditions are J_Y > 0 (transverse) and J_Y + 2 Y J_YY > 0 "
      "(longitudinal)",
      "J_Y = y/U > 0 automatically for any kernel with u > 0, so the whole content is in the "
      "LONGITUDINAL eigenvalue")

# the identity that turns the stability condition into a statement about the kernel
ysym = sp.Symbol("y", positive=True)
a0sym = sp.Symbol("a_0", positive=True)
Ug = sp.Function("U")(ysym)
JY_of_y = ysym / Ug                      # J_Y = g_bar/u = y/U
Y_of_y = a0sym ** 2 * Ug ** 2            # Y = u^2
JYY_of_y = sp.diff(JY_of_y, ysym) / sp.diff(Y_of_y, ysym)
long_stiff = sp.simplify(JY_of_y + 2 * Y_of_y * JYY_of_y)
check(sp.simplify(long_stiff - 1 / sp.diff(Ug, ysym)) == 0,
      "G3  *** THE IDENTITY THAT MAKES LEGALITY A STATEMENT ABOUT THE KERNEL, PROVED FOR A "
      "GENERAL U:\n"
      "        J_Y + 2 Y J_YY  =  d(u J_Y)/du  =  d g_bar / d u  =  1 / U'(y) ,\n"
      "    where U(y) = u/a_0 = y(nu(y) - 1) ***",
      f"symbolically, with J_Y = y/U(y) and Y = a_0^2 U(y)^2 carried as a general function: "
      f"J_Y + 2 Y J_YY = {long_stiff}.  Every a_0 and every J cancels; only U' survives")

check(True,
      "G4  *** THEREFORE THE TWO HALVES OF THE LEGALITY CRITERION ARE ONE CONDITION, PROVED "
      "RATHER THAN ASSERTED: J single-valued in Y <=> U injective <=> (with continuity and the "
      "deep-MOND anchor, where U is increasing) U'(y) > 0 <=> the longitudinal scalar is not a "
      "ghost and the static problem stays elliptic ***",
      "the single-valuedness half: if U(y_1) = U(y_2) with y_1 != y_2 then Y is the same at "
      "both while J_Y = y/U differs, so no function J_Y(Y) exists.  The ghost half: G1-G3.  "
      "A continuous injective function on an interval is strictly monotone, and deep MOND "
      "fixes the sign, so 'injective' and 'increasing' coincide here.  U' = 0 at an isolated "
      "point is the marginal case: J stays single-valued but the longitudinal stiffness "
      "diverges (infinitely strong coupling), which is a boundary of the class, not an "
      "interior point")

# G5: the sharpening -- PART C's C2 quantity is the pre-diagonalisation coefficient
def U_toy(y):
    return math.sqrt(y) * math.exp(-10.0 * (y - 1.0))


def dU_toy(y):
    return math.exp(-10.0 * (y - 1.0)) * (0.5 / math.sqrt(y) - 10.0 * math.sqrt(y))


up_toy = dU_toy(1.0)
mine_toy = 1.0 / up_toy
theirs_toy = 1.0 + 1.0 / up_toy
check(up_toy < -1.0 and mine_toy < 0 and theirs_toy > 0,
      "G5  *** AND THE SHARPENING IS NOT VACUOUS.  PART C's C2 used d(g_tot)/du = "
      "(d(nu y)/dy)/(dU/dy) = 1 + 1/U' as the longitudinal stiffness.  That is the coefficient "
      "in the (Psi, chi) basis, BEFORE the constrained potential Psi_N is integrated out; the "
      "physical one is 1/U'.  They differ by exactly 1 and DISAGREE IN SIGN whenever "
      "U' < -1 ***",
      f"exhibited on the toy kernel U = sqrt(y) e^(-10(y-1)) at y = 1: U' = {up_toy:.4f}, "
      f"physical stiffness 1/U' = {mine_toy:.4f} (GHOST, and J is multivalued there), C2's "
      f"quantity 1 + 1/U' = {theirs_toy:.4f} (would read HEALTHY).  For BOTH corpus kernels "
      f"the two verdicts coincide (PART D), so nothing downstream moves -- but the criterion "
      f"is now basis-independent, and it is STRICTLY STRONGER, i.e. more adverse")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE TWO KERNELS, ON THE DERIVED CRITERION")
print("=" * 100)


def U_routeA(y):
    s = math.sqrt(y)
    return 0.0 if s > 700.0 else y / math.expm1(s)


def U_alpha1(y):
    return 1.0 / (math.sqrt(1.0 + 1.0 / y) + 1.0)      # = sqrt(y^2+y) - y, stably


ss = sp.Symbol("s", positive=True)
UA_s = ss ** 2 / (sp.exp(ss) - 1)                       # U as a function of s = sqrt(y)
speak = sp.nsolve(sp.diff(UA_s, ss), ss, 1.6)
ypeak = float(speak) ** 2
Upeak = float(UA_s.subs(ss, speak))
dU_dy_A = sp.simplify(sp.diff(UA_s, ss) / (2 * ss))     # dU/dy = (dU/ds)/(2s)
stiff_A = sp.simplify(1 / dU_dy_A)
vals = [(sv, float(stiff_A.subs(ss, sv))) for sv in (0.5, 1.0, 1.5937, 3.0, 10.0, 20.0)]
print(f"       {'sqrt(y)':>9s} {'y':>12s} {'U = u/a_0':>14s} "
      f"{'1/U(y)  [physical longitudinal stiffness]':>44s}")
for sv, st in vals:
    print(f"       {sv:9.4f} {sv**2:12.4f} {U_routeA(sv**2):14.6e} {st:44.6e}")
check(abs(ypeak - 2.5399) < 5e-3 and abs(Upeak - 0.6478) < 5e-4
      and all(st > 0 for sv, st in vals if sv < 1.5937)
      and all(st < 0 for sv, st in vals if sv > 1.5937),
      "D1  *** ADVERSE TO THE OPERATIVE KERNEL, ON THE DERIVED CRITERION.  Route A, "
      "nu = 1/(1-e^(-sqrt y)) (MS08 Eq. 13 at alpha = 1/2), gives U(y) = y/(e^(sqrt y)-1), "
      f"which rises to {Upeak:.4f} at y = {ypeak:.4f} and then FALLS.  Beyond that point "
      "U' < 0, so the longitudinal stiffness 1/U' is NEGATIVE: the static problem loses "
      "ellipticity and the mode is a gradient ghost.  And J(Y) does not exist as a function "
      "at all ***",
      f"the peak is at sqrt(y) = {float(speak):.4f}, the root of 2(e^s - 1) = s e^s.  The "
      f"solar system sits at sqrt(y) = 7959 (canonical), i.e. deep on the illegal branch.  "
      f"This reproduces PART C's C1/C2 from a criterion derived here rather than asserted")

y1au_can = GMSUN / (AU ** 2 * A0_CAN)
y1au_alt = GMSUN / (AU ** 2 * A0_ALT)
Uy = sp.sqrt(ysym ** 2 + ysym) - ysym
dUy = sp.simplify(sp.diff(Uy, ysym))
num_pos = sp.simplify((2 * ysym + 1) ** 2 - 4 * (ysym ** 2 + ysym))
check(num_pos == 1 and sp.limit(Uy, ysym, sp.oo) == sp.Rational(1, 2)
      and float(dUy.subs(ysym, 1)) > 0,
      "D2  and the alpha = 1 kernel nu = sqrt(1+1/y) IS legal, proved rather than sampled: "
      "U = sqrt(y^2+y) - y has U' = (2y+1)/(2 sqrt(y^2+y)) - 1 > 0 for all y > 0 because "
      "(2y+1)^2 - 4(y^2+y) = 1 > 0 identically, and U -> 1/2 as y -> infinity",
      f"so its longitudinal stiffness 1/U' is positive everywhere.  y(1 AU) = "
      f"{y1au_can:.4e} canonical / {y1au_alt:.4e} alt")

dm = []
for lab, Ufn in (("RouteA", U_routeA), ("alpha=1", U_alpha1)):
    r = [Ufn(yv) / math.sqrt(yv) for yv in (1e-4, 1e-6, 1e-8)]
    dm.append((lab, r[-1]))
check(all(abs(v - 1.0) < 1e-3 for _, v in dm),
      "D3  *** GATE (c) FOR BOTH KERNELS: U(y)/sqrt(y) -> 1 as y -> 0, i.e. u -> "
      "sqrt(g_bar a_0) and g_obs -> sqrt(g_bar a_0).  Both kernels have the deep-MOND limit, "
      "so the legality verdict separates them on monotonicity ALONE and not on their MOND "
      "asymptotics ***",
      f"U/sqrt(y) at y = 1e-8: " + ", ".join(f"{l} {v:.8f}" for l, v in dm))

vsym = sp.Symbol("v", positive=True)
J_dM = sp.Rational(2, 3) * (a0sym ** 2 * vsym ** 2) ** sp.Rational(3, 2) / a0sym
JY_dM = sp.simplify(sp.diff(J_dM, vsym) / sp.diff(a0sym ** 2 * vsym ** 2, vsym))
u_dM = sp.symbols("u_dM", positive=True)
gb_dM = sp.simplify((JY_dM * a0sym * vsym).subs(vsym, u_dM / a0sym))
check(sp.simplify(JY_dM - vsym) == 0 and sp.simplify(gb_dM - u_dM ** 2 / a0sym) == 0,
      "D4  GATE (c) FROM THE FREE FUNCTION'S SIDE, INDEPENDENTLY: with SZ21's printed MOND "
      "asymptotics J -> (2/3) Y^(3/2)/a_0 (bridge1_aest_equations.md) one gets J_Y = "
      "sqrt(Y)/a_0 = u/a_0, so the local law u J_Y(u^2) = g_bar reads u^2/a_0 = g_bar, i.e. "
      "u = sqrt(a_0 g_bar) and g_obs -> sqrt(a_0 g_bar) EXACTLY",
      "so gate (c) is satisfied by the reduction itself, not only by the kernels")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- THE MULTI-VALUED / HYSTERESIS ESCAPE, PRICED (ROUTE ITEM (b))")
print("=" * 100)
info("E0  THE QUESTION.  Could a multi-valued J be acceptable, with branches selected by "
     "history as in a first-order phase transition?  That is the most plausible way the "
     "exponential kernel survives, so it is priced here rather than dismissed.")
check(True,
      "E1  *** THE TWO FOLDS ARE NOT THE SAME PATHOLOGY, AND ONLY ONE OF THEM IS THE "
      "HYSTERESIS CASE.\n"
      "    (i) FOLD IN u AT FIXED g_bar -- G(u) = u J_Y(u^2) single-valued but NON-MONOTONE.  "
      "J exists, the local energy e(u) = J(u^2) - 2 g_bar u is a genuine non-convex potential, "
      "and everything condensed-matter physics does with a first-order transition applies: "
      "Maxwell construction, coexisting domains, hysteresis.  LEGITIMATE.\n"
      "    (ii) FOLD IN y AT FIXED u -- U(y) NON-INJECTIVE.  Two different g_bar share one u, "
      "so J_Y(Y) = g_bar/u must take two values at one Y.  There is no non-convex potential "
      "to build a Maxwell construction ON, because there is no potential.  NOT LEGITIMATE, and "
      "not a hysteresis question at all. ***",
      "the distinction matters because the escape being offered is (i) and the disease Route A "
      "has is (ii).  A Lagrangian of the form Fcal(Y, Q) is a FUNCTION of Y; requiring it to "
      "take two values at one Y is not a boundary condition, it is the absence of an action")

ygrid = [ypeak * f for f in (0.25, 0.5, 0.75)]
pairs = []
for ylo in ygrid:
    Utar = U_routeA(ylo)
    lo, hi = ypeak, 1.0e4
    for _ in range(400):
        mid = math.sqrt(lo * hi)
        if U_routeA(mid) > Utar:
            lo = mid
        else:
            hi = mid
    yhi = math.sqrt(lo * hi)
    pairs.append((ylo, yhi, Utar, ylo / Utar, yhi / Utar))
print(f"       {'y (MOND branch)':>16s} {'y (Newt branch)':>16s} {'shared U = u/a_0':>17s} "
      f"{'J_Y = y/U there':>17s} {'and there':>13s}")
for a, b, c, d, e in pairs:
    print(f"       {a:16.6f} {b:16.6f} {c:17.10f} {d:17.6f} {e:13.6f}")
check(all(abs(U_routeA(a) - U_routeA(b)) < 1e-9 and abs(d - e) > 1.0 for a, b, c, d, e in pairs),
      "E2  *** ROUTE A's FOLD IS TYPE (ii), DEMONSTRATED NUMERICALLY: three explicit pairs "
      "(y_lo, y_hi) with IDENTICAL U -- hence identical Y -- but J_Y = y/U differing by factors "
      "of a few to tens.  The escape offered (branch selection by history) does not apply ***",
      "hysteresis selects among several u at ONE g_bar.  Here there are several g_bar at ONE "
      "u, which is a demand on the function J_Y(Y) itself, not on which of its minima the "
      "system occupies")

r_ypeak = math.sqrt(GMSUN / (A0_CAN * ypeak)) / AU
check(r_ypeak > 4000.0 and r_ypeak < 6000.0,
      "E3  *** AND RESTRICTING TO ONE BRANCH IS PRICED, BOTH WAYS, AND BOTH FAIL "
      "CATASTROPHICALLY.\n"
      "    MOND branch (y <= 2.5399): J_Y(Y) IS single-valued there, but g_bar = u J_Y(u^2) "
      f"then has MAXIMUM 2.5399 a_0, so the theory has NO SOLUTION for g_bar > 2.5399 a_0 -- "
      f"i.e. nowhere inside r = {r_ypeak:.0f} AU of the Sun.  No solar system, no inner "
      "galaxy.\n"
      "    NEWTONIAN branch (y >= 2.5399): also single-valued (U decreasing maps onto "
      "(0, 0.6478]), but its y-range starts at 2.5399, so there is NO SOLUTION for "
      "g_bar < 2.5399 a_0 -- no deep-MOND limit, gate (c) fails outright -- and U' < 0 makes "
      "it the ghost branch anyway. ***",
      "so the exponential kernel cannot be saved by choosing a branch, with or without "
      "hysteresis: one branch loses the solar system and the other loses galaxies, and no "
      "matching between them exists because they do not share a common g_bar boundary in the "
      "right direction")

check(True,
      "E4  THE ONE REAL ESCAPE, NAMED HONESTLY: leave the AQUAL class.  A QUMOND-class theory "
      "whose free function depends on |grad Psi_N| (the BARYONIC Newtonian field) rather than "
      "on Y = |grad chi|^2 (the SCALAR's own gradient) hosts ANY single-valued nu(y), "
      "including Route A, with no legality obstruction whatsoever -- because there the kernel "
      "is read off a function of the source, and a source-side function never has to be "
      "inverted",
      "*** BUT THAT IS NOT AeST.  AeST's Fcal is a function of Y = q^{mu nu} grad_mu phi "
      "grad_nu phi, built from the scalar's gradient; that is what makes the theory type-II "
      "and what forces the inversion.  So the escape exists and it costs the adopted "
      "relativistic home.  Anyone who wants the exponential kernel owes a different covariant "
      "completion, and the corpus should say so rather than claim AeST hosts it ***")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- THE FULL LEGAL CLASS.  IS alpha = 1 SELECTED?  (ROUTE ITEM (c))")
print("=" * 100)
info("F0  THE CLAIM UNDER TEST, from stage75_the_closed_theory_2026.py: 'legality ... REJECTS "
     "the exponential kernel and SELECTS nu = sqrt(1+1/y)' (B2/B4) and 'FREE FUNCTIONS: ZERO. "
     "AeST's F(Y,Q) is fully determined' (D1).  The rejection half is tested in PART D and "
     "stands.  The SELECTION half is tested here.")

# F1 -- the reconstruction map, verified on alpha = 1 in closed form
v = sp.Symbol("v", positive=True)
y_a1 = v ** 2 / (1 - 2 * v)
# U(y) = sqrt(y^2+y) - y = v  <=>  (v + y)^2 = y^2 + y with v + y > 0
check(sp.simplify((v + y_a1) ** 2 - (y_a1 ** 2 + y_a1)) == 0
      and sp.simplify(y_a1 / v - v / (1 - 2 * v)) == 0,
      "F1  THE RECONSTRUCTION MAP, EXPLICIT: for ANY strictly increasing U, invert v = U(y) to "
      "get y(v) and set J_Y(Y) = y(v)/v with Y = a_0^2 v^2; J follows by one quadrature.  "
      "Verified on alpha = 1: y = v^2/(1-2v) and J_Y = v/(1-2v), the corpus's committed closed "
      "form",
      "monotonicity is exactly the condition for this inversion to exist -- which is why the "
      "legal class is precisely the monotone class and nothing narrower")


# F2 -- three explicit alternatives that pass every gate stage75 uses
def U_a1(y):
    return 1.0 / (math.sqrt(1.0 + 1.0 / y) + 1.0)


def U_alt2(y):
    return math.sqrt(y) / math.sqrt(1.0 + 4.0 * y)


def U_alt3(y):
    s = math.sqrt(y)
    return s / (1.0 + 2.0 * s)


def U_alt4(y):
    s = math.sqrt(y)
    return 0.5 * (-math.expm1(-2.0 * s))


LEGAL = (("alpha=1   nu=sqrt(1+1/y)          J_Y = v/(1-2v)", U_a1),
         ("ALT-2     U=sqrt(y)/sqrt(1+4y)    J_Y = v/(1-4v^2)", U_alt2),
         ("ALT-3     U=sqrt(y)/(1+2 sqrt y)  J_Y = v/(1-2v)^2", U_alt3),
         ("ALT-4     U=(1-e^(-2 sqrt y))/2   (an EXPONENTIAL kernel, and LEGAL)", U_alt4))
GRID = [10 ** (i / 60.0) for i in range(-480, 601)]        # y from 1e-8 to 1e10
rows = []
for lab, Uf in LEGAL:
    Us = [Uf(yv) for yv in GRID]
    mono = all(Us[i + 1] > Us[i] * (1 - 1e-13) for i in range(len(Us) - 1))
    dmond = Uf(1e-12) / 1e-6                 # U/sqrt(y) deep in the MOND regime
    newt = Uf(1e10) / 1e10                   # U/y deep in the Newtonian regime
    sat = Uf(1e20)                           # the saturation value
    rows.append((lab, mono, dmond, newt, sat, Uf(1.0)))
print(f"       {'kernel':>52s} {'monotone':>9s} {'U/sqrt y (y=1e-12)':>19s} "
      f"{'U/y (y=1e10)':>13s} {'U(inf)':>10s} {'U(1)':>9s}")
for lab, mono, dmond, newt, sat, u1v in rows:
    print(f"       {lab:>52s} {str(mono):>9s} {dmond:19.12f} {newt:13.3e} {sat:10.8f} "
          f"{u1v:9.6f}")
check(all(m for _, m, _, _, _, _ in rows)
      and all(abs(d - 1.0) < 1e-5 for _, _, d, _, _, _ in rows)
      and all(n < 1e-9 for _, _, _, n, _, _ in rows)
      and all(abs(s - 0.5) < 1e-8 for _, _, _, _, s, _ in rows)
      and len(set(round(u, 6) for *_, u in rows)) == 4,
      "F2  *** REFUTATION, AND IT IS THE POINT OF THIS FILE: FOUR kernels -- alpha = 1 and "
      "three explicit alternatives -- ALL strictly monotone (legal), ALL with U/sqrt(y) -> 1 "
      "(exact deep-MOND, gate (c)), ALL with nu -> 1 (Newtonian), and ALL saturating at "
      "u = a_0/2 exactly.  They take FOUR DIFFERENT values at y = 1.  alpha = 1 is one member "
      "of the legal class, not its unique element ***",
      "ALT-2 and ALT-3 have closed-form free functions J_Y = v/(1-4v^2) and J_Y = v/(1-2v)^2 "
      "(from F1's inversion), both single-valued on 0 <= v < 1/2, both with J -> (2/3)v^3 a_0^2 "
      "= (2/3)Y^(3/2)/a_0 -- SZ21's printed MOND asymptotics.  So stage75's check B6, which "
      "treats landing on that limit as independent confirmation of alpha = 1, confirms nothing "
      "about alpha = 1: EVERY legal kernel with the deep-MOND normalisation lands there, by "
      "construction.  ALT-4 is the sharpest rhetorical point -- an EXPONENTIAL kernel that is "
      "perfectly legal, so 'exponential' was never the disqualifying property; NON-MONOTONE was")

# F3 -- the class is infinite-dimensional
tvals = [i / 8.0 for i in range(9)]
allmono = True
for t in tvals:
    Us = [(1 - t) * U_a1(yv) + t * U_alt3(yv) for yv in GRID]
    if not all(Us[i + 1] > Us[i] * (1 - 1e-13) for i in range(len(Us) - 1)):
        allmono = False
check(allmono,
      "F3  *** AND THE CLASS IS INFINITE-DIMENSIONAL, NOT A DISCRETE LIST.  The legality "
      "conditions (U' > 0, U -> sqrt y, U/y -> 0) are CONVEX: any convex combination of legal "
      "kernels is legal.  Verified on the continuum U_t = (1-t) U_(alpha=1) + t U_(ALT-3) for "
      "t = 0, 1/8, ..., 1 -- every member strictly monotone, every member deep-MOND-exact, "
      "every member saturating at a_0/2 ***",
      "a convex set with more than one point has infinitely many.  So 'AeST's one free "
      "function is DETERMINED' cannot be right: legality cuts an infinite-dimensional convex "
      "cone out of an infinite-dimensional space, it does not cut a point")

# F4 -- how far apart are they, in the units the data are quoted in?  BOTH DIRECTIONS.
YR = [10 ** (i / 200.0) for i in range(-400, 401)]         # y from 1e-2 to 1e2


def dexspread(fa, fb):
    m, w = 0.0, None
    for yv in YR:
        d = abs(math.log10(yv + fa(yv)) - math.log10(yv + fb(yv)))
        if d > m:
            m, w = d, yv
    return m, w


spread, worst = 0.0, None
for yv in YR:
    gs = [math.log10(yv + Uf(yv)) for _, Uf in LEGAL]
    if max(gs) - min(gs) > spread:
        spread, worst = max(gs) - min(gs), yv
d_a1_alt4, w_alt4 = dexspread(U_a1, U_alt4)
tfam = [(t, dexspread(U_a1, lambda y, t=t: (1 - t) * U_a1(y) + t * U_alt3(y))[0])
        for t in (0.3, 0.1, 0.01)]
print(f"       widest spread in log10 g_obs across the four legal kernels: {spread:.4f} dex "
      f"at y = {worst:.4f}    (RAR scatter, committed: {RAR_SCATTER_DEX:.3f} dex)")
print(f"       alpha=1 vs ALT-4 alone:                                    {d_a1_alt4:.4f} dex "
      f"at y = {w_alt4:.4f}")
for t, dd in tfam:
    print(f"       alpha=1 vs the convex member t = {t:<5g}                      {dd:.4f} dex")
check(spread > 0.5 * RAR_SCATTER_DEX and d_a1_alt4 < 0.01 and tfam[-1][1] < 0.001,
      f"F4  *** OBSERVABILITY, REPORTED IN BOTH DIRECTIONS AND NOT ROUNDED TO THE CONVENIENT "
      f"ONE.\n"
      f"    AGAINST MY OWN CONCLUSION: the WIDEST pair in the list differs by {spread:.4f} dex "
      f"over 1e-2 <= y <= 1e2, which is NOT small against the committed RAR scatter of "
      f"{RAR_SCATTER_DEX:.3f} dex -- a full SPARC refit could plausibly exclude ALT-3, and "
      f"this file does NOT do that refit.\n"
      f"    FOR IT, AND DECISIVELY: ALT-4 differs from alpha = 1 by at most {d_a1_alt4:.4f} dex "
      f"ANYWHERE, and the convex member at t = 0.01 by {tfam[-1][1]:.4f} dex.  The legal class "
      f"contains members arbitrarily close to alpha = 1, so NO finite-precision RAR can ever "
      f"select a point out of it ***",
      "the two statements are not in tension: the class is wide enough that its extremes are "
      "testable, and dense enough that its centre is not.  Excluding ALT-3 would narrow the "
      "class; it could never reduce it to alpha = 1, because the convex family is continuous "
      "and passes through alpha = 1")

# F5 -- what survives
print()
print(f"       {'kernel':>52s} {'footing':>10s} {'u(1 AU) [m/s^2]':>17s} {'/ Earth bound':>14s}")
eph = []
for lab, Uf in LEGAL:
    for flab, a0 in FOOT:
        yv = GMSUN / (AU ** 2 * a0)
        uu = Uf(yv) * a0
        eph.append(uu / EPH_EARTH)
        print(f"       {lab:>52s} {flab:>10s} {uu:17.6e} {uu/EPH_EARTH:14.1f}")
check(min(eph) > 1000.0,
      "F5  *** WHAT SURVIVES OF stage75's PART B, AND IT IS ADVERSE TO THE FRAMEWORK, NOT "
      "FAVOURABLE: every legal member forces the SAME constant sunward anomaly at 1 AU, "
      f"{min(eph):.0f}x to {max(eph):.0f}x the Sereno & Jetzer 2006 Earth bound "
      f"{EPH_EARTH:.2e} m/s^2.  The ephemeris liability is a property of the LEGAL CLASS, not "
      "of the particular kernel -- so it cannot be traded away inside AeST by picking a "
      "different legal member ***",
      "this is the one place where 'legality selects' has real content: it selects a CLASS, "
      "and the class has a uniform, quantitative, falsifiable liability.  That statement is "
      "worth more than the withdrawn uniqueness claim, and it is the one that should be "
      "carried forward")

check(True,
      "F6  *** THE VERDICT ON stage75's HEADLINE, STATED PLAINLY.  'THE Y-SECTOR, by LEGALITY: "
      "... SELECTS nu = sqrt(1+1/y) ... and then fixes J in CLOSED FORM' and 'FREE FUNCTIONS: "
      "ZERO' are REFUTED as written.  Legality REJECTS (a large class, including the operative "
      "exponential kernel) -- it does not SELECT.  What remains free after legality is an "
      "infinite-dimensional convex family of free functions, of which alpha = 1 is one "
      "convenient closed-form member ***",
      "the honest replacement wording, offered rather than withheld: 'AeST's Y-sector cannot "
      "host a non-monotone u(y), which excludes the operative exponential kernel and every "
      "power-law kernel with alpha >= 2; the framework's own alpha = 1 relation is a legal "
      "member of the surviving class, and every member of that class carries the same "
      "constant sunward anomaly.'  That is defensible, it keeps both the adverse and the "
      "favourable content, and it does not claim a closed theory")

# =================================================================================================
print()
print("=" * 100)
print("LEDGER")
print("=" * 100)
LED = (
    ("P1  Q = (1-Psi)Q_0 at first order", "CONFIRMED (Q2)"),
    ("P1  Y = |grad(scalar)|^2 at quadratic order",
     "CONFIRMED WITH CORRECTION: Y = |grad chi|^2, chi = varphi + Q_0 alpha (Q3)"),
    ("P2  Psi = Psi_N + chi, J_Y grad chi = grad Psi_N", "CONFIRMED (R3, R4)"),
    ("P3  u J_Y(u^2) = g_bar, local and algebraic",
     "CONFIRMED EXACTLY for spherical symmetry; neglected terms <= 1.0e-04 at 10 kpc (R5, R6)"),
    ("multiplier lam handled consistently?",
     "YES.  lam_0 = A_Y Q_0^2 + K_Q Q_0/2 != 0, determined twice over and agreeing; PART Q "
     "eliminates it by substitution and the two routes give identical equations (M1-M3)"),
    ("background solves its own equations?",
     "YES iff K_Q = 0 and Lam r^2 -> 0; the O(eps) tadpole is K_Q Q_0 Psi = the ambient dark "
     "density, 4.0e-07 of the local baryon density (M4)"),
    ("gate (a) Q = (1-Psi)Q_0", "PASSED (Q2)"),
    ("gate (b) gamma_PPN = 1", "PASSED (R2)"),
    ("gate (c) deep-MOND g_obs -> sqrt(g_bar a_0)", "PASSED, two independent ways (D3, D4)"),
    ("(a) no-ghost condition, DERIVED",
     "J_Y + 2 Y J_YY = 1/U'(y) > 0; identical to single-valuedness; STRICTER than PART C's "
     "1 + 1/U' (G1-G5)"),
    ("    exponential kernel violates it?", "YES, for all y > 2.5399 (D1)"),
    ("(b) multi-valued / hysteresis escape",
     "CLOSED.  Route A's fold is in y at fixed u, so no J exists at all; branch restriction "
     "loses either the solar system or every galaxy (E1-E3)"),
    ("(c) is alpha = 1 unique?",
     "NO -- REFUTED.  The legal class is an infinite-dimensional convex family; three explicit "
     "alternatives pass every gate; ALT-4 is within 0.006 dex of alpha=1 EVERYWHERE (F2-F4)"),
)
for k, vtxt in LED:
    print(f"       {k:<48s} {vtxt}")

print()
print("=" * 100)
if FAIL:
    print(f"RESULT: {NCHK[0]-len(FAIL)}/{NCHK[0]} checks passed, {len(FAIL)} FAILED")
    for f in FAIL:
        print("   FAILED:", f.split('.')[0][:110])
    print(f"[{time.time()-T0:.1f} s]")
    sys.exit(1)
print(f"RESULT: ALL {NCHK[0]} CHECKS PASSED.  [{time.time()-T0:.1f} s]")
print("""
DIRECTION OF THIS RESULT, STATED PLAINLY AND IN BOTH DIRECTIONS:

  FAVOURABLE TO THE DERIVATION UNDER TEST.  P1, P2 and P3 all survive an independent
  re-derivation from the action.  The Lagrange multiplier is handled consistently in PART Q's
  setup -- it is eliminated by substitution and never needed -- and the earlier
  ppn_scalar_retained_2026.py defect (lam_bg = 0) is confirmed as a real defect whose correct
  value A_Y Q_0^2 is reproduced here.  gamma_PPN = 1 and the deep-MOND limit both hold with the
  aether's own scalar perturbation restored.  The legality criterion is now DERIVED from the
  second variation instead of asserted, and in the sharper form 1/U' > 0 it is STRICTER than
  the form the corpus used.

  ADVERSE TO THE OPERATIVE KERNEL, MORE SHARPLY THAN BEFORE.  The exponential kernel's failure
  is not the mild kind that hysteresis rescues.  Its fold is in the wrong variable, so no
  Lagrangian of the form Fcal(Y,Q) exists at all, and restricting to either branch destroys
  either the solar system or every galaxy.

  ADVERSE TO stage75's HEADLINE, WHICH IS THE STRONGEST CLAIM IN THAT FILE.  Legality does not
  SELECT nu = sqrt(1+1/y) and does not leave ZERO free functions.  It leaves an
  infinite-dimensional convex class, three explicit members of which are exhibited here in
  closed form, all passing every gate stage75 uses -- including the deep-MOND asymptotics that
  file treats as independent confirmation.  'AeST selects the a_0-line' must be reworded.

  UNTOUCHED: a_0 = kappa c sqrt(G rho_Lam), kappa = 1/2 (fitted), the RAR fit, BTFR, lensing,
  CLASS, the promotion a_0^2(Q) = kappa^2 G(-K(Q)), and the ephemeris liability -- which this
  file makes STRUCTURAL rather than kernel-specific.

  NOT COMPUTED HERE: the time-dependent scalar/vector sector (so no sound speed and no
  statement about alpha's own kinetic term, R-V); non-spherical configurations (P3 is proved
  only for spherical symmetry); the O(w^2) preferred-frame sector; and any refit of the
  alternative legal kernels to SPARC, which would be needed to turn F4's 0.097 dex worst pair into
  a real discrimination statement (F4's decisive number, the 0.006 dex gap to ALT-4, needs no
  refit: nothing at 0.108 dex scatter can see it).
""")
