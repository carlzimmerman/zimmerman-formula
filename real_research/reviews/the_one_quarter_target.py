#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
How do we derive 0.173? Reframe the target -- the coefficient is exactly 1/4.
============================================================================

'How do we come up with this?' The honest research answer starts by writing the
target in the form most likely to be derivable. a0/cH = 0.173 is unrecognizable.
But substitute Friedmann and the number becomes clean:

    a0 = (c/2) sqrt(G rho_c)   =>   a0^2 = (1/4) c^2 G rho_c.

The coefficient is EXACTLY 1/4 -- which is the Bekenstein-Hawking entropy
coefficient (S = A/4G), the single deepest number in gravity. So the question
'derive 0.173' reframes to a sharp, physics-grounded one:

    Does the dark-sector acceleration carry the black-hole-entropy 1/4?

This script states the reframing, is HONEST about why it is a lead and not a
result, and lays out the concrete research prongs to settle it.

Pure stdlib. Run:  python reviews/the_one_quarter_target.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def main():
    rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
    rho_L = OL * rho_c                       # DARK-ENERGY density rho_Lambda (the framework's a0<->Lambda source)
    print("=" * 78)
    print("(1) The reframing: a0^2 = (1/4) c^2 G rho_Lambda -- the coefficient is 1/4")
    print("=" * 78)
    a0_quarter_L = math.sqrt(0.25 * C ** 2 * G * rho_L)   # framework: 1/4 on the DARK-ENERGY density
    a0_quarter_c = math.sqrt(0.25 * C ** 2 * G * rho_c)   # the SAME 1/4 on TOTAL density (a different thesis)
    print(f"   a0 (observed)                 = {A0:.3e} m/s^2")
    print(f"   sqrt( (1/4) c^2 G rho_Lambda) = {a0_quarter_L:.3e} m/s^2  <- FRAMEWORK (a0 from dark energy):")
    print(f"                                                     LOW EDGE of the observed band, not its centre")
    print(f"   sqrt( (1/4) c^2 G rho_c )     = {a0_quarter_c:.3e} m/s^2  <- TOTAL density: matches observed only")
    print(f"                                                     by abandoning a0<->Lambda (the rising-a0 branch)")
    print(f"   => the clean 1/4 belongs on rho_Lambda. You CANNOT have BOTH 'coefficient=1/4' AND 'matches")
    print(f"      observed 1.2e-10': the 1/4 needs rho_Lambda (9.9e-11), the data-match needs rho_total.")
    print(f"   (Z^2 = 4 x (8pi/3) = 32pi/3 is an ALGEBRAIC identity for ANY rho,H with H^2=8piGrho/3 -- it")
    print(f"    confirms the (c/2)sqrt(Grho) FORM, not the data value of a0, and holds for EITHER density.)\n")

    print("=" * 78)
    print("(2) Why 1/4 is the RIGHT target to chase (and not 0.173 or '8')")
    print("=" * 78)
    print("   * 1/4 = the Bekenstein-Hawking coefficient (S = A c^3 / 4 G hbar). It is")
    print("     the most fundamental, most DERIVED number in gravity -- it comes from")
    print("     the gravitational path integral / the area law, computed many ways.")
    print("   * a target of '1/4' is the kind of thing a counting argument CAN land on")
    print("     exactly; '0.173' and 'the cube's 8' are not (they are unrecognizable or")
    print("     need the compactification).")
    print("   * If the emergent dark sector is genuinely horizon-entropic, the 1/4 SHOULD")
    print("     propagate into its acceleration scale. So a0^2 = (1/4)c^2 G rho is")
    print("     exactly what an emergent-gravity origin would predict.\n")

    print("=" * 78)
    print("(3) HONEST: why this is a LEAD, not a result (turn the blade on it)")
    print("=" * 78)
    print("   * 'the coefficient is 1/4 AND Bekenstein is 1/4' is, by itself, a")
    print("     SUGGESTIVE NUMERICAL MATCH -- the same grade of evidence I have been")
    print("     skeptical of all session. 1/4 is a common number. Until a CALCULATION")
    print("     connects the dark-sector scale to S=A/4G, it is a coincidence-grade hint.")
    print("   * the 1/4 is clean only in the DENSITY form a0^2 ~ c^2 G rho. In the")
    print("     horizon form a0/cH the coefficient is the ugly 0.173. Which form is")
    print("     fundamental is THE open question -- the same units issue as before.")
    print("   * so: promising target, not a derivation. Excited and suspicious at once.\n")

    print("=" * 78)
    print("(4) The concrete research prongs to actually settle it")
    print("=" * 78)
    print("   A. de Sitter entropy displacement (Verlinde-done-right). Set up: S_dS =")
    print("      A/4G; a baryonic mass M displaces dS; the entropic force gives a0.")
    print("      Track EVERY factor of pi and the 1/4. Does a0^2 = (1/4)c^2 G rho fall")
    print("      out? (Caveat: Verlinde's elastic step is contested -- may give Newton.)")
    print("   B. MEASURE a0 to ~5% (WALLABY + Gaia DR4). Current 20% systematic cannot")
    print("      tell 1/2pi (0.159) from 1/6 (0.167) from the 1/4-implied 0.173. A 5%")
    print("      measurement PICKS the target coefficient and tells you which counting")
    print("      to aim for. Cheapest, most decisive step -- and it needs no new theory.")
    print("   C. orbifold DOF route (if A fails). Does the dark-sector degree-of-freedom")
    print("      count carry the orbifold order 8? That is the interlocking-web route --")
    print("      the only one where the cosmology coefficient meets the particle side.")
    print("   D. Padmanabhan holographic equipartition with the FULL Komar energy +")
    print("      area law; extract the a0 coefficient symbolically; check for the 1/4.\n")

    print("=" * 78)
    print("VERDICT -- how you come up with it")
    print("=" * 78)
    print("  You do NOT guess 0.173. You (1) write the target in derivable form --")
    print("  a0^2 = (1/4) c^2 G rho_c, isolating the single coefficient 1/4; (2) note")
    print("  that 1/4 is the Bekenstein-Hawking number, so the question becomes 'does")
    print("  the dark sector carry the black-hole entropy 1/4?' -- a real quantum-gravity")
    print("  question, not a number-hunt; (3) attack it two ways -- DERIVE it (de Sitter")
    print("  entropy displacement, prong A/D) and MEASURE which coefficient nature uses")
    print("  (a0 to 5%, prong B). If the entropy calc yields 1/4 AND the data lands on")
    print("  0.173 rather than 1/2pi or 1/6, the O(1) is solved and emergent.")
    print()
    print("  That is the honest method: reframe to the most fundamental coefficient,")
    print("  pose it as a derivation problem, and let a cheap measurement pick the target.")
    print("  Excited because 1/4 is the deepest number in gravity; suspicious because")
    print("  'it equals 1/4' is exactly the kind of hint that has to be EARNED by a calc.")


if __name__ == "__main__":
    main()
