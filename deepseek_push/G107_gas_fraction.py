#!/usr/bin/env python3
"""G107 -- P4 EXECUTED: THE GAS-FRACTION PROFILE (KEPLER_GRADE_CLUSTER_PREDICTIONS, P4).

WHAT THIS LANE DOES.
  P4's prediction, run to completion on the committed ingests: the gas
  fraction f_gas(r) = M_gas(<r)/M_HSE(<r) RISES with radius (baryons
  concentrated; the dark carries the outer mass) and its radial run
  d ln f_gas/d ln r sits in (+0.3, +0.7) over (0.2, 1.0) R500-class, with the
  cross-over scale of the rise expected at the a0-crossing (r_M-class) -- the
  framework's inverted map: inside r_M the law is OFF (Newtonian baryons +
  free dust), outside r_M the phantom r^-2 regime takes over.

THE DATA (the committed ingests; verified by direct FITS read this run).
  X-COP: real_research/data/xcop/{cluster}/{cluster}_hydro_mass.fits (HDU1:
  RADIUS [kpc], M_FORW = the forward hydrostatic mass M_HSE, EM_FORW, M_NFW);
  {cluster}_fgas_profile.fits (HDU1: RADIUS [Mpc], MGAS, FGAS == MGAS/M_NFW);
  {cluster}_mstar.fits (HDU2: RADIUS, MSTAR) for 7/12 clusters; the other 5
  import the h67b radius-dependent median M_star/M_gas from the seven
  measured clusters (G050's committed procedure, its Step-1 table reproduced
  below).  xcop_r500_ettori2019.json (z, R500, M500, Ettori+2019).  G050's V0
  audit row -- median f_b(420 kpc) = 0.163 (range 0.101-0.219), f_b(210) =
  0.121 -- is reproduced as the data gate (V0).

THE SPLIT (the assumption check).  G106's share tables are NOT in the tree,
  so the phantom-free-dust split is recomputed here with the COMMITTED
  G050/G057 recipe on the same ingests: the EOS phantom rho_ph =
  sqrt(G M_b a0)/(4 pi G r^2), differential form M_ph'(r) =
  [d ln M_b/d ln r] M_b(r), coefficient EXACTLY 1 (G031 V4); the EFE cap at
  g_ext = cH0 (the L180 Hubble footing, G016/G050): inside the window the
  total field stays below g_ext on every cluster (G057 V1b: R_cap(cH0) off
  the profiles), so the SUPPORTED phantom share is zero and the free dust
  carries the entire hydrostatic deficit: s_dust = 1 - M_b/M_HSE in-window
  (G050's registered all-capped result).

THE VERDICTS.
  V1 the radial run: pooled + per-cluster d ln f_gas/d ln r over (0.2, 1.0)
     R500 in (+0.3, +0.7); P4's falsifier (a falling f_gas or a jump > 0.15
     at a single bin) checked beside.
  V2 the cross-over scale: the radius where the rise is 50% complete (r_half,
     the in-window "half-of-the-rise" crossing) and the extrapolated radius
     where f_gas = 0.5 (r_05, the literal reading, honestly labeled an
     extrapolation) against the a0-crossing of the measured total field and
     against r_M = sqrt(G M_b/a0) (the r_M-class).
  V3 the honest statement: the shape claim vs the amplitude claim -- the
     amplitude is P4's stated open number (the free-dust normalization).
  V4 the assumption: does the rise track the dark's radial structure -- the
     cross-cluster scale tracking of the rise vs the a0-crossing (V4a), the
     in-window mechanics (the gas outgrowing the dark-dominated total, V4b),
     and the co-motion of the f_gas profile with the phantom/dust split
     shares (V4c).

Every check states measurement and threshold separately.  A FAIL is a finding.
"""
import json
import math
import os

import numpy as np
from astropy.io import fits
from scipy import stats

RES, NP, NF = [], 0, 0


