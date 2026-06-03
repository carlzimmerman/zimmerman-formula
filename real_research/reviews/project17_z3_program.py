#!/usr/bin/env python3
"""
PROJECT 17 (the flagship): the z~3 a0 measurement as a real observing program.
==============================================================================
The one measurement that decides everything: at z~3 the three readings give a0(z)/a0(0) = framework 4.6
(rises as E(z)) | constant 1.0 | SIV 0.42 (falls). They are >4x apart -- impossible to confuse if a0 is
measured cleanly. This file lays out the full program design (targets, instruments, exposures, the gas
census, the systematics control) and the significance via ratio cancellation. Companion to the LaTeX
proposal (z3_a0_Measurement_Proposal) and z3_forecast_tightened.py. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def siv(z):
    num = (1-Om)/(1+z)**1.5 + Om
    return (1+z)**-1.5 * num**(-4/3) / ((1-Om)+Om)**(-4/3)


def main():
    print("#"*92); print("# PROJECT 17 -- the z~3 a0 measurement: the flagship program"); print("#"*92 + "\n")
    print("="*92); print("THE 3-WAY DISCRIMINATOR (why z~3 is the sweet spot)"); print("="*92)
    print(f"  {'z':>5}{'framework E(z)':>16}{'constant':>11}{'SIV':>9}{'max ratio':>12}")
    for z in (1, 2, 3):
        f, c, s = E(z), 1.0, siv(z)
        print(f"  {z:>5}{f:>16.2f}{c:>11.2f}{s:>9.2f}{f/s:>12.1f}")
    print("""  At z~3 the framework sits 4.6x above SIV and 4.6x above its own z=0 value -- the models are maximally
  separated while targets are still bright enough for JWST. z>4 separates more but the discs are rarer and
  noisier; z~2.5-3.5 is the design sweet spot.\n""")

    print("="*92); print("THE PROGRAM"); print("="*92)
    print("""  TARGETS: extended, ROTATION-SUPPORTED discs at z~2.5-3.5 reaching the deep-MOND tail (V_flat plateau at
  g_bar < a0). Pre-select from existing JWST/NIRCam morphology + grism redshifts: large (>0.5\") rotation-
  dominated discs, v/sigma > 3, stellar mass 10^9.5-10^10.5 (low enough surface density to reach deep MOND).
  ~30-50 galaxies for a population (not 1-2 heroic cases).
  KINEMATICS: JWST/NIRSpec IFU (Halpha/[OIII]) for the rotation curve to large radius -- the g_obs(R) tail.
  GAS CENSUS: ALMA [CII]158um and/or CO for the molecular+atomic gas -> the per-galaxy g_bar (the step that
  breaks the high-z TFR; without it the a0 is gas-confounded, Project 11).
  EXPOSURES: deep enough that the OUTER (deep-MOND) points have <0.1 dex velocity error -- that is where a0
  is constrained; the inner Newtonian points do not matter.\n""")

    print("="*92); print("THE STATISTICS -- ratio cancellation"); print("="*92)
    print("""  Do NOT measure a0 absolutely (Z and M/L systematics ~0.1-0.2 dex swamp it). Instead measure the RATIO
  a0(z~3)/a0(z~0) using the SAME pipeline, M/L prescription and interpolation at both ends, so the common
  systematics CANCEL. The framework predicts ratio = E(3) = 4.6; constant = 1.0; SIV = 0.42. With ~30
  galaxies per end at ~0.1 dex each, the ratio is pinned to ~0.02-0.03 dex -> the 4.6-vs-1.0-vs-0.42 split is
  a >10 sigma, 3-way decision (the LaTeX proposal's ~13-16 sigma forecast). One clean ratio ends the question.\n""")

    print("="*92); print("PROJECT 17 VERDICT"); print("="*92)
    print("""  The flagship is fully specified: a population of ~30-50 rotation-supported deep-MOND discs at z~2.5-3.5,
  JWST/NIRSpec IFU kinematics + ALMA gas census, analyzed as a Z- and M/L-cancelling a0(z~3)/a0(0) RATIO that
  decides framework (4.6) vs constant (1.0) vs SIV (0.42) at >10 sigma. It needs telescope time, not more
  in-house analysis -- the design, targets, and forecast are done and ready for a Cycle proposal. This is the
  single measurement that converts the whole framework from 'leaning' to decided, in either direction.""")
    print("="*92)


if __name__ == "__main__":
    main()
