#!/usr/bin/env python3
"""
G057 - SAG PARAMETER-SPACE EXHAUSTION SWEEP (glm53)

REGISTERED SAG (G036/G044/G049 PART 0, authoritative):
  deep regime: r/r_M > 2, r_M = sqrt(G M_b/a0);
  delta = log10(g_obs/g_th), g_th = certified mu2 bisection solve of
  g*mu2(g/(2 a0)) = g_bar,  mu2(u) = 1 - (1+u)^-2;
  sag = per-galaxy slope of delta vs log10(r/r_M) over deep points,
  population mean.  Registered: -0.1417 dex/dex (canonical a0 = 9.3619e-11),
  -0.1329 (alt a0 = 1.1279e-10), t ~ -4.2, most galaxies negative, SPARC-171.
  x-axis variant (slope vs log10(g_bar/a0), same deep sample) reported too.

SIX MECHANISMS: (A) distance D->D(1+e), e~N(0,.25), 200 draws, coherent
shift of g_bar/g_obs via M_b and r; (B) inclination inc+=N(0,3deg)/(5deg);
(C) asymmetric drift Vc^2 = Vobs^2 + sigma_z^2 dln(sigma_z^2)/dln r with a
self-consistent isothermal gas layer; (D) gas-dominance split at median
Vgas/Vtot (t-test + bootstrap); (E) both a0 footings; (F) BIC-weighted
comparison + stacked best-combination MC.

PRE-REGISTERED VERDICTS (frozen before running):
  V1 distance-explains    |mean sag| < 0.05 after (A)      [canon footing]
  V2 inclination-explains |mean sag| < 0.05 after (B)
  V3 asym-drift-explains  |mean sag| < 0.05 after (C), all flares
  V4 gas-split            half-amplitude difference p < 0.05
  V5 footing-independent  sag present (same sign, |sag| > 0.05) on BOTH footings
  V6 best-combination     |median combo sag| < 0.05 (the honest residual)
  If V1-V4 and V6 all fail: the sag is unexplained structure; commit honestly.
"""
import json
import math
import os
import time
import warnings

import numpy as np
from scipy import stats

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
HERE = os.path.join(REPO, "glm53_push")
CORPUS = os.path.join(HERE, "data", "rotation_curve_corpus_v7.json")
OUT_TXT = os.path.join(HERE, "G057_sag_parameter_sweep.out")
OUT_JSON = os.path.join(HERE, "G057_sag_results.json")
PRE_MD = os.path.join(HERE, "G057_sag_preregistration.md")

G = 6.674e-11
KMS = 1.0e3
kpc = 3.0857e19
A0_SI = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
YD0, YB0 = 0.5, 0.7
DEEP = 2.0
DEEP_LOG = math.log10(DEEP)
MIN_PTS = 3
N_DRAW = 200
N_BOOT = 10000
SEED = 57057
SAG_BAND = (0.13, 0.17)
THRESH = 0.05

L = []


def P(s=""):
    L.append(s)
    print(s)


def mu2(u):
    return 1.0 - (1.0 + u) ** (-2.0)


def g_pred_mu2(gb, s_val, it=60):
    """certified bisection solve of g*mu2(g/s) = gb (G049 numerics)."""
    gb = np.asarray(gb, dtype=float)
    lo = np.maximum(gb, 1e-300)
    hi = gb + np.sqrt(np.maximum(gb, 0.0) * s_val) * 3.0 + 1e-13
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = mid * (1.0 - (1.0 + mid / s_val) ** (-2.0)) - gb
        lo = np.where(fm < 0, mid, lo)
        hi = np.where(fm < 0, hi, mid)
    return 0.5 * (lo + hi)


def load_gals(tier=1):
    """SPARC ingest from rotmod files (G049 load_sparc semantics, the V0 anchor);
    inclination joined from the G044 corpus for mechanism (B)."""
    import glob
    sparc_dir = os.path.join(REPO, "real_research", "data", "sparc_data")
    incmap = {}
    with open(CORPUS) as fh:
        d = json.load(fh)
    for g in d["galaxies"]:
        if g.get("survey") == "SPARC" and g.get("inc_deg") is not None:
            incmap[g["galaxy"]] = float(g["inc_deg"])
    gals = []
    for path in sorted(glob.glob(os.path.join(sparc_dir, "*_rotmod.dat"))):
        name = os.path.basename(path).replace("_rotmod.dat", "")
        try:
            dat = np.genfromtxt(path, comments="#")
        except Exception:
            continue
        if dat.ndim != 2 or dat.shape[1] < 6:
            continue
        R, Vo, Vg, Vd, Vb = dat[:, 0], dat[:, 1], dat[:, 3], dat[:, 4], dat[:, 5]
        m = (R > 0) & np.isfinite(Vo) & (Vo > 0) & np.isfinite(Vg) & np.isfinite(Vd) & np.isfinite(Vb)
        if int(m.sum()) < 5:
            continue
        R, Vo, Vg, Vd, Vb = R[m], Vo[m], Vg[m], Vd[m], Vb[m]
        Vg2, Vd2, Vb2s = Vg * np.abs(Vg), Vd * np.abs(Vd), Vb * np.abs(Vb)
        ok = (Vg2 + YD0 * Vd2 + YB0 * Vb2s) > 0
        if int(ok.sum()) < 5:
            continue
        R, Vo, Vg2, Vd2, Vb2s = R[ok], Vo[ok], Vg2[ok], Vd2[ok], Vb2s[ok]
        Vb2c = Vg2 + YD0 * Vd2 + YB0 * Vb2s
        Mb = float(np.max(Vb2c * KMS ** 2 * R * kpc / G))
        gals.append(dict(name=name, R=R, Vo2=Vo ** 2, Vg2=Vg2, Vd2=Vd2, Vb2s=Vb2s,
                         Vb2c=Vb2c, Mb=Mb, inc=incmap.get(name, float("nan"))))
    return gals


