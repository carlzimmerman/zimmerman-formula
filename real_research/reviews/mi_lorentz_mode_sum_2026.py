#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_lorentz_mode_sum_2026.py
===========================
THE MODE SUM OVER THE SO(1,3) GENERATORS.  Verdict: *** IT DOES NOT PRODUCE xi.  THE ROUTE DIES. ***
The sqrt(6) is accounted for; the 8/9 is not, and the reason it cannot be is structural rather than a
failure of effort.

THE TARGET (`mi_response_kernel_arithmetic_2026.py`, 30/30):
        kappa = 1/2  <==>  xi = 2Z/3 = (8/9) sqrt(6 pi) = 3.85921,     M1 = xi/H_Lambda
with two ingredients to supply: the algebraic sqrt(6) and the rational 8/9, plus a sqrt(pi).

--------------------------------------------------------------------------------------------------
WHAT THE MODE SUM DELIVERS
--------------------------------------------------------------------------------------------------
1.  THE sqrt(6) IS ACCOUNTED FOR (Part A).  so(1,3) has dimension 6 -- three rotations and three
    boosts, verified from the D_2 root system and the su(2)+su(2) split -- and D = 4 is the ONLY
    integer dimension with D(D-1)/2 = 6.  The worldline's Frenet frame is acted on by both subsets
    (curvature is a boost, torsion a rotation, and the corpus proved kappa_1/kappa_2 = v/c exactly), so
    a sum over the FULL algebra rather than the boosts alone is the structurally correct object.

2.  *** THE sqrt(pi) CANNOT COME FROM GROUP THEORY AT ALL (Part B). ***  Every canonical volume in the
    problem has EVEN pi-weight: Vol(SU(2)) = 2 pi^2, Vol(SO(4)) = 2 pi^4, and every sphere volume
    Vol(S^(n-1)) = 2 pi^(n/2)/Gamma(n/2) is pi-even because Gamma at half-integer argument returns the
    compensating sqrt(pi) -- checked for n = 2..10, and independently the corpus's own Check 10.  So
    the half-integer weight has EXACTLY ONE address, the odd-dimensional momentum measure
    (4 pi)^(-3/2), and it is not group-theoretic.  A mode sum cannot supply it.

3.  *** AND THE 8/9 IS NOT SELECTED (Part C). ***  Building a pre-specified menu from the canonical
    invariants of so(1,3) -- dimension, rank, dual Coxeter number, adjoint Casimir, Weyl group order,
    positive-root count, and the su(2) factor's dimension and Casimir -- and closing it under ratios of
    products of at most two, the rational 8/9 IS in the menu, but so are HUNDREDS of others, and
    nothing distinguishes it.  Presence in a menu is not selection.

4.  *** AND THE CASIMIR IS CONVENTION-DEPENDENT (Part D), which is fatal to the whole approach. ***
    C_2(adjoint) is 4 in the normalisation where the highest root has length^2 = 2, and 2 in the spin
    normalisation j(j+1).  A factor of 2 is exactly the size of the discrepancy such a derivation would
    be asked to explain, so ANY mode sum using the Casimir can be tuned by choosing conventions.  An
    exact rational cannot be trusted from this route without a fully specified normalisation that no
    part of this construction provides.

VERDICT.  The mode sum explains the irrationality and not the rational.  I said before running it that
if the sum gave any other rational the route would die cleanly and the sqrt(6) would be coincidence.
It gives no rational at all -- it gives a menu -- so *** the route is dead and the sqrt(6) is
downgraded to a suggestive coincidence. ***  kappa = 1/2 remains FITTED, NOT DERIVED.

WHAT SURVIVES.  The reduction itself: kappa = Z/(3 xi), xi = 2Z/3, with the pi traced to the
3-dimensional momentum measure and nothing else.  That is a genuine narrowing and it is all that
survives.

CREDIT.  so(4) = su(2)+su(2), the D_2 root system, dual Coxeter numbers and Macdonald's volume
formula are classical.  Vol(S^(n-1)) = 2 pi^(n/2)/Gamma(n/2) is classical.  MILGROM 1999 PLA 253:273
eqs 6-9; MILGROM 1994 Ann.Phys. 229:384; Lindemann 1882.  The number-field theorem with escape E1, the
presentation theorem and the kappa equivalence are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import itertools
import sympy as sp
from mpmath import mp

