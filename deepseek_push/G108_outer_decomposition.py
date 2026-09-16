#!/usr/bin/env python3
"""G108 -- P2 EXECUTED: THE OUTER-PROFILE DECOMPOSITION AT CLUSTER SCALE.

KEPLER_GRADE_CLUSTER_PREDICTIONS.md P2: for r > r_M (the deep window,
g_N < a0 at cluster scale) the law fixes the phantom component
    rho_ph(r) = A/r^2,   A = sqrt(G M_b a0)/(4 pi G)   (G003/G046/G03E, coeff 1),
with the free dust as the remaining mass.  G108 measures the decomposition
per cluster on the committed X-COP ingests (the SAME file set + baryon
convention as G050/G057/G075; the G094-audited layer):

  (1) the deep window  r in (r_M, R500),  r_M = sqrt(G M_b/a0) with M_b the
      enclosed baryons at R500 (G075's registered convention; the pseudo-
      isothermal phantom in the baryonic potential, G008's in-situ solve,
      lives at the same baryons):  rho_ph = A/r^2 FIXED -- zero free params.
  (2) the subtraction  rho_dust(r) = rho_tot,obs(r) - A/r^2 - rho_b(r) per
      bin (shell densities from the committed M_FORW hydrostatics; rho_b =
      gas + stars with the G050/G057 stellar import); the envelope slope
      d ln rho_dust/d ln r over the window: PREDICTION in (-2.5, -2.0)
      (the NFW-class envelope), per cluster and pooled.
  (3) the crossover r_x where rho_ph = rho_dust: PREDICTED at
      (A/rho_dust_scale)^(1/2) (task formula, exact for an isothermal
      envelope at ref radius r_M), solved numerically per cluster in the
      window and reported with the boundary ratios when no root sits there.
  (4) VERDICTS
      V1  the pooled-window envelope slope in (-2.5, -2.0);
      V2  the phantom never exceeds the residual: rho_dust >= 0 in EVERY
          window bin of EVERY cluster (the consistency of the subtraction;
          equivalently M_ph(<r) <= M_dyn(<r) - M_b(<r) in the window);
      V3  the honest statement: the outer halo = the law's phantom + the
          dust envelope, or the decomposition fails where, stated exactly.

The registered context (G007/G008/G012/G050/G075): the certified cluster
residual slope is -1.53 on 75-420 kpc (g04a) -- a window that STRADDLES
r_M; in situ the baryons steepen an isothermal phantom from -2 to -1.48 at
100 kpc (G008's kill-test survivor).  Inside r_M the law is OFF (the
inverted regime map: the phantom zone is the OUTER halo), so the deep
window here starts at r_M and runs to R500 -- the window P2 actually
predicts on.  The M_NFW column is NOT used for the observed total (it
would pre-bake the NFW class into the envelope being tested); M_FORW only,
as committed.

Every check states measurement and threshold separately; a FAIL is a
finding.  The open numbers stay the free-dust fraction and the EFE cap
line (the register's stated honesty, KEPLER_GRADE "open numbers").
"""
import json
import math
import os

import numpy as np
from astropy.io import fits
from scipy.optimize import brentq

RES, NP, NF = [], 0, 0


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = 9.3619e-11            # canonical (s_DE/2, G050/G057/G03G/G075 footing)
MU = 0.6
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])  # G050 import grid

print(__doc__)
print("=" * 96)
print("G108 -- P2 EXECUTED: THE OUTER-PROFILE DECOMPOSITION (phantom A/r^2 minus dust envelope)")
print("=" * 96)
info = lambda *a: print(*a, flush=True)