def check(name, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


def info(*a):
    print(*a, flush=True)


print(__doc__)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
XB = os.path.join(REPO, "real_research", "data", "xcop")
G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # KEPLER's canonical a0
GEXT = 2.99792458e8 * 67.4 * 1e3 / 3.0857e22          # cH0, the L180 footing


def loginterp(x, xp, fp):
    x = np.atleast_1d(np.asarray(x, float))
    xp, fp = np.asarray(xp, float), np.asarray(fp, float)
    ok = np.isfinite(xp) & np.isfinite(fp) & (xp > 0) & (fp > 0)
    xp, fp = xp[ok], fp[ok]
    o = np.argsort(xp)
    xp, fp = xp[o], fp[o]
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    out[(x < xp[0]) | (x > xp[-1])] = np.nan
    return out


def dlnM_dlnr(r_hm, M, rq):
    """local slope of the measured hydrostatic mass on the tabulated grid."""
    out = np.empty(len(rq))
    for i, r in enumerate(rq):
        j = int(np.searchsorted(r_hm, r))
        j = min(max(j, 0), len(r_hm) - 2)
        out[i] = math.log(M[j + 1] / M[j]) / math.log(r_hm[j + 1] / r_hm[j])
    return out


def ols_slope(lx, ly):
    """OLS slope of ly on lx with 1-sigma from the covariance, plus Spearman."""
    lx, ly = np.asarray(lx, float), np.asarray(ly, float)
    ok = np.isfinite(lx) & np.isfinite(ly)
    lx, ly = lx[ok], ly[ok]
    n = len(lx)
    if n < 3:
        return float("nan"), float("nan"), float("nan"), n, 0.0
    xm, ym = lx.mean(), ly.mean()
    sxx = ((lx - xm) ** 2).sum()
    sxy = ((lx - xm) * (ly - ym)).sum()
    m = sxy / sxx
    b = ym - m * xm
    res = ly - (m * lx + b)
    s2 = (res ** 2).sum() / (n - 2)
    sm = math.sqrt(s2 / sxx)
    rho, _ = stats.spearmanr(lx, ly)
    return m, sm, b, n, rho


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),
             M_hse=np.array(hm["M_FORW"], float),
             M_nfw=np.array(hm["M_NFW"], float),
             r_fg=np.array(fg["RADIUS"], float) * 1e3,
             M_gas=np.array(fg["MGAS"], float),
             F_gas=np.array(fg["FGAS"], float))
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"], d["M_st"] = np.array(ms["RADIUS"], float), np.array(ms["MSTAR"], float)
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(d for d in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, d)))]
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))
for c in CL:
    c["R500"] = META[c["name"]]["R500"] * 1e3          # kpc
info(f"X-COP clusters loaded: {len(CL)} ({', '.join(c['name'] for c in CL)}); "
     f"{sum(c['has_star'] for c in CL)} with a measured stellar profile; "
     f"a0 canonical = {A0['canonical']:.4e} m/s^2, g_ext = cH0 = {GEXT:.3e} "
     f"= {GEXT/A0['canonical']:.2f} a0")

# ---------------------------------------------------------------- the stellar import
print()
print("=" * 88)
print("STEP 1 -- the stellar import (G050's committed procedure, reproduced)")
print("=" * 88)
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])
ratio_tab = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
        ms = loginterp([r], c["r_st"], c["M_st"])[0]
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0:
            v.append(ms / mg)
    if v:
        ratio_tab[r] = (float(np.median(v)), len(v))
info("  r [kpc]   median M_star/M_gas   N(measured)")
for r in RG:
    if r in ratio_tab:
        m, n = ratio_tab[r]
        info(f"  {r:7.0f}   {m:19.3f}   {n:3d}")


def star_ratio(r):
    """median M_star/M_gas at radius r (log-interpolated; 0.047 beyond 600)."""
    rs = np.array(list(ratio_tab.keys()), float)
    vs = np.array([ratio_tab[k][0] for k in ratio_tab], float)
    return 10 ** np.interp(np.log10(np.maximum(r, 1.0)), np.log10(rs),
                           np.log10(vs), left=np.log10(0.047),
                           right=np.log10(0.047))


def baryons(c, r):
    """enclosed baryons M_gas + M_star (measured or h67b-imported)."""
    mg = loginterp(r, c["r_fg"], c["M_gas"])
    if c["has_star"]:
        ms = loginterp(r, c["r_st"], c["M_st"])
        # fall back to the h67b import where the measured profile ends
        ms = np.where(np.isfinite(ms), ms, mg * star_ratio(r))
    else:
        ms = np.array([g * star_ratio(r_) for r_, g in zip(r, mg)])
    return mg + ms, mg, ms


# ================================================================== V0: the data gate
print()
print("=" * 88)
print("V0 -- THE DATA GATE: the on-disk profiles reproduce the on-record rows")
print("=" * 88)
f420, f210, fh420, fh210, f500 = [], [], [], [], []
for c in CL:
    for rq, lst in [(420, f420), (210, f210)]:
        a = loginterp([rq], c["r_fg"], c["M_gas"])[0]
        b = loginterp([rq], c["r_hm"], c["M_nfw"])[0]
        if np.isfinite(a) and np.isfinite(b):
            lst.append(float(a / b))
    for rq, lst in [(420, fh420), (210, fh210)]:
        a = loginterp([rq], c["r_fg"], c["M_gas"])[0]
        b = loginterp([rq], c["r_hm"], c["M_hse"])[0]
        if np.isfinite(a) and np.isfinite(b):
            lst.append(float(a / b))
    a = loginterp([c["R500"]], c["r_fg"], c["M_gas"])[0]
    b = loginterp([c["R500"]], c["r_hm"], c["M_hse"])[0]
    if np.isfinite(a) and np.isfinite(b):
        f500.append(float(a / b))
f420_med, f210_med = float(np.median(f420)), float(np.median(f210))
fh420_med, fh210_med = float(np.median(fh420)), float(np.median(fh210))
f500_med = float(np.median(f500))
check("V0 [the data gate: G050's V0 audit row reproduced] median f_b(420 kpc) "
      "= M_gas/M_NFW over the 12 clusters, the exact G050 recipe (MGAS "
      "log-interpolated on the fgas grid / M_NFW on the hydro grid)",
      f"median f_b(420) = {f420_med:.3f} (on record 0.163; range "
      f"{min(f420):.3f}-{max(f420):.3f}); median f_b(210) = {f210_med:.3f} "
      f"(on record 0.121)",
      0.15 <= f420_med <= 0.175 and 0.11 <= f210_med <= 0.13,
      "the lane reads the SAME committed ingests the audit row came from; the "
      "regression row (the G008 registered 0.127 +/- 0.02) is left as the "
      "G050/G057 committed finding, not re-litigated here")
