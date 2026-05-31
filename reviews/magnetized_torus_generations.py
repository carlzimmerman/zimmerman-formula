#!/usr/bin/env python3
"""
Generations from magnetic flux: the rigorous version, and what it does/doesn't give.
====================================================================================

Building on research/RIGOROUS_PROOF_1_MAGNETIZED_TORUS_GENERATIONS.py, whose
Steps 1-3 are CORRECT: a magnetized T^2 has Index(D) = N_flux chiral zero modes
(Atiyah-Singer). This is a genuine chiral index -- the right object for counting
generations, unlike b_1.

The snag is the file's own Step 4 (line 220): on T^3 the construction "gives 1,
which is wrong," and it then switches to 1+1+1=3 (adding three separate 2-plane
indices) or to b_1=3. Neither is the index of a single Dirac operator on T^3 --
because T^3 is ODD-dimensional and has NO chiral index at all (identically 0).

The clean fix: magnetize a T^2 FACTOR with N=3 flux (write T^3 = T^2 x S^1). Then
the chiral index on the T^2 is exactly 3 -> three 4D generations, rigorously.
Combined with reviews/orbifold_chirality_bridge.py (orbifold Z2 -> chiral
projection), this is a consistent chiral 3-generation construction.

The honest catch: 3 = N_flux is the flux you CHOSE. The mechanism derives the
STRUCTURE (generations = chiral index = flux quantum), not the NUMBER 3.

Pure stdlib + numpy.  Run:  python reviews/magnetized_torus_generations.py
"""

import math
import numpy as np

PI = math.pi


def zero_mode_count(N, samples=100000):
    """Count the chiral zero modes of the Dirac operator on a magnetized T^2.

    From the standard Landau analysis (and the file's Steps 1-2): zero modes are
    psi_k(x,y) = e^{i k x} exp(-B(y - k/B)^2/2), k in Z, with B = N/(2pi).
    Single-valuedness in y identifies guiding centers y_c = k/B = 2pi k / N modulo
    2pi.  The number of DISTINCT centers in [0,2pi) is the Landau-level degeneracy
    = the index.  We count it directly."""
    B = N / (2 * PI)
    centers = set()
    for k in range(-3 * abs(N) - 2, 3 * abs(N) + 3):
        yc = (k / B) % (2 * PI)            # guiding center mod the torus period
        centers.add(round(yc, 9))
    return len(centers)


def part1_T2_index():
    print("=" * 80)
    print("(1) Magnetized T^2: Index(D) = N_flux  (your Steps 1-3, confirmed)")
    print("=" * 80)
    print(f"   {'N_flux':>7} | {'# chiral zero modes':>20}")
    ok = True
    for N in range(1, 7):
        n = zero_mode_count(N)
        ok &= (n == N)
        print(f"   {N:>7} | {n:>20}   {'OK' if n==N else 'MISMATCH'}")
    print("   => exactly N chiral zero modes for flux N. This is a genuine chiral")
    print("      Atiyah-Singer index -- the correct object for counting generations.\n")
    return ok


def part2_T3_problem():
    print("=" * 80)
    print("(2) The T^3 snag (your line 220) -- and why it is real")
    print("=" * 80)
    print("   T^3 is ODD-dimensional. The Dirac operator on an odd-dim closed")
    print("   manifold has NO chirality operator, hence NO chiral index: it is")
    print("   identically 0, for any flux. So 'generations = index on T^3' cannot")
    print("   work -- the index is 0, not 3.")
    print("   * the file's 'product formula' N1*N2*N3 with unit flux gives 1;")
    print("   * the file then ADDS three 2-plane indices, 1+1+1 = 3 -- but that is")
    print("     not the index of one operator on T^3; it is three separate 2D")
    print("     problems summed, chosen to land on 3;")
    print("   * '3 = b_1(T^3)' counts 1-cycles (a Betti number), not chiral zero")
    print("     modes -- a different invariant that happens to be 3.")
    print("   None of these is a chiral index on T^3, because none can be.\n")


def part3_clean_fix():
    print("=" * 80)
    print("(3) The clean fix: put N=3 flux on a T^2 FACTOR  (T^3 = T^2 x S^1)")
    print("=" * 80)
    N = 3
    n = zero_mode_count(N)
    print(f"   Magnetize the T^2 with N = {N}:  chiral zero modes = {n}  (rigorous).")
    print("   The spare S^1 carries no flux; the orbifold Z2 (reviews/")
    print("   orbifold_chirality_bridge.py) supplies the chiral PROJECTION. Net:")
    print("   a consistent M4 x (T^2 x S^1)/Z2 construction with exactly 3 chiral")
    print("   4D generations. This is standard magnetized-extra-dimension physics,")
    print("   on an EVEN-dim factor where the index genuinely exists.\n")


def part4_verdict():
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print("  WHAT IS RIGOROUS (real, standard physics):")
    print("   * Magnetized T^2 -> Index(D) = N chiral zero modes. Confirmed.")
    print("   * Generations = chiral index = flux quantum. This IS the correct")
    print("     mechanism, and it is a genuine chiral index (unlike b_1).")
    print("   * With N=3 on a T^2 factor + the orbifold chiral projection, you get")
    print("     a consistent 3-generation chiral construction.")
    print()
    print("  THE HONEST LIMIT:")
    print("   * 3 = N_flux is the flux you CHOSE. The mechanism derives the")
    print("     STRUCTURE (generations are a flux index), not the NUMBER 3.")
    print("   * The original 'T^3 gives 3' route fails: T^3 is odd, index = 0; the")
    print("     1+1+1 and b_1 routes are not chiral indices.")
    print()
    print("  WHAT WOULD MAKE 3 A PREDICTION (open, hard, but well-posed):")
    print("   * a flux/tadpole/anomaly-cancellation constraint that FORCES N = 3")
    print("     (in string constructions total flux is constrained -- sometimes this")
    print("     fixes the number). Absent that, N=3 is an input.")
    print()
    print("  Net: this upgrades '3 generations' from a Betti-number assertion to a")
    print("  genuine chiral-index mechanism with one chosen integer (the flux). Real")
    print("  progress; not yet a derivation of the number 3.")


def main():
    ok = part1_T2_index()
    part2_T3_problem()
    part3_clean_fix()
    part4_verdict()


if __name__ == "__main__":
    main()
