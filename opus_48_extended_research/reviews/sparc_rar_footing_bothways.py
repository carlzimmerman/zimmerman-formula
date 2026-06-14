#!/usr/bin/env python3
"""
The both-ways footing check on the SPARC RAR a0 (MEMORY working-rule verification).
==================================================================================

The project's #1 working rule (MEMORY.md): test the equation on ITS OWN footing
(a0 = 9.36e-11, Upsilon ~ 0.70), and verify a framework-FAVORABLE claim as hard as
an unfavorable one. The standing claim on record is:

    "under standard UNWEIGHTED dex-scatter the framework value a0=9.36e-11 is within
     ~0.3% of optimal" -- and the rival 'a0 is ~20% too low' is an artifact of using
     the McGaugh M/L=0.5 footing + an RAR-preferred weighting instead of the
     framework's own Upsilon~0.70 + unweighted dex-scatter.

This script tests that claim adversarially on the REAL 175 SPARC rotation curves
(data/sparc_data/*_rotmod.dat, Lelli+2016), with NO synthetic data:

  (A) re-derive the unweighted-dex-scatter-optimal a0 at TWO footings:
      Upsilon_disk = 0.50 (McGaugh standard) and 0.70 (framework);
  (B) report where the framework's a0=9.36e-11 lands vs each optimum, AND the
      scatter PENALTY of forcing a0=9.36e-11 vs the free optimum (the honest cost);
  (C) bound the convention spread (how much the optimum swings with M/L alone),
      so a 'deficit' can be judged real-vs-artifact.

Both directions are reported. A framework-favorable result here is only banked if it
survives the same scrutiny a kill would get.

Run:  python reviews/sparc_rar_footing_bothways.py     (needs numpy, scipy)
"""

import glob
import math
import os
import numpy as np
from scipy.optimize import minimize_scalar

KPC_M = 3.0856775814913673e19
KMS_MS = 1.0e3
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")

C = 2.99792458e8
A0_FRAMEWORK = 9.36e-11      # c H_Lambda / Z on the pure-Lambda rho_DE footing
A0_MCGAUGH = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def load_points(ml_disk, ml_bulge):
    """RAR points (g_bar, g_obs) at a chosen stellar M/L; standard err<0.1 cut."""
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
            if everr <= 0 or everr / vobs > 0.10:
                continue
            vbar2 = (vgas * abs(vgas)
                     + ml_disk * vdisk * abs(vdisk)
                     + ml_bulge * vbul * abs(vbul))
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
    """McGaugh interpolating RAR in log space."""
    gbar = 10.0 ** log_gbar
    x = np.sqrt(gbar / a0)
    gobs = gbar / (1.0 - np.exp(-x))
    return np.log10(gobs)


def dex_scatter(lgbar, lgobs, a0):
    """UNWEIGHTED rms vertical (dex) residual of the RAR at this a0 -- the metric."""
    resid = lgobs - rar_logmodel(lgbar, a0)
    return float(np.sqrt(np.mean(resid ** 2)))


def optimal_a0(lgbar, lgobs):
    """a0 minimizing the unweighted dex scatter (the framework's preferred metric)."""
    f = lambda la0: dex_scatter(lgbar, lgobs, 10.0 ** la0)
    res = minimize_scalar(f, bounds=(math.log10(5e-11), math.log10(3e-10)),
                          method="bounded", options={"xatol": 1e-6})
    return 10.0 ** res.x, res.fun


def report_footing(name, ml_disk, ml_bulge):
    gbar, gobs, ngal = load_points(ml_disk, ml_bulge)
    lgbar, lgobs = np.log10(gbar), np.log10(gobs)
    a0_opt, s_opt = optimal_a0(lgbar, lgobs)
    s_fw = dex_scatter(lgbar, lgobs, A0_FRAMEWORK)
    off_fw = (A0_FRAMEWORK - a0_opt) / a0_opt * 100.0
    penalty = s_fw - s_opt
    print(f"--- footing: {name}  (Upsilon_disk={ml_disk}, bulge={ml_bulge}) ---")
    print(f"    galaxies / points            : {ngal} / {len(gbar)}")
    print(f"    unweighted-dex-OPTIMAL a0    : {a0_opt:.3e}   (scatter {s_opt:.4f} dex)")
    print(f"    framework a0 = 9.36e-11      : scatter {s_fw:.4f} dex")
    print(f"    framework offset from optimal: {off_fw:+.2f}%")
    print(f"    scatter PENALTY of framework : {penalty:+.4f} dex "
          f"({penalty/s_opt*100:+.2f}% of the optimum)")
    print()
    return a0_opt, s_opt, off_fw, penalty


def main():
    print("=" * 76)
    print("BOTH-WAYS FOOTING CHECK -- framework a0=9.36e-11 vs the SPARC RAR optimum")
    print("=" * 76)
    print(f"   metric: UNWEIGHTED rms dex scatter (the framework's preferred metric)")
    print(f"   framework a0 = {A0_FRAMEWORK:.3e}  (= c H_Lambda / Z, Z={Z:.4f})")
    print(f"   McGaugh   a0 = {A0_MCGAUGH:.3e}")
    print()
    std = report_footing("McGaugh standard", 0.50, 0.70)
    fw = report_footing("framework", 0.70, 0.70)
    # also a 0.60 midpoint, to bound the convention spread continuously
    mid = report_footing("midpoint", 0.60, 0.70)

    a0_std, a0_fw = std[0], fw[0]
    spread = abs(a0_std - a0_fw) / ((a0_std + a0_fw) / 2) * 100.0
    print("=" * 76)
    print("VERDICT (both ways)")
    print("=" * 76)
    print(f"   * The unweighted-dex-optimal a0 SWINGS {spread:.1f}% from M/L alone")
    print(f"     ({a0_std:.3e} at 0.50  ->  {a0_fw:.3e} at 0.70).")
    print(f"   * On the FRAMEWORK footing (Upsilon=0.70), a0=9.36e-11 lands "
          f"{fw[2]:+.2f}% from optimal,")
    print(f"     a scatter penalty of {fw[3]:+.4f} dex -- "
          f"{'NEGLIGIBLE (claim holds)' if abs(fw[2])<3 else 'NON-trivial'}.")
    print(f"   * On the McGAUGH footing (Upsilon=0.50), the SAME a0 lands "
          f"{std[2]:+.2f}% from optimal.")
    print()
    if abs(fw[2]) < 3.0:
        print("   => HONEST READ: the 'a0 is ~20% too low' gap is a FOOTING ARTIFACT.")
        print("      Raising M/L from the McGaugh 0.50 to the framework's own 0.70")
        print("      moves the unweighted-dex optimum down ONTO 9.36e-11; the apparent")
        print("      deficit is the convention, not the equation. (MEMORY rule upheld:")
        print("      checked on the framework's OWN footing, deficit vanishes => not real.)")
    else:
        print("   => HONEST READ: a residual gap survives even at Upsilon=0.70 --")
        print("      report it at full weight; it is NOT a pure footing artifact.")
    print()
    print("   Caveat kept both ways: this is a0 magnitude at z=0 only. It does NOT")
    print("   test a0(z), does NOT single out Z (H0-hostage coefficient), and a")
    print("   higher M/L is itself a framework CHOICE, not a free win -- the honest")
    print("   statement is that the magnitudes are convention-compatible, not that")
    print("   9.36e-11 is uniquely selected by the data.")


if __name__ == "__main__":
    main()
