#!/usr/bin/env python3
"""
Turning the blade on the survivor: is a0 CONSTANT (the cosmological constant) or
EVOLVING (cH(z)/Z)? The framework claims both -- only one can be the prediction.
=============================================================================

I have been calling a0(z) = cH(z)/Z "the legitimate finding." Honesty demands the
same skeptical pressure I put on the numerology. The TOE doc lists THREE unifying
identities for a0:
   (1) surface gravity:  a0 = (c/2) sqrt(G rho)         [free-fall clock]
   (2) cosmological const: a0 = (c^2/2) sqrt(Lambda/8pi) [dark energy]
   (3) horizon temperature: a0 from apparent-horizon c^2/R_A
But (1) and (3), using the TOTAL density / apparent horizon, give a0 ~ H(z) --
EVOLVING. (2), read literally as "a0 = sqrt(Lambda)", gives a0 = CONSTANT. These
agree only TODAY. They make OPPOSITE predictions for z>0. So which is the claim?

This script proves: a0 = (c/2)sqrt(G rho_total) is ALGEBRAICALLY identical to
cH(z)/Z, so identities (1) and (3) ARE the evolving law; the Lambda identity (2)
is just that law evaluated at the de Sitter FLOOR (rho_total -> rho_Lambda). So
there is no contradiction -- BUT the catchy "a0 IS dark energy" must be read as
"a0 FLOORS at dark energy," not "a0 is constant." The only distinctive, testable
content of the whole survivor is the EVOLUTION a0 ~ H(z), resting on ONE pillar
(total-density / horizon), with the standard MOND constant-a0 as the null to beat.

Pure stdlib. Run:  python reviews/a0_constant_vs_evolving_fork.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
H0 = 67.4e3 / MPC
OM, OL = 0.315, 0.685
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def main():
    print("=" * 78)
    print("(1) The algebra: a0 = (c/2)sqrt(G rho_total) IS cH(z)/Z")
    print("=" * 78)
    print("   Friedmann: H^2 = (8piG/3) rho_total  =>  sqrt(G rho_total) = sqrt(3/8pi) H")
    print("   so  a0 = (c/2) sqrt(G rho_total) = (c/2) sqrt(3/8pi) H = cH / (2 sqrt(8pi/3))")
    print("         = cH / Z.   [identity (1) with TOTAL density = the evolving law]")
    lhs = (C / 2) * math.sqrt(3 / (8 * math.pi))
    rhs = C / Z
    print(f"   check: (c/2)sqrt(3/8pi) = {lhs:.6e},  c/Z = {rhs:.6e}  -> equal\n")

    print("=" * 78)
    print("(2) The Lambda identity is the FLOOR of that same law, not a constant")
    print("=" * 78)
    H_Lambda = H0 * math.sqrt(OL)              # de Sitter rate (far future)
    a0_today = C * H0 / Z
    a0_floor = C * H_Lambda / Z
    print("   far future: rho_total -> rho_Lambda, H -> H_Lambda = H0 sqrt(OL).")
    print(f"   a0_floor = c H_Lambda / Z = a0(0) * sqrt(OL) = a0(0) * {math.sqrt(OL):.3f}")
    print(f"     a0(0)   = cH0/Z        = {a0_today:.3e} m/s^2")
    print(f"     a0_floor= cH_Lambda/Z  = {a0_floor:.3e} m/s^2   (= the 'a0 = Lambda' value)")
    print(f"   So 'a0 IS the cosmological constant' = a0 at its de Sitter FLOOR, which is")
    print(f"   already {(1-math.sqrt(OL))*100:.0f}% BELOW today's a0. Read literally as 'a0 = const =")
    print("   sqrt(Lambda)', it would NEGATE the evolution. The identity is a floor, not")
    print("   the prediction.\n")

    print("=" * 78)
    print("(3) The three candidate laws -- they agree today, diverge in the past")
    print("=" * 78)
    print(f"   {'z':>5}{'CONST (std MOND)':>18}{'CONST (Lambda flr)':>20}{'EVOLVING cH(z)/Z':>20}")
    for z in (0, 0.5, 1, 2, 4, 6, 10):
        const_mond = 1.0
        const_lam = math.sqrt(OL)
        evolving = E(z)
        print(f"   {z:>5.1f}{const_mond:>18.2f}{const_lam:>20.2f}{evolving:>20.2f}")
    print("   (all in units of a0(0).) Standard MOND and the literal-Lambda reading are")
    print("   FLAT; only cH(z)/Z climbs. By z=2 it is 3x; by z=10, 20x. THAT gap is the")
    print("   entire distinctive, falsifiable content of the survivor.\n")

    print("=" * 78)
    print("(4) The observational lever -- and what existing data can/can't say")
    print("=" * 78)
    print("   Deep-MOND BTFR: v_flat^4 = G M_b a0(z)  =>  at fixed M_b, v_flat ~ a0^(1/4)")
    print(f"   {'z':>5}{'a0(z)/a0(0)':>14}{'v_flat shift = E^(1/4)':>24}")
    for z in (0.5, 1, 2, 4):
        print(f"   {z:>5.1f}{E(z):>14.2f}{E(z)**0.25:>24.3f}")
    print("   => a clean ~16% (z=1) to ~32% (z=2) UPWARD shift of the BTFR zero-point,")
    print("      for the SAME baryonic mass. Standard MOND predicts ZERO shift.")
    print()
    print("   WHAT BEARS ON IT:")
    print("    * CLEAN test: deep-MOND (low-acceleration, g < a0) rotators at z>1 --")
    print("      LSB dwarfs, outer HI disks. The BTFR zero-point vs z is the observable.")
    print("    * NOT a clean test: high-z MASSIVE compact disks (Genzel+ 2017-type,")
    print("      baryon-dominated, declining RCs). They sit at g > a0 even with a0 tripled")
    print("      -> Newtonian regime -> no MOND boost regardless of a0(z). Their 'low DM'")
    print("      neither confirms nor refutes the evolution. (Easy to misread as a test.)")
    print("    * The z=0 anchor (SPARC a0 = 1.2e-10) is solid; the high-z deep-MOND")
    print("      points are not yet measured -- which is why this is a PREDICTION.\n")

    print("=" * 78)
    print("VERDICT -- the survivor, audited honestly")
    print("=" * 78)
    print("  * NO internal contradiction: identities (1) free-fall and (3) horizon, using")
    print("    the TOTAL density, are algebraically the evolving law cH(z)/Z; identity (2)")
    print("    Lambda is its de Sitter floor. They are one statement at z=0.")
    print("  * BUT the only DISTINCTIVE, testable content is the EVOLUTION a0 ~ H(z). The")
    print("    'a0 = cosmological constant' line, read as constant a0, would kill it -- so")
    print("    it must be stated as 'a0 floors at dark energy; today it is ~21% above that")
    print("    floor and climbs into the past.' The three-identities story is a z=0 snapshot,")
    print("    not three independent confirmations of the evolution.")
    print("  * The prediction therefore rests on a SINGLE pillar (total-density/horizon),")
    print("    its coefficient 1/Z is hostage to H0, and its distinctive regime (deep-MOND,")
    print("    z>1) is UNMEASURED. It is the best surviving piece -- and still just a clean,")
    print("    unconfirmed prediction with standard constant-a0 MOND as the null to beat.")
    print("    Honest status: promising, falsifiable, not yet evidence.")


if __name__ == "__main__":
    main()