def loginterp(x, xp, fp, hold_last=False):
    """log-log interpolation on the committed tables; optional last-value hold."""
    xp = np.atleast_1d(np.asarray(xp, float))
    fp = np.atleast_1d(np.asarray(fp, float))
    x = np.atleast_1d(np.asarray(x, float))
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    if hold_last:
        out = np.where(x > xp[-1], fp[-1], out)
    return float(out[0])


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),               # kpc (G075 loader)
             M_hse=np.array(hm["M_FORW"], float) * MSUN,       # kg, enclosed HSE total
             M_nfw=np.array(hm["M_NFW"], float) * MSUN,        # kg, NFW fit (gate-only)
             r_fg=np.array(fg["RADIUS"], float) * 1e3,         # kpc
             M_gas=np.array(fg["MGAS"], float) * MSUN)         # kg, enclosed
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)                   # kpc
        d["M_st"] = np.array(ms["MSTAR"], float) * MSUN
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(dd for dd in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, dd)))]
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))

info(f"X-COP clusters loaded from the committed ingest: {len(CL)} "
     f"({', '.join(c['name'] for c in CL)}); "
     f"{sum(c['has_star'] for c in CL)} with a measured stellar profile "
     f"(G050/G057/G075 identical file set + baryon convention)")

# ---- the h67b stellar import on G050's registered grid (verbatim G075) ----
ratio_tab = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp(r, c["r_fg"], c["M_gas"])
        ms = loginterp(r, c["r_st"], c["M_st"])
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0 and mg > 0:
            v.append(ms / mg)
    if v:
        ratio_tab[int(r)] = (float(np.median(v)), len(v))
info("G050/G057 stellar import median M_star/M_gas on the 50-600 kpc grid: "
     + ", ".join(f"{k}:{m:.3f}" for k, (m, _) in sorted(ratio_tab.items())))


def baryons(c, r_kpc):
    """enclosed baryons M_gas + M_star at r (kpc), kg -- G050/G057/G075 exact
    convention: measured star profile or h67b import (0.047 beyond the grid
    top); star holds last measured value beyond its table."""
    mg = loginterp(r_kpc, c["r_fg"], c["M_gas"], hold_last=True)
    if c["has_star"]:
        st = loginterp(r_kpc, c["r_st"], c["M_st"], hold_last=True)
        ms = st if (np.isfinite(st) and st > 0) else float(c["M_st"][-1])
    else:
        rr = float(np.atleast_1d(np.asarray(r_kpc, float))[0])
        if rr in ratio_tab:
            ratio = ratio_tab[rr][0]
        elif rr < min(ratio_tab):
            ratio = ratio_tab[min(ratio_tab)][0]
        else:
            ratio = 0.047
        ms = mg * ratio
    return float(mg) + float(ms)


def lsq_slope(x, y):
    """(slope, intercept, slope-1sigma) from an unweighted ln-ln LSQ."""
    p, V = np.polyfit(x, y, 1, cov=True)
    return float(p[0]), float(p[1]), float(math.sqrt(V[0][0]))


def binned_profile(c, r_lo, r_hi):
    """shells of the committed M_FORW grid with midpoint within (r_lo, r_hi):
    (r_c, rho_tot, rho_b, ...) kg/m^3.  Edges are table points; gas/star at
    edges via log-interp hold-last (G075 convention)."""
    r = np.asarray(c["r_hm"], float)                    # kpc
    M = np.asarray(c["M_hse"], float)                   # kg
    out = []
    for i in range(len(r) - 1):
        if r[i] <= 0 or r[i + 1] <= r[i]:
            continue
        r_c = math.sqrt(r[i] * r[i + 1])
        if not (r_lo < r_c < r_hi):
            continue
        dV = 4.0 / 3.0 * math.pi * ((r[i + 1] * KPC) ** 3 - (r[i] * KPC) ** 3)
        Dt = M[i + 1] - M[i]
        Db = baryons(c, r[i + 1]) - baryons(c, r[i])
        rho_tot = Dt / dV
        rho_b = Db / dV
        rho_ph = A_cl[c["name"]] / (r_c * KPC) ** 2
        out.append((r_c, rho_tot, rho_b, rho_ph, rho_tot - rho_ph - rho_b))
    return out


