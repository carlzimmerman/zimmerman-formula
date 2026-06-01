#!/usr/bin/env python3
"""
a0(z) test pipeline -- the one surviving prediction, tested honestly.
=====================================================================

The surviving claim of the whole program is a0(z)/a0(0) = E(z): the MOND
acceleration scale rises with the Hubble rate. This pipeline tests it WITHOUT the
trick that invalidated examples/07 (which fit galaxy-by-galaxy via sqrt(a0/g), a
quantity monotonic in a0, so a larger a0(z) "always wins"). Instead it measures a
single robust observable -- the BAR Tully-Fisher ZERO-POINT as a function of
redshift -- and compares its SHAPE to three parameter-free hypotheses.

Deep-MOND BTFR:   V_flat^4 = G * M_bar * a0(z)
  => log M_bar = 4 log V_flat + b(z),   b(z) = -log10(G a0(z)) + const.
So the zero-point shift relative to the lowest-z bin is

    db(z) = -log10[ a0(z) / a0(z_anchor) ].

Three parameter-free predictions for db(z) (NO free knobs, NO per-galaxy fit):
    H0  constant a0 (standard MOND, the NULL):  db = 0
    H1  a0 ~ H(z) total density   (E(z)):       db = -log10 E(z)
    H2  a0 ~ matter free-fall ((1+z)^1.5):      db = -1.5 log10(1+z)

H1 vs H2 is the Schwarzschild density fork (real_research/FRAMEWORK.md). The test
is a straight chi^2 of the MEASURED zero-point shifts against these three curves --
self-anchored on the lowest-z bin, so absolute calibration cancels and there is no
monotonicity rigging.

USAGE
  python a0_evolution_pipeline.py                 # show predictions + data schema
  python a0_evolution_pipeline.py --selftest      # verify the estimator (injected signal)
  python a0_evolution_pipeline.py --data FILE.csv # run the real test

INPUT SCHEMA (CSV header, one row per galaxy with a FLAT-rotation-curve measurement):
  id, z, logMbar, e_logMbar, logVflat, e_logVflat
  (M_bar in Msun = M_star + 1.33 M_HI; V_flat in km/s = the asymptotic flat speed,
   NOT v at 2Re. Require deep-MOND systems: g = V_flat^2/R_flat <~ a0.)

Needs numpy, scipy. The real high-z kinematics (e.g. KMOS3D/KGES/KROSS velocity
tables, or JWST/ALMA dynamics) are NOT in this repo; supply them with --data.
"""

import argparse
import csv
import math
import sys
import numpy as np

OM, OL = 0.315, 0.685
A0_SPARC = 1.13e-10               # z~0 anchor from real SPARC RAR (sparc_rar_honest.py)


def E(z):
    return np.sqrt(OM * (1.0 + np.asarray(z, float)) ** 3 + OL)


def db_const(z):   return np.zeros_like(np.asarray(z, float))
def db_total(z):   return -np.log10(E(z))                       # a0 ~ H(z)
def db_matter(z):  return -1.5 * np.log10(1.0 + np.asarray(z, float))   # a0 ~ (1+z)^1.5

HYP = {"H0 constant a0 (null)": db_const,
       "H1 a0~H(z)  [E(z)]":   db_total,
       "H2 a0~(1+z)^1.5 [matter]": db_matter}


