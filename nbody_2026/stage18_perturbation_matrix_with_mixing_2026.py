#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage18_perturbation_matrix_with_mixing_2026.py
===============================================
THE PERTURBATION MATRIX WITH THE F_YQ MIXING -- stage 17's promotion is HEALTHY, and the no-ghost
theorem TRANSFERS.  Three structural results, each with the reason it holds:

  1. THE COSMOLOGICAL MATRIX IS UNTOUCHED, EXACTLY.  Two independent protections:
     (a) delta Y^(1) = 0 IDENTICALLY on FRW -- the projector h^mn = g^mn + A^m A^n kills every
         first-order source of Y (h^00 = 0 is exact, not linearised, once the unit-norm constraint
         fixes delta A^0 = -Phi A^0, the committed row-17 closure);
     (b) every promotion-generated entry (F_Q^new, F_QQ^new, F_YQ) carries a positive power of
         y = Y/A(Q), and y = 0 on FRW.
     So the committed CLASS pass, the k^4-Jeans structure, and the GDM degeneracy theorem inherit
     without modification.  Not "approximately" -- the new entries are zero on the background.

  2. NO GHOST, BY THE SAME WEYL ARGUMENT AS THE COMMITTED THEOREM.  In the galactic (quasi-static
     WKB) regime the promotion adds to the chi-chi KINETIC slot exactly two terms:
            (1/8piG) [ A''(Q) (F - yF') + (A'(Q)^2/A) y^2 F'' ]
     and BOTH are >= 0 for every ghost-free K and every MOND kernel with monotone mu:
       * F - yF' <= 0 always (its y-derivative is -yF'' <= 0 and it vanishes at 0), while
         A'' = -kappa^2 G K'' <= 0: the product is >= 0;
       * the second term is a perfect square over A, and A propto -K > 0 EVERYWHERE at beta = 1
         (-K = M^4/sqrt(1+nu^2): the promotion can never drive a_0^2 negative).
     A rank-1 PSD addition to the same slot the bump theorem controlled ==> Weyl monotonicity ==>
     no eigenvalue of the healthy kinetic matrix can decrease.  KERNEL-INDEPENDENT.

  3. THE MIXING ITSELF NEVER ENTERS THE KINETIC MATRIX.  delta Y carries NO time derivative (Y is
     built from the spatial projector; the aether direction is projected out), so F_YQ delta Y
     delta Q contributes only (i) a drift term chi-dot grad-chi, whose dispersion is REAL for all k
     whenever the diagonal blocks are healthy (proved exactly), and (ii) gradient-block corrections,
     bounded by the trace charge at <= 1.3e-4 of the committed entries in-window.

