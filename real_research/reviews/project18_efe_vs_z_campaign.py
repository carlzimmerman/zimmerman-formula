#!/usr/bin/env python3
"""
PROJECT 18: the EFE-vs-z campaign -- the costlier, doubly-forbidden Tier-2 test.
================================================================================
Project 12 showed the framework predicts the External Field Effect WEAKENS with redshift as eta ~ 1/E(z)
(because a0 rises). In LambdaCDM the EFE does not exist at ANY z (SEP holds), so BOTH its presence and any
z-trend are forbidden -- a doubly-distinctive signature. But measuring an EFE at high z is hard: it needs
environment-resolved galaxies in the deep-MOND tail with known external fields. This file designs the staged
program and states honestly why it is Tier-2 (costlier, later) than the z~3 a0 ratio (#17). Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# PROJECT 18 -- the EFE-vs-z campaign"); print("#"*92 + "\n")
    print("="*92); print("THE SIGNAL"); print("="*92)
    print(f"  {'z':>5}{'a0(z)/a0':>11}{'eta/eta_0 = 1/E(z)':>22}{'EFE downturn shift':>22}")
    for z in (0.0, 0.5, 1.0, 2.0):
        print(f"  {z:>5.1f}{E(z):>11.2f}{1/E(z):>22.3f}{'-'+str(round(np.log10(E(z)),2))+' dex in g_bar':>22}")
    print("""  As a0 rises, a FIXED external field g_ext becomes a smaller fraction of a0, so the EFE downturn in the
  RAR (Project 12) both SHRINKS (depth ~1/E(z)) and MOVES to lower g_bar (by E(z)). LambdaCDM predicts a flat
  zero at every z. Detecting the trend is the test.\n""")

    print("="*92); print("THE STAGED PROGRAM"); print("="*92)
    print("""  STAGE 1 (z~0.3-0.7, existing+near-term): extend the SPARC-style EFE detection (Project 12) to
  intermediate z with KMOS/MUSE rotation curves, using photometric-redshift density fields for g_ext. Goal:
  confirm the EFE still appears and begin constraining its amplitude vs z.
  STAGE 2 (z~1-2, JWST): environment-resolved deep-MOND discs (a subset of the Project-17 sample) WITH a
  reconstructed local density field (needs a spectroscopic redshift survey around each target). Measure the
  residual-vs-g_ext slope per z-bin.
  STAGE 3 (z>=4, costly): the regime where 1/E(z) is most suppressed -- requires ~600-1600 galaxies with both
  deep-MOND kinematics AND environment reconstruction, a multi-facility (JWST+ALMA+wide spectroscopy) effort.
  This is why it is Tier-2: the environment reconstruction at high z is the expensive part.\n""")

    print("="*92); print("PROJECT 18 VERDICT"); print("="*92)
    print("""  The EFE-vs-z trend (eta ~ 1/E(z)) is a doubly-forbidden LambdaCDM signature and an independent
  confirmation channel for rising a0 -- but it is COSTLIER than the z~3 ratio (#17) because it needs per-
  galaxy environments, not just kinematics. Correct sequencing: do #17 first (cheaper, decisive on rising-vs-
  constant), then stage the EFE-vs-z program as the confirning Tier-2 test. Designed and ranked honestly; not
  the first move, but a real one once #17 lands.""")
    print("="*92)


if __name__ == "__main__":
    main()