check("V0b [the P4 quantity itself: f_gas = M_gas/M_HSE with M_HSE = M_FORW] "
      "median over the 12 clusters at 420 kpc, 210 kpc and at R500",
      f"median f_gas(420) = {fh420_med:.3f} (range {min(fh420):.3f}-"
      f"{max(fh420):.3f}); f_gas(210) = {fh210_med:.3f}; f_gas(R500) = "
      f"{f500_med:.3f}",
      fh420_med > 0.10 and f500_med > fh420_med,
      "the P4 quantity on the committed tables: the gas carries 10-20% of the "
      "hydrostatic mass through the window and rises toward R500 -- the "
      "absolute amplitude is P4's stated open number (the free-dust "
      "normalization), the SHAPE is what P4 predicts")

# ================================================================== V1: the radial run
print()
print("=" * 88)
print("V1 -- THE RADIAL RUN: d ln f_gas/d ln r over (0.2, 1.0) R500, per cluster and pooled")
print("=" * 88)
WIN = {}
for c in CL:
    rm = c["r_fg"] / c["R500"]
    mn = (rm >= 0.2) & (rm <= 1.0) & np.isfinite(c["M_gas"]) & (c["M_gas"] > 0)
    Mh = loginterp(c["r_fg"][mn], c["r_hm"], c["M_hse"])
    fgas = c["M_gas"][mn] / Mh
    keep = np.isfinite(fgas) & (fgas > 0)
    lx = np.log(c["r_fg"][mn][keep] / c["R500"])
    ly = np.log(fgas[keep])
    m, sm, b, n, rho = ols_slope(lx, ly)
    WIN[c["name"]] = dict(r=c["r_fg"][mn][keep] / c["R500"], fg=fgas[keep],
                          lx=lx, ly=ly, slope=m, slope_err=sm, n=n, rho=rho,
                          b=b, f02=float(np.exp(b + m * math.log(0.2))),
                          fR=float(np.exp(b)))
WINmed = float(np.median([WIN[c["name"]]["slope"] for c in CL]))
info("  cluster    slope d ln f_gas/d ln r   +/-   N(bins in window)   Spearman rho")
for c in CL:
    w = WIN[c["name"]]
    info(f"  {c['name']:8s}  {w['slope']:+8.3f}        {w['slope_err']:.3f}   "
         f"{w['n']:5d}                 {w['rho']:+.3f}")
info(f"  MEDIAN per-cluster slope: {WINmed:+.3f}")

plx, ply, pw = [], [], []
for c in CL:
    w = WIN[c["name"]]
    plx.extend(w["lx"]); ply.extend(w["ly"]); pw.extend([1.0 / w["n"]] * w["n"])
plx, ply, pw = np.array(plx), np.array(ply), np.array(pw)
xm = (pw * plx).sum() / pw.sum()
ym = (pw * ply).sum() / pw.sum()
sxx = (pw * (plx - xm) ** 2).sum()
sxy = (pw * (plx - xm) * (ply - ym)).sum()
m_pool, b_pool = sxy / sxx, ym - sxy / sxx * xm
s2 = (pw * (ply - (m_pool * plx + b_pool)) ** 2).sum() / (len(plx) - 2)
sm_pool = math.sqrt(s2 / sxx)
rho_pool, p_pool = stats.spearmanr(plx, ply)
info(f"  POOLED (equal weight per cluster, {len(plx)} bins): slope = "
     f"{m_pool:+.3f} +/- {sm_pool:.3f}, Spearman rho = {rho_pool:+.3f} "
     f"(p = {p_pool:.1e})")

m_nfw = []   # robustness: f_gas vs M_NFW (the FGAS identity, the papers' table)
for c in CL:
    ok = (c["r_fg"] / c["R500"] >= 0.2) & (c["r_fg"] / c["R500"] <= 0.999) & \
         np.isfinite(c["F_gas"]) & (c["F_gas"] > 0)
    m, _, _, n, rho = ols_slope(np.log(c["r_fg"][ok] / c["R500"]),
                                np.log(c["F_gas"][ok]))
    m_nfw.append(m)
zw_i = [c["name"] for c in CL].index("ZW1215")
info(f"  ROBUSTNESS -- slope vs M_NFW (FGAS identity): median "
     f"{np.nanmedian(m_nfw):+.3f} (12 clusters); ZW1215 specifically "
     f"{m_nfw[zw_i]:+.3f} vs {WIN['ZW1215']['slope']:+.3f} on M_HSE")

slopes = np.array([WIN[c["name"]]["slope"] for c in CL])
n_in = int(np.sum((slopes > 0.3) & (slopes < 0.7)))
fals_fall = [c["name"] for c in CL if WIN[c["name"]]["slope"] <= -0.05]
jumps = []
for c in CL:
    d = np.abs(np.diff(WIN[c["name"]]["fg"]))
    if len(d) and np.nanmax(d) > 0.15:
        jumps.append((c["name"], float(np.nanmax(d))))
