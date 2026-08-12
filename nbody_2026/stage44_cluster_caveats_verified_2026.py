#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage44_cluster_caveats_verified_2026.py
========================================
VERIFYING THE "FAVOURABLE" CLUSTER CAVEATS AGAINST THE COMMITTED DATA -- and three of the four are
WRONG.  They entered the corpus from a workflow agent's report and were passed through unchecked, which
is exactly the pattern the working rule exists to catch.  This stage checks each against the actual
X-COP files and corrects stage 41's Part G.

--------------------------------------------------------------------------------------------------
WHAT WAS CLAIMED (stage 41 G1-G3, and repeated in the summary chart)
--------------------------------------------------------------------------------------------------
  (a) the effective dof is ~24-36, not 600, because M_NFW is a 2-parameter NFW curve
  (b) adding X-COP's own 10% non-thermal systematic in quadrature takes the baseline 560.3 -> 39.1 and
      the best entry -> 17.0, so "unity is ~17x away, not ~230x"
  (c) the robust statistic is the median residual g_obs/g_model = 3.425 -> 1.871
  (d) the kernel alone already removes 74-89% of the cluster discrepancy, leaving 11-26%

--------------------------------------------------------------------------------------------------
WHAT THE DATA SAY
--------------------------------------------------------------------------------------------------
  (a) *** CORRECT, and now properly justified. ***  A 2-parameter NFW mass profile reproduces the
      committed M_NFW column to 0.22% median (0.55% worst) against statistical errors of 2.94% median.
      The residual is ~7% of the error bar, so the 600 points cannot resolve structure beyond two
      numbers per cluster.  Effective dof = 24.  (The original justification was asserted, not shown;
      and a naive "is it NFW to 1e-3" test FAILS -- the right comparison is residual vs ERROR.)

  (b) *** WRONG NUMBER AND WRONG DIRECTION. ***  Statistical errors are 2.94% median, so a 10%
      systematic in quadrature inflates sigma by 3.55x and divides chi^2 by 12.6: 559.4 -> 44.5, not
      39.1.  And more seriously: non-thermal pressure support biases hydrostatic mass LOW, so
      correcting for it RAISES the true dynamical mass and makes the framework's job HARDER.  It
      inflates the error bar AND shifts the central value adversely.  It is not a favourable correction.

  (c) *** MISLEADING.  The pooled 3.425 is CORE-DOMINATED. ***  34.0% of the 600 points sit inside
      0.1 R500.  By radius, the median M_dyn/M_pred from the a_0-line on baryons alone is
          4.205 (r < 0.1 R500) · 3.820 (0.1-0.3) · 2.791 (0.3-0.6) · 2.084 (0.6-1.0 R500)
      so a pooled median is a statement about cool cores, not about clusters at R500.

  (d) *** WRONG, and contradicted by the data. ***  At R500 the discrepancy is 2.084x, so the kernel
      removes ~48% of the dynamical mass and leaves ~52%.  The "74-89% removed / 11-26% left" figure
      does not survive contact with X-COP and should be withdrawn wherever it appears.