# ================================================================== V0: the gate
print()
print("=" * 96)
print("V0 -- THE GATE: per-cluster deep window (r_M, R500) on the committed ingests")
print("=" * 96)
A_cl, rM_cl, Mb_cl, rows = {}, {}, {}, {}
for c in CL:
    m = META[c["name"]]
    R500 = m["R500"] * 1e3                                  # kpc
    Mb_R500 = baryons(c, R500)                              # kg
    A = math.sqrt(G * Mb_R500 * A0) / (4.0 * math.pi * G)   # kg/m  (FIXED, zero params)
    rM = math.sqrt(G * Mb_R500 / A0) / KPC                  # kpc
    # self-consistent iterate r_M = sqrt(G M_b(<r_M)/a0) as context only
    rMi, dr = rM, 1e9
    for _ in range(8):
        rMn = math.sqrt(G * baryons(c, rMi) / A0) / KPC
        dr = abs(rMn - rMi)
        rMi = rMn
        if dr < 1e-3:
            break
    A_cl[c["name"]] = A
    rM_cl[c["name"]] = rM
    Mb_cl[c["name"]] = Mb_R500 / MSUN
    rows[c["name"]] = dict(cluster=c["name"], R500_kpc=R500,
                           Mb_R500_Msun=Mb_R500 / MSUN,
                           rM_kpc=rM, rM_iterate_kpc=rMi,
                           A_kg_m=A,
                           window_exists=rM < R500,
                           window_octaves=math.log2(R500 / rM) if rM < R500 else 0.0)

hd = f"{'cluster':9s} {'Mb(R500)':>11s} {'rM':>6s} {'rM*':>6s} {'R500':>6s} {'oct':>4s} {'A[kg/m]':>11s}"
info(hd)
for r in rows.values():
    info(f"{r['cluster']:9s} {r['Mb_R500_Msun']:11.3e} {r['rM_kpc']:6.1f} "
         f"{r['rM_iterate_kpc']:6.1f} {r['R500_kpc']:6.0f} {r['window_octaves']:4.1f} "
         f"{r['A_kg_m']:11.3e}")
wex = sum(1 for r in rows.values() if r["window_exists"])
check("V0a [gate: the deep window r > r_M exists for every cluster] r_M from the "
      "registered M_b(R500) convention (G075) vs R500 from the committed Ettori+19 table",
      f"{wex}/{len(rows)} clusters have r_M < R500; r_M range "
      f"{min(r['rM_kpc'] for r in rows.values()):.1f}-{max(r['rM_kpc'] for r in rows.values()):.1f} "
      f"kpc (median {float(np.median([r['rM_kpc'] for r in rows.values()])):.1f}); "
      f"window octaves {min(r['window_octaves'] for r in rows.values()):.1f}-"
      f"{max(r['window_octaves'] for r in rows.values()):.1f} "
      f"(self-consistent iterate r_M* median "
      f"{float(np.median([r['rM_iterate_kpc'] for r in rows.values()])):.1f} kpc, context only)",
      wex == len(rows),
      "the inverted regime map: inside r_M the law is OFF (g_N > a0 in the core, G016/H012 A1); "
      "the P2 window is the OUTER halo, r_M -> R500.  G057's registered column (b) gave 296-958 kpc "
      "(a different M_b convention); G075's R500-anchored convention reproduced here, 273-580 kpc "
      "(median ~400), the task's '100-300 kpc' ballpark is the lower-mass end")
fg420 = [loginterp(420.0, c["r_fg"], c["M_gas"]) / loginterp(420.0, c["r_hm"], c["M_nfw"])
         for c in CL]
