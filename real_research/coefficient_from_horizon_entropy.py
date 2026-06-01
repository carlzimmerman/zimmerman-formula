#!/usr/bin/env python3
"""
FRONT 1 (rigorous): can horizon entropy DERIVE the coefficient, or only bracket it?
===================================================================================

The one posited number is the coefficient a0/cH = 1/Z = 1/sqrt(32pi/3) = 0.173.
This carries the holographic/entropic derivations through to see what they actually
give -- honestly, including the negative result.

Findings:
  (1) [EXACT] Bare holographic equipartition gives NEWTON, not MOND, with no a0.
      Mc^2 = (1/2) N kB T,  N = A/lp^2 (bits),  T = hbar a/(2pi c kB) (Unruh)
      => a = GM/r^2.  So a0 is NOT in pure area-law holography.
  (2) MOND requires a VOLUME/density law: a0 ~ sqrt(G rho_cosmic) ~ cH. Both the
      free-fall reading (-> 1/Z) and Verlinde's de Sitter volume entropy (-> 1/6)
      are this same physics; they are NOT competing theories.
  (3) [KEY] The coefficient factorizes as a0/cH = 1/(2n):
        * the '2' is the escape-velocity / elastic-energy factor (robust);
        * n ~ 3 is either the integer spatial DIMENSION (entropy: n=3 -> 1/6) or
          the free-fall density factor sqrt(8pi/3)=2.894 (geometry -> 1/Z).
      Horizon entropy gives n=3 (a0=cH/6), NOT n=sqrt(8pi/3). The geometric Z is a
      3.5% deviation that swaps the integer dimension for a free-fall convention.
  (4) Observation cannot decide: a0/cH0 is H0-hostage and brackets 1/2pi, 1/6, 1/Z.

Honest verdict: horizon entropy does NOT derive 1/sqrt(32pi/3); it derives ~1/6
(volume entropy, d=3), which is arguably the MORE principled value. The geometric Z
is a near-miss. The falsifiable prediction a0(z) prop E(z) is coefficient-INDEPENDENT
and is untouched by this.

Run:  python real_research/coefficient_from_horizon_entropy.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)
N3 = math.sqrt(8 * math.pi / 3)   # the free-fall "n" = 2.894...


def main():
    print("=" * 76)
    print("(1) [EXACT] bare holographic equipartition -> Newton, no a0")
    print("=" * 76)
    M, r = 2e30, 1e20
    lp2 = HBAR * G / c ** 3
    N = 4 * math.pi * r ** 2 / lp2                 # area-law bit count
    a = (M * c ** 2) / (0.5 * N * HBAR / (2 * math.pi * c))
    print("   Mc^2 = (1/2) N kB T,  N = A/lp^2,  T = hbar a/(2pi c kB)")
    print(f"   => a = {a:.4e},  GM/r^2 = {G*M/r**2:.4e},  ratio = {a/(G*M/r**2):.6f}")
    print("   Pure AREA-law holography reproduces Newton exactly and contains NO a0.")
    print("   So the MOND scale cannot come from area-law counting alone.\n")

    print("=" * 76)
    print("(2) MOND needs a VOLUME/density law -- and it is one family")
    print("=" * 76)
    print("   a0 = (c/2) sqrt(G rho_cosmic) ~ cH  is a VOLUME (density) relation.")
    print("   * free-fall reading: a0 = c^2/2R, R = c/sqrt(G rho)  -> coefficient 1/Z")
    print("   * Verlinde (2016): baryons displace the de Sitter VOLUME entropy; the")
    print("     elastic strain gives apparent dark matter, deep-MOND a0 ~ cH/6.")
    print("   These are the SAME physics (a0 set by cosmic density), not rivals.\n")

    print("=" * 76)
    print("(3) [KEY] the coefficient factorizes:  a0/cH = 1/(2n)")
    print("=" * 76)
    print(f"   {'approach':<40}{'n':>10}{'1/(2n)':>10}")
    rows = [
        ("Schwarzschild / escape (Hubble scale)", 1.0),
        ("Gibbons-Hawking temperature (1/2pi)", math.pi),
        ("Verlinde de Sitter volume entropy (d=3)", 3.0),
        ("geometric free-fall (dynamical time)", N3),
    ]
    for name, n in rows:
        tag = "  <- 1/Z" if abs(1/(2*n) - 1/Z) < 1e-6 else ("  <- 1/6" if abs(1/(2*n)-1/6)<1e-6 else "")
        print(f"   {name:<40}{n:>10.4f}{1/(2*n):>10.4f}{tag}")
    print()
    print(f"   The '2' is the escape-velocity/elastic factor -- shared by all routes.")
    print(f"   The difference is ENTIRELY in n ~ 3:")
    print(f"     entropy / dimension : n = 3        -> a0 = cH/6   = {1/6:.4f} cH")
    print(f"     geometric free-fall : n = {N3:.3f}    -> a0 = cH/Z   = {1/Z:.4f} cH")
    print(f"     they differ by {(3-N3)/3*100:.1f}% -- the integer dimension 3 vs sqrt(8pi/3).")
    print("   => horizon entropy gives 1/6, NOT 1/sqrt(32pi/3). It does not derive Z.\n")

    print("=" * 76)
    print("(4) observation is H0-hostage and cannot pick among them")
    print("=" * 76)
    a0 = 1.2e-10
    print(f"   {'H0':>8}{'a0/cH0':>10}{'nearest':>14}")
    for H0 in (67.4, 70.0, 73.0):
        coeff = a0 / (c * H0 * 1e3 / MPC)
        near = min([("1/Z", 1/Z), ("1/6", 1/6), ("1/2pi", 1/(2*math.pi))],
                   key=lambda t: abs(t[1] - coeff))[0]
        print(f"   {H0:>8.1f}{coeff:>10.4f}{near:>14}")
    print("   The H0 tension alone moves a0/cH0 across all three candidates. To decide")
    print("   the 3.5% fork needs sigma(a0)/a0 < ~1.8%; today it is ~20% systematic.\n")

    print("=" * 76)
    print("VERDICT (rigorous, including the negative part)")
    print("=" * 76)
    print("  * Pure area-law holography = Newton, no a0 (exact). The MOND scale needs a")
    print("    VOLUME/density law -- a0 ~ sqrt(G rho) ~ cH -- shared by the free-fall and")
    print("    Verlinde-entropy readings.")
    print("  * The coefficient is 1/(2n), n~3. Horizon entropy fixes n = 3 (a0=cH/6, the")
    print("    integer dimension); the geometric value uses n = sqrt(8pi/3)=2.894 (a0=cH/Z).")
    print("    So entropy does NOT derive 1/sqrt(32pi/3) -- it derives 1/6, and the")
    print("    geometric Z is a 3.5% near-miss using a free-fall convention instead of d=3.")
    print("  * Honestly, 1/6 (integer dimension, emergent gravity) is the MORE principled")
    print("    value; 'Z = sqrt(32pi/3) = cube x sphere' looks like geometric dressing.")
    print("  * BUT the data cannot choose (H0-hostage), and -- crucially -- the falsifiable")
    print("    prediction a0(z)/a0(0)=E(z) is coefficient-INDEPENDENT. So this weakens the")
    print("    specific number Z, not the surviving physics. The coefficient stays the one")
    print("    open posit, now located precisely as 1/(2n) with n between 2.89 and 3.14.")


if __name__ == "__main__":
    main()
