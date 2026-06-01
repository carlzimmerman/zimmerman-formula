#!/usr/bin/env python3
"""
Custom quasar/galaxy GHOST calculation for the 20.6 Gpc T^3 box -- and what the
existing data already says.
==============================================================================

Carl's idea (correct method!): if the universe is a T^3 box of edge L_c = 20.6
Gpc, distant objects have topological ghost images (light wrapping the box). So
look in existing catalogs for the ghosts. This script does the custom geometry
with STANDARD LCDM and shows three things:

  (1) WHERE the nearest ghost falls. For an object at comoving distance D1 along
      the line of sight, the nearest lattice-translate image is at
      D2 = L_c - D1 in the ANTIPODAL direction (RA+180, Dec->-Dec). (This is the
      BEST case -- the closest possible ghost; off-axis objects ghost farther.)

  (2) THE LOOK-BACK CATCH -- why discrete-object ghosts are hard. We see the
      object at redshift z1 = z(D1) but its ghost at z2 = z(D2). When D2 > D1 the
      ghost shows the SAME object at an EARLIER epoch -- often before it (or any
      galaxy) existed. The two images are at different cosmic times.

  (3) THE SWEET SPOT. Only at D1 = D2 = L_c/2 (=10.3 Gpc) are z1 = z2, so both
      images show the same epoch and are matchable. That sits at one specific
      redshift z* -- the only clean window for direct ghosts.

Then the punchline: this test has ALREADY been run on existing data -- by the
repo's own ghost hunter (research/digital_twin/ghost_miner.py -> null) AND, far
more sensitively, by Planck's CMB matched circles (the same ghost test at the
last-scattering surface, millions of pixels, a single epoch in all directions),
which EXCLUDE L_c = 20.6 Gpc (matched_circle_*_verification.py).

Pure stdlib + numpy. Run:  python reviews/quasar_ghost_custom.py
"""

import numpy as np

C = 299792.458          # km/s
H0 = 67.4               # km/s/Mpc  (Planck)
OM, OR = 0.315, 9.1e-5
OL = 1 - OM - OR
L_C = 20.6              # Gpc, the framework's cubic edge

# --- standard LCDM comoving distance D(z) and its inverse z(D), in Gpc -------
_zg = np.linspace(0.0, 1100.0, 400001)
_invE = 1.0 / np.sqrt(OR * (1 + _zg) ** 4 + OM * (1 + _zg) ** 3 + OL)
_Dc = np.concatenate([[0.0], np.cumsum((_invE[1:] + _invE[:-1]) / 2 * np.diff(_zg))])
_Dc *= (C / H0) / 1e3   # Mpc -> Gpc
D_LSS = float(_Dc[-1])


def D_of_z(z):
    return float(np.interp(z, _zg, _Dc))


def z_of_D(D):
    return float(np.interp(D, _Dc, _zg))


# Epoch landmarks (comoving, for "is the ghost observable?")
Z_REION = 6.0           # below: reionized, galaxies common
Z_FIRST = 30.0          # above: cosmic dark ages, no luminous sources yet


def observability(z2):
    if z2 >= Z_FIRST:
        return "DARK AGES -- no luminous sources existed (ghost is blank)"
    if z2 >= 15.0:
        return "beyond the JWST galaxy frontier (z~14)"
    return "in principle JWST-observable"


# Real high-z objects (name, redshift)
OBJECTS = [
    ("SDSS J1030+0524  (quasar)", 6.31),
    ("ULAS J1120+0641  (quasar)", 7.09),
    ("J0313-1806       (quasar)", 7.64),
    ("GN-z11           (galaxy)", 10.60),
    ("GLASS-z12        (galaxy)", 12.34),
    ("JADES-GS-z14-0   (galaxy)", 14.32),
]


