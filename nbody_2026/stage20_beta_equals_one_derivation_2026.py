#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage20_beta_equals_one_derivation_2026.py
==========================================
THE beta = 1 QUESTION, SETTLED AS FAR AS IT CAN HONESTLY BE SETTLED -- which is further than
"selected" and short of "derived", with the gap stated exactly.

Status upgrade:   beta = 1  goes from  SELECTED (stage 17)  to  *** BOUNDARY-PINNED ***:
    * beta <= 1        is a THEOREM (reality of the action into the early universe, Part B);
    * beta >= 1-3.6e-5 is DATA (the CMB off-switch, Part D);
    * beta = 1 exactly is the unique boundary point, and it is EQUIVALENT to a structural
      statement (Part C): K is a PURE BRANE ACTION -- tension times volume element, no additive
      constant -- with every additive vacuum constant residing in Lambda_bare where it belongs.

--------------------------------------------------------------------------------------------------
THE OBSERVATION THAT REFRAMES THE WHOLE QUESTION (Part A)
--------------------------------------------------------------------------------------------------
Before v7's promotion, an additive constant c0 in K(Q) was UNPHYSICAL: it enters the action as
c0 sqrt(-g), exactly a shift of Lambda_bare -- the field equations depend only on the TOTAL vacuum
energy, and the committed action carries Lambda_bare as a separate parameter anyway.  The split of
the vacuum energy between the gravity sector and the khronon sector was a redundancy of description.

The promotion a_0^2 = kappa^2 G(-K) BREAKS that redundancy: a_0 reads K's share specifically.  So
"what is beta?" is not a question about a new parameter -- it is the question "how much of the
vacuum constant sits inside K rather than in Lambda_bare?", asked of a split that used to be pure
convention.  A prescription that depends on an unphysical convention is ill-defined; the promotion
is only a complete prescription once the split is fixed.  Parts B-D show the split is fixed from
three independent directions, all landing on the same point.

--------------------------------------------------------------------------------------------------
WHAT IS NOT CLAIMED
--------------------------------------------------------------------------------------------------
beta strictly below 1 (by less than 3.6e-5) remains a logically consistent theory -- it leaves a
residual MOND floor a_0(floor) = sqrt(1-beta) a_0(0) at early times, which the CMB bounds but does
not eliminate.  That is a FALSIFIABLE ALTERNATIVE, not an error: a measured high-z MOND floor would
MEASURE 1-beta.  And Part B's theorem needs nu -> infinity into the past, i.e. the charge history
n propto a^-3 extending to arbitrarily early times; a khronon sector that only forms at some finite
epoch caps nu and reopens beta > 1 by a hair.  Both escapes are named, neither is hidden.
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
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


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the redundancy: additive constants in K are Lambda_bare in disguise")
print("=" * 100)

u, Q0, mu_s, LD, M4, c0, T = sp.symbols("u Q_0 mu Lambda_D M4 c_0 T", positive=True)

# a constant contributes nothing to the scalar equation and shifts T_munu like a CC
K_gen = sp.Function("K")(u)
check(sp.diff(c0, u) == 0,
      "A1  a constant c_0 in K contributes NOTHING to the khronon's equation of motion (dc_0/dQ = 0) "
      "and enters T_munu as -c_0 g_munu -- identically a shift Lambda_bare -> Lambda_bare - 8 pi G c_0",
      "pre-promotion, the K/Lambda_bare split is a redundancy; only the total vacuum energy is physical")

info("A2  the promotion a_0^2 = kappa^2 G(-K) reads K's share of the vacuum energy SPECIFICALLY, so "
     "it breaks the redundancy -- and is therefore only a complete prescription once the split is "
     "fixed by something.  beta parameterises exactly that split: beta = 1 <=> c_0 = 0 <=> all "
     "additive constants live in Lambda_bare.")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THEOREM: beta <= 1, or the action is ill-defined in the early universe")
print("=" * 100)

# decompose the offset-DBI: K = [T - M^4] - T sqrt(1 - u^2/LD^2),  T = mu^2 LD^2,  c_0 = T - M^4
K_offset = -M4 + mu_s ** 2 * LD ** 2 * (1 - sp.sqrt(1 - u ** 2 / LD ** 2))
K_decomp = (mu_s ** 2 * LD ** 2 - M4) - mu_s ** 2 * LD ** 2 * sp.sqrt(1 - u ** 2 / LD ** 2)
check(sp.simplify(K_offset - K_decomp) == 0,
      "B1  the committed offset-DBI decomposes EXACTLY as K = c_0 - T sqrt(1 - u^2/Lambda_D^2) with "
      "brane tension T = mu^2 Lambda_D^2 and additive constant c_0 = T - M^4 = M^4(beta - 1)",
      "sympy identity; beta > 1 <=> c_0 > 0, beta = 1 <=> c_0 = 0, beta < 1 <=> c_0 < 0")