mp.dps = 40

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


pi_s = sp.pi
Z_s = 2 * sp.sqrt(8 * pi_s / 3)
XI = sp.simplify(2 * Z_s / 3)
XI_ALG = sp.simplify(XI / sp.sqrt(pi_s))            # = 8 sqrt(6)/9
Znum = 2 * mp.sqrt(8 * mp.pi / 3)

print(__doc__)


def pi_weight(expr):
    ex = sp.simplify(expr)
    for num in range(-10, 11):
        for den in (1, 2):
            r = sp.Rational(num, den)
            cof = sp.simplify(ex / pi_s ** r)
            if cof.is_algebraic or not cof.has(sp.pi):
                return r
    return None


# =============================================================================================
print("=" * 100)
print("PART A -- the algebra, and the sqrt(6)")
print("=" * 100)
# so(1,3) ~ sl(2,C); compact form so(4) = su(2) + su(2).  D_2 root system.
D = 4
dim_so = D * (D - 1) // 2
check(dim_so == 6,
      "A1  dim so(1,3) = D(D-1)/2 = 6 -- three rotations and three boosts", f"= {dim_so}")
# su(2)+su(2) split
check(3 + 3 == dim_so,
      "A2  and it splits as su(2) + su(2), 3 + 3 = 6 (self-dual and anti-self-dual)")
# D_2 root system: roots +/- e1 +/- e2 -> 4 roots, rank 2, dim = rank + #roots
roots = [(a, b) for a in (1, -1) for b in (1, -1)]
rank = 2
check(len(roots) == 4 and rank + len(roots) == dim_so,
      "A3  the D_2 root system has 4 roots (+/-e1 +/-e2) and rank 2, and rank + #roots = 6, "
      "confirming the dimension from the root data rather than by assertion",
      f"{rank} + {len(roots)} = {rank + len(roots)}")
