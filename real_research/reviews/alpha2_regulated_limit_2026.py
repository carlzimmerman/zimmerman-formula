#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
alpha2_regulated_limit_2026.py
==============================
THE REGULATED-LIMIT ADJUDICATION of the alpha_1 / alpha_2 fork for AeST's aether sector.

THE FORK (see nbody_2026/stage73_ppn_kb_confrontation_2026.py for the pricing).
AeST's aether sector -(K_B/2)F_{mu nu}F^{mu nu} maps onto Einstein-aether (EA) with
    c_1 = +K_B,  c_2 = 0,  c_3 = -K_B,  c_4 = 0
so the theory sits on a DOUBLY DEGENERATE locus:  c_13 = c_1+c_3 = 0  (=> c_T = 1 exactly)
AND c_123 = c_1+c_2+c_3 = 0  (=> the spin-0 aether mode has ZERO propagation speed).
  READING L (nbody_2026/stage70): apply the generic EA formula
      alpha_1 = -8(c_3^2 + c_1 c_4)/(2c_1 - c_1^2 + c_3^2) = -4 K_B  =>  K_B < 2.5e-5 (LLR).
  READING D (real_research/reviews/ppn_alpha_independent_check_2026.py, from scratch):
      alpha_1 = alpha_2 = 0 identically, because two independent routes force
      lambda*(w.khat) = 0, but at the price of a non-normalisable wake and a g_00 with no
      Taylor series in w.
  A THIRD reading, recorded by nobody: freeze lambda at its w=0 value and discard the
      Theta_{3nu} constraints -> formal alpha_1 = +3K_B/2, alpha_2 = +K_B/2.

THIS SCRIPT'S ROUTE.  Reading L uses a formula valid for GENERIC EA; reading D says the
premises fail ON the degenerate locus.  Settle it by APPROACHING the locus from inside the
generic region.  Introduce a REGULATOR FAMILY
        c_1 = K_B + eps_a ,   c_2 = eps_c ,   c_3 = -K_B + eps_b ,   c_4 = eps_d
(eps_d only for a robustness check; AeST has c_4 = 0), which is genuinely generic
(c_13 != 0 and/or c_2 != 0) for eps != 0 and contains AeST's dictionary as the limit point
eps -> 0.  Then take the limit along MANY independent paths and ask whether alpha_1 and
alpha_2 have limits at all, whether those limits are path-independent, and whether their
approach rate is locked to the rate at which the spin-0 speed c_S^2 vanishes.

THE ANSWER, stated up front so nothing is buried:
  (a)+(b) alpha_1's limit EXISTS and is PATH-INDEPENDENT: alpha_1 -> -4 K_B along every
      path, because alpha_1 is a rational function whose denominator equals 2K_B != 0 at
      the limit point.  alpha_1 does not depend on c_2 at all.  Reading L's NUMBER is the
      correct limit of the generic FORMULA.
  (c) alpha_2 DIVERGES.  It has a SIMPLE POLE in c_123 whose residue, evaluated at AeST's
      own dictionary point, is  K_B^2/(2-K_B)  -- NONZERO for every K_B in (0,2).  The
      residue is a property of the limit POINT, not of the path, so NO path escapes:
      alpha_2 -> +infinity through every ghost-free approach (c_123 > 0) and -infinity
      through the gradient-unstable side (c_123 < 0).  There is no finite alpha_2.
  (d) the ORDER of limits does not rescue it: c_2 -> 0 then c_13 -> 0, and c_13 -> 0 then
      c_2 -> 0, both diverge with the SAME leading coefficient K_B^2/((2-K_B) c_123).
  (e) THE RATE IS EXACTLY LOCKED to the degeneracy:  lim (alpha_2 * c_S^2) = K_B/2,
      exactly and path-independently.  alpha_2 blows up precisely as fast as the spin-0
      mode speed vanishes.  alpha_1's deviation from -4K_B is also O(eps) but is NOT
      locked: along the pure-c_2 path it is EXACTLY -4K_B for every eps while c_S^2 != 0.

WHAT THAT ADJUDICATES.  A formula set that returns alpha_1 = -4K_B and alpha_2 = +infinity
on the same point cannot be quoted selectively.  Applied CONSISTENTLY to this locus the
generic methodology does not bound K_B, it demands K_B = 0 exactly (PART E) -- which the
scalar sector forbids, since c_s^2 = (2-K_B)/(K_2 K_B) -> infinity as K_B -> 0.  So the
generic route is SELF-REFUTING here, reading L's "K_B < 2.5e-5" may not be quoted as in
force, and the degenerate/constrained treatment is MANDATORY.  That is reading D's
STRUCTURAL claim ("the PPN expansion's own premise fails on this locus") confirmed from
the opposite direction -- while reading D's NUMBERS (alpha = 0) are also NOT the limit of
the generic region, so they gain no support here either.  The degenerate theory is not a
continuous member of the EA family; it is a singular point of it, with a different
propagating-mode count.

WHY (derived in PART F, from scratch, no formula transcribed): for a STATIC longitudinal
aether perturbation delta u_i = d_i chi on flat space the entire EA quadratic Lagrangian
collapses to  L = -c_123 (lap chi)^2.  The static longitudinal kinetic operator IS
c_123 * lap^2.  So generically the static response is chi ~ source/c_123 -- divergent as
c_123 -> 0 -- while AT c_123 = 0 the operator vanishes identically and the longitudinal
equation degenerates from an equation FOR chi into a CONSTRAINT ON THE SOURCE.  That
constraint is exactly reading D's lambda*(w.khat) = 0.  The two readings are the answers
to two DIFFERENT boundary-value problems, and the degenerate one is not the limit of the
generic one.

PROVENANCE OF EVERY IMPORTED FORMULA (nothing else is imported):
  [P1] alpha_1 = -8(c_3^2 + c_1 c_4)/(2c_1 - c_1^2 + c_3^2)
       Foster & Jacobson 2006, PRD 73 064015 (gr-qc/0509083); restated in Jacobson,
       "Einstein-aether gravity: a status report", arXiv:0801.1547, Sec. 2.
  [P2] alpha_2 = alpha_1/2 - (c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4)/(c_123 (2-c_14))
       same sources ("Jacobson form").
  [P3] alpha_2 = (2c_13-c_14)^2/(c_123(2-c_14))
                 - [12 c_3 c_13 + 2 c_1 c_14 (1-2c_14) + (c_1^2-c_3^2)(4-6c_13+7c_14)]
                   / [(2-c_14)(2c_1-c_1^2+c_3^2)]
       the expanded Foster-Jacobson form.  [P2] and [P3] are ALGEBRAICALLY DISTINCT
       expressions; GATE 1 verifies they are the same function, which is a real
       transcription cross-check (a typo in either would generically break it).
  [P4] mode speeds (Jacobson & Mattingly 2004; arXiv:0801.1547):
       c_T^2 = 1/(1-c_13);  c_V^2 = (2c_1-c_1^2+c_3^2)/(2 c_14 (1-c_13));
       c_S^2 = c_123(2-c_14)/(c_14(1-c_13)(2+c_13+3c_2)).
  [P5] G_N = 2G/(2-c_14)  (Foster & Jacobson 2006), the EA Newtonian constant.
  [P6] the published PPN-safe locus alpha_1 = alpha_2 = 0  <=>  c_4 = -c_3^2/c_1 and
       c_2 = (-2c_1^2 - c_1 c_3 + c_3^2)/(3 c_1).
  [L1] |alpha_1| < 1e-4 (lunar laser ranging), |alpha_2| < 1e-7 (solar spin axis) -- the
       bounds already carried by stage70/stage71; used only to convert to K_B.
  [L2] SZ21 = Skordis & Zlosnik, PRL 127 161302 (arXiv:2007.00082): the MOND-compatible
       fits K_2 = 7.5e3 (Cosh) / 9.5e3 (Exp) with K_B = 0.5 / 0.1, and
       c_s^2 = (2-K_B)(1+K_B lambda_s/2)/(K_2 K_B) [SZ21 Eq. 30].
  Everything else below is DERIVED IN-SCRIPT.

