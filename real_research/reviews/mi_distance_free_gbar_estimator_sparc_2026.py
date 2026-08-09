#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_distance_free_gbar_estimator_sparc_2026.py
=============================================
THE DISTANCE-FREE g_bar ESTIMATOR, RUN ON REAL SPARC DATA (175 galaxies, 2803 quality points).

Uses the framework's OWN pieces throughout: a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 (canonical
footing) and the in-force Route A kernel nu(y) = 1/(1 - e^-sqrt(y)) per Amendments 8/9.  NOT McGaugh's nu.

*** WHAT WORKS, VERIFIED ON THE REAL DATA: the estimator is EXACTLY distance-immune.  Under a common
distance rescaling D -> D(1+delta) the physical radii scale as R -> R(1+delta) and the mass-model
velocities as V_bar -> V_bar sqrt(1+delta) (since V_bar^2 ~ GM/R ~ D^2/D), while V_obs is measured and
unchanged.  So g_bar = V_bar^2/R is EXACTLY invariant and g_obs = V_obs^2/R scales as 1/(1+delta).
Fitting with a FREE vertical offset C -- which absorbs any common g_obs rescaling -- returns the
IDENTICAL a_0 at delta = 0, +5% and +10%, to five significant figures, while the standard fit moves by
about 2 delta as predicted. ***

*** AND IT BUYS A REAL FACTOR: at fixed Upsilon the statistical-plus-distance budget drops from 6.83%
to 1.84%, i.e. sigma(kappa) from 0.0435 to 0.0097. ***

--------------------------------------------------------------------------------------------------
AND WHAT DOES NOT WORK -- THE EIGHTH NEAR-MISS OF THIS SESSION, CAUGHT BY ITS OWN ARTIFACT CHECK
--------------------------------------------------------------------------------------------------
The standard and shape-only estimators have OPPOSITE Upsilon-dependence (standard falls, shape-only
rises), so they CROSS -- at Upsilon_d = 0.578, kappa = 0.543.  That looks like it BREAKS the a_0-Upsilon
degeneracy the corpus flagged as irreducible, and I was about to report it as such.

*** IT DOES NOT.  Varying the BULGE mass-to-light moves the crossing to kappa = 0.413 at
Upsilon_bul = 0.5, and at Upsilon_bul = 0.98 there is NO crossing in the searched range at all.  Across
the artifact checks the "determination" spans kappa = 0.41 to 0.60.  The degeneracy is not broken --
it is RELOCATED from the disc M/L to the bulge M/L. ***

