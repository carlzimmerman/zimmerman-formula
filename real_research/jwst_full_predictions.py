#!/usr/bin/env python3
"""
The FULL list: every JWST measurement type vs the evolving-a0 prediction.
========================================================================

Comprehensive map of what a0(z)=a0(0)E(z) predicts for each JWST observable -- including the
ones it does NOT touch, because the boundary is the honest part. Labels:

  [FORCED]      a0-dependent (galaxy KINEMATICS); follows if the premise is true.
  [SUGGESTIVE]  plausible, needs the nonlinear/relativistic treatment to be quantitative.
  [NOT a0]      gas/nuclear/linear physics -- the framework predicts NOTHING here (stated so).

The whole signature is that every FORCED line keys off the SAME E(z). Run: python <thisfile>
"""

import math
OM, OL = 0.315, 0.685
def E(z): return math.sqrt(OM * (1 + z) ** 3 + OL)


def table():
    print("MASTER SCALING TABLE (a0(z)/a0(0)=E(z); a0(0)=1.2e-10):")
    print(f"  {'z':>4}{'E(z)':>8}{'sqrt(E)':>9}{'E^1/4':>8}{'1/sqrt(E)':>11}{'-log10 E':>10}")
    for z in (1, 2, 4, 6, 8, 10, 13):
        e = E(z)
        print(f"  {z:>4}{e:>8.1f}{math.sqrt(e):>9.2f}{e**0.25:>8.2f}{1/math.sqrt(e):>11.2f}{-math.log10(e):>10.2f}")
    print("   uses: sqrt(E)=Mdyn/dispersion-mass boost; E^1/4=v,sigma; 1/sqrt(E)=sizes; -logE=BTFR dex; E=surface density.\n")


def block(title, rows):
    print("=" * 88); print(title); print("=" * 88)
    for tag, obs, pred in rows:
        print(f"  [{tag:10}] {obs}")
        print(f"               -> {pred}")
    print()


