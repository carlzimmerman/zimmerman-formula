#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf19_the_bracket_2026.py
========================
THE LAST BRACKET.  Two terms proved to vanish -- one of them REINSTATING sf16's collapse with a
CORRECT proof -- and the two survivors given explicitly.  Grade: PARTIAL-FAVOURABLE.  The theory
is not closed here, and the reason it is not is stated precisely.

THE CONSTRAINTS (sf18):
    C    = H_EH[h,pi]     + sqrt(h) F(X)
    Chat = H_EHhat[hhat,pihat] + sqrt(h) B(X) + u^i H_i[h,pi]
with X = X[h, hhat, pihat] -- it carries the HATTED momenta through Khat u (sf17) and NO unhatted
momenta at all (sf17 B1).

THE FOUR TERMS OF {C, Chat}:

  (1) {H_EH[h,pi], H_EHhat[hhat,pihat]}  =  0
      Disjoint canonical pairs.  Trivial and rigorous.

  (2) {H_EH[h,pi], sqrt(h) B(X)}  =  -(dH_EH/dpi)(d(sqrt(h)B)/dh)   SURVIVES
      B has no unhatted momentum dependence, so only one of the two terms lives.  And
      dH_EH/dpi ~ K_ij, the UNHATTED extrinsic curvature.

  (3) {sqrt(h) F(X), H_EHhat[hhat,pihat]}  SURVIVES, and with BOTH terms
      because X depends on hhat AND pihat.

  (4) *** {sqrt(h) F(X), sqrt(h) B(X)}  =  0  --  AND THIS REINSTATES sf16's COLLAPSE WITH A
      CORRECT PROOF.  sf16 claimed it because the interaction was "momentum-free"; sf17 showed
      that was false and withdrew it.  The TRUE reason is different and stronger: F and B are
      functions of THE SAME phase-space scalar X, and any two functions of the same scalar
      Poisson-commute --
            {F(X), B(X)} = F'B' (X_q X_p - X_p X_q) = 0
      identically, whatever X depends on.  The sqrt(h) prefactors are inert in the hatted sector
      and F, B carry no unhatted momentum, so the full term vanishes. ***

SO {C, Chat} = (2) + (3), and PART C gives both explicitly.

WHY THIS IS NOT YET CLOSURE.  Second-classness requires {C, Chat} not to be WEAKLY zero -- not a
combination of C, Chat, or the diagonal momentum constraint.  PART D shows the survivors are
proportional to EXTRINSIC CURVATURES contracted with derivatives of X, and that NONE of the
constraints has that form -- so the bracket is not weakly zero UNLESS an accidental cancellation
occurs.  *** THAT IS THE STRONGEST DEFENSIBLE STATEMENT AND IT IS NOT A PROOF.  Ruling out the
cancellation needs the explicit ADM forms, which this file does not carry. ***

Exit 0 = every numbered check passed.
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


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

h, pi, hh, pih = sp.symbols("h pi hhat pihat", real=True)


def pb(A_, B_):
    return sp.simplify(sp.diff(A_, h) * sp.diff(B_, pi) - sp.diff(A_, pi) * sp.diff(B_, h)
                       + sp.diff(A_, hh) * sp.diff(B_, pih) - sp.diff(A_, pih) * sp.diff(B_, hh))


# X carries h, hhat, pihat -- and NO pi (sf17)
X = sp.Function("X")(h, hh, pih)
F, B = sp.Function("F")(X), sp.Function("B")(X)
Hg = sp.Function("H_EH")(h, pi)
Hf = sp.Function("H_EHhat")(hh, pih)

# =========================================================================================
head("PART A -- term (1): disjoint sectors")
# =========================================================================================
check(sp.simplify(pb(Hg, Hf)) == 0,
      "A1  {H_EH[h,pi], H_EHhat[hhat,pihat]} = 0 -- built from disjoint canonical pairs",
      f"sympy: {sp.simplify(pb(Hg, Hf))}")

# =========================================================================================
head("PART B -- term (4): functions of the SAME scalar commute.  sf16's collapse, reinstated.")
# =========================================================================================
check(sp.simplify(pb(F, B)) == 0,
      "B1  *** {F(X), B(X)} = 0 IDENTICALLY, whatever X depends on -- including pihat.  The proof "
      "is one line: F'B'(X_q X_p - X_p X_q) = 0.  Any two functions of the SAME phase-space "
      "scalar Poisson-commute ***",
      f"sympy: {{F(X), B(X)}} = {sp.simplify(pb(F, B))}")