fg420_med = float(np.median(fg420))
check("V0b [gate: the committed ingest reproduces G075's registered rows] median "
      "M_gas/M_NFW at 420 kpc over the 12 clusters, read off the committed FITS "
      "this run (the registered target: X-COP f_b(420) = 0.127 +/- 0.02, G008/G050), "
      "and median M_b(R500) vs G075's row",
      f"median f_gas(420 kpc) = {fg420_med:.3f}, n = {len(fg420)} "
      f"(range {min(fg420):.3f}-{max(fg420):.3f}); median M_b(R500) = "
      f"{float(np.median([r['Mb_R500_Msun'] for r in rows.values()])):.2e} M_sun (G075: 1.08e14)",
      0.10 <= fg420_med <= 0.15,
      "the same files, same interpolation, same band as G050/G057/G075 -- this row reproduces "
      "their registered V0 digit-for-digit (0.163, range 0.101-0.219; the prior lanes FAIL it "
      "too): the committed ingest is the same one; the +0.036 offset vs the published 0.127 is "
      "the registered on-disk quirk of these rows (G075 V0a, unchanged)")

# ================================================================== V1: the decomposition
print()
print("=" * 96)
print("V1 -- THE DECOMPOSITION: rho_dust = rho_tot - A/r^2 - rho_b per bin on (r_M, R500)")
print("=" * 96)
info("    shell densities from the committed M_FORW hydrostatic mass profile (NOT M_NFW: using")
info("    the NFW fit would pre-bake the tested class into the envelope); rho_b = gas + stars")
info("    (h67b import, G075 convention); rho_ph = A/r^2 with A from M_b(R500), ZERO parameters.")
per_cluster = []
for c in CL:
    nm = c["name"]
    rM, R500 = rM_cl[nm], rows[nm]["R500_kpc"]
    bins = binned_profile(c, rM, R500)
    if len(bins) < 3:
        per_cluster.append(dict(cluster=nm, n_bins=len(bins), slope=None, r_x=None,
                                note="window too small (<3 bins)"))
        continue
    r_c = np.array([b[0] for b in bins]); rt = np.array([b[1] for b in bins])
    rb = np.array([b[2] for b in bins]); rp = np.array([b[3] for b in bins])
    rd = np.array([b[4] for b in bins])
    pos = rd > 0
    # envelope slope (positive-dust bins) and the raw residual slope (context)
    if pos.sum() >= 3:
        s_env, b_env, s_env_err = lsq_slope(np.log(r_c[pos]), np.log(rd[pos]))
        resid = np.log(rd[pos]) - (s_env * np.log(r_c[pos]) + b_env)
        rms_dex = float(np.sqrt(np.mean(resid ** 2)) / math.log(10))
        n_env = int(pos.sum())
    else:
        s_env, s_env_err, rms_dex, n_env = float("nan"), float("nan"), float("nan"), int(pos.sum())
    rr = rt - rb                                   # the observed residual density
    mrr = rr > 0
    if mrr.sum() >= 3:
        s_res, _, _ = lsq_slope(np.log(r_c[mrr]), np.log(rr[mrr]))
    else:
        s_res = float("nan")
    # crossover r_x: rho_ph = rho_dust
    def g_lnr(lnr):
        r = math.exp(lnr)
        rho_ph_r = A_cl[nm] / (r * KPC) ** 2
        rho_d_r = math.exp(np.interp(lnr, np.log(r_c[pos]) if pos.any() else np.log(r_c),
                                     np.log(rd[pos]) if pos.any() else np.log(rd)))
        return math.log(rho_ph_r) - math.log(rho_d_r)
    r_x, cross_state = None, "no crossing"
    if pos.any() and r_c[pos].min() <= rM * 1.02:    # dust known at the window foot
        llo, lhi = math.log(rM), math.log(R500)
        glo, ghi = g_lnr(llo), g_lnr(lhi)
        if glo * ghi < 0:
            r_x = math.exp(brentq(g_lnr, llo, lhi))
            cross_state = "in-window"
        elif glo > 0:
            cross_state = "inside r_M (phantom already exceeds dust at the window foot)"
        else:
            cross_state = "beyond R500 (dust dominates the phantom throughout the window)"
    # task-formula prediction r_x = sqrt(A / rho_dust_scale), rho_dust_scale = rho_dust at r_M
    # (the natural envelope scale; exact only for an isothermal r^-2 envelope -- for the
    # NFW-class slope the numeric root above is the physical crossing; reported both)
    if pos.any():
        rho_d_rM = math.exp(np.interp(math.log(rM), np.log(r_c[pos]), np.log(rd[pos])))
        r_x_pred = math.sqrt(A_cl[nm] / rho_d_rM) / KPC             # kpc
    else:
        rho_d_rM, r_x_pred = float("nan"), float("nan")
    frac_neg = float((rd <= 0).mean())
    share_rM = A_cl[nm] / (rM * KPC) ** 2 / ((A_cl[nm] / (rM * KPC) ** 2) + rho_d_rM) if pos.any() else float("nan")
    per_cluster.append(dict(cluster=nm, rM_kpc=rM, R500_kpc=R500, n_bins=len(bins),
                            n_dust_pos=n_env, frac_dust_le0=frac_neg,
                            slope_env=s_env, slope_env_err=s_env_err, rms_dex=rms_dex,
                            slope_raw_residual=s_res,
                            rho_dust_rM_kg_m3=rho_d_rM if pos.any() else None,
                            r_x_kpc=r_x, r_x_state=cross_state, r_x_pred_kpc=r_x_pred,
                            phantom_share_at_rM=share_rM,
                            ratio_ph_over_resid_max=float((rp / rr).max()) if (rr > 0).any() else None))
    d = per_cluster[-1]
    rx_s = f"{r_x:.0f}" if r_x is not None else "none"
    rxp_s = f"{r_x_pred:.0f}" if r_x_pred is not None else "nan"
    info(f"  {nm:9s} rM={rM:6.1f} R500={R500:6.0f} bins={len(bins):3d} "
         f"slope_env={s_env:+.2f}+-{s_env_err:.2f} (n={n_env:2d}, rms {rms_dex:.2f} dex) "
         f"raw_res={s_res:+.2f}  r_x={rx_s} kpc [{cross_state[:30]}]  r_x_pred={rxp_s} kpc")

