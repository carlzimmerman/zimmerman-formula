#!/usr/bin/env python3
"""
BTFR slope + scatter on the real SPARC master table — ODR (unbiased), both footings.
====================================================================================

Independent cross-check for THE_HONEST_LCDM_STRESS_BRIEF.md Part I (the BTFR arrow).
Banks the number the workflow flagged as run-inline-but-not-committed: the
baryonic Tully-Fisher slope with PROPER cuts (quality Q<=2, Vflat>30, inclination>30)
and the statistically-correct ODR/orthogonal regression (a naive forward M-on-V fit
is attenuated by V-scatter and gives a biased-shallow slope ~3.4 — an artifact, NOT
a framework loss; this script shows the unbiased slope lands near 4 at Upsilon=0.70).

Data: real_research/data/sparc_master_clean.csv (Lelli+2016 SPARC master table:
name,T,D_Mpc,fD,inc,L36,MHI,Vflat,Q,ref). M_bar = Upsilon*L36*1e9 + 1.33*MHI*1e9
(1.33 = helium correction). Deep-MOND BTFR predicts V_flat^4 = G M_bar a0 (slope exactly 4).

Run:  python reviews/btfr_slope_odr_bothways.py     (needs numpy, scipy)
"""

import csv, math, os
import numpy as np
from scipy import odr

G = 6.674e-11; Msun = 1.989e30; kms = 1e3
CSV = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_master_clean.csv")


def load():
    rows = []
    with open(CSV) as f:
        for r in csv.DictReader(f):
            try:
                L36 = float(r["L36"]); MHI = float(r["MHI"])
                Vf = float(r["Vflat"]); Q = int(r["Q"]); inc = float(r["inc"])
            except (ValueError, KeyError):
                continue
            rows.append((r["name"], L36, MHI, Vf, Q, inc))
    return rows


def sample(rows, ml, qmax=2, vmin=30, imin=30):
    """Proper BTFR cuts: quality Q<=2, real flat velocity Vflat>30, inclination>30 deg."""
    logM, logV, a0s = [], [], []
    for name, L36, MHI, Vf, Q, inc in rows:
        if Q > qmax or Vf <= vmin or inc < imin:
            continue
        Mbar = ml * L36 * 1e9 + 1.33 * MHI * 1e9      # solar masses
        if Mbar <= 0:
            continue
        logM.append(math.log10(Mbar)); logV.append(math.log10(Vf))
        a0s.append((Vf * kms) ** 4 / (G * Mbar * Msun))  # deep-MOND a0 = Vf^4/(G Mbar)
    return np.array(logV), np.array(logM), np.array(a0s)


def slopes(logV, logM):
    af, _ = np.polyfit(logV, logM, 1)                    # forward M-on-V (attenuated)
    av, _ = np.polyfit(logM, logV, 1); ainv = 1.0 / av   # inverse V-on-M, inverted (steepened)
    lin = lambda B, x: B[0] * x + B[1]
    out = odr.ODR(odr.RealData(logV, logM), odr.Model(lin),
                  beta0=[4.0, np.median(logM) - 4 * np.median(logV)]).run()
    aodr = out.beta[0]                                   # ODR/orthogonal (unbiased)
    b4 = np.median(logM - 4 * logV)
    scat4 = float(np.std(logM - (4 * logV + b4)))        # vertical scatter at fixed slope=4
    return af, ainv, aodr, scat4


def main():
    rows = load()
    print("=" * 76)
    print("BTFR slope + scatter on real SPARC (Q<=2, Vflat>30, inc>30) — ODR, both footings")
    print("=" * 76)
    for ml, tag in [(0.5, "McGaugh standard"), (0.7, "framework")]:
        lV, lM, a0s = sample(rows, ml)
        af, ainv, aodr, scat4 = slopes(lV, lM)
        print(f"--- Upsilon_disk = {ml} ({tag}) ---  N = {len(lV)} galaxies")
        print(f"    forward slope (M-on-V, attenuated)  : {af:.2f}")
        print(f"    inverse slope (V-on-M, inverted)    : {ainv:.2f}")
        print(f"    ODR/orthogonal slope (UNBIASED)     : {aodr:.2f}   <- the correct one")
        print(f"    scatter at fixed slope=4            : {scat4:.4f} dex")
        print(f"    BTFR-implied a0 (median)            : {np.median(a0s):.3e} m/s^2")
        print()
    print("Reference: Lelli+2019 (referee-grade BTFR sample) slope 3.85+-0.09, scatter 0.10 dex.")
    print("Both-ways read: slope-4 is bracketed only at Upsilon=0.70 (ODR 3.87); at the standard")
    print("  Upsilon=0.50 the ODR slope is 3.73 (excludes 4.0). The ~0.10-dex scatter IS a published")
    print("  LCDM tension (Wheeler/Trujillo-Gomez 2015), but Ferrero/Sales 2017 reproduce the bright-end")
    print("  slope in EAGLE/APOSTLE -> CONTESTED, not a kill; and the BTFR-implied a0 (~1.3-1.5e-10)")
    print("  DISPREFERS the framework's own 9.36e-11. Non-diagnostic on the framework's own terms.")


if __name__ == "__main__":
    main()