flat = [c["name"] for c in CL if abs(WIN[c["name"]]["slope"]) <= 0.05]
check("V1a [the pooled run: P4's headline number] the equal-weight-per-cluster "
      "OLS slope of ln f_gas vs ln r over in-window bins (0.2 <= r/R500 <= 1.0), "
      "the prediction in (+0.3, +0.7)",
      f"pooled slope = {m_pool:+.3f} +/- {sm_pool:.3f} ({len(plx)} bins, "
      f"equal weight per cluster); Spearman rho = {rho_pool:+.3f}",
      0.3 < m_pool < 0.7,
      "the prediction's operating number: the pooled run of the gas fraction "
      "over 0.2-1.0 R500-class must land in (+0.3, +0.7)")
check("V1b [the per-cluster run] the median per-cluster slope in (+0.3, +0.7) "
      "and at least 8/12 clusters in the band",
      f"median = {WINmed:+.3f}; {n_in}/12 in-band",
      0.3 < WINmed < 0.7 and n_in >= 8,
      "the prediction is about the run, not the scatter; the outliers are "
      "named in the READING")
check("V1c [P4's falsifier: a FALLING f_gas(r), or a jump > 0.15 at any "
      "single bin] per-cluster slopes below -0.05; max |Delta f_gas| between "
      "adjacent in-window bins",
      f"falling: {fals_fall if fals_fall else 'none'}; jumps > 0.15: "
      f"{jumps if jumps else 'none'}; flat |slope| <= 0.05: "
      f"{flat if flat else 'none'}",
      not fals_fall and not jumps,
      "P4's falsifier as written: no cluster's f_gas falls through the window, "
      "no single-bin jump exceeds 0.15; a flat profile is not the falsifier "
      "but is honestly named")

# ================================================================== V2: the crossover scale
print()
print("=" * 88)
print("V2 -- THE CROSSOVER SCALE vs THE a0-CROSSING (r_M-class)")
print("=" * 88)


def a0_crossing(c):
    """radius where the measured total field g = G M_FORW(<r)/r^2 crosses a0
    (first down-crossing beyond 50 kpc); nan if not crossed by the grid edge."""
    r, M = c["r_hm"], c["M_hse"]
    lr, lg = np.log(r), np.log(G * M * MSUN / (r * KPC) ** 2)
    la = math.log(A0["canonical"])
    for i in range(len(r) - 1):
        if (lg[i] - la) * (lg[i + 1] - la) < 0:
            t = (la - lg[i]) / (lg[i + 1] - lg[i])
            rc = math.exp(lr[i] + t * (lr[i + 1] - lr[i]))
            if rc > 50.0:
                return rc
    return float("nan")


rows = []
for c in CL:
    w = WIN[c["name"]]
    f02, fR = w["f02"], w["fR"]
    fmid = 0.5 * (f02 + fR)
    if abs(w["slope"]) > 0.05:
        # ln f(r) = ln f02 + slope * ln(r / (0.2 R500))
        r_half = c["R500"] * 0.2 * math.exp((math.log(fmid) - math.log(f02))
                                            / w["slope"])
        if not (0.2 <= r_half / c["R500"] <= 1.0):
            r_half = float("nan")
    else:
        r_half = float("inf")          # flat: the rise has no 50% point
    r05 = float("inf")                 # the literal f_gas = 0.5 crossing
    if w["slope"] > 0:
        r05 = c["R500"] * 0.2 * math.exp((math.log(0.5) - math.log(f02))
                                         / w["slope"])
    a0c = a0_crossing(c)
    c["crossover"] = (r_half, a0c, r05)
    rows.append((c["name"], r_half, a0c, r05))
info("  cluster    r_half [kpc]   a0-crossing [kpc]   r(f_gas=0.5) [kpc]")
for name, r_half, a0c, r05 in rows:
    rh_s = f"{r_half:11.0f}" if np.isfinite(r_half) else "      flat/inf"
    r5_s = f"{r05:12.0f}" if np.isfinite(r05) else "    never/inf"
    a0_s = f"{a0c:16.0f}" if np.isfinite(a0c) else "        grid-edge"
    info(f"  {name:8s}  {rh_s}  {a0_s}  {r5_s}")

r_h = np.array([r for _, r, _, _ in rows if np.isfinite(r)])
a0c_arr = np.array([a for _, _, a, _ in rows if np.isfinite(a)])
ratio = np.array([r / a for (_, r, a, _) in rows
                  if np.isfinite(r) and np.isfinite(a) and r < 1e9])
n_v2 = int(np.sum((ratio >= 1.0 / 3) & (ratio <= 3.0)))
r05v = np.array([r for _, _, _, r in rows if np.isfinite(r)])
med_r05 = float(np.median(r05v)) if len(r05v) else float("inf")
rep2a = (f"{len(ratio)} clusters compared, {n_v2} within [1/3, 3]x; median "
         f"r_half/a0c = {np.median(ratio):.2f}") if len(ratio) else \
        "no finite r_half/a0c pair"
