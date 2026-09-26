#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XC4 -- NU_MONO'S SPLICE, COMPUTED: where nu_mono leaves nu_RAR, how far apart the two get, how smooth the join is.

The recipe's user-decision block and the spec's operative requirement 1 (commit 9092fc0fd) described nu_mono as "nu_RAR
below the peak" and "within 0.01 dex of nu_RAR everywhere".  The cross-thread review (XR3 K1-K2,
real_research/cross_thread_review_2026_09_26/) found both slightly inexact.  This lane recomputes them independently --
closed forms at 40 digits (mpmath), not the review's grid -- and compares with L340's stored construction.

DEFINITION (L340 A1; the recipe's user-decision block):
  h_mono(y) = int_0^y max(h'_RAR(s), delta h_p/(s + y_p)) ds,   nu_mono(y) = 1 + h_mono(y)/y,
  h_RAR(y) = y/(e^sqrt(y) - 1) (the phantom of nu_RAR = 1/(1 - e^-sqrt(y))), y_p its peak, h_p = h_RAR(y_p), delta = 0.05.

WHAT THIS LANE CHECKS
  S1 y_p and h_p (closed form) reproduce L340's stored A1 values.
  S2 the max() switches branch exactly once, at y* = 2.3374 < y_p, where h'_RAR = delta h_p/(y + y_p); the floor binds
     at every y > y*.  So h_mono = h_RAR for y <= y*, and h_RAR(y*) + delta h_p ln((y + y_p)/(y* + y_p)) above.
  S3 nu_mono = nu_RAR identically for y <= y*; on (y*, y_p] they differ, by at most 9.1e-5 dex; L340's grid
     construction agrees with the closed form to grid level everywhere.
  S4 the largest |log10(nu_mono/nu_RAR)| is 0.01037 dex at y = 14.35 (L340 stores 0.010370): the bound is 0.0104 dex,
     not "<= 0.01".
  S5 smoothness at the splice: C_L = h' is continuous and positive at y*, and its derivative jumps (-0.0361 -> -0.0014).
     h is C^{1,1}, not C^2, so the QUMOND primitive Q(Z) = Z + 2 int_0^sqrt(Z) h_mono is C^2, not C^3 (XC5's scope line).
  S6 above y* nu_mono's Newtonian-side coefficient C_T = nu - 1 exceeds nu_RAR's by a growing factor (3.01 at y = 20)
     while nu itself moves <= 0.0104 dex: a lane that evaluates C_T at y > y* must use nu_mono.  XC3's cluster-core row
     used nu_RAR's C_T; it is corrected in XC3 in the same commit.

MUTATE=1 takes the old wording literally -- nu_RAR up to the peak y_p, the floor above it -- and S5 must FAIL: that
function's C_L jumps from 0 to delta h_p/(2 y_p) = 0.0064 at y_p (a discontinuous constitutive coefficient).  S3 and
S4, which test the true construction's numbers, fail with it.  rc = 1.

SCOPE.  The kernel as a function of one variable.  Whether the author declares a C^2 variant of the splice (a smooth
max) or the symbol and G8 arguments are done nonsmoothly is a decision (XR3 step 0 (b)), not computed here.

Run from the repository root:  python3 real_research/extra_crispy_2026/XC4_nu_mono_splice.py
"""
import os, sys, json, time
import numpy as np
import mpmath as mp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "XC4", "XC4_nu_mono_splice"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
mp.mp.dps = 40


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the splice is put at the peak y_p (the old wording read literally); S5 must FAIL ***")
L340 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")))
A1 = L340["numbers"]["A1"]


# ============================================================================================ closed forms (40 digits)
def hR(y):
    z = mp.sqrt(y); return y / mp.expm1(z)
def dhR(y):                                                      # [2(e^z - 1) - z e^z] / [2 (e^z - 1)^2], z = sqrt(y)
    z = mp.sqrt(y); em = mp.expm1(z); return (2 * em - z * (1 + em)) / (2 * em**2)
def d2hR(y):
    return mp.diff(dhR, y)


YP = mp.findroot(dhR, 2.5); HP = hR(YP); DELTA = mp.mpf("0.05")
floor = lambda y: DELTA * HP / (y + YP)
YS = mp.findroot(lambda y: dhR(y) - floor(y), 2.3)
YSW = YP if MUTATE else YS                                       # where the construction under test leaves nu_RAR


def h_mono(y):
    y = mp.mpf(y)
    return hR(y) if y <= YSW else hR(YSW) + DELTA * HP * mp.log((y + YP) / (YSW + YP))
def CL_mono(y):                                                  # d(y nu)/dy - 1 = h'
    y = mp.mpf(y)
    return dhR(y) if y <= YSW else floor(y)
nu_rar = lambda y: 1 / (-mp.expm1(-mp.sqrt(y)))
nu_mono = lambda y: 1 + h_mono(y) / y
dev = lambda y: mp.log10(nu_mono(y) / nu_rar(y))

# ============================================================================================ S1
banner("S1  THE PEAK: y_p and h_p against L340's stored A1")
P(f"    y_p = {mp.nstr(YP, 12)}, h_p = {mp.nstr(HP, 12)} a0   (L340: {A1['y_p']:.10f}, {A1['h_p']:.10f})")
OUT["numbers"]["S1"] = {"y_p": float(YP), "h_p": float(HP), "L340_y_p": A1["y_p"], "L340_h_p": A1["h_p"]}
check("S1 the closed-form peak of nu_RAR's phantom reproduces L340's stored y_p and h_p",
      f"|dy_p| = {abs(float(YP) - A1['y_p']):.1e}, |dh_p| = {abs(float(HP) - A1['h_p']):.1e}",
      abs(float(YP) - A1["y_p"]) < 1e-6 and abs(float(HP) - A1["h_p"]) < 1e-9,
      "L340 finds y_p with a finite-difference derivative; its value agrees to 4e-10")

# ============================================================================================ S2
banner("S2  THE SWITCH: where max(h'_RAR, delta h_p/(y + y_p)) changes branch")
grid = [mp.mpf(10)**e for e in np.linspace(-8, 8, 4001)]
sg = [mp.sign(dhR(y) - floor(y)) for y in grid]
n_changes = sum(1 for a, b in zip(sg, sg[1:]) if a != b)
P(f"    sign changes of h'_RAR - floor on y in 1e-8..1e8 (4001 log points): {n_changes}")
P(f"    y* = {mp.nstr(YS, 12)}  (y_p - y* = {mp.nstr(YP - YS, 6)}); C_L(y*) = {mp.nstr(floor(YS), 10)}")
P("    above y_p, h'_RAR < 0 < floor analytically (sign of 2 - 2e^-z - z, concave with one positive root z_p)")
OUT["numbers"]["S2"] = {"y_star": float(YS), "sign_changes": n_changes, "CL_at_y_star": float(floor(YS))}
check("S2 the max() switches branch exactly once, at y* = 2.3374, strictly below the peak y_p = 2.5396; the floor binds "
      "at every y > y*", f"{n_changes} sign change; y* = {mp.nstr(YS, 8)} < y_p = {mp.nstr(YP, 8)}",
      n_changes == 1 and YS < YP and abs(YS - mp.mpf("2.3374124053")) < 1e-9,
      "so 'nu_mono = nu_RAR below the peak' is exact only up to y*; on (y*, y_p] the floor already binds")

# ============================================================================================ S3
banner("S3  WHERE THE TWO ARE EQUAL, AND WHERE THEY ARE NOT: the closed form against L340's grid construction")
below = [YS * mp.mpf(10)**(-e) for e in np.linspace(0.0005, 5, 400)]
d_below = max(abs(dev(y)) for y in below)
band = [YS + (YP - YS) * k / 2000 for k in range(1, 2001)]
d_band = max(abs(dev(y)) for y in band)


def h_rar_np(y):                                                 # L340 A1's construction, verbatim
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar_np(y, e=1e-6):
    return (h_rar_np(y * (1 + e)) - h_rar_np(y * (1 - e))) / (2 * y * e)
Y_P_np = brentq(lambda y: float(dh_rar_np(y)), 1.0, 5.0); H_P_np = float(h_rar_np(Y_P_np))
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar_np(YG), 0.05 * H_P_np / (YG + Y_P_np))
H_MONO = float(h_rar_np(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
ycmp = np.logspace(-3, 4, 1401)
nu_grid = 1.0 + np.interp(np.log10(ycmp), LYG, H_MONO) / ycmp
d_grid = max(abs(float(mp.log10(mp.mpf(float(g)) / nu_mono(mp.mpf(float(y)))))) for g, y in zip(nu_grid, ycmp))
P(f"    y <= y*:       max |log10(nu_mono/nu_RAR)| = {mp.nstr(d_below, 3)} dex (identical by construction)")
P(f"    (y*, y_p]:     max |log10(nu_mono/nu_RAR)| = {mp.nstr(d_band, 6)} dex")
P(f"    L340's grid construction vs this closed form, y in 1e-3..1e4: max {d_grid:.1e} dex")
OUT["numbers"]["S3"] = {"max_dev_below_y_star": float(d_below), "max_dev_band": float(d_band), "grid_vs_closed_dex": d_grid}
check("S3 nu_mono = nu_RAR identically for y <= y*; on (y*, y_p] they differ by at most 9.1e-5 dex (not zero); L340's "
      "grid construction matches the closed form to <= 1e-7 dex", f"below y*: {mp.nstr(d_below, 2)}; band: "
      f"{mp.nstr(d_band, 4)} dex; grid vs closed: {d_grid:.1e} dex",
      d_below < 1e-30 and 5e-5 < d_band < 9.2e-5 and d_grid < 1e-7,
      "the recipe's 'below the peak nu_mono = nu_RAR' should read 'for y <= y* = 2.3374'")

# ============================================================================================ S4
banner("S4  THE LARGEST DEVIATION: nu_mono against nu_RAR over all y")
scan = [mp.mpf(10)**e for e in np.linspace(-3, 6, 1801)]
i_max = int(np.argmax([abs(float(dev(y))) for y in scan]))
y_max = mp.findroot(lambda y: mp.diff(dev, y), scan[i_max])
d_max = abs(dev(y_max))
P(f"    max |log10(nu_mono/nu_RAR)| = {mp.nstr(d_max, 8)} dex at y = {mp.nstr(y_max, 6)}   (L340 stores "
  f"{A1['max_dlog_vs_rar']:.8f} on its 1e-3..1e4 grid)")
P(f"    the difference decays as delta h_p ln(y)/(y ln 10) above: at y = 1e6 it is {mp.nstr(abs(dev(mp.mpf(10)**6)), 3)} dex")
OUT["numbers"]["S4"] = {"max_dev_dex": float(d_max), "y_at_max": float(y_max), "L340_max_dlog": A1["max_dlog_vs_rar"]}
check("S4 the largest deviation is 0.01037 dex at y = 14.35 (L340 stores 0.010370): the bound is 0.0104 dex, "
      "not '<= 0.01'", f"{mp.nstr(d_max, 6)} dex at y = {mp.nstr(y_max, 5)}; L340 {A1['max_dlog_vs_rar']:.6f}",
      d_max > mp.mpf("0.01") and abs(float(d_max) - A1["max_dlog_vs_rar"]) < 5e-6 and abs(y_max - mp.mpf("14.3507")) < 1e-3,
      "the recipe and the spec's operative requirement 1 should say <= 0.0104 dex (max at y = 14.35)")

# ============================================================================================ S5
banner("S5  SMOOTHNESS AT THE SPLICE: C_L and its derivative on both sides")
eps = mp.mpf("1e-25")
CL_left, CL_right = CL_mono(YSW - eps), CL_mono(YSW + eps)
dCL_left = d2hR(YSW)
dCL_right = -DELTA * HP / (YSW + YP)**2
P(f"    splice at y = {mp.nstr(YSW, 10)}: C_L left = {mp.nstr(CL_left, 10)}, right = {mp.nstr(CL_right, 10)}")
P(f"    dC_L/dy left = {mp.nstr(dCL_left, 8)}, right = {mp.nstr(dCL_right, 8)}, jump = {mp.nstr(dCL_right - dCL_left, 6)}")
cl_scan = min(CL_mono(y) for y in scan)
P(f"    min C_L on y in 1e-3..1e6: {mp.nstr(cl_scan, 4)}")
OUT["numbers"]["S5"] = {"y_splice": float(YSW), "CL_left": float(CL_left), "CL_right": float(CL_right),
                        "dCL_left": float(dCL_left), "dCL_right": float(dCL_right), "min_CL": float(cl_scan)}
check("S5 C_L is continuous and positive at the splice and everywhere, and its derivative jumps there: h is C^{1,1} "
      "(not C^2), so Q(Z) = Z + 2 int h_mono is C^2 but not C^3",
      f"C_L jump {mp.nstr(abs(CL_right - CL_left), 3)}; C_L(splice) = {mp.nstr(CL_right, 6)}; dC_L/dy "
      f"{mp.nstr(dCL_left, 5)} -> {mp.nstr(dCL_right, 5)}; min C_L {mp.nstr(cl_scan, 3)}",
      abs(CL_right - CL_left) < 1e-20 and CL_left > 0 and cl_scan > 0 and abs(dCL_right - dCL_left) > 0.03,
      "strict convexity (XC5 E3) needs only C_L > 0; the jump in dC_L/dy leaves the cubic constitutive vertex without a "
      "unique value at y* -- a C^2 variant (smooth max) or nonsmooth analysis is XR3's step-0 (b) decision")

# ============================================================================================ S6
banner("S6  THE NEWTONIAN SIDE: C_T = nu - 1 of nu_mono against nu_RAR above y*")
rowsS6 = {}
for y in (2.3, 5.0, 14.35, 20.0, 100.0):
    ym = mp.mpf(y)
    rowsS6[y] = {"CT_rar": float(hR(ym) / ym), "CT_mono": float(h_mono(ym) / ym), "ratio": float(h_mono(ym) / hR(ym)),
                 "dev_dex": float(dev(ym))}
    P(f"    y = {y:6.2f}: C_T nu_RAR = {rowsS6[y]['CT_rar']:.5f}, nu_mono = {rowsS6[y]['CT_mono']:.5f} "
      f"(x{rowsS6[y]['ratio']:.3f}); log10(nu_mono/nu_RAR) = {rowsS6[y]['dev_dex']:.5f}")
OUT["numbers"]["S6"] = rowsS6
check("S6 above y* nu_mono's C_T exceeds nu_RAR's by a growing factor (3.01 at the cluster-core y = 20) while nu moves "
      "<= 0.0104 dex: C_T at y > y* must come from nu_mono", f"ratio at y = 20: {rowsS6[20.0]['ratio']:.4f}; "
      f"at y = 100: {rowsS6[100.0]['ratio']:.1f}; at y = 2.3: {rowsS6[2.3]['ratio']:.4f}",
      rowsS6[2.3]["ratio"] == 1.0 and 2.9 < rowsS6[20.0]["ratio"] < 3.1 and rowsS6[100.0]["ratio"] > rowsS6[20.0]["ratio"],
      "the monotone phantom keeps rising (delta h_p ln y) where nu_RAR's decays as e^-sqrt(y): small in nu, not in C_T. "
      "XC3's cluster-core row (y = 20) used nu_RAR's C_T; corrected there")

banner("VERDICT")
P(f"""  nu_mono leaves nu_RAR at y* = 2.3374, just below the peak y_p = 2.5396, not at the peak; on (y*, y_p] the two differ by
  <= 9.1e-5 dex, and the largest difference anywhere is 0.01037 dex at y = 14.35 -- so '<= 0.0104 dex', not '<= 0.01'.
  The join is C^{{1,1}}: C_L continuous and positive, its slope jumping from -0.0361 to -0.0014.  Above y* the kernel moves
  nu by at most 0.0104 dex but C_T = nu - 1 by a growing factor (3.0 at y = 20), so any lane that evaluates C_T there has
  to use nu_mono.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
