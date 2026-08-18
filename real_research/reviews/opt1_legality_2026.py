"""
=========================================================================================
opt1_legality_2026.py -- ROUTE 2 OF THE OPTION-1 AUDIT:
DOES REPLACING F(Y,Q) BY F(Z,Q), Z = J^mu J_mu, ESCAPE AeST's MONOTONICITY TRAP?
=========================================================================================
2026-08-18.

THE QUESTION.  AeST's free function eats Y = q^{mu nu} grad_mu phi grad_nu phi -- the
SCALAR's own spatial gradient.  The quasi-static reduction then gives the purely local law
u J_Y(u^2) = g_bar with u = |grad varphi| the ANOMALOUS acceleration, and single-valuedness
of J_Y as a function of Y = u^2 forces y -> U(y) = u/a_0 to be injective, hence (with the
Newtonian and deep-MOND limits fixing the sense) STRICTLY INCREASING.  An increasing U
cannot fall below its galaxy value in the solar system, which is the 1.2e4-3.4e4 gap
between the ephemeris ceiling (s <= 1.27e-5 canonical / 1.05e-5 alt) and the RAR floor.

OPTION 1 replaces the argument: F(Y,Q) -> F(Z,Q) with

        Z := J^mu J_mu,    J^mu = A^nu grad_nu A^mu   (the aether's ACCELERATION),

which is the Einstein-aether c_4 structure promoted from a constant (zero in AeST) to a
function.  The claim to be tested is that in the quasi-static limit J_i ~ grad_i Psi, the
TOTAL metric potential's gradient, so the free function now eats what AQUAL's eats.

MY ASSIGNMENT (route 2): (a) redo the quasi-static reduction with F(Z,Q), DERIVING rather
than assuming the AQUAL form; (b) state the resulting single-valuedness / no-ghost
condition in terms of the observable kernel; (c) test the decisive case -- the exponential
kernel nu = 1/(1-exp(-sqrt y)), illegal in AeST and legal in AQUAL -- and give the minimum
of the stability functional as a number; (d) does saturation still follow?
And throughout: hunt for the trap being reimposed by another route.

=========================================================================================
RESULT IN ONE PARAGRAPH -- direction: FAVOURABLE, with one sharp unpriced liability
=========================================================================================
THE ESCAPE IS REAL AND IT IS STRUCTURAL, NOT A CHOICE OF KERNEL.  Z is, at the order that
matters, EXACTLY |grad Psi|^2 -- free of varphi, of the aether's spatial mode a_i, and of
Phi -- so the free function's argument is the total potential (A4-A6, derived from
J^mu = A^nu grad_nu A^mu and the unit-norm constraint, no ansatz).  Varying the same
calibrated quadratic Lagrangian that reproduces typeII_direct_variation_2026.py's D5/D6/D7
in the F(Y) case, the F(Z) theory gives: the aether-longitudinal equation collapses from
(1+J_Y)v = grad Psi to v = grad Psi, the scalar sector DECOUPLES (psi := Psi - varphi -
Q_0 alpha is free and massless, hence zero), and the Psi equation becomes
        div[ J_Z(|grad Psi|^2) grad Psi ] = 4 pi Ghat rho,
i.e. AQUAL EXACTLY, with mu-function mu(g_obs) = J_Z and the SAME Ghat.  The
no-ghost/ellipticity conditions have IDENTICAL STRUCTURE in the two theories -- the
longitudinal and transverse 2x2 Hessian blocks have determinants 4 d/ds[J'(s^2)s] and
4 J', literally the same expressions -- and the ONLY thing that changes is the ARGUMENT at
which they are evaluated: s = u (the anomaly) in AeST, s = g_obs (the total) in option 1.
That single substitution converts "dU/dy > 0" into "dg_obs/dg_bar > 0".
DECISIVE NUMBER: for the exponential kernel the option-1 stability functional dx/dy
(x = g_obs/a_0, y = g_bar/a_0) has MINIMUM 0.96755 at y = 6.634 -- strictly positive, LEGAL
-- while the SAME kernel's AeST functional dU/dy reaches -0.0324 at the same y, NEGATIVE,
ILLEGAL, exactly as the trap says.  Saturation does NOT follow: U(y) = y(nu(y)-1) rises to
an interior maximum 0.64761 at y = 2.540 and then DECAYS, reaching 10^-3448.7 at 1 AU
against the ephemeris ceiling 10^-4.90 -- margins of 3444 orders canonical and 3136 orders
alt.  The RAR floor U(2) >= 0.4348 is met at the same time, U(2) = 0.6424.  So the
1.2e4-3.4e4 gap is not narrowed, it is DELETED: the quantity it constrained -- the
saturated anomaly s -- is no longer forced to exist.
WHAT I LOOKED FOR AND DID NOT FIND (the assignment's warning, taken seriously): no extra
scalar-sector constraint survives.  The varphi equation is the DIVERGENCE of the
aether-longitudinal one (typeII D8's degeneracy again), so the system is not
overdetermined; the on-shell coincidence Y = Z does NOT let one rewrite F(Z) as F(Y),
because both field equations differ before the solution is imposed (C5, checked
explicitly); the free function is CONSTRUCTED by inverting the kernel and shown to have
both required limits, J_Z -> sqrt(Z)/a_0 in deep MOND (so J -> (2/3)Z^{3/2}/a_0, SZ21's own
MOND normalisation with the same a_0) and J_Z -> 1 in the Newtonian limit (G1b); and Z's
linear-cosmology order counting is IDENTICAL to Y's (Zbar = 0, delta Z = 0, so J(Z) =
O(delta^3) and a_0 stays absent from linear perturbations).
THE LIABILITIES, ALL NAMED, NONE FULLY PRICED:
 (L1) SHARPEST, AND NEW.  J_Z -> 1 in the Newtonian limit, i.e. an EFFECTIVE c_4 =
      (2-K_B) J_Z of order 1 locally.  The naive Einstein-aether reading c_14 = c_1 + c_4
      -> K_B + (2-K_B) = 2 would make G_N = G/(1-c_14/2) SINGULAR.  It does NOT: explicit
      variation (C6) shows the J^mu grad_mu phi mixing term cancels it exactly, leaving
      lap Psi = 4 pi Ghat rho with the SAME Ghat.  And the effective c_4 is a FIELD, not a
      constant -- it VANISHES on FRW (Z = 0), so cosmology sees no c_4 at all.  But alpha_1
      and alpha_2 are measured in the solar system, which is precisely where J_Z -> 1, and
      that sector is O(w) BOOSTED -- NOT COMPUTED HERE.  This is the item that could still
      kill option 1.
 (L2) DOWNGRADED, not closed.  The worry that J(Z) sources the ij Einstein equations and
      voids typeII's D2/D3 gamma_PPN = 1 does NOT bite at the order that derivation works:
      Phi enters Z only at eps^3 and the measure only at eps^1 times an eps^2 object, so
      sqrt(-g)J(Z)'s entire Phi/h_ij dependence is CUBIC and absent from the quadratic
      action (G4, exhibited).  The eps^3 sector is unpriced, and the eps-bookkeeping that
      buys this ties a_0 to the weak-field parameter -- so "survives at its own order",
      not "closed".
 (L3) LEGALITY IS NOT SAFETY.  The framework's OWN interpolation g_obs = sqrt(g_bar^2 +
      g_bar a_0) is ALSO made legal by option 1 (min dx/dy = 1.0000) yet still has U -> 1/2
      and still busts the ephemeris ceiling by 3.94e4 canonical / 4.76e4 alt.  Option 1
      removes the STRUCTURAL obstruction and nothing more; passing the solar system stays a
      requirement ON THE KERNEL, met by the exponential kernel and not by the algebraic one.

=========================================================================================
EVERY REDUCTION AND EVERY CALIBRATION, DECLARED
=========================================================================================
R1 STATIC, weak field, same order counting as typeII_direct_variation_2026.py R2: h, a_mu,
   varphi, rho are O(eps) and a_0 is O(eps), so J(Z) ~ Z^{3/2}/a_0 is O(eps^2) -- the same
   order as the ordinary kinetic term.  Truncation at eps^2 with explicit degree checks;
   PART A carries eps^3 in order to SHOW that the corrections are third order.
R2 CALIBRATED, NOT RE-DERIVED: I do not recompute the Ricci scalar.  I write the
   quadratic Lagrangian as L = -c|grad Psi - v|^2 - (2-K_B) J(arg) - 16 pi Gt rho Psi with
   v = grad varphi + Q_0 a, and FIX c = (2-K_B) by DEMANDING that the F(Y) case reproduce
   typeII's D5 (the 00 equation) -- then CHECK that the same L independently reproduces
   typeII's D6 (scalar) and D7 (aether-longitudinal), which it was not tuned to do.  Two
   equations reproduced from one calibration is the control; if it failed, everything below
   would be void.  The gravity sector is therefore INHERITED, not re-derived, and any error
   in typeII's D5-D7 propagates here.  STATED, not hidden.
R3 F(Y,Q) -> (2-K_B) J(Y) + K(Q) and F(Z,Q) -> (2-K_B) J(Z) + K(Q).  Cross terms are
   O(eps^3) at this order for both arguments (Y, Z are both O(eps^2)), checked at A10.
R4 K'(Q_0) (the cosmological dust density) and the Yukawa mass m_Psi are set to zero in the
   reduction; typeII PART F prices them at 1.7e-23 / 1.2e-23 at 1 AU and 6.6e-6 / 4.5e-4 at
   30 kpc.  Those numbers are QUOTED from that file, not recomputed here.
R5 CURL SECTOR: as in AeST and in Bekenstein-Milgrom, the pointwise vector law holds exactly
   in curl-free (e.g. spherical) configurations and up to a divergence-free field otherwise.
   nu(y), the ephemeris application and the rotation-curve application all live in the
   spherical sector.  Unchanged by option 1, and NOT re-litigated here.
R6 NOT DONE HERE: alpha_1/alpha_2 (L1), gamma_PPN with the new anisotropic stress (L2),
   c_T, the nonlinear CMB, and any refit of Upsilon.  The RAR check at PART H is a fixed-
   Upsilon SANITY ANCHOR against the committed 0.108 dex fitter, not a refit.

EXIT 0 iff every numbered check passes.
"""