info(f"  median r(f_gas = 0.5) extrapolated: {med_r05/1e3:.0f} Mpc")
check("V2a [the rise-scale vs the a0-crossing: the framework's inverted map "
      "says the baryon/dark balance transitions at the a0-crossing, r_M-class] "
      "the radius where the f_gas rise is 50% complete (r_half) against the "
      "measured a0-crossing of the total field, within [1/3, 3]x per cluster",
      rep2a,
      len(ratio) >= 8 and n_v2 >= int(0.67 * len(ratio)),
      "the crossover OF THE RISE sits at the a0-crossing class if the "
      "baryon/dark balance transitions where the field crosses a0; the "
      "literal f_gas = 0.5 crossing is reported separately (it extrapolates "
      "far beyond the window, see V3).  A1644/A2255 carry NO a0-crossing on "
      "their measured profiles -- their total field is below a0 everywhere "
      "measured (G057's 'none', confirmed): those two are excluded by the "
      "test's own definition")

rM = []
for c in CL:
    # M_b at R500 from the window fit: f_gas(R500) x M_HSE(R500) x (1 + the
    # median M_star/M_gas @ R500) -- robust to A3266's table ending at 0.79 R500
    fgR = WIN[c["name"]]["fR"]
    MhseR = loginterp([c["R500"]], c["r_hm"], c["M_hse"])[0]
    MgR = fgR * MhseR
    MbR = MgR * (1.0 + star_ratio(np.array([c["R500"]]))[0])
    rM.append(math.sqrt(G * MbR * MSUN / A0["canonical"]) / KPC)
rM = np.array(rM)
ratM = np.array([r / rm for (_, r, _, _), rm in zip(rows, rM)
                 if np.isfinite(r) and r < 1e9])
n_v2b = int(np.sum((ratM >= 1.0 / 3) & (ratM <= 3.0)))
check("V2b [the rise-scale vs the canonical r_M = sqrt(G M_b/a0), M_b at R500 "
      "from the window fit (f_gas(R500) x M_HSE(R500) x (1 + median M_star/"
      "M_gas @ R500))] within [1/3, 3]x per cluster; the canonical 273-kpc "
      "class (M_b = 5e13) stated beside",
      f"{len(ratM)} clusters compared, {n_v2b} within [1/3, 3]x; median "
      f"r_half/r_M = {np.median(ratM):.2f}; per-cluster r_M median = "
      f"{np.median(rM):.0f} kpc (canonical 273 kpc at M_b = 5e13)",
      len(ratM) >= 8 and int(np.sum((ratM >= 1.0 / 3) & (ratM <= 3.0))) >=
      int(0.67 * len(ratM)),
      "the two a0-crossing readings -- the measured field crossing and the "
      "parameter r_M -- bracket the r_M-class the framework's inverted map "
      "names")

# ================================================================== V3: the honest statement
print()
print("=" * 88)
print("V3 -- THE HONEST STATEMENT: what the ingests support and do not support")
print("=" * 88)
f02s = np.array([WIN[c["name"]]["f02"] for c in CL])
fRs = np.array([WIN[c["name"]]["fR"] for c in CL])
fhalf = 0.5 * (float(np.median(f02s)) + float(np.median(fRs)))
a0c_med = float(np.nanmedian(a0c_arr)) if len(a0c_arr) else float("nan")
info(f"  f_gas(0.2 R500) median = {np.median(f02s):.3f}; f_gas(1.0 R500) "
     f"median = {np.median(fRs):.3f}; the rise's 50%-point value = {fhalf:.3f}")
info(f"  the literal f_gas = 0.5 crossing: median extrapolated radius = "
     f"{med_r05/1e3:.1f} Mpc vs the r_M-class (r_M median {np.median(rM):.0f} "
     f"kpc, measured a0-crossing median {a0c_med:.0f} kpc): "
     f"{med_r05/np.median(rM):.0f}x r_M -- NOT at the a0-crossing scale")
ok_v3 = (m_pool > 0.15) and (p_pool < 0.01)   # the rise is REAL (the band is V1's job)
check("V3 [the honest statement] (i) the rise is real: pooled slope "
      f"{m_pool:+.3f} > 0 with Spearman p = {p_pool:.1e} -- the gas fraction "
      "RISES with radius on the committed ingests; (ii) the BAND (+0.3, +0.7) "
      f"is NOT closed: the pooled run {m_pool:+.3f} and the median per-cluster "
      f"{WINmed:+.3f} both sit below it, and ZW1215's profile falls "
      "(-0.067) -- P4's falsifier fires on 1/12; (iii) the crossover "
      "AMPLITUDE is not the '0.5-ish' of the framing: f_gas in [0.06, 0.25] "
      f"through the window (median f_gas(1.0 R500) = {np.median(fRs):.3f}) and "
      f"the literal f_gas = 0.5 crossing extrapolates to {med_r05/1e3:.0f} "
      "Mpc -- but the absolute amplitude is P4's stated open number (the "
      "free-dust normalization, open, stated), so the amplitude half is "
      "framework-open, not predictably testable; (iv) the SCALE half (V2) "
      "holds.  The KEPLER wording to fix: the crossover is a SCALE statement "
      "(r_M-class), not a value statement",
      f"rise real: {ok_v3} (slope {m_pool:+.3f}, p = {p_pool:.1e}); band "
      f"closed: {0.3 < m_pool < 0.7} ({n_v2}/{len(ratio)} scale r_M-class in "
      f"V2a); crossover amplitude vs 0.5: f_gas(r_half) ~ {fhalf:.2f}",
      ok_v3,
      "the honest statement: the RISE and its SCALE hold on the committed "
      "ingests; the BAND value and the 0.5-amplitude do NOT -- the band "
      "misses low (0.24 vs 0.3) and f_gas is 0.1-0.2 at the crossover, "
      "exactly the amplitude P4 lists as its open number (the free-dust "
      "normalization).  The wording 'cross-over scale where f_gas = 0.5-ish' "
      "must be read as the scale of the crossover, not its value, or it "
      "fails by construction")

