#!/usr/bin/env python3
"""
TIGHTENED z=3 forecast for the evolving-a0 test -- a more defensible error budget.
=================================================================================
The published z~3 proposal caps the constant-a0 rejection near 7 sigma, limited by the z=0 anchor's
mass-to-light systematic (sigma_A ~ 0.09 dex). This script tightens that, rigorously, using the
session's own anchor results -- and by making explicit that the TEST IS ON THE RATIO a0(z=3)/a0(0),
so systematics COMMON to both epochs cancel. Three insights, each reproducible:

  I1  a0 read from DEEP-MOND points (g_bar < a0) is interpolation-function-INDEPENDENT -- in the deep
      limit every interpolation agrees, g_obs -> sqrt(g_bar a0). This REMOVES the ~0.12 dex
      function ambiguity (McGaugh a0=1.36 vs algebraic 1.78 at z=0, both verified this session).
  I2  GAS-DOMINATED deep-MOND points give an M/L-robust a0 (~10% swing vs ~75% for star-dominated,
      sparc_anchor_universality.py) -> sigma_A(M/L) ~ log10(1.10) = 0.04 dex.
  I3  the RATIO cancels COMMON systematics; only the DIFFERENTIAL (evolving) M/L survives -> budget
      ~0.03-0.05 dex with consistent SED modeling at both epochs.

Net: the plateau rises from ~7 sigma to ~13-16 sigma, and 15 galaxies from ~7 to ~11 sigma. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E3 = np.sqrt(Om*(1+3)**3 + OL)
DELTA = np.log10(E3)                          # the signal, log10 E(3)
SIG_GAL = 0.15                                # per-galaxy a0 uncertainty at z=3 (dex), from the proposal


def sigma_rej(N, sigma_A):
    return DELTA / np.sqrt((SIG_GAL/np.sqrt(N))**2 + sigma_A**2)


def main():
    print("="*86)
    print(f"TIGHTENED z=3 FORECAST  (signal Delta = log10 E(3) = {DELTA:.3f} dex; sigma_gal = {SIG_GAL} dex)")
    print("="*86)
    print("""  WHY a tighter anchor is justified (the test is on the RATIO a0(z=3)/a0(0), same pipeline both ends):
    I1  use DEEP-MOND points -> a0 is interpolation-function-INDEPENDENT (removes ~0.12 dex ambiguity);
    I2  use GAS-DOMINATED systems -> M/L-robust a0, sigma_A(M/L) ~ 0.04 dex (vs 0.09 all-points);
    I3  the ratio cancels common systematics -> only DIFFERENTIAL M/L survives (~0.03-0.05 dex).
  So a defensible tightened anchor is sigma_A ~ 0.04-0.05 dex (vs the current 0.09).\n""")
    print(f"  {'N gal':>6}{'current (sA=0.09)':>20}{'tightened (sA=0.05)':>22}{'best (sA=0.04)':>17}")
    for N in (10, 15, 25, 50, 100):
        print(f"  {N:>6}{sigma_rej(N,0.09):>17.1f} s{sigma_rej(N,0.05):>19.1f} s{sigma_rej(N,0.04):>14.1f} s")
    print(f"\n  plateau (N->inf):  current {DELTA/0.09:.1f} sigma  ->  tightened {DELTA/0.05:.1f}-{DELTA/0.04:.1f} sigma")
    print("""
  READING IT: the published proposal's ~7 sigma plateau is set by treating the z=0 anchor as an
  ABSOLUTE a0 with the full M/L systematic. But the evolution test only needs the RATIO, and a0 from
  deep-MOND gas-dominated points is both function-independent (I1) and M/L-robust (I2); the common
  part cancels in the ratio (I3). The residual is the DIFFERENTIAL M/L between epochs -- real, but
  controllable to ~0.04-0.05 dex with consistent SED modeling and gas-traced rotation (ALMA [CII]/CO)
  at z=3. That lifts the decisive significance from ~7 sigma to ~13-16 sigma at fixed sample size, and
  makes even ~10-15 galaxies a >10 sigma test of evolution. NONE of this changes the Tier-1 caveat
  (LCDM can mimic an evolving APPARENT a0 via halo evolution); it only makes the evolution measurement
  itself robust. The distinctive test remains Tier 2 (the EFE, eta ~ 1/E(z)).""")
    print("="*86)
    print("HONEST RESIDUALS (do not skip):")
    print("""  * differential M/L (younger high-z populations -> lower M/L) is the dominant non-cancelling
    systematic; budgeted at 0.03-0.05 dex, it must be MEASURED (consistent SED + gas) not assumed.
  * pressure support: high-z discs have V/sigma ~ 3-10; the asymmetric-drift correction is a real
    per-galaxy systematic folded into sigma_gal=0.15 dex (and the reason rotation-supported, V/sigma>3,
    extended discs are the required sample -- not compact dispersion-dominated systems).
  * the gain is in the ANCHOR (sigma_A), so it saturates: beyond sigma_A~0.04 dex other systematics
    (distance ladder, abundance matching of the baryon census) would dominate. ~13-16 sigma is the
    realistic ceiling, not a path to arbitrary significance.""")
    print("="*86)


if __name__ == "__main__":
    main()
