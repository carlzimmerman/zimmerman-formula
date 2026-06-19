#!/usr/bin/env python3
"""
JWST early-structure predictions under the framework's FAITHFUL a0(z).
======================================================================

CORRECTED. This script previously used the RETIRED "rising" reading a0(z)=a0(0)E(z) with
E(z)=sqrt(Om(1+z)^3+OL) -- the rho_total/cH0 conflation the project explicitly retired. The
framework's settled reading is that a0 is set by the DARK-ENERGY density, so

    a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)),
    CPL:  rho_DE(z)/rho0 = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z)),   DESI DR2 w0=-0.752, wa=-0.86

(identical to opus_48_extended_research/papers/a0z_desi_figure.py, verified to 1e-6). Under DESI
this is NON-MONOTONIC and DECLINING: a small +6% bump at z~0.41, then a0 FALLS to 0.737 a0 at
z=3, 0.51 at z=6, 0.36 at z=10. So every high-z kinematic effect has the OPPOSITE SIGN from the
retired rising reading -- a0 is WEAKER early, not stronger, and discs sit BELOW the local BTFR.

Two honesty splits (unchanged and correct):
  * a0 is ABSENT from the LINEAR cosmological perturbations (Bridge-1 order-counting theorem) ->
    evolving a0 does NOT boost linear growth, the power spectrum, or the halo mass function. It
    does NOT, by itself, make 'more stellar mass earlier.'
  * a0 enters at NONLINEAR / quasi-static order -- the DYNAMICS of formed galaxies. With a
    DECLINING a0, that modulation REDUCES the MOND boost at high z.

QUARANTINE: a0(0) is the INPUT; only the SHAPE a0(z)/a0(0) is predicted. Run: python <thisfile>
"""

import numpy as np

# DESI DR2 (arXiv:2503.14738) w0wa CDM, DESI+CMB+DESY5
W0, WA = -0.752, -0.86


def a0z(z):
    """a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) -- framework's faithful (declining) reading."""
    rho = (1 + z) ** (3 * (1 + W0 + WA)) * np.exp(-3 * WA * z / (1 + z))
    return np.sqrt(rho)