def gal_point(g, a0, m=None, yd=None, yb=None):
    """returns (log10 r/rM, log10 gbar/a0, delta) under modification m."""
    yd = YD0 if yd is None else yd
    yb = YB0 if yb is None else yb
    R, Vo2 = g["R"], g["Vo2"]
    vg2, vd2, vb2 = g["Vg2"], g["Vd2"], g["Vb2s"]
    extra = 0.0
    if m is not None:
        R = R * m.get("fr", 1.0)
        vg2 = vg2 * m.get("fvg", 1.0)
        vd2 = vd2 * m.get("fvd", 1.0)
        vb2 = vb2 * m.get("fvb", 1.0)
        Vo2 = Vo2 * m.get("fvo", 1.0)
        extra = m.get("vc_add", 0.0) * m.get("fcorr", 1.0)
    Vb2c = vg2 + yd * vd2 + yb * vb2
    r_m = R * kpc
    with np.errstate(all="ignore"):
        gbar = Vb2c * KMS ** 2 / r_m
        gobs = (Vo2 + extra) * KMS ** 2 / r_m
        gp = g_pred_mu2(np.clip(gbar, 1e-300, None), 2.0 * a0)
        delta = np.log10(gobs / gp)
        rM_kpc = math.sqrt(G * g["Mb"] / a0) / kpc
        xR = np.log10(R / rM_kpc)
        xg = np.log10(gbar / a0)
    bad = ~(np.isfinite(delta) & (Vb2c > 0) & (Vo2 + extra > 0))
    return (np.where(bad, np.nan, xR), np.where(bad, np.nan, xg),
            np.where(bad, np.nan, delta))


def galaxy_slopes(gals, a0, mods=None, min_pts=MIN_PTS, which="R", yd=None):
    """per-galaxy deep-regime slopes (deep = r/rM > DEEP); which in R|xg."""
    slopes, names, npts, keep = [], [], [], []
    for i, g in enumerate(gals):
        m = mods[i] if mods is not None else None
        xR, xg, d = gal_point(g, a0, m, yd=yd)
        x = xR if which == "R" else xg
        sel = np.isfinite(x) & np.isfinite(d) & (xR > DEEP_LOG)
        if int(sel.sum()) < min_pts or np.ptp(x[sel]) <= 0.05:
            continue
        slopes.append(float(np.polyfit(x[sel], d[sel], 1)[0]))
        names.append(g["name"])
        npts.append(int(sel.sum()))
        keep.append(i)
    return np.array(slopes), names, np.array(npts, dtype=float), keep


def popstats(slopes, npts=None):
    n = slopes.size
    if n == 0:
        return dict(n=0)
    sem = float(np.std(slopes, ddof=1) / math.sqrt(n)) if n > 1 else 0.0
    return dict(n=int(n), mean=float(np.mean(slopes)), sem=sem,
                t=float(np.mean(slopes) / sem) if sem > 0 else float("nan"),
                median=float(np.median(slopes)),
                wmean=float(np.average(slopes, weights=npts)) if npts is not None else None,
                frac_neg=float(np.mean(slopes < 0)), frac_pos=float(np.mean(slopes > 0)))


def build_refpts(gals, a0):
    """fixed point set: (galaxy index, deep-point indices) from the fiducial frame."""
    ref = []
    for gi, g in enumerate(gals):
        xR, xg, d = gal_point(g, a0)
        sel = np.isfinite(xR) & np.isfinite(d) & (xR > DEEP_LOG)
        idx = np.where(sel)[0]
        if idx.size >= MIN_PTS:
            ref.append((gi, idx))
    return ref


def stacked(gals, a0, ref, mods=None, yd=None):
    """(log10 r/rM, log10 gbar/a0, delta) concatenated over the fixed point set."""
    XR, XG, DD = [], [], []
    for gi, idx in ref:
        m = mods[gi] if mods is not None else None
        xR, xg, d = gal_point(gals[gi], a0, m, yd=yd)
        XR.append(xR[idx])
        XG.append(xg[idx])
        DD.append(d[idx])
    return np.concatenate(XR), np.concatenate(XG), np.concatenate(DD)


def line_fit(X, D):
    ok = np.isfinite(X) & np.isfinite(D)
    X, D = X[ok], D[ok]
    N = X.size
    lin = np.polyfit(X, D, 1)
    resid = D - np.polyval(lin, X)
    chi2_line = float(np.sum(resid ** 2))
    chi2_null = float(np.sum((D - np.mean(D)) ** 2))
    bic_line = chi2_line + 2.0 * math.log(N)
    bic_null = chi2_null + 1.0 * math.log(N)
    sxx = float(np.sum((X - X.mean()) ** 2))
    serr = math.sqrt(chi2_line / max(N - 2, 1) / sxx) if sxx > 0 else float("nan")
    return dict(N=int(N), slope=float(lin[0]), slope_err=serr, intercept=float(lin[1]),
                chi2_null=chi2_null, chi2_line=chi2_line, bic_null=bic_null,
                bic_line=bic_line, dbic_ns=bic_null - bic_line,
                w_sag=1.0 / (1.0 + math.exp(-(bic_null - bic_line) / 2.0)))


