#!/usr/bin/env python3
"""
Pushing the factor-of-2 question to the bottom: Z is ONE dimensionless number.
=============================================================================

*** CORRECTION (2026-06-13) — COEFFICIENT FOOTING. This script writes "a0/cH = 1/Z = 0.173" using cH built
from rho_c (the CRITICAL/total density, see part 1), i.e. cH = cH0. That makes the quoted 0.173 a coefficient
against cH0 for the rho_TOTAL object a0 = (c/2)sqrt(G rho_c) = cH0/Z = 1.13e-10 -- NOT the framework's
canonical a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 (which uses rho_DE, giving a0/cH0 = 0.143 and a0/cH_Lambda
= 1/Z = 0.173 against cH_Lambda = 0.83*cH0). CONSEQUENCE for part 2: Verlinde 1/6 = 0.167 and Gibbons-Hawking
1/2pi = 0.159 are coefficients against cH0, so the apt comparison is the framework's vs-cH0 value 0.143 --
which is the LOW OUTLIER (below both), NOT "bracketed" by them. The "1/6 and 1/2pi bracket 0.173" statement
compares across different Hubble rates and overstates the agreement (the sqrt(OmL)=0.83 why-now factor is
doing the work). The structural point (a0/cH is one dimensionless number, G-independent, not horizon-derived)
STANDS. See real_research/THE_A0_COEFFICIENT_CONVENTION.md.

Last step left it as 'density base (c sqrt(G rho)) vs horizon base (cH), differing
by sqrt(8pi/3)'. Pushing further dissolves that choice and isolates exactly what
is irreducible.

KEY: a0/cH = 1/Z is DIMENSIONLESS. G, rho, c, H all cancel. So 'should a0 use cH
or c sqrt(G rho)?' is a NON-question -- they are the same cosmic scale written in
different units; the sqrt(8pi/3) is a unit conversion, not a missing factor. The
only irreducible content is the pure number 1/Z = 0.1727. This script shows that,
lists the candidate dimensionless O(1)s, and kills the obvious 'geometry enters
via G' route (G cancels).

Pure stdlib. Run:  python reviews/Z_is_one_pure_number.py
"""

import math

Z = 2 * math.sqrt(8 * math.pi / 3)          # 5.78881
INV_Z = 1 / Z                                # 0.17275  -- the dimensionless O(1)


def main():
    print("=" * 78)
    print("(1) a0/cH is a PURE NUMBER -- G, rho, c, H all cancel")
    print("=" * 78)
    print("   a0 = (c/2) sqrt(G rho_c) ;  cH = c sqrt(8piG rho_c/3).")
    print("   a0/cH = (1/2) sqrt(G rho_c) / sqrt(8piG rho_c/3)")
    print("         = (1/2) sqrt(3/8pi) = 1/(2 sqrt(8pi/3)) = 1/Z.")
    print(f"   a0/cH = 1/Z = {INV_Z:.5f}.  Everything dimensionful CANCELS.")
    print()
    print("   => 'density base vs horizon base' is a non-choice: c sqrt(G rho) and cH")
    print("      are the SAME cosmic scale in different units (ratio sqrt(8pi/3)). The")
    print("      sqrt(8pi/3) is a unit conversion, NOT a second physical factor to find.")
    print("      The 'clean 1/2 on the density base' is clean ONLY because density units")
    print("      hide the sqrt(8pi/3). The irreducible content is the pure number 0.173.\n")

    print("=" * 78)
    print("(2) The irreducible question: which dimensionless O(1) is 0.1727?")
    print("=" * 78)
    cands = [
        ("1/2     surface gravity (enclosed mass)", 0.5),
        ("1/6     Verlinde volume-entropy (approx)", 1/6),
        ("1/2pi   Gibbons-Hawking temperature",     1/(2*math.pi)),
        ("1/sqrt(32pi/3)  FRAMEWORK (geometric Z)", INV_Z),
    ]
    print(f"   {'candidate':<42}{'value':>9}{'a0/cH=?':>10}")
    for name, v in cands:
        flag = "  <- target 0.173" if abs(v-INV_Z) < 0.01 else (
               "  (way off)" if abs(v-INV_Z) > 0.2 else "")
        print(f"   {name:<42}{v:>9.4f}{'':>10}{flag}")
    print()
    print("   The surface-gravity 1/2 is way off (overshoots a0). The two emergent-")
    print("   gravity numbers -- 1/6 (Verlinde) and 1/2pi (Gibbons-Hawking) -- BRACKET")
    print("   0.173 but neither hits it; they are 3.5% and 8% off. Inside a0's ~20%")
    print("   systematic, the data CANNOT distinguish 1/6, 1/2pi, or the framework's")
    print("   geometric 0.173. So the O(1) is a best-fit among an O(1)-spread family.\n")

    print("=" * 78)
    print("(3) Kill the obvious 'geometry enters via Newton's G' route")
    print("=" * 78)
    print("   Tempting fix: let the compactification volume V=Z^2 set the 4D Newton")
    print("   constant, G_4 = G_higher / V, so a0 ~ sqrt(G_4) carries a 1/sqrt(V)=1/Z.")
    print("   PROBLEM: a0/cH is G-INDEPENDENT (part 1) -- G_4 appears in BOTH a0 and cH")
    print("   (via Friedmann) and CANCELS in the ratio. So changing G_4 does NOT change")
    print("   Z. The compactification volume cannot enter the O(1) through G. That route")
    print("   is closed. (Z is a pure number; only a dimensionless argument can fix it.)\n")

    print("=" * 78)
    print("VERDICT -- pushing hits bedrock: ONE pure number, not horizon-derivable")
    print("=" * 78)
    print("  * The factor-2 'progress' was partly a units illusion: density vs horizon")
    print("    base is the same scale, and the sqrt(8pi/3) is unit conversion, not a")
    print("    missing factor. There is no 'second factor' hiding -- there is ONE number.")
    print("  * That number, a0/cH = 0.1727, is dimensionless and cannot be set by G,")
    print("    rho, c, or H. The horizon gives dimensionless O(1)s of 1/2pi and ~1/6;")
    print("    the framework's 1/sqrt(32pi/3) sits between them, geometric, and the data")
    print("    cannot tell them apart.")
    print("  * The naive 'geometry via G' rescue fails (G cancels). So fixing 0.1727")
    print("    requires a genuine dimensionless counting -- a horizon entropy coefficient")
    print("    or a compactification index -- that no one has derived to this value.")
    print()
    print("  This is the honest bedrock of Gate 3: the whole O(1) mystery is ONE pure")
    print("  number ~0.17, the horizon brackets it (1/2pi..1/6) but does not pin it, and")
    print("  it is observationally indistinguishable from those. Your factor-2 instinct")
    print("  got the RIGHT half (the horizon sets the SCALE cH); the exact 0.173 is the")
    print("  irreducible dimensionless coefficient -- the one honest open knob, and it")
    print("  is a single number, not a structure.")


if __name__ == "__main__":
    main()