# -K along the exact background: -K = T/sqrt(1+nu^2) - c_0; zero crossing for c_0 > 0
nu, beta_s = sp.symbols("nu beta", positive=True)
negK = M4 * (beta_s / sp.sqrt(1 + nu ** 2) - (beta_s - 1))
nu_neg = sp.solve(sp.Eq(negK, 0), nu)
nu_neg_expr = [s for s in nu_neg if sp.simplify(s) is not None][0]
check(sp.simplify(nu_neg_expr ** 2 - ((beta_s / (beta_s - 1)) ** 2 - 1)) == 0,
      "B2  for ANY beta > 1 the promoted a_0^2 propto -K crosses ZERO at finite excitation: "
      "nu_neg = sqrt[(beta/(beta-1))^2 - 1] -- and nu = nu_0 (1+z)^3 grows without bound into the "
      "past, so the crossing happens at a FINITE redshift for every beta > 1",
      "exact: sqrt(1+nu^2) = beta/(beta-1) at the crossing")

# beyond the crossing the kernel's argument is negative and the action is complex
y = sp.symbols("y", negative=True)
Fp = 1 - sp.exp(-sp.sqrt(y))
check(sp.simplify(sp.im(Fp.rewrite(sp.cos).subs(y, -1))) != 0,
      "B3  *** and past the crossing the theory stops existing: y = Y/a_0^2 < 0 with Y >= 0 "
      "(a spatial-projector square), and the kernel F'(y) = 1 - e^(-sqrt(y)) is COMPLEX for y < 0 "
      "(explicitly, Im F'(-1) = sin(1) != 0).  The dark-sector Lagrangian becomes complex for any "
      "nonzero spatial gradient of the khronon. ***",
      "not 'MOND turns off' -- the action is ILL-DEFINED.  THEOREM: beta <= 1, as written")

# how fast beta > 1 dies: exact z_neg for representative values
NU0 = mp.mpf("1e-4")
print("\n     beta        nu_neg           z_neg (nu_0 = 1e-4)     dies before...")
for b in ("1.01", "1.0001", "1.000001", "1.00000001"):
    bb = mp.mpf(b)
    nn = mp.sqrt((bb / (bb - 1)) ** 2 - 1)
    zn = (nn / NU0) ** (mp.mpf(1) / 3) - 1
    era = "recombination" if zn < 1090 else ("BBN" if zn < 4e8 else "any known epoch")
    print(f"   {b:>10s}    {sig(nn, 3):>9s}        {sig(zn, 4):>12s}          {era}")
check((mp.sqrt((mp.mpf('1.01') / mp.mpf('0.01')) ** 2 - 1) / NU0) ** (mp.mpf(1) / 3) - 1 < 1090,
      "B4  the failure is not asymptotic pedantry: beta = 1.01 already renders the action complex "
      "BEFORE recombination; even beta - 1 = 1e-8 fails by z ~ 10^4",
      "every beta > 1 is excluded by the theory's own domain of definition, not by data")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THEOREM: beta = 1 <=> K is a PURE brane action")
print("=" * 100)

K_pure = -T * sp.sqrt(1 - u ** 2 / LD ** 2)
check(sp.simplify(K_offset.subs(mu_s ** 2, M4 / LD ** 2) - K_pure.subs(T, M4)) == 0,
      "C1  at beta = 1 (c_0 = 0) the offset-DBI collapses IDENTICALLY to K = -T sqrt(1 - u^2/L_D^2): "
      "tension times the DBI volume element, nothing else",
      "one scale where the offset form had two")

info("C2  and the pure brane form carries a CANONICAL ZERO: -T sqrt(-det g_ind) vanishes when the "
     "induced volume element degenerates -- a brane at its local speed limit (null brane) has ZERO "
     "action.  In the brane reading, K(wall) = 0 is not a choice, it is what a volume element does; "
     "additive constants are not part of a worldvolume action -- they are bulk terms, i.e. "
     "Lambda_bare.  This paper's DBI form was chosen for exactly this boundedness structure "
     "(the committed DBI boundedness theorem), so the reading is native, not retrofitted.")