def main():
    print("=" * 80)
    print("(1) The geometry -- comoving distances under standard LCDM")
    print("=" * 80)
    print(f"   H0={H0}, Om={OM}, OL={OL:.3f}")
    print(f"   comoving distance to last scattering  : {D_LSS:.2f} Gpc")
    print(f"   box edge L_c                          : {L_C} Gpc")
    print(f"   nearest-ghost rule: D2 = L_c - D1, antipodal (RA+180, Dec->-Dec)")
    print(f"   (this is the CLOSEST possible ghost; off-axis objects ghost farther.)\n")

    print("=" * 80)
    print("(2) Where the ghosts fall -- and the look-back catch")
    print("=" * 80)
    print(f"   {'object':<28}{'z1':>6}{'D1':>7}{'D2':>7}{'z2(ghost)':>11}  observability")
    for name, z1 in OBJECTS:
        D1 = D_of_z(z1)
        D2 = L_C - D1
        if D2 <= 0:
            print(f"   {name:<28}{z1:>6.2f}{D1:>7.2f}{D2:>7.2f}{'--':>11}  object beyond L_c")
            continue
        if D2 >= D_LSS:
            print(f"   {name:<28}{z1:>6.2f}{D1:>7.2f}{D2:>7.2f}{'>z_rec':>11}  ghost behind last scattering")
            continue
        z2 = z_of_D(D2)
        print(f"   {name:<28}{z1:>6.2f}{D1:>7.2f}{D2:>7.2f}{z2:>11.1f}  {observability(z2)}")
    print()
    print("   The ghost redshift z2 is pushed HIGH: a z~6-8 quasar ghosts into the")
    print("   dark ages (z2 ~ 30-60), where it predates all galaxies -- so the ghost")
    print("   is blank. This is the real reason discrete-object ghosts are hard, and")
    print("   why the framework's own ghost_miner.py predicted a z=46 ghost for")
    print("   GLASS-z12 (its nonstandard expansion law inflates it further still).\n")

    print("=" * 80)
    print("(3) The sweet spot -- the only clean window for a direct ghost")
    print("=" * 80)
    D_half = L_C / 2.0
    z_star = z_of_D(D_half)
    print(f"   z1 = z2 only when D1 = D2 = L_c/2 = {D_half:.2f} Gpc")
    print(f"   that single redshift is  z* = {z_star:.1f}")
    print(f"   Only objects near z~{z_star:.0f} have a ghost at the SAME epoch (also z~{z_star:.0f},")
    print("   antipodal) -- matchable in principle. That window sits right at the")
    print("   JWST high-z frontier we are only now reaching. Even there, the two")
    print("   images view OPPOSITE sides of the object across a light-path difference,")
    print("   so confirmation needs spectral/morphological ID -- hard, but doable.\n")

    print("=" * 80)
    print("(4) What the existing data already says")
    print("=" * 80)
    print("   * The repo's OWN ghost hunter (research/digital_twin/ghost_miner.py)")
    print("     searched JWST (GLASS/JADES/CEERS), SDSS and MAST for these antipodal")
    print("     pairs and found NONE (ghost_predictions.json / *_ghost_*results.json).")
    print("   * Planck's CMB matched circles ARE this same ghost test, but performed")
    print("     at the last-scattering surface -- which exists at ONE cosmic epoch in")
    print("     EVERY direction (no look-back mismatch) and gives millions of pixels")
    print("     instead of a handful of z~13 galaxies. That is the most sensitive ghost")
    print("     search possible, and it finds nothing AND excludes L_c = 20.6 Gpc by a")
    print("     wide margin (matched_circle_planck_verification.py: R_i = 0.74 chi_rec")
    print("     vs the required > 0.97; 42 deg circles vs a 15 deg floor).")
    print()

    print("=" * 80)
    print("VERDICT -- your method is right; the data has already answered it")
    print("=" * 80)
    print("  * Looking for ghosts in existing data is exactly the correct test, and it")
    print("    HAS been done -- directly (quasar/galaxy catalogs, null) and, far more")
    print("    powerfully, in the CMB (matched circles, null + exclusion).")
    print("  * Direct discrete-object ghosts are intrinsically weak: the wrapped image")
    print(f"    shows the object at a different (usually pre-galactic) epoch; only a thin")
    print(f"    window at z~{z_star:.0f} gives same-epoch antipodal pairs, and none are seen.")
    print("  * The CMB already forecloses the box, so no quasar-ghost survey can revive")
    print("    a 20.6 Gpc T^3. (And none of this touches the surviving physics: the")
    print("    evolving-a0 prediction needs no cosmic topology at all.)")


if __name__ == "__main__":
    main()
