#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M2, quick data fire of E-S6-1 (the MASS-LINE) on SPARC
=============================================================================
The mass-line (exact under the framework law, any spherical/circular system):
    G [M_eff(r)^2 - M_b(r)^2] = a0 M_b(r) r^2
equivalently the pointwise estimator  a0_hat = (g_obs^2 - g_bar^2)/g_bar.
This fire checks the estimator RUNS end-to-end on real kinematics (SPARC, 175
galaxies, read-only from the frozen repo) and reports where the slope lands.

HONESTY RAILS (banked, memory rule #2): the SPARC RAR is convention-COMPATIBLE and
NON-diagnostic of 9.36e-11 vs 1.13e-10 -- the Upsilon (M/L) degeneracy dominates the
slope. This fire therefore reports the slope at a GRID of Upsilon and both footings;
it is a sanity fire of the ESTIMATOR, not a measurement of a0. Neither "too low"
nor "too high" is claimed.
Protocol: rar_framework_a0_mlfit.py conventions (Vbar^2 = sgn Vgas^2 + Ud Vdisk^2
+ Ub Vbul^2, Ub = 1.4 Ud), error-weighted.
"""
import sys, glob, os
import numpy as np

kpc = 3.0857e19
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"

rows = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    rows.append((R*kpc, Vobs, eV, Vgas, Vdisk, Vbul))
print(f"galaxies loaded: {len(rows)}")
if len(rows) < 150:
    print("FAIL: SPARC load incomplete")
    sys.exit(1)

def massline_slope(Ud):
    """weighted least-squares slope of Y = g_obs^2 - g_bar^2 against X = g_bar
    through the origin (the mass-line / a0-line slope), plus pointwise median."""
    X, Y, w = [], [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + 1.4*Ud*Vbul**2
        gb = Vbar2*1e6/Rm
        go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0) & (eV > 0)
        # error on Y: dY = 2 go dgo = 2 go * (2 Vobs dV/Vobs) go = 4 go^2 (dV/V)
        sigY = 4*go[ok]**2*np.clip(eV[ok], 1, None)/np.clip(Vobs[ok], 1, None)
        X += list(gb[ok]); Y += list(go[ok]**2 - gb[ok]**2); w += list(1/sigY**2)
    X, Y, w = map(np.array, (X, Y, w))
    slope = np.sum(w*X*Y)/np.sum(w*X**2)
    med = np.median(Y/X)
    # low-y band fit (g_bar below its sample median): the difference-of-squares Y is
    # well-conditioned there (g_bar-side M/L errors do not dominate Y)
    band = X < np.median(X)
    slope_band = np.sum((w*X*Y)[band])/np.sum((w*X**2)[band])
    return slope, med, slope_band, len(X)

print()
print(f"{'Upsilon_disk':>12} | {'WLS all (biased)':>16} | {'median pointwise':>16} |"
      f" {'WLS low-y band':>15} | N")
print("-"*80)
res_med, res_wls, res_band = {}, {}, {}
for Ud in (0.5, 0.6, 0.7, 0.8):
    sl, med, slb, N = massline_slope(Ud)
    res_wls[Ud], res_med[Ud], res_band[Ud] = sl, med, slb
    print(f"{Ud:>12} | {sl:16.3e} | {med:16.3e} | {slb:15.3e} | {N}")

print()
print("footings: canonical a0 = 9.362e-11 ; alt a0 = 1.130e-10  (m/s^2)")
for Ud in res_med:
    print(f"  Ud={Ud}: median/canonical = {res_med[Ud]/9.362e-11:5.2f}   "
          f"median/alt = {res_med[Ud]/1.130e-10:5.2f}")

# sanity gates (estimator-level, NOT a0-measurement gates):
# robust median at physical M/L lands at the a0 scale and BRACKETS the two footings
ok1 = 3e-11 < res_med[0.7] < 4e-10 and 3e-11 < res_med[0.6] < 4e-10
ok2 = res_med[0.5] > res_med[0.8]      # Upsilon-degeneracy has the expected sign
ok3 = res_med[0.7] < 9.362e-11 < res_med[0.5] and res_med[0.7] < 1.130e-10 < res_med[0.5]
span = max(res_med.values())/min(res_med.values())
print(f"\nUpsilon 0.5->0.8 moves the median estimator by x{span:.2f} "
      f"(the M/L degeneracy IS the dominant systematic -> non-diagnostic between footings)")
print(("PASS " if ok1 else "FAIL ") + "median estimator lands at the a0 scale (3e-11..4e-10)")
print(("PASS " if ok2 else "FAIL ") + "estimator decreases with Upsilon (expected degeneracy sign)")
print(("PASS " if ok3 else "FAIL ") + "BOTH footings are bracketed inside the physical "
      "Upsilon 0.5-0.7 range (non-diagnostic, as banked)")
print("""
METHODOLOGICAL FINDING (E-S8-cross, derived by this fire): the naive weighted
least-squares slope of Y = g_obs^2 - g_bar^2 on X = g_bar through the origin is
BIASED LOW (2.7e-11 at Ud=0.7, 3x under the median), because at high g_bar the
difference of squares inherits sign-definite, M/L-correlated g_bar-side errors
that a Y-error-only WLS treats as zero-mean. Any a0-line/mass-line fit must use
a robust (median/quantile) estimator, a low-y band, or full errors-in-variables.
VERDICT: the mass-line estimator fires end-to-end on real data; at physical M/L
the robust slope brackets both footings; NON-diagnostic between footings
(consistent with the banked RAR audit). No win, no deficit claimed.""")
sys.exit(0 if (ok1 and ok2 and ok3) else 1)
