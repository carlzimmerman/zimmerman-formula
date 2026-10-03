#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG309 POST HOC diagnostics (NOT frozen; written after the main run; nothing here changes a frozen check, vote or the decision).
They read the main run's per-galaxy fits (cfg309_per_galaxy.csv: the busy-function parameters of the frozen n = 2 fits) and the main JSON.
kappa = 1/2 is FITTED.

Why: the frozen T4 width is W50 at 50 % of the MAXIMUM of the fitted profile.  MM26 S4.5 defines its W50 at 50 % of the AVERAGE of the two peaks
of the fitted profile.  For an asymmetric double horn, average < maximum, so the catalogue's definition gives a wider W50 than the frozen one, and
that difference is a method offset of the same sign as the main run's T4 lean (m_R < 0).  The main run's in-script 'POSTHOC_avg_two_peaks' line is
WRONG: it took the outermost local maxima of the fitted function over the whole grid, which include tiny numerical bumps in the far wings
(median W50avg/W50max 1.95).  PH1 replaces it.

Reading rules (fixed before the first run of this script):
  PH1  catalogue-definition W50: local maxima of the fitted B(v) - b0 with height >= 0.2 P (P = the maximum); if >= 2 such maxima, the reference level is
       the mean of the outermost two (left-most and right-most); if 1, P.  W50 = the outermost crossings of 0.5 x reference (outside in, linear
       interpolation, 0.05 km/s grid).  Variant PH1b: the mean of the two HIGHEST such maxima.  Reported: m_R = median log(W50_PH1 / W50_cat) and
       m_O = median(that + log(1+z)) with the frozen bootstrap (B 4000, seed 3094) on the frozen GOOD set, and how the frozen T4L/T4S readings WOULD read
       on these widths.  This is a diagnostic of the method offset, not a vote.
  PH2  the same on the frozen variants' sets (NBFLAG 0; 3-sigma clipped).
  PH3  Delta (frozen and PH1) by z tercile of the GOOD set: median and n; REST predicts flat medians, OBS predicts medians falling as -log(1+z).
  PH4  how much of the frozen m_R the PH1 definition removes: median(Delta_PH1 - Delta_frozen).
Writes cfg309_posthoc.out and cfg309_posthoc_results.json.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LOG, NUM = [], {}
TAU = 0.010


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def busy(v, p, n=2):
    a, b1, b2, w, ve, dd, h, b0 = p
    vp = ve + dd * w
    return a / 4.0 * (erf(b1 * (w + v - ve)) + 1.0) * (erf(b2 * (w - v + ve)) + 1.0) * (h * np.abs(v - vp) ** n / w ** n + 1.0) + b0


def width_at(vg, y, ref):
    thr = 0.5 * ref; ab = np.nonzero(y >= thr)[0]
    if ab.size == 0 or ab[0] == 0 or ab[-1] == y.size - 1: return np.nan
    lo, hi = int(ab[0]), int(ab[-1])
    vlo = vg[lo - 1] + (thr - y[lo - 1]) / (y[lo] - y[lo - 1]) * (vg[lo] - vg[lo - 1])
    vhi = vg[hi + 1] + (thr - y[hi + 1]) / (y[hi] - y[hi + 1]) * (vg[hi] - vg[hi + 1])
    return float(vhi - vlo)


def widths(row):
    p = [row.a, row.b1, row.b2, row.w, row.v_e, row.d, row.h, row.b0]
    vg = np.arange(-row.V_fit - 300.0, row.V_fit + 300.0 + 0.025, 0.05)
    y = busy(vg, p) - row.b0; Pk = float(y.max())
    im = np.nonzero((y[1:-1] > y[:-2]) & (y[1:-1] >= y[2:]))[0] + 1
    im = im[y[im] >= 0.2 * Pk]
    ref_out = 0.5 * (y[im[0]] + y[im[-1]]) if im.size >= 2 else Pk
    ref_top = float(np.mean(np.sort(y[im])[-2:])) if im.size >= 2 else Pk
    return width_at(vg, y, Pk), width_at(vg, y, ref_out), width_at(vg, y, ref_top), int(im.size)


def pct(a, q=(2.5, 97.5)):
    return [float(v) for v in np.percentile(a, q)]


def readings(D, x, seed=3094, B=4000, Bs=2000):
    n = len(D); rg = np.random.default_rng(seed); I = rg.integers(0, n, size=(B, n))
    mR, mO = float(np.median(D)), float(np.median(D + x))
    ciR, ciO = pct(np.median(D[I], axis=1)), pct(np.median((D + x)[I], axis=1))
    ex = lambda c: c[0] > TAU or c[1] < -TAU
    L = "REST" if (ex(ciO) and not ex(ciR)) else ("OBS" if (ex(ciR) and not ex(ciO)) else "UNDECIDED")
    rs = np.random.default_rng(3095); Is = rs.integers(0, n, size=(Bs, n)); ii, jj = np.triu_indices(n, 1)
    dx = x[Is][:, jj] - x[Is][:, ii]; dy = D[Is][:, jj] - D[Is][:, ii]
    with np.errstate(invalid="ignore", divide="ignore"):
        bb = np.nanmedian(np.where(dx != 0, dy / dx, np.nan), axis=1)
    ciS = pct(bb)
    Sv = "REST" if (ciS[0] <= 0 <= ciS[1] and not ciS[0] <= -1 <= ciS[1]) else ("OBS" if (ciS[0] <= -1 <= ciS[1] and not ciS[0] <= 0 <= ciS[1]) else "UNDECIDED")
    return dict(n=n, mR=mR, ciR=ciR, mO=mO, ciO=ciO, T4L=L, ciS=ciS, T4S=Sv)


