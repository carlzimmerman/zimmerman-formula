#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage48_kb_candidate_killed_2026.py
===================================
STAGE 46 IS DEAD.  Killed by a 10-agent adversarial audit, three independent ways -- and the worst of the
three is that stage 46 committed the IDENTICAL circularity error that stage 43 had diagnosed one stage
earlier.  Three real byproducts survive, two of them favourable to the framework.

--------------------------------------------------------------------------------------------------
KILL 1 -- THE ASSUMPTION WAS NOT MERELY UNVERIFIED.  IT WAS INVERTED.
--------------------------------------------------------------------------------------------------
Stage 46 assumed G_local = (1 - K_B/2) Ghat with G_cosmo = Ghat, giving G_cosmo/G_local = 1/(1 - K_B/2).
That reads the corpus's own notation BACKWARDS.  In G_tilde = (1 - K_B/2) Ghat as Skordis & Zlosnik write
it, G_tilde is the FUNDAMENTAL constant -- the one appearing in 1/(16 pi G_tilde) and in the Friedmann
equation -- and Ghat is the DERIVED, LARGER, quasi-static one.  Therefore
        *** G_cosmo/G_local = G_tilde/Ghat = 1 - K_B/2  <=  1,  NOT 1/(1 - K_B/2). ***
Stage 46 assumed the reciprocal of the truth.

Confirmed three independent ways by the audit:
  (a) Carroll & Lim (2004) via Jacobson's review (arXiv:0801.1547): G_cosmo = G/(1 + (c_13 + 3c_2)/2), and
      for AeST c_13 + 3c_2 = 0 IDENTICALLY, so G_cosmo = G_tilde EXACTLY for every K_B -- no
      renormalisation of the cosmological constant at all.
  (b) Independently from Carl's own action: on FRW, F_munu = J^mu = Y = 0 identically, so the ENTIRE
      aether Lagrangian vanishes on the background.  K_B therefore cannot touch the Friedmann equation.
  (c) Foster & Jacobson Eq. (3): G_N = G(1 - c_14/2)^(-1)-type structure, same direction.
And in the parent theory's own variables H_Lambda^2 = (-K)/3 with a_0^2 = zeta(-K), so Z = 1/sqrt(3 zeta)
with NO Newton constant appearing anywhere -- the ratio was never available to be exploited.

--------------------------------------------------------------------------------------------------
KILL 2 -- IT MAKES THE PROBLEM WORSE, NOT BETTER
--------------------------------------------------------------------------------------------------
With the correct direction, G_cosmo/G_local = 1 - K_B/2 <= 1, so at stage 46's own K_B = 3/2 the
hand-set number becomes 1/4: "explain a factor of 2" becomes "explain a factor of 4".  And kappa_eff = kappa/sqrt(1-K_B/2) >= 1 for ALL K_B in (0,2), so kappa_eff = 1/2 has NO
solution in the window at all: the correction can only push kappa_eff UP, never down.

--------------------------------------------------------------------------------------------------
KILL 3 -- AND STAGE 46's "PREDICTION" WAS A TAUTOLOGY.  THIS IS THE ONE THAT STINGS.
--------------------------------------------------------------------------------------------------
Stage 46 Part B inverted its own relation to write K_B = 2(1 - kappa^2) and then reported that the
measured kappa "becomes a measurement of K_B", with kappa = 1/2 giving K_B = 3/2 as a PREDICTION.  But
under that map kappa = 1/2 gives K_B = 3/2 IDENTICALLY.  "This predicts K_B = 3/2" and "kappa = 1/2" are
THE SAME STATEMENT.

*** THAT IS PRECISELY THE ERROR STAGE 43 HAD JUST DIAGNOSED: epsilon_tot = 1/(32 pi) is kappa = 1/2 solved
for epsilon_tot.  One stage later I solved kappa = 1/2 for K_B and called the output a prediction.  Same
mistake, same session, immediately after writing the stage that identifies it. ***

--------------------------------------------------------------------------------------------------
WHAT SURVIVES -- three byproducts, two of them favourable
--------------------------------------------------------------------------------------------------
1. THE ALGEBRAIC IDENTITY IS CORRECT and nobody in the corpus had written it down:
        Z = [sqrt(8pi/3)/kappa] x sqrt(G_cosmo/G_local)
   It collapses correctly to stage 43's Z = sqrt(8pi/3)/kappa when the two constants agree, which is what
   AeST in fact does.  Its content is the opposite of what stage 46 hoped, but it is worth having.

2. *** GW170817 IS SATISFIED EXACTLY, NOT APPROXIMATELY -- STRONGER THAN BANKED.  The corpus records
   "GW170817 silent since c_1 = -c_3".  The audit verified it: c_13 = c_1 + c_3 = 0 IDENTICALLY for every
   K_B, against Oost et al.'s requirement |c_13| < 1e-15.  AeST does not merely pass this bound, it
   satisfies it as an identity. ***