def main():
    table()

    block("I. KINEMATICS  (NIRSpec dispersions; NIRCam grism / NIRSpec-IFU resolved velocity fields)", [
        ("FORCED", "velocity dispersion sigma vs stellar mass M_*",
         "sigma ~ E(z)^1/4 at fixed baryonic M: +59% (z=4), +80% (z=6), +113% (z=10). Zero-point shifts up."),
        ("FORCED", "rotation velocity / baryonic Tully-Fisher (rotators)",
         "v^4=G M a0(z): zero-point shifts -log10 E(z) dex: -0.48 (z=2), -1.02 (z=6), -1.31 (z=10). [Ubler+17: -0.45@z2.3]"),
        ("FORCED", "dynamical-to-stellar mass ratio M_dyn/M_*",
         "M_dyn/M_bar ~ sqrt(E(z)): x3.2 (z=6), x4.5 (z=10) -- DEEP-MOND ONLY (compact galaxies go Newtonian). [de Graaff+24 M_dyn/M*~40 is ~10x beyond this boost: NOT support -- see reviews/redteam_the_puzzle.py]"),
        ("FORCED", "resolved radial-acceleration relation g_obs vs g_bar",
         "the MOND knee g_dagger=a0(z)=E(z)*a0(0) moves to HIGHER acceleration with z."),
        ("FORCED", "scatter of a redshift-MIXED kinematic sample",
         "broadened by log10 E(z_max); scaling each galaxy by E(z_gal) RE-TIGHTENS to ~0.1 dex (clean null test)."),
        ("FORCED", "'impossible' dynamically-massive galaxies",
         "M_dyn (Newtonian) over-inferred by sqrt(E(z)): true baryonic mass LOWER; high v is MOND, not mass."),
    ])

    block("II. STRUCTURE / MORPHOLOGY  (NIRCam imaging: sizes, surface brightness, support)", [
        ("FORCED", "MOND/characteristic radius r where g~a0",
         "r_MOND=sqrt(GM/a0(z)) ~ 1/sqrt(E): the deep-MOND regime starts at SMALLER radius at high z (x3.2 smaller @ z=6)."),
        ("FORCED", "critical surface density (HSB/LSB boundary), Freeman-law analog",
         "Sigma_M=a0(z)/G ~ E(z): x10 by z=6 -> high-z disks should be DENSER; the disk-stability line rises."),
        ("SUGGESTIVE", "dispersion- vs rotation-support fraction",
         "higher a0 -> deeper-MOND internal dynamics -> more pressure/MOND-boosted support at fixed mass."),
        ("FORCED", "external field effect (EFE) on high-z dwarfs/satellites",
         "g_ext/a0(z)=g_ext/(E(z)a0(0)) is SMALLER at high z -> WEAKER EFE -> high-z low-mass galaxies more boosted/isolated."),
    ])

    block("III. BLACK HOLES & AGN  (NIRSpec broad/narrow lines, MIRI)", [
        ("SUGGESTIVE", "M_BH-sigma relation at high z",
         "if host sigma is E^1/4-boosted, M_BH-sigma zero-point shifts; some 'overmassive' BHs partly a sigma-inference effect."),
        ("SUGGESTIVE", "AGN host-galaxy dynamics",
         "host kinematics carry the same sqrt(E)/E^1/4 boosts as ordinary galaxies."),
    ])

    block("IV. DEMOGRAPHICS  (NIRCam counts: stellar-mass & luminosity functions) -- THE HONEST LIMIT", [
        ("NOT a0", "stellar mass function / abundance of massive galaxies",
         "a0 is ABSENT from LINEAR growth -> evolving a0 does NOT form more/earlier galaxies. NO over-production predicted."),
        ("FORCED", " ...but the high-mass end IF mass is dynamically inferred",
         "those masses are over-estimated by sqrt(E) (cf. M_dyn above) -- a measurement artifact, not extra galaxies."),
        ("NOT a0", "UV luminosity function / cosmic star-formation-rate density",
         "set by star formation & gas physics, not a0. The framework predicts nothing here."),
        ("NOT a0", "high-z galaxy clustering / 2-point correlation",
         "linear/large-scale -> a0 absent -> unchanged from LCDM (Bridge-1 theorem). Not a discriminator."),
    ])

    block("V. SPECTROSCOPY / CHEMISTRY / REIONIZATION  (NIRSpec lines, MIRI dust) -- NOT a0", [
        ("NOT a0", "metallicities, abundance ratios, ionization, dust",
         "nuclear/gas/radiative physics -- a0-independent. No prediction (do not claim these)."),
        ("NOT a0", "reionization history, Lyman-continuum escape fraction",
         "gas & radiation physics -- not set by a0."),
    ])

    block("VI. COSMOLOGY FROM JWST  (the payoff channel)", [
        ("FORCED", "a0-cosmography: H(z) = Z a0(z)/c from the kinematics",
         "a 3rd, independent expansion probe. A clean a0 at several z arbitrates Planck(67.4) vs SH0ES(73)."),
        ("SUGGESTIVE", "lensed high-z sources behind clusters (UNCOVER etc.)",
         "deflection involves the relativistic MOND sector + the cluster residual-mass issue -- needs the covariant theory."),
    ])

    print("=" * 88)
    print("  THE TEST (one line): every [FORCED] row keys off the SAME E(z). Measure them across")
    print("  z and check the coherence -- M_dyn/M_*~sqrt(E), BTFR~-logE, sigma~E^1/4, sizes~1/sqrt(E),")
    print("  Sigma~E -- ALL from one number. That coherence is unforgeable by LCDM+systematics.")
    print("  The [NOT a0] rows are where the framework is SILENT -- claiming them is the old overreach.")
    print("=" * 88)


if __name__ == "__main__":
    main()
