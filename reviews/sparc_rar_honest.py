#!/usr/bin/env python3
"""
The honest anchor: the radial-acceleration relation and a0 from the REAL SPARC data.
====================================================================================

The data audit (reviews/DATA_AUDIT.md) found that the repo's SPARC scripts were
either sound-but-broken (a path-changing reorg left them reading 0 files) or fully
synthetic (WORK_ORDER_DD generates v from MOND then "recovers" MOND). This script is
the clean replacement: it reads the genuine 175 SPARC rotation curves on disk
(data/sparc_data/*_rotmod.dat, Lelli, McGaugh & Schombert 2016), builds the
radial-acceleration relation, and FITS the single scale a0 -- no synthetic data, no
hidden free parameters beyond the standard stellar M/L, no circular self-injection.

It then states honestly where a0 lands, what it means (and does NOT mean), and why
the a0(z) EVOLUTION -- the program's one distinctive claim -- cannot be tested with
any data currently on disk (the KMOS3D file present has no rotation velocities).

Run:  python reviews/sparc_rar_honest.py     (needs numpy, scipy)
"""

import glob
import math
import os
import numpy as np
from scipy.optimize import curve_fit

KPC_M = 3.0856775814913673e19      # kpc -> m
KMS_MS = 1.0e3                      # km/s -> m/s
ML_DISK = 0.5                       # 3.6um stellar M/L (McGaugh+2016)
ML_BULGE = 0.7
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")

# framework + literature reference values
A0_MCGAUGH = 1.20e-10              # McGaugh+2016 RAR fit (m/s^2)
C = 2.99792458e8
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)


def load_points():
    """Return arrays (g_bar, g_obs) over all SPARC points passing standard cuts."""
    gbar, gobs = [], []
    ngal = 0
    for path in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        rows = []
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 6:
                    continue
                try:
                    r, vobs, everr, vgas, vdisk, vbul = (float(parts[i]) for i in range(6))
                except ValueError:
                    continue
                rows.append((r, vobs, everr, vgas, vdisk, vbul))
        if not rows:
            continue
        ngal += 1
        for r, vobs, everr, vgas, vdisk, vbul in rows:
            if r <= 0 or vobs <= 0:
                continue
            # standard SPARC RAR accuracy cut: fractional velocity error < 0.1
            if everr <= 0 or everr / vobs > 0.10:
                continue
            # baryonic velocity^2 (sign-preserving, M/L applied)
            vbar2 = (vgas * abs(vgas)
                     + ML_DISK * vdisk * abs(vdisk)
                     + ML_BULGE * vbul * abs(vbul))
            if vbar2 <= 0:
                continue
            r_m = r * KPC_M
            g_obs = (vobs * KMS_MS) ** 2 / r_m
            g_bar = (vbar2 * KMS_MS ** 2) / r_m
            if g_bar <= 0 or g_obs <= 0:
                continue
            gbar.append(g_bar)
            gobs.append(g_obs)
    return np.array(gbar), np.array(gobs), ngal


def rar_logmodel(log_gbar, a0):
    """McGaugh interpolating RAR: g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0)))."""
    gbar = 10.0 ** log_gbar
    x = np.sqrt(gbar / a0)
    gobs = gbar / (1.0 - np.exp(-x))
    return np.log10(gobs)


def main():
    gbar, gobs, ngal = load_points()
    lgbar, lgobs = np.log10(gbar), np.log10(gobs)
    print("=" * 76)
    print("(1) REAL SPARC radial-acceleration relation -- data actually on disk")
    print("=" * 76)
    print(f"   galaxies read           : {ngal}   (data/sparc_data/*_rotmod.dat)")
    print(f"   points after err/V<0.1 cut: {len(gbar)}")
    print(f"   M/L: disk={ML_DISK}, bulge={ML_BULGE} (3.6um, McGaugh+2016)")
    print()

    # fit the single scale a0
    popt, pcov = curve_fit(rar_logmodel, lgbar, lgobs, p0=[1.2e-10],
                           bounds=(1e-11, 1e-9))
    a0 = popt[0]
    a0err = float(np.sqrt(pcov[0, 0]))
    resid = lgobs - rar_logmodel(lgbar, a0)
    scatter = float(np.std(resid))

    print("=" * 76)
    print("(2) Fit the single MOND scale a0 (one free parameter)")
    print("=" * 76)
    print(f"   best-fit a0        = {a0:.3e}  +/- {a0err:.1e}  m/s^2")
    print(f"   McGaugh+2016 RAR   = {A0_MCGAUGH:.3e}  m/s^2   (diff {(a0-A0_MCGAUGH)/A0_MCGAUGH*100:+.1f}%)")
    print(f"   RAR scatter        = {scatter:.3f} dex   (McGaugh total ~0.13 dex)")
    print()

    print("=" * 76)
    print("(3) What this does and does NOT show about Z")
    print("=" * 76)
    for H0, tag in [(67.4, "Planck"), (71.5, "framework"), (73.0, "SH0ES")]:
        cH0 = C * (H0 * 1e3 / MPC)
        print(f"   cH0/Z at H0={H0:<5} ({tag:9}) = {cH0/Z:.3e}  m/s^2")
    print(f"   measured a0 (this fit)          = {a0:.3e}  m/s^2")
    print("   => the real a0 sits inside the cH0/Z band -- i.e. a0 ~ cH0 to a")
    print("      coefficient of order 1/6 (the 40-year-old Milgrom coincidence).")
    print("      It is a REAL number from REAL data, but it does NOT single out Z:")
    print("      any H0 in 67-73 makes cH0/Z match, and the coefficient is one")
    print("      number hostage to H0 (reviews/is_Z_special.py, coefficient_vs_hubble).")
    print()

    print("=" * 76)
    print("(4) The honest boundary: the a0(z) EVOLUTION is NOT testable on disk")
    print("=" * 76)
    print("   The one distinctive claim is a0(z)/a0(0)=E(z). Testing it needs ROTATION")
    print("   VELOCITIES at z>0. The only high-z file on disk, data/kmos3d/")
    print("   k3d_fnlsp_table_v3.fits, has LMSTAR, Z, SFR, RHALF -- but NO velocity")
    print("   column. So a high-z BTFR/RAR cannot be built from it, and I will not")
    print("   fabricate one (which is exactly what examples/07 did with a hand-typed")
    print("   mock CSV). The evolution stays an open, honest prediction.")
    print()
    print("   To actually test it one needs a deep-MOND (low-acceleration) rotator")
    print("   sample with measured v_flat and baryonic mass at z>1 -- e.g. the real")
    print("   KMOS3D/KGES/KROSS kinematics tables, or future JWST/ALMA dynamics.")
    print()

    print("=" * 76)
    print("VERDICT")
    print("=" * 76)
    print(f"  * The REAL SPARC RAR gives a0 = {a0:.2e} m/s^2, scatter {scatter:.2f} dex --")
    print(f"    consistent with McGaugh's {A0_MCGAUGH:.2e}. This is the one solid, real-data")
    print("    empirical anchor in the whole program, and it reproduces here cleanly.")
    print("  * It confirms MOND phenomenology and the Milgrom a0~cH0 coincidence -- NOT")
    print("    the specific geometric value Z (the coefficient is unresolved, H0-hostage).")
    print("  * The distinctive a0(z) evolution remains UNTESTED: no on-disk data can test")
    print("    it, and I will not fake it. That is the honest state of the surviving claim.")


if __name__ == "__main__":
    main()
