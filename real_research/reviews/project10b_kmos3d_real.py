#!/usr/bin/env python3
"""
PROJECT 10b: the a0(z) pipeline run on REAL high-z data (KMOS3D / Ubler+2017) -- an honest, deflating result.
============================================================================================================
Project 10 specified the deep-MOND-tail a0(z) pipeline. This file RUNS it on real data: the 135-galaxy
KMOS3D baryonic Tully-Fisher sample (Ubler+2017, z=0.6-2.5), with baryonic masses, circular velocities, and
pressure-support dispersions. The honest finding: raw KMOS3D does NOT show the framework's rising a0. The
sample is massive and often dispersion-supported -- a0=V^4/(G M_bar) is biased HIGH (it rises with mass) and
the galaxies are not in the deep-MOND tail, so this is the WRONG sample to test the prediction. That is
exactly why Project 10 demands deep-MOND-tail selection. Reported straight, not spun. Data:
real_research/data/kmos3d_ubler2017.csv (fetched from Vizier J/ApJ/842/121). Needs numpy.
"""
import numpy as np
import os

G, Msun, Mpc = 6.674e-11, 1.989e30, 3.0857e22
H0 = 67.4e3/Mpc
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
CSV = os.path.join(os.path.dirname(__file__), "..", "data", "kmos3d_ubler2017.csv")


def load():
    d = np.genfromtxt(CSV, delimiter=",", names=True)
    return d["z"], d["logMbar"], d["Vcirc_kms"], d["sigma0_kms"]


def main():
    print("#"*92); print("# PROJECT 10b -- the a0(z) pipeline on REAL data (KMOS3D / Ubler+2017)"); print("#"*92 + "\n")
    z, lMb, V, sig = load()
    a0 = (V*1e3)**4/(G*10**lMb*Msun)
    print(f"  {len(z)} galaxies, z = {z.min():.2f}-{z.max():.2f}. a0 = V_circ^4/(G M_bar) (the deep-MOND BTFR).")
    print(f"  full-sample median a0 = {np.median(a0)*1e10:.2f}e-10  (local SPARC ~1.2e-10) -- already ~4x high.\n")

    print("="*92); print("RED FLAG 1 -- a0 RISES WITH MASS (a high-acceleration bias, not physics)"); print("="*92)
    print(f"  {'logMb':>12}{'N':>4}{'median a0 (1e-10)':>18}")
    for lo, hi in [(9.0, 10.0), (10.0, 10.5), (10.5, 11.0), (11.0, 12.0)]:
        m = (lMb >= lo) & (lMb < hi)
        if m.sum() < 3: continue
        print(f"  {f'{lo}-{hi}':>12}{m.sum():>4}{np.median(a0[m])*1e10:>18.2f}")
    print("""  a0 climbs from ~2 (logMb~9.5) to ~5 (logMb~10.7). A true a0 is universal; this gradient means the
  MASSIVE galaxies (high acceleration, far from the deep-MOND tail) give a BIASED a0=V^4/GM_bar. KMOS3D is a
  massive sample, so its median a0 is dominated by the biased high-mass end.\n""")

    print("="*92); print("RED FLAG 2 -- the z-trend is FLAT-to-DECLINING, NOT the framework's rise"); print("="*92)
    print(f"  {'z-bin':>10}{'N':>4}{'median a0':>11}{'framework pred':>15}")
    bins = [(0.6, 0.9), (0.9, 1.3), (1.3, 1.8), (1.8, 2.7)]
    meds = [np.median(a0[(z >= lo) & (z < hi)]) for lo, hi in bins]
    zc = [(lo+hi)/2 for lo, hi in bins]
    for (lo, hi), md, zz in zip(bins, meds, zc):
        n = ((z >= lo) & (z < hi)).sum()
        print(f"  {f'{lo}-{hi}':>10}{n:>4}{md*1e10:>11.2f}{meds[0]*E(zz)/E(zc[0])*1e10:>15.2f}")
    print("""  the data go 5.8 -> 5.5 -> 4.0 -> 4.0 (flat/declining); the framework (rising as E(z)) predicts
  5.8 -> 7 -> 9 -> 13. The real KMOS3D trend does NOT rise. (It is also ~2x ABOVE the MUSE-DARK z=0.9 point
  the 3-point compilation used -- the high-z a0 estimates DISAGREE at the ~2x level, i.e. systematics dominate.)\n""")

    print("="*92); print("WHY -- and what it means (honest)"); print("="*92)
    print("""  KMOS3D galaxies are massive and often dispersion-supported (V/sigma ~ a few), so:
    * V_circ carries LARGE asymmetric-drift/pressure corrections (the dominant high-z systematic);
    * the galaxies sit at high acceleration (g >~ a0), NOT in the deep-MOND tail where V^4=G M_bar a0 holds;
    * hence a0=V^4/GM_bar is biased and its trend is not a clean a0(z).
  So raw KMOS3D is the WRONG sample to test rising a0, and taken at face value it does NOT support the
  framework -- if anything it leans flat/declining. This is not a refutation of the prediction; it is a
  demonstration that the readily-available massive IFU samples cannot test it, which is EXACTLY why Project 10
  specifies deep-MOND-tail (low-surface-brightness) selection + a per-galaxy gas census. The honest status of
  the empirical case is weaker than the 3-point compilation implied: the real high-z data are systematics-
  dominated and currently INCONCLUSIVE, and the clean test (deep-MOND discs at z~1-3, project 17) is still to be done.\n""")

    print("="*92); print("PROJECT 10b VERDICT"); print("="*92)
    print("""  Running the pipeline on real KMOS3D data is sobering and useful: a0=V^4/GM_bar is ~4x local and rises
  with mass (a high-acceleration bias), and its z-trend is flat-to-declining, NOT the framework's rise. The
  massive, dispersion-supported KMOS3D sample simply cannot measure a0 cleanly. Net: the current real high-z
  data neither confirm nor cleanly refute rising a0 -- they are systematics-dominated and require the deep-
  MOND-tail selection of Project 10 / the dedicated z~3 program of Project 17. Reported as found: the
  empirical case is more open, and more systematics-limited, than the curated 3-point compilation suggested.""")
    print("="*92)


if __name__ == "__main__":
    main()