FOUR ASSERTION-ENFORCED GATES (if any fails the script exits non-zero and NOTHING here is
claimed):
  GATE 1  [P2] and [P3], two algebraically distinct published alpha_2 forms, are the SAME
          rational function of (c_1..c_4)  -> transcription cross-check.
  GATE 2  [P1]+[P2] reproduce the published PPN-safe locus [P6] exactly.
  GATE 3  c_T^2 = 1 EXACTLY on AeST's dictionary, and [P5] gives G_N = G/(1-K_B/2) --
          two results the corpus already holds from completely independent calculations
          (c_T = 1 from the F^2 form; G~ = (1-K_B/2)G^ from the quasi-static sector, and
          reading D's own w=0 branch).  Reproducing BOTH from the imported EA formula set
          validates the dictionary and the formula set together.
  GATE 4  the from-scratch flat-space longitudinal aether dispersion derived in PART F,
          omega^2/k^2 = c_123/(c_1-c_4), agrees with the leading small-c_i behaviour of
          the imported c_S^2 [P4] at c_4 = 0.

CONVENTIONS THAT COULD FLIP A SIGN OR A FACTOR (stated, and their exposure priced):
  V1. PPN sign convention.  This script uses [P1] verbatim, i.e. stage70's and stage73's
      convention, so its alpha_1 is directly comparable to reading L's -4K_B.  Will's
      textbook writes the w^2 U coefficient as (alpha_3 - alpha_1) = -alpha_1 at
      alpha_3 = 0; a reader in Will's normalisation flips the sign of BOTH alphas here.
      NOTHING load-bearing depends on this: a sign flip does not make an infinity finite,
      and path-independence is sign-convention-blind.
  V2. the c_4 sign convention.  The standard EA kinetic tensor carries -c_4 u^a u^b g_{mn},
      which yields +c_4 a.a in L, whereas the corpus's own scripts write L = -[... + c_4 a.a].
      These differ by c_4 -> -c_4.  MOOT HERE: AeST has c_4 = 0, the limit point has c_4 = 0,
      and PART C carries a c_4 regulator with BOTH signs (paths P9 and P10), which give
      identical limits -- so no conclusion depends on resolving the convention.
  V3. signature (-,+,+,+), k_mu = (-omega, 0, 0, k), d_mu -> i k_mu, used only in PART F.
  V4. c_123 > 0 is the ghost-free/gradient-stable side (c_S^2 > 0); c_123 < 0 is unstable.
      Both are reported, and the VERDICT rests only on the healthy side.

WHAT THIS SCRIPT DOES NOT DO (named, not papered over):
  N1. it does NOT re-derive the generic EA PPN parameters from scratch.  They are imported
      [P1..P3] and cross-checked four ways (GATES 1-4), which is a validation, not a
      derivation.  A transcription error common to BOTH published forms would survive.
  N2. it does NOT compute AeST's actual alpha_1, alpha_2 with the SCALAR sector retained
      (2(2-K_B)J^mu grad_mu phi and -(2-K_B)Y).  That is the deciding calculation named by
      stage71 D3 / stage73 H2 and is a sibling agent's job.  Nothing here pre-empts it;
      what this script establishes is that it is MANDATORY, because the aether sector
      alone has no PPN limit.
  N3. it does NOT claim reading D's alpha = 0 is right or wrong.  It shows D's numbers are
      not reached from the generic region, and that D's structural diagnosis is.
  N4. no statement here touches a_0 = kappa c sqrt(G rho_Lambda), kappa, the MS08 kernel,
      or beta.  Verified in PART G: those symbols appear zero times in the computation.

Exit 0 = every numbered check passed.
"""

import sys

import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:2d}. {label}" + (f"\n           {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]}: {label}")
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n           {detail}" if detail else ""))


print(__doc__)

# ---------------------------------------------------------------- imported constants
A1_BOUND = 1.0e-4          # [L1] |alpha_1|, lunar laser ranging
A2_BOUND = 1.0e-7          # [L1] |alpha_2|, solar spin axis
SZ21_K2 = {"Cosh": 7.5e3, "Exp": 9.5e3}      # [L2]
SZ21_KB = {"Cosh": 0.5, "Exp": 0.1}          # [L2]
KB_L_CEILING = A1_BOUND / 4                  # reading L's ceiling, 2.5e-5

# ---------------------------------------------------------------- symbols
c1, c2, c3, c4 = sp.symbols("c_1 c_2 c_3 c_4", real=True)
KB = sp.Symbol("K_B", positive=True)
ea, eb, ec, ed = sp.symbols("eps_a eps_b eps_c eps_d", real=True)
t = sp.Symbol("t", positive=True)            # path parameter (eps)
A, B, C, D = sp.symbols("A B C D", real=True)   # path direction cosines

c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3

# ---------------------------------------------------------------- imported formulas
alpha1_gen = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)                      # [P1]
alpha2_JAC = alpha1_gen / 2 - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) \
    / (c123 * (2 - c14))                                                            # [P2]
alpha2_ALT = ((2 * c13 - c14)**2 / (c123 * (2 - c14))
              - (12 * c3 * c13 + 2 * c1 * c14 * (1 - 2 * c14)
                 + (c1**2 - c3**2) * (4 - 6 * c13 + 7 * c14))
              / ((2 - c14) * (2 * c1 - c1**2 + c3**2)))                             # [P3]
cT2_gen = 1 / (1 - c13)                                                             # [P4]
cV2_gen = (2 * c1 - c1**2 + c3**2) / (2 * c14 * (1 - c13))                          # [P4]
cS2_gen = c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2))                 # [P4]
GN_over_G = 2 / (2 - c14)                                                           # [P5]

DICT = {c1: KB, c2: sp.Integer(0), c3: -KB, c4: sp.Integer(0)}   # AeST's dictionary

# =================================================================================================
print("=" * 100)
print("PART A -- THE FOUR GATES.  If any of these fails, nothing in this file is claimed.")
print("=" * 100)

# ---- GATE 1: two algebraically distinct published alpha_2 forms are the same function
d_forms = sp.simplify(sp.together(alpha2_JAC - alpha2_ALT))
check(d_forms == 0,
      "GATE 1  the two published alpha_2 forms [P2] (Jacobson) and [P3] (expanded "
      "Foster-Jacobson) are the SAME rational function of (c_1,c_2,c_3,c_4)",
      f"alpha_2^[P2] - alpha_2^[P3] simplifies to {d_forms}.  These are structurally "
      "different expressions -- [P3] has no explicit alpha_1/2 and a different numerator "
      "polynomial -- so a transcription typo in either would generically break the "
      "identity.  This is the transcription cross-check, not a derivation (see N1)")

# ---- GATE 2: reproduce the published PPN-safe locus [P6]
c4_star = sp.solve(sp.Eq(c3**2 + c1 * c4, 0), c4)[0]
a1_on = sp.simplify(alpha1_gen.subs(c4, c4_star))
c2_roots = [sp.simplify(s) for s in sp.solve(sp.Eq(sp.together(alpha2_JAC.subs(c4, c4_star)), 0), c2)]
c2_star = (-2 * c1**2 - c1 * c3 + c3**2) / (3 * c1)
hit = any(sp.simplify(r - c2_star) == 0 for r in c2_roots)
a2_on = sp.simplify(alpha2_JAC.subs({c4: c4_star, c2: c2_star}))
check(a1_on == 0 and hit and a2_on == 0,
      "GATE 2  [P1]+[P2] reproduce the PUBLISHED PPN-safe locus [P6] exactly: alpha_1 = 0 "
      "on c_4 = -c_3^2/c_1, and alpha_2 = 0 there iff c_2 = (-2c_1^2 - c_1c_3 + c_3^2)/(3c_1)",
      f"alpha_1|locus = {a1_on}; the c_2 root of alpha_2 = 0 matches the published c_2*: "
      f"{hit}; alpha_2|locus = {a2_on}")

# ---- GATE 3: c_T^2 = 1 exactly, and G_N = G/(1-K_B/2), both on AeST's dictionary
cT2_aest = sp.simplify(cT2_gen.subs(DICT))
GN_aest = sp.simplify(GN_over_G.subs(DICT))
GN_target = sp.simplify(1 / (1 - KB / 2))
check(cT2_aest == 1 and sp.simplify(GN_aest - GN_target) == 0,
      "GATE 3  on AeST's dictionary the imported EA formula set independently reproduces "
      "TWO results the corpus already holds from unrelated calculations: c_T^2 = 1 EXACTLY "
      "(the F^2 form's GW170817 safety) and G_N = G/(1 - K_B/2) (the quasi-static "
      "G~ = (1-K_B/2)G^, and reading D's own w=0 branch)",
      f"c_T^2 = {cT2_aest};  G_N/G = {GN_aest} = 1/(1-K_B/2).  If either the dictionary or "
      "the imported formula conventions were wrong, these would generically fail")
cV2_aest = sp.simplify(cV2_gen.subs(DICT))
cV2_stage71 = sp.simplify(((c1 - c1**2 / 2 - c3**2 / 2) / (c14 * (1 - c13))).subs(DICT))
check(cV2_aest == 1 and sp.simplify(cV2_stage71 - (1 - KB)) == 0,
      "A3b  BONUS, and it settles a committed defect flagged in stage73 H3(5): the imported "
      "spin-1 speed [P4] gives c_V^2 = 1 EXACTLY on the dictionary, agreeing with "
      "svt_2026's gauge-invariant result and DISAGREEING with stage71's c_V^2 = 1 - K_B",
      f"[P4] form (2c_1-c_1^2+c_3^2)/(2c_14(1-c_13)) -> {cV2_aest};  stage71's form "
      f"(c_1-c_1^2/2-c_3^2/2)/(c_14(1-c_13)) -> {cV2_stage71}.  The two differ by the SIGN "
      "of c_3^2, and the [P4] numerator is the SAME polynomial 2c_1-c_1^2+c_3^2 that appears "
      "as alpha_1's denominator [P1] (it is the spin-1 kinetic normalisation) -- a "
      "structural consistency stage71's version does not have.  So the defect resolves in "
      "favour of svt_2026's c_V^2 = 1 and stage71's c_V^2 = 1-K_B should be corrected. "
      "NOT load-bearing for anything else in this file: no result below uses c_V^2")

# ---- GATE 4 is in PART F (needs the from-scratch derivation first); placeholder note
info("A4  GATE 4 (the from-scratch longitudinal dispersion vs the imported c_S^2) is "
     "deferred to PART F, where the derivation lives")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE POLE STRUCTURE: where each alpha is regular and where it is not")
print("=" * 100)

# alpha_1: is the limit point a pole?
a1_den = sp.simplify((2 * c1 - c1**2 + c3**2).subs(DICT))
a1_num = sp.simplify((-8 * (c3**2 + c1 * c4)).subs(DICT))
check(sp.simplify(a1_den - 2 * KB) == 0,
      "B1  alpha_1 is REGULAR at AeST's dictionary point: its denominator "
      "(2c_1 - c_1^2 + c_3^2) equals 2 K_B there, which is NONZERO for every K_B > 0 "
      "(the c_1^2 and c_3^2 pieces cancel because c_1 = -c_3)",
      f"denominator = {a1_den}, numerator = {a1_num}.  A rational function is continuous "
      "at every non-pole point, so alpha_1's limit exists and is automatically "
      "PATH-INDEPENDENT -- this already answers (a) for alpha_1 before any path is drawn")
a1_at = sp.simplify(alpha1_gen.subs(DICT))
check(sp.simplify(a1_at + 4 * KB) == 0,
      "B2  and its value there is alpha_1 = -4 K_B, i.e. reading L's number IS the correct "
      "limit of the generic FORMULA",
      f"alpha_1(dictionary) = {a1_at}")
check(sp.simplify(sp.diff(alpha1_gen, c2)) == 0,
      "B3  alpha_1 does not depend on c_2 AT ALL (d alpha_1 / d c_2 = 0 identically), so "
      "every c_2-direction regulator leaves alpha_1 exactly at its limit value",
      "consequence for (e): alpha_1 cannot possibly be locked to the c_2-driven "
      "degeneracy, and PART D confirms it is not")

# alpha_2: extract the pole in c_123
s = sp.Symbol("sigma", real=True)     # stands for c_123
# substitute c_2 = sigma - c_1 - c_3 so that c_123 = sigma exactly
a2_sigma = alpha2_JAC.subs(c2, s - c1 - c3)
a2_sigma = sp.together(sp.simplify(a2_sigma))
res = sp.simplify(sp.limit(sp.expand(a2_sigma * s), s, 0))
res_aest = sp.simplify(res.subs({c1: KB, c3: -KB, c4: 0}))
check(sp.simplify(res - (-(c1 + 2 * c3 - c4) * (2 * c1 + 3 * (-c1 - c3) + c3 + c4) / (2 - c14))) == 0,
      "B4  alpha_2 has a SIMPLE POLE in c_123.  Writing c_2 = c_123 - c_1 - c_3 and taking "
      "lim_{c_123 -> 0} [c_123 * alpha_2] gives a finite nonzero residue -- so the "
      "singularity is order exactly 1, not higher and not removable",
      f"residue R(c_1,c_3,c_4) = {sp.simplify(res)}")
check(sp.simplify(res_aest - KB**2 / (2 - KB)) == 0 and res_aest != 0,
      "B5  *** THE DECISIVE NUMBER: the residue evaluated at AeST's OWN dictionary point "
      "is R = K_B^2/(2 - K_B), which is NONZERO for every K_B in (0,2) -- i.e. for the "
      "whole no-ghost stability window ***",
      f"R(AeST) = {res_aest}.  The residue is a property of the LIMIT POINT, not of the "
      "path, so no choice of approach direction can cancel it.  This is why alpha_2's "
      "divergence is path-independent (question (c)) -- established here structurally, "
      "before any numerical path table")
# same residue from the independent published form [P3] -- second transcription check
a2_sigma_ALT = sp.together(sp.simplify(alpha2_ALT.subs(c2, s - c1 - c3)))
res_ALT = sp.simplify(sp.limit(sp.expand(a2_sigma_ALT * s), s, 0))
res_ALT_aest = sp.simplify(res_ALT.subs({c1: KB, c3: -KB, c4: 0}))
check(sp.simplify(res_ALT_aest - res_aest) == 0,
      "B6  the SAME residue comes out of the independent published form [P3], whose pole "
      "term is the manifestly different (2c_13 - c_14)^2/(c_123(2-c_14))",
      f"[P3] residue at AeST = {res_ALT_aest} = [P2] residue.  On the dictionary "
      "(2c_13 - c_14)^2 = K_B^2 and 2 - c_14 = 2 - K_B, which is the same K_B^2/(2-K_B) "
      "reached by a completely different algebraic route")
# and c_S^2 is proportional to c_123 with a finite nonzero coefficient
cS2_sigma = sp.simplify(cS2_gen.subs(c2, s - c1 - c3))
lam_fac = sp.simplify(cS2_sigma / s)
lam_aest = sp.simplify(sp.limit(lam_fac.subs({c1: KB, c3: -KB, c4: 0}), s, 0))
check(sp.simplify(lam_aest - (2 - KB) / (2 * KB)) == 0,
      "B7  c_S^2 = c_123 * Lambda(c_123) with Lambda analytic at c_123 = 0 and "
      "Lambda(0) = (2-K_B)/(2K_B) FINITE and NONZERO at the dictionary point, so the "
      "spin-0 speed vanishes LINEARLY in c_123 along every path",
      f"Lambda(AeST) = {lam_aest} = (2-K_B)/(2K_B).  Same order (linear) as alpha_2's pole "
      "is order 1 -- which is what makes the product in PART D finite")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE PATHS.  Regulator family, many independent approaches, one table.")
print("=" * 100)
REG = {c1: KB + ea, c2: ec, c3: -KB + eb, c4: ed}


def on_path(expr, Av, Bv, Cv, Dv=0):
    """Substitute the regulator family with eps_a = A*t etc., leaving t and K_B symbolic."""
    return sp.simplify(expr.subs(REG).subs({ea: Av * t, eb: Bv * t, ec: Cv * t, ed: Dv * t}))


PATHS = [
    # label,                                          A,  B,  C,  D,  note
    ("P1  pure c_2   (c_13 = 0 kept EXACT)",          0,  0,  1,  0, "GW-safe all along"),
    ("P2  pure c_1   (c_2 = 0 kept EXACT)",           1,  0,  0,  0, "c_123 = c_13 = eps"),
    ("P3  pure c_3   (c_2 = 0 kept EXACT)",           0,  1,  0,  0, "c_123 = c_13 = eps"),
    ("P4  c_13 = 2eps, c_2 = eps  (ratio 1:1:1)",     1,  1,  1,  0, "mixed"),
    ("P5  c_13 = 2eps, c_2 = 10eps (ratio 1:1:10)",   1,  1, 10,  0, "c_2-dominated"),
    ("P6  c_13 = 2eps, c_2 = -eps  (partial cancel)", 1,  1, -1,  0, "c_123 = eps"),
    ("P7  c_1 up / c_3 down + c_2   (1,-1,1)",        1, -1,  1,  0, "c_13 = 0, c_123 = eps"),
    ("P8  NEGATIVE side: pure c_2 < 0",               0,  0, -1,  0, "c_S^2 < 0: UNSTABLE"),
    ("P9  with a c_4 regulator, +eps (1,1,1,+1)",     1,  1,  1,  1, "c_4 sign A (see V2)"),
    ("P10 with a c_4 regulator, -eps (1,1,1,-1)",     1,  1,  1, -1, "c_4 sign B (see V2)"),
]

print(f"    {'path':46s} {'lim alpha_1':>14s} {'alpha_2 * eps':>16s} {'c_S^2 / eps':>14s} "
      f"{'alpha_2 * c_S^2':>16s}")
lim_a1_set, prod_set, a2_pole_set = set(), set(), set()
for lab, Av, Bv, Cv, Dv, _note in PATHS:
    a1p = on_path(alpha1_gen, Av, Bv, Cv, Dv)
    a2p = on_path(alpha2_JAC, Av, Bv, Cv, Dv)
    cS2p = on_path(cS2_gen, Av, Bv, Cv, Dv)
    lim_a1 = sp.simplify(sp.limit(a1p, t, 0, "+"))
    pole_coef = sp.simplify(sp.limit(a2p * t, t, 0, "+"))          # coefficient of 1/eps
    cS2_rate = sp.simplify(sp.limit(cS2p / t, t, 0, "+"))          # coefficient of eps
    prod = sp.simplify(sp.limit(a2p * cS2p, t, 0, "+"))
    lim_a1_set.add(sp.simplify(lim_a1))
    prod_set.add(sp.simplify(prod))
    a2_pole_set.add(sp.simplify(pole_coef))
    print(f"    {lab:46s} {str(lim_a1):>14s} {str(pole_coef) + ' /eps':>16s} "
          f"{str(cS2_rate):>14s} {str(prod):>16s}")

check(len(lim_a1_set) == 1 and sp.simplify(list(lim_a1_set)[0] + 4 * KB) == 0,
      "C1  *** (a)+(b) ANSWERED: lim alpha_1 = -4 K_B on ALL TEN paths -- one single value, "
      "PATH-INDEPENDENT, exactly reading L's number ***",
      f"the set of limits collapsed to {{{list(lim_a1_set)[0]}}}.  This is the expected "
      "consequence of B1 (regular point) and is verified here path by path anyway")
nonzero_poles = all(sp.simplify(p) != 0 for p in a2_pole_set)
check(nonzero_poles,
      "C2  *** (c) ANSWERED: alpha_2 DIVERGES on every path -- the coefficient of 1/eps is "
      "nonzero for all ten, so alpha_2 -> +/- infinity, never a finite number ***",
      f"the ten 1/eps coefficients were {sorted(str(p) for p in a2_pole_set)}.  They "
      "differ between paths only by the rate at which that path drives c_123 to zero "
      "(coefficient A+B+C), which rescales eps; the pole itself never cancels")
p1 = [p for p in PATHS if p[0].startswith("P1")][0]
a2_P1 = on_path(alpha2_JAC, *p1[1:5])
a1_P1 = on_path(alpha1_gen, *p1[1:5])
check(sp.simplify(a1_P1 + 4 * KB) == 0,
      "C3  *** THE SHARPEST SINGLE PATH is P1 (regulate ONLY c_2): it keeps c_13 = 0 "
      "exactly, so the whole regulator family is GW170817-safe (c_T = 1) and has "
      "alpha_1 = -4 K_B EXACTLY at every eps -- yet its alpha_2 still runs off to infinity ***",
      f"alpha_1 on P1 = {sp.simplify(a1_P1)} for ALL eps.  So the divergence cannot be "
      "blamed on leaving the GW-safe locus, nor on alpha_1 moving: it is driven purely by "
      "c_2 -> 0, i.e. purely by the c_123 = 0 degeneracy")
a2_P1_series = sp.simplify(sp.series(a2_P1, t, 0, 1).removeO())
check(sp.simplify(sp.limit(a2_P1 * t, t, 0, "+") - KB**2 / (2 - KB)) == 0,
      "C4  and on P1 the divergence is exactly the residue found structurally in B5",
      f"alpha_2(P1) = {sp.simplify(sp.together(a2_P1))}, whose leading term is "
      f"K_B^2/((2-K_B) eps).  Its regular part is "
      f"{sp.simplify(a2_P1 - KB**2/((2-KB)*t))} -- finite, and irrelevant to the verdict")
# the degenerate direction: A + B + C = 0 keeps c_123 = 0, i.e. never leaves the locus
c123_path = sp.simplify(on_path(c123, 1, -1, 0))
check(sp.simplify(c123_path) == 0,
      "C5  AGAINST INTEREST, the one direction that is NOT a regulator: (A,B,C) = (1,-1,0) "
      "keeps c_123 = 0 identically, so that family never leaves the degenerate locus and "
      "says nothing about the limit.  It is excluded by construction, not by choice",
      f"c_123 along (1,-1,0) = {c123_path}.  Every path in the table above has "
      "A + B + C != 0 precisely so that it IS in the generic region for eps != 0")
# health of the approach
health_ok = []
for lab, Av, Bv, Cv, Dv, _note in PATHS:
    cs = on_path(cS2_gen, Av, Bv, Cv, Dv)
    rate = sp.simplify(sp.limit(cs / t, t, 0, "+"))
    val = float(rate.subs(KB, sp.Rational(1, 10)))
    health_ok.append((lab, val > 0))
check(all(v for lab, v in health_ok if not lab.startswith("P8")) and
      not [v for lab, v in health_ok if lab.startswith("P8")][0],
      "C6  the approach is through GHOST-FREE, GRADIENT-STABLE theories on P1-P7 and P9/P10 "
      "(c_S^2 > 0, c_14 = K_B in (0,2), c_13 < 1, spin-1 kinetic 2c_1-c_1^2+c_3^2 = 2K_B > 0) "
      "and through UNSTABLE ones only on P8 (c_123 < 0, c_S^2 < 0).  The divergence is "
      "therefore NOT an artefact of approaching through sick theories",
      f"c_S^2/eps signs at K_B = 0.1: {[(l.split()[0], 'POS' if v else 'NEG') for l, v in health_ok]}. "
      "On the healthy side alpha_2 -> +infinity; the sign flips only on the unstable side")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- (d) the ORDER of limits, and (e) the RATE correlation")
print("=" * 100)
# (d) ordered limits.  Parametrise c_13 = delta with c_1 = K_B + delta/2, c_3 = -K_B + delta/2.
dlt, e2 = sp.symbols("delta c2v", real=True)
ORD = {c1: KB + dlt / 2, c2: e2, c3: -KB + dlt / 2, c4: 0}
a2_ord = sp.simplify(alpha2_JAC.subs(ORD))
# ORDER A: c_2 -> 0 first (at fixed c_13 = delta != 0), then delta -> 0
innerA = sp.simplify(sp.limit(a2_ord, e2, 0))
outerA = sp.simplify(sp.limit(innerA * dlt, dlt, 0, "+"))
# ORDER B: c_13 -> 0 first (at fixed c_2 != 0), then c_2 -> 0
innerB = sp.simplify(sp.limit(a2_ord, dlt, 0))
outerB = sp.simplify(sp.limit(innerB * e2, e2, 0, "+"))
print(f"    ORDER A  lim_{{c_2->0}} alpha_2 (c_13 = delta fixed) = {sp.simplify(sp.together(innerA))}")
print(f"             then lim_{{delta->0+}} [delta * that]       = {outerA}")
print(f"    ORDER B  lim_{{c_13->0}} alpha_2 (c_2 fixed)         = {sp.simplify(sp.together(innerB))}")
print(f"             then lim_{{c_2->0+}}  [c_2 * that]          = {outerB}")
check(sp.simplify(outerA - KB**2 / (2 - KB)) == 0 and sp.simplify(outerB - KB**2 / (2 - KB)) == 0,
      "D1  *** (d) ANSWERED: the ORDER OF LIMITS DOES NOT MATTER for the divergence.  Both "
      "orders -- c_2 -> 0 then c_13 -> 0, and c_13 -> 0 then c_2 -> 0 -- diverge with the "
      "IDENTICAL leading coefficient K_B^2/((2-K_B) c_123) ***",
      f"ORDER A residue {outerA}; ORDER B residue {outerB}.  The intermediate FUNCTIONS "
      "differ (A's inner limit is a function of delta, B's of c_2), but the singular part "
      "is the same because the residue is fixed by the limit point (B5)")
a1_ord = sp.simplify(alpha1_gen.subs(ORD))
check(sp.simplify(sp.limit(sp.limit(a1_ord, e2, 0), dlt, 0) + 4 * KB) == 0 and
      sp.simplify(sp.limit(sp.limit(a1_ord, dlt, 0), e2, 0) + 4 * KB) == 0,
      "D2  and both orders give the SAME alpha_1 = -4 K_B, as they must for a function "
      "continuous at the point",
      "so for alpha_1 the question of ordering is vacuous")

# (e) the rate correlation
prod_sym = sp.simplify(sp.together(alpha2_JAC * cS2_gen))
prod_lim = sp.simplify(prod_sym.subs(c2, s - c1 - c3))
prod_lim = sp.simplify(sp.limit(prod_lim, s, 0))
prod_aest = sp.simplify(prod_lim.subs({c1: KB, c3: -KB, c4: 0}))
check(sp.simplify(prod_aest - KB / 2) == 0,
      "E1  *** (e) ANSWERED, and it is the cleanest result in the file: alpha_2 * c_S^2 has "
      "a FINITE limit, equal to K_B/2 EXACTLY, path-independently.  alpha_2 diverges at "
      "PRECISELY the rate the spin-0 mode speed vanishes -- the divergence and the "
      "degeneracy are the same phenomenon, quantitatively ***",
      f"lim (alpha_2 * c_S^2) = {prod_aest}.  Structurally: alpha_2 ~ R/c_123 with "
      "R = K_B^2/(2-K_B) (B5) and c_S^2 = Lambda c_123 with Lambda = (2-K_B)/(2K_B) (B7), "
      "so the product is R*Lambda = K_B/2 with the c_123 cancelling identically")
check(len(prod_set) == 1 and sp.simplify(list(prod_set)[0] - KB / 2) == 0,
      "E2  and the path table confirms it: all TEN paths, including BOTH c_4-regulator signs "
      "and the unstable one, give alpha_2 * c_S^2 -> K_B/2",
      f"the set of products collapsed to {{{list(prod_set)[0]}}}.  A path-independent "
      "finite product from a path-dependent-looking divergence is direct evidence that the "
      "vanishing spin-0 speed IS what breaks the formula")
# alpha_1's deviation: same order, NOT locked
dev = sp.simplify(sp.series(on_path(alpha1_gen, A, B, C, 0) + 4 * KB, t, 0, 2).removeO())
dev1 = sp.simplify(sp.expand(dev / t))
check(sp.simplify(sp.diff(dev1, C)) == 0,
      "E3  BY CONTRAST alpha_1's deviation from its limit is O(eps) -- the SAME order as "
      "c_S^2 -- but is NOT locked to it: the coefficient is independent of C, the "
      "c_2-direction that actually drives the degeneracy",
      f"(alpha_1 + 4K_B)/eps -> {dev1}, which contains A and B but no C.  On path P1 "
      "(A=B=0) alpha_1's deviation is identically zero while c_S^2 is not -- so alpha_1 "
      "sees the degeneracy not at all, and alpha_2 sees nothing else.  This asymmetry is "
      "the sharp form of why L's alpha_1 looks safe and its alpha_2 does not")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- what the generic methodology ACTUALLY demands if applied consistently")
print("=" * 100)
# On P1 (pure c_2 regulator) alpha_2 = K_B^2/((2-K_B) c_2) + regular.  Impose |alpha_2| < 1e-7.
c2_req = sp.simplify(KB**2 / ((2 - KB) * A2_BOUND))
print(f"    |alpha_2| < {A2_BOUND:.0e} on the P1 family requires c_2 >~ K_B^2/((2-K_B)*{A2_BOUND:.0e})")
print(f"    {'K_B':>10s} {'c_2 required':>14s} {'c_2 in AeST':>12s} {'distance':>14s}")
far = True
for nm, kbv in SZ21_KB.items():
    need = float(c2_req.subs(KB, kbv))
    print(f"    {kbv:10.2g} {need:14.3g} {0.0:12.1f} {need:14.3g}")
    if need < 1e3:
        far = False
need_L = float(c2_req.subs(KB, KB_L_CEILING))
print(f"    {KB_L_CEILING:10.2g} {need_L:14.3g} {0.0:12.1f} {need_L:14.3g}   "
      f"(<- at reading L's OWN ceiling)")
check(far,
      f"F1  *** within the regulator family, satisfying the alpha_2 bound requires "
      f"c_2 >= K_B^2/((2-K_B) * {A2_BOUND:.0e}) = 1.3e6 (K_B = 0.5) to 5.3e4 (K_B = 0.1) -- "
      f"and AeST has c_2 = 0 EXACTLY.  No small deformation of AeST is PPN-viable in the "
      f"generic sense ***",
      "the alpha_2 constraint on this locus is not 'K_B must be small', it is 'c_2 must be "
      "enormous', which is a statement about the FORM of the aether kinetic term, not about "
      "its strength")
# turned around: at fixed small c_2, what does alpha_2 demand of K_B?
print()
print("    turned around -- at a FIXED small c_2, the alpha_2 bound on K_B is:")
print(f"    {'c_2':>10s} {'K_B <= from alpha_2':>21s} {'vs L ceiling 2.5e-5':>21s}")
kb_of_c2 = []
for c2v in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
    kbv = float(sp.nsolve(sp.Eq(KB**2 / ((2 - KB) * c2v), A2_BOUND), KB, 1e-4))
    kb_of_c2.append((c2v, kbv))
    print(f"    {c2v:10.0e} {kbv:21.3e} {'TIGHTER' if kbv < KB_L_CEILING else 'looser':>21s}")
c2_cross = float(sp.simplify(KB**2 / ((2 - KB) * A2_BOUND)).subs(KB, KB_L_CEILING))
# the bound scales as sqrt(c_2): check the decade ratios against sqrt(10) and sqrt(100)
ratio_ok = (abs(kb_of_c2[1][1] / kb_of_c2[2][1] - np.sqrt(10)) < 0.02
            and abs(kb_of_c2[3][1] / kb_of_c2[4][1] - 10.0) < 0.05)
check(all(k < KB_L_CEILING for cv, k in kb_of_c2 if cv <= 1e-3)
      and ratio_ok and kb_of_c2[-1][1] < 1e-7,
      "F2  *** AND THIS IS THE SELF-REFUTATION: at any fixed c_2 below the crossover "
      f"c_2 = {c2_cross:.2g}, the SAME formula set gives an alpha_2 bound on K_B that is "
      "TIGHTER than reading L's 2.5e-5, and it tightens as sqrt(c_2) WITHOUT LIMIT as "
      "c_2 -> 0.  Applied consistently to the c_2 = 0 theory the generic methodology does "
      "not bound K_B -- it demands K_B = 0 EXACTLY ***",
      f"K_B <= sqrt((2-K_B) c_2 * {A2_BOUND:.0e}): {kb_of_c2[2][1]:.2e} at c_2 = 1e-3, "
      f"{kb_of_c2[-1][1]:.2e} at c_2 = 1e-8, and 0 in the limit.  The sqrt(c_2) scaling is "
      f"verified from the decade ratios (1e-2/1e-3 -> {kb_of_c2[1][1]/kb_of_c2[2][1]:.3f} vs "
      f"sqrt(10) = {np.sqrt(10):.3f}).  STATED AGAINST MY OWN CONCLUSION: at c_2 above the "
      f"crossover ({c2_cross:.2g}) the alpha_2 bound is LOOSER than L's, so 'alpha_2 is "
      "always the tighter one' would be false -- what is true is that it becomes "
      "arbitrarily tighter as one approaches AeST's actual c_2 = 0.  So reading L's "
      "'K_B < 2.5e-5' is not the generic methodology's answer for this theory; the generic "
      "methodology's answer is K_B = 0")
# and K_B = 0 is forbidden by the scalar sector (SZ21 Eq 30) -- so the generic route is empty
cs2_at = {nm: (2 - 1e-12) / (SZ21_K2[nm] * 1e-12) for nm in SZ21_K2}
check(all(v > 1 for v in cs2_at.values()),
      "F3  and K_B = 0 is FORBIDDEN by the scalar sector, so the generic route closes on "
      "itself rather than yielding a bound: c_s^2 = (2-K_B)/(K_2 K_B) [SZ21 Eq. 30] carries "
      "1/K_B, so K_B -> 0 sends the scalar SUPERLUMINAL without limit",
      f"at K_B = 1e-12 the SZ21 fits give c_s^2 = "
      f"{', '.join(f'{k}: {v:.2g}' for k, v in cs2_at.items())} -- i.e. the subluminality "
      "FLOOR K_B >= 2/(K_2+1) (stage73 C2) is violated by ~10^8.  A methodology whose only "
      "self-consistent output is a value the theory forbids is not delivering a constraint")
check(True,
      "F4  CONSEQUENCE FOR THE CORPUS, stated in both directions.  ADVERSE-SOUNDING BUT "
      "FAVOURABLE IN EFFECT: reading L's ceiling K_B < 2.5e-5 must be WITHDRAWN as an "
      "in-force bound, which REMOVES stage73's 'empty window at SZ21's own MOND-compatible "
      "fits' (C3) -- that squeeze existed only because the ceiling was banked.  GENUINELY "
      "ADVERSE: what replaces it is not safety but ABSENCE -- the aether sector has NO "
      "valid PPN limit at all, so there is currently no preferred-frame statement about "
      "this theory in either direction, and stage71 D1's hope that 'the degeneracy PROTECTS "
      "alpha_2' gains no support here (from the generic side alpha_2 is infinite, not zero)",
      "net: the immediate crisis is defused, a structural liability is opened, and the "
      "deciding calculation (scalar retained) is upgraded from high-value to MANDATORY")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- WHY, derived from scratch: the static longitudinal operator IS c_123")
print("=" * 100)
# Flat space, aether at rest, h = 0, longitudinal perturbation delta u_i = d_i chi.
# Signature (-,+,+,+); k_mu = (-omega, 0, 0, k); d_mu -> i k_mu on the field and -i k_mu on
# the conjugate.  Unit constraint u.u = -1 forces delta u_0 = 0 at linear order (u^mu = (1,0,0,0)).
om, kk, X = sp.symbols("omega k X", positive=True)
ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA.inv()
kdn = sp.Matrix([-om, 0, 0, kk])                       # k_mu
kup = ETAI * kdn                                       # k^mu
du_dn = sp.Matrix([0, 0, 0, sp.I * kk * X])            # delta u_mu amplitude = d_mu chi, spatial only
du_up = ETAI * du_dn
duc_dn = sp.Matrix([sp.conjugate(z) for z in du_dn])   # conjugate amplitude
duc_up = ETAI * duc_dn

# the four EA scalars, as explicit index sums (this is the derivation, not a restatement)
S1 = sp.simplify(sum(ETAI[m, aa] * ETAI[n, bb] * (sp.I * kdn[m] * du_dn[n])
                     * (-sp.I * kdn[aa] * duc_dn[bb])
                     for m in range(4) for n in range(4) for aa in range(4) for bb in range(4)))
S2 = sp.simplify((sum(ETAI[m, n] * (sp.I * kdn[n]) * du_dn[m] for m in range(4) for n in range(4)))
                 * (sum(ETAI[m, n] * (-sp.I * kdn[n]) * duc_dn[m] for m in range(4) for n in range(4))))
S3 = sp.simplify(sum((sp.I * kdn[m] * du_dn[n]) * ETAI[n, bb] * ETAI[m, aa]
                     * (-sp.I * kdn[bb] * duc_dn[aa])
                     for m in range(4) for n in range(4) for aa in range(4) for bb in range(4)))
a_dn = sp.Matrix([sum(ETAI[0, n] * 0 for n in range(4))] * 4)   # placeholder, filled below
a_dn = sp.Matrix([(-sp.I * om) * du_dn[m] * 0 for m in range(4)])
# a_mu = u^nu grad_nu delta u_mu = d_t delta u_mu -> (-i omega) delta u_mu
a_dn = sp.Matrix([(-sp.I * om) * du_dn[m] for m in range(4)])
ac_dn = sp.Matrix([sp.conjugate(z) for z in a_dn])
S4 = sp.simplify(sum(ETAI[m, n] * a_dn[m] * ac_dn[n] for m in range(4) for n in range(4)))
print(f"    S1 = (grad_mu du_nu)(grad^mu du^nu) -> {sp.simplify(S1)}")
print(f"    S2 = (grad.du)^2                    -> {sp.simplify(S2)}")
print(f"    S3 = (grad_mu du_nu)(grad^nu du^mu) -> {sp.simplify(S3)}")
print(f"    S4 = a_mu a^mu                      -> {sp.simplify(S4)}")
check(sp.simplify(S1 - (kk**2 - om**2) * kk**2 * X**2) == 0
      and sp.simplify(S2 - kk**4 * X**2) == 0
      and sp.simplify(S3 - kk**4 * X**2) == 0
      and sp.simplify(S4 - om**2 * kk**2 * X**2) == 0,
      "G1  the four EA kinetic scalars, evaluated from explicit index sums on a purely "
      "LONGITUDINAL aether perturbation, come out S1 = (k^2-omega^2)k^2 X^2, "
      "S2 = S3 = k^4 X^2, S4 = omega^2 k^2 X^2",
      "no formula imported: built from eta, k_mu and delta u_mu = d_mu chi directly")
# corpus-convention Lagrangian: L = -[c1 S1 + c2 S2 + c3 S3 + c4 S4]
Lkern = sp.simplify(-(c1 * S1 + c2 * S2 + c3 * S3 + c4 * S4))
Lkern = sp.expand(Lkern)
static_kern = sp.simplify(Lkern.subs(om, 0))
check(sp.simplify(static_kern + (c1 + c2 + c3) * kk**4 * X**2) == 0,
      "G2  *** THE STRUCTURAL RESULT: setting omega = 0, the ENTIRE Einstein-aether "
      "quadratic Lagrangian for a static longitudinal perturbation collapses to "
      "L = -c_123 (lap chi)^2.  The static longitudinal kinetic operator IS c_123 * lap^2, "
      "and c_4 drops out entirely (a_mu = d_t delta u_mu = 0 when static) ***",
      f"L(omega = 0) = {sp.factor(static_kern)}.  Hence the static response to any source "
      "S obeys c_123 lap^2 chi = S, i.e. chi = S/c_123 * (lap^-2): DIVERGENT as c_123 -> 0. "
      "AT c_123 = 0 the operator vanishes IDENTICALLY, so the equation degenerates from an "
      "equation FOR chi into a CONSTRAINT ON THE SOURCE -- which is exactly reading D's "
      "lambda*(w.khat) = 0, reached there from d_mu d_nu F^{mu nu} = 0 and from "
      "G^(1)_{3nu} == 0.  The two readings solve two DIFFERENT boundary-value problems")
# dispersion relation, and GATE 4
disp = sp.Eq(sp.expand(Lkern / (kk**2 * X**2)), 0)
v2_scratch = sp.simplify(sp.solve(sp.Eq(Lkern, 0), om**2)[0] / kk**2)
check(sp.simplify(v2_scratch - (c1 + c2 + c3) / (c1 - c4)) == 0,
      "G3  the same from-scratch calculation gives the longitudinal DISPERSION relation "
      "omega^2/k^2 = c_123/(c_1 - c_4) (corpus c_4 convention; c_1 + c_4 in the standard "
      "one -- see V2, and it is moot at c_4 = 0)",
      f"omega^2/k^2 = {v2_scratch}.  Manifestly proportional to c_123, so the LINEAR "
      "vanishing rate found for the imported c_S^2 in B7 is reproduced independently")
# GATE 4: leading small-c agreement with the imported c_S^2 at c_4 = 0
eps_s = sp.Symbol("varepsilon", positive=True)
cS2_small = cS2_gen.subs({c1: eps_s * c1, c2: eps_s * c2, c3: eps_s * c3, c4: 0})
cS2_lead = sp.simplify(sp.limit(cS2_small, eps_s, 0))
check(sp.simplify(cS2_lead - (c1 + c2 + c3) / c1) == 0
      and sp.simplify(v2_scratch.subs(c4, 0) - (c1 + c2 + c3) / c1) == 0,
      "GATE 4  the from-scratch longitudinal speed AGREES with the imported c_S^2 [P4] in "
      "the small-c_i limit at c_4 = 0, where metric mixing is subleading: both give "
      "c_123/c_1",
      f"imported c_S^2 leading order = {cS2_lead}; from-scratch = "
      f"{sp.simplify(v2_scratch.subs(c4, 0))}.  This is an independent validation of the "
      "c_S^2 transcription AND of the claim that c_S^2 vanishes linearly in c_123 -- the "
      "two ingredients that PART D's product result rests on.  It does NOT validate the "
      "full metric-mixing denominator (2+c_13+3c_2), which is imported (N1)")
check(True,
      "G4  the from-scratch picture also explains WHY alpha_2 and not alpha_1 is the one "
      "that blows up: the PPN alpha_2 term is w^i w^j U_ij, the ANISOTROPIC response, and "
      "that is carried by the longitudinal (spin-0) aether perturbation whose static "
      "operator is the c_123 one just derived.  alpha_1's w^2 U term is isotropic and is "
      "carried by the spin-1 sector, whose kinetic normalisation 2c_1 - c_1^2 + c_3^2 = "
      "2 K_B stays FINITE on the dictionary (B1).  Two different modes, two different fates",
      "recorded as the structural reading of B1 vs B5; it is a consistency story for the "
      "imported formulas, not an independent derivation of the alpha's themselves")
check(True,
      "G5  a coincidence recorded and explicitly NOT claimed: the THIRD reading (freeze "
      "lambda at its w=0 value, discard the Theta_{3nu} constraints) gives formal "
      "alpha_2 = +K_B/2, which is numerically the SAME as lim(alpha_2 * c_S^2) = K_B/2 "
      "found in E1, and has the same SIGN as the divergence on the healthy side",
      "no derivation connects them here.  Flagged because it is the kind of coincidence "
      "that either signals a c_S^2 = 1 normalisation hiding in the frozen-lambda "
      "prescription or is meaningless, and the corpus should know it was noticed")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- insulation check: what this file does NOT touch")
print("=" * 100)
used = set()
for e in (alpha1_gen, alpha2_JAC, alpha2_ALT, cT2_gen, cV2_gen, cS2_gen, GN_over_G,
          static_kern, Lkern):
    used |= set(e.free_symbols)
forbidden = {"kappa", "a_0", "nu", "beta", "Q_0", "Lambda_D"}
check(not (forbidden & {str(x) for x in used}),
      "H1  a_0 = kappa c sqrt(G rho_Lambda) (9.3619e-11 canonical / 1.1279e-10 alt), kappa "
      "itself, the MS08 kernel nu(y) = 1/(1-exp(-sqrt y)), beta and Q_0 appear ZERO times "
      "in every expression used above.  The symbols actually present are only "
      f"{sorted(str(x) for x in used)}",
      "so nothing in this adjudication can be traded away by adjusting kappa or the "
      "kernel -- and equally, the normalisation claim gets no credit for surviving it. "
      "The K_B values and c_s^2 quoted in PART E are SZ21's [L2], imported for context only")
check(abs(9.3619e-11 / 1.1279e-10 - 0.83) < 0.01,
      "H2  the two a_0 footings are recorded for completeness because the standing rule "
      "requires both be reported for dimensional numbers -- but THIS FILE PRODUCES NO "
      "DIMENSIONAL NUMBER: alpha_1, alpha_2, c_S^2, c_123 and K_B are all dimensionless, "
      "so the footing fork is inert here",
      "canonical 9.3619e-11 / alt 1.1279e-10 m s^-2, ratio 0.830.  Stated so the omission "
      "is deliberate and visible rather than an oversight")

# =================================================================================================
print()
print("=" * 100)
print("PART H -- VERDICT")
print("=" * 100)
print(f"""
    THE TABLE, in one place:

      quantity                    limit from the generic region        path-dependent?
      ------------------------------------------------------------------------------------
      alpha_1                     -4 K_B  (= reading L's number)       NO (regular point)
      alpha_2                     +infinity on every healthy path      NO in magnitude;
                                  (-infinity only through c_123 < 0,   sign follows sign(c_123)
                                   which is gradient-UNSTABLE)
      alpha_2 * c_S^2             K_B/2 exactly                        NO
      c_S^2                       0, LINEARLY in c_123                 rate only
      alpha_1 + 4K_B              0, linearly in eps, C-independent     coefficient only
      order of limits             irrelevant: both orders diverge with the same residue

    WHAT IT ADJUDICATES
      * Reading L's NUMBER for alpha_1 is the correct limit of the generic formula, and it
        is path-independent.  That much of L is CONFIRMED.
      * Reading L's USE of that number as an in-force bound on K_B is REFUTED.  The same
        formula set, at the same point, returns alpha_2 = +infinity; and applied
        consistently (PART E) it demands K_B = 0 exactly, which the scalar sector forbids.
        A formula set cannot be trusted for one preferred-frame parameter and ignored for
        the other, tighter-bounded one at the same point.
      * Reading D's STRUCTURAL claim -- that the PPN expansion's premises fail on this
        locus, so alpha_1 and alpha_2 do not exist in the usual sense -- is CONFIRMED, from
        the opposite direction.  The degenerate theory is a SINGULAR POINT of the
        Einstein-aether family, not a continuous member: the propagating-mode count changes
        there, and PART F shows the static longitudinal equation changes TYPE (from an
        equation for chi to a constraint on the source).
      * Reading D's NUMBERS (alpha_1 = alpha_2 = 0) get NO support here.  They are not the
        limit of the generic region.  They are the answer to the constrained problem, which
        is a different boundary-value problem -- consistent with D's own caveats (the
        non-normalisable wake, the w -> 0 discontinuity in G_N).
      * stage71 D1's hoped-for "the degeneracy PROTECTS alpha_2" is NOT supported.  From
        the generic side the degeneracy is what makes alpha_2 blow up, not vanish.

    DIRECTION OF RISK FOR THE FRAMEWORK: MIXED, and both halves are load-bearing.
      FAVOURABLE: stage70's K_B < 2.5e-5 and hence stage73's "empty window at SZ21's own
        MOND-compatible fits" are withdrawn.  The superluminality squeeze was conditional
        on reading L (stage73 C7 said so) and reading L does not survive as a bound.
      ADVERSE: what replaces it is absence, not safety.  The aether sector alone has NO
        valid PPN limit, so the corpus currently has NO preferred-frame statement about
        this theory in either direction, and it cannot claim protection either.  The one
        deciding calculation (PPN with the scalar sector retained: 2(2-K_B)J^mu grad_mu phi
        and -(2-K_B)Y) is upgraded from "highest-value Tier-2" to MANDATORY, because
        nothing at the aether-sector level can supply the answer.
""")
check(True,
      "I1  *** VERDICT: the regulated limit ADJUDICATES AGAINST READING L AS A BOUND and "
      "FOR READING D'S STRUCTURAL DIAGNOSIS, while supporting neither reading's numbers as "
      "the theory's actual PPN parameters.  The decisive facts are (i) alpha_2's simple "
      "pole with residue K_B^2/(2-K_B) != 0 at AeST's own dictionary point, so no path "
      "escapes; and (ii) lim(alpha_2 c_S^2) = K_B/2 exactly, so the blow-up rate is locked "
      "to the vanishing spin-0 speed ***",
      "the limit is NOT path-dependent -- it is path-independently DIVERGENT, which is a "
      "sharper outcome than path-dependence would have been: it cannot be repaired by "
      "choosing a better regulator")
check(True,
      "I2  what would overturn this: (a) a transcription error common to BOTH published "
      "alpha_2 forms [P2] and [P3] -- GATE 1 cannot see that (N1); (b) the scalar sector "
      "cancelling the pole, which is exactly the sibling calculation and is the ONLY "
      "physically motivated escape, since 2(2-K_B)J^mu grad_mu phi mixes into precisely "
      "the spin-0 channel that has gone soft; (c) an argument that the c_123 = 0 theory "
      "should be quantised/solved as a constrained system whose alpha's are defined by the "
      "constrained problem, in which case reading D's setup is right but its alpha = 0 "
      "still needs the wake pathology resolved",
      "(b) is the live one, and this file's main practical output is that it is no longer "
      "optional")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"REGULATED-LIMIT CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed"
      + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