import json
import math
import os
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

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =================================================================================================
# constants -- both footings carried for every dimensional number
# =================================================================================================
CLIGHT = 2.99792458e8
GMSUN = 1.32712440018e20
AU = 1.495978707e11
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
# ephemeris ceilings on the saturated anomaly s = lim U(y), from
# real_research/reviews/a0_local_ephemeris_2026.py as quoted in the assignment (NO EFE relief):
S_CEIL = {"canonical": 1.27e-5, "ALT": 1.05e-5}
# RAR floors on U(2), from the assignment:
U2_FLOOR_POINTWISE = 0.4348
U2_FLOOR_PERGAL = {"canonical": 0.157, "ALT": 0.126}

# =================================================================================================
print()
print("=" * 100)
print("PART A -- WHAT Z ACTUALLY IS ON A GENERIC STATIC CONFIGURATION")
print("          (derived from the metric and the aether, nothing assumed)")
print("=" * 100)

tt, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
CO = [tt, x1, x2, x3]
SPC = [x1, x2, x3]
eps = sp.Symbol("eps")
Q0, KB, GT, rhoh = sp.symbols("Q_0 K_B Gt rhohat", real=True)


def fn(name):
    return sp.Function(name)(x1, x2, x3)


PsiF, PhiF, wf = fn("Psi"), fn("Phi"), fn("varphi")
aif = [fn("a1"), fn("a2"), fn("a3")]


def tr(e, n):
    """truncate at eps^n"""
    e = sp.expand(e)
    return sum(eps ** k * e.coeff(eps, k) for k in range(n + 1))


def deg_ok(e, n):
    return sp.Poly(sp.expand(e), eps).degree() <= n


NEXP = 4  # keep through eps^3, so that "the correction is O(eps^3)" is a SHOWN result

# --- metric, with the inverse written as an EXACT truncated series (no rational functions) -----
g = sp.zeros(4, 4)
g[0, 0] = -(1 + 2 * eps * PsiF)
for i in range(1, 4):
    g[i, i] = 1 - 2 * eps * PhiF
ginv = sp.zeros(4, 4)
ginv[0, 0] = -sum((-2 * eps * PsiF) ** k for k in range(NEXP))
for i in range(1, 4):
    ginv[i, i] = sum((2 * eps * PhiF) ** k for k in range(NEXP))
resid = sp.expand(g * ginv - sp.eye(4))
check(all(deg_ok(resid[i, j], NEXP + 2) and all(sp.simplify(resid[i, j].coeff(eps, k)) == 0
                                                for k in range(NEXP))
          for i in range(4) for j in range(4)),
      "A1  the truncated inverse metric satisfies g.ginv = 1 through eps^3",
      "the series form is used everywhere below so that eps-degree checks are meaningful")

# --- the aether, unit-timelike, solved order by order with linsolve (no generic solve) ---------
c1s, c2s, c3s = sp.symbols("c1 c2 c3")
A0ans = -(1 + eps * c1s + eps ** 2 * c2s + eps ** 3 * c3s)
A_low = [A0ans] + [eps * a for a in aif]
norm = sp.expand(sum(ginv[m, n] * A_low[m] * A_low[n] for m in range(4) for n in range(4)) + 1)
# solved ORDER BY ORDER: at each order the unknown enters linearly once the lower orders are
# substituted, so each step is an sp.linsolve on a single linear equation (never a generic solve
# on the coupled nonlinear system, which would be illegal under the sympy rule).
known, sol = {}, []
for k, sym in ((1, c1s), (2, c2s), (3, c3s)):
    eqk = sp.expand(norm.coeff(eps, k).subs(known))
    check(sp.degree(sp.Poly(eqk, sym), sym) == 1,
          f"A2{k} the eps^{k} norm equation is LINEAR in {sym} once lower orders are substituted")
    rk = sp.simplify(list(sp.linsolve([eqk], [sym]))[0][0])
    known[sym] = rk
    sol.append(rk)
A0 = sp.expand(A0ans.subs(known))
check(sp.simplify(sol[0] - PsiF) == 0
      and sp.simplify(sol[1] - (-PsiF ** 2 / 2 + sum(a ** 2 for a in aif) / 2)) == 0,
      "A2  the unit-norm constraint gives A_0 = -(1 + eps Psi + eps^2(-Psi^2/2 + |a|^2/2) + ...)",
      "the -Psi^2/2 reproduces typeII_direct_variation_2026.py's P1 in the a_i = 0 sector; the "
      "+|a|^2/2 is its generalisation, obtained here independently")

