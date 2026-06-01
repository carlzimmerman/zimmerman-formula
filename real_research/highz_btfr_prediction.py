#!/usr/bin/env python3
"""
The one recoverable prediction, made concrete and pre-registered.
=================================================================

Recovery sweep of ai_slop/ (four independent agents + the repo's own audit) found
exactly ONE sound, recoverable physics prediction: the MOND acceleration scale
evolves as a0(z) = a0(0) * E(z), E(z)=sqrt(Om(1+z)^3+OL). It is Z-INDEPENDENT
(Z cancels in the ratio), rests on standard MOND (McGaugh) + the exact Friedmann
scaling rho_c ∝ E^2 -- NOT on Z^2=32pi/3 -- and its clean regime (z>10 deep-MOND)
is unmeasured. Everything else in the program is numerology/dead/failing.

This script states the prediction the way it must be tested -- as a BARYONIC
TULLY-FISHER ZERO-POINT OFFSET vs the local relation -- with no Z, no per-object
tuning, and an honest account of what current data already says.

Deep-MOND: sigma^4 (or v_flat^4) = G * M_bar * a0(z). At fixed baryonic mass,
  sigma(z)/sigma(0) = [a0(z)/a0(0)]^(1/4) = E(z)^(1/4).
So a galaxy at redshift z should sit ABOVE the local BTFR (in log sigma at fixed
M_bar) by

    d_logsigma(z) = (1/4) log10 E(z)        [EVOLVING a0, this prediction]
    d_logsigma(z) = 0                        [CONSTANT a0, standard MOND -- the NULL]

That offset is the entire, parameter-free, falsifiable content.

Run:  python real_research/highz_btfr_prediction.py
"""

import math

OM, OL = 0.315, 0.685


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def offset_dex(z):
    return 0.25 * math.log10(E(z))


def main():
    print("=" * 74)
    print("(1) The parameter-free prediction: BTFR zero-point offset vs local")
    print("=" * 74)
    print("   d_logsigma(z) = (1/4) log10 E(z)   [evolving]   vs   0   [constant a0]")
    print(f"   {'z':>6}{'E(z)':>9}{'offset [dex]':>15}{'sigma ratio E^1/4':>20}")
    for z in (0.5, 1, 2, 4, 6, 10, 12.3, 14.2):
        print(f"   {z:>6.1f}{E(z):>9.2f}{offset_dex(z):>15.3f}{E(z)**0.25:>20.2f}")
    print("   => the split is small at z<2 (a few %), large at z>10 (>2x). The test")
    print("      is only decisive in the deep-MOND z>10 regime.\n")

    print("=" * 74)
    print("(2) What current data already says -- honestly")
    print("=" * 74)
    print("   * z<1 (MIGHTEE-HI, local BTFR): zero-point does NOT evolve. Consistent with")
    print("     CONSTANT a0 -- but E(1)^1/4=1.16, a ~16% effect at the edge of detectability,")
    print("     so it weakly disfavors evolving a0 (does not kill it).")
    print("   * z~4-6 (ALMA [CII] rotating disks; high-z BTFR): also ~no zero-point shift")
    print("     reported. E(5)^1/4~1.7 would be a clear 0.23 dex shift -- so this DISfavors")
    print("     evolving a0 -- BUT those are MASSIVE disks at g>a0 (Newtonian regime), where")
    print("     a0(z) barely enters. NOT a clean deep-MOND test (the regime trap).")
    print("   * z~6 (de Graaff+24 JADES dispersions): evolving a0 has a ~6.5sigma mean offset")
    print("     -- poor, though it beats constant-a0 MOND (10.7sigma) and stellar-mass/gas")
    print("     uncertainties dominate at z~6 where E^1/4 is modest.")
    print("   * z>10 (GN-z11 etc.): the advertised 'exact match' is an ARTIFACT -- the factor-2")
    print("     stellar-mass band (77-109 km/s) is wider than the measurement, and GN-z11 is")
    print("     AGN-contaminated. Genuinely AMBIGUOUS / data-limited. This is the open regime.\n")

    print("=" * 74)
    print("(3) PRE-REGISTERED test on the decisive z>10 targets")
    print("=" * 74)
    print("   For each, deep-MOND predicts sigma at fixed M_bar to be E^1/4 ABOVE the local")
    print("   BTFR if a0 evolves, or ON it if a0 is constant. Decision needs only resolved")
    print("   sigma (NIRSpec-IFU / ALMA [OIII]88um) + a baryonic mass to ~0.3 dex:")
    print(f"   {'target':<22}{'z':>7}{'evolving offset':>17}{'sigma_evolv/sigma_const':>24}")
    for name, z in [("GN-z11", 10.6), ("GLASS-z12", 12.34),
                    ("Maisie's Galaxy", 11.44), ("JADES-GS-z14-0", 14.18)]:
        print(f"   {name:<22}{z:>7.2f}{offset_dex(z):>17.3f}{E(z)**0.25:>24.2f}")
    print()
    print("   FALSIFICATION RULE (pre-registered, parameter-free):")
    print("   * if z>12 deep-MOND galaxies sit ON the local BTFR  -> a0 is CONSTANT;")
    print("     the evolving prediction (this program's one survivor) is DEAD.")
    print("   * if they sit ~0.36-0.38 dex (factor ~2.3x in sigma) ABOVE it -> a0 EVOLVES;")
    print("     first genuine positive result of the program.")
    print("   No Z, no 137, no orbifold -- just E(z)^1/4 vs 1.\n")

    print("=" * 74)
    print("VERDICT")
    print("=" * 74)
    print("  * This is the single recoverable physics prediction; it is sound, Z-free, and")
    print("    falsifiable. It is NOT original (it is Milgrom's a0~cH(z) idea) and current")
    print("    data MILDLY DISFAVORS it -- but only in the wrong (Newtonian) regime, where")
    print("    the effect is suppressed. The clean deep-MOND z>10 test is unmeasured and")
    print("    decisive (>2x split), and JWST/ALMA are delivering exactly those data now.")
    print("  * Honest: defend it as a sharp, pre-registered, near-term-killable prediction,")
    print("    not as a discovery. That is the most the recovered science supports.")


if __name__ == "__main__":
    main()
