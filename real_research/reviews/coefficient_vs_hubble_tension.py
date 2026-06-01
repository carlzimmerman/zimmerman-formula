#!/usr/bin/env python3
"""
Why the coefficient fork is hostage to the Hubble tension -- and why the
EVOLUTION escapes it.
=======================================================================

The coefficient fork is geometric 1/sqrt(32pi/3)=0.173 vs emergent-gravity
1/6=0.167 -- a 3.6% difference. To measure it you compare a0 (from galaxies) to
cH0. But a0/cH0 depends on H0, and H0 is DISPUTED by ~9% (the Hubble tension). So:

  * the H0 tension makes a0/cH0 range over ~0.169-0.183 -- which SPANS and EXCEEDS
    the 3.6% geometric-vs-emergent fork. The fork is currently SWAMPED by H0.
  * the coefficient is doubly hostage: the a0 M/L systematic (~20%) AND the H0
    tension (~9%). Both must reach ~2% to settle it.
  * the EVOLUTION a0(z)/a0(0) = E(z) is a RATIO: H0 cancels AND Z cancels. It
    escapes both obstacles -- which is exactly why it is the clean falsifiable test.

Pure stdlib. Run:  python reviews/coefficient_vs_hubble_tension.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
A0 = 1.20e-10                    # measured a0 (from galaxies w/ independent distances)
Z = 2 * math.sqrt(8 * math.pi / 3)
OM, OL = 0.315, 0.685


def cH0(H0):
    return C * (H0 * 1e3 / MPC)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def main():
    print("=" * 78)
    print("(1) The coefficient a0/cH0 depends on H0 -- and H0 is in tension")
    print("=" * 78)
    print("   a0 is measured from galaxies (v_flat, baryonic mass via direct distances);")
    print("   it does NOT depend on H0. But cH0 does. So a0/cH0 ~ 1/H0.")
    print()
    print(f"   {'H0 source':<16}{'H0':>6}{'cH0':>11}{'a0/cH0':>9}{'= 1/(...)':>10}")
    for H0, src in [(67.4, "Planck"), (71.5, "framework"), (73.0, "SH0ES")]:
        ch = cH0(H0)
        coeff = A0 / ch
        print(f"   {src:<16}{H0:>6.1f}{ch:>11.3e}{coeff:>9.4f}{1/coeff:>10.3f}")
    print()
    coeff_planck = A0 / cH0(67.4)
    coeff_shoes = A0 / cH0(73.0)
    print(f"   So a0/cH0 ranges {coeff_shoes:.4f} (SH0ES) to {coeff_planck:.4f} (Planck)")
    print(f"   -- a spread of {(coeff_planck/coeff_shoes-1)*100:.1f}% from the H0 tension alone.\n")

    print("=" * 78)
    print("(2) That H0 spread SWAMPS the geometric-vs-emergent fork")
    print("=" * 78)
    geom = 1 / Z
    emerg = 1 / 6
    print(f"   the fork:  geometric 1/sqrt(32pi/3) = {geom:.4f}")
    print(f"              emergent  1/6            = {emerg:.4f}   (differ {abs(geom-emerg)/emerg*100:.1f}%)")
    print(f"   the H0-induced range of a0/cH0: {coeff_shoes:.4f} - {coeff_planck:.4f} "
          f"({(coeff_planck/coeff_shoes-1)*100:.0f}% wide)")
    print("   The H0 range is WIDER than the fork and brackets it:")
    print(f"     with SH0ES H0=73:  a0/cH0={coeff_shoes:.4f} -- nearer the EMERGENT value")
    print(f"     with Planck H0=67.4: a0/cH0={coeff_planck:.4f} -- ABOVE the geometric value")
    print("   => you literally cannot say which side of the fork you are on until the")
    print("      Hubble tension is resolved. The deepest open number is hostage to H0.\n")

    print("=" * 78)
    print("(3) The two obstacles, and the precision each needs")
    print("=" * 78)
    print("   To settle the 3.6% fork at 2 sigma you need a0/cH0 to ~1.8%. That requires:")
    print("    OBSTACLE 1 -- a0 M/L systematic (~20%): beat it with GAS-DOMINATED")
    print("       galaxies (baryonic mass = HI gas, measured from 21cm flux, no stellar")
    print("       M/L). WALLABY delivers exactly these. Random distance scatter averages")
    print("       down as 1/sqrt(N) -> a few-% a0 from a large gas-rich sample is feasible.")
    print("    OBSTACLE 2 -- the Hubble tension (~9% in H0): cH0 ~ H0, so a0/cH0 ~ 1/H0.")
    print("       Until H0 is pinned to ~2%, the fork stays buried. This one is NOT in")
    print("       the framework's control -- it rides on the broader H0 resolution.\n")

    print("=" * 78)
    print("(4) The escape: the EVOLUTION is a RATIO -- H0-free AND Z-free")
    print("=" * 78)
    print("   a0(z)/a0(0) = H(z)/H0 = E(z) = sqrt(Om(1+z)^3 + OL).")
    print("   H0 CANCELS (it is a ratio). Z CANCELS (it is a ratio). So the evolution")
    print("   depends only on Om (known to ~1%) -- NOT on the coefficient, NOT on H0.")
    print(f"   {'z':>5}{'E(z) [H0-free, Z-free]':>26}")
    for z in (1, 6, 10, 14):
        print(f"   {z:>5}{E(z):>26.3f}")
    print("   => the evolution escapes BOTH obstacles. That is precisely why it is the")
    print("      clean, robust, falsifiable test -- and the coefficient is not.\n")

    print("=" * 78)
    print("VERDICT -- the program's honest strategy falls out of this")
    print("=" * 78)
    print("  * The COEFFICIENT (geometric vs emergent, 3.6%) is doubly hostage: to the")
    print("    a0 M/L systematic (~20%, beatable with WALLABY gas-rich systems) AND to")
    print("    the HUBBLE TENSION (~9% in H0, not the framework's to fix). It cannot be")
    print("    settled until both reach ~2%. Today the H0 tension alone buries the fork.")
    print("  * The EVOLUTION (a0(z)~E(z)) is a ratio -- H0-free and Z-free -- so it is")
    print("    immune to both, and testable NOW (JWST z>10 deep-MOND systems).")
    print("  * STRATEGY (clean and honest): TEST THE EVOLUTION now (the robust claim);")
    print("    SETTLE THE COEFFICIENT later, after the Hubble tension resolves and gas-")
    print("    dominated a0 reaches ~2%. Do not stake the framework on the coefficient --")
    print("    it is entangled with cosmology's own biggest open problem. Stake it on the")
    print("    evolution, which stands alone.")


if __name__ == "__main__":
    main()
