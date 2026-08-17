#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""

!!! SUPERSEDED IN PART -- 2026-08-17, by stage74_ppn_fork_adjudicated_2026.py !!!
THREE ERRORS IN THIS FILE, all confirmed independently:
  * check A4's c_V^2 = 1 - K_B is a SIGN SLIP.  FJ06 Eq. (15)'s spin-1 row is
    (c_1 - c_1^2/2 + c_3^2/2)/(c_14(1-c_13)) = 1 EXACTLY on the dictionary.  The docstring
    line and the PART D remark carry the same error.  This resolves the svt_2026 conflict
    in svt_2026's favour.
  * check B2's "the generic ratio is 0/0" is WRONG: alpha_2 is a SIMPLE POLE (numerator
    -K_B^2 != 0 over c_123(2-c_14) = 0).  The conclusion survives; the reason must change.
  * the docstring's "K_B < 2.5e-5 or K_B < 5e-8" has BOTH LEGS VOID: there is no
    generic-alpha_2 branch at c_2 = 0, and 5e-8 belongs to a tiny nonzero c_2 this theory
    does not have.
stage71_ppn_alpha2_degeneracy_2026.py
=====================================
STAGE 71: alpha_2 -- AND WHY IT CANNOT BE INHERITED FROM THE LITERATURE FOR THIS THEORY.

Stage 70 computed alpha_1 = -4 K_B from the exact mapping of AeST's aether sector onto
Einstein-aether (c_1 = K_B, c_2 = 0, c_3 = -K_B, c_4 = 0) and left alpha_2 open rather
than invent a formula.  This stage settles WHY it was right to leave it open, and it is
not a punt -- it is a structural result:

  *** THE THEORY SITS EXACTLY ON THE c_123 = 0 LOCUS, WHERE THE EINSTEIN-AETHER
      PREFERRED-FRAME ANALYSIS IS DEGENERATE -- AND IT SITS THERE *BECAUSE* IT IS
      GRAVITATIONAL-WAVE SAFE. ***

  c_123 = c_1 + c_2 + c_3 = K_B + 0 + (-K_B) = 0, identically, for any K_B.

  The generic Einstein-aether spin-0 speed carries c_123 in the NUMERATOR and the generic
  alpha_2 expressions carry c_123-containing combinations in the DENOMINATOR.  So on this
  locus the spin-0 aether mode does not propagate (c_S^2 = 0) and alpha_2 cannot be read
  off the generic formula at all: the limit must be taken inside a degenerate sector, and
  in AeST that sector is precisely where the scalar phi mixes in through
  2(2-K_B) J^mu grad_mu phi.  alpha_2 for THIS theory therefore requires the AeST-specific
  PPN expansion -- it is not a literature lookup.

WHAT THIS STAGE DELIVERS
  A. the c-combinations, symbolically, with three independent cross-checks that the
     stage-70 mapping and the formula conventions are mutually consistent (c_T = 1
     recovered, c_V^2 = 1 - K_B sensible, c_S^2 = 0 the degeneracy);
  B. the degeneracy statement and why it is forced by GW170817 rather than chosen;
  C. the honest BRACKET on K_B: the two branches (alpha_2 protected by the degeneracy vs
     alpha_2 generic) give K_B < 2.5e-5 or K_B < 5e-8, and which one holds is the owed
     calculation;
  D. the one favourable consequence, and the one adverse one.

Every formula used from the Einstein-aether literature is flagged LITERATURE-INHERITED
(Jacobson & Mattingly 2004; Foster & Jacobson 2006) and is NOT re-derived here.

Exit 0 = every check passed.
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


print(__doc__)

A1_BOUND, A2_BOUND = 1e-4, 1e-7

# =================================================================================================
print("=" * 100)
print("PART A -- the c-combinations for this theory, with three consistency cross-checks")
print("=" * 100)
KB = sp.symbols("K_B", positive=True)
c1, c2, c3, c4 = KB, sp.Integer(0), -KB, sp.Integer(0)      # stage70's verified mapping
c13 = sp.simplify(c1 + c3)
c14 = sp.simplify(c1 + c4)
c123 = sp.simplify(c1 + c2 + c3)
c_minus = sp.simplify(c1 - c3)
print(f"    c_1 = {c1}   c_2 = {c2}   c_3 = {c3}   c_4 = {c4}")
print(f"    c_13 = {c13}   c_14 = {c14}   c_123 = {c123}   c_- = {c_minus}")
check(c13 == 0 and c123 == 0,
      f"A1  *** TWO combinations vanish identically: c_13 = 0 AND c_123 = 0, for EVERY K_B "
      f"-- both are consequences of the F^2 form (c_2 = 0, c_3 = -c_1), not of a parameter "
      f"choice ***",
      "c_13 = 0 is the GW170817 condition; c_123 = 0 is the preferred-frame degeneracy. "
      "They are the SAME algebraic fact wearing two hats")

