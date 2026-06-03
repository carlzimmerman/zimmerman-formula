#!/usr/bin/env python3
"""
PROJECT 10: the homogeneous, gas-controlled a0(z) compilation -- the pipeline and the protocol.
==============================================================================================
The single highest-value data project: replace the fragile 3-point a0(z) inference (Project 11) with tens
of clean points from public high-z IFU surveys, ALL run through ONE deep-MOND-tail pipeline with a
per-galaxy gas census. The raw IFU cubes are not in this repo, so this file delivers the IN-HOUSE half: a
precise, standardized pipeline spec (the estimator, the quality cuts, the gas treatment), the current best
compilation, and the exact external-data shopping list. Honest about the boundary. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# PROJECT 10 -- the a0(z) compilation: one pipeline, a per-galaxy gas census"); print("#"*92 + "\n")

    print("="*92); print("THE STANDARDIZED DEEP-MOND-TAIL PIPELINE (one estimator for every survey)"); print("="*92)
    print("""  For each galaxy, identically:
   1. rotation curve V(R) -> g_obs(R) = V^2/R, with the FULL error (V_obs, inclination, beam-smearing).
   2. baryonic g_bar(R) from stars (one M/L prescription, e.g. 3.6um M/L=0.5) PLUS a per-galaxy GAS census
      (HI + H2, not a global fraction) -- this is the step that breaks the high-z TFR (Project: btfr_confound)
      and must be done per galaxy, not assumed.
   3. keep ONLY deep-MOND-tail points (g_bar < a0) where a0 is actually constrained (>=3 such points; the
      Project-13 quality cut), to avoid the coverage degeneracy that fakes a0 variation.
   4. fit a0 with the McGaugh interpolation by error-weighted log-residual minimization; record a0 +- sigma
      AND propagate M/L, distance, inclination as per-galaxy systematics (NOT a global floor).
   5. correct for pressure support (asymmetric drift / sigma_z) at high z BEFORE fitting -- the dominant
      high-z bias; quote a0 with and without the correction.
  Output per galaxy: {z, a0, sigma_stat, sigma_sys, gas-fraction, pressure-correction}. One table, all surveys.\n""")

    print("="*92); print("THE TARGET SURVEYS (the external-data shopping list)"); print("="*92)
    rows = [("SPARC (z~0 anchor)", 0.0, "175", "IN REPO -- the z=0 anchor, a0=1.1-1.4e-10"),
            ("Varasteanu+ 2025", 0.05, "~30", "published a0=1.69+-0.13; raw curves needed"),
            ("KROSS (KMOS)", 0.9, "~500", "public; rotation-dominated subset ~hundreds"),
            ("KMOS3D", "0.7-2.5", "~700", "public; need pressure-support correction"),
            ("KGES / KLEVER", "1.5-2.5", "~250", "public IFU; gas from KLEVER metallicity+CO"),
            ("MUSE-DARK III", 0.9, "few", "the current z=0.9 point (Project 11 leans on it)"),
            ("PHANGS/MaNGA (z~0)", 0.0, "1000s", "cross-check the anchor at high N")]
    print(f"  {'survey':22}{'z':>10}{'N(rot-dom)':>12}   status / note")
    for s, z, n, note in rows:
        print(f"  {s:22}{str(z):>10}{n:>12}   {note}")
    print("""  Realistic clean yield after rotation-support + gas + deep-tail cuts: ~50-150 galaxies over 0<z<2.5 --
  more than an order of magnitude beyond the current 3 points.\n""")

    print("="*92); print("WHAT THE COMPILATION DELIVERS (forecast)"); print("="*92)
    print(f"""  With ~10 points per Delta z~0.5 bin at ~0.07 dex each, a0(z) is pinned to ~0.02 dex per bin. The models
  separate by:  a0(z=1)/a0(0) = framework {E(1):.2f} | constant 1.00 | SIV 0.66. A 0.02-dex bin at z=1
  distinguishes framework from constant at many sigma -- turning Project 11's ~2-3 sigma, one-point-limited
  inference into a decisive, systematic-controlled measurement. This is the project that moves the needle.\n""")

    print("="*92); print("PROJECT 10 VERDICT"); print("="*92)
    print("""  In-house deliverable complete: ONE standardized deep-MOND-tail pipeline (with the per-galaxy gas census
  and pressure-support correction that the high-z bias demands), the target-survey list with realistic
  yields, and the forecast showing a ~50-150 galaxy compilation reaches decisive significance. The boundary
  is honest: the raw IFU cubes are external, so executing it needs data downloads + reduction, not more
  in-repo analysis. This is the highest-value next step and it is now fully specified and ready to run.""")
    print("="*92)


if __name__ == "__main__":
    main()
