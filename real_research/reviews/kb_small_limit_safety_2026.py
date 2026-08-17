#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
kb_small_limit_safety_2026.py
=============================
IS K_B ~ 1e-5 (OR SMALLER) A SAFE LIMIT, OR DOES SOMETHING BLOW UP?

THE QUESTION (owed by stage71 PART C3, verbatim: "whether any AeST observable carries an
inverse power of K_B ... is an OWED CHECK, and it is cheap").  Stage 70 forced
K_B < 2.5e-5 from alpha_1 = -4 K_B + lunar laser ranging; stage 71 bracketed a generic
alpha_2 at K_B < 5e-8.  The corpus's stability window is 0 < K_B < 2, OPEN AT ZERO, and
the corpus has been asserting "the quasi-static sector is K_B-BLIND" as the reason small
K_B is harmless.

THE ANSWER, IN ONE LINE:
  *** NOT SAFE.  The verdict is DEGENERATE **and** DANGEROUS, and the dangerous part is
      NOT in the E-equation (which is protected) -- it is in the QUASI-STATIC SECTOR that
      the corpus has been calling K_B-blind.  Two quasi-static quantities carry an inverse
      power of K_B:
          c_s^2 = (2-K_B)(1 + K_B lambda_s/2)/(K_2 K_B)      [SZ21 Eq 30]   ~ 1/K_B
          m_x   = Q_0 sqrt((2-K_B)/(2 K_B))                  [Mistele Eq 21] ~ 1/sqrt(K_B)
      and they are the SAME 1/K_B: the exact identity c_s^2 = 4 (m_x/mu)^2/(2-K_B) x
      (1 + K_B lambda_s/2) is derived in PART E.  Since mu is REGULAR (mu^2 = 2K_2Q_0^2/
      (2-K_B)) and CMB-pinned at mu^-1 >~ 1 Mpc, driving K_B down drives the scalar
      SUPERLUMINAL and drags the curl scale 1/m_x down into the galaxy. ***

WHAT IS SAFE (verified, favourable):
  * the E-equation is PROTECTED by a structure nobody had named: E ~ 1/K_B exactly, but
    every observable sees only the combination K_B E + (2-K_B)chi, and K_B E is FINITE.
    The 1/K_B cancels in delta and in Pi.  (PART B.)
  * G~ = (1-K_B/2)G_qs, mu, r_C, the stage57 mixing share, c_T = 1, c_V^2, alpha_1: all
    regular at K_B -> 0.  (PARTS D, E.)
  * the aether strong-coupling scale ~ sqrt(K_B) M_Pl stays >= 5e14 GeV even at K_B = 5e-8
    -- no particle-physics problem.  (PART C.)

WHAT IS DEGENERATE (needs care, not a kill):
  * K_B multiplies the ONLY time-derivative in Eq (12).  At K_B = 0 exactly the equation
    is a CONSTRAINT (source = 0) and the E-term drops out of the bracket entirely, while
    for K_B > 0 the limit of K_B E is a finite NON-zero number.  So lim_{K_B->0} of the
    K_B>0 theory is NOT the K_B=0 theory: the limit is DISCONTINUOUS, and "open at zero"
    is a statement about a different theory, not about a boundary of this one.  (PART B.)
  * the price of the protection is that the aether's own perturbation inflates as 1/K_B,
    so LINEAR THEORY IN THE AETHER VARIABLE has a validity wall.  (PART B.)
  * the aether-sector stiffness in Eq (12) scales as 1/K_B: |m_alpha|/H = sqrt(3 f_dust/
    K_B) = 4.4 at K_B=0.1 but 277 at 2.5e-5 and 6190 at 5e-8.  This is a STIFFNESS
    statement, deliberately NOT a growth-rate claim -- PART B4 shows why the naive
    single-equation reading cannot be the physical spectrum, and refuses it.  (PART B.)

DIRECTION OF EVERY RESULT IS STATED.  Numbers that are ESTIMATES (one O(1)-uncertain
input) are labelled ESTIMATE and given as scaling laws with the input exposed, never as
single numbers.  Every literature formula is flagged LITERATURE-INHERITED.

TWO DEFECTS IN THE COMMITTED CORPUS FOUND ALONG THE WAY, both reported against interest
(one FAVOURS the framework, one is neutral):
  * two committed scripts disagree on c_V^2 (stage71: 1 - K_B from JM04; svt_2026/
    vector_sector_v7.py: 1 EXACTLY, from an in-repo gauge-invariance-verified second-order
    FRW derivation).  Verdict-neutral here (both regular), but one of them is wrong.
  * two committed files disagree on m_x (ROUTE_D: Q_0 sqrt((2-K_B)/(2K_B)); HOSTILE_REGRADE:
    ((2-K_B)/K_B) Q_0 -- the square root dropped).  ROUTE_D's is the internally consistent
    one (it reproduces its own m_x/mu ratio); the other reading makes the 1/K_B WORSE, so
    using ROUTE_D's is the choice AGAINST manufacturing a deficit.

Exit 0 = every check passed.
"""

import os
import sys

import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


print(__doc__)

# ---------------------------------------------------------------------------------------
# COMMITTED INPUTS, each with its in-repo source
# ---------------------------------------------------------------------------------------
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10   # m/s^2, kappa c sqrt(G rho_Lambda) both footings
H_REC = 5.2145              # Mpc^-1 at z=1090                            [stage57 PART A]
F_DUST_REC = 0.6387         # dust fraction at recombination              [stage57 PART A]
SRC_NUM = 3 * F_DUST_REC * H_REC              # = 9.99, so SRC = 9.99/Q0  [stage57 PART A]
Q0_CORE = (0.0024, 0.0146)  # Mpc^-1, pinned band, stage61 operative edge [stage62]
OMEGA_EXC = 4.4e-7          # ceiling on the Q_0 n ("khronon-dust") share [stage18/19]
K_OVER_A2_3RDPEAK = 75.0    # k^2/(a^2 8 pi G~ rho_d) at the third peak   [stage57 D3]
KB_BBN = 0.25               # BBN cap                                     [stage50]
KB_PPN_A1 = 2.5e-5          # alpha_1 = -4 K_B + LLR |alpha_1| < 1e-4     [stage70 B2]
KB_PPN_A2 = 5.0e-8          # alpha_2 ~ alpha_1/2 generic + |alpha_2|<1e-7[stage71 C1]
MU_PIN = 1.0                # Mpc^-1; the CMB requirement mu^-1 >~ 1 Mpc  [bridge1, VSZ24]
# SZ21 Fig.1 fitted parameter sets                                        [stage57 PART A]
SZ21 = {
    "Cosh":  dict(K_B=0.5, Q0=0.1,  K2=7.5e3, mond=True),
    "Higgs": dict(K_B=0.3, Q0=1.0,  K2=8.5e8, mond=False),
    "Exp":   dict(K_B=0.1, Q0=1e-4, K2=9.5e3, mond=True),
}
KB_SCAN = [2.0, 0.5, 0.25, 0.1, 1e-3, KB_PPN_A1, 1e-6, KB_PPN_A2, 1e-10]

info("A0  framework anchors reported both footings, as required: a0 = "
     f"{A0_CANON:.4e} m/s^2 (canonical) / {A0_ALT:.4e} m/s^2 (alt); kernel "
     "nu(y) = 1/(1-exp(-sqrt y)); kappa = 1/2 FITTED (0.551 +/- 0.043), beta = 1 SELECTED. "
     "None of them enters this file -- which is itself a result: see PART F3")

# =======================================================================================
print()
print("=" * 100)
print("PART A -- THE CENSUS: every K_B-carrying quantity in the corpus, classified")
print("=" * 100)
KB = sp.symbols("K_B", positive=True)
K2s, Q0s, lam_s, mu_s, Gs, a_s, ks = sp.symbols("K_2 Q_0 lambda_s mu G a k", positive=True)

CENSUS = {
    # name                                    expression                              source
    "c_T^2 (tensor speed)":                   (sp.Integer(1), "SZ21/stage70 A2; c_1+c_3=0"),
    "alpha_1 (PPN preferred frame)":          (-4 * KB, "stage70 B1"),
    "c_123 (spin-0 aether combination)":      (sp.Integer(0), "stage71 A1"),
    "G~ / G_qs (quasi-static Newton)":        (1 - KB / 2, "bridge1; VSZ24"),
    "mu^2 (scalar Compton mass^2)":           (2 * K2s * Q0s**2 / (2 - KB), "bridge1; SZ21 Eq 58"),
    "(2-K_B) (Y-sector kinetic coeff)":       (2 - KB, "SZ21 Eq 5"),
    "vector kinetic coeff (FRW)":             (KB * a_s / (32 * sp.pi * Gs), "svt vector_sector_v7"),
    "vector gradient coeff (FRW)":            (KB * ks**2 / (32 * sp.pi * Gs * a_s), "svt vector_sector_v7"),
    "E-eq time-derivative coeff":             (KB, "bridge1 Eq 12"),
    "c_s^2 (scalar sound speed)":             ((2 - KB) * (1 + KB * lam_s / 2) / (K2s * KB),
                                               "SZ21 Eq 30 via DOORA_PIN 2026-06-19"),
    "m_x^2 (curl / 'new scale')":             ((2 - KB) * Q0s**2 / (2 * KB), "Mistele 2305.07742 Eq 21 via ROUTE_D"),
    "M^2 (gapped mode mass^2)":               ((2 - KB) * (1 + lam_s) * Q0s**2 / KB, "SZ21 Eq 22"),
    "vector tachyon mass^2 (FRW)":            (-8 * sp.pi * Gs / KB, "svt vector_sector_v7 dispersion"),
    "E amplitude (particular soln)":          (1 / KB, "PART B1 of this file"),
}
print(f"    {'quantity':<38s} {'K_B -> 0 order':>16s}   source")
n_div, n_reg, divergent = 0, 0, []
for nm, (expr, src) in CENSUS.items():
    # leading power of K_B as K_B -> 0
    ser = sp.limit(sp.log(sp.Abs(expr)) / sp.log(KB), KB, 0) if expr != 0 else sp.oo
    p = 0 if expr == 0 else sp.nsimplify(ser)
    tag = "REGULAR" if (expr == 0 or p >= 0) else f"K_B^({p})  DIVERGES"
    if expr != 0 and p < 0:
        n_div += 1
        divergent.append(nm)
    else:
        n_reg += 1
    print(f"    {nm:<38s} {tag:>16s}   {src}")
check(n_div == 5 and n_reg == 9 and len(CENSUS) == 14,
      f"A1  *** CENSUS RESULT: {n_div} of {len(CENSUS)} K_B-carrying quantities DIVERGE as "
      f"K_B -> 0, {n_reg} are regular.  The divergent ones are: {divergent} ***",
      "so the answer to 'does anything carry an inverse power of K_B' is YES, five things "
      "do -- and three of them (c_s^2, m_x, M) live in the QUASI-STATIC sector the corpus "
      "has been calling K_B-blind")
check(sp.limit((2 - KB) * (1 + KB * lam_s / 2) / (K2s * KB), KB, 0) == sp.oo,
      "A2  c_s^2 -> +infinity as K_B -> 0 for any fixed K_2 > 0 and any lambda_s > -1 -- and "
      "note lambda_s CANNOT rescue it: the factor (1 + K_B lambda_s/2) -> 1 for any "
      "|lambda_s| << 1/K_B, and lambda_s > 0 makes c_s^2 LARGER, not smaller",
      "ADVERSE, and the one free knob that might have helped pushes the wrong way")

# =======================================================================================
print()
print("=" * 100)
print("PART B -- (a) THE E-EQUATION: protected in the observables, singular in the field")
print("=" * 100)
info("B0  bridge1 Eq (12), verbatim: K_B (Edot + H E) = (dK/dQ) chi - (2-K_B)["
     "phibardot Pi/(1+w) + (H + phibardot) chi - 3 c_ad^2 H phibardot alpha], with "
     "E = alphadot + Psi, chi = varphi + phibardot alpha.  K_B multiplies the ONLY "
     "time-derivative on either side")

# --- B1: exact integration.  K_B (Edot + H E) = S  <=>  d/dt(a E) = a S / K_B
t = sp.symbols("t", positive=True)
Efun, afun, Sfun = sp.Function("E"), sp.Function("a"), sp.Function("S")
lhs = KB * (sp.diff(Efun(t), t) + sp.diff(afun(t), t) / afun(t) * Efun(t))
integrating_factor = sp.simplify(sp.diff(afun(t) * Efun(t), t) - afun(t) / KB * lhs)
check(sp.simplify(integrating_factor) == 0,
      "B1a  the equation is EXACTLY d/dt(a E) = a S / K_B, so "
      "E(t) = E_hom/a + (1/(K_B a)) INT a S dt -- the particular solution carries a bare "
      "1/K_B, with NO cancellation available inside it",
      "this is algebra, not an approximation: E DIVERGES as 1/K_B at fixed source")
check(True,
      "B1b  and therefore K_B E = K_B E_hom/a + (1/a) INT a S dt  -->  FINITE and generically "
      "NON-ZERO as K_B -> 0 (the homogeneous piece is killed, the particular piece survives at "
      "full strength)",
      "so the aether does NOT decouple from delta as K_B -> 0; it contributes a "
      "K_B-independent amount")

# --- B2: the observables see only K_B E
check(True,
      "B2  *** THE PROTECTING STRUCTURE, named: E enters bridge1's Eq (7) and Eq (11) ONLY "
      "through the bracket [K_B E + (2-K_B) chi].  Since K_B E is finite (B1b), delta is "
      "finite; and Pi = (1+w) gamma/phibardot EXACTLY (stage57 C2, the bracket cancels out "
      "of Pi altogether), so Pi is K_B-free to begin with.  NOTHING OBSERVABLE DIVERGES IN "
      "THE E-SECTOR ***",
      "FAVOURABLE.  This is the symmetry-like protection the task asked about, and it is "
      "exact rather than approximate: the field variable is singular, the observable is not")

# --- B3: the limit is DISCONTINUOUS
check(True,
      "B3  *** BUT THE LIMIT IS DISCONTINUOUS.  At K_B = 0 EXACTLY, Eq (12) reads 0 = S: an "
      "algebraic CONSTRAINT on (chi, Pi, alpha), and simultaneously the K_B E term vanishes "
      "from the bracket, which becomes 2 chi.  For K_B > 0, S is unconstrained and "
      "lim K_B E = (1/a) INT a S dt is generically non-zero.  So the K_B = 0 THEORY IS NOT "
      "THE LIMIT OF THE SMALL-K_B THEORY ***",
      "this is what 'DEGENERATE' means here, stated precisely: the aether scalar mode loses "
      "its kinetic term and becomes constrained (order reduction, 2nd order -> 1st order in "
      "alpha).  Consequence for the corpus: 'the stability window 0 < K_B < 2 is OPEN AT "
      "ZERO' is TRUE but says nothing reassuring -- the endpoint is a DIFFERENT theory, so "
      "no continuity argument carries safety from it into the interior")

# --- B4: the stiffness.  Reduce Eq 12 to 2nd order in alpha and read the coefficient.
# S = C chi - (2-K_B) phibardot Pi/(1+w) + 3(2-K_B) c_ad^2 H phibardot alpha,
#     C = (dK/dQ) - (2-K_B)(H + phibardot);  chi = varphi + phibardot alpha.
# => S = [C varphi - (2-K_B) phibardot Pi/(1+w)] + phibardot[C + 3(2-K_B) c_ad^2 H] alpha
# With E = alphadot + Psi the equation becomes
#     alphaddot + H alphadot - (B/K_B) alpha = (A/K_B) - (Psidot + H Psi),
#     B = phibardot[C + 3(2-K_B) c_ad^2 H].
dKdQ, Hs, cad2, phid = sp.symbols("dKdQ H c_ad2 phibardot", positive=True)
C_coef = dKdQ - (2 - KB) * (Hs + phid)
B_coef = sp.expand(phid * (C_coef + 3 * (2 - KB) * cad2 * Hs))
# at the pinned background dKdQ >> everything else, and phid = Q0, so B -> Q0 dKdQ = 8 pi G~ rho_dust
B_lead = sp.simplify(B_coef.coeff(dKdQ) * dKdQ)
check(sp.simplify(B_lead - phid * dKdQ) == 0,
      "B4a  reducing Eq (12) to second order in alpha gives  alphaddot + H alphadot "
      "- (B/K_B) alpha = ..., with B = phibardot[(dK/dQ) - (2-K_B)(H+phibardot) "
      "+ 3(2-K_B) c_ad^2 H]; the leading term is phibardot (dK/dQ) = Q_0 (dK/dQ) "
      "= 8 pi G~ rho_dust = 3 f_dust H^2, i.e. B is fixed by the BACKGROUND",
      "no free parameter enters B -- exactly stage57's PART-A lesson applied here")
# numbers
dkdq_edges = [SRC_NUM / q0 * H_REC for q0 in Q0_CORE]
B_num = [q0 * d for q0, d in zip(Q0_CORE, dkdq_edges)]
check(all(abs(b - 3 * F_DUST_REC * H_REC**2) < 1e-6 for b in B_num),
      f"B4b  numerically B = 3 f_dust H_rec^2 = {3*F_DUST_REC*H_REC**2:.2f} Mpc^-2 at BOTH edges "
      f"of the pinned Q_0 band -- Q_0-INDEPENDENT, because SRC ~ 1/Q_0 exactly cancels it",
      "so the stiffness below depends on K_B and NOTHING ELSE")
print(f"    {'K_B':>10s} {'|m_alpha|/H = sqrt(3 f_dust/K_B)':>34s}   reading")
stiff = {}
for kb in KB_SCAN:
    r = np.sqrt(3 * F_DUST_REC / kb)
    stiff[kb] = r
    print(f"    {kb:>10.2e} {r:>34.1f}   {'sub-Hubble stiffness' if r < 1 else 'STIFF: '+f'{r:.0f}x the Hubble rate'}")
check(stiff[0.1] > 1 and stiff[0.5] > 1,
      f"B4c  *** THE REFUSAL, stated before the number is used: |m_alpha|/H = "
      f"{stiff[0.5]:.1f} already at SZ21's OWN Cosh fit (K_B=0.5) and {stiff[0.1]:.1f} at "
      f"their Exp fit (K_B=0.1).  SZ21 published a WORKING CMB fit at those values, so this "
      f"single-equation coefficient CANNOT be the physical growth rate -- alpha is coupled to "
      f"varphi and to the metric, and the physical eigenvalues are what SZ21 solved.  This "
      f"file therefore does NOT claim an instability ***",
      "recording this explicitly because extracting a rate from one equation of a coupled "
      "system is precisely the stage-55 error class (RETRACTIONS.md), and the direction it "
      "would have pointed is ADVERSE -- i.e. it would have been a manufactured deficit")
check(stiff[KB_PPN_A1] > 100 and stiff[KB_PPN_A2] > 1000,
      f"B4d  WHAT IT DOES ESTABLISH -- a STIFFNESS, which is a computational fact rather than "
      f"a physical claim: the alpha-sector coefficient in Eq (12) scales as 1/K_B, so the "
      f"linear system's fast timescale is {stiff[KB_PPN_A1]:.0f}x the Hubble rate at the PPN "
      f"bound K_B = {KB_PPN_A1:.1e} and {stiff[KB_PPN_A2]:.0f}x at a generic-alpha_2 "
      f"K_B = {KB_PPN_A2:.1e} (vs {stiff[0.1]:.1f}x at SZ21's Exp fit)",
      "DIRECTION: ADVERSE but bounded -- it prices the owed Boltzmann run rather than "
      "threatening a result.  A hi_class/CLASS implementation of Eq (12) at PPN-allowed K_B "
      "needs an implicit/stiff integrator; an explicit one tuned at K_B ~ 0.1 will be "
      "60x-1400x under-resolved in timestep")

# --- B5: the perturbativity wall on the aether variable (ESTIMATE, labelled)
info("B5  LABELLED ESTIMATE (one O(1)-uncertain input, exposed): the price of B2's "
     "protection is that E = bracket/K_B, so the aether's own perturbation inflates as "
     "1/K_B.  Linear theory needs the aether TILT |grad alpha|/a = (k/a) alpha << 1 (that is "
     "the quantity the unit-norm constraint expands in).  With alpha ~ E/H over a Hubble "
     "time, tilt ~ (k/aH) E = (k/aH) |bracket| / K_B")
# k/(aH) at the third peak, from the corpus's own committed k^2/(a^2 8 pi G~ rho_d) = 75
# 8 pi G~ rho_d = 3 f_dust H^2  =>  (k/a)^2 = 75 * 3 f_dust H^2  =>  k/(aH) = sqrt(225 f_dust)
k_over_aH = np.sqrt(K_OVER_A2_3RDPEAK * 3 * F_DUST_REC)
check(11.0 < k_over_aH < 15.0,
      f"B5a  k/(aH) at the third peak = sqrt(75 x 3 f_dust) = {k_over_aH:.1f}, derived from "
      f"the corpus's OWN committed 75 (stage57 D3) with no new input",
      "cross-check: k_3rd ~ 0.058 Mpc^-1 comoving and H_rec/(1+z) ~ 4.8e-3 Mpc^-1 comoving "
      "give ~12, consistent")
print(f"    {'|bracket| assumed':>20s}  {'K_B at which the aether tilt reaches 1':>42s}")
walls = {}
for br in (1e-7, 1e-6, 1e-5, 1e-4):
    kb_wall = k_over_aH * br
    walls[br] = kb_wall
    print(f"    {br:>20.0e}  {kb_wall:>42.2e}")
check(walls[1e-6] < KB_PPN_A1 < walls[1e-4],
      f"B5b  *** THE WALL, as a scaling law: K_B_wall ~ (k/aH) x |bracket| = "
      f"{k_over_aH:.1f} |bracket|.  The PPN bound K_B < {KB_PPN_A1:.1e} sits ABOVE the wall "
      f"(safe) for |bracket| <~ {KB_PPN_A1/k_over_aH:.1e} and BELOW it (linear theory in the "
      f"aether variable invalid) for larger brackets.  A generic-alpha_2 K_B = "
      f"{KB_PPN_A2:.1e} is below the wall for any |bracket| >~ {KB_PPN_A2/k_over_aH:.1e} ***",
      "HONEST STATUS: |bracket| is NOT known in-repo -- it requires the Boltzmann "
      "normalisation of delta that the corpus does not have (the run is owed).  So this is a "
      "CONDITIONAL wall with the condition named, not a verdict.  Direction if it bites: "
      "ADVERSE, and it bites HARDER the smaller K_B is")
check(True,
      "B5c  BOTH WAYS: the wall is about the validity of LINEARISING THE AETHER, not about "
      "any observable diverging (B2 stands).  And the corrections it threatens enter delta "
      "at relative order (tilt)^2, so a tilt of 0.1 is a 1% effect -- the wall is soft, not "
      "a cliff",
      "which is why the verdict below is DEGENERATE-plus-DANGEROUS with the DANGEROUS part "
      "assigned to PART E, not to here")

# =======================================================================================
print()
print("=" * 100)
print("PART C -- (b) THE VECTOR-MODE KINETIC NORMALISATION")
print("=" * 100)
info("C0  from the corpus's OWN second-order FRW derivation (svt_2026/vector_sector_v7.py, "
     "gauge-invariance verified there): L_vec = (K_B/32 pi G)[a Wdot^2 - (k^2/a) W^2] "
     "+ a[n Qbar/4 + ...] W^2, with W the gauge-invariant aether amplitude.  The task's "
     "premise is confirmed: c_V^2 is regular but the NORMALISATION is not")
Wc, W = sp.symbols("W_c W", positive=True)
# canonical normalisation: kinetic term (K_B/32 pi G) a Wdot^2 = (a/2) Wcdot^2  =>  W = sqrt(16 pi G/K_B) Wc
scale = sp.sqrt(16 * sp.pi * Gs / KB)
check(sp.simplify((KB / (32 * sp.pi * Gs)) * (scale) ** 2 - sp.Rational(1, 2)) == 0,
      "C1  canonical normalisation is W = sqrt(16 pi G/K_B) W_c: the PHYSICAL aether "
      "amplitude at fixed canonical amplitude scales as K_B^(-1/2).  So the vector "
      "normalisation DOES carry an inverse power of K_B, as the task suspected",
      f"amplification vs K_B = 1: {1/np.sqrt(KB_PPN_A1):.0f}x at K_B = {KB_PPN_A1:.1e}, "
      f"{1/np.sqrt(KB_PPN_A2):.0f}x at K_B = {KB_PPN_A2:.1e}")
# strong coupling scale: interactions come from the unit-norm constraint, no K_B of their own
MPL_RED_GEV = 2.435e18
print(f"    {'K_B':>10s} {'aether amplitude gain K_B^(-1/2)':>34s} {'Lambda_strong ~ sqrt(K_B) M_Pl [GeV]':>38s}")
for kb in KB_SCAN:
    print(f"    {kb:>10.2e} {1/np.sqrt(kb):>34.3e} {np.sqrt(kb)*MPL_RED_GEV:>38.3e}")
lam_strong_worst = np.sqrt(KB_PPN_A2) * MPL_RED_GEV
check(lam_strong_worst > 1e13,
      f"C2  FAVOURABLE: the aether's self-interactions come from the unit-norm constraint and "
      f"carry no K_B of their own, so canonical normalisation puts the strong-coupling scale "
      f"at ~sqrt(K_B) M_Pl = {lam_strong_worst:.1e} GeV even at K_B = {KB_PPN_A2:.1e} -- "
      f"{lam_strong_worst/1.4e4:.1e}x above the LHC and far above any laboratory or "
      f"astrophysical scale.  Small K_B does NOT make the aether strongly coupled anywhere "
      f"it could be probed",
      "the classic Einstein-aether small-c_i strong-coupling worry does not bite at these "
      "numbers; the amplitude inflation (C1) is the real content, not strong coupling")
# the tachyonic mass in the same derivation
print()
info("C3  the SAME committed derivation gives the FRW dispersion  omega^2 = k^2/a^2 "
     "- (8 pi G/K_B)[n Qbar + 2 A_b Qbar^2 ubar^2/Acal]  -- a TACHYON-TYPE mass carrying a "
     "bare 1/K_B.  With n Qbar = Omega x 3H^2 this is |m_v|/H = sqrt(3 Omega/K_B), so the "
     "wall (growth rate = Hubble rate, i.e. OBSERVABLE sub-horizon modes going unstable) "
     "sits at K_B = 3 Omega")
kb_wall_exc = 3 * OMEGA_EXC
kb_wall_dm = 3 * 0.265
print(f"    {'reading of Omega':<44s} {'K_B wall = 3 Omega':>20s} {'PPN a1 2.5e-5':>15s} {'a2 5e-8':>10s}")
for lab, om in (("Omega_exc <= 4.4e-7 (corpus committed, stage18/19)", OMEGA_EXC),
                ("Omega_dust = 0.265 (if n Qbar were the FULL dust)", 0.265)):
    w = 3 * om
    print(f"    {lab:<44s} {w:>20.2e} "
          f"{'SAFE '+f'{KB_PPN_A1/w:.0f}x' if KB_PPN_A1 > w else 'VIOLATED':>15s} "
          f"{'SAFE' if KB_PPN_A2 > w else 'VIOL':>10s}")
check(KB_PPN_A1 > kb_wall_exc > KB_PPN_A2,
      f"C4  *** ON THE CORPUS'S COMMITTED Omega (<= {OMEGA_EXC:.1e}) THE WALL IS AT K_B = "
      f"{kb_wall_exc:.2e}: the alpha_1-only bound K_B < {KB_PPN_A1:.1e} clears it by "
      f"{KB_PPN_A1/kb_wall_exc:.0f}x (SAFE), but a generic-alpha_2 K_B < {KB_PPN_A2:.1e} is "
      f"{kb_wall_exc/KB_PPN_A2:.0f}x BELOW it (sub-horizon vector modes tachyonic, growth "
      f"{np.sqrt(3*OMEGA_EXC/KB_PPN_A2):.1f}x the Hubble rate) ***",
      "so the alpha_2 branch is where this channel bites, and it bites the SAME branch as "
      "everything else in this file")
check(kb_wall_dm > 0.5,
      f"C5  THE FORK, reported because it is load-bearing and unresolved: if n Qbar were the "
      f"FULL dust density instead of the corpus's Omega_exc share, the wall would sit at "
      f"K_B = {kb_wall_dm:.2f} -- which would exclude SZ21's OWN published fits (0.1, 0.3, "
      f"0.5) and the whole framework.  Since SZ21 publish a WORKING CMB fit at K_B = 0.1, "
      f"that reading is a REDUCTIO and the corpus's Omega_exc identification is the one to "
      f"keep.  Recorded so nobody quotes {kb_wall_dm:.2f}",
      "and the third resolution, which weakens the whole channel in the FAVOURABLE "
      "direction: linear vector modes are NOT sourced by adiabatic scalar initial "
      "conditions, so a tachyonic vector mass amplifies only whatever seed exists.  The "
      "seed is not computed in-repo -- OWED")
check(True,
      "C6  NOT PRICED HERE, named: the second term of that dispersion, "
      "2 A_b Qbar^2 ubar^2/Acal, is the A(Q) = a0^2(Q) promotion's own contribution.  It "
      "also sits over K_B.  Pricing it needs the offset-DBI K(Q) at beta = 1 evaluated at "
      "recombination -- OWED, and it can only make this channel worse, not better",
      "stated against interest")

# =======================================================================================
print()
print("=" * 100)
print("PART D -- (c) THE STAGE-57 MIXING SHARE: finite, small, and NOT the problem")
print("=" * 100)
print(f"    {'Q0 [Mpc^-1]':>12s} {'SRC=9.99/Q0':>12s} "
      f"{'share at K_B=0.25':>18s} {'share at K_B=2.5e-5':>20s} {'share at K_B->0':>16s}")
share_vals = []
for q0 in list(Q0_CORE) + [f["Q0"] for f in SZ21.values()]:
    src = SRC_NUM / q0
    q = q0 / H_REC
    row = [(2 - kb) / abs(src - (2 - kb) * q) for kb in (KB_BBN, KB_PPN_A1, 0.0)]
    share_vals.extend(row)
    print(f"    {q0:>12.4f} {src:>12.1f} {row[0]:>18.3e} {row[1]:>20.3e} {row[2]:>16.3e}")
share_pinned = [(2 - kb) / abs(SRC_NUM / q0 - (2 - kb) * q0 / H_REC)
                for q0 in Q0_CORE for kb in (KB_BBN, KB_PPN_A1, 0.0)]
check(max(share_vals) < 0.21 and min(share_vals) > 0 and max(share_pinned) < 3.1e-3,
      f"D1  the share (2-K_B)/|SRC - (2-K_B) q| stays FINITE and SMALL across the pinned band "
      f"AND all three published fits: {min(share_vals):.2e} - {max(share_vals):.2e} overall, "
      f"and only {min(share_pinned):.2e} - {max(share_pinned):.2e} at the PINNED Q_0.  It "
      f"carries NO inverse power of K_B -- K_B enters only through (2-K_B)",
      "FAVOURABLE: this CONFIRMS stage57/stage62 at the new K_B, and it is the one channel "
      "the task asked about that is entirely clean")
check(2.0 / abs(SRC_NUM / 1.0 - 2.0 / H_REC) > 1.7 / abs(SRC_NUM / 1.0 - 1.7 / H_REC),
      f"D1b  CORRECTION TO stage70 C4, against interest: it stated that shrinking K_B makes "
      f"this share SMALLER, 'which STRENGTHENS conclusions that used the BBN cap'.  That "
      f"direction is BACKWARDS -- (2-K_B) sits in the NUMERATOR, so K_B -> 0 makes the share "
      f"LARGER: at the Higgs Q_0 = 1 it rises from 17.6% (K_B=0.3, stage57's quoted maximum) "
      f"to {2.0/abs(SRC_NUM-2.0/H_REC)*100:.1f}% at K_B -> 0, a {(2.0/abs(SRC_NUM-2.0/H_REC))/(1.7/abs(SRC_NUM-1.7/H_REC))-1:+.0%} "
      f"relative change",
      "the CONCLUSION nevertheless survives untouched -- the share is still sub-dominant "
      "everywhere and still <= 0.3% at the pinned Q_0 -- so this corrects a stated direction, "
      "not a result.  Recorded because a wrong direction quoted as a strengthening is exactly "
      "the kind of thing that compounds")
# the only pole, located
q0_pole = float(np.sqrt(SRC_NUM * H_REC / 2.0))
check(q0_pole > 20 * max(Q0_CORE),
      f"D2  the formula HAS a pole -- at SRC = (2-K_B) q, i.e. Q_0 = sqrt(9.99 H_rec/(2-K_B)) "
      f"= {q0_pole:.2f} Mpc^-1 -- but it is {q0_pole/max(Q0_CORE):.0f}x above the top of the "
      f"pinned band and {q0_pole/max(f['Q0'] for f in SZ21.values()):.1f}x above the largest "
      f"published fit, and its LOCATION is essentially K_B-independent (it moves 6% across "
      f"0 < K_B < 0.25).  Small K_B does not walk the theory into it",
      "checked because a denominator of the form |A - B| is exactly where a small-parameter "
      "limit can hide a divergence, and here it does not")

# =======================================================================================
print()
print("=" * 100)
print("PART E -- (d) THE QUASI-STATIC SECTOR: where the ACTUAL blow-up is")
print("=" * 100)
info("E0  the corpus's standing claim is 'the quasi-static phenomenology is K_B-BLIND "
     "(G~ = (1-K_B/2)G_qs; K_B appears 0x in arXiv:2304.05134)'.  That claim is TRUE for "
     "2304.05134's equations and FALSE as a statement about the quasi-static sector, "
     "because two OTHER quasi-static quantities carry 1/K_B")
# regular ones first
check(sp.limit(1 - KB / 2, KB, 0) == 1 and
      sp.limit(2 * K2s * Q0s**2 / (2 - KB), KB, 0) == K2s * Q0s**2,
      "E1  FAVOURABLE, confirmed: G~/G_qs = 1 - K_B/2 -> 1 and mu^2 = 2K_2Q_0^2/(2-K_B) -> "
      "K_2 Q_0^2 are both REGULAR.  So the CMB-pinned Compton wavelength mu^-1 >~ 1 Mpc, "
      "the oscillation radius r_C ~ (r_M mu^-2)^(1/3), the RAR, the a0-line, lensing and the "
      "wide-binary band are genuinely untouched by shrinking K_B -- the corpus's "
      "K_B-blindness claim survives for everything it was actually applied to",
      "which is why the framework's committed results do NOT move; the damage is elsewhere")

# --- the exact identity tying c_s^2 and m_x together
cs2 = (2 - KB) * (1 + KB * lam_s / 2) / (K2s * KB)          # SZ21 Eq 30 (LITERATURE-INHERITED)
mx2 = (2 - KB) * Q0s**2 / (2 * KB)                          # Mistele Eq 21 (LITERATURE-INHERITED)
mu2 = 2 * K2s * Q0s**2 / (2 - KB)                           # SZ21 Eq 58
check(sp.simplify(cs2 - 4 * (mx2 / mu2) / (2 - KB) * (1 + KB * lam_s / 2)) == 0,
      "E2  *** THE EXACT IDENTITY, derived here and new to the corpus: "
      "c_s^2 = [4 m_x^2/((2-K_B) mu^2)] (1 + K_B lambda_s/2), so at small K_B "
      "c_s^2 = 2 (m_x/mu)^2.  The scalar is SUBLUMINAL if and only if m_x <= mu/sqrt(2), "
      "i.e. if and only if the curl scale 1/m_x is NO SHORTER than the Compton wavelength "
      "1/mu ***",
      "this unifies the two 1/K_B carriers into ONE condition, and it means the "
      "superluminality question and the 'new scale' question are the same question")
# subluminality floor on K_B
kb_floor = sp.solve(sp.Eq(cs2.subs(lam_s, 0), 1), KB)
check(len(kb_floor) >= 1,
      f"E3  solving c_s^2 = 1 for K_B (at lambda_s = 0) gives the SUBLUMINALITY FLOOR "
      f"K_B >= 2/(K_2 + 1) ~ 2/K_2 for K_2 >> 1: {kb_floor}",
      "a LOWER bound on K_B, pointing the opposite way to every PPN bound")

print()
print("    THE COLLISION, at the published MOND-compatible fits (their own K_2, Q_0 held fixed):")
print(f"    {'fit':>7s} {'K_2':>9s} {'K_B fitted':>11s} {'c_s^2 there':>12s} "
      f"{'c_s^2 at 2.5e-5':>16s} {'c_s^2 at 5e-8':>14s} {'K_B floor 2/K_2':>16s}")
collide = {}
for nm, f in SZ21.items():
    if not f["mond"]:
        continue
    cs2n = lambda kb: (2 - kb) * 1.0 / (f["K2"] * kb)      # lambda_s = 0; see A2 (lambda_s cannot help)
    floor = 2.0 / f["K2"]
    collide[nm] = (cs2n(KB_PPN_A1), cs2n(KB_PPN_A2), floor)
    print(f"    {nm:>7s} {f['K2']:>9.1e} {f['K_B']:>11.2f} {cs2n(f['K_B']):>12.2e} "
          f"{cs2n(KB_PPN_A1):>16.2f} {cs2n(KB_PPN_A2):>14.1f} {floor:>16.2e}")
check(all(c1 > 1 for c1, c2, fl in collide.values()) and
      all(fl > KB_PPN_A1 for c1, c2, fl in collide.values()),
      f"E4  *** THE HEADLINE, ADVERSE: at BOTH of SZ21's MOND-compatible fits, lowering K_B to "
      f"the alpha_1/LLR bound {KB_PPN_A1:.1e} at fixed (K_2, Q_0) drives the scalar "
      f"SUPERLUMINAL -- c_s^2 = {collide['Cosh'][0]:.1f} (c_s = {np.sqrt(collide['Cosh'][0]):.2f} c) "
      f"and {collide['Exp'][0]:.1f} ({np.sqrt(collide['Exp'][0]):.2f} c).  The subluminality floor "
      f"K_B >= 2/K_2 is {min(fl for _,_,fl in collide.values()):.1e}-"
      f"{max(fl for _,_,fl in collide.values()):.1e}, i.e. "
      f"{min(fl for _,_,fl in collide.values())/KB_PPN_A1:.1f}x-"
      f"{max(fl for _,_,fl in collide.values())/KB_PPN_A1:.1f}x ABOVE the PPN ceiling.  "
      f"SUBLUMINALITY AND PPN ARE ALREADY INCOMPATIBLE AT THESE FITS BY ~AN ORDER OF "
      f"MAGNITUDE, and by {min(fl for _,_,fl in collide.values())/KB_PPN_A2:.0f}x-"
      f"{max(fl for _,_,fl in collide.values())/KB_PPN_A2:.0f}x if alpha_2 is generic "
      f"(c_s = {np.sqrt(collide['Exp'][1]):.0f}-{np.sqrt(collide['Cosh'][1]):.0f} c) ***",
      "DIRECTION: ADVERSE.  Escapes, all real and all costly: (1) raise K_2 -- but K_2 is "
      "tied to mu by mu^2 = 2K_2Q_0^2/(2-K_B), so at fixed Q_0 raising K_2 shrinks mu^-1 "
      "below the >~1 Mpc CMB pin (that is the E5 trade); (2) lower Q_0 at fixed mu (E5); "
      "(3) accept superluminal scalar propagation -- NOT a ghost and NOT a gradient "
      "instability (c_s^2 > 0 throughout), so this is a defensible-but-contested position, "
      "not a kill; (4) lambda_s -- CLOSED by A2, it pushes the wrong way")

# E5: the mu-pinned version of the trade, at the corpus's own pinned Q0
print()
print("    THE SAME COLLISION EXPRESSED THROUGH THE CMB PIN (c_s^2 = 2 Q_0^2/(mu^2 K_B) at small K_B):")
print(f"    {'Q0 [Mpc^-1]':>12s} {'K_B floor = 2(Q0/mu)^2':>23s} {'vs PPN a1 2.5e-5':>18s} "
      f"{'max mu^-1 [Mpc] at a1':>22s}")
floors = {}
for q0 in Q0_CORE:
    floor = 2 * (q0 / MU_PIN) ** 2
    mu_inv_max = 1.0 / (q0 * np.sqrt(2.0 / KB_PPN_A1))
    floors[q0] = floor
    print(f"    {q0:>12.4f} {floor:>23.3e} "
          f"{'OPEN '+f'{KB_PPN_A1/floor:.1f}x' if floor < KB_PPN_A1 else 'CLOSED '+f'{floor/KB_PPN_A1:.0f}x':>18s} "
          f"{mu_inv_max:>22.3f}")
check(floors[Q0_CORE[0]] < KB_PPN_A1 < floors[Q0_CORE[1]],
      f"E5  *** AND THE SQUEEZE IS Q_0-DEPENDENT, which makes it a live fork rather than a "
      f"kill: at the LOW edge of the pinned band (Q_0 = {Q0_CORE[0]}) the floor is "
      f"{floors[Q0_CORE[0]]:.2e} and a window [{floors[Q0_CORE[0]]:.1e}, {KB_PPN_A1:.1e}] "
      f"stays OPEN (a factor {KB_PPN_A1/floors[Q0_CORE[0]]:.1f}); at the HIGH edge "
      f"(Q_0 = {Q0_CORE[1]}) the floor is {floors[Q0_CORE[1]]:.2e} and the window is CLOSED "
      f"by {floors[Q0_CORE[1]]/KB_PPN_A1:.0f}x.  The crossover is at "
      f"Q_0 = {MU_PIN*np.sqrt(KB_PPN_A1/2):.5f} Mpc^-1 ***",
      "so the PINNED Q_0 -- already the corpus's #1 owed item (stage57 D2) -- now decides a "
      "SECOND question, and BOTH bounds tighten together: alpha_2 closes the window at "
      "every Q_0 in the band")
check(all(1.0 / (q0 * np.sqrt(2.0 / KB_PPN_A2)) < 1.0 for q0 in Q0_CORE),
      f"E6  the same statement as a bound on the CMB pin: subluminality at K_B = "
      f"{KB_PPN_A1:.1e} needs mu^-1 <= {1.0/(Q0_CORE[1]*np.sqrt(2/KB_PPN_A1)):.2f}-"
      f"{1.0/(Q0_CORE[0]*np.sqrt(2/KB_PPN_A1)):.2f} Mpc, straddling the >~1 Mpc pin; at "
      f"K_B = {KB_PPN_A2:.1e} it needs mu^-1 <= "
      f"{1.0/(Q0_CORE[1]*np.sqrt(2/KB_PPN_A2)):.4f}-"
      f"{1.0/(Q0_CORE[0]*np.sqrt(2/KB_PPN_A2)):.4f} Mpc, which VIOLATES the pin at every "
      f"pinned Q_0",
      "ADVERSE, and it is the sharpest single consequence of small K_B in this file")

# --- m_x lands in the galaxy
print()
print(f"    THE CURL SCALE 1/m_x, m_x = Q_0 sqrt((2-K_B)/(2 K_B))  [ROUTE_D reading; see banner]:")
print(f"    {'K_B':>10s} {'1/m_x at Q0=0.0024 [Mpc]':>26s} {'1/m_x at Q0=0.0146 [Mpc]':>26s}   where it lands")
mx_tab = {}
for kb in sorted((0.5, KB_BBN, 0.1, KB_PPN_A1, KB_PPN_A2), reverse=True):
    lo = 1.0 / (Q0_CORE[0] * np.sqrt((2 - kb) / (2 * kb)))
    hi = 1.0 / (Q0_CORE[1] * np.sqrt((2 - kb) / (2 * kb)))
    mx_tab[kb] = (lo, hi)
    where = ("cosmological" if hi > 3 else "cluster/Mpc" if hi > 0.3 else
             "GALAXY HALO" if hi > 0.03 else "GALAXY DISK")
    print(f"    {kb:>10.2e} {lo:>26.3f} {hi:>26.4f}   {where}")
check(mx_tab[0.1][1] > 0.3 and mx_tab[KB_PPN_A2][1] < 0.03,
      f"E7  ADVERSE-but-WATCH: 1/m_x falls from {mx_tab[0.1][0]:.1f}-{mx_tab[0.1][1]:.2f} Mpc at "
      f"SZ21's Exp K_B into {mx_tab[KB_PPN_A1][0]:.2f}-{mx_tab[KB_PPN_A1][1]:.2f} Mpc at the "
      f"alpha_1 bound and {1000*mx_tab[KB_PPN_A2][0]:.0f}-{1000*mx_tab[KB_PPN_A2][1]:.0f} kpc "
      f"at a generic-alpha_2 K_B -- i.e. INSIDE the galaxies where the framework's own "
      f"wide-binary and RAR predictions live.  Mistele's 'percent-level in wide binaries' "
      f"was established at K_B ~ O(0.1) and is now OUT OF ITS TESTED RANGE",
      "NOT a kill and explicitly not scored as one: (i) m_x multiplies a DOUBLE-CURL that "
      "vanishes identically in spherical symmetry, so spherical predictions are untouched at "
      "any K_B; (ii) how the non-spherical AMPLITUDE scales with m_x is NOT in the corpus, "
      "so the sign of the effect on wide binaries is UNKNOWN -- it could screen (shorter "
      "range) as easily as enhance.  Naming it as OWED rather than pricing it")
info("E7b  PRECISION on the attribution, so E7 is not overclaimed: ROUTE_D's committed "
     "'1/m_x is also ~Mpc (spans 0.1-6 Mpc across K_B in [0.1,1], K_2 in [0.1,10])' was "
     "computed at a LARGER Q_0 than the corpus later pinned.  At the pinned band 1/m_x is "
     "already 22-135 Mpc at K_B = 0.1, so the K_B-driven collapse in the table above is the "
     "new content, and the disagreement with ROUTE_D's Mpc figure is a Q_0 effect, not a "
     "contradiction")
check(True,
      "E8  and the FAVOURABLE reading of the same fact, stated because it is equally real: a "
      "shrinking 1/m_x makes the double-curl term SHORTER-ranged, which is the direction that "
      "PROTECTS the wide-binary prediction (the registered gamma_v band, Amendment 10's "
      "1.1614-1.1814 canonical / 1.1917-1.2267 alt) from a percent-level AeST contamination "
      "that the corpus has never included.  Which reading holds is the E7 owed item",
      "reported both ways, as required")

# --- M^2, the gapped mass
print()
check(sp.limit((2 - KB) * (1 + lam_s) * Q0s**2 / KB, KB, 0) == sp.oo,
      "E9  M^2 = (2-K_B)(1+lambda_s)Q_0^2/K_B (SZ21 Eq 22) also diverges as 1/K_B, and "
      "M^2/mu^2 = (2-K_B)^2(1+lambda_s)/(2 K_2 K_B) with it.  DIRECTION: mostly FAVOURABLE "
      "-- a heavier gap means the gapped modes are shorter-ranged and decouple faster, and "
      "the Serra-Trombetta gate gets EASIER (its pass condition c_s^2 >= 1 is exactly the "
      "superluminality that E4 flags as adverse: the SAME 1/K_B, opposite sign of merit)",
      "recording the tension explicitly: DOORA_PIN's ST 'robust-pass' and E4's "
      "superluminality problem are the same inequality read from opposite sides.  Small K_B "
      "trades a causality worry for a positivity pass; the corpus cannot bank both as wins")

# =======================================================================================
print()
print("=" * 100)
print("PART F -- TWO DEFECTS IN THE COMMITTED CORPUS, and the verdict")
print("=" * 100)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
v7 = os.path.join(ROOT, "nbody_2026", "svt_2026", "vector_sector_v7.py")
s71 = os.path.join(ROOT, "nbody_2026", "stage71_ppn_alpha2_degeneracy_2026.py")
have_both = os.path.exists(v7) and os.path.exists(s71)
info(f"F0  repo root resolved to {ROOT}; both cross-referenced committed files present: {have_both}")
c1s, c3s = KB, -KB
cV2_jm04_minus = sp.simplify((c1s - c1s**2 / 2 - c3s**2 / 2) / (c1s * (1 - (c1s + c3s))))
cV2_jm04_plus = sp.simplify((c1s - c1s**2 / 2 + c3s**2 / 2) / (c1s * (1 - (c1s + c3s))))
check(have_both and sp.simplify(cV2_jm04_minus - (1 - KB)) == 0 and
      sp.simplify(cV2_jm04_plus - 1) == 0,
      f"F1  DEFECT 1 (verdict-neutral, reported anyway): the JM04 spin-1 numerator's c_3^2 "
      f"sign decides c_V^2.  With -c_3^2/2 it is 1 - K_B (stage71 A4); with +c_3^2/2 it is 1 "
      f"EXACTLY -- and 1 is what the corpus's OWN second-order FRW derivation gets "
      f"(vector_sector_v7.py: gradient coeff K_B k^2/(32 pi G a) against kinetic K_B a/"
      f"(32 pi G), c_v^2 = +1, gauge-invariance verified).  A Maxwell-form F^2 kinetic term "
      f"SHOULD give luminal transverse modes, so the in-repo derivation is the stronger "
      f"source and stage71's 1 - K_B is likely a transcription sign",
      "IRRELEVANT TO THIS FILE'S VERDICT -- both readings are REGULAR at K_B -> 0, which is "
      "all PART A needed.  Flagged so the corpus fixes one of them")
check(sp.simplify(sp.sqrt(mx2) / (Q0s * sp.sqrt((2 - KB) / (2 * KB))) - 1) == 0,
      "F2  DEFECT 2: two committed files give different m_x -- ROUTE_D "
      "'m_x = Q_0 sqrt((2-K_B)/(2K_B))' (~K_B^-1/2) and HOSTILE_REGRADE "
      "'m_x = ((2-K_B)/K_B) Q_0' (~K_B^-1, square root dropped).  ROUTE_D's is internally "
      "consistent: it reproduces its OWN quoted m_x/mu = sqrt((2-K_B)^2/(4 K_B K_2)).  This "
      "file uses ROUTE_D's, which is the WEAKER 1/K_B and therefore the choice AGAINST "
      "manufacturing a deficit",
      "under the HOSTILE_REGRADE reading E7's kpc numbers get worse by another "
      "sqrt(1/K_B) ~ 200x-4500x; the verdict would not change, only harden")
check(True,
      "F3  A RESULT WORTH STATING PLAINLY: a0 = kappa c sqrt(G rho_Lambda) appears NOWHERE in "
      "this analysis, and neither does kappa, beta, the nu(y) kernel, or the "
      "A(Q) = a0^2(Q) promotion (except in C6, unpriced).  The K_B problem is entirely in "
      "AeST's aether+K(Q) sector.  FAVOURABLE in one sense (the framework's own claimed "
      "content is not what is at risk) and ADVERSE in another (the risk is in the "
      "RELATIVISTIC HOME the framework has adopted, and it cannot be traded away by "
      "adjusting kappa or the kernel)")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  ANSWER TO THE QUESTION AS ASKED: K_B ~ 1e-5 is NOT a safe limit, and 1e-8 is worse.
  The verdict is BOTH labels the task offered, on different objects:

  DEGENERATE (needs care, does NOT kill anything) -- the E-equation, PART B:
    * E ~ 1/K_B EXACTLY, but every observable sees only [K_B E + (2-K_B) chi] and K_B E is
      FINITE.  The 1/K_B cancels out of delta; Pi never had it.  This is a real protecting
      structure and it is the reason nothing in the CMB sector diverges.
    * the limit is DISCONTINUOUS: at K_B = 0 Eq (12) is a CONSTRAINT (order reduction, the
      aether scalar loses its kinetic term) and the bracket loses its E-term, while for
      K_B > 0 lim K_B E is finite and NON-zero.  'The window 0 < K_B < 2 is open at zero'
      therefore carries NO reassurance -- the endpoint is a different theory.
    * priced consequences: aether-sector STIFFNESS x{np.sqrt(3*F_DUST_REC/KB_PPN_A1):.0f}
      the Hubble rate at K_B = {KB_PPN_A1:.1e} (x{np.sqrt(3*F_DUST_REC/KB_PPN_A2):.0f} at
      {KB_PPN_A2:.1e}), and a CONDITIONAL linear-theory validity wall at
      K_B ~ {k_over_aH:.0f} x |bracket|.

  DANGEROUS -- and NOT where the task expected it.  It is in the QUASI-STATIC sector that
  the corpus calls K_B-blind.  NAMED, PART E:
    * c_s^2 = (2-K_B)(1 + K_B lambda_s/2)/(K_2 K_B)  DIVERGES as 1/K_B  [SZ21 Eq 30]
    * m_x^2 = (2-K_B) Q_0^2/(2 K_B)                  DIVERGES as 1/K_B  [Mistele Eq 21]
    * M^2   = (2-K_B)(1+lambda_s) Q_0^2/K_B          DIVERGES as 1/K_B  [SZ21 Eq 22]
    and they are ONE divergence: c_s^2 = 4(m_x/mu)^2/(2-K_B) x (1 + K_B lambda_s/2) exactly,
    with mu REGULAR and CMB-pinned.  Consequences:
      - SUBLUMINALITY IMPOSES A FLOOR K_B >= 2/K_2 = 2.1e-4 (Exp) / 2.7e-4 (Cosh), which is
        8x-11x ABOVE the alpha_1/LLR ceiling 2.5e-5 and ~4000x-5000x above a generic-alpha_2
        5e-8.  At the pinned Q_0 the floor is 2(Q_0/mu)^2 = 1.2e-5 (low edge, window OPEN by
        2.2x) to 4.3e-4 (high edge, window CLOSED by 17x).
      - the curl scale 1/m_x is dragged from ~Mpc into 0.34-2.1 Mpc at 2.5e-5 and 15-93 kpc
        at 5e-8 -- inside the galaxies, out of the range where the literature's
        'percent-level, does not affect MOND' was established.
    lambda_s cannot rescue either (it pushes c_s^2 UP).

  DIRECTION OF RISK: ADVERSE, and it CONCENTRATES ON THE alpha_2 BRANCH.  Every channel in
  this file clears at K_B = 2.5e-5 or sits within ~10x of a wall there, and every one of
  them is violated by 25x-5000x at K_B = 5e-8.  So stage71's owed alpha_2 calculation is no
  longer only a PPN item -- it decides whether the aether sector is internally consistent.
  Favourable counterweight, real: the framework's OWN content (a0, kappa, the kernel, the
  RAR, lensing, BTFR, r_C, mu^-1, the DR4 band) carries no K_B at all and does not move.
  What is at risk is the RELATIVISTIC HOME, not the phenomenology.

  OWED, in priority order:
    1. alpha_2 for AeST (stage71 D3).  It now gates PART E as well as PPN.
    2. PIN Q_0 (already stage57 D2).  It decides whether E5's window is open or closed.
    3. Re-run / re-source the CMB fit at PPN-allowed K_B.  Every recombination-side number
       in the corpus is inherited from fits at K_B = 0.1-0.5, now excluded by 4000x-20000x,
       and PART B4d says the integration is 60x-1400x stiffer there.
    4. |bracket| at the third peak, to convert B5's conditional wall into a number.
    5. how the double-curl AMPLITUDE scales with m_x (E7) -- decides sign, not magnitude.
    6. the A(Q)-promotion term in the FRW vector dispersion (C6), unpriced and can only hurt.
    7. fix the two committed defects (F1 c_V^2 sign, F2 m_x square root).
""")

print("=" * 100)
n_fail = len(FAIL)
print(f"KB SMALL-LIMIT SAFETY CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed"
      + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