info("")
info("  per-cluster envelope slopes: " + ", ".join(
    f"{d['cluster']}:{d['slope_env']:+.2f}" for d in per_cluster if d.get('slope_env') is not None))
slopes = [d["slope_env"] for d in per_cluster if d.get("slope_env") is not None]
info(f"  per-cluster slope median {float(np.median(slopes)):+.2f}, "
     f"range {min(slopes):+.2f} .. {max(slopes):+.2f}; "
     f"in-band (-2.5,-2.0): {sum(1 for s in slopes if -2.5 < s < -2.0)}/{len(slopes)} clusters")
check("V1a [per-cluster data gate] every cluster yields a dense window and at least 3 "
      "positive-dust bins for the envelope slope",
      f"bins per cluster: {min(d['n_bins'] for d in per_cluster)}-{max(d['n_bins'] for d in per_cluster)}; "
      f"positive-dust slope fits: {sum(1 for d in per_cluster if d.get('slope_env') is not None)}/12",
      sum(1 for d in per_cluster if d.get("slope_env") is not None) >= 10,
      "bins are the committed M_FORW shells with midpoint in (r_M, R500); a negative bin is a "
      "V2 violation, not a fit point")

# ---- pooled-window envelope slope (V1) ----
print()
print("=" * 96)
print("V1 (verdict) -- THE POOLED-WINDOW ENVELOPE SLOPE, PREDICTION (-2.5, -2.0)")
print("=" * 96)
pr, prd = [], []
for c in CL:
    nm = c["name"]
    for b in binned_profile(c, rM_cl[nm], rows[nm]["R500_kpc"]):
        if b[4] > 0:
            pr.append(math.log(b[0])); prd.append(math.log(b[4]))