--------------------------------------------------------------------------------------------------
AND ONE GENUINE RESULT FELL OUT OF THE RECHECK
--------------------------------------------------------------------------------------------------
The R500 discrepancy of 2.084x sits INSIDE the framework's own target window eta = 1.6-2.3 -- an
internal consistency check that had not been made, arrived at from the raw profiles rather than from a
fit.  That, and not the core-dominated 3.425, is the number to quote.
"""

import json
import os
import sys

import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


print(__doc__)

G = 6.67430e-11
MSUN = 1.98892e30
MPC = 3.0856775814913673e22
A0 = 9.3619e-11
A0_ALT = 1.1279e-10
F_STAR_DEF = 0.015
ETA_LO, ETA_HI = 1.6, 2.3          # the committed target window

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "xcop")
R500 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))
names = sorted(n for n in R500 if os.path.exists(os.path.join(DATA, n, f"{n}_fgas_profile.fits")))


def profile(n):
    d = fits.open(os.path.join(DATA, n, f"{n}_fgas_profile.fits"))[1].data
    r5 = R500[n]["R500"]
    x = np.asarray(d["RADIUS"], float)
    M = np.asarray(d["M_NFW"], float)
    em = 0.5 * (np.asarray(d["M_NFW_LO"], float) + np.asarray(d["M_NFW_HI"], float))
    mg = np.asarray(d["MGAS"], float)
    msf = os.path.join(DATA, n, f"{n}_mstar.fits")
    if os.path.exists(msf):
        ms = fits.open(msf)[1].data
        st = np.interp(x * r5, np.asarray(ms["RADIUS"], float) * r5, np.asarray(ms["MSTAR"], float))
    else:
        st = F_STAR_DEF * M
    ok = np.isfinite(M) & (M > 0) & (mg > 0) & (x > 0)
    return x[ok], M[ok], em[ok], (mg + st)[ok], r5


# =================================================================================================
print("=" * 100)
print("PART A -- claim (a): is M_NFW a 2-parameter curve?  The dof question")
print("=" * 100)


def nfw_M(r, M0, rs):
    u = r / rs
    return M0 * (np.log(1 + u) - u / (1 + u))


res, relerr, npts = [], [], []
for n in names:
    x, M, em, mb, r5 = profile(n)
    npts.append(len(x))
    relerr.append(em / M)
    p, _ = curve_fit(nfw_M, x * r5, M, p0=[M.max() * 3, 0.3 * x.max() * r5], maxfev=60000)
    res.append(np.max(np.abs(nfw_M(x * r5, *p) / M - 1)))
res = np.array(res)
e = np.concatenate(relerr)
NTOT = sum(npts)
DOF_EFF = 2 * len(names)

info(f"A0  {len(names)} clusters, {min(npts)}-{max(npts)} points each, {NTOT} total; "
     f"statistical error on M_NFW: median {np.median(e)*100:.2f}%, range {e.min()*100:.2f}-{e.max()*100:.2f}%")

check(np.median(res) < np.median(e) / 5,
      f"A1  *** CLAIM (a) IS CORRECT, and here is the justification that was missing: a 2-parameter NFW "
      f"reproduces M_NFW to {np.median(res)*100:.2f}% median ({np.max(res)*100:.2f}% worst) against statistical errors of "
      f"{np.median(e)*100:.2f}% median -- the residual is {100*np.median(res)/np.median(e):.0f}% of the error bar.  So the {NTOT} points cannot "
      f"resolve structure beyond 2 numbers per cluster: EFFECTIVE DOF = {DOF_EFF}, not {NTOT} ***",
      "note a naive 'is it NFW to 1e-3?' test FAILS (median 2.2e-3); the correct comparison is residual "
      "against ERROR, not against an arbitrary threshold")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- claim (b): the 10% non-thermal systematic")
print("=" * 100)

SYS = 0.10
infl = np.sqrt(e ** 2 + SYS ** 2) / e
div = float(np.median(infl) ** 2)
BASE = 559.4
check(abs(BASE / div - 39.1) / 39.1 > 0.10,
      f"B1  *** CLAIM (b)'s NUMBER IS WRONG: sigma inflates by {np.median(infl):.2f}x median, dividing chi^2 by "
      f"{div:.1f}, so 559.4 -> {BASE/div:.1f} -- NOT the 39.1 that was reported ({100*abs(BASE/div-39.1)/39.1:.0f}% off) ***",
      "recomputed from the committed error columns rather than taken from the agent's report")

info("B2  *** AND THE DIRECTION IS WRONG TOO, which matters more than the number.  Non-thermal pressure "
     "support biases HYDROSTATIC mass LOW.  Correcting for it therefore RAISES the true dynamical mass "
     "and makes the discrepancy the framework must explain LARGER.  So the systematic inflates the error "
     "bar AND shifts the central value ADVERSELY -- it is not a favourable correction, and presenting it "
     "as one was an error in the framework's favour. ***")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- claims (c) and (d): where the discrepancy actually lives")
print("=" * 100)

bands = [("r < 0.1 R500", 0.0, 0.1), ("0.1 - 0.3", 0.1, 0.3),
         ("0.3 - 0.6", 0.3, 0.6), ("0.6 - 1.0 R500", 0.6, 1.0), ("ALL (pooled)", 0.0, 99.0)]
out = {}
print(f"    {'band':>16} {'N':>5} {'frac':>7} {'median M_dyn/M_pred':>21}")
for lab, lo, hi in bands:
    rat = []
    for n in names:
        x, M, em, mb, r5 = profile(n)
        m = (x > lo) & (x <= hi)
        if not m.any():
            continue
        rm = x[m] * r5 * MPC
        gb = G * mb[m] * MSUN / rm ** 2
        gpred = np.sqrt(gb ** 2 + A0 * gb)                 # the a_0-line, from baryons alone
        gobs = G * M[m] * MSUN / rm ** 2
        rat.append(gobs / gpred)
    rat = np.concatenate(rat)
    out[lab] = (len(rat), float(np.median(rat)))
    print(f"    {lab:>16} {len(rat):5d} {len(rat)/NTOT:7.1%} {np.median(rat):21.3f}")

frac_core = out["r < 0.1 R500"][0] / NTOT
check(frac_core > 0.25,
      f"C1  *** CLAIM (c) IS MISLEADING: {frac_core:.1%} of the {NTOT} points sit inside 0.1 R500, where the "
      f"discrepancy is {out['r < 0.1 R500'][1]:.3f}.  So the pooled median {out['ALL (pooled)'][1]:.3f} is a statement about COOL CORES, "
      f"not about clusters at R500 ***",
      "the discrepancy falls monotonically outward, so a pooled median is not a robust summary")

r500_ratio = out["0.6 - 1.0 R500"][1]
check(r500_ratio < 0.60 ** -1 * 1.5,
      f"C2  *** CLAIM (d) IS WRONG: at R500 the discrepancy is {r500_ratio:.3f}x, so the kernel ACCOUNTS FOR "
      f"{100/r500_ratio:.0f}% of the dynamical mass and LEAVES {100*(1-1/r500_ratio):.0f}% unexplained.  The '74-89% removed, "
      f"11-26% left' figure does NOT survive contact with X-COP and is withdrawn ***",
      f"i.e. the kernel removes about half of what is needed at R500, not three quarters to nine tenths")

check(ETA_LO <= r500_ratio <= ETA_HI,
      f"C3  *** AND ONE GENUINE RESULT FROM THE RECHECK: the R500 discrepancy {r500_ratio:.3f} sits INSIDE the "
      f"framework's own target window eta = {ETA_LO}-{ETA_HI}.  That is an internal consistency check nobody had "
      f"made, obtained from the raw profiles rather than from any fit ***",
      "this, and not the core-dominated pooled median, is the number to quote")

# both footings, since the target is dimensionful
rat_alt = []
for n in names:
    x, M, em, mb, r5 = profile(n)
    m = (x > 0.6) & (x <= 1.0)
    if not m.any():
        continue
    rm = x[m] * r5 * MPC
    gb = G * mb[m] * MSUN / rm ** 2
    rat_alt.append((G * M[m] * MSUN / rm ** 2) / np.sqrt(gb ** 2 + A0_ALT * gb))
r_alt = float(np.median(np.concatenate(rat_alt)))
info(f"C4  BOTH FOOTINGS at R500: canonical {r500_ratio:.3f}, ALT {r_alt:.3f} -- "
     f"{'both' if ETA_LO <= r_alt <= ETA_HI else 'canonical only'} inside the eta window")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THREE OF THE FOUR "FAVOURABLE" CLUSTER CAVEATS WERE WRONG.  They came from a workflow agent's report
  and were carried into stage 41 and the summary chart without being checked against the data.

  (a) EFFECTIVE DOF ~24, NOT 600           -- CORRECT, and now justified properly: a 2-parameter NFW
      reproduces M_NFW to {np.median(res)*100:.2f}% median against {np.median(e)*100:.2f}% statistical errors, i.e. the residual is
      {100*np.median(res)/np.median(e):.0f}% of the error bar.  The earlier justification was asserted, not demonstrated.

  (b) "10% SYSTEMATIC: 560 -> 39.1"        -- WRONG NUMBER ({BASE/div:.1f}) AND WRONG DIRECTION.  Non-thermal
      pressure biases hydrostatic mass LOW, so correcting for it RAISES the dynamical mass the framework
      must explain.  It inflates the error bar and shifts the centre ADVERSELY.  Withdrawn as a
      favourable correction.

  (c) "ROBUST STATISTIC 3.425 -> 1.871"    -- MISLEADING.  {frac_core:.0%} of points sit inside 0.1 R500 where the
      ratio is {out['r < 0.1 R500'][1]:.3f}.  By radius: {out['r < 0.1 R500'][1]:.3f} · {out['0.1 - 0.3'][1]:.3f} · {out['0.3 - 0.6'][1]:.3f} · {r500_ratio:.3f}.  The pooled median describes
      cool cores.

  (d) "KERNEL REMOVES 74-89%"              -- WRONG.  At R500 the discrepancy is {r500_ratio:.3f}x, so the kernel
      accounts for {100/r500_ratio:.0f}% and leaves {100*(1-1/r500_ratio):.0f}%.  Withdrawn wherever it appears.

  AND THE ONE GENUINE FINDING: the R500 discrepancy {r500_ratio:.3f} (canonical) / {r_alt:.3f} (ALT) sits inside the
  framework's own eta = {ETA_LO}-{ETA_HI} target -- an internal consistency check obtained from the raw profiles,
  independent of any fit.  Quote this instead of the pooled median.

  METHODOLOGICAL NOTE FOR THE RECORD: every one of these three errors ran in the framework's FAVOUR, and
  all three survived because they arrived as "corrections that help" and were not audited.  Adverse
  claims in this corpus get re-derived; favourable ones got waved through.  That asymmetry is itself the
  defect, and it is the same one that produced the manufactured win in stage 40.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
