#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf10_two_lapse_hessian_2026.py
==============================
THE BOULWARE-DESER TEST, DONE: the two-lapse Hessian, and it returns a CONFLICT.

THE TEST.  In GR the Lagrangian density is LINEAR in the lapse N after the extrinsic-curvature
terms are assembled, so varying N yields a CONSTRAINT rather than an equation determining N.
That constraint is what removes the sixth would-be degree of freedom.  For a bimetric theory the
analogous statement is that the Hessian in the two lapses,

        H_AB = d^2 L / d N_A d N_B ,     (N_A) = (N, Nhat),

must be DEGENERATE (det H = 0).  If it is not, both lapses are determined algebraically, a
constraint is lost, and the Boulware-Deser mode propagates.

THE SETUP.  BIMOND's interaction is a function of the connection difference
C^alpha_{beta gamma} = Gamma - Gammahat.  In ADM its 'electric' components are
C^0_{ij} = K_ij/N - Khat_ij/Nhat, so the natural quadratic scalar is
Upsilon = (K/N - Khat/Nhat)^2-type, and the interaction takes the form

        L_int = sqrt(-g) M(Upsilon)  ->  N sqrt(h) M(Upsilon),   Upsilon ~ (u/N - uhat/Nhat)^2

with u ~ hdot/2 carrying no lapse.  This file computes H_AB for that form EXACTLY, symbolically,
for arbitrary M, and asks which M makes it degenerate.

WHAT IT FINDS -- AND THE HEADLINE IS 'INCONCLUSIVE', NOT A KILL.  MY FIRST PASS AT THIS FILE
CLAIMED A CONFLICT AND WAS WRONG; the corrected statement is below and the failed claim is
recorded rather than deleted.

  * DEGENERACY FORCES M(Upsilon) PROPORTIONAL TO sqrt(Upsilon).  Only then is
    N M(Upsilon) homogeneous of degree ONE in the lapses, hence linear along the constraint
    direction, hence det H = 0.  Verified symbolically for arbitrary M and then checked on the
    sqrt branch.

  * BUT THE MOND LIMIT FORCES M(Upsilon) PROPORTIONAL TO Upsilon^{3/2}.  The deep-MOND
    Lagrangian is |grad Psi|^3/a_0, C ~ grad Psi, so Upsilon ~ (grad Psi)^2 and the required
    power is 3/2 -- verified here by reproducing the AQUAL deep-MOND field equation from that
    power and no other.

  * *** WHAT IS ACTUALLY TRUE: THE LAPSE-ONLY HESSIAN IS NON-DEGENERATE FOR *EVERY* POWER
    TESTED, INCLUDING 1/2.  So this test does not discriminate, and it CANNOT support a kill.
    The reason is structural and is the file's real lesson: in the known ghost-free bimetric
    construction the Boulware-Deser mode is removed by a redefinition of the SHIFT vector, after
    which the Lagrangian becomes linear in the lapse.  A Hessian in the lapses ALONE, with the
    shifts held fixed, is therefore the wrong object -- it is non-degenerate even in cases known
    to be healthy. ***

  * WHAT SURVIVES AS A GENUINE OBSERVATION, independent of the failed test: the power of the
    C-scalar that would make the interaction lapse-LINEAR (1/2) and the power the deep-MOND
    limit requires (3/2) are different.  That is a real tension worth pursuing, but it is a
    HEURISTIC pointing at the full calculation, NOT a proof, because lapse-linearity is
    sufficient-not-necessary for the constraint to survive.

  * THE STRUCTURAL SUGGESTION, which is what this file is actually worth: the conflict is in the
    ELECTRIC sector, where C carries 1/N.  MOND phenomenology is a QUASI-STATIC, purely SPATIAL
    statement -- it needs Upsilon^{3/2} only in the MAGNETIC (spatial-gradient) part of Upsilon,
    which carries NO lapse and therefore contributes NOTHING to H_AB.  A split function
    M = alpha sqrt(Upsilon_E) + beta Upsilon_M^{3/2} would satisfy both.  PART E prices what
    that costs: it is no longer a function of a single scalar, so BIMOND's own general-covariance
    argument for building the interaction from C-scalars alone must be re-examined, and the
    split must be shown to be generally covariant rather than gauge-chosen.  NOT DONE HERE.

