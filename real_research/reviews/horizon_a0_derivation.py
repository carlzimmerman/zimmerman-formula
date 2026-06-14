#!/usr/bin/env python3
"""
Architecture C: derive a0 = cH/Z from de Sitter horizon thermodynamics?
=======================================================================

This is the one route that dodges BOTH the heavy-vs-light tension and the
varying-constants bound (radion stays frozen; the evolving scale comes from the
horizon, not a rolling field). The challenge: derive a0 = cH/Z with Z =
2 sqrt(8pi/3) = 5.789 from horizon thermodynamics, with 1/Z as the geometric
coupling.

This script works the standard horizon-thermo routes and reports, with numbers,
EXACTLY how far the derivation gets:

  * the EVOLUTION a0(z) ~ H(z) is FORCED by any horizon mechanism      [DERIVED]
  * the ORDER OF MAGNITUDE a0 ~ cH is robust across routes             [DERIVED]
  * the SPECIFIC factor Z = 2 sqrt(8pi/3) is NOT uniquely forced: the
    sqrt(8pi/3) is just Friedmann (definitional), and the residual O(1)
    differs by route (1/2, 1, 2, 2pi, 6 ...). Z is the BEST-FIT member
    of that family, not a forced output.                              [FIT]

So C half-closes: scaling + magnitude yes, exact O(1) no. That is the honest
verdict, and it is also exactly what the framework's own a0_cH0_Z_check.py
admits ("assembles the factor 2 from horizon thermodynamics by hand").

Pure stdlib. Run:  python reviews/horizon_a0_derivation.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
G = 6.674e-11
H0 = 71.5 * 1e3 / MPC          # 1/s
OM, OL = 0.315, 0.685
A0_OBS = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)     # 5.78881
cH0 = C * H0


def Efunc(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def part1_evolution_forced():
    print("=" * 80)
    print("(1) The EVOLUTION a0(z) ~ H(z) is FORCED by any horizon mechanism [DERIVED]")
    print("=" * 80)
    print("   Premise of architecture C: a0 is set by the INSTANTANEOUS de Sitter")
    print("   horizon -- its temperature T_dS = hbar H(z)/(2pi k_B), equivalently the")
    print("   horizon acceleration c H(z). Whatever the O(1), a0(z) = (O1) * c H(z).")
    print("   Therefore a0(z)/a0(0) = H(z)/H0 = E(z), INDEPENDENT of the O(1) and of Z.")
    print()
    print(f"   {'z':>4} {'E(z)':>7} {'a0(z)/a0(0) (any route)':>26}")
    for z in (0, 1, 3, 6, 10, 14):
        print(f"   {z:>4} {Efunc(z):>7.2f} {Efunc(z):>26.2f}")
    print("   => the falsifiable, distinctive prediction is DERIVED here and needs no")
    print("      O(1): the horizon ties a0 to H(z). This is the robust half. ✓\n")


def part2_order_of_magnitude():
    print("=" * 80)
    print("(2) a0 ~ cH across standard routes -- but the O(1) is route-dependent [FIT]")
    print("=" * 80)
    print(f"   cH0 = {cH0:.3e} m/s^2 ;  observed a0 = {A0_OBS:.3e} ;  cH0/a0 = "
          f"{cH0/A0_OBS:.3f} (= Z)")
    print()
    # each standard derivation gives a0 = (factor) * cH0; record the factor
    routes = [
        ("Unruh = de Sitter crossover  T_U(a0)=T_dS",      1.0,
         "a0/c = H  ->  a0 = cH"),
        ("Milgrom vacuum (modified inertia)",              2.0,
         "deep limit a = sqrt(2cH a_N) -> a0 = 2cH"),
        ("Surface gravity of critical mass at R_H",        0.5,
         "g = GM_c/R_H^2 = cH/2"),
        ("Verlinde elastic / volume entropy (approx)",     1.0/6,
         "apparent-DM volume law -> a0 ~ cH/6"),
        ("a0 = cH/2pi  (Milgrom's 1983 estimate)",         1.0/(2*math.pi),
         "T-formula 2pi -> a0 = cH/2pi"),
        ("FRAMEWORK  a0 = cH/Z, Z=2sqrt(8pi/3)",           1.0/Z,
         "the best-fit member"),
    ]
    print(f"   {'route':<46}{'a0/cH0':>9}{'a0 [m/s^2]':>13}{'vs obs':>9}")
    for name, fac, _ in routes:
        a0 = fac * cH0
        print(f"   {name:<46}{fac:>9.3f}{a0:>13.2e}{a0/A0_OBS:>8.1f}x")
    print()
    print("   Reading: every route gives a0 ~ cH (within ~an order of magnitude), so")
    print("   the SCALE is robust. But the O(1) ranges over {1/6, 1/2pi, 1/2, 1, 2}")
    print("   depending on which thermodynamic assumption you make. The observed a0")
    print("   favors the LARGER divisors (~6): the framework's Z=5.79 is in that")
    print("   family and is the best fit -- but it is SELECTED, not forced. \n")


def part3_decompose_Z():
    print("=" * 80)
    print("(3) What is actually free? Decompose Z = 2 * sqrt(8pi/3)")
    print("=" * 80)
    rho_c0 = 3 * H0 ** 2 / (8 * math.pi * G)
    a0_from_rho = (C / 2) * math.sqrt(G * rho_c0)
    print(f"   a0 = cH0/Z = (c/2) sqrt(G rho_c)  (identity): "
          f"{cH0/Z:.3e} = {a0_from_rho:.3e} ✓")
    print(f"   sqrt(8pi/3) = {math.sqrt(8*math.pi/3):.4f}  <- this is JUST Friedmann:")
    print("       H = sqrt(8piG/3 rho_c), so cH = c sqrt(8pi/3) sqrt(G rho_c).")
    print("       Writing a0 in terms of rho_c instead of H AUTOMATICALLY produces")
    print("       sqrt(8pi/3). It carries no new physics -- it is a unit conversion.")
    print(f"   The factor 2  <- this is the ONLY genuinely-physical free O(1), the")
    print("       'horizon-thermodynamics factor'. Clean derivations give it as")
    print("       {1/2, 1, 2, 2pi, 6}; the framework sets it (with the sqrt) so that")
    print(f"       the total divisor is Z = {Z:.3f}.")
    print()
    print("   => 'Deriving Z' reduces ENTIRELY to deriving that one factor of 2 from")
    print("      first principles. No route here forces exactly that value. The")
    print("      framework's own a0_cH0_Z_check.py says the same: the factor 2 is")
    print("      'assembled by hand'. This part is FIT, and I will not pretend otherwise.\n")


def part4_geometric_conjecture():
    print("=" * 80)
    print("(4) Could the GEOMETRY pin the O(1)? The interlocking-web conjecture")
    print("=" * 80)
    print(f"   The framework's hope: the coupling Z = sqrt(compactification modulus),")
    print(f"   i.e. Z = sqrt(Z^2) with Z^2 = 32pi/3 = {32*math.pi/3:.4f} (the volume")
    print("   modulus of (T^2)^3/(Z2xZ2)). Then a0 = cH/sqrt(32pi/3) = cH/(2sqrt(8pi/3)).")
    print("   IF a horizon-thermo derivation produced a0 = cH / sqrt(V_modulus), and")
    print("   V_modulus = 32pi/3, the geometry WOULD pin the O(1).")
    print()
    print("   Honest status: that 'coupling = sqrt(volume modulus)' relation is a")
    print("   POSIT -- the central interlocking-web hypothesis -- not a derived")
    print("   holographic identity. It is exactly the link that has never been shown")
    print("   (six failed routes to derive 32pi/3 as a spectral invariant; it is the")
    print("   compactification INPUT). So this would CONVERT one unproven number")
    print("   (the O(1)) into another (the volume modulus). It is a hypothesis to test,")
    print("   not a closure. Stating it plainly is the honest move.\n")


def part5_tensions_dodged():
    print("=" * 80)
    print("(5) Does C actually dodge the two tensions? Yes -- that is its whole point")
    print("=" * 80)
    print("   * heavy-vs-light: the radion is STABILIZED (heavy, frozen) -- it fixes")
    print("     Z^2 and supplies the O(1) coupling. The EVOLUTION comes from H(z) (the")
    print("     background), not from a rolling light field. No ultralight modulus")
    print("     needed -> no heavy-vs-light tension. ✓")
    print("   * varying constants: a frozen radion means Z^2 (hence alpha, couplings)")
    print("     is CONSTANT. a0(z) varies only because H(z) varies. No alpha-dot. ✓")
    print("   Price: the radion sets the COUPLING, the horizon sets the DYNAMICS --")
    print("   so the radion is not literally 'the MOND field'. That is the trade.\n")


def main():
    part1_evolution_forced()
    part2_order_of_magnitude()
    part3_decompose_Z()
    part4_geometric_conjecture()
    part5_tensions_dodged()
    print("=" * 80)
    print("VERDICT -- how far the horizon derivation actually gets")
    print("=" * 80)
    print("  DERIVED (robust, route-independent):")
    print("   * a0(z) ~ H(z): the evolving, falsifiable prediction -- forced by tying")
    print("     a0 to the instantaneous horizon. This is the real win and it needs no Z.")
    print("   * a0 ~ cH: the order of magnitude, from multiple standard routes.")
    print()
    print("  NOT DERIVED (fit / conjecture):")
    print("   * the specific Z = 2 sqrt(8pi/3): the sqrt(8pi/3) is Friedmann (free), the")
    print("     residual factor 2 is the horizon O(1), which no clean route forces to")
    print("     this value. Z is the best-fit member of {1/2,1,2,2pi,6}-type family.")
    print("   * the geometric pin (coupling = sqrt(volume modulus)) is the unproven")
    print("     interlocking-web posit, not a holographic identity.")
    print()
    print("  NET: architecture C is the RIGHT home for evolving-a0 -- it derives the")
    print("  testable scaling and the order of magnitude while dodging both tensions.")
    print("  It does NOT derive the O(1) coupling Z; that remains a best fit (and the")
    print("  framework's own files admit it). The honest one-liner: 'the horizon makes")
    print("  a0 ~ cH(z) and forces a0(z) ~ E(z); the precise factor 1/Z is fit, and")
    print("  pinning it to the compactification volume is a conjecture to be tested.'")


if __name__ == "__main__":
    main()