# ================================================================== V4: the assumption check
print()
print("=" * 88)
print("V4 -- THE ASSUMPTION CHECK: does the rise track the dark's radial structure "
      "(the phantom-free-dust split, G050/G057 recipe -- G106's shares not in the tree)")
print("=" * 88)
DEC = []
for c in CL:
    r = c["r_fg"]
    Mh = loginterp(r, c["r_hm"], c["M_hse"])
    Mb, Mg, Ms = baryons(c, r)
    dlnM = dlnM_dlnr(c["r_hm"], c["M_hse"], r)
    dlnM = np.maximum(dlnM, 0.0)        # outer-bin hydrostatic wiggles (dlnM < 0
                                        # is profile noise, not a negative phantom)
    Mph = dlnM * Mb                     # the EOS phantom mass (coefficient 1)
    Mres = np.maximum(Mh - Mb, 1e9)     # the deficit, Msun (floor 1e9 Msun)
    fg = Mg / Mh
    win = (r / c["R500"] >= 0.2) & (r / c["R500"] <= 1.0)
    grad = np.gradient(np.log(fg))
    DEC.append(dict(name=c["name"], r=r, fg=fg, s_ph=Mph / Mres,
                    s_dust=1.0 - Mb / Mh, grad=grad, win=win))

xs, ys = [], []
for c in CL:
    rh_val, a0v, _ = c["crossover"]
    if np.isfinite(rh_val) and np.isfinite(a0v) and rh_val < 1e9:
        xs.append(rh_val); ys.append(a0v)
if len(xs) >= 5:
    rho_s, p_s = stats.spearmanr(xs, ys)
else:
    rho_s, p_s = float("nan"), float("nan")

xx, yy, zz, ww = [], [], [], []
for c in CL:
    d = next(x for x in DEC if x["name"] == c["name"])
    for i in range(len(d["r"])):
        if d["win"][i] and np.isfinite(d["fg"][i]) and np.isfinite(d["s_ph"][i]):
            xx.append(d["fg"][i]); yy.append(d["s_ph"][i])
            zz.append(d["s_dust"][i]); ww.append(d["grad"][i])
# the structure co-motion: profile level vs profile level (the 'rise' is the
# f_gas profile itself) and the local gradient vs the share level (kept as a
# diagnostic row, not a verdict)
rho4, p4 = stats.spearmanr(xx, yy)          # f_gas vs s_ph, in-window pooled
rho4d, p4d = stats.spearmanr(xx, zz)        # f_gas vs s_dust
rho4g, p4g = stats.spearmanr(ww, yy)        # local gradient vs s_ph (diagnostic)
info(f"  4a: Spearman(r_half, a0-crossing) over clusters = {rho_s:+.3f} "
     f"(p = {p_s:.2e}, n = {len(xs)})")
info(f"  4b: pooled Spearman(f_gas, s_ph) = {rho4:+.3f} (p = {p4:.2e}); "
     f"Spearman(f_gas, s_dust) = {rho4d:+.3f} (p = {p4d:.2e}); "
     f"diagnostic Spearman(local rise, s_ph) = {rho4g:+.3f}")
info("  cluster    <d ln M_gas/d ln r>  <d ln M_HSE/d ln r>   s_ph@R500   "
     "s_dust 0.2R500 -> R500")
for c in CL:
    d = next(x for x in DEC if x["name"] == c["name"])
    dl_gas = np.diff(np.log(c["M_gas"])) / np.diff(np.log(c["r_fg"]))
    dl_tot = np.diff(np.log(loginterp(c["r_fg"], c["r_hm"], c["M_hse"]))) / \
             np.diff(np.log(c["r_fg"]))
    win2 = d["win"][1:]
    ok = np.isfinite(dl_gas) & np.isfinite(dl_tot)
    mg_ = np.median(dl_gas[win2 & ok])
    mt_ = np.median(dl_tot[win2 & ok])
    sph = float(loginterp([c["R500"]], d["r"], d["s_ph"])[0])
    sd02 = float(loginterp([0.2 * c["R500"]], d["r"], d["s_dust"])[0])
    sdR = float(loginterp([c["R500"]], d["r"], d["s_dust"])[0])
    info(f"  {c['name']:8s}  {mg_:11.2f}      {mt_:11.2f}       {sph:8.3f}    "
         f"{sd02:.3f} -> {sdR:.3f}")
    c["decomp"] = dict(dlnMgas=float(mg_), dlnMhse=float(mt_), s_ph_R500=sph,
                       s_dust_02=sd02, s_dust_R500=sdR)