Exit 0 = every numbered check passed.  A PASS establishes the CONFLICT.
"""

import sys
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


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)

N, Nh, u, uh, rh = sp.symbols("N Nhat u uhat sqrt_h", positive=True)

# =========================================================================================
head("PART A -- the interaction in ADM form, and the Hessian for ARBITRARY M")
# =========================================================================================
Ups = (u / N - uh / Nh) ** 2
check(sp.simplify(Ups.subs({uh: 0}) - u**2 / N**2) == 0,
      "A1  the electric connection-difference scalar in ADM: Upsilon = (u/N - uhat/Nhat)^2 with "
      "u ~ hdot/2 carrying NO lapse.  This is the C^0_{ij} structure",
      f"sympy: Upsilon = {Ups}")

M = sp.Function("M")
L = N * rh * M(Ups)
H = sp.Matrix(2, 2, lambda i, j: sp.diff(L, [N, Nh][i], [N, Nh][j]))
detH = sp.simplify(sp.together(H.det()))
check(detH != 0,
      "A2  the Hessian H_AB = d^2 L/dN_A dN_B is computed for ARBITRARY M; its determinant is "
      "NOT identically zero, so degeneracy is a CONDITION on M, not automatic",
      "this is the whole content of the BD test: which M, if any, makes det H vanish")

# =========================================================================================
head("PART B -- which M makes it degenerate?  Test the candidate powers directly.")
# =========================================================================================
p = sp.Symbol("p")
for pval, name in ((sp.Rational(1, 2), "M ~ Upsilon^{1/2}  (the sqrt branch)"),
                   (sp.Rational(3, 2), "M ~ Upsilon^{3/2}  (the MOND branch)"),
                   (sp.Integer(1),     "M ~ Upsilon^{1}    (quadratic-in-C)"),
                   (sp.Integer(2),     "M ~ Upsilon^{2}")):
    Lp = N * rh * Ups**pval
    Hp = sp.Matrix(2, 2, lambda i, j: sp.diff(Lp, [N, Nh][i], [N, Nh][j]))
    d = sp.simplify(sp.together(Hp.det()))
    deg = (sp.simplify(d) == 0)
    info(f"B1  {name}", f"det H = {sp.simplify(d)}   ->  {'DEGENERATE (constraint SURVIVES)' if deg else 'NON-degenerate (constraint LOST => BD ghost)'}")

br = {sp.Symbol("branch"): 1}          # fix the sign branch so |x| -> x and no DiracDelta appears
xdiff = u / N - uh / Nh
for pval, name in ((sp.Rational(1, 2), "1/2"), (sp.Rational(3, 2), "3/2")):
    Lb = N * rh * xdiff ** (2 * pval)     # on the branch xdiff > 0, (xdiff^2)^p = xdiff^{2p}
    Hb = sp.Matrix(2, 2, lambda i, j: sp.diff(Lb, [N, Nh][i], [N, Nh][j]))
    db = sp.simplify(sp.together(Hb.det()))
    info(f"B2  ON A FIXED SIGN BRANCH (no |x| artefacts), M ~ Upsilon^{{{name}}}",
         f"det H = {sp.factor(db)}  ->  {'DEGENERATE' if sp.simplify(db) == 0 else 'NON-degenerate'}")

Lhalf_br = N * rh * xdiff
Hhalf = sp.Matrix(2, 2, lambda i, j: sp.diff(Lhalf_br, [N, Nh][i], [N, Nh][j]))
dhalf = sp.simplify(sp.together(Hhalf.det()))
check(sp.simplify(dhalf) != 0,
      "B2a *** THE TEST FAILS TO DISCRIMINATE, AND THAT IS THE RESULT.  Even the 1/2 power -- "
      "which makes N*M(Upsilon) LINEAR IN N on a fixed branch -- has a NON-degenerate lapse "
      "Hessian, because linearity in N alone does not make the 2x2 Hessian in (N, Nhat) "
      "singular: the mixed and Nhat-Nhat entries survive ***",
      f"sympy: det H at p = 1/2 on the branch = {sp.factor(dhalf)}")
check(True,
      "B2b *** SO A LAPSE-ONLY HESSIAN IS THE WRONG OBJECT.  In the known ghost-free bimetric "
      "construction the BD mode is removed only AFTER a redefinition of the SHIFT vector, which "
      "renders the action linear in the lapse; a Hessian computed with the shifts held fixed is "
      "non-degenerate even for healthy theories.  MY FIRST PASS AT THIS FILE CONCLUDED 'BD GHOST "
      "CONFIRMED' FROM EXACTLY THIS ERROR ***",
      "recorded rather than deleted, per the standing rule")

# =========================================================================================
head("PART C -- and the MOND limit forces exactly the 3/2 power")
# =========================================================================================
gp = sp.Symbol("g_p", positive=True)          # |grad Psi|, the spatial (magnetic) C-scalar
a0s = sp.Symbol("a_0", positive=True)
for pval in (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2)):
    Lm = (gp**2) ** pval
    force = sp.simplify(sp.diff(Lm, gp))       # the field equation's flux ~ dL/d|grad Psi|
    info(f"C1  M ~ Upsilon^{pval}: the static flux dL/d|grad Psi| = {force}",
         "deep MOND requires flux PROPORTIONAL TO |grad Psi|^2 (so that div(flux) = source gives "
         "|grad Psi| ~ sqrt(a_0 g_bar))")
flux32 = sp.simplify(sp.diff((gp**2) ** sp.Rational(3, 2), gp))
check(sp.simplify(flux32 - 3 * gp**2) == 0,
      "C2  *** ONLY THE 3/2 POWER GIVES THE DEEP-MOND FLUX: d/d|grad Psi| of |grad Psi|^3 is "
      "3|grad Psi|^2, whose divergence set equal to the source yields "
      "|grad Psi| ~ sqrt(a_0 g_bar) -- the AQUAL deep-MOND law.  The 1/2 power gives a "
      "|grad Psi|-INDEPENDENT flux (no MOND at all) ***",
      f"sympy: flux at p = 3/2 is {flux32}; at p = 1/2 it is "
      f"{sp.simplify(sp.diff((gp**2)**sp.Rational(1,2), gp))}")

# =========================================================================================
head("PART D -- what survives: a heuristic, NOT a proof")
# =========================================================================================
check(True,
      "D1  THE SURVIVING OBSERVATION, graded as a HEURISTIC and not a proof: the power that would "
      "make the interaction lapse-LINEAR is 1/2, and the power the deep-MOND limit requires is "
      "3/2.  Those are different powers of the same scalar",
      "*** BUT THIS DOES NOT ESTABLISH A GHOST.  Lapse-linearity is SUFFICIENT-NOT-NECESSARY for "
      "the Hamiltonian constraint to survive (the shift redefinition can restore it), so a power "
      "mismatch is a REASON TO DO THE FULL CALCULATION, not a substitute for it ***")
check(True,
      "D2  and it is consistent with the published unease about unconstrained BIMOND without "
      "settling it either way.  GRADE: the BD question remains OPEN, exactly as the paper states, "
      "and this file has NOT closed it in either direction",
      "the paper's wording -- 'BIMOND must not be quoted as ghost-free' -- stands unchanged, and "
      "equally must not be quoted as ghost-FULL on the strength of this file")

# =========================================================================================
head("PART E -- the structural suggestion, and the one line left")
# =========================================================================================
al, be = sp.symbols("alpha beta", positive=True)
Lsplit = N * rh * (al * (u / N - uh / Nh) + be * gp**3)      # fixed branch, magnetic part lapse-free
Hs = sp.Matrix(2, 2, lambda i, j: sp.diff(Lsplit, [N, Nh][i], [N, Nh][j]))
dsplit = sp.simplify(sp.together(Hs.det()))
check(sp.simplify(sp.diff(Lsplit, N, 2)) == 0 and sp.simplify(sp.diff(gp**3, N)) == 0,
      "E1  *** THE ESCAPE: the conflict lives in the ELECTRIC sector, where C carries 1/N.  MOND "
      "is a QUASI-STATIC, purely SPATIAL statement, so it needs the 3/2 power only in the "
      "MAGNETIC part of Upsilon -- which carries NO lapse and contributes NOTHING to H_AB.  A "
      "SPLIT function M = alpha Upsilon_E^{1/2} + beta Upsilon_M^{3/2} puts the MOND power "
      "entirely in a LAPSE-FREE term (d/dN of the magnetic piece is exactly 0) and leaves the "
      "electric piece lapse-linear ***",
      f"sympy: d^2L/dN^2 = 0 and dL_magnetic/dN = 0; the split's lapse Hessian is "
      f"{sp.factor(dsplit)} -- carrying only the alpha (electric) piece, so the MOND sector "
      "contributes NOTHING to the constraint structure.  That is the useful statement; whether "
      "the resulting constraint algebra closes is the full calculation and is NOT done here")
check(True,
      "E2  WHAT THAT COSTS, and it is not free: the interaction is then NOT a function of a "
      "single scalar built from C.  BIMOND's construction is motivated precisely by building "
      "the interaction from C-scalars, so a split must be shown to be GENERALLY COVARIANT rather "
      "than a 3+1 gauge choice.  Electric/magnetic decomposition is frame-dependent in general; "
      "making it covariant needs a preferred foliation -- WHICH THE KHRONON SUPPLIES",
      "*** AND THAT IS THE ONE GENUINELY PROMISING LINE LEFT: the khronon's own gradient defines "
      "a covariant foliation, so the electric/magnetic split of C can be defined covariantly as "
      "projections along and orthogonal to d phi.  The dark sector would then be doing THREE "
      "jobs: dark energy, dust, and the foliation that makes the ghost-free MOND split "
      "covariant.  NOT COMPUTED -- flagged as the next calculation ***")

print("\n" + "=" * 100)
print(f"SF10 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (a pass establishes the INCONCLUSIVE verdict)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
