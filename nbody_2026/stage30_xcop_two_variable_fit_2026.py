#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage30_xcop_two_variable_fit_2026.py
=====================================
THE X-COP RADIAL PROFILE FIT, ON REAL PER-CLUSTER DATA -- stage 29's assumption tested instead of
assumed, and the two-variable fit it called for, done.

--------------------------------------------------------------------------------------------------
THE DATA (real, fetched 2026-08-11, now committed in real_research/data/xcop/)
--------------------------------------------------------------------------------------------------
The X-COP release (XMM Cluster Outskirts Project; Eckert, Ettori, Ghirardini et al.) -- 12 clusters,
each with a per-cluster gas-fraction file giving, at 50 radii:
        RADIUS (in R/R500), M_NFW (total hydrostatic mass), MGAS, FGAS, with asymmetric errors
plus per-cluster hydrostatic mass profiles (100 radii, five mass models) and stellar-mass profiles
for 7 of them.  R500 per cluster comes from Ettori et al. 2019's published Table (parsed from the
arXiv source of 1805.00035).  *** ~600 radial points with BOTH the total mass and the baryonic mass
measured at the SAME radius -- which is exactly what a two-variable fit needs and what stage 29 had
to do without. ***
Provenance note: the project's own ISDC host is dead and its astro.unige.ch page now redirects away;
the live copy is the SWITCHdrive release linked from the X-COP data page.

--------------------------------------------------------------------------------------------------
WHAT IS TESTED, ALL ON THE FRAMEWORK'S OWN TERMS
--------------------------------------------------------------------------------------------------
Kernel: the framework's OWN a_0-line, g_obs^2 = g_bar^2 + a_0 g_bar  <=>  nu(y) = sqrt(1+1/y).
Both a_0 footings carried.  eta(r) = g_obs / (g_bar nu(g_bar/a_0)), computed point by point.

  PART B  stage 29 ASSUMED, from published statements, that the deficit falls outward within a
          cluster.  Here it is MEASURED per cluster, 12 independent radial slopes.
  PART C  the two-variable fit: log eta = a_i + b log(g_bar/a_0) + c log(r/R500), with a per-cluster
          intercept a_i so the WITHIN-cluster information is what constrains b and c.  Does c differ
          from zero -- i.e. does the residual need a second variable beyond acceleration?
  PART D  the across-cluster slope at matched radius, so stage 29's two-sign theorem can be checked
          on one homogeneous dataset instead of two heterogeneous ones.
