#!/usr/bin/env python3
"""
The coefficient endgame: actually carry out the entropy derivations of MOND.
===========================================================================

Not cite Verlinde -- DO the equipartition/entropy derivations and see what they
give. Findings:

  (A) E = (1/2)N kB (T_a - T_dS)  [excess over de Sitter floor] -> a = g_N + cH.
      NOT MOND. Fails.
  (B) E = (1/2)N kB T(a),  T(a) = (hbar/2pi c kB) sqrt(a^2 + c^2 H^2) [Deser-Levin]
      -> a = sqrt(g_N^2 - (cH)^2). NOT MOND (and imaginary for g_N<cH). Fails.

So NAIVE equipartition does not produce MOND -- the coefficient is not cheap. The
only entropy route that yields a MOND law is Verlinde's elastic VOLUME entropy,
which gives a coefficient ~1/6 (the d=3 factor) -- and is contested.

Then the punchline: the entropy answer (~1/6) and the framework's geometric value
(1/sqrt(32pi/3)) are DIFFERENT NUMBERS, 3.6% apart -- a concrete, in-principle
measurable fork, not an abstract mystery.

Pure stdlib. Run:  python reviews/entropy_coefficient_rigorous_endgame.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
H0 = 71.5e3 / MPC
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)
cH0 = C * H0


def main():
    print("=" * 78)
    print("(A) Equipartition with the de Sitter temperature FLOOR -- carried through")
    print("=" * 78)
    print("   Standard entropic gravity: E = (1/2) N kB T_a, N = 4pi r^2/lp^2,")
    print("   T_a = hbar a/(2pi c kB), E = Mc^2  =>  a = GM/r^2 (Newton). To get MOND")
    print("   try the EXCESS over the de Sitter floor T_dS = hbar H/(2pi kB):")
    print("     Mc^2 = (1/2)N kB (T_a - T_dS) = (r^2 c^2/G)(a - cH)/c ... carry it:")
    print("     => a = GM/r^2 + cH = g_N + cH.")
    print("   RESULT: a = g_N + cH. A constant offset, NOT the MOND sqrt law. FAILS.\n")

    print("=" * 78)
    print("(B) Equipartition with the full Deser-Levin temperature -- carried through")
    print("=" * 78)
    print("   Accelerated observer in de Sitter: T(a) = (hbar/2pi c kB) sqrt(a^2+c^2H^2).")
    print("   E = (1/2)N kB T(a) = Mc^2:")
    print("     (r^2 c^2/G) sqrt(a^2+c^2H^2) = Mc^2  =>  sqrt(a^2+c^2H^2) = GM/r^2 = g_N")
    print("     => a = sqrt(g_N^2 - (cH)^2).")
    print("   RESULT: a = sqrt(g_N^2-(cH)^2). Imaginary for g_N<cH; ->g_N for g_N>>cH.")
    print("   NOT the MOND law (deep-MOND needs a -> sqrt(g_N a0), rising as sqrt g_N). FAILS.\n")

    print("=" * 78)
    print("(C) Verdict on the naive routes, and what actually works")
    print("=" * 78)
    print("   Both clean equipartition routes FAIL to give MOND. The coefficient is not")
    print("   cheap -- you cannot get the deep-MOND sqrt law from a temperature floor on")
    print("   the holographic screen. The ONLY entropy mechanism that yields a MOND law")
    print("   is Verlinde's: the dark energy carries a VOLUME-law entropy; a baryonic")
    print("   mass elastically DISPLACES it; the strain response gives an extra inward")
    print("   acceleration g_D = sqrt(g_N a_M). The d=3 strain integral fixes a_M ~ cH/6.")
    print("   (And even this is contested -- the 'Inconsistencies' analysis argues the")
    print("    elastic step, done carefully, recovers Newton.) So: hard, and not clean.\n")

    print("=" * 78)
    print("(D) THE PUNCHLINE -- entropy vs geometry is a CONCRETE 3.6% fork")
    print("=" * 78)
    a_verlinde = cH0 / 6
    a_geom = cH0 / Z
    a_gh = cH0 / (2 * math.pi)
    print(f"   {'value':<34}{'a0/cH':>9}{'a0 [m/s^2]':>13}")
    print(f"   {'emergent gravity (Verlinde 1/6)':<34}{1/6:>9.4f}{a_verlinde:>13.3e}")
    print(f"   {'Gibbons-Hawking (1/2pi)':<34}{1/(2*math.pi):>9.4f}{a_gh:>13.3e}")
    print(f"   {'FRAMEWORK geometric 1/sqrt(32pi/3)':<34}{1/Z:>9.4f}{a_geom:>13.3e}")
    print(f"   {'observed (central)':<34}{A0/cH0:>9.4f}{A0:>13.3e}")
    print()
    d_gv = abs(a_geom - a_verlinde) / a_verlinde * 100
    print(f"   geometric vs emergent-gravity: differ by {d_gv:.1f}%.")
    print(f"   => these are DIFFERENT THEORIES predicting DIFFERENT a0. The 'whole game'")
    print(f"      is not an abstract mystery -- it is a {d_gv:.1f}% difference between a")
    print("      GEOMETRIC value (cube x sphere) and an EMERGENT-GRAVITY value (d=3 entropy),")
    print("      and in principle a precise a0 measurement decides which nature uses.")
    print()
    # required precision to separate at 2 sigma
    sep = d_gv / 100
    print(f"   To distinguish at 2 sigma needs sigma(a0)/a0 < {sep/2*100:.1f}%.")
    print("   HARD: a0's error is ~20% SYSTEMATIC (stellar M/L, distance ladder), not")
    print("   statistical. Beating it to ~2% requires controlling the M/L systematic --")
    print("   the real obstacle. So the fork is sharp but currently below the systematic.\n")

    print("=" * 78)
    print("VERDICT -- the rigorous endgame, honestly")
    print("=" * 78)
    print("  * Naive entropy equipartition does NOT give MOND (routes A,B fail explicitly).")
    print("  * The one entropy mechanism that does (Verlinde elastic volume entropy) gives")
    print("    a0 ~ cH/6 -- NOT the framework's geometric cH/sqrt(32pi/3). They differ by")
    print(f"    {d_gv:.1f}%. The rigorous emergent-gravity prediction is a0 slightly BELOW")
    print("    the geometric value.")
    print("  * So 'is the coefficient geometric or emergent-gravitational?' is, in")
    print("    principle, an EMPIRICAL question -- a 3.6% fork -- not undecidable mysticism.")
    print("    It is currently hidden by a0's 20% M/L systematic; controlling that to ~2%")
    print("    is the concrete (hard) experiment that would settle the deepest open number.")
    print("  * Honest: I did not derive 1/sqrt(32pi/3). The rigorous calc gives ~1/6, and")
    print("    the geometric value is a near-miss of it. The whole game reduces to one")
    print("    systematic-limited measurement -- which is the most honest 'answer' there is.")


if __name__ == "__main__":
    main()