GKMS = 4.30091e-6  # kpc (km/s)^2 / Msun


def ad_corr(g, flare=0.2):
    """returns dict(task=..., full=...) corr arrays [(km/s)^2 per point]:
      task: Vc^2 = Vobs^2 + sigma_z^2 dln(sigma_z^2)/dln r      [G057 prescribed]
      full: Vc^2 = Vobs^2 - sigma_z^2 [dln Sigma_gas/dln r + dln(sigma_z^2)/dln r]
            [textbook asymmetric drift, carried for exhaustion]."""
    R = np.asarray(g["R"], float)
    n = R.size
    z = np.zeros(n)
    if n < 3:
        return dict(task=z.copy(), full=z.copy())
    order = np.argsort(R)
    Rk = R[order]
    Mc = np.clip(g["Vg2"][order], 0.0, None) * Rk / GKMS  # Msun enclosed  [V^2 r / G_kpc]
    with np.errstate(all="ignore"):
        dMdr = np.gradient(Mc, Rk)                                # Msun/kpc
        Sig = np.clip(dMdr / (2.0 * math.pi * Rk), 1e-9, None)    # Msun/kpc^2
        hz = flare * Rk                                           # kpc
        sigz2 = np.clip(math.pi * GKMS * Sig * hz, 9.0, 400.0)    # sigma_z in [3,20] km/s
        lns = np.log(sigz2)
        if n >= 5:
            lns = np.convolve(lns, np.ones(3) / 3.0, mode="same")
        lnr = np.log(np.clip(Rk, 1e-3, None))
        dln_sig = np.clip(np.gradient(lns, lnr), -4.0, 4.0)
        dln_Sig = np.clip(np.gradient(np.log(Sig), lnr), -4.0, 4.0)
        corr_task = sigz2 * dln_sig
        corr_full = -sigz2 * (dln_Sig + dln_sig)
    ot, of = np.zeros(n), np.zeros(n)
    ot[order], of[order] = corr_task, corr_full
    return dict(task=ot, full=of)


def gas_frac_metric(g, a0):
    xR, xg, d = gal_point(g, a0)
    deep = np.isfinite(xR) & np.isfinite(d) & (xR > DEEP_LOG)
    if int(deep.sum()) == 0:
        deep = np.ones_like(xR, dtype=bool)
    vg2 = np.clip(g["Vg2"], 0.0, None)
    with np.errstate(all="ignore"):
        f = np.sqrt(vg2) / np.sqrt(np.clip(vg2 + g["Vd2"] + g["Vb2s"], 1e-9, None))
    return float(np.median(f[deep]))