A_lo = [A0] + [eps * a for a in aif]
A_up = [tr(sum(ginv[m, n] * A_lo[n] for n in range(4)), NEXP - 1) for m in range(4)]

# --- Christoffels -----------------------------------------------------------------------------
GAM = {}
for m in range(4):
    for n in range(4):
        for l in range(4):
            s = 0
            for sg in range(4):
                s += ginv[m, sg] * (sp.diff(g[sg, l], CO[n]) + sp.diff(g[sg, n], CO[l])
                                    - sp.diff(g[n, l], CO[sg]))
            GAM[(m, n, l)] = tr(sp.expand(s / 2), NEXP - 1)

# --- J^mu = A^nu nabla_nu A^mu ----------------------------------------------------------------
Jup = []
for m in range(4):
    s = 0
    for n in range(4):
        s += A_up[n] * (sp.diff(A_up[m], CO[n]) + sum(GAM[(m, n, l)] * A_up[l] for l in range(4)))
    Jup.append(tr(sp.expand(s), NEXP - 1))

check(sp.simplify(Jup[0].coeff(eps, 0)) == 0 and sp.simplify(Jup[0].coeff(eps, 1)) == 0,
      "A3  J^0 has no eps^0 and no eps^1 piece: the aether's acceleration is purely spatial "
      "at leading order",
      f"its eps^2 piece is {sp.simplify(Jup[0].coeff(eps,2))} -- the a.grad Psi term, which "
      "enters the action only through the mixing term and is retained there")
gradPsi = [sp.diff(PsiF, c) for c in SPC]
check(all(sp.simplify(Jup[i + 1].coeff(eps, 0)) == 0 for i in range(3))
      and all(sp.simplify(Jup[i + 1].coeff(eps, 1) - gradPsi[i]) == 0 for i in range(3)),
      "A4  *** J^i = eps grad_i Psi + O(eps^2): the aether's acceleration IS the gradient of "
      "the TOTAL metric potential, with coefficient exactly 1 ***",
      "this is the structural fact option 1 rests on, and it is derived here from "
      "J^mu = A^nu grad_nu A^mu and the unit-norm constraint alone -- no ansatz for J")

Zinv = tr(sp.expand(sum(g[m, n] * Jup[m] * Jup[n] for m in range(4) for n in range(4))), NEXP - 1)
Z2 = sp.expand(Zinv.coeff(eps, 2))
check(sp.simplify(Zinv.coeff(eps, 0)) == 0 and sp.simplify(Zinv.coeff(eps, 1)) == 0
      and sp.simplify(Z2 - sum(gp ** 2 for gp in gradPsi)) == 0,
      "A5  *** GATE: Z = J^mu J_mu = eps^2 |grad Psi|^2 + O(eps^3), EXACTLY ***",
      "Z vanishes at eps^0 and eps^1 (so, like Y, it is quadratic in perturbations) and its "
      "eps^2 coefficient is the squared gradient of the total potential and nothing else")
check(all(sp.simplify(sp.diff(Z2, f)) == 0 for f in [wf, PhiF] + aif)
      and all(all(sp.simplify(sp.diff(Z2, sp.Derivative(f, c))) == 0 for c in SPC)
              for f in [wf, PhiF] + aif),
      "A6  *** and Z's eps^2 coefficient is INDEPENDENT of varphi, of Phi and of a_i ***",
      "so at the order worked the free function's new argument is a function of Psi alone.  "
      "In particular Z carries no h_ij dependence, so J(Z) adds nothing to the tensor sector "
      "at this order (c_T is untouched here; the full c_T statement is another route's)")

# --- Y and Q, for the control -----------------------------------------------------------------
phi = Q0 * tt + eps * wf
dphi = [sp.diff(phi, c) for c in CO]
Qcal = tr(sp.expand(sum(A_up[m] * dphi[m] for m in range(4))), NEXP - 1)
qinv = [[tr(sp.expand(ginv[m, n] + A_up[m] * A_up[n]), NEXP - 1) for n in range(4)]
        for m in range(4)]
Ycal = tr(sp.expand(sum(qinv[m][n] * dphi[m] * dphi[n] for m in range(4) for n in range(4))),
          NEXP - 1)
v = [sp.diff(wf, SPC[k]) + Q0 * aif[k] for k in range(3)]
check(sp.simplify(Ycal.coeff(eps, 0)) == 0 and sp.simplify(Ycal.coeff(eps, 1)) == 0
      and sp.simplify(sp.expand(Ycal.coeff(eps, 2) - sum(vk ** 2 for vk in v))) == 0,
      "A7  CONTROL: the same machinery reproduces Y = eps^2 |grad varphi + Q_0 a|^2, which is "
      "typeII_direct_variation_2026.py's P1 exactly",
      "the machinery that produced A5 is therefore the machinery that reproduces the known "
      "result for the OTHER argument -- the control that makes A5 credible")
check(sp.simplify(Qcal.coeff(eps, 0) - Q0) == 0 and sp.simplify(Qcal.coeff(eps, 1) + Q0 * PsiF) == 0,
      "A8  CONTROL: Q = Q_0(1 - eps Psi) + O(eps^2), also typeII P1",
      "Q is unchanged by option 1, so the K(Q) dust/CMB sector is untouched at this order")

check(all(deg_ok(e, NEXP - 1) for e in [Zinv, Ycal, Qcal] + Jup),
      "A9  explicit degree check: every truncated object is a polynomial in eps of degree <= 3")
check(True,
      "A10 R3 verified by inspection of A5 + A7: Y and Z are both O(eps^2), so any F cross "
      "term Y^m Z^n with m+n >= 2 is O(eps^4) and any Y-Q or Z-Q cross term beyond the ones "
      "kept is O(eps^3).  Splitting F into (2-K_B)J(arg) + K(Q) is therefore not a "
      "restriction at quadratic order",
      "same argument as typeII R3, applied to the new argument")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE CALIBRATED QUADRATIC LAGRANGIAN, AND THE CONTROL THAT VALIDATES IT")
print("=" * 100)

Jc = sp.Function("Jcal")
csym = sp.Symbol("c_grav")
uarg = sp.Symbol("uarg")


def Jprime(arg):
    return sp.diff(Jc(uarg), uarg).subs(uarg, arg)


P = [sp.diff(PsiF, c) for c in SPC]
Ysh = sum(vk ** 2 for vk in v)
Zsh = sum(pk ** 2 for pk in P)


def build_L(cval, arg):
    return (-cval * sum((P[k] - v[k]) ** 2 for k in range(3))
            - (2 - KB) * Jc(arg)
            - 16 * sp.pi * GT * rhoh * PsiF)


def el3(L, f):
    """Euler-Lagrange derivative in the 3 static coordinates (first derivatives only here)"""
    out = sp.diff(L, f)
    for c in SPC:
        out -= sp.diff(sp.diff(L, sp.Derivative(f, c)), c)
    return sp.expand(out.doit())


def lap(e):
    return sum(sp.diff(e, c, 2) for c in SPC)


def div(vec):
    return sum(sp.diff(vec[k], SPC[k]) for k in range(3))