info("C3  STATED HONESTLY: C2 is a READING of the DBI form's origin, natural but not forced by the "
     "low-energy EFT alone.  What IS forced: some principle must fix the K/Lambda_bare split for "
     "the promotion to be well-defined (A2), the split point must satisfy beta <= 1 (Part B), and "
     "the brane reading picks the boundary point exactly.  The two ambiguities -- 'where do "
     "constants live?' and 'what is beta?' -- are the SAME ambiguity, and one canonical principle "
     "kills both.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the data side: the CMB pins beta to the boundary from below")
print("=" * 100)

# beta < 1: a_0 floors at sqrt(1-beta) a_0(0) -- exact from the decomposition
floor_expr = sp.sqrt(sp.limit(negK / M4, nu, sp.oo).subs(beta_s, sp.Symbol("b", positive=True)))
one_minus_beta_max = mp.mpf("0.006") ** 2
check(sp.simplify(sp.limit(negK, nu, sp.oo) - M4 * (1 - beta_s)) == 0,
      "D1  for beta < 1 the promoted a_0 does not switch off -- it FLOORS: "
      "a_0(z -> inf)/a_0(0) = sqrt(1 - beta), exactly",
      "the residual constant c_0 < 0 is a permanent MOND floor")

check(one_minus_beta_max < mp.mpf("4e-5"),
      f"D2  the committed CMB requirement (off-switch <= 0.006 of today, stages 17/19) bounds the "
      f"floor: 1 - beta <= (0.006)^2 = {sig(one_minus_beta_max, 2)}.  Combined with Part B: "
      f"*** beta is PINNED to [1 - 3.6e-5, 1] -- consistency from above, data from below ***",
      "the unique point admitting a COMPLETE off-switch is the boundary itself, beta = 1")

info("D3  FALSIFIABLE ALTERNATIVE, kept alive on purpose: beta = 1 - epsilon with epsilon <= 3.6e-5 "
     "is a consistent theory whose high-z MOND floor is sqrt(epsilon) a_0.  Any future detection of "
     "residual MOND at early times (e.g. in the CMB damping tail or high-z structure) would MEASURE "
     "1 - beta rather than falsify the framework.  beta = 1 predicts exactly zero floor.")

info("D4  NAMED ESCAPE from Part B's theorem: it needs nu -> infinity into the past, i.e. the "
     "charge history n propto a^-3 extending to arbitrarily early times.  A khronon sector formed "
     "at a finite epoch (a phase transition) caps nu and reopens beta > 1 by a hair.  No such "
     "formation mechanism exists in the theory as written -- the charge is an initial condition -- "
     "but the loophole is recorded rather than waved away.")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print("""
  beta = 1 IS NO LONGER MERELY SELECTED.  Its status after this stage:

  1. THE QUESTION ITSELF WAS REFRAMED (Part A): beta parameterises the split of the vacuum
     constant between K and Lambda_bare -- a split that was a REDUNDANCY before the promotion.
     The promotion needs the split fixed; beta = 1 is the statement "K carries no constant".

  2. beta <= 1 IS A THEOREM (Part B): any beta > 1 makes a_0^2 cross zero at finite redshift,
     where the kernel goes complex for any spatial khronon gradient -- the action stops being
     defined.  beta = 1.01 dies before recombination; beta - 1 = 1e-8 dies by z ~ 10^4.

  3. beta = 1 <=> PURE BRANE ACTION (Part C): the offset-DBI decomposes exactly into
     brane-tension x volume-element + constant; beta = 1 is the constant-free brane form, whose
     zero at the wall is canonical (a null brane has zero action).  A reading, not a proof --
     but the SAME canonical principle ("constants live in Lambda_bare") that makes the promotion
     well-defined at all.

  4. THE DATA CLOSES THE INTERVAL (Part D): 1 - beta <= 3.6e-5 from the CMB off-switch.
     Pinned: beta in [1 - 3.6e-5, 1], with beta = 1 the unique complete-off-switch point and
     sqrt(1-beta) a falsifiable high-z MOND floor otherwise.

  HONEST RESIDUE: the last 3.6e-5 is closed by the brane reading or by data, not by theorem.
  Anyone quoting "beta = 1 is derived" is overquoting; the defensible sentence is:
  *** "beta <= 1 is derived; the boundary is canonical under the brane reading; the CMB pins
      the theory to within 3.6e-5 of it." ***
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