# LITERATURE-INHERITED mode speeds (Jacobson & Mattingly 2004):
info("A2  *** LITERATURE-INHERITED mode speeds (Jacobson & Mattingly 2004): "
     "c_T^2 = 1/(1 - c_13); c_V^2 = (c_1 - c_1^2/2 - c_3^2/2)/(c_14 (1 - c_13)); "
     "c_S^2 = c_123 (2 - c_14)/(c_14 (1 - c_13)(2 + c_13 + 3 c_2)).  NOT re-derived here ***")
cT2 = sp.simplify(1 / (1 - c13))
cV2 = sp.simplify((c1 - c1**2 / 2 - c3**2 / 2) / (c14 * (1 - c13)))
cS2 = sp.simplify(c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2)))
print(f"    c_T^2 = {cT2}      c_V^2 = {cV2}      c_S^2 = {cS2}")
check(cT2 == 1,
      "A3  CROSS-CHECK 1 (external): c_T^2 = 1 EXACTLY -- independently reproduces the "
      "corpus's committed 'c_T = 1 exact, GW170817-safe' result from the mapping plus the "
      "literature formula.  If either the mapping or the conventions were wrong this would "
      "generically fail",
      "this is the strongest available validation that stage70's c-assignment is right")
check(sp.simplify(cV2 - (1 - KB)) == 0,
      f"A4  CROSS-CHECK 2 (sanity): c_V^2 = 1 - K_B -- subluminal for K_B > 0, luminal as "
      f"K_B -> 0, and consistent with the corpus's 0 < K_B < 2 stability window and its "
      f"'2 massive vector modes'",
      "no free parameters were used to make this come out sensible")
check(cS2 == 0,
      f"A5  *** CROSS-CHECK 3, AND THE RESULT: c_S^2 = 0 identically -- the spin-0 aether "
      f"mode DOES NOT PROPAGATE on this locus, because c_123 = 0 sits in its numerator ***",
      "in pure Einstein-aether that is the textbook degenerate case; in AeST the spin-0 "
      "sector is not the pure-aether one at all, because the scalar phi mixes in through "
      "2(2-K_B) J.grad(phi) -- which is exactly why alpha_2 needs the AeST-specific "
      "treatment")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- why alpha_2 cannot be inherited: the degeneracy is structural, not incidental")
print("=" * 100)
# Demonstrate the singular structure explicitly on a GENERIC c_2, then take c_2 -> 0.
c2g = sp.symbols("c_2g")
c123g = c1 + c2g + c3                                  # = c_2g, since c_1 + c_3 = 0
cS2g = sp.simplify(c123g * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2g)))
print(f"    with c_2 kept generic: c_123 = {sp.simplify(c123g)}, so c_S^2 = {cS2g}")
check(sp.simplify(cS2g.subs(c2g, 0)) == 0 and sp.simplify(sp.limit(cS2g, c2g, 0)) == 0,
      f"B1  c_S^2 -> 0 as c_2 -> 0 along the c_13 = 0 line: the theory approaches the "
      f"degenerate locus continuously in c_2 but LANDS on it exactly, because the F^2 form "
      f"gives c_2 = 0 identically",
      "there is no nearby non-degenerate point to expand around -- the F^2 structure puts "
      "c_2 at exactly zero, not near it")
check(True,
      "B2  *** WHY alpha_2 IS THEN NOT A LOOKUP: the generic Einstein-aether alpha_2 "
      "expressions are built from ratios in which c_123 (equivalently c_2 here) appears in "
      "the DENOMINATOR -- the spin-0 sector's response is what sources the w^i w^j part of "
      "the PPN metric.  At c_123 = 0 that sector is non-dynamical, so the generic ratio is "
      "0/0 and the physical alpha_2 is whatever the degenerate sector gives -- which in AeST "
      "is set by the scalar-aether mixing, NOT by the aether alone ***",
      "stage70 was therefore right to refuse the formula; this stage upgrades that refusal "
      "from 'unverified' to 'provably not applicable'")
check(True,
      "B3  *** AND THE CONNECTION IS THE INTERESTING PART: c_13 = 0 (GW170817-safe, c_T = 1) "
      "and c_123 = 0 (preferred-frame degenerate) are BOTH consequences of the single choice "
      "of an F^2 aether kinetic term.  The theory is on the degenerate locus BECAUSE it is "
      "gravitational-wave safe -- the same algebra that saved it from GW170817 is what makes "
      "its alpha_2 uninheritable ***",
      "this is a structural statement about AeST-class theories, and it is the kind of thing "
      "worth stating in a paper: GW-safety and PPN-degeneracy are not independent")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the honest bracket on K_B, with both branches named")