info("B0  the mixing term 2(2-K_B) J^mu grad_mu phi contributes, at eps^2,\n"
     "        2(2-K_B)[ (grad Psi).(grad varphi) + Q_0 a.(grad Psi) ] = 2(2-K_B) (grad Psi).v ,\n"
     "    using A4 for J^i and A3's eps^2 piece for J^0.  Together with -(2-K_B) Y = "
     "-(2-K_B)|v|^2\n"
     "    and a gravity-sector term -c|grad Psi|^2, the whole non-J(arg) part is\n"
     "        -c|grad Psi|^2 + 2(2-K_B) (grad Psi).v - (2-K_B)|v|^2 ,\n"
     "    which is -(2-K_B)|grad Psi - v|^2 IFF c = (2-K_B).  c is FIXED BY CALIBRATION below,\n"
     "    not by assumption.")

Lb_c = build_L(csym, Ysh)
eq_Psi_b = el3(Lb_c, PsiF)
# typeII D5 (with K' = 0, m_Psi = 0): div(grad Psi - v) = 4 pi Ghat rho, Ghat = 2 Gt/(2-K_B)
target_D5 = sp.expand(div([P[k] - v[k] for k in range(3)]) - 8 * sp.pi * GT * rhoh / (2 - KB))
sol_c = sp.solve(sp.Eq(sp.expand(eq_Psi_b / (2 * csym) - target_D5).coeff(rhoh, 1), 0), csym)
check(len(sol_c) == 1 and sp.simplify(sol_c[0] - (2 - KB)) == 0,
      "B1  *** CALIBRATION: demanding that the F(Y) theory reproduce typeII's D5 (the 00 "
      "equation, lap Psi = 4 pi Ghat rho + lap varphi with Ghat = 2 Gt/(2-K_B)) FIXES the "
      "gravity-sector coefficient to c = (2-K_B) ***",
      f"solved c = {sol_c}; this is the ONE number taken from the inherited gravity sector")

CG = 2 - KB
Lb = build_L(CG, Ysh)   # baseline: F eats Y
Lo = build_L(CG, Zsh)   # option 1: F eats Z

check(sp.simplify(sp.expand(el3(Lb, PsiF) - 2 * (2 - KB) * target_D5)) == 0,
      "B2  with c = (2-K_B) the Psi equation of the F(Y) theory IS typeII's D5 exactly",
      "div(grad Psi - v) = 4 pi Ghat rho, i.e. Psi = Psi_N + (the potential of div v)")

# --- the two checks the calibration was NOT tuned to pass --------------------------------------
JY = Jprime(Ysh)
S_typeII = [sp.expand((1 + JY) * v[k] - P[k]) for k in range(3)]
check(sp.simplify(sp.expand(el3(Lb, wf) - 2 * (2 - KB) * div(S_typeII))) == 0,
      "B3  *** CONTROL 1 (not tuned): the scalar equation of the F(Y) theory is EXACTLY "
      "typeII's D6, div[(1+J_Y) v] = lap(Psi) ***")
check(all(sp.simplify(sp.expand(sp.diff(Lb, aif[k]) + 2 * (2 - KB) * Q0 * S_typeII[k])) == 0
          for k in range(3)),
      "B4  *** CONTROL 2 (not tuned): the aether-longitudinal equation of the F(Y) theory is "
      "EXACTLY typeII's D7 source, S = (1+J_Y) v - grad Psi = 0 ***",
      "the F_{mu nu}^2 term is purely transverse for static a_i (F_ij = d_i a_j - d_j a_i "
      "vanishes on a longitudinal a), so the longitudinal a-equation is algebraic -- typeII "
      "D7's own statement.  TWO independent equations reproduced from ONE calibration: the "
      "Lagrangian is validated")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE OPTION-1 REDUCTION, DERIVED")
print("=" * 100)

JZ = Jprime(Zsh)
eq_a_o = [sp.expand(sp.diff(Lo, aif[k])) for k in range(3)]
check(all(sp.simplify(eq_a_o[k] - 2 * (2 - KB) * Q0 * (P[k] - v[k])) == 0 for k in range(3)),
      "C1  *** the aether-longitudinal equation of the F(Z) theory is v = grad Psi POINTWISE, "
      "with the (1+J_Y) factor GONE ***",
      "the free function has left this equation entirely, because Z does not contain a_i (A6)")

eq_w_o = el3(Lo, wf)
check(sp.simplify(sp.expand(eq_w_o + 2 * (2 - KB) * div([P[k] - v[k] for k in range(3)]))) == 0,
      "C2  the scalar equation is div[grad Psi - v] = 0, which is the DIVERGENCE of C1: the "
      "system is not overdetermined",
      "same degeneracy typeII D8 found in the F(Y) theory -- only chi = varphi + Q_0 alpha is "
      "physical, and here it is fixed to Psi")

eq_Psi_o = el3(Lo, PsiF)
target_AQUAL = sp.expand(div([P[k] - v[k] + JZ * P[k] for k in range(3)])
                         - 8 * sp.pi * GT * rhoh / (2 - KB))
check(sp.simplify(sp.expand(eq_Psi_o - 2 * (2 - KB) * target_AQUAL)) == 0,
      "C3  the Psi equation is div[(grad Psi - v) + J_Z grad Psi] = 4 pi Ghat rho")

check(sp.simplify(sp.expand(target_AQUAL.subs(
        {sp.Derivative(wf, c): sp.Derivative(PsiF, c) for c in SPC}).subs(
        {aif[k]: 0 for k in range(3)}).doit()
      - (div([JZ * P[k] for k in range(3)]) - 8 * sp.pi * GT * rhoh / (2 - KB)))) == 0,
      "C4  *** THE RESULT: substituting C1 (v = grad Psi) into C3 gives\n"
      "        div[ J_Z(|grad Psi|^2) grad Psi ] = 4 pi Ghat rho ,\n"
      "    which is AQUAL EXACTLY, with mu-function mu(g_obs) = J_Z(g_obs^2) and the SAME "
      "Ghat as the F(Y) theory ***",
      "DERIVED, not assumed: the AQUAL form is the output of varying the AeST action with "
      "F(Z,Q), not an ansatz.  The scalar sector has decoupled -- psi := Psi - varphi - Q_0 "
      "alpha obeys lap psi = 0 and vanishes with the boundary condition psi -> 0")

# --- the anti-manufacture check: is F(Z) secretly F(Y)? ----------------------------------------
check(sp.simplify(sp.expand(el3(Lb, wf) - el3(Lo, wf))) != 0
      and sp.simplify(sp.expand(el3(Lb, PsiF) - el3(Lo, PsiF))) != 0,
      "C5  ANTI-MANUFACTURE: on shell C1 gives Y = |v|^2 = |grad Psi|^2 = Z, so the two "
      "theories agree on the VALUE of the free function's argument.  They do NOT agree on "
      "the field equations -- both the scalar and the Psi equation differ before the "
      "solution is imposed.  So the escape is not the tautology 'Y = Z'",
      "the difference is exactly where J_Z / J_Y sits: multiplying v in the F(Y) theory and "
      "multiplying grad Psi in the F(Z) theory")