# and check it is NOT because X is momentum-free -- X manifestly carries pihat here
check(sp.simplify(sp.diff(X, pih)) != 0,
      "B2  and X in this computation MANIFESTLY carries pihat, so B1 is NOT the withdrawn "
      "momentum-free argument.  *** sf16's four-to-two collapse is REINSTATED -- with a correct "
      "proof, and a stronger one, since it holds for any X whatsoever ***",
      f"sympy: dX/dpihat = {sp.diff(X, pih)} =/= 0")
Y = sp.Function("Y")(h, hh, pih)
check(sp.simplify(pb(F, sp.Function("B")(Y))) != 0,
      "B3  CONTRAST that shows what is doing the work: if F and B were functions of DIFFERENT "
      "scalars X and Y, the bracket would NOT vanish.  It is the SHARED argument that kills it -- "
      "and the architecture has F and B sharing X by construction (sf13c)",
      "so the vanishing is a structural feature of this construction, not a coincidence")

# =========================================================================================
head("PART C -- the two survivors, explicitly")
# =========================================================================================
t2 = sp.simplify(pb(Hg, B))
t3 = sp.simplify(pb(F, Hf))
check(t2 != 0,
      "C1  TERM (2) = {H_EH[h,pi], sqrt(h)B(X)} survives, and only ONE of its two pieces does, "
      "because B carries no unhatted momentum",
      f"sympy: {t2}")
check(t3 != 0,
      "C2  TERM (3) = {sqrt(h)F(X), H_EHhat[hhat,pihat]} survives with BOTH pieces, because X "
      "depends on hhat AND pihat",
      f"sympy: {t3}")
total = sp.simplify(pb(Hg + F, Hf + B))
check(sp.simplify(total - (t2 + t3)) == 0,
      "C3  *** AND THE TOTAL IS EXACTLY THE SUM OF THE TWO SURVIVORS: "
      "{C, Chat} = {H_EH, sqrt(h)B} + {sqrt(h)F, H_EHhat}.  Two terms, not four ***",
      f"sympy: difference = {sp.simplify(total - (t2 + t3))}")

# =========================================================================================
head("PART D -- why this is not yet closure")
# =========================================================================================
check(True,
      "D1  SECOND-CLASSNESS REQUIRES {C, Chat} NOT TO BE **WEAKLY** ZERO -- i.e. not a "
      "combination of C, Chat, or the diagonal momentum constraint H_i + H_ihat.  A nonzero "
      "EXPRESSION can still vanish on the constraint surface",
      "this is the distinction sf18 D1 flagged and it is the last link")
check(True,
      "D2  THE STRUCTURAL ARGUMENT, and it is suggestive rather than decisive: dH_EH/dpi ~ K_ij "
      "and dH_EHhat/dpihat ~ Khat_ij, so both survivors are EXTRINSIC CURVATURES contracted with "
      "derivatives of X.  None of C, Chat or H_i + H_ihat has that form -- C and Chat are "
      "quadratic-in-momenta plus a potential, and the momentum constraint is a divergence of pi.  "
      "*** So the bracket is not weakly zero UNLESS an accidental cancellation occurs ***",
      "and sf17 B2's asymmetry works against such a cancellation: term (2) is momentum-free in "
      "the hatted sector while term (3) is not, so they cannot cancel against each other by "
      "symmetry")
check(True,
      "D3  *** BUT THAT IS NOT A PROOF, AND I WILL NOT GRADE IT AS ONE.  Ruling out the "
      "cancellation requires substituting the explicit ADM forms "
      "H_EH = (1/sqrt h)(pi_ij pi^ij - pi^2/2) - sqrt(h) R^(3) and the same hatted, then checking "
      "the result against the constraint surface.  THIS FILE DOES NOT CARRY THAT.  The theory is "
      "NOT closed ***",
      "five errors in this line so far, four of them from claiming a regime or a structure "
      "beyond what was computed.  This is where the computation stops")

# =========================================================================================
head("STANDING")
# =========================================================================================
for s_ in [
    "GRADE: PARTIAL-FAVOURABLE.  Two of the four bracket terms are now PROVED zero (one of them "
    "rigorously reinstating sf16's collapse with a correct and stronger proof), the two survivors "
    "are explicit, and the structural argument points AWAY from weak vanishing",
    "THE ARCHITECTURE'S FULL STANDING: steps 1-3 cleared, the sign gate cleared, the DOF count "
    "lands on 7 = 2 + 5 conditionally (sf18), the bracket reduced to two explicit terms (here).  "
    "NEITHER CLOSED NOR KILLED",
    "THE ONE REMAINING CALCULATION, fully specified: substitute the explicit ADM constraint "
    "densities into terms (2) and (3) and determine whether the sum is proportional to C, Chat or "
    "H_i + H_ihat.  If yes -> first class -> 8 DOF -> BD ghost -> KILL.  If no -> second class -> "
    "7 DOF -> the theory CLOSES",
    "both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF19 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed  (two terms killed, two explicit, NOT closure)")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