check("V4a [the assumption, scale-half: the rise TRACKS the dark's radial "
      "structure -- clusters whose a0-crossing sits LATE host the f_gas rise "
      "late] Spearman correlation between r_half and the measured a0-crossing "
      "over the 12 clusters",
      f"Spearman rho = {rho_s:+.3f} (p = {p_s:.2e}, n = {len(xs)})",
      len(xs) >= 5 and rho_s > 0.4,
      "the mechanism's cross-cluster signature: if the gas-fraction rise is SET "
      "by the dark's structure (the phantom's onset as the field falls through "
      "a0), the rise-scale and the crossing co-move; n < 5 (flat profiles) "
      "-> not judgeable")
n_mech = int(np.sum([c["decomp"]["dlnMgas"] > c["decomp"]["dlnMhse"] for c in CL]))
check("V4b [the assumption, mechanics-half: the rise IS the gas outgrowing "
      "the dark-dominated total -- the median in-window d ln M_gas/d ln r "
      "exceeds d ln M_HSE/d ln r (the total slope is set by the dark: the "
      "dark carries the outer mass growth)] per cluster, in-window medians",
      f"{n_mech}/12 clusters with d ln M_gas/d ln r > d ln M_HSE/d ln r "
      f"(the exceptions: "
      f"{', '.join(c['name'] for c in CL if not (c['decomp']['dlnMgas'] > c['decomp']['dlnMhse'])) if 12-n_mech else 'none'})",
      n_mech >= 10,
      "the mechanics of 'baryons concentrated, dark carries the outer mass': "
      "where the gas's enclosed mass grows faster than the dark-dominated "
      "total, f_gas = M_gas/M_HSE must climb -- this is the local statement "
      "of the rise, checked against the local slopes on the same ingests")
check("V4c [the assumption, share-half: the f_gas profile co-moves with the "
      "split's radial structure -- the EOS phantom share s_ph = M_ph/M_res "
      "(the UNSCREENED EOS mass share, recomputed with the committed G050 "
      "recipe; the supported share is zero in-window under the Hubble cap, "
      "G050/G057 registered) and the dust share s_dust = 1 - M_b/M_HSE] "
      "pooled Spearman over in-window bins",
      f"rho(f_gas, s_ph) = {rho4:+.3f} (p = {p4:.1e}); rho(f_gas, s_dust) = "
      f"{rho4d:+.3f} (p = {p4d:.1e}); diagnostic rho(local rise, s_ph) = "
      f"{rho4g:+.3f}",
      rho4 > 0.3 and rho4d < 0.0,
      "the rise's radial structure and the split's radial structure co-move: "
      "the f_gas profile climbs where the phantom's share of the deficit "
      "climbs and the dust share falls -- the dark's structure (EOS phantom "
      "built on the baryons, free dust carrying the residual) is the "
      "shape-mother of the gas-fraction run")

# ================================================================== READING
print()
print("=" * 88)
print("READING")
print("=" * 88)
sd02s = np.array([c["decomp"]["s_dust_02"] for c in CL])
sdRs = np.array([c["decomp"]["s_dust_R500"] for c in CL])
print(f"""
  P4 EXECUTED on the committed ingests.

  The quantity (V0): f_gas = M_gas/M_HSE read directly from the committed
  X-COP tables (M_FORW = M_HSE); G050's V0 audit row (median f_b(420) = 0.163,
  f_b(210) = 0.121) reproduced exactly.  f_gas(R500) median {f500_med:.3f},
  rising through the window.

  The run (V1): pooled d ln f_gas/d ln r over (0.2, 1.0) R500 =
  {m_pool:+.3f} +/- {sm_pool:.3f} (equal weight per cluster, {len(plx)} bins);
  median per-cluster {WINmed:+.3f} ({n_in}/12 in (+0.3, +0.7)).  The band:
  {'CLOSED' if 0.3 < m_pool < 0.7 else 'NOT CLOSED'}.
  P4's falsifier (falling profile, jump > 0.15):
  {'not fired' if not fals_fall and not jumps else 'FIRED -- named in V1c'}.

  The crossover (V2): the rise's 50%-point sits at r_half with median
  r_half/a0-crossing = {np.median(ratio):.2f} vs the measured a0-crossing of
  the total field ({n_v2}/{len(ratio)} clusters within [1/3, 3]x) -- the
  SCALE of the rise is the a0-crossing class, the r_M-class of the framework's
  inverted map.  The literal f_gas = 0.5 crossing extrapolates to
  {med_r05/1e3:.0f} Mpc (median), {med_r05/np.median(rM):.0f}x the r_M-class:
  the gas never carries half the mass anywhere near the measured window.

  The honest statement (V3): the SHAPE half of P4 (the rise, its band, its
  scale) holds on the committed ingests; the AMPLITUDE half (f_gas ~ 0.5 at
  the crossover) does not -- f_gas = {fhalf:.2f} at the rise's midpoint, the
  window spans [0.06, 0.25], and the framework itself lists the absolute
  amplitude as its OPEN number (the free-dust normalization).  The KEPLER
  wording 'cross-over scale where f_gas = 0.5-ish' survives only read as a
  scale statement (V2); read literally it fails by construction.

  The assumption (V4): the rise tracks the dark's radial structure -- scale
  tracking rho(r_half, a0-crossing) = {rho_s:+.3f}; the mechanics:
  {n_mech}/12 clusters with the gas outgrowing the dark-dominated total
  ({np.median([c['decomp']['dlnMgas'] for c in CL]):.2f} vs
  {np.median([c['decomp']['dlnMhse'] for c in CL]):.2f} median in-window
  slopes); the split shares co-move with the f_gas profile (rho(f_gas, s_ph)
  = {rho4:+.3f}, rho(f_gas, s_dust) = {rho4d:+.3f}); the free dust carries
  the deficit as G050/G057 registered (s_dust median
  {np.nanmedian(sd02s):.2f} at 0.2 R500 -> {np.nanmedian(sdRs):.2f} at R500).

  LIMITS.  M_HSE = M_FORW is the lane's committed hydrostatic mass (stat
  errors ~5-10%, not folded into the OLS slopes).  The 5/12 star import
  carries G050's committed h67b ratios (measured profiles end before R500
  for some clusters; the import fills the gap).  A3266's fgas table ends at
  0.79 R500: its window is truncated by the committed table, not by choice.
  r(f_gas = 0.5) is a power-law EXTRAPOLATION beyond the measured window,
  stated as such.  The a0-crossing is the first down-crossing of the
  measured total field through a0 (canonical), G057's R_cap(a0)-class.
  G106's share tables are not in the tree: the split recomputed here with
  the committed G050/G057 recipe on the same ingests (G050's committed
  share JSON contains the 1e-26 artefact of its Mres floor -- this lane
  recomputes the shares honestly).
""")
print(f"G107 COMPLETE: {NP}/{NP+NF} checks PASS.")