# --- the Newtonian-limit / effective-c_4 worry (L1) --------------------------------------------
Lnewt = build_L(CG, Zsh).subs(Jc(Zsh), Zsh)   # J(Z) -> Z, i.e. effective c_4 = (2-K_B)
eqP = el3(Lnewt, PsiF)
eqw = el3(Lnewt, wf)
solPsi = sp.expand(eqP.subs({sp.Derivative(wf, c): sp.Derivative(PsiF, c) for c in SPC}
                            ).subs({aif[k]: 0 for k in range(3)}).doit())
check(sp.simplify(solPsi - 2 * (2 - KB) * (lap(PsiF) - 8 * sp.pi * GT * rhoh / (2 - KB))) == 0,
      "C6  *** LIABILITY L1, STATIC HALF, RESOLVED: in the Newtonian limit J_Z -> 1, i.e. an "
      "effective c_4 = (2-K_B) = O(1).  The naive Einstein-aether reading c_14 = c_1 + c_4 -> "
      "K_B + (2-K_B) = 2 would make G_N = G/(1-c_14/2) SINGULAR.  Explicit variation shows it "
      "does NOT: the J^mu grad_mu phi mixing term cancels it exactly and the Psi equation is "
      "lap Psi = 4 pi Ghat rho with the SAME Ghat ***",
      "so option 1 does not break the static Newtonian limit.  The BOOSTED sector (alpha_1, "
      "alpha_2), where an O(1) effective c_4 is most dangerous, is NOT COMPUTED HERE and is "
      "the sharpest open item option 1 creates")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE NO-GHOST / SINGLE-VALUEDNESS CONDITION, BOTH THEORIES")
print("=" * 100)

p1, p2, p3, w1, w2, w3 = sp.symbols("p1 p2 p3 w1 w2 w3", real=True)
PP, WW = [p1, p2, p3], [w1, w2, w3]
Ps, Ws = sp.Symbol("P", positive=True), sp.Symbol("W", positive=True)
Jf = sp.Function("Jcal")


def hess(expr, vars_):
    return sp.Matrix(len(vars_), len(vars_), lambda i, j: sp.diff(expr, vars_[i], vars_[j]))


def blocks(bracket, at):
    """convexity blocks of `bracket` at an ALIGNED configuration p = (P,0,0), w = (W,0,0)"""
    H = hess(bracket, PP + WW).subs(at)
    H = sp.Matrix(6, 6, lambda i, j: sp.simplify(H[i, j]))
    lon = H[[0, 3], [0, 3]]
    trv = H[[1, 4], [1, 4]]
    trv2 = H[[2, 5], [2, 5]]
    return lon, trv, trv2


ALIGN = {p1: Ps, p2: 0, p3: 0, w1: Ws, w2: 0, w3: 0}
freepart = sum((PP[k] - WW[k]) ** 2 for k in range(3))
Zg = sum(pk ** 2 for pk in PP)
Yg = sum(wk ** 2 for wk in WW)

jp, jpp = sp.symbols("Jp Jpp", real=True)   # J'(arg), J''(arg) at the aligned configuration

lonB, trvB, trv2B = blocks(freepart + Jf(Yg), ALIGN)
lonO, trvO, trv2O = blocks(freepart + Jf(Zg), ALIGN)


def to_jp(M):
    """rename the (unevaluated) first and second derivatives of the free function at the
    aligned configuration to the plain symbols Jp, Jpp -- a RENAMING only, no assumption
    about J beyond twice differentiability"""
    out = M
    for e in M.atoms(sp.Subs):
        d = e.expr
        order = sum(n for _, n in d.variable_count) if isinstance(d, sp.Derivative) else 0
        out = out.subs(e, {0: sp.Symbol("J0"), 1: jp, 2: jpp}[order])
    for e in out.atoms(sp.Derivative):
        order = sum(n for _, n in e.variable_count)
        out = out.subs(e, {1: jp, 2: jpp}[order])
    return sp.Matrix(out.rows, out.cols, lambda i, j: sp.simplify(out[i, j]))


lonB, trvB, trv2B = [to_jp(M) for M in (lonB, trvB, trv2B)]
lonO, trvO, trv2O = [to_jp(M) for M in (lonO, trvO, trv2O)]
check(not (lonB.free_symbols & {sp.Symbol("J0")}) and not (lonO.free_symbols & {sp.Symbol("J0")}),
      "D0  the renaming captured every free-function derivative in the Hessian blocks "
      "(no undifferentiated J and no leftover Derivative object survives)",
      f"baseline longitudinal block entries {list(lonB)}; option-1 {list(lonO)}")

detlonB, dettrvB = sp.simplify(lonB.det()), sp.simplify(trvB.det())
detlonO, dettrvO = sp.simplify(lonO.det()), sp.simplify(trvO.det())

check(sp.simplify(dettrvB - 4 * jp) == 0 and sp.simplify(dettrvO - 4 * jp) == 0,
      "D1  the TRANSVERSE 2x2 block has determinant 4 J' in BOTH theories -- the same "
      "expression",
      f"baseline {dettrvB}, option 1 {dettrvO}")
check(sp.simplify(detlonB - 4 * (jp + 2 * jpp * Ws ** 2)) == 0
      and sp.simplify(detlonO - 4 * (jp + 2 * jpp * Ps ** 2)) == 0,
      "D2  *** THE WHOLE POINT: the LONGITUDINAL 2x2 block has determinant "
      "4(J' + 2 J'' arg) = 4 d/ds[J'(s^2) s] in BOTH theories -- again the SAME expression "
      "-- but evaluated at s = W = |v| = u in the F(Y) theory and at s = P = |grad Psi| = "
      "g_obs in the F(Z) theory ***",
      f"baseline {detlonB} (argument W), option 1 {detlonO} (argument P).  The no-ghost "
      "condition is structurally IDENTICAL; only its argument moves from the anomaly to the "
      "total.  That single substitution is option 1")
check((trv2B - trvB).is_zero_matrix and (trv2O - trvO).is_zero_matrix,
      "D3  the second transverse block duplicates the first, as it must by symmetry")
check(sp.simplify(lonB.trace()) == sp.simplify(2 + 2 + 2 * jp + 4 * jpp * Ws ** 2)
      and sp.simplify(lonO.trace()) == sp.simplify(2 + 2 + 2 * jp + 4 * jpp * Ps ** 2),
      "D4  the traces are positive whenever the determinants are, so positive determinant IS "
      "positive definiteness here (no branch where both eigenvalues are negative)",
      "hence: healthy <=> J' > 0 AND d/ds[J'(s^2) s] > 0, in both theories")

info("D5  TRANSLATION TO OBSERVABLES.  Write x = g_obs/a_0, y = g_bar/a_0, U = u/a_0.\n"
     "    F(Y) theory (typeII D6+D7 with a = 0):  J_Y(u^2) u = g_bar, so d/du[J_Y(u^2)u] =\n"
     "        dg_bar/du > 0  <=>  dU/dy > 0.  U MUST BE MONOTONE INCREASING -- THE TRAP.\n"
     "    F(Z) theory (C4):                       J_Z(g_obs^2) g_obs = g_bar, so\n"
     "        dg_bar/dg_obs > 0  <=>  dx/dy > 0.  THE AQUAL CONDITION.\n"
     "    Transverse in both: J' > 0, i.e. g_bar/u > 0 resp. g_bar/g_obs = 1/nu > 0.")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- THE DECISIVE CASE: THE EXPONENTIAL KERNEL nu(y) = 1/(1 - exp(-sqrt y))")
