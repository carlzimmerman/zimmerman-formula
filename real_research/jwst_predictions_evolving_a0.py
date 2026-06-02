#!/usr/bin/env python3
"""
The full set of JWST early-structure predictions IF a0(z)=a0(0)E(z) is real.
============================================================================

Worked out properly, with one honesty split that the original v1.0.1 paper got wrong:

  * a0 is ABSENT from the LINEAR cosmological perturbations (Bridge-1 order-counting
    theorem, bridge1_aest_equations.md). So evolving a0 does NOT boost linear growth, the
    linear power spectrum, or the number of halos that collapse. It does NOT, by itself,
    make 'more stellar mass earlier.'
  * a0 enters at NONLINEAR / quasi-static order -- the DYNAMICS of galaxies that have already
    formed (rotation, dispersion, apparent dark mass). THOSE are boosted, by powers of E(z).

So every robust prediction below is about the KINEMATICS of formed galaxies, all scaling with
the SAME E(z). A coherent E(z) dependence across all of them, tied to one number, is the
signature no LCDM-with-systematics conspiracy reproduces. Run: python <thisfile>
"""

import math

OM, OL = 0.315, 0.685


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def main():
    zs = [2, 4, 6, 8, 10, 15]
    print("=" * 84)
    print("THE SCALING TABLE -- everything keys off E(z) (one number)")
    print("=" * 84)
    print(f"  {'z':>4}{'E(z)=a0(z)/a0(0)':>18}{'sqrt(E) [Mdyn boost]':>22}"
          f"{'E^1/4 [v,sigma]':>17}{'-logE [BTFR dex]':>18}")
    for z in zs:
        e = E(z)
        print(f"  {z:>4}{e:>18.1f}{math.sqrt(e):>22.2f}{e**0.25:>17.2f}{-math.log10(e):>18.2f}")
    print()

    print("=" * 84)
    print("ROBUST PREDICTIONS  (kinematics of formed galaxies; a0-dependent, forced if true)")
    print("=" * 84)

    print("\nP1 [SHARPEST] dynamical-mass excess rises as sqrt(E(z)).")
    print("   deep-MOND apparent DM: M_dyn/M_bar = sqrt(a0(z)/g_bar) ~ sqrt(E(z)) at fixed g_bar.")
    print("   JWST observable: NIRSpec sigma / resolved kinematics -> M_dyn vs stellar M_*.")
    print("   PREDICTION: M_dyn/M_* grows with z as sqrt(E): +2.5x (z=4), +3.2x (z=6), +4.5x (z=10).")
    print("   CONTRAST: constant-a0 MOND is flat in z; LCDM has its own (different) halo evolution.")
    print("   DATA HINT: de Graaff+2024 (JADES z=5.5-7.4) M_dyn/M_* up to 40 -- needs the boost.")

    print("\nP2 [STRONG, has precedent] BTFR / Faber-Jackson zero-point shifts by -log10(E(z)) dex.")
    print("   v^4 = G M a0(z): at fixed v, inferred baryonic mass is LOWER at high z by 1/E(z).")
    print("   JWST observable: high-z stellar/baryonic Tully-Fisher (rotators) or M-sigma (dispersers).")
    print("   PREDICTION: zero-point shift -0.48 dex (z=2), -0.80 (z=4), -1.02 (z=6), -1.31 (z=10).")
    print("   DATA HINT: Ubler+2017 (KMOS3D) measured -0.45 dex at z~2.3 (predicted -0.48). Extends to JWST.")

    print("\nP3 velocity / dispersion zero-points: at fixed baryonic M, v and sigma ~ E(z)^1/4.")
    print("   PREDICTION: +32% (z=2), +59% (z=4), +80% (z=6), +113% (z=10) in v or sigma at fixed M_*.")
    print("   the sigma version is exactly de Graaff's channel (dispersions), so P1 and P3 are linked.")

    print("\nP4 the RAR knee moves to higher acceleration: g_dagger = a0(z) = E(z)*a0(0).")
    print("   PREDICTION: a resolved high-z radial-acceleration relation transitions at g ~ E(z)*1.2e-10.")
    print("   JWST observable: resolved rotation/dispersion profiles at z>4 mapping g_obs vs g_bar.")

    print("\nP5 [CLEAN NULL TEST] a redshift-MIXED RAR/BTFR is intrinsically broadened by log10(E(z_max)).")
    print("   a sample over z=4-10 spans a0 by E(10)/E(4)=3.2x -> +0.5 dex extra scatter UNLESS each")
    print("   galaxy is scaled by E(z_gal). PREDICTION: scaling by E(z) RE-TIGHTENS the relation to ~0.1 dex.")
    print("   This is the cleanest falsifier: a built-in null (do nothing -> broad; scale by E -> tight).")

    print("\nP6 [REFRAME, not over-production] 'impossible' DYNAMICALLY-massive galaxies are over-inferred.")
    print("   A Newtonian M_dyn ~ sigma^2 R/G over-estimates the true baryonic mass by the MOND boost")
    print("   sqrt(E(z)). So some 'too massive' z>6 galaxies have LOWER true baryonic mass; the high")
    print("   velocities are evolving-a0 MOND, not extra mass. PREDICTION: the excess M_dyn/M_* tracks")
    print("   sqrt(E(z)) (P1), and correcting for it removes the 'impossibility' for the dispersion-based ones.")

    print("\n" + "=" * 84)
    print("HONEST LIMITS  (where the original paper overreached -- stated plainly)")
    print("=" * 84)
    print("  * NOT predicted: more stellar mass / faster LINEAR collapse / a boosted halo mass function.")
    print("    a0 is absent from linear perturbations, so evolving a0 does NOT, by itself, form more")
    print("    galaxies earlier. The 'impossible early galaxies' are addressed only where their mass is")
    print("    DYNAMICALLY inferred (P6); a stellar-mass-density excess from SED fitting is NOT solved here.")
    print("  * NONLINEAR caveat: the boost in formed-galaxy dynamics is quasi-static MOND; a precise")
    print("    number needs the covariant theory's 2nd-order/screening treatment (the Y^3/2 non-analyticity).")
    print("  * DEGENERACY: any single observable can be mimicked by LCDM halo evolution or by systematics")
    print("    (IMF, sigma->mass conversion, beam smearing). The DISCRIMINATOR is the COHERENT E(z) scaling")
    print("    across P1-P5 simultaneously -- one E(z), many channels. That coherence is the real test.")

    print("\n" + "=" * 84)
    print("  HOW TO TEST IT: measure these at SEVERAL redshifts and check they all key off the SAME E(z).")
    print("  Don't fit one point -- fit the z-trend across channels. If M_dyn/M_* ~ sqrt(E), the BTFR")
    print("  zero-point ~ -log E, and sigma ~ E^1/4 all hold together, that is the evolving-a0 signature;")
    print("  if they scatter independently, the premise is wrong. The decisive datum remains a clean a0")
    print("  (i.e. M_dyn/M_bar at known g_bar) at z>2.")
    print("=" * 84)


if __name__ == "__main__":
    main()