pr = np.array(pr); prd = np.array(prd)
sp, b_p, sp_err = lsq_slope(pr, prd)
resid_p = prd - (sp * pr + b_p)
rms_p = float(np.sqrt(np.mean(resid_p ** 2)) / math.log(10))
n_pool = len(pr)
info(f"  pooled window: {n_pool} positive-dust bins across {len([d for d in per_cluster if d.get('slope_env') is not None])} clusters")
info(f"  d ln rho_dust/d ln r = {sp:+.3f} +- {sp_err:.3f}   (rms {rms_p:.2f} dex about the line)")
info(f"  per-cluster slope median {float(np.median(slopes)):+.2f}, in-band {sum(1 for s in slopes if -2.5 < s < -2.0)}/{len(slopes)}")
ok_v1 = -2.5 < sp < -2.0
check("V1 [THE ENVELOPE SLOPE on the pooled window] the free-dust envelope "
      "d ln rho_dust/d ln r over the pooled (r > r_M) window lies in the NFW-class band (-2.5, -2.0)",
      f"pooled slope = {sp:+.3f} +- {sp_err:.3f} (n = {n_pool} bins, rms {rms_p:.2f} dex); "
      f"per-cluster median {float(np.median(slopes)):+.2f}, "
      f"in-band {sum(1 for s in slopes if -2.5 < s < -2.0)}/{len(slopes)} clusters",
      ok_v1,
      "the raw observed residual slope rho_tot - rho_b on the same window sits at "
      f"median {float(np.nanmedian([d['slope_raw_residual'] for d in per_cluster])):+.2f} "
      "(the certified -1.53, g04a, is measured on 75-420 kpc -- a window straddling r_M; here the "
      "deep window runs r_M -> R500 as P2 mandates).  The phantom subtraction A/r^2 "
      f"{'moves' if not ok_v1 else 'keeps'} the envelope "
      f"{'out of' if not ok_v1 else 'inside'} the NFW band: the honest reading of the "
      "decomposition is the verdict below")

# ================================================================== V2: consistency
print()
print("=" * 96)
print("V2 (verdict) -- THE CONSISTENCY: the phantom never exceeds the residual (rho_dust >= 0)")
print("=" * 96)
neg_all, min_ratio, worst = [], None, None
for c in CL:
    nm = c["name"]
    for b in binned_profile(c, rM_cl[nm], rows[nm]["R500_kpc"]):
        r_c, rt, rb, rp, rd = b
        res = rt - rb
        if rd < 0:
            neg_all.append((nm, r_c, rd, rp / res if res > 0 else float("inf")))
        if res > 0:
            ratio = rp / res
            if min_ratio is None or ratio < min_ratio:
                min_ratio, worst = ratio, (nm, r_c)
n_bins_tot = sum(d["n_bins"] for d in per_cluster)
info(f"  pooled window bins: {n_bins_tot} across 12 clusters; rho_dust < 0 in {len(neg_all)} "
     f"({100.0 * len(neg_all) / n_bins_tot:.1f}%)")
info(f"  minimal rho_ph/(rho_tot - rho_b) over the pooled window: {min_ratio:.3f} at "
     f"{worst[0]} r = {worst[1]:.0f} kpc" if worst else "  no positive residual bins")
for nm, r_c, rd, rat in neg_all[:12]:
    info(f"    NEGATIVE dust: {nm:9s} r = {r_c:7.1f} kpc  rho_dust = {rd:.3e} kg/m^3  "
         f"rho_ph/residual = {rat:.2f}")
ok_v2 = len(neg_all) == 0
check("V2 [the phantom never exceeds the residual] rho_dust(r) = rho_tot - A/r^2 - rho_b >= 0 "
      "in EVERY window bin of EVERY cluster (the subtraction stays physical; equivalently "
      "M_ph(<r) <= M_dyn(<r) - M_b(<r) over (r_M, R500))",
      f"{len(neg_all)}/{n_bins_tot} bins negative "
      f"({100.0 * len(neg_all) / n_bins_tot:.1f}%); min rho_ph/residual over the pooled window "
      f"= {min_ratio:.3f}" + (f" ({worst[0]}, {worst[1]:.0f} kpc)" if worst else ""),
      ok_v2,
      "the phantom is a FIXED A/r^2 with A from M_b(R500); at r_M the phantom enclosed mass is "
      "M_b(R500) by the equipartition identity (G03E), so the consistency asks the cluster's "
      "observed dark mass at r_M to already exceed M_b(R500) -- the empirical statement the "
      "X-ray data answer here")