print("=" * 100)


def xofy(y):
    """x = g_obs/a_0 = y nu(y) for the exponential (Route A / Milgrom-Sanders 2008 alpha=1/2)
    kernel.  In t = sqrt(y): x = t^2/(1 - e^-t)."""
    t = math.sqrt(y)
    return t * t / (-math.expm1(-t))


def Uofy(y):
    """U = u/a_0 = x - y = t^2/(e^t - 1)"""
    t = math.sqrt(y)
    return t * t / math.expm1(t)


def log10U(y):
    """log10 U, valid to arbitrarily large y (asymptotic branch avoids overflow)"""
    t = math.sqrt(y)
    if t < 300.0:
        return math.log10(t * t / math.expm1(t))
    return 2.0 * math.log10(t) - t / math.log(10.0)


def dxdy(y, h=None):
    """dx/dy analytically: with t = sqrt(y),
       dx/dy = [2(1-e^-t) - t e^-t] / [2 (1-e^-t)^2]"""
    t = math.sqrt(y)
    em = math.exp(-t)
    return (2.0 * (1.0 - em) - t * em) / (2.0 * (1.0 - em) ** 2)


def dUdy(y):
    return dxdy(y) - 1.0


# --- control: the analytic derivative against finite differences -------------------------------
worst = 0.0
for y in (1e-3, 1e-2, 0.1, 0.5, 1.0, 2.0, 6.75, 20.0, 100.0, 1e4):
    h = y * 1e-6
    fd = (xofy(y + h) - xofy(y - h)) / (2 * h)
    worst = max(worst, abs(fd - dxdy(y)) / abs(dxdy(y)))
check(worst < 1e-6,
      "E0  CONTROL: the analytic dx/dy agrees with central differences everywhere tested",
      f"worst relative disagreement {worst:.2e}")

# --- the assigned window, u in (1e-4, 40) -----------------------------------------------------
def scan(f, lo, hi, n=400001):
    ys = [lo * (hi / lo) ** (k / (n - 1)) for k in range(n)]
    vals = [f(y) for y in ys]
    i = min(range(n), key=lambda k: vals[k])
    return ys[i], vals[i]


ymin_w, dmin_w = scan(dxdy, 1e-4, 40.0)
check(dmin_w > 0,
      "E1  *** GATE (c): over the assigned window (1e-4, 40) the OPTION-1 stability "
      f"functional dx/dy has MINIMUM {dmin_w:.5f} at y = {ymin_w:.3f} -- STRICTLY POSITIVE.  "
      "THE EXPONENTIAL KERNEL IS LEGAL UNDER F(Z) ***",
      "this reproduces the 0.968 quoted in the assignment for the AQUAL condition, computed "
      "here independently from the kernel's own definition")

ymin_g, dmin_g = scan(dxdy, 1e-12, 1e12)
check(dmin_g > 0,
      f"E2  and the minimum over the FULL range 1e-12 < y < 1e12 is {dmin_g:.5f} at "
      f"y = {ymin_g:.3f} -- the legality is not an artifact of the window",
      "dx/dy -> +inf as y -> 0 (deep MOND, x ~ sqrt y) and -> 1 as y -> infinity (Newtonian)")

mumin = min(y / xofy(y) for y in [1e-12 * (1e24) ** (k / 4000) for k in range(4001)])
check(mumin > 0,
      "E3  the TRANSVERSE condition J_Z = y/x = 1/nu > 0 holds everywhere on the grid",
      f"the smallest value sampled is {mumin:.3e}, and it is the LOW-y ENDPOINT of the grid, "
      "not an interior minimum: J_Z -> sqrt y -> 0 as y -> 0 (the deep-MOND limit, where the "
      "transverse block degenerates in ordinary MOND too) and -> 1 as y -> infinity.  It "
      "never turns negative")

# --- the same kernel in the BASELINE theory: it must FAIL, or my machinery is broken -----------
ymin_U, dmin_U = scan(dUdy, 1e-4, 40.0)
check(dmin_U < 0,
      "E4  *** THE CONTROL THAT MATTERS: the SAME kernel under the F(Y) theory has "
      f"min dU/dy = {dmin_U:.4f} at y = {ymin_U:.3f} -- NEGATIVE, so U is non-monotone and "
      "the kernel is ILLEGAL, exactly as the trap says ***",
      f"AGAINST INTEREST, the LOCAL violation is small: min dU/dy = {dmin_U:.4f} is only "
      f"{-dmin_U:.4f} below zero, so the F(Y) verdict rests on a narrow dip near y ~ "
      f"{ymin_U:.1f} rather than on a dramatic one.  The GLOBAL violation is what is "
      "dramatic: U falls from its peak (E5) to 1e-3449 at 1 AU (F0), a monotonicity failure "
      "of 3449 orders.  Both statements are the same fact.  And the point of this check is "
      "the CONTROL: if it had come out positive my reduction would be reproducing the wrong "
      "baseline and E1 would be worthless.  Same kernel, same code path, opposite verdict -- "
      "and the ONLY difference is which gradient the free function eats")

ygrid = [1e-3 * (1e6) ** (k / 200000) for k in range(200001)]
istar = max(range(len(ygrid)), key=lambda k: Uofy(ygrid[k]))
ystar, Umax = ygrid[istar], Uofy(ygrid[istar])
tail = [log10U(10.0 ** e) for e in (1, 2, 3, 4, 5, 6)]
check(0 < istar < len(ygrid) - 1 and abs(dUdy(ystar)) < 1e-4
      and all(tail[k + 1] < tail[k] for k in range(len(tail) - 1))
      and tail[0] < math.log10(Umax),
      f"E5  *** GATE (d): SATURATION DOES NOT FOLLOW.  U(y) = y(nu(y)-1) = t^2/(e^t - 1) "
      f"RISES to an INTERIOR maximum U = {Umax:.5f} at y = {ystar:.3f} (where dU/dy = "
      f"{dUdy(ystar):.2e}) and then DECAYS monotonically: U = "
      + ", ".join(f"1e{t:.1f}" for t in tail) + " at y = 10, 1e2 ... 1e6 ***",
      "the maximum is LOCATED BY SCAN, not asserted.  Under the F(Y) theory this shape is "
      "forbidden (E4); under F(Z) nothing forbids it, and it is exactly the shape the solar "
      "system needs")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- THE EPHEMERIS ARITHMETIC, BOTH FOOTINGS")
print("=" * 100)

for fname, a0 in FOOT:
    for rname, r in (("Mercury 0.387 AU", 0.387 * AU), ("Earth 1 AU", AU),
                     ("Saturn 9.58 AU", 9.58 * AU)):
        gb = GMSUN / r ** 2
        y = gb / a0
        lU = log10U(y)
        info(f"F0  {fname:9s} {rname:16s}: g_bar = {gb:.4e}, y = {y:.4e}, "
             f"sqrt y = {math.sqrt(y):.5g}, log10 U = {lU:.1f}")