def main():
    zs = [0.41, 1, 2, 3, 4, 6, 10]
    print("=" * 86)
    print("THE SCALING TABLE -- everything keys off the SAME declining a0(z)/a0(0)")
    print("  a0(z)=(c/2)sqrt(G rho_DE(z)), DESI DR2 DESY5 | quarantine: a0(0) input, SHAPE predicted")
    print("=" * 86)
    print(f"  {'z':>5}{'a0(z)/a0(0)':>13}{'sqrt [Mdyn/Mbar]':>18}{'^1/4 [v,sigma]':>16}{'BTFR dex':>11}")
    for z in zs:
        a = a0z(z)
        print(f"  {z:>5}{a:>13.3f}{np.sqrt(a):>18.3f}{a ** 0.25:>16.3f}{np.log10(a ** 0.25):>11.3f}")
    print("  a0(z)<1 for z>~0.45 -> sqrt, ^1/4 all <1 -> boosts WEAKEN; BTFR offset NEGATIVE.\n")

    print("=" * 86)
    print("ROBUST PREDICTIONS  (kinematics of formed galaxies; signs FORCED by the declining a0(z))")
    print("=" * 86)

    print("\nP1 [SIGNATURE -- the cleanest discriminator is the SIGN] high-z discs rotate SLOWER")
    print("   at fixed baryonic mass: V_flat^4 = G M_bar a0(z), so V ~ a0(z)^1/4 and discs sit")
    print("   BELOW the local BTFR. dlogV = (1/8) log10(rho_DE(z)/rho_DE0).")
    print(f"   PREDICTION (NEGATIVE offset): dV = {100 * (a0z(2) ** 0.25 - 1):+.1f}% (z=2), "
          f"{100 * (a0z(3) ** 0.25 - 1):+.1f}% (z=3), {100 * (a0z(6) ** 0.25 - 1):+.1f}% (z=6), "
          f"{100 * (a0z(10) ** 0.25 - 1):+.1f}% (z=10).")
    print("   CONTRAST: LCDM & constant-a0 MOND predict no a0-decline; the retired RISING reading")
    print("   predicted discs ABOVE. Discs BELOW the z=0 BTFR at z>1 is the framework's signature.")
    print("   DATA: Ubler+2017 (KMOS3D z~2.3) shows the right (negative) DIRECTION, but the framework's")
    print("   magnitude there (~-0.02 dex) is below per-galaxy scatter -- existing data cannot decide.")

    print("\nP2 dynamical-to-baryonic ratio DECREASES with z (LESS apparent dark matter early).")
    print("   deep-MOND M_dyn/M_bar = sqrt(a0(z)/g_bar) ~ sqrt(a0(z)) at fixed g_bar.")
    print(f"   PREDICTION: M_dyn/M_bar x{np.sqrt(a0z(3)):.2f} (z=3), x{np.sqrt(a0z(6)):.2f} (z=6), "
          f"x{np.sqrt(a0z(10)):.2f} (z=10) vs local -- ~{100 * (1 - np.sqrt(a0z(10))):.0f}% LESS apparent DM by z=10.")
    print("   HONEST NON-WIN: a DECLINING a0 does NOT explain JWST's HIGH dynamical-to-stellar ratios")
    print("   (de Graaff+2024, M_dyn/M_* up to ~40); it makes the MOND boost SMALLER early -- the wrong")
    print("   way to help. Those high dynamical masses are NOT a faithful-a0(z) effect.")

    print("\nP3 velocity / dispersion zero-points DROP at fixed baryonic mass: v, sigma ~ a0(z)^1/4.")
    print(f"   PREDICTION: {100 * (a0z(2) ** 0.25 - 1):+.0f}% (z=2), {100 * (a0z(4) ** 0.25 - 1):+.0f}% (z=4), "
          f"{100 * (a0z(6) ** 0.25 - 1):+.0f}% (z=6), {100 * (a0z(10) ** 0.25 - 1):+.0f}% (z=10) -- the sigma")
    print("   version is de Graaff's dispersion channel; P1 and P3 are the same declining a0(z).")

    print("\nP4 the RAR knee moves to LOWER acceleration: g_dagger = a0(z) = a0(0)*a0(z)/a0(0).")
    print(f"   PREDICTION: a resolved high-z RAR transitions at g ~ a0(z)*1.2e-10, i.e. x{a0z(6):.2f} lower")
    print("   by z=6. JWST observable: resolved rotation/dispersion profiles at z>4 mapping g_obs vs g_bar.")

    print("\nP5 [CLEAN NULL TEST] a redshift-MIXED RAR/BTFR is intrinsically broadened by")
    print(f"   log10(a0(z_max)/a0(z_min)). A z=2-10 sample spans a0 by {a0z(2)/a0z(10):.1f}x -> "
          f"~{abs(np.log10(a0z(10)/a0z(2))):.2f} dex extra scatter UNLESS each galaxy is scaled by a0(z_gal).")
    print("   PREDICTION: scaling by the declining a0(z) RE-TIGHTENS the relation. Built-in null falsifier.")

    print("\nP6 [REFRAME] high-z dynamical masses are NOT strongly over-inferred (the boost is small).")
    print("   Because a0 DECLINES, the deep-MOND over-inference of M_dyn is WEAKER at high z than locally,")
    print("   so correcting for evolving-a0 MOND removes LESS 'impossible' mass than the rising reading")
    print("   claimed. The 'too-massive-too-early' galaxies are NOT resolved by faithful a0(z).")

    print("\n" + "=" * 86)
    print("HONEST LIMITS  (stated plainly)")
    print("=" * 86)
    print("  * NOT predicted: more stellar mass / faster LINEAR collapse / a boosted halo mass function.")
    print("    a0 is absent from linear perturbations; evolving a0 forms NO galaxies earlier. And the")
    print("    DECLINING a0 of the faithful reading does NOT help the JWST 'too-massive-too-early' tension")
    print("    (an honest non-win -- the boost is weaker early, not stronger).")
    print("  * MAGNITUDES ARE SMALL: the high-z kinematic effects are tens of percent at z>3 and BELOW")
    print("    current per-galaxy scatter at z<=2.5 -- forward predictions, not yet-detectable signals.")
    print("  * DEGENERACY: any single observable can be mimicked by LCDM halo evolution / systematics.")
    print("    The DISCRIMINATOR is the COHERENT, correctly-SIGNED a0(z) scaling across P1-P5 (discs BELOW")
    print("    BTFR, boosts WEAKENING with z) -- one declining a0(z), many channels.")
    print("  * HOSTAGE TO DESI: the whole signature rides on evolving w(z). If w -> -1 (LCDM), a0 stops")
    print("    evolving and these predictions vanish (a0(z)=const). A high-z BTFR that comes back flat or")
    print("    POSITIVE directly falsifies the evolving-a0 bridge.")

    print("\n" + "=" * 86)
    print("  HOW TO TEST IT: measure these at SEVERAL redshifts and check they all key off the SAME")
    print("  declining a0(z). The decisive datum is a clean z>=3 BTFR point: discs ~7% slow (below the")
    print("  z=0 relation) is the framework; flat-or-above falsifies it.")
    print("=" * 86)


if __name__ == "__main__":
    main()