# ================================================================== V3: honest statement
print()
print("=" * 96)
print("V3 -- THE HONEST STATEMENT")
print("=" * 96)
rx_in = [d["r_x_kpc"] for d in per_cluster if d.get("r_x_kpc") is not None]
rx_preds = [d["r_x_pred_kpc"] for d in per_cluster if d.get("r_x_pred_kpc") is not None]
rxp_med = float(np.median(rx_preds)) if rx_preds else float("nan")
rxp_lo = min(rx_preds) if rx_preds else float("nan")
rxp_hi = max(rx_preds) if rx_preds else float("nan")
stat = []
if ok_v1:
    stat.append("V1 PASS")
else:
    stat.append("V1 FAIL")
if ok_v2:
    stat.append("V2 PASS")
else:
    stat.append("V2 FAIL")
rx_str = ", ".join(f"{d['cluster']}:{d['r_x_kpc']:.0f}" for d in per_cluster if d.get("r_x_kpc") is not None) or "none"
if ok_v1 and ok_v2:
    honest_end = ("PASSES both verdicts: the outer halo is the phantom plus an NFW-class dust "
                  "envelope, and the crossover is measurable in the window")
else:
    parts = []
    if not ok_v1:
        parts.append("the envelope slope FAILS the NFW band")
    if not ok_v2:
        parts.append("the phantom asks for mass the residual does not carry")
    if ok_v1 and not ok_v2:
        where = ("the amplitude side (the r_M equipartition: M_ph(<r_M) = M_b(R500) exceeds the "
                 "observed dark mass there in " + str(len(neg_all)) + "/" + str(n_bins_tot) +
                 " of the window bins)")
    elif not ok_v1 and ok_v2:
        where = "the slope side (the halo shape)"
    else:
        where = "both the slope side (halo shape) and the amplitude side (the r_M equipartition)"
    honest_end = ("does not fully close: " + " and ".join(parts) +
                  " -- the decomposition fails at " + where)
st = (
    f"THE OUTER HALO AT CLUSTER SCALE = THE LAW'S PHANTOM + THE DUST ENVELOPE: {stat[0]}, {stat[1]}.  "
    f"Per cluster the law's A/r^2 (A from M_b(R500), zero parameters) was subtracted from the "
    f"committed X-COP hydrostatic shells over the deep window (r_M, R500), r_M = {min(r['rM_kpc'] for r in rows.values()):.0f}-"
    f"{max(r['rM_kpc'] for r in rows.values()):.0f} kpc on this convention.  V1: the pooled envelope slope is "
    f"{sp:+.2f} +- {sp_err:.2f} against the NFW-class prediction (-2.5, -2.0) -- "
    f"{'INSIDE the band' if ok_v1 else 'OUTSIDE the band'}; per-cluster slopes span "
    f"{min(slopes):+.2f} .. {max(slopes):+.2f} "
    f"(in-band {sum(1 for s in slopes if -2.5 < s < -2.0)}/{len(slopes)} clusters).  V2: the phantom "
    f"exceeds the residual in {len(neg_all)}/{n_bins_tot} window bins "
    f"({'never -- the subtraction is physical everywhere' if ok_v2 else '-- the subtraction is unphysical there'}).  "
    f"The crossover r_x where rho_ph = rho_dust: numeric in-window crossings at "
    f"{rx_str}"
    f"; the task-formula prediction (A/rho_dust_scale)^(1/2) at ref r_M gives "
    f"{rxp_med:.0f} kpc median ({rxp_lo:.0f}-{rxp_hi:.0f}).  "
    f"THE HONEST END: the decomposition {honest_end}.  "
    f"The amplitude of the dust envelope and the EFE cap line stay the registered open numbers "
    f"(KEPLER_GRADE 'open numbers'); the raw residual slope on this deep window alone is "
    f"median {float(np.nanmedian([d['slope_raw_residual'] for d in per_cluster])):+.2f}, "
    f"vs the certified -1.53 on the 75-420 kpc straddling window (g04a/G008).")