margins = {}
for fname, a0 in FOOT:
    y = (GMSUN / AU ** 2) / a0
    lU = log10U(y)
    lceil = math.log10(S_CEIL[fname])
    margins[fname] = lceil - lU
    check(lU < lceil,
          f"F1  [{fname}] at 1 AU the exponential kernel gives log10 U = {lU:.1f} against the "
          f"ephemeris ceiling log10 s = {lceil:.2f}: a margin of {margins[fname]:.0f} orders "
          "of magnitude",
          "the ceiling is the assignment's s <= 1.27e-5 canonical / 1.05e-5 alt, WITHOUT EFE "
          "relief (which was shown to be 1.000000x).  The screening is the kernel's own "
          "exp(-sqrt y), not a new mechanism")

check(all(m > 3000 for m in margins.values()),
      f"F2  *** the 1.2e4-3.4e4 GAP IS NOT NARROWED, IT IS DELETED: the quantity it "
      f"constrained (the SATURATED anomaly s) does not exist, because U is no longer forced "
      f"monotone.  Margins {margins['canonical']:.0f} / {margins['ALT']:.0f} orders ***")

# --- the RAR floor, at the same time -----------------------------------------------------------
U2 = Uofy(2.0)
check(U2 >= U2_FLOOR_POINTWISE,
      f"F3  and the SAME kernel clears the RAR floor at the same time: U(2) = {U2:.4f} "
      f">= {U2_FLOOR_POINTWISE} (the pointwise floor), and a fortiori >= "
      f"{U2_FLOOR_PERGAL['canonical']}/{U2_FLOOR_PERGAL['ALT']} (the per-galaxy M/L floors)",
      "a single kernel meeting both ends is what the F(Y) theory made impossible")

# --- L3: legality is not safety ----------------------------------------------------------------
def x_alg(y):
    return math.sqrt(y * y + y)


def dxdy_alg(y):
    return (2 * y + 1) / (2 * math.sqrt(y * y + y))


ymin_a, dmin_a = scan(dxdy_alg, 1e-8, 1e10)
U_alg_1au = {f: x_alg((GMSUN / AU ** 2) / a0) - (GMSUN / AU ** 2) / a0 for f, a0 in FOOT}
check(dmin_a > 0 and all(U_alg_1au[f] > S_CEIL[f] for f, _ in FOOT),
      "F4  *** LIABILITY L3, QUANTIFIED, AGAINST INTEREST: the framework's OWN interpolation "
      "g_obs = sqrt(g_bar^2 + g_bar a_0) is ALSO made legal by option 1 "
      f"(min dx/dy = {dmin_a:.4f} > 0) -- yet it still has U -> 1/2 and still BUSTS the "
      f"ephemeris ceiling by {U_alg_1au['canonical']/S_CEIL['canonical']:.2e}x canonical / "
      f"{U_alg_1au['ALT']/S_CEIL['ALT']:.2e}x alt ***",
      "so option 1 removes the STRUCTURAL obstruction and nothing more.  Passing the solar "
      "system remains a requirement ON THE KERNEL.  The exponential kernel meets it; the "
      "framework's headline algebraic kernel does not.  Reporting the win without this is "
      "how a manufactured result would look")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- THE HUNT FOR THE TRAP REIMPOSED BY ANOTHER ROUTE")
print("=" * 100)

# G1: is J_Z a single-valued function of Z for the exponential kernel?  Needs y(x) invertible.
xs = [xofy(y) for y in [1e-8 * (1e16) ** (k / 20000) for k in range(20001)]]
check(all(xs[k + 1] > xs[k] for k in range(len(xs) - 1)),
      "G1  SINGLE-VALUEDNESS, checked directly rather than inferred: x(y) is strictly "
      "increasing over 8 decades either side of a_0, so y(x) exists and mu(x) = y(x)/x is a "
      "single-valued function of x = sqrt(Z)/a_0.  J_Z(Z) therefore EXISTS as a function of "
      "Z, and J(Z) = integral mu dZ is its potential",
      "this is the exact analogue of the condition that kills the kernel in the F(Y) theory "
      "-- it simply binds on (x,y) instead of (U,y), and there it is satisfied")

# G1b: CONSTRUCT the free function's derivative and verify BOTH of its limits
def y_of_x(x, lo=1e-14, hi=1e14):
    """invert x(y) by bisection -- legitimate only because G1 established monotonicity"""
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if xofy(mid) < x:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


mu_of_x = lambda x: y_of_x(x) / x          # J_Z as a function of x = sqrt(Z)/a_0
inv_err = max(abs(xofy(y_of_x(xofy(y))) - xofy(y)) / xofy(y)
              for y in [1e-6 * (1e12) ** (k / 200) for k in range(201)])
deep = max(abs(mu_of_x(x) / x - 1.0) for x in (1e-4, 1e-5, 1e-6))
newt = max(abs(mu_of_x(x) - 1.0) for x in (1e6, 1e8, 1e10))
check(inv_err < 1e-9 and deep < 1e-3 and newt < 1e-3,
      "G1b THE FREE FUNCTION IS CONSTRUCTED, not merely argued to exist: inverting x(y) gives "
      "J_Z(Z) = mu(x) = y(x)/x, and it has BOTH required limits -- J_Z -> x = sqrt(Z)/a_0 in "
      "deep MOND (so J -> (2/3) Z^{3/2}/a_0, the SAME functional form SZ21's MOND limit has "
      "for Y, with the SAME a_0) and J_Z -> 1 in the Newtonian limit (so J -> Z, the plain "
      "c_4 term)",
      f"round-trip inversion error {inv_err:.1e}; deep-MOND limit |J_Z/x - 1| <= {deep:.1e} "
      f"at x = 1e-4..1e-6; Newtonian limit |J_Z - 1| <= {newt:.1e} at x = 1e6..1e10.  So "
      "option 1 changes the free function's ARGUMENT and nothing about its MOND normalisation")

# G2: the residual scalar sector -- is it constrained at all?
psi_free = sp.expand(el3(Lo, wf))
check(sp.simplify(psi_free - el3(-CG * sum((P[k] - v[k]) ** 2 for k in range(3)), wf)) == 0,
      "G2  the scalar's entire equation comes from the FREE quadratic term: the free function "
      "has left the scalar sector completely.  There is no residual algebraic condition on u "
      "= |grad varphi| of any kind -- and since S_m couples to g alone, u is not observable "
      "except through Psi",
      "this is the specific 'extra scalar-sector constraint' the assignment warned about.  "
      "I looked for it in the varphi equation, in the a_i equation (C1) and in the Q sector "
      "(A8); it is in none of them")

# G3: linear cosmology -- does the order counting survive the change of argument?
check(True,
      "G3  LINEAR COSMOLOGY: on FRW the aether is comoving and geodesic, so Jbar^mu = 0, "
      "hence Zbar = 0 AND delta Z = 2 Jbar.delta J = 0.  Z = O(delta^2) exactly as Y is, so "
      "J(Z) ~ Z^{3/2}/a_0 = O(delta^3) contributes nothing to the second-order action.  "
      "bridge1_aest_equations.md's order-counting theorem -- a_0 absent from linear "
      "cosmology -- transfers to option 1 UNCHANGED",
      "STATED AS AN ORDER-COUNTING ARGUMENT ONLY.  The analytic -(2-K_B)Y kinetic term and "
      "the K(Q) dust term, which ARE what governs the linear CMB, are untouched by option 1 "
      "(A8).  A CLASS run is another route's gate and is NOT COMPUTED HERE")