--------------------------------------------------------------------------------------------------
THE REDSHIFT SCALING, CHECKED RATHER THAN ASSUMED (Carl asked twice; he was right to)
--------------------------------------------------------------------------------------------------
The framework's a_0(z)/a_0(0) = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z)) applied to SPARC's own
distances (0.98-127.8 Mpc, z = 0.0002-0.0287): the correction is EXACTLY 0.0000% on pure Lambda and at
most 0.40% on a DESI-like (w0,wa) = (-0.9,-0.4).  Against a 6%+ error budget that is negligible -- but
it is now a VERIFIED negligible, carried in the script.
"""

import sys
import glob
import math
import re
import numpy as np
from scipy.optimize import minimize, brentq

FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


FILES = sorted(glob.glob("real_research/data/sparc_data/*_rotmod.dat"))
K = 3.2408e-14                     # (km/s)^2/kpc -> m/s^2
A0 = 9.3619e-11                    # framework canonical
A0_ALT = 1.1279e-10                # alt footing
DEN = 1.87094e-10                  # c sqrt(G rho_Lambda) -- so kappa = a_0/DEN
DEN_ALT = DEN * (A0_ALT / A0)
SIG0 = 0.034                       # RAR intrinsic scatter (Desmond 2023)

print(__doc__)


def load(UD=0.5, UB=0.7, qcut=0.1):
    gb, go, ew = [], [], []
    for f in FILES:
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
        m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < qcut)
        R, V, eV, Vg, Vd, Vb = R[m], V[m], eV[m], Vg[m], Vd[m], Vb[m]
        v2 = np.sign(Vg) * Vg ** 2 + UD * Vd ** 2 + UB * Vb ** 2   # SPARC sign convention
        ok = v2 > 0
        gb.append(v2[ok] / R[ok] * K)
        go.append(V[ok] ** 2 / R[ok] * K)
        ew.append(2 * eV[ok] / V[ok] / math.log(10))
    return np.concatenate(gb), np.concatenate(go), np.concatenate(ew)


def nu(y):
    """The framework's IN-FORCE Route A kernel (Amendments 8/9). NOT McGaugh's."""
    return 1 / (1 - np.exp(-np.sqrt(y)))


def chi2(la, C, gb, go, ew, SIG=SIG0):
    s = np.sqrt(ew ** 2 + SIG ** 2)
    return np.sum(((np.log10(go) - (np.log10(gb * nu(gb / 10 ** la)) + C)) / s) ** 2)


def fit_std(gb, go, ew, SIG=SIG0):
    r = minimize(lambda p: chi2(p[0], 0.0, gb, go, ew, SIG), [math.log10(A0)], method="Nelder-Mead")
    return 10 ** r.x[0]


def fit_shape(gb, go, ew, SIG=SIG0):
    def prof(la):
        r = minimize(lambda c: chi2(la, c[0], gb, go, ew, SIG), [0.0], method="Nelder-Mead")
        return r.fun
    r = minimize(lambda p: prof(p[0]), [math.log10(A0)], method="Nelder-Mead")
    return 10 ** r.x[0], prof


# =============================================================================================
print("=" * 100)
print("PART A -- the data, and the framework's own ingredients")
print("=" * 100)

gb, go, ew = load()
ngal = len(FILES)
check(ngal > 150 and len(gb) > 2000,
      f"A1  loaded {ngal} SPARC galaxies, {len(gb)} quality radial points (err/V < 10%)",
      f"g_bar spans {gb.min()/A0:.4f} - {gb.max()/A0:.1f} a_0")

check(abs(nu(1e-6) - 1 / (1 - math.exp(-1e-3))) < 1e-6,
      "A2  the kernel is the framework's IN-FORCE Route A nu = 1/(1-e^-sqrt(y)), NOT McGaugh's",
      "per Amendment 8/9; deep-MOND and Newtonian limits verified in earlier committed scripts")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- *** THE REDSHIFT SCALING, CHECKED NOT ASSUMED ***")
print("=" * 100)

Ds = []
for f in FILES:
    with open(f) as fh:
        for line in fh:
            m = re.search(r"Distance\s*=\s*([\d.]+)", line)
            if m:
                Ds.append(float(m.group(1)))
                break
Ds = np.array(Ds)
zs = 67.36 * Ds / 2.99792458e5


def a0z(z, w0, wa):
    return (1 + z) ** (1.5 * (1 + w0 + wa)) * math.exp(-1.5 * wa * z / (1 + z))


dev_L = max(abs(a0z(z, -1.0, 0.0) - 1) for z in zs)
dev_D = max(abs(a0z(z, -0.9, -0.4) - 1) for z in zs)
print(f"\n   SPARC distances {Ds.min():.2f}-{Ds.max():.1f} Mpc  ->  z = {zs.min():.5f}-{zs.max():.5f}")
print(f"   max |a_0(z)/a_0(0) - 1| : pure Lambda {dev_L*100:.4f}%   DESI-like (-0.9,-0.4) {dev_D*100:.4f}%")

check(dev_L < 1e-9,
      "B1  on pure Lambda the framework's a_0(z) law is EXACTLY flat -- zero correction, as it must be",
      f"{dev_L*100:.6f}%")
check(dev_D < 0.01,
      f"B2  and on a DESI-like fork it is at most {dev_D*100:.3f}% over SPARC -- NEGLIGIBLE against a 6%+ "
      "budget",
      "verified rather than assumed; it matters for the a_0(z) front at z ~ 1-3, not for a local RAR")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- *** THE DISTANCE-IMMUNITY, VERIFIED ON THE REAL DATA ***")
print("=" * 100)

print("""
   Under D -> D(1+delta):  R -> R(1+delta) ;  V_bar^2 ~ GM/R ~ D^2/D = D  so V_bar -> V_bar sqrt(1+delta) ;
   V_obs is MEASURED and unchanged.  Therefore
        g_bar = V_bar^2/R  is EXACTLY invariant        g_obs = V_obs^2/R  scales as 1/(1+delta)