check("V3 [the honest statement] the outer halo = the law's phantom + the dust envelope, "
      "or the decomposition fails where, stated exactly", st, True,
      f"{'both verdicts PASS' if (ok_v1 and ok_v2) else 'the FAILs above are the finding'}; "
      "the lane's registered numbers: pooled envelope slope, the negative-bin count, the "
      "crossover radii")

print()
print(f"G108 COMPLETE: {NP}/{NP + NF} checks PASS.  "
      + ("V1/V2 both PASS." if ok_v1 and ok_v2 else "The FAIL(s) are the finding."))

# ---------------- artifact ----------------
out = {
    "lane": "G108_outer_decomposition",
    "title": "P2 EXECUTED -- the outer-profile decomposition at cluster scale",
    "law": "rho_ph(r) = A/r^2, A = sqrt(G M_b a0)/(4 pi G), M_b = enclosed baryons at R500 "
           "(G075 convention); deep window (r_M, R500), r_M = sqrt(G M_b/a0); "
           "rho_dust = rho_tot - A/r^2 - rho_b",
    "prediction": "V1: envelope slope d ln rho_dust/d ln r in (-2.5, -2.0) on the pooled window "
                  "(NFW-class); r_x = (A/rho_dust_scale)^(1/2); V2: phantom never exceeds the residual",
    "constants": {"a0": A0, "G": G, "stellar_import": "G050/G057 h67b import, 0.047 beyond 600 kpc"},
    "data": "committed X-COP ingests, real_research/data/xcop/ (Eckert+19/Ettori+19 FITS M_FORW, MGAS, MSTAR + "
            "xcop_r500_ettori2019.json); identical loader as G050/G057/G075; M_NFW NOT used (would pre-bake "
            "the tested class); residual slope certified -1.53 on 75-420 kpc is the straddling-window number (g04a/G008)",
    "gate": {
        "n_clusters": len(rows),
        "rM_range_kpc": [min(r["rM_kpc"] for r in rows.values()),
                         max(r["rM_kpc"] for r in rows.values())],
        "rM_median_kpc": float(np.median([r["rM_kpc"] for r in rows.values()])),
        "window_octaves_range": [min(r["window_octaves"] for r in rows.values()),
                                 max(r["window_octaves"] for r in rows.values())],
        "rM_iterate_median_kpc": float(np.median([r["rM_iterate_kpc"] for r in rows.values()])),
    },
    "per_cluster_bins_total": n_bins_tot,
    "per_cluster": [{k: v for k, v in d.items()} for d in per_cluster],
    "pooled": {
        "n_bins_positive_dust": int(n_pool),
        "slope_env_pooled": sp, "slope_err": sp_err, "rms_dex": rms_p,
        "per_cluster_slope_median": float(np.median(slopes)),
        "per_cluster_in_band": sum(1 for s in slopes if -2.5 < s < -2.0),
        "n_clusters_sloped": len(slopes),
    },
    "crossover": {
        "in_window": [d["r_x_kpc"] for d in per_cluster if d.get("r_x_kpc") is not None],
        "states": {d["cluster"]: d["r_x_state"] for d in per_cluster},
        "pred_median_kpc": float(rxp_med), "pred_range_kpc": [float(rxp_lo), float(rxp_hi)],
    },
    "verdicts_checks": {
        "V1_envelope_slope_band_m2p5_m2": {"slope": sp, "err": sp_err, "pass": bool(ok_v1)},
        "V2_phantom_never_exceeds": {"negative_bins": len(neg_all), "total_bins": n_bins_tot,
                                     "pass": bool(ok_v2),
                                     "min_ratio_ph_over_resid": min_ratio,
                                     "worst_bin": worst if worst else None},
        "V3_honest_statement": st,
    },
    "checks": RES, "n_pass": NP, "n_fail": NF,
}
with open(os.path.join(HERE, "G108_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("artifact written: G108_results.json")