P(__doc__.strip())
pg = pd.read_csv(os.path.join(HERE, "cfg309_per_galaxy.csv"), dtype={"ID": str})
g = pg[pg.good.astype(str) == "True"].copy().reset_index(drop=True)
W = np.array([widths(r) for r in g.itertuples()])
g["W_max_re"], g["W_ph1"], g["W_ph1b"], g["n_peaks"] = W[:, 0], W[:, 1], W[:, 2], W[:, 3].astype(int)
P(f"\nPH0 re-evaluation of the frozen width from the saved parameters: max |W_max_re / W50_busy - 1| = {np.max(np.abs(g.W_max_re / g.W50_busy - 1)):.2e} (n {len(g)})")
x = g.log1pz.values
D0 = np.log10(g.W50_busy.values / g.W50_cat_compared.values)
D1 = np.log10(g.W_ph1.values / g.W50_cat_compared.values)
D1b = np.log10(g.W_ph1b.values / g.W50_cat_compared.values)
P(f"profiles with >= 2 peaks (>= 0.2 P): {int((g.n_peaks >= 2).sum())} of {len(g)}; median W_ph1/W50_frozen {np.median(g.W_ph1 / g.W50_busy):.4f} "
  f"(max {np.max(g.W_ph1 / g.W50_busy):.4f}); PH1b median ratio {np.median(g.W_ph1b / g.W50_busy):.4f}")
for nm, D in (("frozen (50% of max)", D0), ("PH1 (50% of mean of outermost two peaks)", D1), ("PH1b (50% of mean of two highest peaks)", D1b)):
    r = readings(D, x); NUM[nm] = r
    P(f"  {nm}: m_R {r['mR']:+.4f} ({r['ciR'][0]:+.4f}..{r['ciR'][1]:+.4f}); m_O {r['mO']:+.4f} ({r['ciO'][0]:+.4f}..{r['ciO'][1]:+.4f}); "
      f"T4L would read {r['T4L']}; slope 95% {r['ciS'][0]:+.2f}..{r['ciS'][1]:+.2f}, T4S would read {r['T4S']}")
P("\nPH2 frozen variant sets with the PH1 definition:")
nb0 = g.NBFLAG.values == 0
r = readings(D1[nb0], x[nb0]); NUM["PH2 NBFLAG 0"] = r
P(f"  NBFLAG 0 (n {r['n']}): m_R {r['mR']:+.4f} ({r['ciR'][0]:+.4f}..{r['ciR'][1]:+.4f}); m_O {r['mO']:+.4f}; T4L would read {r['T4L']}")
mm = np.median(D1); s = 1.4826 * np.median(np.abs(D1 - mm)); kp = np.abs(D1 - mm) <= 3 * s
r = readings(D1[kp], x[kp]); NUM["PH2 clipped"] = r
P(f"  3-sigma clipped (n {r['n']}): m_R {r['mR']:+.4f} ({r['ciR'][0]:+.4f}..{r['ciR'][1]:+.4f}); m_O {r['mO']:+.4f}; T4L would read {r['T4L']}")
P("\nPH3 Delta by z tercile (GOOD set):")
order = np.argsort(g.z_freq.values); terc = np.array_split(order, 3); ph3 = []
for k, t in enumerate(terc):
    row = dict(tercile=k + 1, n=len(t), z_med=float(np.median(g.z_freq.values[t])), minus_x_med=float(-np.median(x[t])), D_frozen=float(np.median(D0[t])), D_ph1=float(np.median(D1[t])))
    ph3.append(row)
    P(f"  T{k + 1} (n {len(t)}, median z {row['z_med']:.4f}): median Delta frozen {row['D_frozen']:+.4f}, PH1 {row['D_ph1']:+.4f}; OBS would predict {row['minus_x_med']:+.4f} + offset, REST a constant offset")
NUM["PH3"] = ph3
sh = float(np.median(D1 - D0)); NUM["PH4_median_shift"] = sh
P(f"\nPH4 median(Delta_PH1 - Delta_frozen) = {sh:+.4f} dex (the part of the frozen m_R that the catalogue's own peak definition accounts for)")
open(os.path.join(HERE, "cfg309_posthoc.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(lane="CFG309", script=os.path.basename(__file__), note="POST HOC; not frozen; no vote", numbers=NUM), open(os.path.join(HERE, "cfg309_posthoc_results.json"), "w"), indent=1)