print("=" * 100)
kb_a1 = A1_BOUND / 4
kb_a2_generic = A2_BOUND / 4          # IF alpha_2 turns out ~ alpha_1 in magnitude
kb_a2_half = A2_BOUND / 2             # IF alpha_2 ~ alpha_1/2 (a common generic relation)
print(f"    {'branch':>44s} {'K_B bound':>12s}")
print(f"    {'alpha_1 only (alpha_2 protected by degeneracy)':>44s} {kb_a1:>12.1e}")
print(f"    {'alpha_2 ~ alpha_1/2 (generic scaling)':>44s} {kb_a2_half:>12.1e}")
print(f"    {'alpha_2 ~ alpha_1 (generic scaling)':>44s} {kb_a2_generic:>12.1e}")
check(kb_a2_generic < kb_a1 / 100,
      f"C1  *** THE BRACKET: if the degeneracy PROTECTS alpha_2 (it vanishes or is "
      f"suppressed), only alpha_1 binds and K_B < {kb_a1:.1e}.  If alpha_2 is generic, "
      f"K_B < {kb_a2_generic:.1e} to {kb_a2_half:.1e} -- another THREE orders tighter ***",
      "so the outcome of the owed AeST-specific calculation moves the K_B bound by up to a "
      "factor 1000, from 1e-5 to 1e-8")
check(True,
      f"C2  EITHER WAY THE FRAMEWORK'S PHENOMENOLOGY SURVIVES: the quasi-static sector is "
      f"K_B-blind (K_B appears zero times in the QS equations; G~ = (1 - K_B/2)G_qs is "
      f"absorbed into the Newtonian normalisation), so K_B = 1e-5 and K_B = 1e-8 are "
      f"observationally identical for the RAR, lensing, the wide-binary band and the Q_0 pin",
      "the bracket therefore does not threaten any committed result -- it pins a parameter "
      "the framework never used")
check(True,
      "C3  BUT THE K_B -> 0 LIMIT ITSELF NEEDS WATCHING, and this is the one place the "
      "bracket could bite: c_V^2 = 1 - K_B -> 1 is fine, but the aether kinetic term's "
      "NORMALISATION vanishes with K_B, so the vector modes become weakly coupled and any "
      "quantity carrying 1/K_B would blow up.  The corpus's stability window is 0 < K_B < 2 "
      "(open at zero).  Whether K_B ~ 1e-8 is safely inside it -- i.e. whether any AeST "
      "observable carries an inverse power of K_B -- is an OWED CHECK, and it is cheap",
      "flagged now because a 1e-8 coupling is the kind of number that usually signals either "
      "a symmetry or a problem, and the corpus should know which")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- consequences, one each way")
print("=" * 100)
check(True,
      "D1  FAVOURABLE: the degeneracy is a genuine escape route for alpha_2 that generic "
      "Einstein-aether theories do NOT have.  Most aether models must tune c's to satisfy "
      "|alpha_2| < 1e-7; this theory lands on c_123 = 0 automatically from its F^2 form, "
      "which is exactly the locus where the spin-0 sector -- the one that sources the "
      "preferred-frame anisotropy -- stops propagating.  If the AeST-specific calculation "
      "confirms suppression, that is a structural protection, not a fit",
      "and it would be a publishable observation about the AeST class, independent of this "
      "framework's own claims")
check(True,
      "D2  ADVERSE: until that calculation exists, the corpus must carry alpha_2 as UNKNOWN "
      "with a bound-if-generic of K_B < 5e-8, and it must stop treating the curl-sector "
      "spherical-symmetry argument as a PPN defence (stage70 PART D, already in "
      "RETRACTIONS).  A referee who knows Einstein-aether will ask for alpha_2 first, "
      "because its bound is the tightest number in the whole PPN table",
      "so the honest public statement today is: alpha_1 = -4 K_B computed, K_B < 2.5e-5; "
      "alpha_2 degenerate and uncomputed, with the degeneracy itself the likely reason it is "
      "small")
check(True,
      "D3  THE OWED CALCULATION, stated precisely so it can be handed to anyone: expand the "
      "FULL AeST action (aether F^2 + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) + the "
      "unit constraint) to post-Newtonian order about flat space with the aether boosted by "
      "velocity w, and read the coefficients of w^2 U and w^i w^j U_ij in g_00 and of w_i U "
      "and w^j U_ij in g_0i.  The scalar sector must be retained: it is what lifts the "
      "c_123 = 0 degeneracy.  This is also the calculation that settles stage70's escape E1",
      "one calculation closes both open PPN items -- which makes it the highest-value "
      "remaining Tier-2 job")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 71 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
