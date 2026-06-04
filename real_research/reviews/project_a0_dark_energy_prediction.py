#!/usr/bin/env python3
"""
THE BREAKTHROUGH PREDICTION (done right): a0 is the dark-energy scale, so DESI's w(z) FIXES a0(z).
=================================================================================================
The session's novel, defensible claim: a0 is the de Sitter EVENT-horizon surface gravity, a0 ~ c sqrt(Lambda/3)
~ c sqrt(rho_DE) (derived: the DSSYK dual is the de Sitter static patch = the event horizon, NOT the apparent
horizon). That UNIFIES the two dark sectors -- dark matter (as MOND) and dark energy are one scale, set by the
cosmological horizon. The sharp, falsifiable consequence: a0 tracks the dark-energy density, so

    a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE(0) ),    with rho_DE(z) MEASURED by DESI.

No free galaxy-scale parameter. Galaxy dynamics becomes a dark-energy probe, and vice versa. This script
propagates the DESI DR2 w0-wa posterior to the a0(z) prediction with a 68% band, contrasts it with the two
alternatives (constant a0; apparent-horizon rising a0 ~ E(z)), and forecasts the measurement that decides it.

RESULT: the event-horizon/DESI branch predicts a MILD DECLINE -- a0(z)/a0(0) ~ 0.99 (z=1), 0.87 (z=2), 0.77
(z=3) -- distinct from constant only at z>~2 (a few-% measurement) but VERY distinct from rising (already
disfavored by the high-z disks). So the prediction is consistent with all current direct data and decided by a
~5% a0 measurement at z~2-3.

HONEST CAVEATS (loud, this is the part that keeps it real):
  (1) NORMALIZATION. The parameter-free a0(0) = c H0 sqrt(OmegaLambda)/Z (Z=2sqrt(8pi/3)) = 0.93e-10 is ~22%
      BELOW the observed 1.2e-10 (the apparent-horizon c H0/Z = 1.12e-10 is closer, ~7% low). So the absolute
      value is so-so; the breakthrough claim is the a0(z) SHAPE (dark-energy tracking), not the normalization.
  (2) THE WALL. The whole construction rests on Narovlansky-Verlinde (de Sitter = the DSSYK center) -- the one
      unsettled input (project_the_wall.py). a0 ~ sqrt(rho_DE) also assumes the EVENT-horizon reading (derived
      from the dual, but the apparent reading is the emergent-gravity tradition).
  (3) DESI ITSELF. The evolving-DE signal is 2.8-4.2 sigma and could revert to Lambda (then a0 = constant).
So: a NOVEL, FALSIFIABLE unification with a parameter-free a0(z) prediction -- presented as a research program
with its single assumption (N-V) and its normalization tension named, not as a finished result. Needs numpy.
"""
import numpy as np

Om = 0.315
c = 2.998e8; G = 6.674e-11; H0 = 67e3/3.086e22; OL = 0.685
Z = 2*np.sqrt(8*np.pi/3)
E = lambda z: np.sqrt(Om*(1+z)**3 + (1-Om))


def rho_de(z, w0, wa):
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))


def main():
    print("#"*92)
    print("# a0 IS THE DARK-ENERGY SCALE -- DESI's w(z) fixes a0(z) (the breakthrough prediction, done right)")
    print("#"*92 + "\n")
    rng = np.random.RandomState(7)
    w0c, wac, sw0, swa, corr = -0.83, -0.65, 0.06, 0.25, -0.8
    cov = np.array([[sw0**2, corr*sw0*swa], [corr*sw0*swa, swa**2]])
    draws = rng.multivariate_normal([w0c, wac], cov, size=20000)

    print("="*92); print("THE PREDICTION: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)), rho_DE(z) from the DESI posterior"); print("="*92)
    print(f"  DESI DR2+SNe w0waCDM (representative): w0 = {w0c}+-{sw0}, wa = {wac}+-{swa} (anticorrelated rho={corr})")
    print(f"  {'z':>5}{'EVENT ~sqrt(rhoDE) [DESI]':>28}{'constant':>11}{'apparent ~E(z)':>16}")
    for z in (0.5, 1.0, 1.5, 2.0, 3.0):
        r = np.sqrt(np.array([rho_de(z, w0, wa) for w0, wa in draws]))
        lo, md, hi = np.percentile(r, [16, 50, 84])
        print(f"  {z:>5.1f}{md:>17.3f} (+{hi-md:.2f}/-{md-lo:.2f}){1.00:>11.2f}{E(z):>16.2f}")
    print()

    print("="*92); print("THE DECISIVE TEST: a0(z) precision to separate the three readings"); print("="*92)
    for z in (1.0, 2.0, 3.0):
        r = np.sqrt(np.array([rho_de(z, w0, wa) for w0, wa in draws]))
        md = np.median(r)
        print(f"  z={z}: event {md:.2f}  vs constant 1.00 (gap {abs(1-md):.2f})  vs rising {E(z):.2f} (gap {abs(E(z)-md):.2f})"
              f"  -> need sigma_a0/a0 < {abs(1-md)/3:.2f} to beat constant")
    print("""  => event vs RISING is already decided (huge gap; high-z disks favor non-rising). event vs CONSTANT needs
     a ~5% a0 measurement at z~2-3 (the gap grows with z as dark energy fades). A gas-clean z~2-3 disk SAMPLE
     -- or an extension of MUSE-DARK-style RAR fits to z~2 -- is the experiment.\n""")

    print("="*92); print("HONEST NORMALIZATION CHECK & THE SINGLE ASSUMPTION"); print("="*92)
    print(f"  parameter-free a0(0): event c H0 sqrt(OL)/Z = {c*H0*np.sqrt(OL)/Z/1e-10:.2f}e-10 (~22% low);"
          f" apparent c H0/Z = {c*H0/Z/1e-10:.2f}e-10 (~7% low) vs obs 1.2+-0.26.")
    print("  The normalization mildly favors apparent; the EVOLUTION favors event. The breakthrough is the SHAPE.")
    print("  Single assumption: Narovlansky-Verlinde (de Sitter = DSSYK center) -- the wall. DESI evolving-DE is")
    print("  2.8-4.2 sigma (could revert to Lambda -> a0 constant).\n")

    print("="*92); print("VERDICT -- a novel, falsifiable unification (not a finished result)"); print("="*92)
    print("""  The claim: a0 is the de Sitter event-horizon scale, so the MOND acceleration and the cosmological constant
  are ONE scale -- dark matter (as MOND) and dark energy unified through a0 ~ c sqrt(Lambda/3). The derivation
  chain is largely done (sign + sqrt-law + interpolation + a0~c sqrt(Lambda) order + event-horizon evolution +
  Z=Friedmann), resting on the single open proposition de Sitter = the DSSYK center. The novel, parameter-free,
  falsifiable consequence: a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE(0)), FIXED by DESI -- galaxy dynamics is a dark-
  energy probe. Current data are consistent (the predicted mild decline matches the high-z disks that ruled out
  the rising bet). A ~5% a0 measurement at z~2-3 turns it into a discovery or a refutation. Reported as a
  research program with its one assumption (N-V) and its ~22% normalization tension named -- the honest form of
  a breakthrough, not a press release.""")
    print("="*92)


if __name__ == "__main__":
    main()