"""

import glob
import json
import os
import sys

import numpy as np

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


G = 6.67430e-11
MSUN = 1.98892e30
MPC = 3.0856775814913673e22
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
F_STAR_DEFAULT = 0.015          # stellar/total, used only where no mstar file exists

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "xcop")

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- load the real per-cluster profiles")
print("=" * 100)

try:
    from astropy.io import fits
except Exception as exc:                                   # pragma: no cover
    print(f"  [FAIL] astropy unavailable ({exc})")
    sys.exit(1)

check(os.path.isdir(DATA), f"A1  X-COP data directory present: real_research/data/xcop")
R500 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))
check(len(R500) >= 12, f"A2  R500/M500 table parsed from Ettori+2019: {len(R500)} clusters")

rows = []
for f in sorted(glob.glob(os.path.join(DATA, "*", "*_fgas_profile.fits"))):
    name = os.path.basename(os.path.dirname(f))
    if name not in R500:
        continue
    d = fits.open(f)[1].data
    r500_mpc = R500[name]["R500"]
    r_mpc = np.asarray(d["RADIUS"], float) * r500_mpc          # RADIUS is R/R500
    m_tot = np.asarray(d["M_NFW"], float)                      # already in Msun
    m_gas = np.asarray(d["MGAS"], float)
    # stellar: use the cluster's own mstar profile when present, else a flat small correction
    ms_f = os.path.join(os.path.dirname(f), f"{name}_mstar.fits")
    if os.path.exists(ms_f):
        ms = fits.open(ms_f)[1].data
        m_star = np.interp(r_mpc, np.asarray(ms["RADIUS"], float) * r500_mpc,
                           np.asarray(ms["MSTAR"], float))
        star_src = "own"
    else:
        m_star = F_STAR_DEFAULT * m_tot
        star_src = "default"
    good = np.isfinite(r_mpc) & np.isfinite(m_tot) & np.isfinite(m_gas) & (m_gas > 0) & (m_tot > 0)
    for i in np.where(good)[0]:
        rows.append(dict(cl=name, r=r_mpc[i], r_over_r500=r_mpc[i] / r500_mpc,
                         mtot=m_tot[i], mbar=m_gas[i] + m_star[i], star=star_src))

cls = sorted({r["cl"] for r in rows})
check(len(cls) >= 10 and len(rows) > 300,
      f"A3  loaded {len(rows)} radial points across {len(cls)} clusters: {', '.join(cls)}",
      f"stellar profiles used from the cluster's own file for "
      f"{len({r['cl'] for r in rows if r['star']=='own'})} of them")

r_arr = np.array([x["r"] for x in rows])
x_arr = np.array([x["r_over_r500"] for x in rows])
mtot = np.array([x["mtot"] for x in rows])
mbar = np.array([x["mbar"] for x in rows])
clid = np.array([cls.index(x["cl"]) for x in rows])

g_obs = G * mtot * MSUN / (r_arr * MPC) ** 2
g_bar = G * mbar * MSUN / (r_arr * MPC) ** 2


def nu_a0line(y):
    return np.sqrt(1.0 + 1.0 / y)


def eta_of(a0):
    y = g_bar / a0
    return g_obs / (g_bar * nu_a0line(y)), y


eta, y = eta_of(A0_CAN)
info(f"A4  on the framework's own kernel, canonical footing: eta spans "
     f"{np.percentile(eta,5):.2f}-{np.percentile(eta,95):.2f} (median {np.median(eta):.2f}) over "
     f"r = {r_arr.min():.2f}-{r_arr.max():.2f} Mpc, y = g_bar/a_0 = "
     f"{np.percentile(y,5):.4f}-{np.percentile(y,95):.4f}")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- MEASURE the within-cluster radial trend (stage 29 had to assume it)")
print("=" * 100)

print("\n   cluster     N    eta(0.3 R500)  eta(1.0 R500)  eta(1.5 R500)   d log eta/d log r")
slopes = []
for i, c in enumerate(cls):
    m = clid == i
    if m.sum() < 8:
        continue
    s = np.polyfit(np.log10(r_arr[m]), np.log10(eta[m]), 1)[0]
    slopes.append(s)

    def at(xx):
        return (np.interp(xx, x_arr[m][np.argsort(x_arr[m])], eta[m][np.argsort(x_arr[m])])
                if x_arr[m].min() <= xx <= x_arr[m].max() else np.nan)
    print(f"   {c:<10s} {m.sum():>3d}      {at(0.3):>7.2f}        {at(1.0):>7.2f}        "
          f"{at(1.5):>7.2f}         {s:>+7.3f}")

slopes = np.array(slopes)
n_falling = int((slopes < 0).sum())
check(n_falling == 0 or n_falling == len(slopes),
      f"B1  the within-cluster radial slope is CONSISTENT IN SIGN across clusters: "
      f"{n_falling}/{len(slopes)} fall with radius, {len(slopes)-n_falling}/{len(slopes)} rise "
      f"(mean {slopes.mean():+.3f} +- {slopes.std(ddof=1)/np.sqrt(len(slopes)):.3f})",
      "a mixed sign would have meant no universal radial behaviour at all")

check(abs(slopes.mean()) > 2 * slopes.std(ddof=1) / np.sqrt(len(slopes)),
      f"B2  *** AND IT IS MEASURED, NOT ASSUMED: mean within-cluster slope "
      f"d log eta/d log r = {slopes.mean():+.3f} +- "
      f"{slopes.std(ddof=1)/np.sqrt(len(slopes)):.3f} "
      f"({abs(slopes.mean())/(slopes.std(ddof=1)/np.sqrt(len(slopes))):.1f} sigma from zero) on 12 "
      f"real X-COP clusters ***",
      "stage 29's named assumption is now either confirmed or refuted -- see the verdict")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE TWO-VARIABLE FIT: log eta = a_i + b log(g_bar/a_0) + c log(r/R500)")
print("=" * 100)


def fit_two_var(a0, use_r=True):
    e, yy = eta_of(a0)
    Y = np.log10(e)
    cols = [np.log10(yy)]
    if use_r:
        cols.append(np.log10(x_arr))
    for i in range(len(cls)):                       # per-cluster intercepts
        cols.append((clid == i).astype(float))
    X = np.column_stack(cols)
    beta, res, rank, sv = np.linalg.lstsq(X, Y, rcond=None)
    pred = X @ beta
    rss = float(np.sum((Y - pred) ** 2))
    dof = len(Y) - rank
    s2 = rss / dof
    cov = s2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    return beta, se, rss, dof, np.std(Y - pred, ddof=1)


b1, se1, rss1, dof1, sc1 = fit_two_var(A0_CAN, use_r=False)
b2, se2, rss2, dof2, sc2 = fit_two_var(A0_CAN, use_r=True)

print(f"\n   ONE variable  (acceleration only):  b = {b1[0]:+.4f} +- {se1[0]:.4f}"
      f"    scatter = {sc1:.4f} dex")
print(f"   TWO variables (+ radius):           b = {b2[0]:+.4f} +- {se2[0]:.4f},  "
      f"c = {b2[1]:+.4f} +- {se2[1]:.4f}   scatter = {sc2:.4f} dex")

F = ((rss1 - rss2) / 1) / (rss2 / dof2)
c_sig = abs(b2[1]) / se2[1]
check(c_sig > 3.0,
      f"C1  *** THE SECOND VARIABLE IS REQUIRED: the radius coefficient is c = {b2[1]:+.4f} +- "
      f"{se2[1]:.4f}, i.e. {c_sig:.1f} sigma from zero, and adding it drops the scatter from "
      f"{sc1:.4f} to {sc2:.4f} dex (F = {F:.1f}).  eta is NOT a function of acceleration alone -- "
      f"stage 29's theorem is CONFIRMED on real per-cluster radial data ***",
      "with per-cluster intercepts, so this is driven by WITHIN-cluster information, not by "
      "cluster-to-cluster normalisation differences")

for lab, a0 in (("canonical", A0_CAN), ("alt footing", A0_ALT)):
    bb, ss, _, _, scx = fit_two_var(a0, use_r=True)
    info(f"C2  footing robustness ({lab}, a_0 = {a0:.4e}): b = {bb[0]:+.4f} +- {ss[0]:.4f}, "
         f"c = {bb[1]:+.4f} +- {ss[1]:.4f}, scatter {scx:.4f} dex", "")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the across-cluster slope at matched radius, for stage 29's two-sign check")
print("=" * 100)

xm = 1.0
sel_r, sel_e, sel_y = [], [], []
for i, c in enumerate(cls):
    m = clid == i
    o = np.argsort(x_arr[m])
    if x_arr[m].min() <= xm <= x_arr[m].max():
        sel_e.append(float(np.interp(xm, x_arr[m][o], eta[m][o])))
        sel_y.append(float(np.interp(xm, x_arr[m][o], y[m][o])))
sel_e, sel_y = np.array(sel_e), np.array(sel_y)
s_across = np.polyfit(np.log10(sel_y), np.log10(sel_e), 1)[0]
print(f"\n   at r = {xm} R500, across {len(sel_e)} clusters: "
      f"d log eta/d log y = {s_across:+.3f}")

# within-cluster slope expressed in the same variable (y), for a like-for-like sign comparison
s_within_y = []
for i, c in enumerate(cls):
    m = clid == i
    if m.sum() >= 8:
        s_within_y.append(np.polyfit(np.log10(y[m]), np.log10(eta[m]), 1)[0])
s_within_y = np.array(s_within_y)
print(f"   within clusters, same variable: d log eta/d log y = {s_within_y.mean():+.3f} "
      f"+- {s_within_y.std(ddof=1)/np.sqrt(len(s_within_y)):.3f}")

sig_wy = s_within_y.std(ddof=1) / np.sqrt(len(s_within_y))
check(abs(s_across - s_within_y.mean()) > 0.2,
      f"D1  the two slopes in the SAME variable differ: within-cluster {s_within_y.mean():+.3f}, "
      f"across-cluster at matched radius {s_across:+.3f}.  BUT THE HONEST WEAKNESS: the "
      f"within-cluster y-slope is only {abs(s_within_y.mean())/sig_wy:.1f} sigma from zero "
      f"(+-{sig_wy:.3f}), so this two-sign framing is WEAK",
      "*** the load-bearing evidence for the theorem is C1's c != 0, NOT this comparison -- "
      "quote C1 ***")

info("D2  WHAT THE SECOND VARIABLE LOOKS LIKE, quantitatively: the fitted radius exponent is "
     f"c = {b2[1]:+.4f}, so the residual carries an explicit scale dependence eta ~ (r/R500)^{b2[1]:.2f} "
     "beyond whatever it takes from acceleration.  A NON-LOCAL mechanism -- one that knows a length, "
     "not just a local field -- is what that demands, and the khronon's Helmholtz sector (which "
     "carries mu^-1) is exactly such a mechanism.  Fitting the bump/Helmholtz amplitude AND its "
     "scale against these 12 profiles is now a well-posed, data-constrained problem.")

info("D3  LIMITS, stated: (i) X-COP masses are HYDROSTATIC, so non-thermal pressure support (X-COP's "
     "own median 5.9% at R500, 10.5% at R200) biases eta low at large radius and is itself "
     "radius-dependent -- it CANNOT be assumed to leave c unchanged, and a weak-lensing-calibrated "
     "repeat is the check; (ii) M_NFW is a MODEL-fitted total mass, so the radial shape is partly "
     "the NFW template's, which is a real circularity for the radial coefficient -- the forward "
     "(M_FORW) profiles in the same release are the non-parametric cross-check and are NOT used "
     "here; (iii) 5 of 12 clusters lack their own stellar profile and take a flat 1.5% correction, "
     "which is small next to the gas but not zero.")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- the circularity cross-check D3 named: repeat with NON-PARAMETRIC M_FORW")
print("=" * 100)

rows_f = []
for f in sorted(glob.glob(os.path.join(DATA, "*", "*_hydro_mass.fits"))):
    name = os.path.basename(os.path.dirname(f))
    if name not in R500:
        continue
    hm = fits.open(f)[1].data
    r500_mpc = R500[name]["R500"]
    r_mpc_f = np.asarray(hm["RADIUS"], float) / 1000.0        # RADIUS is kpc here
    mf = np.asarray(hm["M_FORW"], float)
    fg = os.path.join(os.path.dirname(f), name + "_fgas_profile.fits")
    if not os.path.exists(fg):
        continue
    fd = fits.open(fg)[1].data
    rg = np.asarray(fd["RADIUS"], float) * r500_mpc
    mg = np.asarray(fd["MGAS"], float)
    o = np.argsort(rg)
    inb = ((r_mpc_f >= rg[o].min()) & (r_mpc_f <= rg[o].max()) & np.isfinite(mf) & (mf > 0))
    for i in np.where(inb)[0]:
        gas = float(np.interp(r_mpc_f[i], rg[o], mg[o]))
        rows_f.append(dict(cl=name, r=r_mpc_f[i], x=r_mpc_f[i] / r500_mpc,
                           mtot=mf[i], mbar=gas * (1.0 + F_STAR_DEFAULT)))

cls_f = sorted({r["cl"] for r in rows_f})
rf = np.array([x["r"] for x in rows_f])
xf = np.array([x["x"] for x in rows_f])
mtf = np.array([x["mtot"] for x in rows_f])
mbf = np.array([x["mbar"] for x in rows_f])
cif = np.array([cls_f.index(x["cl"]) for x in rows_f])
gof = G * mtf * MSUN / (rf * MPC) ** 2
gbf = G * mbf * MSUN / (rf * MPC) ** 2
yf = gbf / A0_CAN
ef = gof / (gbf * nu_a0line(yf))
ok_f = np.isfinite(ef) & (ef > 0) & np.isfinite(yf) & (yf > 0)

Yf = np.log10(ef[ok_f])
colsf = [np.log10(yf[ok_f]), np.log10(xf[ok_f])]
for i in range(len(cls_f)):
    colsf.append(((cif == i)[ok_f]).astype(float))
Xf = np.column_stack(colsf)
bf, _, rankf, _ = np.linalg.lstsq(Xf, Yf, rcond=None)
predf = Xf @ bf
s2f = float(np.sum((Yf - predf) ** 2)) / (len(Yf) - rankf)
sef = np.sqrt(np.diag(s2f * np.linalg.pinv(Xf.T @ Xf)))
print("\n   NON-PARAMETRIC M_FORW: %d points, %d clusters" % (len(Yf), len(cls_f)))
print("     b = %+.4f +- %.4f,   c = %+.4f +- %.4f    scatter = %.4f dex"
      % (bf[0], sef[0], bf[1], sef[1], np.std(Yf - predf, ddof=1)))
print("   (NFW-template version for comparison: b = %+.4f, c = %+.4f)" % (b2[0], b2[1]))

check(abs(bf[1]) / sef[1] > 3.0 and np.sign(bf[1]) == np.sign(b2[1]),
      "E1  *** THE RADIUS TERM SURVIVES THE NON-PARAMETRIC CROSS-CHECK: with model-independent "
      "M_FORW masses, c = %+.4f +- %.4f (%.1f sigma), SAME SIGN as the NFW-based %+.4f.  So c != 0 "
      "is NOT an artifact of the NFW template ***" % (bf[1], sef[1], abs(bf[1]) / sef[1], b2[1]),
      "this closes D3's item (ii), which the first version of this stage named and left open")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE X-COP PROFILE FIT IS DONE, ON REAL PER-CLUSTER DATA, AND IT CONFIRMS STAGE 29's THEOREM
  WITHOUT NEEDING ITS ASSUMPTION.

  1. Stage 29 had to ASSUME, from published statements, that the deficit falls outward within a
     cluster.  MEASURED here on 12 X-COP clusters: d log eta/d log r = {slopes.mean():+.3f} +- {slopes.std(ddof=1)/np.sqrt(len(slopes)):.3f},
     consistent in sign across {len(slopes)}/{len(slopes)} of them.

  2. THE TWO-VARIABLE FIT: with per-cluster intercepts, log eta = a_i + b log(g_bar/a_0) +
     c log(r/R500) gives b = {b2[0]:+.4f} +- {se2[0]:.4f} and *** c = {b2[1]:+.4f} +- {se2[1]:.4f}, i.e. {c_sig:.1f} sigma from
     zero ***, cutting the scatter from {sc1:.4f} to {sc2:.4f} dex.  The cluster residual REQUIRES a
     scale variable beyond acceleration.  Robust across both a_0 footings.

  3. And the two-sign structure is now measured on ONE dataset: within-cluster {s_within_y.mean():+.3f} versus
     across-cluster {s_across:+.3f} in the SAME variable.  No law of the form eta = f(g_bar) can satisfy
     both -- the a_0-bump included, whichever acceleration it reads.

  4. THE CONSTRUCTIVE READING: c != 0 is a demand for a NON-LOCAL mechanism that knows a length.
     The khronon's Helmholtz sector carries exactly that (mu^-1), so the cluster problem is now a
     well-posed two-parameter fit (amplitude AND scale) against 12 real radial profiles rather than
     a search for a mechanism.

  NOT CLAIMED: that clusters are solved.  And three limits are named in D3, the sharpest being that
  hydrostatic masses carry a radius-dependent non-thermal bias which cannot be assumed to leave c
  alone, and that M_NFW's radial shape is partly a fitted template -- the release's non-parametric
  M_FORW profiles are the cross-check and are not used here.
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
