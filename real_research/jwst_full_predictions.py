#!/usr/bin/env python3
"""
The FULL list: every JWST measurement type vs the FAITHFUL evolving-a0 prediction.
=================================================================================

CORRECTED. This script previously used the RETIRED "rising" reading a0(z)=a0(0)E(z),
E(z)=sqrt(Om(1+z)^3+OL) (the rho_total/cH0 conflation the project retired). The framework's
settled reading sets a0 by the DARK-ENERGY density:

    a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)),
    CPL: rho_DE(z)/rho0 = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z)),  DESI DR2 w0=-0.752, wa=-0.86

(identical to opus_48_extended_research/papers/a0z_desi_figure.py, verified to 1e-6). Under DESI
this is NON-MONOTONIC and DECLINING (+6% bump at z~0.41, then 0.737 at z=3, 0.51 at z=6, 0.36 at
z=10). Every FORCED line therefore has the OPPOSITE SIGN from the retired rising reading: a0 is
WEAKER early -> kinematic boosts WEAKEN with z, discs sit BELOW the BTFR, sizes GROW, surface
densities DROP, and the EFE STRENGTHENS at high z. Labels:

  [FORCED]      a0-dependent (galaxy KINEMATICS/structure); sign follows if the premise is true.
  [SUGGESTIVE]  plausible, needs the nonlinear/relativistic treatment to be quantitative.
  [NOT a0]      gas/nuclear/linear physics -- the framework predicts NOTHING here (stated so).

QUARANTINE: a0(0) is the INPUT; only the SHAPE a0(z)/a0(0) is predicted. Run: python <thisfile>
"""

import math

W0, WA = -0.752, -0.86  # DESI DR2 DESY5


def a0z(z):
    """a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) -- faithful (declining) reading."""
    rho = (1 + z) ** (3 * (1 + W0 + WA)) * math.exp(-3 * WA * z / (1 + z))
    return math.sqrt(rho)


def table():
    print("MASTER SCALING TABLE  (a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE0); a0(0) is the INPUT):")
    print(f"  {'z':>4}{'a0(z)/a0(0)':>13}{'sqrt':>8}{'^1/4':>8}{'1/sqrt':>9}{'-log10':>9}")
    for z in (0.41, 1, 2, 4, 6, 8, 10):
        a = a0z(z)
        print(f"  {z:>4}{a:>13.3f}{math.sqrt(a):>8.3f}{a ** 0.25:>8.3f}{1 / math.sqrt(a):>9.3f}{-math.log10(a):>9.3f}")
    print("   uses: sqrt=Mdyn/dispersion-mass boost; ^1/4=v,sigma; 1/sqrt=sizes; -log10=BTFR dex; ratio=surface density.")
    print("   a0(z)<1 for z>~0.45 -> boosts WEAKEN, BTFR dex NEGATIVE (discs BELOW), sizes LARGER, density LOWER.\n")


def block(title, rows):
    print("=" * 90); print(title); print("=" * 90)
    for tag, obs, pred in rows:
        print(f"  [{tag:10}] {obs}")
        print(f"               -> {pred}")
    print()