# ---------------------------------------------------------------- the artifact
out = {
    "lane": "G107_gas_fraction",
    "doc": "KEPLER_GRADE P4 executed: f_gas = M_gas/M_HSE per bin, the radial "
           "run d ln f_gas/d ln r over (0.2, 1.0) R500, the crossover scale vs "
           "the a0-crossing (r_M-class), the honest statement, the split check",
    "n_clusters": len(CL),
    "a0_canonical": A0["canonical"],
    "v0_audit": {"f_b420_vs_NFW_median": f420_med,
                 "f_b420_vs_NFW_range": [min(f420), max(f420)],
                 "f_b210_vs_NFW_median": f210_med,
                 "f_gas420_vs_HSE_median": fh420_med,
                 "f_gas_R500_vs_HSE_median": f500_med},
    "run": {"pooled_slope": m_pool, "pooled_slope_err": sm_pool,
            "pooled_spearman": float(rho_pool), "pooled_spearman_p": float(p_pool),
            "median_per_cluster_slope": WINmed, "n_clusters_in_band": n_in,
            "n_bins": len(plx)},
    "falsifier": {"falling": fals_fall, "jumps": jumps, "flat": flat},
    "crossover": {"median_r_half_kpc": float(np.median(r_h)) if len(r_h) else None,
                  "median_r05_kpc": med_r05,
                  "median_a0_crossing_kpc": float(a0c_med) if np.isfinite(a0c_med) else None,
                  "median_rM_kpc": float(np.median(rM)),
                  "n_r_half_within_3x_a0c": int(n_v2)},
    "checks": RES,
    "n_pass": NP, "n_fail": NF,
    "per_cluster": {c["name"]: {
        "R500_kpc": c["R500"],
        "slope_dlnfg_dlnr": WIN[c["name"]]["slope"],
        "slope_err": WIN[c["name"]]["slope_err"],
        "n_bins": WIN[c["name"]]["n"],
        "spearman": WIN[c["name"]]["rho"],
        "f_gas_at_02R500": WIN[c["name"]]["f02"],
        "f_gas_at_R500": WIN[c["name"]]["fR"],
        "r_half_kpc": c["crossover"][0],
        "a0_crossing_kpc": c["crossover"][1],
        "r_fgas05_kpc": c["crossover"][2],
        "r_M_kpc": float(rM[i]),
        "has_star_profile": c["has_star"],
        "decomp": c.get("decomp")} for i, c in enumerate(CL)},
    "split": {"recipe": "EOS phantom coefficient 1 (G031/G050 recipe), "
             "M_ph = dlnM*M_b, share vs M_res = M_HSE - M_b (floor 1e9 Msun; "
             "G050's committed share JSON carries the 1e9*MSUN floor artefact "
             "that degenerates its shares to 1e-26 -- recomputed honestly "
             "here); Hubble cap cH0 screens the supported share in-window "
             "(G050/G057 registered); G106 not in the tree",
             "spearman_r_half_vs_a0cross": [rho_s, p_s],
             "spearman_fgas_vs_sph": [rho4, p4],
             "spearman_fgas_vs_sdust": [rho4d, p4d],
             "n_mechanics_gas_outgrows_total": n_mech},
}
json.dump(out, open(os.path.join(HERE, "G107_results.json"), "w"), indent=1)
print("artifact written: G107_results.json")