def binned_zeropoint(z, logMbar, e_logMbar, logVflat, e_logVflat, edges):
    """Inverse-variance weighted BTFR zero-point b=logMbar-4logVflat in each z-bin."""
    r = logMbar - 4.0 * logVflat
    sr2 = e_logMbar ** 2 + 16.0 * e_logVflat ** 2
    zc, b, be, n = [], [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (z >= lo) & (z < hi)
        if m.sum() < 3:
            continue
        w = 1.0 / sr2[m]
        bw = np.sum(w * r[m]) / np.sum(w)
        zc.append(np.mean(z[m]))
        b.append(bw)
        be.append(1.0 / math.sqrt(np.sum(w)))
        n.append(int(m.sum()))
    return (np.array(zc), np.array(b), np.array(be), np.array(n))


def run_test(z, logMbar, e_logMbar, logVflat, e_logVflat, edges):
    zc, b, be, n = binned_zeropoint(z, logMbar, e_logMbar, logVflat, e_logVflat, edges)
    if len(zc) < 2:
        print("  not enough populated z-bins (need >=2 with >=3 galaxies). abort.")
        return
    db = b - b[0]                              # self-anchor on lowest-z bin
    dbe = np.sqrt(be ** 2 + be[0] ** 2)
    print(f"  {'z':>6}{'N':>5}{'zeropoint b':>14}{'db (meas)':>12}{'+/-':>8}")
    for i in range(len(zc)):
        print(f"  {zc[i]:>6.2f}{n[i]:>5}{b[i]:>14.3f}{db[i]:>12.3f}{dbe[i]:>8.3f}")
    print()
    print(f"  {'hypothesis':<28}{'chi2':>9}{'dof':>5}{'chi2/dof':>10}")
    best, best_chi = None, 1e99
    dof = len(zc) - 1
    for name, fn in HYP.items():
        pred = fn(zc) - fn(zc[0])              # anchored to lowest-z bin too
        chi2 = float(np.sum(((db - pred) / dbe) ** 2))
        if chi2 < best_chi:
            best, best_chi = name, chi2
        print(f"  {name:<28}{chi2:>9.2f}{dof:>5}{chi2/max(dof,1):>10.2f}")
    print(f"\n  => favored: {best}")
    print("     (lowest chi2; if H0 wins, the evolution is falsified; if H1/H2, it lives,")
    print("      and H1-vs-H2 says whether a0 tracks total density or matter free-fall.)")


def selftest():
    """Inject a known H1 signal and confirm the estimator recovers H1 (NOT science)."""
    print("SELF-TEST (synthetic, labelled -- verifies the fitter, not a result):")
    rng = np.random.default_rng(1)
    n = 400
    z = rng.uniform(0.05, 2.5, n)
    logVflat = rng.uniform(1.9, 2.4, n)                 # ~80-250 km/s
    true_b0 = math.log10(1.0)                           # arbitrary
    # inject H1: db = -log10 E(z); so logMbar = 4 logV + (b0 + dbH1)
    logMbar = 4 * logVflat + true_b0 + (-np.log10(E(z)))
    e_logMbar = np.full(n, 0.08); e_logVflat = np.full(n, 0.03)
    logMbar += rng.normal(0, e_logMbar)
    logVflat += rng.normal(0, e_logVflat)
    run_test(z, logMbar, e_logMbar, logVflat, e_logVflat,
             edges=np.array([0.0, 0.4, 0.9, 1.5, 2.6]))
    print("  expected: H1 favored (we injected it). If so, the estimator is sound.\n")


def show_predictions():
    print("=" * 72)
    print("a0(z) test pipeline -- predictions and data schema (no real high-z data on disk)")
    print("=" * 72)
    print(f"  z~0 anchor: a0 = {A0_SPARC:.2e} m/s^2 (real SPARC RAR, sparc_rar_honest.py)")
    print()
    print("  Parameter-free BTFR zero-point shift db(z) = -log10[a0(z)/a0(0)]:")
    print(f"  {'z':>6}{'H0 const':>11}{'H1 E(z)':>11}{'H2 (1+z)^1.5':>14}")
    for z in (0.5, 1.0, 1.5, 2.0, 3.0):
        print(f"  {z:>6.1f}{0.0:>11.3f}{db_total(z):>11.3f}{db_matter(z):>14.3f}")
    print()
    print("  H1 and H2 separate cleanly by z=1 (-0.25 vs -0.45 dex) -- a ~0.1 dex")
    print("  zero-point measurement in 2-3 redshift bins distinguishes all three.")
    print()
    print("  TO RUN THE REAL TEST: supply --data FILE.csv with columns")
    print("    id, z, logMbar, e_logMbar, logVflat, e_logVflat")
    print("  for deep-MOND (g=V_flat^2/R <~ a0) flat-rotation-curve galaxies at z>0")
    print("  (KMOS3D/KGES/KROSS kinematics, or JWST/ALMA dynamics). NOT included here.")
    print()
    print("  HONEST CAVEAT: massive high-z disks (Genzel/Ubler-type) sit at g>a0")
    print("  (Newtonian) even with a0 tripled -- they do NOT test this. The sample must")
    print("  reach the low-acceleration regime, or the null/alternatives are degenerate.")


def load_csv(path):
    rows = {k: [] for k in ("z", "logMbar", "e_logMbar", "logVflat", "e_logVflat")}
    with open(path) as fh:
        for row in csv.DictReader(fh):
            for k in rows:
                rows[k].append(float(row[k]))
    return {k: np.array(v) for k, v in rows.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="CSV of high-z rotators (see schema)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    elif args.data:
        d = load_csv(args.data)
        print(f"loaded {len(d['z'])} galaxies from {args.data}")
        run_test(d["z"], d["logMbar"], d["e_logMbar"], d["logVflat"], d["e_logVflat"],
                 edges=np.array([0.0, 0.4, 0.9, 1.5, 2.6, 4.0]))
    else:
        show_predictions()


if __name__ == "__main__":
    main()
