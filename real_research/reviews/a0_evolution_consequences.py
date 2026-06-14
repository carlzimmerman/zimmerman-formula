#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
IF a0(z) = a0(0) E(z) is true, what else follows? The consequence cascade.
=========================================================================

A good prediction is valuable because it GENERATES correlated consequences you
can independently check, not because it is one number. This derives everything
that follows from the one surviving prediction, tiered by rigor:

  DIRECT (kinematic, rigorous): BTFR, dispersions, MOND radius -- all evolve.
  BIG ONE (rigorous + novel): a0(z)/a0(0) = E(z) = H(z)/H0 is Z-INDEPENDENT, so
    galaxy kinematics at redshift z directly MEASURE H(z) -- a new, distance-
    ladder-independent expansion probe that could arbitrate the Hubble tension.
  CONCEPTUAL: the Milgrom a0~cH0 coincidence dissolves; a0 ties to dark energy.
  SUGGESTIVE (qualitative): stronger early MOND boost -> early structure / JWST.

Pure stdlib. Run:  python reviews/a0_evolution_consequences.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def part1_direct():
    print("=" * 80)
    print("(1) DIRECT kinematic consequences (rigorous -- pure deep-MOND algebra)")
    print("=" * 80)
    print("   deep MOND: v_flat^4 = G M a0(z);  sigma^4 = (4/9) G M a0(z);")
    print("   transition radius r_t = sqrt(G M / a0(z)).  With a0(z)=a0(0)E(z):")
    print(f"   {'z':>5}{'E(z)':>8}{'v_flat/v0':>11}{'sigma/sig0':>12}{'r_MOND/r0':>11}")
    for z in (0, 0.5, 1, 2, 6, 10, 14):
        print(f"   {z:>5.1f}{E(z):>8.2f}{E(z)**0.25:>11.3f}{E(z)**0.25:>12.3f}"
              f"{E(z)**-0.5:>11.3f}")
    print("   => at fixed baryonic mass, galaxies SPIN FASTER (v~E^1/4) and become")
    print("      MONDian at SMALLER radius (r_t~E^-1/2) at high z. Two correlated,")
    print("      independently-checkable trends from the same law.\n")


def part2_Hz_probe():
    print("=" * 80)
    print("(2) THE BIG ONE: a0(z) is a Z-INDEPENDENT probe of H(z) (rigorous + novel)")
    print("=" * 80)
    print("   a0(z)/a0(0) = E(z) = H(z)/H0  -- the Z and a0(0) CANCEL. So measuring the")
    print("   BTFR zero-point at redshift z directly returns H(z)/H0, with NO distance")
    print("   ladder, NO standard candle, NO CMB. Galaxy kinematics become a map of the")
    print("   cosmic expansion history.")
    print()
    print(f"   {'z':>5}{'measured a0(z)/a0(0)':>22}{'= H(z)/H0':>11}{'H(z) [km/s/Mpc]':>17}")
    for z in (0, 0.5, 1, 2):
        Hz = H0 * E(z) * MPC / 1e3
        print(f"   {z:>5.1f}{E(z):>22.3f}{E(z):>11.3f}{Hz:>17.1f}")
    print()
    print("   CONSEQUENCES that follow:")
    print("    * an INDEPENDENT H(z) -- a new rung that does not share the systematics")
    print("      of SNe/BAO/CMB, so it can ARBITRATE the Hubble tension;")
    print("    * differentiate H(z) -> reconstruct the dark-energy w(z) from galaxy")
    print("      dynamics alone;")
    print("    * a built-in consistency test: the H(z) you read off galaxies MUST match")
    print("      the H(z) from BAO/SNe. If they disagree, a0(z)~E(z) is falsified.")
    print("   This is the richest derivable consequence and it is Z-independent.\n")


def part3_conceptual():
    print("=" * 80)
    print("(3) CONCEPTUAL consequences (follow logically)")
    print("=" * 80)
    a0_now = C * H0 / Z
    H_inf = H0 * math.sqrt(OL)
    a0_inf = C * H_inf / Z
    print("   * The Milgrom coincidence DISSOLVES. 'Why is a0 ~ cH0 today?' is no longer")
    print("     a coincidence -- a0 = cH(z)/Z holds at EVERY epoch; today is not special.")
    print(f"   * a0 is tied to DARK ENERGY. As H(z)->H_inf=H0 sqrt(OL) (de Sitter), a0")
    print(f"     freezes at a0_inf = cH_inf/Z = {a0_inf:.2e} m/s^2 = a0_now/sqrt(OL) inverse...")
    print(f"     a0_now = {a0_now:.2e}; a0_future = {a0_inf:.2e} (ratio {a0_now/a0_inf:.3f}=1/sqrt(OL)).")
    print("     So the FINAL MOND scale is set purely by Lambda -- a0 and dark energy")
    print("     are the same number, which is what an emergent/horizon origin predicts.")
    print("   * a0 had NO well-defined value before dark-energy domination in the same")
    print("     way -- in the deep matter era a0(z) ~ cH0 E(z) was much larger, so the")
    print("     MOND regime was a fixed FRACTION (1/Z of the horizon) at all times.\n")


def part4_suggestive():
    print("=" * 80)
    print("(4) SUGGESTIVE consequences (qualitative -- need a real calculation)")
    print("=" * 80)
    print("   * EARLY STRUCTURE FORMATION. a0 was LARGER in the past (E(z)x), so the")
    print("     MOND gravity boost was STRONGER earlier -> structure forms faster and")
    print("     earlier than even constant-a0 MOND (which already beats LCDM). This is")
    print("     the natural direction to address the JWST 'too-massive-too-early'")
    print("     galaxies. HONEST: this is qualitative -- MOND structure formation is")
    print("     hard, and the JWST tension is itself contested. A real N-body/Boltzmann")
    print("     calc is needed before claiming it. But the SIGN is a genuine consequence.")
    print("   * The MOND fifth-force RANGE tracks the horizon c/H(z) (apparent-horizon")
    print("     picture), so the scale of modified gravity shrinks with cosmic time.")
    print("   * Pressure-supported dwarfs at high z: dispersions boosted by E(z)^1/4 --")
    print("     a second, independent kinematic channel beyond rotation curves.\n")


def main():
    part1_direct()
    part2_Hz_probe()
    part3_conceptual()
    part4_suggestive()
    print("=" * 80)
    print("THE META-POINT -- why this matters")
    print("=" * 80)
    print("  a0(z) ~ E(z) is not ONE prediction; it is a GENERATOR of correlated,")
    print("  independently-checkable consequences: faster spins + smaller MOND radii +")
    print("  boosted dispersions at high z, an independent H(z) (hence a Hubble-tension")
    print("  arbiter and a w(z) probe), the dissolution of Milgrom's coincidence, an")
    print("  a0-Lambda identity, and (suggestively) early structure growth. They are")
    print("  ALL forced by the same law, so they form a tight web: confirm one, the")
    print("  others must follow; break one, the law is dead. THAT is what makes it real")
    print("  science worth doing -- a fertile hypothesis, not an isolated number.")
    print()
    print("  HONEST boundary: none of this DERIVES the value Z (still fit), nor fixes")
    print("  the cluster problem, nor needs the dead numerology. It is the consequence")
    print("  tree of the ONE surviving prediction -- and it is a surprisingly rich one.")


if __name__ == "__main__":
    main()
