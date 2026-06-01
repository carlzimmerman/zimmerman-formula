#!/usr/bin/env python3
"""
The honest chiral index on (T^2)^3/(Z2xZ2) -- correcting NN's script AND my own.
===============================================================================

The NIELSEN_NINOMIYA script claims N_gen=3 = "number of 1-cycles of T^3" (wrong),
via four incoherent routes. The honest question this raises: does the orbifold
ACTUALLY give 3 chiral generations, and is 3 forced or chosen? My own earlier
z2z2_three_generations.py said "3 from 3 twisted sectors" -- a clean heuristic.
This script does it the rigorous way and reports the result, which revises BOTH.

The correct mechanism: generations = the CHIRAL INDEX (net L-R zero modes) of the
Dirac operator on the orbifold, NOT the number of 1-cycles. The index is set by
the orbifold's fixed-point structure (twisted sectors) and the gauge bundle.

Pure stdlib. Run:  python reviews/orbifold_chiral_index_honest.py
"""

import math


def part1_mechanism():
    print("=" * 78)
    print("(1) The CORRECT object: the chiral index, not the cycle count")
    print("=" * 78)
    print("   Nielsen-Ninomiya script: N_gen = #(1-cycles of T^3) = dim H_1(T^3)=3. WRONG.")
    print("   1-cycles are momentum/winding directions; generations are the net chiral")
    print("   zero-mode count: Index(D) = n_L - n_R (Atiyah-Singer). The numerical match")
    print("   3=3 is a coincidence -- the mechanisms are unrelated. The real count comes")
    print("   from the orbifold TWISTED SECTORS (fixed points), below.\n")


def part2_fixed_points():
    print("=" * 78)
    print("(2) COMPUTED: the fixed-point structure of Z2xZ2 on (T^2)^3")
    print("=" * 78)
    # Group elements act on the 3 T^2's. Non-trivial elements act as -1 on TWO T^2's,
    # +1 on one. A -1 (inversion) on a single T^2 has 4 fixed points (half-periods).
    elements = {
        "g1   = (-1,-1,+1)": (-1, -1, +1),
        "g2   = (+1,-1,-1)": (+1, -1, -1),
        "g1g2 = (-1,+1,-1)": (-1, +1, -1),
    }
    fp_per_T2_inversion = 4   # |T^2[2]| = 4 two-torsion points
    total_fixed_tori = 0
    print("   each -1 on a single T^2 has 4 fixed points; +1 leaves that T^2 free.")
    print(f"   {'element':<22}{'fixed locus':<28}{'# fixed tori':>12}")
    for name, act in elements.items():
        n_inv = sum(1 for a in act if a == -1)      # number of inverted T^2's (=2)
        n_free = sum(1 for a in act if a == +1)     # the surviving T^2 (=1)
        fixed = fp_per_T2_inversion ** n_inv        # 4^2 = 16 fixed points in the 2 inverted T^2's
        total_fixed_tori += fixed
        locus = f"{fixed} copies of the free T^2"
        print(f"   {name:<22}{locus:<28}{fixed:>12}")
    print(f"   ----------------------------------------------------------------")
    print(f"   3 twisted sectors x 16 = {total_fixed_tori} fixed tori total. (COMPUTED.)")
    print("   Each fixed torus hosts twisted-sector chiral matter. So there are 48")
    print("   loci of chiral matter -- NOT 3. '3 sectors' counts the GROUP elements,")
    print("   not the generations.\n")
    return total_fixed_tori


def part3_generation_count():
    print("=" * 78)
    print("(3) CITED (literature): the bare generation number is ~48, not 3")
    print("=" * 78)
    # Standard Z2xZ2 orbifold of T^6 (no discrete torsion):
    h11, h21 = 51, 3            # Hodge numbers (well-known; the discrete-torsion mirror swaps them)
    chi = 2 * (h11 - h21)
    n_gen_bare = abs(chi) // 2
    print(f"   The Z2xZ2 orbifold of T^6 has (standard embedding, no discrete torsion):")
    print(f"     Hodge numbers h^(1,1)={h11}, h^(2,1)={h21}  [literature value, CITED]")
    print(f"     Euler characteristic chi = 2(h11 - h21) = {chi}")
    print(f"     net chiral generations = |chi|/2 = {n_gen_bare}")
    print(f"   => the BARE orbifold gives ~{n_gen_bare} generations, NOT 3.")
    print("   (Discrete torsion gives the mirror, chi=-96, same |chi|/2=48.)")
    print("   Getting down to exactly 3 requires WILSON LINES / freely-acting shifts")
    print("   that quotient the 48 -- the Faraggi-class three-generation construction.")
    print("   That reduction is a MODEL-BUILDING CHOICE, not a topological necessity.\n")
    return n_gen_bare


def main():
    part1_mechanism()
    part2_fixed_points()
    n = part3_generation_count()
    print("=" * 78)
    print("VERDICT -- what is actually true about orbifold chirality (revising both)")
    print("=" * 78)
    print("  REAL: the orbifold genuinely produces a chiral index -- chiral fermions")
    print("  from twisted sectors, evading Nielsen-Ninomiya. This part is legitimate")
    print("  physics and it is the framework's strongest particle-side claim.")
    print()
    print("  BUT the number is NOT topologically forced to 3:")
    print("   * the NN script's '3 = #(1-cycles)' is the wrong object (coincidence 3=3);")
    print(f"   * the bare Z2xZ2 orbifold gives |chi|/2 = {n} generations, not 3;")
    print("   * reducing to exactly 3 needs Wilson lines (a CHOICE), consistent with")
    print("     generation_number_tadpole_anomaly.py (anomalies are generation-blind).")
    print()
    print("  SELF-CORRECTION: my own z2z2_three_generations.py framed '3 from 3 twisted")
    print("  sectors' as if rigorous. It is a HEURISTIC -- '3 sectors' counts the group")
    print("  elements, not the generations. The rigorous bare count is 48; 3 is a Wilson-")
    print("  line model-building choice. The chirality survivor stands; the clean '3 from")
    print("  3' does not. The blade cuts my earlier claim too -- which is the point.")


if __name__ == "__main__":
    main()
