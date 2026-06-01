#!/usr/bin/env python3
"""
The rigorous version of "3 from 3 planes": (T^2)^3 / (Z2 x Z2) three twisted sectors.
====================================================================================

The framework's "3 generations from 3 directions" (heuristically "3 = b_1(T^3)") has
a genuine, standard-physics home: the heterotic Z2xZ2 orbifold of T^6 = (T^2)^3, where
family triplication is the THREE TWISTED SECTORS = the three internal 2-planes (Faraggi
et al., the most realistic 3-family string models).

This script computes the rigorous geometric backbone and states honestly which part is
forced (the x3 triplication) and which is model-building (exactly one family per sector).

Pure stdlib + numpy.  Run:  python reviews/z2z2_three_generations.py
"""

import itertools
import numpy as np

# A Z2 element acting on the 3 complex planes is a sign vector in {+1,-1}^3,
# where -1 means z -> -z on that plane.
ALL_SIGNS = list(itertools.product([+1, -1], repeat=3))


def susy_group():
    """The SUSY-preserving Z2xZ2: each element must lie in SU(3), i.e. product of
    the three eigenvalues = +1 (det = +1). That selects the 4 sign-vectors with an
    EVEN number of -1's -- the Klein four-group."""
    return [s for s in ALL_SIGNS if np.prod(s) == +1]


def part1_group_and_sectors():
    print("=" * 80)
    print("(1) The SUSY Z2xZ2 on (T^2)^3: three twisted sectors, one per plane")
    print("=" * 80)
    G = susy_group()
    print("   Calabi-Yau / N=1 SUSY condition: each element has det = +1 (in SU(3)).")
    print("   The 4 elements with an even number of sign-flips (Klein four-group):")
    names = {(+1,+1,+1): "1  (identity)", (+1,-1,-1): "theta  ",
             (-1,+1,-1): "omega  ", (-1,-1,+1): "theta*omega"}
    nontrivial = []
    for s in G:
        s = tuple(s)
        fixed_plane = [i+1 for i, v in enumerate(s) if v == +1]
        det = int(np.prod(s))
        tag = names.get(s, str(s))
        if s != (1, 1, 1):
            nontrivial.append((tag, s, fixed_plane[0] if fixed_plane else None))
        print(f"     {tag:<14} signs={s}  det={det:+d}  fixes plane(s) {fixed_plane}")
    print()
    print(f"   => {len(nontrivial)} non-trivial elements, and each fixes EXACTLY ONE")
    print( "      2-plane while reflecting the other two:")
    for tag, s, fp in nontrivial:
        print(f"        {tag:<12} -> twisted sector localized on plane {fp}")
    print("   The THREE twisted sectors = the three internal 2-planes. This is the")
    print("   rigorous origin of family triplication (x3). [det=+1 = the reason this")
    print("   even-dim Z2xZ2 preserves SUSY, unlike the odd T^3/Z2 with det(-I_3)=-1.]\n")
    return nontrivial


def part2_fixed_points(nontrivial):
    print("=" * 80)
    print("(2) Fixed points per twisted sector")
    print("=" * 80)
    # z -> -z on one T^2 has 4 fixed half-period points: {0, 1/2, tau/2, (1+tau)/2}
    fp_per_T2 = 4
    print(f"   On each reflected T^2, z -> -z fixes {fp_per_T2} half-period points")
    print( "   {0, 1/2, tau/2, (1+tau)/2}. Each sector reflects TWO planes:")
    for tag, s, fp in nontrivial:
        n_fixed = fp_per_T2 * fp_per_T2     # 4 x 4 on the two reflected planes
        print(f"     {tag:<12} : {fp_per_T2} x {fp_per_T2} = {n_fixed} fixed points "
              f"(x the un-reflected plane {fp})")
    print("   => 16 fixed points per twisted sector, 3 x 16 = 48 fixed tori total.\n")
    return 16


def part3_hodge_and_count(fp_per_sector):
    print("=" * 80)
    print("(3) Hodge numbers, Euler character, and the generation count")
    print("=" * 80)
    h11, h21 = 51, 3              # standard T^6/(Z2xZ2) resolution (no discrete torsion)
    chi = 2 * (h11 - h21)
    print(f"   Resolved Calabi-Yau T^6/(Z2xZ2):  (h^1,1, h^2,1) = ({h11}, {h21})")
    print(f"   Euler characteristic chi = 2(h11 - h21) = {chi}.")
    print(f"   KEY: h^2,1 = {h21} = the three complex-structure moduli = the three T^2's.")
    print( "        That '3' is the geometric origin of the three families.")
    print()
    naive = abs(chi) // 2
    print(f"   Standard-embedding net generations = |chi|/2 = {naive}.")
    print(f"   That is {fp_per_sector} per sector x 3 sectors = {fp_per_sector*3}... i.e.")
    print( "   the NAIVE count is 48, NOT 3 -- the 16 fixed points per sector are not")
    print( "   yet projected down.\n")
    return naive


def part4_verdict():
    print("=" * 80)
    print("VERDICT -- what is forced vs chosen")
    print("=" * 80)
    print("  FORCED / GEOMETRIC (rigorous):")
    print("   * The SUSY Z2xZ2 on (T^2)^3 has exactly THREE non-trivial elements, each")
    print("     fixing one 2-plane -> THREE twisted sectors -> family triplication x3.")
    print("   * h^2,1 = 3 (the three 2-tori) is the topological '3'. This is the real,")
    print("     standard mechanism the framework's '3 from 3 planes' was shadowing, and")
    print("     it lives on an EVEN-dim space where a chiral index actually exists.")
    print()
    print("  CHOSEN / MODEL-BUILDING (not forced):")
    print("   * The naive net count is |chi|/2 = 48 (16 fixed points x 3 sectors).")
    print("     Getting EXACTLY 3 (one family per sector) requires Wilson lines /")
    print("     asymmetric shifts that project 16 -> 1 -- exactly what the free-fermionic")
    print("     3-generation literature (Faraggi et al.) uses. That projection is a")
    print("     choice, and the orbifold T^6/(Z2xZ2) itself is a chosen geometry.")
    print()
    print("  NET: this upgrades '3 generations' from a Betti-number assertion to the")
    print("  genuine three-twisted-sector mechanism -- the x3 triplication is rigorous")
    print("  and geometric. But exactly-3 still needs a chosen projection, and the '3'")
    print("  is the three 2-tori you chose. Mechanism real; number still not derived.")
    print("  Same frontier as all of string phenomenology (no one forces 3).")


def main():
    nt = part1_group_and_sectors()
    fp = part2_fixed_points(nt)
    part3_hodge_and_count(fp)
    part4_verdict()


if __name__ == "__main__":
    main()