""")
print("   delta      a_0 STANDARD (C=0)        a_0 SHAPE-ONLY (C free)")
res = {}
for dlt in [0.0, 0.05, 0.10]:
    gos = go / (1 + dlt)
    a_s = fit_std(gb, gos, ew)
    a_h, _ = fit_shape(gb, gos, ew)
    res[dlt] = (a_s, a_h)
    print(f"   {dlt:+.2f}     {a_s:.5e} ({a_s/A0:.4f}x)   {a_h:.5e} ({a_h/A0:.4f}x)")

spread_h = max(v[1] for v in res.values()) / min(v[1] for v in res.values())
spread_s = max(v[0] for v in res.values()) / min(v[0] for v in res.values())
check(spread_h < 1.0001,
      f"C1  *** the SHAPE-ONLY estimator is EXACTLY distance-immune: spread {(spread_h-1)*1e6:.2f} ppm "
      "across a 10% distance error ***",
      "the free offset C absorbs the common g_obs rescaling entirely")

check(spread_s > 1.2,
      f"C2  while the STANDARD estimator moves {(spread_s-1)*100:.1f}% -- consistent with the predicted "
      "2 delta",
      f"so the immunity is a real property of the estimator, not an insensitivity of the data")

# C3 -- what it buys, at fixed Upsilon.
def err1d(f, x0, step=1e-3):
    c = f(x0)
    lo = x0
    while f(lo) - c < 1.0 and x0 - lo < 1.0:
        lo -= step
    hi = x0
    while f(hi) - c < 1.0 and hi - x0 < 1.0:
        hi += step
    return (hi - lo) / 2


a_h0, prof = fit_shape(gb, go, ew)
s_h = err1d(prof, math.log10(a_h0)) * math.log(10)
a_s0 = fit_std(gb, go, ew)
s_s = err1d(lambda la: chi2(la, 0.0, gb, go, ew), math.log10(a_s0)) * math.log(10)
tot_s = math.hypot(s_s, 0.068)      # standard carries the 6.8% distance systematic
tot_h = s_h                          # shape-only carries none
print(f"\n   STANDARD   : stat {s_s*100:.2f}% + distance 6.8%  = {tot_s*100:.2f}%   sigma(kappa) = {a_s0/DEN*tot_s:.4f}")
print(f"   SHAPE-ONLY : stat {s_h*100:.2f}% + distance 0.0%  = {tot_h*100:.2f}%   sigma(kappa) = {a_h0/DEN*tot_h:.4f}")
check(tot_h < tot_s / 2,
      f"C3  *** the distance-free estimator cuts the stat+distance budget {tot_s*100:.2f}% -> {tot_h*100:.2f}%, "
      f"a factor {tot_s/tot_h:.2f} ***",
      "this is the free win, on data that already existed, and it is real")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- *** THE NEAR-MISS: the 'degeneracy breaking' that ISN'T ***")
print("=" * 100)


def both(UD, UB=0.7, qcut=0.1, SIG=SIG0):
    g, o, e = load(UD, UB, qcut)
    a_s = fit_std(g, o, e, SIG)
    a_h, _ = fit_shape(g, o, e, SIG)
    return a_s / DEN, a_h / DEN


print("\n   Ups_d    kappa(standard)   kappa(shape)   difference")
for UD in [0.45, 0.50, 0.55, 0.58, 0.60, 0.65, 0.70]:
    s, h = both(UD)
    print(f"   {UD:.2f}     {s:.4f}            {h:.4f}        {s-h:+.4f}")

ups_c = brentq(lambda u: both(u)[0] - both(u)[1], 0.45, 0.75, xtol=1e-4)
k_c = both(ups_c)[1]
check(0.4 < k_c < 0.7,
      f"D1  the two estimators have OPPOSITE Upsilon-dependence and CROSS at Ups_d = {ups_c:.4f}, "
      f"kappa = {k_c:.4f}",
      "which LOOKS like it breaks the a_0-Upsilon degeneracy the corpus flagged as irreducible")

print("\n   *** ARTIFACT CHECKS -- and they kill it ***")
print("   variation             Ups_cross    kappa")
ks = [k_c]
for lbl, kw in [("baseline", {}), ("no intrinsic scatter", {"SIG": 1e-6}), ("SIG_INT = 0.06", {"SIG": 0.06}),
                ("quality cut 5%", {"qcut": 0.05}), ("quality cut 20%", {"qcut": 0.2}),
                ("Ups_bul = 0.5", {"UB": 0.5})]:
    try:
        u = brentq(lambda x: both(x, **kw)[0] - both(x, **kw)[1], 0.40, 0.85, xtol=1e-4)
        kk = both(u, **kw)[1]
        ks.append(kk)
        print(f"   {lbl:22s} {u:.4f}      {kk:.4f}")
    except Exception:
        print(f"   {lbl:22s} NO CROSSING in [0.40, 0.85]")
try:
    brentq(lambda x: both(x, UB=0.98)[0] - both(x, UB=0.98)[1], 0.40, 0.85, xtol=1e-4)
    ub98 = True
except Exception:
    ub98 = False
    print(f"   {'Ups_bul = 0.98':22s} NO CROSSING in [0.40, 0.85]")

k_spread = max(ks) - min(ks)
check(k_spread > 0.1 or not ub98,
      f"D2  *** IT IS AN ARTEFACT: the 'determination' spans kappa = {min(ks):.3f} to {max(ks):.3f} "
      f"(spread {k_spread:.3f}), and at Ups_bul = 0.98 the crossing DISAPPEARS ***",
      "the degeneracy is NOT broken -- it is RELOCATED from the disc M/L to the BULGE M/L")

check(k_spread > 0.076,
      f"D3  and the spread {k_spread:.3f} is WIDER than the corpus's existing sigma(kappa) = 0.076, so the "
      "'crossing' determination is worse than what it would replace",
      "eighth near-miss of the session; caught by its own artifact check")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the honest bottom line, both footings")
print("=" * 100)

# Upsilon sensitivity of the shape-only estimator, which is what survives.
k_lo, k_hi = both(0.5)[1], both(0.7)[1]
ups_sys = abs(k_hi - k_lo) / 2 / ((k_hi + k_lo) / 2)
GAS = math.hypot(0.05, 0.025, 0.03)          # flux + self-absorption + molecular
tot_frac = math.hypot(s_h, ups_sys, GAS)
k_cen = (k_hi + k_lo) / 2
print(f"\n   shape-only kappa at Ups_d = 0.5 : {k_lo:.4f}")
print(f"   shape-only kappa at Ups_d = 0.7 : {k_hi:.4f}")
print(f"   -> Upsilon systematic {ups_sys*100:.2f}% ;  gas-scale terms {GAS*100:.2f}% ;  stat {s_h*100:.2f}%")
print(f"   TOTAL {tot_frac*100:.2f}%   ->   kappa = {k_cen:.3f} +/- {k_cen*tot_frac:.3f}   (canonical footing)")
print(f"   alt footing: kappa_alt = {k_cen*DEN/DEN_ALT:.3f} +/- {k_cen*DEN/DEN_ALT*tot_frac:.3f}")

t_half = abs(k_cen - 0.5) / (k_cen * tot_frac)
t_isq3 = abs(k_cen - 1 / math.sqrt(3)) / (k_cen * tot_frac)
check(t_half < 2 and t_isq3 < 2,
      f"E1  kappa = {k_cen:.3f} +/- {k_cen*tot_frac:.3f} is {t_half:.2f} sigma from 1/2 and {t_isq3:.2f} sigma from "
      "1/sqrt(3) -- CONSISTENT WITH BOTH",
      "so the distance-free estimator does NOT discriminate them either")

check(k_cen * tot_frac < 0.076,
      f"E2  it IS an improvement on the corpus's 0.076: sigma(kappa) = {k_cen*tot_frac:.3f}, a factor "
      f"{0.076/(k_cen*tot_frac):.2f}",
      "the gain is real but modest, and it comes entirely from removing the distance systematic")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- ON JWST, since it was asked")
print("=" * 100)

print("""
   JWST's early massive galaxies ARE a real tension for LCDM, and MOND-class theories predict
   ACCELERATED structure formation -- McGaugh, Schombert, Lelli & Franck 2024 argue exactly that, and
   it is a genuine qualitative point in this framework's favour.  Two honest caveats:
     * *** IT IS McGAUGH'S ARGUMENT, not this framework's distinctive content, and it is CONTESTED. ***
       Do not write "we resolve it".
     * It does NOT help here.  JWST gives no local rotation curves, so it cannot measure kappa.  Where
       it COULD bite is the a_0(z) front at z ~ 1-3, where Part B's correction stops being negligible
       (0.40% at SPARC's z ~ 0.03 becomes tens of percent at z ~ 2 on a DESI-like fork).
   *** So JWST is a front to open, not an input to this measurement. ***""")

check(dev_D < 0.01 and a0z(2.0, -0.9, -0.4) != 1.0,
      "F1  and the reason is quantitative: the a_0(z) correction is "
      f"{dev_D*100:.2f}% at SPARC's z but {abs(a0z(2.0,-0.9,-0.4)-1)*100:.1f}% at z = 2 on a DESI-like fork",
      "which is why JWST-era data is the right place for a_0(z), and SPARC is not")


print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  *** THE ESTIMATOR WORKS AND IS EXACTLY DISTANCE-IMMUNE, verified on 175 real SPARC galaxies.
      A 10% common distance error moves the shape-only a_0 by {(spread_h-1)*1e6:.2f} ppm while moving the standard
      fit by {(spread_s-1)*100:.1f}%. ***  g_bar = V_bar^2/R is invariant because R ~ D and V_bar^2 ~ D cancel.

  2.  *** AND IT BUYS A REAL FACTOR: stat+distance {tot_s*100:.2f}% -> {tot_h*100:.2f}%, i.e. {tot_s/tot_h:.2f}x, on data that
      already existed. ***

  3.  *** BUT THE 'DEGENERACY BREAKING' IS AN ARTEFACT -- eighth near-miss of the session.  The two
      estimators have opposite Upsilon-dependence and cross at kappa = {k_c:.3f}, which looks like it
      breaks the a_0-Upsilon degeneracy.  Varying the BULGE M/L moves it to 0.413, and at
      Ups_bul = 0.98 the crossing vanishes entirely.  Spread {k_spread:.3f} -- WIDER than the corpus's
      existing sigma(kappa) = 0.076.  The degeneracy is RELOCATED, not broken. ***

  4.  HONEST BOTTOM LINE: kappa = {k_cen:.3f} +/- {k_cen*tot_frac:.3f} (canonical), Upsilon-dominated.
      {t_half:.2f} sigma from 1/2 and {t_isq3:.2f} sigma from 1/sqrt(3) -- consistent with BOTH.
      An improvement on 0.076 by {0.076/(k_cen*tot_frac):.2f}x, entirely from killing the distance term.

  5.  REDSHIFT SCALING CHECKED, not assumed: exactly 0.0000% on pure Lambda, {dev_D*100:.3f}% max on a
      DESI-like fork over SPARC's z = 0.0002-0.0287.  Negligible HERE; {abs(a0z(2.0,-0.9,-0.4)-1)*100:.0f}% at z = 2, which is
      where JWST-era data belongs.

  6.  JWST: a real LCDM tension and a qualitative point in the framework's favour, but it is McGAUGH'S
      argument, it is contested, and it cannot measure kappa.  A front to open, not an input here.
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f_ in FAIL:
        print(f"  - {f_}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
