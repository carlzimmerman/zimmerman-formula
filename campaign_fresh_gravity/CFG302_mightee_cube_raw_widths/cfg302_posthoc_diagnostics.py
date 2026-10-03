#!/usr/bin/env python3
"""CFG302 POST HOC diagnostics (NOT frozen; dated 2026-10-02; written after the first main and MUTATE runs; no map entry or check of the
frozen runs is changed).  Two things in the frozen main run need a diagnosis: C-OFF(b) FAILED (the robust std of S/N_win in the
line-free offset windows is 0.489, so the frozen error model over-states window-sum errors by about 2x), and the flux scale
DIFFERS (lower) by -0.30 dex with only 58 of 179 sources detected at the frozen S/N_L >= 5.  This script re-extracts the same aperture
spectra with the frozen script's own functions (identical code path) and asks four questions.  READING RULES, fixed before this script
was first run:

PH1 (noise at long lags): pooled over the primary set, F(n) = Var(n-channel block sums) / (n sigma_ch^2) by MAD, for n = 1 ... 128 in the
     frozen noise bands.  If F(64) and F(128) are below 0.5 F(8), window-sum noise is suppressed at long lags (the spectra behave as if
     high-pass filtered) and the frozen sigma_S, which assumes F is flat beyond 8 channels, over-states window-sum errors.  PH1b re-scales
     the C-OFF S/N_win with F interpolated at each window's length: if its robust std lands in [0.75, 1.33], PH1 explains the C-OFF(b)
     failure.
PH2 (recalibrated detection): with k = the robust std of S/N_L in the offset windows (C-OFF), a "calibrated 5 sigma" is S/N_L >= 5k.
     Counts at that threshold in the main run, in the offset windows and in the MUTATE run are reported; if the offset or MUTATE
     windows give more than 5 % false detections at that threshold, the recalibration is not clean and only the frozen counts stand.
     The width and flux comparisons are repeated on the recalibrated set (reported, not map entries).
PH3 (what the flux deficit depends on): over ALL primary sources the median linear S_win/S_cat in terciles of the catalogue SNR_3D, and
     Spearman correlations of log(S_win/S_cat) (recalibrated set) with SNR_3D, W50_cat, z and log S_cat.  A ratio rising with SNR_3D
     (Spearman > 0.3, p < 0.01) toward 1 in the top tercile means the deficit sits in the faint sources (consistent with catalogue flux
     boosting near the detection limit or with residual-flux scaling in the cube; this lane cannot tell which); a flat dependence means a
     global scale (beam area or units); a ratio falling with W50_cat at fixed SNR_3D is consistent with spectral filtering of broad lines.
PH4 (aperture completeness): S_win in apertures of 1.0, 1.5, 2.0 and 2.5 theta for the recalibrated set; a point source gives 0.9375,
     0.998, 1.000, 1.000 of its flux.  If the median S(2.5 theta)/S(1.5 theta) exceeds 1.10, emission extends beyond the frozen aperture
     (the frozen flux is incomplete); within 1.00 +- 0.05 the frozen aperture is complete.
Checks: PH0 the re-extraction reproduces the frozen CSV's S_win and W50 for every primary source (code-path identity), to 1e-5 relative.

RUN 1 (kept as cfg302_posthoc_diagnostics_run1.out / _run1_results.json) demanded 1e-9 relative, which cannot pass against a CSV written
to 6 significant figures (rounding up to 5e-6 relative): a design flaw in the check, so PH0 failed for all 179 sources in run 1.  Run 2
uses 1e-5 relative; PH1-PH4 and their reading rules are unchanged; one reported line in PH4 now uses a NaN-aware median.
RUN 2 (kept as cfg302_posthoc_diagnostics_run2.out / _run2_results.json) still failed PH0 for 37 sources: the frozen script's CSV
(%.6g) had rounded the INPUT columns too (freq_MHz 1383.623 -> 1383.62, shifting some windows by up to ~1 km/s).  The frozen script's
CSV format was then raised to %.10g (no computation changed: its main and MUTATE JSONs are identical before and after; first outputs
kept as *_run1*), and run 3 (this output) reads the full-precision CSV.  PH1-PH5 and their rules are unchanged from run 2.
PH5 (ADDED AFTER RUN 1, rule fixed before run 2): the aperture spectra of the PH2 recalibrated set, each divided by the catalogue's mean
     flux density S_cat / (W50_cat nu_c / c) and put on u = v / (W50_cat / 2), are averaged with equal weights.  If the mean of the stack
     over the flanks 1.2 < |u| < 3 lies below -3 sigma (sigma from the scatter of the per-source flank means), the spectra carry negative
     bowls beside the lines, the signature of a spectral filter that took part of the line; if within +-3 sigma of zero, no bowl is seen.
     The stack's mean over |u| < 1 is reported against 1 (the catalogue's mean flux density).
Outputs: cfg302_posthoc_diagnostics.out, cfg302_posthoc_diagnostics_results.json.
"""
import os, sys, json, math, importlib.util
import numpy as np, pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cfg302", os.path.join(HERE, "cfg302_raw_widths.py")); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
OUT = os.path.join(HERE, "cfg302_posthoc_diagnostics")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok):
    CHK.append((name, bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


main = pd.read_csv(os.path.join(HERE, "cfg302_per_galaxy.csv")); mut = pd.read_csv(os.path.join(HERE, "cfg302_per_galaxy_MUTATE.csv"))
prim = main[main.primary == 1].reset_index(drop=True)
cubes = c.load_cubes()
NG = c.NG; OWN = c.owner(np.arange(NG))
BMAJ = np.array([cubes[OWN[g]]["bmaj"][g - 1000 * OWN[g]] for g in range(NG)]); BMIN = np.array([cubes[OWN[g]]["bmin"][g - 1000 * OWN[g]] for g in range(NG)])
VALID = (BMAJ >= 50) & (BMAJ <= 120) & (BMIN >= 50) & (BMIN <= 120)
med_beam = {k: float(np.median(BMAJ[(OWN == k) & VALID])) for k in range(4)}
BMAJ_eff = np.where(VALID, BMAJ, [med_beam[k] for k in OWN]); BMIN_eff = np.where(VALID, BMIN, [med_beam[k] for k in OWN])
A_g = math.pi * BMAJ_eff * BMIN_eff / (4 * math.log(2)) / c.PIX ** 2
cat = pd.read_csv(c.CAT).set_index("ID_catalogue")

P("CFG302 POST HOC diagnostics (not frozen; reading rules in the docstring, fixed before the first run)")
NS = [1, 2, 4, 8, 16, 32, 64, 128]; pool = {n: [] for n in NS}; ph0_bad = []; growth = []; offres = []; stacks = {}
for i, r in prim.iterrows():
    nu_c = r.freq_MHz * 1e6; w50c = r.W50_cat; Vw = r.V_w_kms; side = int(r.O_side); vO = 2 * Vw + 100.0
    span = 3 * Vw + 1100.0
    v_lo = -span if side >= 0 else -(vO + span); v_hi = (vO + span) if side > 0 else span
    g_lo = max(int(math.floor(c.g_of_nu(c.nu_of_v(nu_c, v_hi)))) - 2, 0); g_hi = min(int(math.ceil(c.g_of_nu(c.nu_of_v(nu_c, v_lo)))) + 2, NG - 1)
    nu_O = c.nu_of_v(nu_c, side * vO)
    gs, sp, pt, edge, info = c.aperture_spectrum(cubes, r.RA_deg, r.Dec_deg, g_lo, g_hi, r.R_ap_arcsec, BMAJ_eff, A_g)
    Om = np.abs(c.C * (nu_O / c.nu_g(gs) - 1)) <= Vw
    m, v, W, L, N = c.measure(gs, sp, nu_c, w50c, excl=Om, rng=None, nmc=0)
    if not (abs(m["S_win"] / r.S_win_Jy_Hz - 1) <= 1e-5 and ((np.isnan(m["W50"]) and np.isnan(r.W50_rest_kms)) or abs(m["W50"] / r.W50_rest_kms - 1) <= 1e-5)):
        ph0_bad.append(r.ID)
    sig = m["sigma_ch"]; idx = np.nonzero(N)[0]; runs = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1)
    for n in NS:
        for rr in runs:
            for j in range(0, rr.size - n + 1, n): pool[n].append(sp[rr[j:j + n]].sum() / (sig * math.sqrt(n)))
    vOr = c.C * (nu_O / c.nu_g(gs) - 1); Wo = np.abs(vOr) <= Vw; Lo = np.abs(vOr) <= w50c / 2 + 50
    offres.append(dict(ID=r.ID, nW=int(Wo.sum()), nL=int(Lo.sum()), sumW=float(sp[Wo].sum()), sumL=float(sp[Lo].sum()), sig=sig))
    ugrid = np.arange(-8.0, 8.0001, 0.1); uu = v / (w50c / 2.0); o_ = np.argsort(uu)
    norm = r.S_cat / (w50c * nu_c / c.C * 1.0)                                              # catalogue mean flux density [Jy] (W50 in km/s -> Hz via nu_c / c)
    stk = np.interp(ugrid, uu[o_], sp[o_] / norm, left=np.nan, right=np.nan); stk[(ugrid < uu.min()) | (ugrid > uu.max())] = np.nan
    stacks[r.ID] = stk
    row = dict(ID=r.ID, snr_L=r.snr_L)                                                       # aperture growth for every primary source (PH4 reads the recalibrated set)
    for f in (1.0, 1.5, 2.0, 2.5):
        g2, s2, _, e2, _ = c.aperture_spectrum(cubes, r.RA_deg, r.Dec_deg, int(gs[W].min()), int(gs[W].max()), f * r.beam_arcsec, BMAJ_eff, A_g)
        row[f"S{f}"] = float(c.DNU * s2.sum()); row[f"edge{f}"] = bool(e2)
    growth.append(row)

check("PH0 the re-extraction reproduces the frozen CSV's S_win and W50 to 1e-5 relative (the CSV now carries 10 significant figures) for every primary source", f"mismatches: {ph0_bad}", len(ph0_bad) == 0)

P("\n== PH1 noise at long lags (pooled over the primary set; F(n) = robust var of n-channel block sums / (n sigma_ch^2)) ==")
F = {}
for n in NS:
    a = np.array(pool[n]); F[n] = float((1.4826 * np.median(np.abs(a - np.median(a)))) ** 2) if a.size >= 30 else float("nan")
    P(f"  n = {n:4d}: F = {F[n]:.3f}  (blocks {len(pool[n])})")
read1 = F[64] < 0.5 * F[8] and F[128] < 0.5 * F[8]
P(f"  F(64)/F(8) = {F[64] / F[8]:.3f}, F(128)/F(8) = {F[128] / F[8]:.3f} -> {'window-sum noise SUPPRESSED at long lags' if read1 else 'no strong long-lag suppression by the rule'}")
lnF = np.interp(np.log([o['nW'] for o in offres]), np.log(NS), np.log([F[n] for n in NS]))
lnFL = np.interp(np.log([o['nL'] for o in offres]), np.log(NS), np.log([F[n] for n in NS]))
snrW_emp = np.array([o["sumW"] / (o["sig"] * math.sqrt(o["nW"] * math.exp(l))) for o, l in zip(offres, lnF)])
snrL_emp = np.array([o["sumL"] / (o["sig"] * math.sqrt(o["nL"] * math.exp(l))) for o, l in zip(offres, lnFL)])
sdW = c.mad_sigma(snrW_emp); sdL = c.mad_sigma(snrL_emp)
P(f"  PH1b C-OFF S/N with F(n) at each window's length: robust std S/N_win {sdW:.3f}, S/N_L {sdL:.3f} (frozen: 0.489 / 0.497) -> "
  f"{'PH1 explains the C-OFF(b) failure' if 0.75 <= sdW <= 1.33 else 'PH1 does not fully explain it'}")
NUM["PH1"] = dict(F=F, suppressed=read1, robust_std_win_rescaled=sdW, robust_std_L_rescaled=sdL)

P("\n== PH2 recalibrated detection (k = robust std of S/N_L in the offset windows) ==")
k = c.mad_sigma(prim.off_SNR_L); thr = 5 * k
nmain = int((prim.snr_L >= thr).sum()); noff = int((np.abs(prim.off_SNR_L) >= thr).sum())
pm = mut[mut.primary == 1]; nmut = int((pm.snr_L >= thr).sum()); nmut_abs = int((np.abs(pm.snr_L) >= thr).sum())
clean = noff <= 0.05 * len(prim) and nmut_abs <= 0.05 * len(pm)
P(f"  k = {k:.3f}; calibrated threshold S/N_L >= {thr:.2f}: main {nmain}/{len(prim)}; offset windows |S/N_L| >= thr {noff}/{len(prim)}; MUTATE S/N_L >= thr {nmut}/{len(pm)} (|.| {nmut_abs}) -> {'clean' if clean else 'NOT clean (only the frozen counts stand)'}")
rc = prim[(prim.snr_L >= thr) & np.isfinite(prim.W50_rest_kms)]
lw = np.log10(rc.W50_rest_kms / rc.W50_cat); ls_ = np.log10(rc.S_win_Jy_Hz[rc.S_win_Jy_Hz > 0] / rc.S_cat[rc.S_win_Jy_Hz > 0])
P(f"  recalibrated set n = {len(rc)}: W50 median log ratio {np.median(lw):+.4f} dex (robust scatter {c.mad_sigma(lw):.4f}); flux median log ratio {np.median(ls_):+.4f} dex (robust scatter {c.mad_sigma(ls_):.4f}, n {ls_.size})")
NUM["PH2"] = dict(k=k, threshold=thr, n_main=nmain, n_off=noff, n_mutate=nmut, n_mutate_abs=nmut_abs, clean=clean, n_recal=len(rc), W50_median=float(np.median(lw)), W50_scatter=c.mad_sigma(lw), S_median=float(np.median(ls_)), S_scatter=c.mad_sigma(ls_))

P("\n== PH3 what the flux deficit depends on ==")
q = prim.S_win_Jy_Hz / prim.S_cat; t = np.percentile(prim.SNR_3D_cat, [33.33, 66.67])
bins = [(-np.inf, t[0]), (t[0], t[1]), (t[1], np.inf)]
tq = [float(np.median(q[(prim.SNR_3D_cat > a) & (prim.SNR_3D_cat <= b)])) for a, b in bins]
tn = [int(((prim.SNR_3D_cat > a) & (prim.SNR_3D_cat <= b)).sum()) for a, b in bins]
P(f"  all primary, median S_win/S_cat by SNR_3D tercile (edges {t[0]:.1f}, {t[1]:.1f}): {[round(x, 3) for x in tq]} (n {tn})")
rcp = rc[rc.S_win_Jy_Hz > 0]; lr = np.log10(rcp.S_win_Jy_Hz / rcp.S_cat)
cors = {}
for nm, col in (("SNR_3D", rcp.SNR_3D_cat), ("W50_cat", rcp.W50_cat), ("z", rcp.z_HI), ("log S_cat", np.log10(rcp.S_cat))):
    rho, p = spearmanr(col, lr); cors[nm] = (float(rho), float(p)); P(f"  Spearman(log S_win/S_cat, {nm}) = {rho:+.3f} (p {p:.2g}; n {len(rcp)})")
# W50 at fixed SNR_3D: partial (residual) correlation
res = lambda y, x: y - np.polyval(np.polyfit(x, y, 1), x)
rho_w, p_w = spearmanr(res(lr.values, np.log10(rcp.SNR_3D_cat.values)), rcp.W50_cat.values)
P(f"  Spearman(residual of log ratio after a linear fit in log SNR_3D, W50_cat) = {rho_w:+.3f} (p {p_w:.2g})")
rising = cors["SNR_3D"][0] > 0.3 and cors["SNR_3D"][1] < 0.01
P(f"  reading: {'the deficit sits in the faint sources (ratio rises with SNR_3D)' if rising else 'no significant rise with SNR_3D by the rule'}; top-tercile median ratio {tq[2]:.3f}; "
  f"{'ratio falls with W50 at fixed SNR_3D (consistent with spectral filtering)' if (rho_w < -0.3 and p_w < 0.01) else 'no significant W50 dependence at fixed SNR_3D by the rule'}")
NUM["PH3"] = dict(tercile_edges=list(map(float, t)), tercile_median_ratio=tq, tercile_n=tn, spearman=cors, partial_W50=(float(rho_w), float(p_w)), rising=rising)

P("\n== PH4 aperture completeness (recalibrated set) ==")
gdf = pd.DataFrame(growth); gdf = gdf[gdf.ID.isin(rc.ID)]
rat = {f: float(np.median(gdf[f"S{f}"] / gdf["S1.5"])) for f in (1.0, 2.0, 2.5)}
P(f"  median S(R)/S(1.5 theta): 1.0 theta {rat[1.0]:.3f}, 2.0 theta {rat[2.0]:.3f}, 2.5 theta {rat[2.5]:.3f} (point source 0.939, 1.002, 1.002); n {len(gdf)}; any off-image {int(gdf[['edge2.5']].values.sum())}")
P(f"  reading: {'emission extends beyond the frozen aperture (frozen flux incomplete)' if rat[2.5] > 1.10 else ('the frozen aperture is complete' if abs(rat[2.5] - 1) <= 0.05 else 'between the two rules')}")
gall = pd.DataFrame(growth)
P(f"  all primary (any S/N): median S(2.5 theta)/S_cat {np.nanmedian(gall['S2.5'] / prim.set_index('ID').loc[gall.ID, 'S_cat'].values):.3f} vs S(1.5 theta)/S_cat {np.nanmedian(gall['S1.5'] / prim.set_index('ID').loc[gall.ID, 'S_cat'].values):.3f}; non-finite 2.5 theta apertures {int((~np.isfinite(gall['S2.5'])).sum())}")
NUM["PH4"] = dict(median_ratio_to_1p5=rat, n=len(gdf))

P("\n== PH5 stacked spectra (recalibrated set; added after run 1) ==")
ug = np.arange(-8.0, 8.0001, 0.1); S5 = np.array([stacks[i] for i in rc.ID])
mstk = np.nanmean(S5, axis=0)
fl = (np.abs(ug) > 1.2) & (np.abs(ug) < 3.0); ln = np.abs(ug) < 1.0; far = (np.abs(ug) > 4.0) & (np.abs(ug) < 8.0)
fm = np.nanmean(S5[:, fl], axis=1); lm = np.nanmean(S5[:, ln], axis=1); fr = np.nanmean(S5[:, far], axis=1)
fm, lm, fr = fm[np.isfinite(fm)], lm[np.isfinite(lm)], fr[np.isfinite(fr)]
zf = float(np.mean(fm) / (np.std(fm, ddof=1) / math.sqrt(fm.size)))
P(f"  n {S5.shape[0]}; stack mean over |u| < 1 (line): {np.mean(lm):.3f} +- {np.std(lm, ddof=1) / math.sqrt(lm.size):.3f} (catalogue = 1); flanks 1.2 < |u| < 3: {np.mean(fm):+.4f} +- {np.std(fm, ddof=1) / math.sqrt(fm.size):.4f} ({zf:+.2f} sigma); far 4 < |u| < 8: {np.mean(fr):+.4f} +- {np.std(fr, ddof=1) / math.sqrt(fr.size):.4f}")
P("  stack profile (u: mean): " + ", ".join(f"{u:+.1f}: {mstk[j]:+.3f}" for j, u in enumerate(ug) if abs(round(u * 10) % 5) == 0 and abs(u) <= 6))
P(f"  reading: {'negative bowls beside the lines (spectral-filter signature)' if zf < -3 else ('no bowl seen' if abs(zf) <= 3 else 'positive flanks (wings beyond 1.2 x W50/2)')}")
NUM["PH5"] = dict(n=int(S5.shape[0]), line_mean=float(np.mean(lm)), flank_mean=float(np.mean(fm)), flank_z=zf, far_mean=float(np.mean(fr)), profile=dict(u=list(map(float, ug)), mean=list(map(float, mstk))))

P(f"\n{sum(o for _, o in CHK)}/{len(CHK)} checks pass (post hoc; not frozen)")
open(OUT + ".out", "w").write("\n".join(LOG) + "\n")
def clean_(x):
    if isinstance(x, dict): return {str(kk): clean_(vv) for kk, vv in x.items()}
    if isinstance(x, (list, tuple)): return [clean_(vv) for vv in x]
    if isinstance(x, (np.bool_,)): return bool(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating, float)): return None if not np.isfinite(x) else float(x)
    return x
json.dump(clean_(dict(lane="CFG302", stage="POSTHOC", checks=[dict(name=n, ok=o) for n, o in CHK], numbers=NUM)), open(OUT + "_results.json", "w"), indent=1)