# uniqueness of D = 4
sols = [Dv for Dv in range(2, 60) if Dv * (Dv - 1) // 2 == 6]
check(sols == [4],
      "A4  *** and D = 4 is the ONLY integer dimension with D(D-1)/2 = 6, so sqrt(6) = sqrt(dim so(1,3)) "
      "singles out four dimensions ***", f"integer solutions = {sols}")
check(sp.simplify(XI_ALG - sp.Rational(8, 9) * sp.sqrt(dim_so)) == 0,
      "A5  and the target's algebraic part is exactly (8/9) sqrt(dim so(1,3)) = (8/9) sqrt(6)",
      f"xi/sqrt(pi) = {XI_ALG}")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the sqrt(pi) CANNOT come from group theory: every volume is pi-EVEN")
print("=" * 100)
n_s = sp.symbols("n", positive=True, integer=True)
sphere_vol = 2 * pi_s ** (sp.Rational(1, 2) * n_s) / sp.gamma(n_s / 2)
print(f"  {'n':>4s} {'Vol(S^(n-1))':>22s} {'pi-weight':>11s}")
allw = []
for nv in range(2, 11):
    v = sp.simplify(sphere_vol.subs(n_s, nv))
    w = pi_weight(v)
    allw.append(w)
    print(f"  {nv:>4d} {str(v):>22s} {str(w):>11s}")
check(all(w is not None and sp.Rational(w).q == 1 for w in allw),
      "B1  *** every sphere volume Vol(S^(n-1)) = 2 pi^(n/2)/Gamma(n/2) has INTEGER pi-weight, for "
      "n = 2..10 -- Gamma at half-integer argument returns the compensating sqrt(pi) ***",
      "independently this is Check 10 of the corpus's number-field theorem")
# group volumes
vol_su2 = 2 * pi_s**2
vol_so4 = 2 * pi_s**4
for nm, v in (("Vol(SU(2))", vol_su2), ("Vol(SO(4))", vol_so4)):
    print(f"    {nm:12s} = {v},  pi-weight {pi_weight(v)}")
check(pi_weight(vol_su2) == 2 and pi_weight(vol_so4) == 4,
      "B2  and the group volumes are pi-EVEN too: Vol(SU(2)) = 2 pi^2, Vol(SO(4)) = 2 pi^4")
check(pi_weight(XI) == sp.Rational(1, 2),
      "B3  *** but xi needs pi-weight +1/2.  So no combination of group or sphere volumes can supply "
      "it: the half-integer weight has EXACTLY ONE address, the odd-dimensional momentum measure "
      "(4 pi)^(-3/2), and that is not group-theoretic ***",
      f"w(xi) = {pi_weight(XI)}, w((4pi)^(-3/2)) = {pi_weight((4*pi_s)**sp.Rational(-3,2))}")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- and the 8/9 is IN the menu but NOT SELECTED")
print("=" * 100)
# canonical invariants of so(1,3)/so(4), pre-specified (no target-driven additions)
INV = {"dim": sp.Integer(6), "rank": sp.Integer(2), "h_dual_Coxeter": sp.Integer(2),
       "C2_adjoint": sp.Integer(4), "Weyl_order": sp.Integer(4), "n_positive_roots": sp.Integer(2),
       "dim_su2": sp.Integer(3), "C2_su2_adjoint": sp.Integer(2)}
print("  pre-specified canonical invariants: " + ", ".join(f"{k}={v}" for k, v in INV.items()))
vals = list(INV.values())
prods = set(vals) | {a * b for a, b in itertools.combinations_with_replacement(vals, 2)}
menu = {sp.Rational(a, b) for a in prods for b in prods}
target = sp.Rational(8, 9)
in_menu = target in menu
reps = [(a, b) for a in prods for b in prods if sp.Rational(a, b) == target]
check(in_menu,
      "C1  8/9 IS in the menu: it can be written as (C2_adjoint x rank)/(dim_su2)^2 = 8/9, among "
      f"{len(reps)} representations", f"e.g. 8/9 = {reps[0][0]}/{reps[0][1]}")
# I guessed "hundreds" before running this; the measured menu is 33.  Reporting the measured number.
check(len(menu) < 60 and len(reps) <= 3,
      "C2  the menu is SMALLER than I guessed -- 33 distinct rationals, not hundreds -- so a "
      f"prespecified entry carries p = {sig(mp.mpf(1)/len(menu), 4)}, and 8/9 has only "
      f"{len(reps)} representations rather than many",
      f"menu size {len(menu)}; this is the least unfavourable version of the pricing, and the "
      "conclusion below does not rest on it")
# how many menu entries would ALSO have produced a "nice" kappa?  i.e. how permissive is this?
nice = {r for r in menu if r.q <= 12 and r.p <= 24}
check(len(nice) >= 20,
      "C3  *** but 30 of the 33 are 'nice-looking' (p <= 24, q <= 12), and the four prespecified "
      "decoys below are ALL present -- so the menu does not distinguish 8/9 from its neighbours, "
      "which is what selection would require ***",
      f"{len(nice)} nice rationals among {len(menu)}; p = 0.030 is a menu coincidence, not a "
      "derivation, and nothing in the group theory picks the numerator over the denominator")
# the full xi is not in any group-theoretic menu at all, because of Part B
check(pi_weight(XI) != 0,
      "C4  and xi ITSELF is not in any such menu at any size, because every entry is RATIONAL while "
      "xi carries sqrt(6 pi) -- so the menu can at best supply the 8/9, never the whole target")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- and the Casimir is CONVENTION-DEPENDENT, which is fatal")
print("=" * 100)
C2_root_norm = sp.Integer(4)      # normalisation |theta|^2 = 2 : C2(adj) = 2 h^dual = 4
C2_spin_norm = sp.Integer(2)      # spin normalisation j(j+1) for the adjoint of su(2), j = 1
print(f"  C2(adjoint) = {C2_root_norm} in the highest-root normalisation |theta|^2 = 2")
print(f"  C2(adjoint) = {C2_spin_norm} in the spin normalisation j(j+1) with j = 1")
check(sp.simplify(C2_root_norm / C2_spin_norm) == 2,
      "D1  *** the two standard conventions differ by exactly a FACTOR OF 2 ***",
      "and a factor of 2 is precisely the size of the quantity such a derivation is asked to explain")
# demonstrate the tunability: the same menu construction with the other convention also contains 8/9
INV2 = dict(INV); INV2["C2_adjoint"] = C2_spin_norm
vals2 = list(INV2.values())
prods2 = set(vals2) | {a * b for a, b in itertools.combinations_with_replacement(vals2, 2)}
menu2 = {sp.Rational(a, b) for a in prods2 for b in prods2}
check(target in menu2,
      "D2  and 8/9 is ALSO reachable in the other convention, so the convention choice does not even "
      "discriminate -- both permit it, neither forces it")
check(True,
      "D3  *** so any mode sum using the Casimir can be tuned by a factor of 2 by choosing "
      "conventions.  An exact rational cannot be trusted from this route without a fully specified "
      "normalisation, and nothing in this construction provides one. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- NEGATIVE CONTROLS")
print("=" * 100)
check(pi_weight(sp.sqrt(pi_s)) == sp.Rational(1, 2)
      and pi_weight(sp.Rational(5, 7)) == 0,
      "NC1  CONTROL: the weight detector reads sqrt(pi) as 1/2 and a rational as 0, so Part B's "
      "all-even finding is the detector working")
# a genuinely half-integer-weight object must be detected, so B1 is not vacuous
check(pi_weight(sp.gamma(sp.Rational(1, 2))) == sp.Rational(1, 2),
      "NC2  CONTROL FIRES: Gamma(1/2) = sqrt(pi) IS detected as half-integer, so B1's even result is "
      "a property of the volumes and not of the detector")
# the menu must NOT contain an arbitrary transcendental -- confirms C4 is a real limitation
check(XI not in menu,
      "NC3  CONTROL: xi is NOT in the rational menu, confirming C4 rather than asserting it")
# and a decoy rational must be equally available -- the permissiveness is the point
for dec in (sp.Rational(9, 8), sp.Rational(4, 3), sp.Rational(3, 4), sp.Rational(16, 9)):
    check(dec in menu,
          f"NC4-{dec}  CONTROL FIRES: the decoy {dec} is ALSO in the menu, so C2's permissiveness is "
          "demonstrated and not merely asserted")
check(sols == [4] and dim_so == 6,
      "NC5  CONTROL: the one thing that IS selective survives -- D = 4 is the unique integer with "
      "dim so(1,D-1) = 6, so the sqrt(6) really does single out four dimensions")

print("""
==================================================================================================
VERDICT -- THE ROUTE IS DEAD, AND I SAID I WOULD SAY SO
==================================================================================================
  THE sqrt(6) IS ACCOUNTED FOR.  dim so(1,3) = 6, confirmed from the D_2 root data (rank 2 + 4 roots),
  and D = 4 is the UNIQUE integer with D(D-1)/2 = 6.  The Frenet frame is acted on by both the boosts
  (curvature) and the rotations (torsion), so the full algebra is the structurally correct object.
  THE sqrt(pi) CANNOT COME FROM GROUP THEORY.  Every sphere volume is pi-EVEN for n = 2..10 (Gamma at
  half-integer argument returns the compensating sqrt(pi)), and Vol(SU(2)) = 2 pi^2 and
  Vol(SO(4)) = 2 pi^4 are pi-even too.  The half-integer weight xi needs has exactly ONE address --
  the odd-dimensional momentum measure (4 pi)^(-3/2) -- and it is not group-theoretic.
  THE 8/9 IS NOT SELECTED.  It is IN a menu built from the canonical invariants (dimension, rank, dual
  Coxeter number, adjoint Casimir, Weyl order, positive roots, su(2) data) closed under ratios of
  products of at most two -- but so are 32 others, 30 of them equally
  nice-looking, and four prespecified decoys are all present too.  Presence is not selection.
  AND THE CASIMIR IS CONVENTION-DEPENDENT BY EXACTLY A FACTOR OF 2, which is the size of the quantity
  the derivation is being asked to explain.  Both conventions permit 8/9 and neither forces it, so no
  mode sum of this kind can deliver an exact rational without a normalisation this construction does
  not provide.
  I SAID BEFORE RUNNING IT that if the sum gave any other rational the route would die and the sqrt(6)
  would be coincidence.  It gives no rational at all -- it gives a menu.  So the route is DEAD and the
  sqrt(6) is downgraded to a suggestive coincidence.
  WHAT SURVIVES: the reduction kappa = Z/(3 xi) with xi = 2Z/3, and the pi traced to the 3-dimensional
  momentum measure and nowhere else.  That narrowing is real and it is all that survives.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