def main():
    table()
    a2, a3, a4, a6, a10 = a0z(2), a0z(3), a0z(4), a0z(6), a0z(10)

    block("I. KINEMATICS  (NIRSpec dispersions; NIRCam grism / NIRSpec-IFU resolved velocity fields)", [
        ("FORCED", "velocity dispersion sigma vs stellar mass M_*",
         f"sigma ~ a0(z)^1/4 at fixed baryonic M: {100*(a4**0.25-1):+.0f}% (z=4), {100*(a6**0.25-1):+.0f}% (z=6), "
         f"{100*(a10**0.25-1):+.0f}% (z=10). Zero-point shifts DOWN (a0 declines)."),
        ("FORCED", "rotation velocity / baryonic Tully-Fisher (rotators) -- THE SIGNATURE",
         f"v^4=G M a0(z): zero-point shifts +log10 a0(z) dex = {math.log10(a2**0.25):+.3f} (z=2), "
         f"{math.log10(a6**0.25):+.3f} (z=6), {math.log10(a10**0.25):+.3f} (z=10) -> discs BELOW the z=0 BTFR. "
         f"[Ubler+17 -0.45@z2.3 is the right DIRECTION but ~20x the framework's ~-0.02 dex: below floor, not a fit.]"),
        ("FORCED", "dynamical-to-stellar mass ratio M_dyn/M_*",
         f"M_dyn/M_bar ~ sqrt(a0(z)): x{math.sqrt(a6):.2f} (z=6), x{math.sqrt(a10):.2f} (z=10) -- LESS apparent DM early "
         f"(deep-MOND only). [de Graaff+24 M_dyn/M*~40 is the WRONG way: declining a0 lowers, not raises, the boost -> NOT support.]"),
        ("FORCED", "resolved radial-acceleration relation g_obs vs g_bar",
         f"the MOND knee g_dagger=a0(z) moves to LOWER acceleration with z (x{a6:.2f} by z=6)."),
        ("FORCED", "scatter of a redshift-MIXED kinematic sample",
         f"broadened by log10(a0(z_max)/a0(z_min)); scaling each galaxy by its declining a0(z_gal) RE-TIGHTENS (clean null test)."),
        ("FORCED", "'impossible' dynamically-massive galaxies",
         "over-inference of M_dyn by sqrt(a0(z)) is WEAKER at high z (a0 declines) -> faithful a0(z) removes LESS 'impossible' mass, not more."),
    ])

    block("II. STRUCTURE / MORPHOLOGY  (NIRCam imaging: sizes, surface brightness, support)", [
        ("FORCED", "MOND/characteristic radius r where g~a0",
         f"r_MOND=sqrt(GM/a0(z)) ~ 1/sqrt(a0(z)): the deep-MOND regime starts at LARGER radius at high z (x{1/math.sqrt(a6):.2f} @ z=6)."),
        ("FORCED", "critical surface density (HSB/LSB boundary), Freeman-law analog",
         f"Sigma_M=a0(z)/G ~ a0(z): x{a6:.2f} by z=6 -> high-z disks have LOWER critical surface density; the disk-stability line FALLS."),
        ("SUGGESTIVE", "dispersion- vs rotation-support fraction",
         "lower a0 -> shallower-MOND internal dynamics at fixed mass -> LESS MOND-boosted support at high z."),
        ("FORCED", "external field effect (EFE) on high-z dwarfs/satellites",
         "g_ext/a0(z) is LARGER at high z (a0 declines) -> STRONGER EFE -> high-z low-mass galaxies MORE quenched/Newtonian at fixed g_ext "
         "(the cosmic external field g_ext also evolves -- net amplitude under study; the a0(z) factor pushes EFE STRONGER)."),
    ])

    block("III. BLACK HOLES & AGN  (NIRSpec broad/narrow lines, MIRI)", [
        ("SUGGESTIVE", "M_BH-sigma relation at high z",
         "if host sigma is a0^1/4-LOWERED, M_BH-sigma zero-point shifts the other way; this does NOT manufacture 'overmassive' BHs."),
        ("SUGGESTIVE", "AGN host-galaxy dynamics",
         "host kinematics carry the same (declining) sqrt(a0)/a0^1/4 factors as ordinary galaxies."),
    ])

    block("IV. DEMOGRAPHICS  (NIRCam counts: stellar-mass & luminosity functions) -- THE HONEST LIMIT", [
        ("NOT a0", "stellar mass function / abundance of massive galaxies",
         "a0 is ABSENT from LINEAR growth -> evolving a0 does NOT form more/earlier galaxies. And declining a0 does NOT help the over-production tension."),
        ("FORCED", " ...high-mass end IF mass is dynamically inferred",
         "those masses are over-estimated by sqrt(a0(z)) < 1 at high z -- a SMALL, declining correction, not a rescue of 'impossible' galaxies."),
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
        ("FORCED", "a0-cosmography: rho_DE(z) read back from the kinematics via a0(z)",
         "a clean a0 at several z reconstructs the dark-energy history sqrt(rho_DE(z)/rho_DE0) -- an independent w(z) probe, hostage to the same DESI evolution."),
        ("SUGGESTIVE", "lensed high-z sources behind clusters (UNCOVER etc.)",
         "deflection involves the relativistic MOND sector + the cluster residual-mass issue -- needs the covariant theory."),
    ])

    print("=" * 90)
    print("  THE TEST (one line): every [FORCED] row keys off the SAME DECLINING a0(z). Measure them")
    print("  across z and check the coherence AND THE SIGN -- M_dyn/M_*~sqrt(a0) (LESS DM early), BTFR")
    print("  BELOW the z=0 line, sigma~a0^1/4 (lower), sizes~1/sqrt(a0) (larger), Sigma~a0 (lower) -- ALL")
    print("  from one declining number. Discs BELOW the BTFR at z>1 is the signature; flat-or-above")
    print("  falsifies the evolving-a0 bridge. HOSTAGE TO DESI: if w->-1, a0=const and all of this vanishes.")
    print("  The [NOT a0] rows are where the framework is SILENT -- claiming them is the old overreach.")
    print("=" * 90)


if __name__ == "__main__":
    main()
