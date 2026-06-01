#!/usr/bin/env python3
"""
FRONT 1 (rigorous, with a self-correction): is the coefficient DERIVED by anyone?
=================================================================================

The one posited number is the coefficient a0/cH = 1/Z = 1/sqrt(32pi/3) = 0.173.
This carries the holographic/entropic arguments through honestly -- INCLUDING a
correction to an earlier overclaim of mine (flagged below).

Findings:
  (1) [SOLID] Bare area-law holographic equipartition gives NEWTON, not MOND, with
      no a0.  Mc^2 = (1/2) N kB T, N = A/lp^2, T = hbar a/(2pi c kB) => a = GM/r^2.
      So a0 is NOT in pure area-law holography; MOND needs an EXTRA ingredient.
  (2) [SOLID] That extra ingredient is a VOLUME/density law: a0 ~ sqrt(G rho)~cH.
      Both the free-fall reading and Verlinde's de Sitter volume entropy are of this
      kind. Verlinde's emergent gravity yields an effective a0 ~ cH0/6 ~ 1.1e-10
      (literature value, matches Milgrom) -- but his mechanism is CONTESTED (a
      published Comment, arXiv:1909.01734; failure for dwarf spheroidals, 1612.06282).
  (3) [SUGGESTIVE, NOT DERIVED] Numerically BOTH values can be written a0/cH=1/(2n)
      with n~3: free-fall n=sqrt(8pi/3)=2.894 (-> 1/Z, by construction) and Verlinde
      ~1/6 (n=3). CAUTION: reading "n=3 = the integer dimension" for Verlinde is a
      parametrization I IMPOSED -- his 1/6 comes from a strain integral that does not
      transparently factor as 2 x dimension. So this is a coincidental near-equality
      (3.5%), NOT a demonstration that entropy "derives" a cleaner number.
  (4) [SOLID] Observation cannot decide: a0/cH0 is H0-hostage and brackets 1/2pi,
      1/6, 1/Z.

Honest verdict (corrected): NO uncontested first-principles route pins the
coefficient. Verlinde's CONTESTED mechanism gives ~cH/6; the geometric reading gives
cH/Z by construction; the two agree to 3.5% and the data cannot separate them. I do
NOT claim entropy "derives" 1/6, nor that 1/6 is preferred over Z -- that earlier
claim over-credited a disputed derivation. The coefficient remains the single
unpinned posit. The falsifiable prediction a0(z) prop E(z) is coefficient-INDEPENDENT
and untouched either way.

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
    print("(3) [SUGGESTIVE, NOT DERIVED] a 3.5% near-equality -- with a caution")
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
    print(f"   Both values can be WRITTEN as 1/(2n) with n~3 -- but note the caution:")
    print(f"     geometric free-fall : n = {N3:.3f} = sqrt(8pi/3)  -> 1/Z  (by construction)")
    print(f"     Verlinde (contested): a0 ~ cH/6, i.e. n = 3       -> 1/6  (NOT a 2 x dim)")
    print(f"     they agree to {(3-N3)/3*100:.1f}% -- a NEAR-EQUALITY of two O(1) numbers from")
    print( "     different, individually-unsettled arguments. Reading 'n=3 = dimension' for")
    print( "     Verlinde is a parametrization I IMPOSED, not his strain derivation. So this")
    print( "     does NOT show entropy 'derives' a cleaner value than Z.\n")

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
    print("VERDICT (corrected -- I walked back an earlier overclaim)")
    print("=" * 76)
    print("  * SOLID: pure area-law holography = Newton, no a0. MOND needs an extra")
    print("    VOLUME/density ingredient -- a0 ~ sqrt(G rho) ~ cH.")
    print("  * NO uncontested first-principles route pins the coefficient. Verlinde's")
    print("    CONTESTED emergent gravity gives ~cH/6 (~1.1e-10); the geometric reading")
    print("    gives cH/Z by construction. The two agree to 3.5%.")
    print("  * I do NOT claim entropy 'derives' 1/6, nor that 1/6 beats Z. That earlier")
    print("    claim over-credited a disputed mechanism and used a factorization I imposed.")
    print("    Neither value is established; the data is H0-hostage and cannot choose.")
    print("  * The coefficient stays the single unpinned posit. The falsifiable prediction")
    print("    a0(z)/a0(0)=E(z) is coefficient-INDEPENDENT and untouched either way.")


if __name__ == "__main__":
    main()