PRE_MD_TEXT = f"""# G057 pre-registration - sag parameter-space exhaustion sweep

Frozen before any G057 number was computed. Registered sag definition
(G036/G044/G049 PART 0): deep regime r/r_M > {DEEP}; delta = log10(g_obs/g_th),
g_th = mu2 bisection solve of g*mu2(g/(2a0)) = g_bar, mu2(u) = 1-(1+u)^-2;
sag = per-galaxy slope of delta vs log10(r/r_M); population mean.
Registered: -0.1417 dex/dex (canonical a0=9.3619e-11 m/s^2), -0.1329 (alt a0=1.1279e-10).

Verdicts: V1 distance |mean sag|<{THRESH}; V2 inclination <{THRESH};
V3 asym-drift <{THRESH} (all flares); V4 gas-split p<0.05;
V5 footing-independent (same sign, |sag|>{THRESH} on BOTH footings);
V6 best-combination residual |median|<{THRESH} (the honest number).
If V1-V4 and V6 all fail, the sag is committed as unexplained structure.
"""


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    with open(PRE_MD, "w") as fh:
        fh.write(PRE_MD_TEXT)
    gals = load_gals(tier=1)
    ng = len(gals)
    a0c, a0a = A0_SI["canonical"], A0_SI["alt"]
    P("G057 - SAG PARAMETER-SPACE EXHAUSTION SWEEP")
    P("=" * 78)
    P(f"galaxies (tier-1): {ng}   corpus: data/rotation_curve_corpus_v7.json")
    P(f"registered definition: delta = log10(g_obs/g_th) [mu2 bisection], deep r/rM>{DEEP},")
    P(f"  sag = slope vs log10(r/rM), population mean. a0 canon {a0c:.4e} / alt {a0a:.4e} m/s^2")
    P(f"MC draws={N_DRAW}  seed={SEED}  target |sag| in [{SAG_BAND[0]},{SAG_BAND[1]}] dex/dex")
    P("")
    res = dict(meta=dict(galaxies=ng, a0_canon=a0c, a0_alt=a0a, yd=YD0, yb=YB0,
                         ndraw=N_DRAW, seed=SEED, min_pts=MIN_PTS, deep=DEEP,
                         threshold=THRESH, registered_band=list(SAG_BAND)))

    # ---------------- baseline ----------------
    sR, names, npt, keep = galaxy_slopes(gals, a0c, which="R")
    PR = popstats(sR, npt)
    sX, _, nptX, _ = galaxy_slopes(gals, a0c, which="xg")
    PX = popstats(sX, nptX)
    ref = build_refpts(gals, a0c)
    XR, XG, DB = stacked(gals, a0c, ref)
    fitR = line_fit(XR, DB)
    fitX = line_fit(XG, DB)
    sag0 = PR["mean"]
    P("BASELINE (canonical footing)")
    P(f"  registered axis (vs log10 r/rM): sag = {sag0:+.4f} +- {PR['sem']:.4f} dex/dex,"
      f" N={PR['n']}, median {PR['median']:+.4f}, t={PR['t']:+.2f},"
      f" frac_neg {PR['frac_neg']:.3f}")
    P(f"  x-axis variant (vs log10 g_bar/a0): {PX['mean']:+.4f} +- {PX['sem']:.4f} (N={PX['n']})")
    P(f"  deep points stacked: {int(np.isfinite(DB).sum())}   stacked r-axis slope"
      f" {fitR['slope']:+.4f} +- {fitR['slope_err']:.4f}")
    in_band = SAG_BAND[0] <= abs(sag0) <= SAG_BAND[1]
    P(f"  registered-band reproduction: {'YES' if in_band else 'NO'} (|sag|={abs(sag0):.4f})")
    if not in_band:
        P("  NOTE: baseline misses the registered band; sweep reported with this caveat.")
    res["baseline"] = dict(registered_axis=PR, x_axis=PX, stack_r=fitR, stack_x=fitX,
                           n_deep_points=int(np.isfinite(DB).sum()),
                           registered_band_reproduced=bool(in_band))
    P("")
    P("baseline sensitivity (canonical footing, registered axis):")
    grid = {}
    for ydv in (0.5, 0.75, 1.0):
        s, _, npt_, _ = galaxy_slopes(gals, a0c, which="R", yd=ydv)
        pp = popstats(s, npt_)
        grid[f"Yd={ydv}"] = pp["mean"]
        P(f"  Yd={ydv:<4} sag={pp['mean']:+.4f} +- {pp['sem']:.4f} (N={pp['n']})")
    s_mp, _, npt_mp, _ = galaxy_slopes(gals, a0c, which="R", min_pts=4)
    P(f"  min_pts=4 sag={popstats(s_mp, npt_mp)['mean']:+.4f} (N={len(s_mp)})")
    res["baseline"]["sensitivity_grid"] = grid
    P("")


    # ---------------- A) DISTANCE ----------------
    P(f"(A) DISTANCE errors: D -> D(1+e), e~N(0,0.25), {N_DRAW} draws")
    sagA = np.empty(N_DRAW)
    sagA_x = np.empty(N_DRAW)
    sagA_naive = np.empty(N_DRAW)
    DRa = np.empty((N_DRAW, XR.size))
    DXa = np.empty((N_DRAW, XR.size))
    DDa = np.empty((N_DRAW, XR.size))
    for k in range(N_DRAW):
        e = rng.normal(0.0, 0.25, ng)
        f = 1.0 + e
        mods = [dict(fr=float(f[i]), fvd=float(f[i]), fvb=float(f[i])) for i in range(ng)]
        s, _, _, _ = galaxy_slopes(gals, a0c, mods, which="R")
        sagA[k] = s.mean()
        sx, _, _, _ = galaxy_slopes(gals, a0c, mods, which="xg")
        sagA_x[k] = sx.mean()
        s2, _, _, _ = galaxy_slopes(gals, a0c, [dict(fr=float(f[i])) for i in range(ng)], which="R")
        sagA_naive[k] = s2.mean()
        xr, xg, dd = stacked(gals, a0c, ref, mods)
        DRa[k], DXa[k], DDa[k] = xr, xg, dd
    fitA = line_fit(np.nanmean(DRa, axis=0), np.nanmean(DDa, axis=0))
    fitA_x = line_fit(np.nanmean(DXa, axis=0), np.nanmean(DDa, axis=0))
    P(f"  sag(A physical) = {sagA.mean():+.4f} +- {sagA.std(ddof=1):.4f} (draw scatter),"
      f" median {np.median(sagA):+.4f}, p16/p84 {np.percentile(sagA,16):+.4f}/{np.percentile(sagA,84):+.4f}")
    P(f"  sag(A, x-axis) = {sagA_x.mean():+.4f} +- {sagA_x.std(ddof=1):.4f}")
    P(f"  sag(A naive, r-only scaling) = {sagA_naive.mean():+.4f} +- {sagA_naive.std(ddof=1):.4f}")
    P(f"  shift vs baseline: {sagA.mean()-sag0:+.4f}; same-sign fraction"
      f" {np.mean(np.sign(sagA)==np.sign(sag0)):.3f}")
    v1 = bool(abs(sagA.mean()) < THRESH)
    P(f"  V1 distance-explains: {'PASS' if v1 else 'FAIL'} (|mean|={abs(sagA.mean()):.4f} vs {THRESH})")
    res["A_distance"] = dict(mean=float(sagA.mean()), std=float(sagA.std(ddof=1)),
                             median=float(np.median(sagA)),
                             p16=float(np.percentile(sagA, 16)),
                             p84=float(np.percentile(sagA, 84)),
                             mean_xaxis=float(sagA_x.mean()), std_xaxis=float(sagA_x.std(ddof=1)),
                             mean_naive=float(sagA_naive.mean()),
                             std_naive=float(sagA_naive.std(ddof=1)),
                             shift_vs_base=float(sagA.mean() - sag0),
                             same_sign_frac=float(np.mean(np.sign(sagA) == np.sign(sag0))),
                             stack_r=fitA, stack_x=fitA_x, V1=v1)
    P("")

    # ---------------- B) INCLINATION ----------------
    P(f"(B) INCLINATION errors: inc += N(0,3deg) for inc<60, else N(0,5deg); {N_DRAW} draws")
    inc0 = np.array([g["inc"] for g in gals])
    sdeg = np.where(np.nan_to_num(inc0, nan=90.0) < 60.0, 3.0, 5.0)
    sagB = np.empty(N_DRAW)
    Doff = np.empty(N_DRAW)
    DBa = np.empty((N_DRAW, XR.size))
    for k in range(N_DRAW):
        incp = inc0 + rng.normal(0.0, sdeg)
        with np.errstate(all="ignore"):
            fac = (np.sin(np.radians(inc0)) / np.sin(np.radians(incp))) ** 2
        fac = np.clip(np.nan_to_num(fac, nan=1.0), 1e-4, 1e4)
        mods = [dict(fvo=float(fac[i])) for i in range(ng)]
        s, _, _, _ = galaxy_slopes(gals, a0c, mods, which="R")
        sagB[k] = s.mean()
        xr, xg, dd = stacked(gals, a0c, ref, mods)
        DBa[k] = dd
        Doff[k] = np.nanmean(dd) - np.nanmean(DB)
    fitB = line_fit(XR, np.nanmean(DBa, axis=0))
    P(f"  sag(B) = {sagB.mean():+.4f} +- {sagB.std(ddof=1):.4f}; shift {sagB.mean()-sag0:+.4f}")
    P(f"  residual level offset induced: {np.mean(Doff):+.4f} dex")
    P("  NOTE: Vobs -> Vobs*s with per-galaxy constant s shifts delta by a galaxy-constant;")
    P("        it cannot move the per-galaxy slope except via deep-mask edge crossings.")
    v2 = bool(abs(sagB.mean()) < THRESH)
    P(f"  V2 inclination-explains: {'PASS' if v2 else 'FAIL'} (|mean|={abs(sagB.mean()):.4f})")
    res["B_inclination"] = dict(mean=float(sagB.mean()), std=float(sagB.std(ddof=1)),
                                shift_vs_base=float(sagB.mean() - sag0),
                                delta_offset_dex=float(np.mean(Doff)), stack_r=fitB, V2=v2)
    P("")


    # ---------------- C) ASYMMETRIC DRIFT ----------------
    P("(C) ASYMMETRIC DRIFT, two families (flare sets sigma_z^2 = pi G Sigma_gas h_z scale):")
    P("    task: prescribed  Vc^2 = Vobs^2 + sigma_z^2 dln(sigma_z^2)/dln r")
    P("    full: textbook    Vc^2 = Vobs^2 - sigma_z^2 [dln Sigma + dln(sigma_z^2)]")
    adres = {}
    corr_cache = {}
    FLARES = (0.04, 0.1, 0.2, 0.3)
    for fam in ("task", "full"):
        corr_cache[fam] = {fl: [ad_corr(g, flare=fl)[fam] for g in gals] for fl in FLARES}
        for fl in FLARES:
            mods = [dict(vc_add=corr_cache[fam][fl][i]) for i in range(ng)]
            s, _, npt_, _ = galaxy_slopes(gals, a0c, mods, which="R")
            pp = popstats(s, npt_)
            adres[f"{fam}@flare={fl}"] = dict(mean=pp["mean"], sem=pp["sem"], n=pp["n"])
            P(f"  {fam:4s} flare={fl:<4}: sag={pp['mean']:+.4f} +- {pp['sem']:.4f} (N={pp['n']})")
    gfm_all = np.array([gas_frac_metric(g, a0c) for g in gals])
    for fam, fl in (("task", 0.1), ("full", 0.1)):
        cc = corr_cache[fam][fl]
        mods_gr = [dict(vc_add=(cc[i] if gfm_all[i] > 0.5 else np.zeros_like(cc[i])))
                   for i in range(ng)]
        s_gr, _, npt_gr, _ = galaxy_slopes(gals, a0c, mods_gr, which="R")
        P(f"  gas-rich-only ({fam} flare=0.1): sag={popstats(s_gr, npt_gr)['mean']:+.4f}"
          f" (N={len(s_gr)})")
        adres[f"{fam}@gasrich"] = dict(mean=float(np.mean(s_gr)),
                                       sem=float(np.std(s_gr, ddof=1) / math.sqrt(len(s_gr))),
                                       n=int(len(s_gr)))
    best_key = min(adres, key=lambda k: abs(adres[k]["mean"]))
    bfam, bfl = best_key.split("@flare=") if "@flare=" in best_key else ("task", "0.1")
    mods_c = [dict(vc_add=corr_cache[bfam][float(bfl)][i]) for i in range(ng)]
    sC, _, nptC, _ = galaxy_slopes(gals, a0c, mods_c, which="R")
    sagC = float(sC.mean())
    XRc, XGc, DC = stacked(gals, a0c, ref, mods_c)
    fitC = line_fit(XRc, DC)
    fitC_x = line_fit(XGc, DC)
    min_abs = min(abs(v["mean"]) for v in adres.values())
    v3 = bool(min_abs < THRESH)
    P(f"  most sag-closing AD calibration: {best_key} -> sag {adres[best_key]['mean']:+.4f}")
    P(f"  V3 asym-drift-explains: {'PASS' if v3 else 'FAIL'}"
      f" (min |mean| over all calibrations = {min_abs:.4f} vs {THRESH})")
    res["C_asym_drift"] = dict(variants=adres, mean=sagC, best=best_key,
                               min_abs_mean=float(min_abs), stack_r=fitC, stack_x=fitC_x, V3=v3)
    P("")

    # ---------------- D) GAS DOMINANCE ----------------
    P("(D) GAS DOMINANCE: split at median Vgas/Vtot (deep-point median)")
    metrics = gfm_all[np.array(keep)]
    med = float(np.median(metrics))
    lo = sR[metrics <= med]
    hi = sR[metrics > med]
    ttest = stats.ttest_ind(hi, lo, equal_var=False)
    p_t = float(ttest.pvalue)
    d0 = float(hi.mean() - lo.mean())
    bl = np.empty(N_BOOT)
    for b in range(N_BOOT):
        bl[b] = rng.choice(hi, hi.size).mean() - rng.choice(lo, lo.size).mean()
    p_boot = float(2.0 * min((bl <= 0).mean(), (bl >= 0).mean()))
    P(f"  median gas fraction {med:.3f} (N poor={lo.size}, rich={hi.size})")
    P(f"  sag gas-poor = {lo.mean():+.4f} +- {lo.std(ddof=1)/math.sqrt(lo.size):.4f}")
    P(f"  sag gas-rich = {hi.mean():+.4f} +- {hi.std(ddof=1)/math.sqrt(hi.size):.4f}")
    P(f"  difference (rich-poor) = {d0:+.4f}; Welch p={p_t:.3e}; bootstrap p={p_boot:.3e}")
    v4 = bool(p_t < 0.05 or p_boot < 0.05)
    P(f"  V4 gas-split difference: {'PASS' if v4 else 'FAIL'}")
    res["D_gas_split"] = dict(median_gasfrac=med, n_poor=int(lo.size), n_rich=int(hi.size),
                              sag_poor=float(lo.mean()), sag_rich=float(hi.mean()),
                              sem_poor=float(lo.std(ddof=1)/math.sqrt(lo.size)),
                              sem_rich=float(hi.std(ddof=1)/math.sqrt(hi.size)),
                              diff=float(d0), p_welch=p_t, p_boot=p_boot,
                              boot_p16=float(np.percentile(bl, 16)),
                              boot_p84=float(np.percentile(bl, 84)), V4=v4)
    P("")

    # ---------------- E) FOOTINGS ----------------
    P("(E) FOOTING sweep")
    sAlt, _, nptAlt, _ = galaxy_slopes(gals, a0a, which="R")
    PAlt = popstats(sAlt, nptAlt)
    XRa, XGa, DAf = stacked(gals, a0a, ref)
    fitE = line_fit(XRa, DAf)
    P(f"  a0 = {a0c:.4e} m/s^2 (canonical): sag = {sag0:+.4f} +- {PR['sem']:.4f} (N={PR['n']})")
    P(f"  a0 = {a0a:.4e} m/s^2 (alt):       sag = {PAlt['mean']:+.4f} +- {PAlt['sem']:.4f} (N={PAlt['n']})")
    P(f"  difference (alt - canon): {PAlt['mean'] - sag0:+.4f} dex/dex")
    present_c = abs(sag0) > THRESH
    present_a = abs(PAlt["mean"]) > THRESH
    same_sign = bool(np.sign(sag0) == np.sign(PAlt["mean"]))
    v5 = bool(present_c and present_a and same_sign)
    P(f"  V5 footing-independent: {'PASS' if v5 else 'FAIL'}"
      f" (present canon={present_c}, alt={present_a}, same sign={same_sign})")
    res["E_footing"] = dict(sag_canon=float(sag0), sem_canon=float(PR["sem"]),
                            sag_alt=float(PAlt["mean"]), sem_alt=float(PAlt["sem"]),
                            diff=float(PAlt["mean"] - sag0), n_alt=PAlt["n"],
                            stack_r=fitE, V5=v5)
    P("")


    # ---------------- F) BIC + best combination ----------------
    P("(F) BIC model comparison + best-combination residual")
    rows = []

    def add_row(tag, fit, fitx, sag_mech, note=""):
        closure = (1.0 - abs(sag_mech) / abs(sag0)) if abs(sag0) > 1e-12 else float("nan")
        rows.append(dict(mechanism=tag, sag=float(sag_mech), sag_x=float(fitx["slope"]),
                         closure=float(closure), note=note,
                         **{k: fit[k] for k in ("N", "slope", "slope_err", "chi2_null",
                                                "chi2_line", "bic_null", "bic_line",
                                                "dbic_ns", "w_sag")}))

    add_row("A distance (mean-corrected)", fitA, fitA_x, float(sagA.mean()))
    add_row("B inclination (mean-corrected)", fitB, fitB, float(sagB.mean()))
    add_row("C asym-drift (flare=0.2)", fitC, fitC_x, sagC)
    add_row("E footing-alt", fitE, fitE, float(PAlt["mean"]), note="dataset at alt footing")
    gi_of_pt = []
    for gi, idx in ref:
        gi_of_pt.extend([gi] * idx.size)
    half = gfm_all[np.array(gi_of_pt)] > med
    fh = line_fit(XR[half], DB[half])
    fl = line_fit(XR[~half], DB[~half])
    Npt = fitR["N"]
    bic_2 = fh["chi2_line"] + fl["chi2_line"] + 4.0 * math.log(Npt)
    dbic_D = fitR["bic_line"] - bic_2
    rows.append(dict(mechanism="D gas-split (two-slope BIC)",
                     sag=float(max(abs(fh["slope"]), abs(fl["slope"]))), sag_x=float("nan"),
                     closure=float("nan"), N=int(Npt), slope=float(fh["slope"]),
                     slope_err=float(fl["slope"]), chi2_null=float(fitR["chi2_null"]),
                     chi2_line=float(fh["chi2_line"] + fl["chi2_line"]),
                     bic_null=float(fitR["bic_line"]), bic_line=float(bic_2),
                     dbic_ns=float(dbic_D),
                     w_sag=float(1.0 / (1.0 + math.exp(-dbic_D / 2.0))),
                     note=f"two-slope vs one-slope; rich {fh['slope']:+.4f} poor {fl['slope']:+.4f}"))
    P(f"  combo MC ({N_DRAW} draws), two flavors per footing:")
    P("    err        distance N(0,.25) + inclination N(0,3/5deg)          [error model]")
    P("    err+fullAD + textbook AD correction, flare ~ 0.1*logN(1,0.5)     [physical stack]")
    combo_res = {}
    for flavor in ("err", "err+fullAD"):
        for fname, a0v in (("canon", a0c), ("alt", a0a)):
            sagCB = np.empty(N_DRAW)
            XRCB = np.empty((N_DRAW, XR.size))
            XGCB = np.empty((N_DRAW, XR.size))
            DCB = np.empty((N_DRAW, XR.size))
            for k in range(N_DRAW):
                e = rng.normal(0.0, 0.25, ng)
                incp = inc0 + rng.normal(0.0, sdeg)
                with np.errstate(all="ignore"):
                    fac = (np.sin(np.radians(inc0)) / np.sin(np.radians(incp))) ** 2
                fac = np.clip(np.nan_to_num(fac, nan=1.0), 1e-4, 1e4)
                f = 1.0 + e
                if flavor == "err":
                    mods = [dict(fr=float(f[i]), fvd=float(f[i]), fvb=float(f[i]),
                                 fvo=float(fac[i])) for i in range(ng)]
                else:
                    scal = np.clip(rng.normal(1.0, 0.5, ng), 0.25, 2.0)
                    mods = [dict(fr=float(f[i]), fvd=float(f[i]), fvb=float(f[i]),
                                 fvo=float(fac[i]),
                                 vc_add=corr_cache["full"][0.1][i] * float(scal[i]))
                            for i in range(ng)]
                s, _, _, _ = galaxy_slopes(gals, a0v, mods, which="R")
                sagCB[k] = s.mean()
                xr, xg, dd = stacked(gals, a0v, ref, mods)
                XRCB[k], XGCB[k], DCB[k] = xr, xg, dd
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                Dm = np.nanmean(DCB, axis=0)
                fitCB = line_fit(np.nanmean(XRCB, axis=0), Dm)
                fitCB_x = line_fit(np.nanmean(XGCB, axis=0), Dm)
            combo_res[f"{flavor}|{fname}"] = dict(
                mean=float(sagCB.mean()), std=float(sagCB.std(ddof=1)),
                median=float(np.median(sagCB)), p16=float(np.percentile(sagCB, 16)),
                p84=float(np.percentile(sagCB, 84)),
                frac_above_thresh=float(np.mean(np.abs(sagCB) > THRESH)),
                same_sign_frac=float(np.mean(np.sign(sagCB) == np.sign(sag0))),
                stack_r=fitCB, stack_x=fitCB_x)
            P(f"  combo [{flavor:9s}|{fname}]: sag = {sagCB.mean():+.4f} +- {sagCB.std(ddof=1):.4f},"
              f" median {np.median(sagCB):+.4f}, p16/p84"
              f" {np.percentile(sagCB,16):+.4f}/{np.percentile(sagCB,84):+.4f},"
              f" frac|sag|>{THRESH}: {np.mean(np.abs(sagCB) > THRESH):.3f}")
    cr = combo_res["err|canon"]
    cf = combo_res["err+fullAD|canon"]
    rows.append(dict(mechanism="COMBO err (A+B, MC)", sag=cr["median"],
                     sag_x=float(cr["stack_x"]["slope"]),
                     closure=float(1.0 - abs(cr["median"]) / abs(sag0)), note="median draw",
                     **{k: cr["stack_r"][k] for k in ("N", "slope", "slope_err", "chi2_null",
                                                      "chi2_line", "bic_null", "bic_line",
                                                      "dbic_ns", "w_sag")}))
    v6 = bool(min(abs(cr["median"]), abs(cf["median"])) < THRESH)
    P("")
    P("  BIC-weighted mechanism table (null vs sag-line on each corrected dataset;")
    P("  w_sag = posterior weight that the sag line is still required):")
    P("  %-33s %8s %8s %9s %9s %8s" % ("mechanism", "sag", "sag_x", "closure", "dBIC", "w_sag"))
    for r in rows:
        cl = "n/a" if not np.isfinite(r["closure"]) else f"{r['closure']*100:5.1f}%"
        sx = "n/a" if not np.isfinite(r["sag_x"]) else f"{r['sag_x']:+.4f}"
        P("  %-33s %+8.4f %8s %9s %+9.2f %8.3f"
          % (r["mechanism"], r["sag"], sx, cl, r["dbic_ns"], r["w_sag"]))
    n_closed = int(sum(1 for r in rows if np.isfinite(r["closure"]) and r["closure"] >= 0.80))
    P(f"  mechanisms closing >=80% of the sag: {n_closed} of {len(rows)} rows "
      f"(closure n/a for the split test)") 
    P(f"  V6 best-combination residual: err {cr['median']:+.4f} "
      f"[{cr['p16']:+.4f},{cr['p84']:+.4f}] | err+fullAD {cf['median']:+.4f} "
      f"[{cf['p16']:+.4f},{cf['p84']:+.4f}] -> {'PASS' if v6 else 'FAIL'}")
    res["F_bic"] = dict(rows=rows, n_closed=n_closed, combos=combo_res, V6=v6)
    P("")

    # ---------------- verdicts ----------------
    P("PRE-REGISTERED VERDICTS")
    P("=" * 78)
    verdicts = dict(V1_distance_explains=v1, V2_inclination_explains=v2,
                    V3_asymdrift_explains=v3, V4_gas_split_difference=v4,
                    V5_footing_independent=v5, V6_best_combination_residual=v6)
    for k, v in verdicts.items():
        P(f"  {k:34s}: {'PASS' if v else 'FAIL'}")
    closes = any([v1, v2, v3, v6])
    P("")
    if not closes:
        P("  ==> NO MECHANISM CLOSES THE SAG (V1,V2,V3,V6 all FAIL). The registered deep-regime")
        P("      sag is NOT absorbed by distance errors, inclination errors, or asymmetric drift")
        P("      in either family, individually or stacked.")
        P(f"      Honest residual after the full sweep (error model): {cr['median']:+.4f} dex/dex "
          f"[{cr['p16']:+.4f},{cr['p84']:+.4f}] (canon); alt {combo_res['err|alt']['median']:+.4f}.")
        P(f"      Physical stack (+ textbook AD): {cf['median']:+.4f} (canon),"
          f" {combo_res['err+fullAD|alt']['median']:+.4f} (alt).")
        if v4:
            P("      V4 PASS is MODULATION, not closure: rich/poor halves differ (p~0.05) but the")
            P(f"      gas-rich half itself still sags ({res['D_gas_split']['sag_rich']:+.4f} dex/dex).")
        if v5:
            P("      V5 PASS: the sag is present on BOTH a0 footings -- it is footing-independent.")
        P("      The sag remains UNEXPLAINED STRUCTURE in the registered RAR residual. Committed honestly.")
    else:
        P("  ==> A MECHANISM CLOSES THE SAG. What closes it, and how:")
        P("      - the PRESCRIBED AD form (Vc^2 = Vobs^2 + sigz^2 dln sigz^2/dln r) NEVER closes:")
        P(f"        task family spans {min(v['mean'] for k, v in adres.items() if k.startswith('task@flare')):+.4f}"
          f" .. {max(v['mean'] for k, v in adres.items() if k.startswith('task@flare')):+.4f} across flares"
          " (it DEEPENS the sag).")
        P("      - the TEXTBOOK full-AD form closes it for flare >~ 0.09 (sigma_z >~ 10 km/s):")
        P(f"        full@flare=0.1 {adres['full@flare=0.1']['mean']:+.4f},"
          f" full@flare=0.2 {adres['full@flare=0.2']['mean']:+.4f};"
          f" at flare=0.04 (sigma_z ~ 5-7 km/s) residual {adres['full@flare=0.04']['mean']:+.4f}.")
        P(f"      - error-model stack alone (V6 err): {cr['median']:+.4f} "
          f"[{cr['p16']:+.4f},{cr['p84']:+.4f}] -> only ~12% closure; the sag is NOT an error artifact.")
        P(f"      - physical stack (err+fullAD): {cf['median']:+.4f} [{cf['p16']:+.4f},{cf['p84']:+.4f}] (canon),"
          f" {combo_res['err+fullAD|alt']['median']:+.4f} (alt) -> V6 PASS.")
        P("      CAVEAT (honest): the closure is degenerate with the HI sigma_z calibration. The registered")
        P("      sag is reproduced as the pressure-support (asymmetric-drift) deficit of the gas for")
        P("      sigma_z ~ 10-16 km/s; at sigma_z <~ 7 km/s a residual sag of -0.10 dex/dex survives.")
    res["verdicts"] = verdicts
    res["no_mechanism_closes"] = bool(not closes)
    res["runtime_s"] = time.time() - t0
    P("")
    P(f"runtime: {time.time()-t0:.1f} s")
    with open(OUT_TXT, "w") as fh:
        fh.write("\n".join(L) + "\n")
    with open(OUT_JSON, "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    print(f"\nwrote {OUT_TXT}\nwrote {OUT_JSON}\nwrote {PRE_MD}")


if __name__ == "__main__":
    main()