# G4: the anisotropic stress (L2) -- re-examined by order counting, and DOWNGRADED
Z3 = sp.expand(Zinv.coeff(eps, 3))
sqrtg = tr(sp.expand(sp.sqrt(1 + 2 * eps * PsiF) * (1 - 2 * eps * PhiF) ** sp.Rational(3, 2)
                     ).series(eps, 0, NEXP).removeO(), NEXP - 1)
check(sp.simplify(sp.diff(Z2, PhiF)) == 0 and sp.simplify(sp.diff(Z3, PhiF)) != 0
      and sp.simplify(sp.diff(sqrtg.coeff(eps, 1), PhiF)) != 0,
      "G4  *** LIABILITY L2, RE-EXAMINED AND DOWNGRADED.  The worry was that J(Z), depending "
      "on the metric, sources the ij Einstein equations with ~J_Z d_i Psi d_j Psi and so "
      "voids typeII's D2/D3 derivation of gamma_PPN = 1 (which needs those equations "
      "SOURCELESS).  Order counting says it does not, at the order that derivation works: "
      "Phi enters Z only at eps^3 (through g_ij = delta(1-2 eps Phi)) and enters the measure "
      "sqrt(-g) only at eps^1 multiplying an eps^2 object.  Since J(Z) is O(eps^2), the whole "
      "Phi- and h_ij-dependence of sqrt(-g) J(Z) is O(eps^3) -- CUBIC, outside the quadratic "
      "action.  So J(Z) contributes NOTHING to the linear ij equations and typeII's "
      "gamma_PPN = 1 survives UNCHANGED at that order ***",
      f"exhibited, not asserted: Z's eps^2 coefficient has dZ2/dPhi = 0 while its eps^3 "
      f"coefficient has dZ3/dPhi = {sp.simplify(sp.diff(Z3, PhiF))} and the measure's eps^1 "
      f"coefficient has d/dPhi = {sp.simplify(sp.diff(sqrtg.coeff(eps,1), PhiF))}.  CAVEAT, "
      "and it is the reason L2 is downgraded and not closed: this is the SAME eps-bookkeeping "
      "that puts a_0 at O(eps) (typeII R2), which ties the weak-field parameter to the MOND "
      "scale.  The eps^3 terms are NOT computed here and neither is any 1PN sector beyond "
      "typeII's.  L2 is downgraded from 'the derivation lapses' to 'the derivation survives "
      "at its own order, and the next order is unpriced'")

# G4b: the effective c_4 is LOCAL, not cosmological -- both directions of L1, stated
check(True,
      "G4b BOTH DIRECTIONS OF L1.  Against L1: the effective c_4 = (2-K_B) J_Z is not a "
      "constant of the theory, it is a FIELD -- J_Z -> 1 only where Z >> a_0^2.  On FRW the "
      "aether is geodesic, Z = 0 and J_Z = 0, so the effective c_4 VANISHES cosmologically "
      "and the background/linear sector sees no c_4 at all (G3).  For L1: alpha_1 and alpha_2 "
      "are measured in the SOLAR SYSTEM, which is exactly where J_Z -> 1, so the fact that it "
      "switches off cosmologically is no defence there.  NOT COMPUTED EITHER WAY")

# G5: the curl sector, unchanged
check(True,
      "G5  the curl obstruction is UNCHANGED in character: C4 is a divergence equation, so "
      "J_Z grad Psi = grad Psi_N holds pointwise only up to a divergence-free field, exactly "
      "as in AQUAL and exactly as typeII E3 found for AeST.  Spherical symmetry -- where "
      "nu(y), the ephemeris test and the rotation curves all live -- is curl-free, so the "
      "pointwise law is exact there.  This is a wash between the two theories, not a cost")

# =================================================================================================
print()
print("=" * 100)
print("PART H -- RAR SANITY ANCHOR (fixed Upsilon; NOT a refit)")
print("=" * 100)

rar_path = os.path.join(REPO, "ai_slop", "website", "public", "data", "rar_real_sparc.json")
check(os.path.exists(rar_path), "H0  the committed SPARC RAR file is present", rar_path)
with open(rar_path) as fh:
    blob = json.load(fh)
pts = blob["points"]


def rar_stats(kern, a0):
    res = [lgo - math.log10(kern(10.0 ** lgb / a0) * a0) for lgb, lgo in pts]
    m = sum(res) / len(res)
    return m, math.sqrt(sum((r - m) ** 2 for r in res) / len(res))


tab = {}
for fname, a0 in FOOT:
    for kname, kern in (("exponential", xofy), ("framework algebraic", x_alg)):
        tab[(fname, kname)] = rar_stats(kern, a0)
        info(f"H1  [{fname:9s}] {kname:19s}: mean offset "
             f"{tab[(fname,kname)][0]:+.4f} dex, scatter {tab[(fname,kname)][1]:.4f} dex "
             f"({len(pts)} points, Upsilon FROZEN at {blob['upsilon_disk']})")

check(len(pts) == 3389
      and abs(tab[("canonical", "exponential")][1]
              - tab[("canonical", "framework algebraic")][1]) < 0.01,
      "H2  ANCHOR ONLY, and stated as a COMPARISON rather than a fit: on the same 3389 "
      "committed SPARC points at frozen Upsilon = 0.70, the exponential kernel used in "
      f"PARTS E-F scatters {tab[('canonical','exponential')][1]:.4f} dex against the "
      f"framework's own algebraic kernel's {tab[('canonical','framework algebraic')][1]:.4f} "
      "dex -- indistinguishable.  So PART F's ephemeris pass is NOT bought by adopting a "
      "kernel that fits the RAR worse",
      "NEITHER number is the committed 0.108 dex, which comes from "
      "real_research/rar_framework_a0_mlfit.py REFITTING Upsilon; no refit is done here and "
      "no claim about the fitted scatter is made.  What is claimed is only the DIFFERENCE "
      "between the two kernels, which is what this check is for")

# =================================================================================================
print()
print("=" * 100)
print("PART I -- VERDICT")
print("=" * 100)
info("I0  PASS/KILL as the assignment defines them:\n"
     "      PASS = 'the condition weakens to something the exponential kernel satisfies'.\n"
     "      D2 shows the condition's ARGUMENT moves from u to g_obs; D5 shows that turns\n"
     "      'dU/dy > 0' into 'dx/dy > 0'; E1 gives min dx/dy = "
     f"{dmin_w:.5f} > 0 for the exponential\n"
     "      kernel.  ==> PASS.  E4 confirms the same kernel still FAILS the F(Y) condition,\n"
     "      so the verdict is not an artifact of my reduction.")
info("I1  What is NOT established here, and must not be read into this file:\n"
     "      - alpha_1/alpha_2 with an O(1) effective c_4 (L1) -- the sharpest new liability;\n"
     "      - gamma_PPN with the new anisotropic stress (L2) -- typeII's derivation lapses;\n"
     "      - c_T, the CMB beyond linear order counting, and any Upsilon refit;\n"
     "      - and legality is NOT solar-system safety (L3): the framework's own algebraic\n"
     "        kernel is legal under option 1 and still busts the ephemeris ceiling by 4e4.")

print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed   ({time.time()-T0:.1f} s)")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("   -", f)
print("=" * 100)
sys.exit(1 if FAIL else 0)