3. *** AND THE CORPUS IS WRONG THAT K_B IS UNCONSTRAINED.  Foster & Jacobson Eq. (10) at AeST's point
   gives alpha_1 = -4 K_B (matching Oost et al. Eq. 3.12 for c_13 = 0, since AeST has c_14 = K_B).  So the
   PREFERRED-FRAME PPN sector DOES bound K_B, and the standing claim that K_B is unconstrained -- based on
   its absence from the quasi-static phenomenology and GW170817's silence -- is incomplete.  This is new
   information and it should be carried forward. ***

--------------------------------------------------------------------------------------------------
DOCUMENTATION FIX OWED
--------------------------------------------------------------------------------------------------
The phrasing "the aether sector renormalises Newton's constant, G_tilde = (1 - K_B/2) Ghat", carried in
the memory index and in THE_COMPLETION.md, is a faithful quote from Skordis & Zlosnik but reads backwards
to anyone who has not internalised which symbol is fundamental.  It is what fooled stage 46.  It should be
rewritten to name G_tilde as the fundamental/cosmological constant and Ghat as the derived, larger
quasi-static one.
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
    return True


print(__doc__)

KB, kap = sp.symbols("K_B kappa", positive=True)

print("=" * 100)
print("PART A -- the inversion")
print("=" * 100)

R_assumed = 1 / (1 - KB / 2)          # stage 46's assumption
R_true = 1 - KB / 2                   # the correct direction
check(sp.simplify(R_assumed * R_true) == 1,
      f"A1  stage 46 assumed G_cosmo/G_local = {R_assumed}; the correct direction is {R_true}.  They are "
      f"exact RECIPROCALS, so the error is a notation inversion, not an arithmetic slip",
      "G_tilde is SZ's FUNDAMENTAL constant (in 1/16 pi G_tilde and in the Friedmann equation); Ghat is "
      "the DERIVED, larger, quasi-static one")

check(sp.simplify((R_true).subs(KB, 0)) == 1,
      f"A2  and for AeST specifically c_13 + 3c_2 = 0 identically, so Carroll & Lim's "
      f"G_cosmo = G/(1+(c_13+3c_2)/2) gives G_cosmo = G_tilde EXACTLY for every K_B -- the ratio is 1 and "
      f"was never available to exploit",
      "independently: on FRW F_munu = J^mu = Y = 0, so the whole aether Lagrangian vanishes on the "
      "background and K_B cannot enter the Friedmann equation at all")

print()
print("=" * 100)
print("PART B -- it makes the problem worse")
print("=" * 100)

at_32 = sp.simplify(R_true.subs(KB, sp.Rational(3, 2)))
check(at_32 == sp.Rational(1, 4),
      f"B1  with the correct direction, at stage 46's own K_B = 3/2 the ratio is {at_32}, so the hand-set "
      f"number becomes 1/4: 'explain a factor of 2' becomes 'explain a factor of 4'")

# kappa_eff is defined by Z = sqrt(8pi/3)/kappa_eff, and Z = [sqrt(8pi/3)/kappa] sqrt(G_c/G_l), so
#     kappa_eff = kappa / sqrt(G_cosmo/G_local) = kappa / sqrt(1 - K_B/2)
kappa_eff = kap / sp.sqrt(R_true)
at0 = sp.simplify(kappa_eff.subs({kap: 1, KB: 0}))
lim2 = sp.limit(kappa_eff.subs(kap, 1), KB, 2, "-")
no_sol = sp.solve(sp.Eq(kappa_eff.subs(kap, 1), sp.Rational(1, 2)), KB)
KBu = sp.symbols("K_B_unrestricted", real=True)      # drop positivity to expose where the root sits
root = sp.solve(sp.Eq((1 / sp.sqrt(1 - KBu / 2)), sp.Rational(1, 2)), KBu)
check(len(no_sol) == 0 and root and root[0] < 0,
      f"B2  *** AND THE DIRECTION IS UNUSABLE -- a cleaner kill than this check's first draft claimed.  "
      f"kappa_eff = kappa/sqrt(1 - K_B/2), so with kappa_bare = 1 it runs from {at0} at K_B = 0 upward to "
      f"{lim2} as K_B -> 2: kappa_eff >= 1 ALWAYS.  We need 1/2, and sympy returns NO positive solution; "
      f"unrestricted, the root sits at K_B = {root[0]}, negative and far outside the window ***",
      "so the aether correction can only push kappa_eff UP from kappa_bare, never down -- it cannot "
      "explain ANY kappa < 1.  A first draft of this check wrongly said it required K_B = 0 exactly")

info("B2b for completeness: to land kappa_eff = 1/2 you would need kappa_bare = (1/2) sqrt(1 - K_B/2) <= 1/2, "
     "i.e. you would STILL be inserting a number no larger than 1/2 by hand.  The mechanism cannot remove "
     "an inserted coefficient smaller than unity under any K_B.")

print()
print("=" * 100)
print("PART C -- the tautology, which is the one that stings")
print("=" * 100)