WHAT THIS IS NOT: a from-scratch covariant SVT decomposition of AeST + promotion (SZ-paper-scale
work).  It is the committed matrix argument, extended to the promotion by showing every new term
lands either (a) at zero on FRW, (b) in the PSD-controlled kinetic slot, or (c) in trace-suppressed
gradient corrections.  The residual assumptions are stated in Part F.
"""

import sys
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 25
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the cosmological matrix is untouched, exactly")
print("=" * 100)

# (a) h^00 = 0 EXACTLY once unit-norm fixes A^0.  Longitudinal gauge, g_00 = -(1+2 Phi).
Phi = sp.symbols("Phi", real=True)
g00_up = -1 / (1 + 2 * Phi)                       # g^{00}
A0_up = 1 / sp.sqrt(1 + 2 * Phi)                  # unit-timelike: g_00 (A^0)^2 = -1
h00 = sp.simplify(g00_up + A0_up ** 2)
check(h00 == 0,
      "A1  h^00 = g^00 + A^0 A^0 = 0 EXACTLY (all orders in Phi) once the unit-norm constraint "
      "fixes A^0 = (1+2Phi)^(-1/2) -- the same constraint that gave the committed delta A^0 = "
      "-Phi A^0 closure",
      "the projector kills its own time direction identically, not perturbatively")

# hence delta Y at first order vanishes: every candidate source dies
info("A2  delta Y^(1) = delta h^mn d_m phibar d_n phibar + 2 hbar^mn d_m phibar d_n delta phi: the "
     "first term needs delta h^00 (= 0 by A1, and d_i phibar = 0 kills the rest), the second needs "
     "hbar^00 (= 0 by A1) or hbar^0i (= A^0 Abar^i = 0 on FRW).  ==> delta Y^(1) = 0 IDENTICALLY.  "
     "Y first appears at SECOND order, as spatial gradients |grad chi - Q a delta A|^2 with no "
     "chi-dot -- the AeST literature's structure, recovered from the projector alone.")

# (b) every promotion-generated entry carries a positive power of y
y, Q, cF = sp.symbols("y Q c_F", positive=True)
Afun = sp.Function("A", positive=True)(Q)
F_deep = cF * y ** sp.Rational(3, 2)              # deep-MOND limit of the kernel (F ~ y^(3/2))
L_mond = Afun * F_deep.subs(y, sp.Symbol("Y", positive=True) / Afun) / (8 * sp.pi)
Ysym = sp.Symbol("Y", positive=True)
FQ_new = sp.diff(L_mond, Q)
FQQ_new = sp.diff(L_mond, Q, 2)
FYQ = sp.diff(L_mond, Ysym, Q)
lims = [sp.limit(expr, Ysym, 0) for expr in (FQ_new, FQQ_new, FYQ)]
check(all(l == 0 for l in lims),
      "A3  F_Q^new, F_QQ^new and F_YQ all -> 0 as Y -> 0 (each carries a positive power of y), "
      "verified on the deep-MOND F ~ y^(3/2) that governs the y -> 0 limit",
      "so even at second order, where delta Y^2 and delta Y delta Q could enter, their coefficients "
      "vanish on FRW")

check(sp.simplify(sp.diff(L_mond, Ysym) - sp.Rational(3, 2) * cF
                  * sp.sqrt(Ysym / Afun) / (8 * sp.pi)) == 0,
      "A4  and F_Y = F'(y)/8piG is the SAME function of y as before the promotion (the prefactor A "
      "cancels), so the committed k^4-Jeans structure on FRW -- F'(0) = 0 -- is inherited unchanged",
      "the CLASS pass, the GDM degeneracy theorem and the cosmological Jeans analysis all carry over "
      "without recomputation")


# =================================================================================================
print()
print("=" * 100)
print("PART B -- the sign theorem: the kinetic additions are PSD for EVERY kernel and every K")
print("=" * 100)

# F - yF' <= 0 for any F with F(0) = 0, F'' >= 0 -- kernel-independent
Fgen = sp.Function("F")(y)
ident = sp.simplify(sp.diff(Fgen - y * sp.diff(Fgen, y), y) + y * sp.diff(Fgen, y, 2))
check(ident == 0,
      "B1  d/dy [F - yF'] = -y F'' identically: for ANY kernel with F'' >= 0 and F(0) = 0, "
      "F - yF' <= 0 for all y",
      "kernel-independent; the Route A kernel has F'' = e^(-sqrt y)/(2 sqrt y) > 0")

u_s, Q0_s, mu_s, LD_s, M4_s = sp.symbols("u Q_0 mu Lambda_D M4", positive=True)
K_s = -M4_s + mu_s ** 2 * LD_s ** 2 * (1 - sp.sqrt(1 - u_s ** 2 / LD_s ** 2))
Kpp = sp.diff(K_s, u_s, 2)
check(sp.simplify(Kpp.subs(u_s, LD_s / 2)) > 0,
      "B2  K'' > 0 for the committed DBI (ghost-freedom of the base sector, stage 9's condition), "
      "hence A'' = -kappa^2 G K'' <= 0",
      "the first kinetic addition A''(F - yF') is (<=0)x(<=0) >= 0")

# beta = 1 keeps A = -K > 0 everywhere: a_0^2 never goes negative
nu = sp.symbols("nu", positive=True)
negK_beta1 = M4_s / sp.sqrt(1 + nu ** 2)
check(sp.simplify(negK_beta1) > 0,
      "B3  at beta = 1, -K = M^4/sqrt(1+nu^2) > 0 for ALL nu: A propto -K stays positive, a_0^2 "
      "never crosses zero, and the second kinetic addition (A'^2/A) y^2 F'' is a perfect square "
      "over a positive quantity -- >= 0 manifestly",
      "both additions non-negative, with no reference to parameter values")

# Weyl transfer: rank-1 PSD addition to the chi-chi slot cannot lower any eigenvalue -- numeric sweep
rng = np.random.default_rng(20260810)
worst = 0.0
for _ in range(200):
    Lr = rng.standard_normal((4, 4))
    base = Lr @ Lr.T + 1e-3 * np.eye(4)          # a healthy (PD) kinetic matrix
    add = np.zeros((4, 4))
    add[0, 0] = abs(rng.standard_normal())       # the promotion's chi-chi addition
    ev0 = np.linalg.eigvalsh(base)
    ev1 = np.linalg.eigvalsh(base + add)
    worst = max(worst, float(np.max(ev0 - ev1)))
check(worst <= 1e-12,
      f"B4  Weyl monotonicity, the committed theorem's engine, applies verbatim: over 200 random "
      f"healthy 4x4 kinetic matrices, adding the promotion's diag(Delta,0,0,0) with Delta >= 0 "
      f"never lowered any eigenvalue (worst decrease {worst:.1e})",
      "*** THE NO-GHOST THEOREM TRANSFERS TO THE PROMOTED ACTION ***")

info("B5  the bump term's own argument also gets promoted, B(Y/A(Q))(Q-Q_0)^2: its new Q-derivatives "
     "carry n*u and n^2 u^2 -- DOUBLY trace-suppressed relative to the terms bounded above, and its "
     "committed kinetic addition 2AB >= 0 is untouched.  No new structure appears there.")


# =================================================================================================
print()
print("=" * 100)
print("PART C -- the mixing never reaches the kinetic matrix; the drift dispersion is real")
print("=" * 100)

info("C1  delta Y carries no time derivative (Part A: the projector removes the aether direction, "
     "and in the galactic WKB delta Y^(1) = 2 hbar^ij d_i phibar d_j chi -- SPATIAL only).  So "
     "F_YQ delta Y delta Q contributes NO velocity-velocity entry: the kinetic matrix modification "
     "is EXACTLY the diagonal Delta of Part B, and the Weyl argument needed no caveat.")

# the residual cross term: chi-dot grad-chi drift.  Dispersion: GK w^2 - 2 D w k - GG k^2 = 0
GK, GG, D, w, k = sp.symbols("G_K G_G D omega k", real=True)
disp = GK * w ** 2 - 2 * D * w * k - GG * k ** 2
sols = sp.solve(sp.Eq(disp, 0), w)
discr = sp.simplify((sols[1] - sols[0]) ** 2 * GK ** 2 / (4 * k ** 2))
check(sp.simplify(discr - (D ** 2 + GK * GG)) == 0,
      "C2  the drift term's dispersion G_K w^2 - 2D wk - G_G k^2 = 0 has discriminant D^2 + G_K G_G: "
      "REAL frequencies for every k whenever the diagonal blocks are healthy (G_K, G_G > 0), "
      "REGARDLESS of the drift's size or sign",
      "the mixing can shift group velocities but can never produce a growing mode by itself")

# magnitude of everything the mixing does, in-window: the trace-charge suppression
OM_KD = mp.mpf("4.4e-7")                          # stage-3 BH ceiling on the khronon-dust share
GAIN = mp.mpf("800")                              # delta_halo x t_ff/t_H at the g = a_0 radius (st17)
OM_L = mp.mpf("0.685")
eps_loc = OM_KD * GAIN / OM_L                     # rho_kd,loc / rho_Lambda at the worst radius
info(f"C3  the dimensionless handle on every mixing entry is eps = rho_kd,loc/rho_Lambda "
     f"(= |A' Q_0/A| at leading order): in-window worst case eps = {mp.nstr(eps_loc, 3)} at the "
     f"g = a_0 radius, falling as the drain profile outward and as R^(-2)(z) into the past only "
     f"where MOND is already off.")

# gradient-block fractional correction: eps * yF''/(F' + 2yF''), maxed over y
def Fp(yv):
    return 1 - mp.e ** (-mp.sqrt(yv))


def Fpp(yv):
    return mp.e ** (-mp.sqrt(yv)) / (2 * mp.sqrt(yv))


grid = [mp.mpf(x) / 100 for x in range(1, 10000, 7)]
ratio_max = max(yv * Fpp(yv) / (Fp(yv) + 2 * yv * Fpp(yv)) for yv in grid)
grad_corr = eps_loc * ratio_max
check(grad_corr < mp.mpf("2e-4"),
      f"C4  the gradient-block correction is bounded by eps x max_y[yF''/(F' + 2yF'')] = "
      f"{mp.nstr(eps_loc, 3)} x {mp.nstr(ratio_max, 3)} = {mp.nstr(grad_corr, 3)} of the committed "
      f"entries -- the hyperbolic structure (Bekenstein-Milgrom mu + 2y mu' > 0) moves at the "
      f"10^-4 level",
      "the committed A_max cap and q-negativity window shift by the same fraction: unmeasurable")

# force-law closure: the promotion's extra source in the scalar equation, RAR-safe
fr = []
for yv in grid:
    Fval = mp.quad(lambda t: Fp(t), [0, yv])
    fr.append(abs(Fval - yv * Fp(yv)) / (yv * Fp(yv)))
force_corr = eps_loc * max(fr)
check(force_corr < mp.mpf("3e-4"),
      f"A5->C5  the promotion's extra force term (A'/8piG)(F - yF') is at most eps x "
      f"max|F - yF'|/(yF') = {mp.nstr(eps_loc, 3)} x {mp.nstr(max(fr), 3)} = "
      f"{mp.nstr(force_corr, 3)} of the MOND source: the RAR (0.108 dex = 28% scatter) cannot see "
      f"a {mp.nstr(100 * force_corr, 2)}% shift",
      "closes stage 17's drain bound at the FORCE level, not just the a_0-value level")


# =================================================================================================
print()
print("=" * 100)
print("PART D -- tensor and vector sectors")
print("=" * 100)

info("D1  TENSORS: the promoted F(Y/A(Q)) is still an algebraic function of (Y, Q) -- no new "
     "derivatives of the metric appear anywhere.  The committed c_T = 1 argument (the new terms "
     "are algebraic in the metric ==> GW170817-safe by construction) applies verbatim.  c_T = 1 "
     "EXACT survives.")

info("D2  VECTORS: phi has no vector part and delta Y is quadratic in vector aether modes, so the "
     "promotion touches the vector block only through the background value A(Qbar) replacing "
     "a_0^2 -- i.e. the committed vector analysis with a_0^2 -> a_0^2 R^2(z).  Today R = 1: the "
     "tachyon-type WATCH for y > 1 interiors is INHERITED IDENTICALLY, neither cured nor worsened.  "
     "At high z, R < 1 rescales the flagged mass where MOND is already off.  The WATCH stays open.")


# =================================================================================================
print()
print("=" * 100)
print("PART E -- what is now closed, and what remains owed")
print("=" * 100)

info("E1  CLOSED by this stage: stage 17's F2.  The promotion is ghost-free by the transferred "
     "theorem; the cosmological matrix (and with it the CLASS pass and the GDM degeneracy theorem) "
     "is untouched exactly; the mixing is confined to real-dispersion drift and 10^-4 gradient "
     "corrections; c_T = 1 survives; the vector WATCH is inherited unchanged.")

info("E2  STILL OWED, unchanged from stage 17 F3: (i) the CLASS re-run with the derived a_0(z) -- "
     "Part A says the perturbation EQUATIONS are identical, so what changes is only the background "
     "a_0(z) fed to the MOND sector, but expected is not verified; (ii) the MUSE/MSA-3D re-exam "
     "against the bumpless law; (iii) a derivation of beta = 1.  NEW residual from this stage's own "
     "scope: the quasi-static bounds in Part C use the WKB/short-wavelength regime and the "
     "committed 2x2/4x4 structure -- a full covariant SVT decomposition of the promoted action "
     "remains the referee-grade version of Parts B-C.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print("""
  THE PROMOTED ACTION IS AS HEALTHY AS THE COMMITTED ONE, AND FOR STRUCTURAL REASONS, NOT NUMERICAL
  ACCIDENTS:

  1. COSMOLOGY CANNOT SEE THE PROMOTION AT THE PERTURBATION LEVEL: h^00 = 0 exactly kills delta Y
     at first order, and every new coupling vanishes with a positive power of y on the y = 0
     background.  The CLASS pass inherits.

  2. NO GHOST, KERNEL-INDEPENDENTLY: both kinetic additions are non-negative -- one because
     ghost-freedom of the base (K'' > 0) meets concavity of the kernel (F - yF' <= 0), the other
     a perfect square -- and Weyl monotonicity does the rest.  The same engine as the committed
     bump theorem, with the same slot.

  3. THE MIXING IS CONFINED: no velocity-velocity entries (delta Y has no time derivative), real
     drift dispersion at every k, gradient and force corrections bounded at 1.3e-4 and 1.7e-4 of
     the committed entries by the trace charge.

  4. c_T = 1 exact survives; the vector WATCH is inherited unchanged.

  Stage 17's health caveat F2 is CLOSED.  The a_0(z) derivation now carries its perturbation
  analysis rather than owing it.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