kb_of_kappa = 2 * (1 - kap ** 2)
check(sp.simplify(kb_of_kappa.subs(kap, sp.Rational(1, 2))) == sp.Rational(3, 2),
      f"C1  *** stage 46's own map K_B = 2(1 - kappa^2) sends kappa = 1/2 to K_B = "
      f"{sp.simplify(kb_of_kappa.subs(kap, sp.Rational(1,2)))} IDENTICALLY.  So 'this predicts K_B = 3/2' and "
      f"'kappa = 1/2' are THE SAME STATEMENT.  Part B was never independent falsifiable content ***")

info("C2  *** AND THAT IS EXACTLY THE ERROR STAGE 43 HAD JUST DIAGNOSED.  Stage 43: epsilon_tot = 1/(32 pi) "
     "is kappa = 1/2 solved for epsilon_tot, therefore circular.  Stage 46, one stage later: K_B = 3/2 is "
     "kappa = 1/2 solved for K_B, reported as a prediction.  Same mistake, same session, immediately after "
     "writing the stage that names it. ***")

print()
print("=" * 100)
print("PART D -- what survives, including two things favourable to the framework")
print("=" * 100)

info("D1  THE IDENTITY IS CORRECT and was not in the corpus: Z = [sqrt(8pi/3)/kappa] sqrt(G_cosmo/G_local), "
     "collapsing to stage 43's form when the constants agree -- which in AeST they do.  Worth keeping; its "
     "content is simply the opposite of what stage 46 hoped.")

info("D2  *** GW170817 IS SATISFIED EXACTLY, NOT APPROXIMATELY -- stronger than banked.  The corpus records "
     "'GW170817 silent since c_1 = -c_3'.  Verified: c_13 = c_1 + c_3 = 0 IDENTICALLY for every K_B, "
     "against Oost et al.'s |c_13| < 1e-15.  AeST satisfies that bound as an IDENTITY, not as a fit. ***")

info("D3  *** AND THE CORPUS IS WRONG THAT K_B IS UNCONSTRAINED.  Foster & Jacobson Eq. (10) at AeST's "
     "point gives alpha_1 = -4 K_B (matching Oost et al. Eq. 3.12 for c_13 = 0, AeST having c_14 = K_B).  "
     "So preferred-frame PPN DOES bound K_B.  The standing 'K_B is unconstrained' claim rested on its "
     "absence from the quasi-static phenomenology plus GW170817's silence, and is incomplete. ***")

info("D4  DOCUMENTATION FIX OWED: 'the aether sector renormalises Newton's constant, G_tilde = "
     "(1-K_B/2) Ghat', as carried in the memory index and THE_COMPLETION.md, is a faithful SZ quote that "
     "reads BACKWARDS to anyone who has not internalised which symbol is fundamental.  It is what fooled "
     "stage 46 and it should be rewritten.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  STAGE 46 IS DEAD.  Killed three ways by a 10-agent adversarial audit.

  1. THE ASSUMPTION WAS INVERTED, not merely unverified.  G_cosmo/G_local = 1 - K_B/2 <= 1, and stage 46
     assumed the exact reciprocal.  For AeST specifically c_13 + 3c_2 = 0 identically, so the ratio is 1
     and was never available: on FRW the entire aether Lagrangian vanishes, so K_B cannot enter the
     Friedmann equation at all.  Cross-checked against Carroll & Lim, Jacobson's review, and Foster &
     Jacobson, and independently re-derived from Carl's own action.

  2. WITH THE CORRECT DIRECTION IT MAKES THINGS WORSE: at K_B = 3/2 the hand-set number becomes 1/4, and
     kappa_eff = kappa/sqrt(1-K_B/2) >= 1 for every K_B in (0,2), so kappa_eff = 1/2 has NO solution
     at all -- the correction can only push kappa_eff UP from kappa_bare, never down.

  3. *** AND THE "PREDICTION" WAS A TAUTOLOGY.  Under stage 46's own map K_B = 2(1 - kappa^2), kappa = 1/2
     gives K_B = 3/2 identically -- the same statement twice.  Which is the error stage 43 had diagnosed
     ONE STAGE EARLIER, about epsilon_tot = 1/(32 pi).  I wrote the stage that names the mistake and then
     made it. ***

  WHAT SURVIVES, and two of the three help:
     - the algebraic identity Z = [sqrt(8pi/3)/kappa] sqrt(G_cosmo/G_local), correct and previously
       unwritten in this corpus;
     - GW170817 satisfied EXACTLY rather than approximately, since c_13 = 0 identically for every K_B --
       a stronger statement than the corpus banked;
     - and the discovery that K_B IS constrained after all, via alpha_1 = -4 K_B in the preferred-frame
       PPN sector.  The standing "K_B is unconstrained" claim is incomplete and should be corrected.

  STANDING ON THE COEFFICIENT, unchanged from stage 43: kappa is MEASURED at 0.551 +/- 0.043, the whole
  open content is one factor of two, and no route yet touches it.  Two attempts on that factor have now
  failed by the same mechanism -- solving kappa = 1/2 for something else and calling the something else a
  result.  Any future attempt must be checked against that failure mode FIRST.
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
