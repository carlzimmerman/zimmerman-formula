#!/usr/bin/env python3
"""G134 -- THE V4 PARTIAL-RECOVERY: the rising-share test done right.

CONTEXT (all from the committed record):
  * G094 corrected the V4 Spearman: on the units-fixed field the pooled
    rho(s_ph, log10(g_tot/a0)) = -0.2975 (p = 3.24e-3, n = 96, 12 clusters x
    8 radii) -- NOT the registered -0.926 / 1.43e-41, which is reproduced
    only on G050's broken g_tot (the 1e9*MSUN floor made the field a
    function of radius alone: the registered rank correlation measured
    share-vs-radius, not share-vs-field).
  * The remaining problem, addressed here: the CORRECTED rho = -0.298 still
    pools ALL radii, and the share s(r) has a strong RADIAL trend (it rises
    with r by construction).  Since the field g_tot/a0 also falls steeply
    with r in the pooled sample, the pooled rank correlation can be (and
    largely is) the radius trend masquerading as field dependence.

THIS LANE (the honest tests, all re-derived from the same committed ingests
with G094's exact pipeline -- baryons(), dlnM_dlnr(), the units-fixed g_tot):
  (1) PARTIAL CORRELATION of s vs log10(g_tot/a0) CONTROLLING for log10 r
      (and separately for r/R500, and both): per cluster (n = 8) and pooled
      (n = 96), with p-values.  The honest test of 'the share rises as the
      field falls' NET of the radius.
  (2) FIXED-RADIUS TEST: within narrow radius shells -- the share vs the
      field at FIXED radius, the cluster-to-cluster variation at the same
      radius.  8 shells x 12 clusters (one per grid radius), plus the
      task's 5-shell coarser grouping; pooled shell-wise Spearman
      (Fisher-z fixed effects) with p; a cluster-jackknife; and a
      decomposition of the share into its two factors (the local mass-
      profile slope dlnM and the baryon-vs-deficit ratio mb/M_res) to
      state WHAT carries any fixed-radius signal.
  (2b) ROBUSTNESS LANE: the PHYSICAL share (G106's s = rho_ph/rho_res,
      computed with the corrected Mres floor) through the same battery --
      the G050/G094 'share' = dlnM*M_b/1.99e39 ~ 1e-27 (the G059-registered
      units slip: the 1e9*MSUN floor mixes units and is a constant, so all
      rank statistics of the committed share -- incl. G094's -0.2975 and
      G050's -0.926 -- measure dlnM*M_b vs the field, not a density share);
      the physical-share lane tells whether the fixed-radius verdict is a
      property of the share itself.
  (3) THE DECISION: does the rising-share signature survive the
      partial/fixed-radius tests at rho > 0.3-class (state the number and
      the p), or is the V4 claim reduced to 'the share rises with radius'
      (a restatement of the profile, not the field)?
  (4) VERDICTS: V1 the partial correlation (with the p); V2 the fixed-shell
      correlation; V3 the honest statement -- field-driven, radius-driven,
      or both, with the numbers that decide.

SIGN CONVENTION (G106, carried): the share RISES outward, g_tot/a0 FALLS
outward, so the V4 claim is a NEGATIVE rho (share falls as the field
rises).  The decision is DIRECTION-AWARE: a 0.3-class significant positive
rho net of radius is NOT a survival of the claim -- it is an inversion.

Gate: the pipeline must reproduce G094's pooled rho = -0.2975 (p = 3.24e-3,
n = 96) on the units-fixed field before any partial/shell statistic counts.
"""
import json
import math
import os

import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr, t, norm

CHECKS = []


def check(name, registered, recomputed, ok, note=""):
    CHECKS.append(dict(name=name, registered=str(registered),
                       recomputed=str(recomputed), pass_=bool(ok), note=note))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         registered: {registered}")
    print(f"         recomputed: {recomputed}")
    if note:
        print(f"         note      : {note}")


print(__doc__)
print("=" * 100)
print("G134 -- THE V4 PARTIAL-RECOVERY")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")

# ------------------------------------------------------------------ constants
G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])
BAND_LO = 0.25       # "0.3-class" bar: |rho| in [0.25, 0.5) counts


def loginterp(x, xp, fp, hold_last=False):
    xp = np.atleast_1d(np.asarray(xp, float))
    fp = np.atleast_1d(np.asarray(fp, float))
    x = np.atleast_1d(np.asarray(x, float))
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    if hold_last:
        out = np.where(x > xp[-1], fp[-1], out)
    return out


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),
             M_hse=np.array(hm["M_FORW"], float),
             M_nfw=np.array(hm["M_NFW"], float),
             r_fg=np.array(fg["RADIUS"], float) * 1e3,     # Mpc -> kpc (G050)
             M_gas=np.array(fg["MGAS"], float))
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)
        d["M_st"] = np.array(ms["MSTAR"], float)
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(dd for dd in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, dd)))]
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))
print(f"X-COP clusters loaded: {len(CL)} ({', '.join(c['name'] for c in CL)}); "
      f"{sum(c['has_star'] for c in CL)} with a measured stellar profile")

# ------------------------------------------------ G050/G094 stellar import
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


def baryons(c, r):
    """G094 verbatim: M_gas + M_star at r (Msun); non-star clusters take the
    imported median M_star/M_gas at that radius (0.047 fallback)."""
    r = np.atleast_1d(np.asarray(r, float))
    mg = loginterp(r, c["r_fg"], c["M_gas"])
    if c["has_star"]:
        ms = loginterp(r, c["r_st"], c["M_st"])
    else:
        ms = np.array([np.nan if (not np.isfinite(g)) else
                       g * ratio_tab.get(r_, (0.047, 0))[0]
                       for r_, g in zip(r, mg)])
    return mg + ms


def dlnM_dlnr(c, r):
    """G094 verbatim: local log-log slope of the committed M_HSE table."""
    r_hm, M = c["r_hm"], c["M_hse"]
    out = np.empty(len(r))
    for i, rq in enumerate(r):
        j = int(np.searchsorted(r_hm, rq))
        j = min(max(j, 0), len(r_hm) - 2)
        out[i] = math.log(M[j + 1] / M[j]) / math.log(r_hm[j + 1] / r_hm[j])
    return out


# ------------------------------------------------- the V4 arrays (G094 exact)
ROWS = []          # one dict per (cluster, radius) point, pooled
for c in CL:
    r = RG.copy()
    mb = baryons(c, r)
    Mh = loginterp(r, c["r_hm"], c["M_hse"])
    dlnM = dlnM_dlnr(c, r)
    Mres = np.maximum(Mh - mb, 1e9 * MSUN)
    share = dlnM * mb / Mres                       # G094/G050's share_unc
    gtot = G * np.maximum(Mh, 1e9) * MSUN / (r * KPC) ** 2   # units-fixed
    R500kpc = (META.get(c["name"]) or {}).get("R500")
    R500kpc = None if R500kpc is None else R500kpc * 1e3
    m = np.isfinite(share) & (gtot > 0)
    for ri, si, gi, di, mi in zip(r, share, gtot, dlnM, m):
        if not mi:
            continue
        ROWS.append(dict(cluster=c["name"], r=float(ri),
                         rR500=None if R500kpc is None else float(ri / R500kpc),
                         share=float(si), logg=float(math.log10(gi / A0["canonical"])),
                         dlnM=float(di), Mres=float(Mres[int(np.argmin(abs(r - ri)))]),
                         mb=float(mb[int(np.argmin(abs(r - ri)))]),
                         mbmres=float(mb[int(np.argmin(abs(r - ri)))] /
                                      Mres[int(np.argmin(abs(r - ri)))])))

NC = len(CL)
print(f"pooled points: {len(ROWS)} = {NC} clusters x {len(RG)} radii")
D = {k: np.array([row[k] for row in ROWS]) for k in ("r", "rR500", "share",
                                                     "logg", "dlnM", "mb",
                                                     "Mres")}
D["logr"] = np.log10(D["r"])
D["mbmres"] = D["mb"] / D["Mres"]      # the share's second factor: s = dlnM * mb/Mres

# ==================================================================== GATE
rho_g, p_g = spearmanr(D["share"], D["logg"])
print(f"\nGATE (G094 replication on the units-fixed field; both footings "
      f"identical -- rank-invariant under the a0 scaling):")
print(f"  pooled Spearman rho(s, log10(g_tot/a0)) = {rho_g:+.4f}, "
      f"p = {p_g:.3e}, n = {len(ROWS)}  (registered -0.2975 / 3.24e-3 / 96)")
check("V0 gate: G094's corrected pooled Spearman -0.2975 (p = 3.24e-3, n = 96)",
      "-0.2975 / 3.24e-3 / 96",
      f"{rho_g:+.4f} / {p_g:.3e} / {len(ROWS)}",
      abs(rho_g - (-0.2975)) < 0.01 and abs(p_g - 3.24e-3) < 2e-3 and
      len(ROWS) == 96,
      "the pipeline below is the same arrays G094's corrected rho was read "
      "from; every partial/shell statistic inherits the gate")

# the broken-field cross-check: G050's registered -0.926 was the RADIUS trend
rho_br, p_br = spearmanr(D["share"], -D["logr"])     # broken g_tot rank == r rank
print(f"  cross-check: rho(s, log10 r) = {spearmanr(D['share'], D['logr'])[0]:+.3f} "
      f"(p = {spearmanr(D['share'], D['logr'])[1]:.2e}); on G050's broken "
      f"radius-only field the rho is by construction "
      f"rho(s, -log r) = {rho_br:+.3f} (p = {p_br:.2e}) -- the registered "
      f"-0.926 / 1.43e-41 IS the radius trend with the sign flipped")
check("V0b: the registered -0.926 is exactly -rho(s, log r) (broken field = "
      "radius alone)", "-0.926 / 1.43e-41", f"{rho_br:+.3f} / {p_br:.2e}",
      abs(rho_br - (-0.926)) < 0.01, "closes G094's identification: the broken "
      "1e9*MSUN floor makes g_tot a pure function of r")

# ------------------------------------------------- radial-trend diagnostics
rho_sr, p_sr = spearmanr(D["share"], D["logr"])
rho_gr, p_gr = spearmanr(D["logg"], D["logr"])
print(f"\nTHE CONFOUNDING TREND (what the raw pooled rho actually rides on):")
print(f"  rho(s, log10 r)          = {rho_sr:+.3f} (p = {p_sr:.1e}) -- the "
      f"share's own radial rise")
print(f"  rho(log10(g/a0), log10 r)= {rho_gr:+.3f} (p = {p_gr:.1e}) -- the "
      f"field's radial fall")
print(f"  raw pooled rho(s, g/a0)  = {rho_g:+.3f} (p = {p_g:.3e})")

# ---- the committed share's numerical level (the persistent units slip)
s_vals = np.array([row["share"] for row in ROWS])
print(f"\nTHE COMMITTED SHARE'S NUMERICAL LEVEL (a units caveat, G059 DATA "
      f"NOTE carried forward):")
print(f"  share values: min {s_vals.min():.2e}, median {np.median(s_vals):.2e}, "
      f"max {s_vals.max():.2e} (Msun/Msun, expected O(0.1-1))")
print(f"  the G050/G094 Mres floor '1e9*MSUN' mixes units (Mh, mb are Msun "
      f"COUNTS): max(Mh - mb, 1e9*MSUN) = 1.99e39 always, so the committed "
      f"'share' = dlnM*M_b/1.99e39 ~ 1e-27 -- the G059-registered slip "
      f"persists in the DENOMINATOR; G094 corrected g_tot only.")
rho_ident, p_ident = spearmanr(s_vals, np.array([row["dlnM"] * row["mb"]
                                                 for row in ROWS]))
print(f"  rank-invariance: Spearman(share, dlnM*M_b) = {rho_ident:+.6f} -- "
      f"the committed share is rank-IDENTICAL to dlnM*M_b (the floor is a "
      f"constant), so every rank statistic below (incl. G094's -0.2975 and "
      f"G050's -0.926) is a statistic of dlnM*M_b vs the field, NOT of a "
      f"density share")
check("V0c: the committed V4 share is rank-identical to dlnM*M_b and its "
      "values are the registered 1e-27 level", "rank identity = 1, values "
      "~1e-27", f"rank rho = {rho_ident:+.4f}, median value "
      f"{np.median(s_vals):.2e}", abs(rho_ident - 1.0) < 1e-9 and
      np.median(s_vals) < 1e-20,
      "the 1e9*MSUN floor (mixed units) makes Mres a constant 1.99e39; the "
      "physical share is G106's s = rho_ph/rho_res (computed in section 2b "
      "with the corrected floor max(Mh - mb, 1e9))")

# raw per-cluster rho (the within-cluster radial run, G106-style)
raw_per = []
for c in CL:
    sub = [row for row in ROWS if row["cluster"] == c["name"]]
    rr_, pp_ = spearmanr([row["share"] for row in sub],
                         [row["logg"] for row in sub])
    raw_per.append(rr_)
print(f"  raw per-cluster rho(s, log g): median {np.median(raw_per):+.3f}, "
      f"{sum(1 for v in raw_per if v < 0)}/{NC} negative (the within-cluster "
      f"radial run is radius-dominated inside a cluster; the sole exception "
      f"A1644 has a ~constant committed share (its field is non-monotone in "
      f"r) -- its raw rho is a tie artifact, not a signal)")

# ================================================================ (1) PARTIAL
def rank(x):
    return np.argsort(np.argsort(x)).astype(float)


def partial_corr(x, y, Z):
    """Partial Pearson on ranks = partial Spearman.  Z: (n, k) controls.
    p: t with df = n - k - 2.  pinv-based projection for rank stability."""
    x, y = rank(x), rank(y)
    Z = np.atleast_2d(np.asarray(Z, float))
    n = len(x)
    k = Z.shape[1]
    if k > 0:
        A = np.column_stack([np.ones(n), Z])
        with np.errstate(all="ignore"):
            P = A @ np.linalg.pinv(A)
            rx = x - P @ x
            ry = y - P @ y
        rx = np.nan_to_num(rx, nan=0.0, posinf=0.0, neginf=0.0)
        ry = np.nan_to_num(ry, nan=0.0, posinf=0.0, neginf=0.0)
    else:
        rx, ry = x, y
    rp = float(np.corrcoef(rx, ry)[0, 1])
    rp = min(max(rp, -1 + 1e-12), 1 - 1e-12)
    df = n - k - 2
    tp = rp * math.sqrt(df / max(1 - rp * rp, 1e-300))
    pp = float(2 * t.sf(abs(tp), df))
    return rp, pp, df


def fisher_pool(rhos, ns, label):
    """Fisher-z fixed-effects pooling; z ~ N(0, 1/sqrt(sum w)), w_j = n_j - 3."""
    zs = np.arctanh(np.clip(np.asarray(rhos), -0.999999, 0.999999))
    ws = np.asarray(ns, float) - 3.0
    zbar = float(np.sum(ws * zs) / np.sum(ws))
    se = 1.0 / math.sqrt(float(np.sum(ws)))
    pp = float(2 * norm.sf(abs(zbar) / se))
    rho_c = float(math.tanh(zbar))
    q = float(np.sum(ws * (zs - zbar) ** 2))
    i2 = max(0.0, (q - (len(rhos) - 1)) / q) if q > 0 else 0.0
    print(f"  {label}: pooled rho = {rho_c:+.3f} (z = {zbar:+.2f}, "
          f"p = {pp:.3e}, k = {len(rhos)} groups, n = {int(sum(ns))}); "
          f"median rho {float(np.median(rhos)):+.3f}; "
          f"{sum(1 for v in rhos if v < 0)}/{len(rhos)} negative; "
          f"Q = {q:.1f} (I^2 = {100*i2:.0f}%)")
    return dict(rho=rho_c, p=pp, z=zbar, se=se, median=float(np.median(rhos)),
                n_neg=sum(1 for v in rhos if v < 0), k=len(rhos),
                n=int(sum(ns)), Q=q, I2=i2)

print()
print("=" * 100)
print("(1) THE PARTIAL CORRELATION: s vs log10(g_tot/a0), CONTROLLING for")
print("    log10 r and for r/R500 -- 'the share rises as the field falls'")
print("    net of the radius.")
print("=" * 100)

# ---- per cluster (n = 8): controls log r ; r/R500 ; both
per = {key: [] for key in ("logr", "rR500", "both")}
per_df = {}
for c in CL:
    sub = [row for row in ROWS if row["cluster"] == c["name"]]
    x = np.array([row["share"] for row in sub])
    y = np.array([row["logg"] for row in sub])
    lr = np.log10(np.array([row["r"] for row in sub]))
    rr = np.array([row["rR500"] for row in sub])
    if any(v is None for v in rr):
        rr = lr.copy()          # no R500 in META -> fall back to log r only
    r1, p1, df1 = partial_corr(x, y, lr.reshape(-1, 1))
    r2, p2, _ = partial_corr(x, y, rr.reshape(-1, 1))
    r3, p3, _ = partial_corr(x, y, np.column_stack([lr, rr]))
    per["logr"].append(r1)
    per["rR500"].append(r2)
    per["both"].append(r3)
    per_df[c["name"]] = dict(df=df1, r1=r1, p1=p1, r2=r2, p2=p2, r3=r3, p3=p3)
    deg = "DEGENERATE" if abs(r1) > 0.99 else ""
    print(f"  {c['name']:9s} partial | log r = {r1:+.3f} (p = {p1:.3f}) {deg}")
print(f"  NOTE: within a cluster both s and log g are smooth functions of r "
      f"on the 8-bin grid, so the net-of-radius residual is curvature noise: "
      f"{sum(1 for v in per['logr'] if abs(v) > 0.99)}/{NC} per-cluster "
      f"partials are degenerate (|rho| > 0.99) -- the per-cluster partial is "
      f"not the informative reading; the pooled/fixed-radius rows are.")
nd = [(v, per_df[c["name"]]["p1"]) for c, v in
      zip(CL, per["logr"]) if abs(v) <= 0.99]
print(f"  non-degenerate per-cluster partials ({len(nd)}/{NC}): values "
      f"{', '.join(f'{v:+.3f}' for v, _ in nd)}, median "
      f"{np.median([v for v, _ in nd]):+.3f}")
f1 = fisher_pool([v for v, _ in nd], [8] * len(nd),
                 "per-cluster partials (log r control, degenerate rows excluded)")
print("  (per cluster, r/R500 is a monotone function of r -- the r/R500 and "
      "'both' rows are rank-identical to the log-r row up to rounding)")

# ---- pooled (n = 96)
print("  pooled (n = 96) partials:")
pool_rows = []
for name, Z in [("control log10 r", D["logr"].reshape(-1, 1)),
                ("control r/R500", D["rR500"].reshape(-1, 1)),
                ("control log10 r + r/R500",
                 np.column_stack([D["logr"], D["rR500"]])),
                ("control log10 r + cluster dummies (fixed effects)",
                 np.column_stack([D["logr"]] + [
                     (np.array([row["cluster"] for row in ROWS]) == c["name"])
                     .astype(float) for c in CL]))]:
    rp, pp, df = partial_corr(D["share"], D["logg"], Z)
    pool_rows.append(dict(control=name, rho=rp, p=pp, df=df))
    print(f"    {name:45s} rho_partial = {rp:+.3f} (p = {pp:.3e}, df = {df})")

# ================================================================ (2) SHELLS
print()
print("=" * 100)
print("(2) THE FIXED-RADIUS TEST: the share vs the field at FIXED radius --")
print("    the cluster-to-cluster variation at the same radius (8 shells x")
print("    12 clusters, one per grid radius), pooled shell-wise Spearman.")
print("    (at fixed r, log g = log(G M_HSE/r^2) = log M_HSE + const, so the")
print("    shell test is rank-identical to share-vs-cluster-mass at fixed r)")
print("=" * 100)
shell = []
for rj in RG:
    sub = [row for row in ROWS if abs(row["r"] - rj) < 1e-9]
    xs = np.array([row["share"] for row in sub])
    ys = np.array([row["logg"] for row in sub])
    rho_j, p_j = spearmanr(xs, ys)
    shell.append(dict(r=float(rj), n=len(sub), rho=float(rho_j), p=float(p_j),
                      field_range_dex=float(np.ptp(ys))))
    print(f"  r = {rj:5.0f} kpc: rho = {rho_j:+.3f} (p = {p_j:.3f}, "
          f"n = {len(sub)}), field range across the 12 clusters = "
          f"{np.ptp(ys):.2f} dex")
shell_med = float(np.median([s["rho"] for s in shell]))
shell_neg = sum(1 for s in shell if s["rho"] < 0)
print(f"  median shell rho = {shell_med:+.3f}; {shell_neg}/8 shells negative")
fs = fisher_pool([s["rho"] for s in shell], [12] * len(shell),
                 "pooled shell-wise Spearman (8 shells x 12)")

# ---- jackknife: drop each cluster in turn, re-pool the 8 shells
jk = []
for cj in CL:
    rhos_j = []
    for rj in RG:
        sub = [row for row in ROWS
               if abs(row["r"] - rj) < 1e-9 and row["cluster"] != cj["name"]]
        rho_j, _ = spearmanr([row["share"] for row in sub],
                             [row["logg"] for row in sub])
        rhos_j.append(rho_j)
    jk.append(dict(cluster=cj["name"],
                   pooled=float(math.tanh(np.mean(np.arctanh(np.clip(
                       np.array(rhos_j), -0.999999, 0.999999)))))))
jk_pooled = [j["pooled"] for j in jk]
print(f"  jackknife (drop-one-cluster, re-pooled shell rho): min "
      f"{min(jk_pooled):+.3f}, max {max(jk_pooled):+.3f}, mean "
      f"{np.mean(jk_pooled):+.3f}; dropping {max(jk, key=lambda j: j['pooled'])['cluster']} "
      f"moves it most ({max(jk_pooled):+.3f})")

# ---- decomposition: which factor of s = dlnM * (mb/M_res) carries the shell signal
print("  decomposition at fixed radius (what the share's fixed-radius signal "
      "is made of):")
decomp = {}
for key, lab in (("dlnM", "rho(dlnM, log g)"), ("mbmres", "rho(mb/Mres, log g)")):
    rhos_d = []
    for rj in RG:
        sub = [row for row in ROWS if abs(row["r"] - rj) < 1e-9]
        rho_d, _ = spearmanr([row[key] for row in sub],
                             [row["logg"] for row in sub])
        rhos_d.append(rho_d)
    fd = fisher_pool(rhos_d, [12] * len(shell), f"  {lab} (8 shells x 12)")
    decomp[key] = fd
print("  (s = dlnM * mb/M_res exactly; whichever factor tracks the field at "
      "fixed radius carries the share's fixed-radius correlation)")

# ---- the task's 5-shell coarser grouping (narrow bands, 12-24 pts each)
bands = [(50.,), (75., 100.), (150., 210.), (300., 420.), (600.,)]
bs = []
for band in bands:
    sub = [row for row in ROWS if any(abs(row["r"] - b) < 1e-9 for b in band)]
    rho_b, p_b = spearmanr([row["share"] for row in sub],
                           [row["logg"] for row in sub])
    bs.append(dict(band=f"{band[0]:.0f}-{band[-1]:.0f} kpc", n=len(sub),
                   rho=float(rho_b), p=float(p_b)))
    print(f"  5-shell grouping, band {band[0]:.0f}-{band[-1]:.0f} kpc: "
          f"rho = {rho_b:+.3f} (p = {p_b:.3f}, n = {len(sub)})")
fb = fisher_pool([b["rho"] for b in bs], [b["n"] for b in bs],
                 "pooled 5-band shell-wise Spearman")

# ============================================== (2b) THE PHYSICAL SHARE LANE
print()
print("=" * 100)
print("(2b) ROBUSTNESS LANE -- the PHYSICAL share (G106's s = rho_ph/rho_res,")
print("     with the CORRECTED Mres floor max(M_hse - M_b, 1e9) Msun), run")
print("     through the same battery: is the fixed-radius INversion a property")
print("     of the degenerate committed share, or of the share itself?")
print("=" * 100)
A0C = A0["canonical"]


def dlnM_local(grid, y):
    """G106's forward-difference local slope on the RG grid (last bin
    backward)."""
    out = np.empty(len(y))
    for i in range(len(y)):
        j = i if i < len(y) - 1 else i - 1
        if y[j + 1] > 0 and y[j] > 0:
            out[i] = math.log(y[j + 1] / y[j]) / math.log(grid[j + 1] / grid[j])
        else:
            out[i] = np.nan
    return out


def phys_share_rows():
    rows = []
    for c in CL:
        r = RG.copy()
        mb = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        Mres = np.maximum(Mh - mb, 1e9)                    # Msun (fixed floor)
        gtot = G * np.maximum(Mh, 1e9) * MSUN / (r * KPC) ** 2
        rho_ph = (math.sqrt(G * MSUN * A0C) * np.sqrt(mb) /
                  (4 * math.pi * G) / (r * KPC) ** 2)      # kg/m^3
        rho_res = (Mres * MSUN * dlnM_local(r, Mres) /
                   (4 * math.pi * (r * KPC) ** 3))         # kg/m^3
        s = rho_ph / rho_res
        for ri, si, gi in zip(r, s, gtot):
            if np.isfinite(si) and gi > 0 and si > 0:
                rows.append(dict(cluster=c["name"], r=float(ri),
                                 share=float(si),
                                 logg=float(math.log10(gi / A0C))))
    return rows


P2 = phys_share_rows()
print(f"  physical share points: {len(P2)} (12 x 8); values "
      f"{min(row['share'] for row in P2):.3f} .. "
      f"{max(row['share'] for row in P2):.3f} (O(0.1-1) -- the corrected "
      f"floor)")
# gate: reproduce G106's registered pooled and per-cluster rows
rho_p2, p_p2 = spearmanr([row["share"] for row in P2],
                         [row["logg"] for row in P2])
raw_p2_per = []
for c in CL:
    sub = [row for row in P2 if row["cluster"] == c["name"]]
    rr_, _ = spearmanr([row["share"] for row in sub],
                       [row["logg"] for row in sub])
    raw_p2_per.append(rr_)
print(f"  G106 gate: pooled rho = {rho_p2:+.3f} (p = {p_p2:.1e}, n = "
      f"{len(P2)}) vs registered -0.542 / 1.2e-8; per-cluster median "
      f"{np.median(raw_p2_per):+.3f} vs registered -0.83")
check("V2b gate: the physical share reproduces G106's pooled -0.542 and "
      "per-cluster median -0.83", "-0.542 / 1.2e-8; median -0.83",
      f"{rho_p2:+.3f} / {p_p2:.1e}; median {np.median(raw_p2_per):+.3f}",
      abs(rho_p2 - (-0.542)) < 0.05 and
      abs(np.median(raw_p2_per) - (-0.83)) < 0.1,
      "G106's arrays recomputed inline from the same FITS with the "
      "corrected floor; the lane inherits the gate")
lp2 = np.log10(np.array([row["r"] for row in P2]))
rp2, pp2, dfp2 = partial_corr([row["share"] for row in P2],
                              [row["logg"] for row in P2],
                              lp2.reshape(-1, 1))
print(f"  pooled partial (control log10 r): rho = {rp2:+.3f} "
      f"(p = {pp2:.3e}, df = {dfp2})")
shell2 = []
for rj in RG:
    sub = [row for row in P2 if abs(row["r"] - rj) < 1e-9]
    rho_j, p_j = spearmanr([row["share"] for row in sub],
                           [row["logg"] for row in sub])
    shell2.append(dict(r=float(rj), n=len(sub), rho=float(rho_j),
                       p=float(p_j)))
    print(f"    r = {rj:5.0f} kpc: rho = {rho_j:+.3f} (p = {p_j:.3f}, "
          f"n = {len(sub)})")
fs2 = fisher_pool([s2["rho"] for s2 in shell2], [12] * len(shell2),
                  "physical share: pooled shell-wise Spearman (8 x 12)")
print(f"  median shell rho = {np.median([s2['rho'] for s2 in shell2]):+.3f}; "
      f"{sum(1 for s2 in shell2 if s2['rho'] < 0)}/8 negative")

# ================================================================ (3) DECISION
print()
print("=" * 100)
print("(3) THE DECISION: does the rising-share signature (NEGATIVE rho --")
print("    share falls as the field rises) survive the partial/fixed-radius")
print("    tests at rho > 0.3-class?")
print("=" * 100)
p_logr = pool_rows[0]
p_dum = pool_rows[3]
sig_p = abs(p_logr["rho"]) >= BAND_LO and p_logr["p"] < 0.05
sig_s = abs(fs["rho"]) >= BAND_LO and fs["p"] < 0.05
if sig_p and sig_s:
    if p_logr["rho"] < 0 and fs["rho"] < 0:
        dec = ("SURVIVES at 0.3-class in the CLAIMED direction: the "
               "share-vs-field anti-correlation persists with the radius "
               "removed -- the signature is BOTH field-driven (claimed "
               "direction) and radius-driven")
    else:
        dec = ("INVERTED: net of radius the share-vs-field relation is "
               "significant at 0.3-class but POSITIVE -- at fixed radius the "
               "share is HIGHER where the field (and the cluster mass) is "
               "higher, the OPPOSITE of the V4 claim; the claimed negative "
               "signature was the radius confound, and the surviving "
               "field-driven component runs the other way")
elif sig_p or sig_s:
    dec = ("PARTIALLY SURVIVES: one of the two net-of-radius readings stays "
           "0.3-class significant; its sign is "
           + ("negative (claimed direction)" if (p_logr["rho"] if sig_p else
              fs["rho"]) < 0 else "POSITIVE (inverted relative to the claim)")
           + "; the other reading collapses")
else:
    dec = ("DOES NOT SURVIVE at 0.3-class: with the radius removed the "
           "share-vs-field correlation collapses below the bar -- the V4 "
           "claim reduces to 'the share rises with radius', a restatement "
           "of the profile, not the field")
print(f"  bar: |rho| >= {BAND_LO} (0.3-class) AND p < 0.05.")
print(f"  pooled partial (control log10 r): rho = {p_logr['rho']:+.3f}, "
      f"p = {p_logr['p']:.3e}")
print(f"  pooled partial (log r + cluster dummies): rho = {p_dum['rho']:+.3f}, "
      f"p = {p_dum['p']:.3e}")
print(f"  pooled shell-wise Spearman (8 x 12): rho = {fs['rho']:+.3f}, "
      f"p = {fs['p']:.3e}; 5-band: rho = {fb['rho']:+.3f}, p = {fb['p']:.3e}")
print(f"  raw (G094) pooled rho for reference: {rho_g:+.3f} (p = {p_g:.3e}); "
      f"the radius trend rho(s, log r) = {rho_sr:+.3f}")
print(f"  DECISION (committed V4 share): {dec}")
sig_p2 = abs(rp2) >= BAND_LO and pp2 < 0.05
sig_s2 = abs(fs2["rho"]) >= BAND_LO and fs2["p"] < 0.05
if sig_p2 and sig_s2:
    if rp2 < 0 and fs2["rho"] < 0:
        dec2 = ("SURVIVES at 0.3-class in the CLAIMED direction on the "
                "PHYSICAL share: net of radius the anti-correlation persists "
                "-- the physical share's field-dependence is radius-driven "
                "AND field-driven (claimed direction)")
    else:
        dec2 = ("INVERTED on the PHYSICAL share too: net of radius the "
                "physical share's field relation is significant at 0.3-class "
                "but POSITIVE")
elif sig_p2 or sig_s2:
    dec2 = ("PARTIALLY SURVIVES on the PHYSICAL share: one reading stays "
            "0.3-class significant, sign "
            + ("negative (claimed direction)" if (rp2 if sig_p2 else
               fs2["rho"]) < 0 else "positive (inverted)")
            + "; the other collapses")
else:
    dec2 = ("DOES NOT SURVIVE at 0.3-class on the PHYSICAL share: with the "
            "radius removed the relation collapses below the bar -- on the "
            "physical share the V4 claim reduces to the radius trend")
print(f"  DECISION (physical share, G106's s = rho_ph/rho_res): {dec2}")

# ================================================================ (4) VERDICTS
print()
print("=" * 100)
print("(4) THE VERDICTS")
print("=" * 100)
print(f"  V1 the partial correlation: pooled rho(s, g/a0 | log10 r) = "
      f"{p_logr['rho']:+.3f}, p = {p_logr['p']:.3e}, n = 96, df = "
      f"{p_logr['df']} (| r/R500 = {pool_rows[1]['rho']:+.3f}, p = "
      f"{pool_rows[1]['p']:.3e}; | both = {pool_rows[2]['rho']:+.3f}, p = "
      f"{pool_rows[2]['p']:.3e}; | log r + cluster dummies (within-cluster) = "
      f"{p_dum['rho']:+.3f}, p = {p_dum['p']:.3e}); per-cluster partials: "
      f"{sum(1 for v in per['logr'] if abs(v) > 0.99)}/{NC} degenerate "
      f"(curvature noise at n = 8); non-degenerate median "
      f"{np.median([v for v, _ in nd]):+.3f}, Fisher-pooled {f1['rho']:+.3f} "
      f"(p = {f1['p']:.3e})")
print(f"  V2 the fixed-shell correlation: pooled shell-wise Spearman = "
      f"{fs['rho']:+.3f}, p = {fs['p']:.3e} (8 shells x 12, Fisher-z, "
      f"Q = {fs['Q']:.1f}, I^2 = {100*fs['I2']:.0f}%); median shell rho = "
      f"{shell_med:+.3f} ({shell_neg}/8 negative); jackknife range "
      f"[{min(jk_pooled):+.3f}, {max(jk_pooled):+.3f}]; share factors: "
      f"dlnM piece {decomp['dlnM']['rho']:+.3f} (p = {decomp['dlnM']['p']:.1e}), "
      f"mb/Mres piece {decomp['mbmres']['rho']:+.3f} (p = {decomp['mbmres']['p']:.1e}); "
      f"5-band grouping {fb['rho']:+.3f} (p = {fb['p']:.3e})")
print(f"  V3 the honest statement: {dec}.  The numbers that decide: raw "
      f"pooled rho = {rho_g:+.3f} (p = {p_g:.3e}) riding on rho(s, log r) = "
      f"{rho_sr:+.3f} (p = {p_sr:.1e}) and rho(log g, log r) = {rho_gr:+.3f}; "
      f"with log10 r controlled, rho_partial = {p_logr['rho']:+.3f} "
      f"(p = {p_logr['p']:.3e}); at fixed radius, pooled shell rho = "
      f"{fs['rho']:+.3f} (p = {fs['p']:.3e}).  Physical-share lane "
      f"(G106's s = rho_ph/rho_res): {dec2} (pooled partial {rp2:+.3f}, "
      f"p = {pp2:.3e}; pooled shell rho {fs2['rho']:+.3f}, p = {fs2['p']:.3e}).")

# ---------------------------------------------------------------- the artifact
out = {
    "lane": "G134_v4_partial",
    "title": "THE V4 PARTIAL-RECOVERY -- the rising-share test done right: "
             "partial correlation net of radius + fixed-radius shells",
    "data": "real_research/data/xcop/ FITS (12 clusters) + "
            "xcop_r500_ettori2019.json; G094's exact pipeline (baryons, "
            "dlnM_dlnr, units-fixed g_tot); G050's share s = dlnM*M_b/M_res",
    "constants": dict(G=G, MSUN=MSUN, KPC=KPC, a0_canonical=A0["canonical"],
                      radii_kpc=RG.tolist(), bar_rho=BAND_LO, bar_p=0.05),
    "gate": dict(registered_rho=-0.2975, registered_p=3.24e-3, n=96,
                 recomputed_rho=rho_g, recomputed_p=p_g,
                 broken_field_rho=rho_br, broken_field_p=p_br),
    "committed_share_caveat": dict(
        share_min=float(s_vals.min()), share_median=float(np.median(s_vals)),
        share_max=float(s_vals.max()),
        rank_rho_share_vs_dlnM_Mb=rho_ident,
        statement="the G050/G094 Mres floor max(M_hse - M_b, 1e9*MSUN) mixes "
                  "units: M_hse and M_b are Msun COUNTS, so 1e9*MSUN = "
                  "1.99e39 dominates everywhere and the committed 'share' = "
                  "dlnM*M_b/1.99e39 ~ 1e-27; rank statistics (incl. G094's "
                  "-0.2975 and G050's -0.926) are invariant and measure "
                  "dlnM*M_b vs the field, not a density share; the physical "
                  "share is G106's s = rho_ph/rho_res (lane 2b)"),
    "physical_share_lane": dict(
        n=len(P2), s_min=min(row["share"] for row in P2),
        s_max=max(row["share"] for row in P2),
        pooled_raw_rho=rho_p2, pooled_raw_p=p_p2,
        registered_G106_pooled_rho=-0.542, registered_G106_pooled_p=1.2e-8,
        per_cluster_rho_median=float(np.median(raw_p2_per)),
        registered_G106_per_cluster_median=-0.83,
        pooled_partial_control_logr=dict(rho=rp2, p=pp2, df=dfp2),
        per_shell=shell2,
        median_shell_rho=float(np.median([s2["rho"] for s2 in shell2])),
        n_negative=sum(1 for s2 in shell2 if s2["rho"] < 0),
        pooled_fisher=fs2),
    "radial_trend_diagnostics": dict(
        rho_share_vs_logr=rho_sr, p_share_vs_logr=p_sr,
        rho_logg_vs_logr=rho_gr, p_logg_vs_logr=p_gr,
        rho_share_vs_logg_raw=rho_g, p_share_vs_logg_raw=p_g,
        raw_per_cluster_rho_median=float(np.median(raw_per)),
        raw_per_cluster_n_negative=sum(1 for v in raw_per if v < 0)),
    "partial": dict(
        per_cluster=[dict(cluster=c["name"], partial_rho_logr=per["logr"][i],
                          p_logr=per_df[c["name"]]["p1"],
                          partial_rho_rR500=per["rR500"][i],
                          partial_rho_both=per["both"][i],
                          df=per_df[c["name"]]["df"],
                          degenerate=bool(abs(per["logr"][i]) > 0.99))
                     for i, c in enumerate(CL)],
        n_degenerate_per_cluster=sum(1 for v in per["logr"] if abs(v) > 0.99),
        non_degenerate_median=float(np.median([v for v, _ in nd])),
        non_degenerate_fisher_pooled=f1,
        pooled=[dict(control=r["control"], rho=r["rho"], p=r["p"], df=r["df"])
                for r in pool_rows]),
    "shells": dict(
        per_shell=shell, median_shell_rho=shell_med, n_negative=shell_neg,
        pooled_fisher=fs, jackknife=jk, jackknife_range=[min(jk_pooled),
                                                         max(jk_pooled)],
        decomposition=decomp,
        bands5=[dict(band=b["band"], n=b["n"], rho=b["rho"], p=b["p"])
                for b in bs],
        pooled_fisher_5band=fb),
    "decision": dict(bar="|rho| >= 0.25 (0.3-class) and p < 0.05",
                     direction_aware=True, survives=bool(sig_p and sig_s),
                     inverted=bool(sig_p and sig_s and p_logr["rho"] > 0),
                     partial_only=bool(sig_p and not sig_s),
                     shell_only=bool(sig_s and not sig_p),
                     statement=dec, pooled_partial_logr=p_logr,
                     pooled_partial_dummies=p_dum,
                     pooled_shell_fisher=fs,
                     physical_share=dict(statement=dec2,
                                         pooled_partial=rp2, p=pp2,
                                         pooled_shell=fs2["rho"],
                                         p_shell=fs2["p"])),
    "verdicts": dict(
        V1=dict(name="the partial correlation", rho_pooled_logr=p_logr["rho"],
                p_pooled_logr=p_logr["p"], df=p_logr["df"],
                rho_pooled_rR500=pool_rows[1]["rho"],
                p_pooled_rR500=pool_rows[1]["p"],
                rho_pooled_both=pool_rows[2]["rho"],
                p_pooled_both=pool_rows[2]["p"],
                rho_pooled_dummies=p_dum["rho"], p_pooled_dummies=p_dum["p"],
                n_degenerate_per_cluster=sum(1 for v in per["logr"]
                                             if abs(v) > 0.99),
                non_degenerate_per_cluster_median=float(np.median([v for v, _ in nd])),
                non_degenerate_fisher_pooled=f1),
        V2=dict(name="the fixed-shell correlation", rho_pooled=fs["rho"],
                p_pooled=fs["p"], shells=len(shell), median_shell=shell_med,
                n_negative=shell_neg, Q=fs["Q"], I2=fs["I2"],
                jackknife_range=[min(jk_pooled), max(jk_pooled)],
                dlnM_piece=decomp["dlnM"], mbmres_piece=decomp["mbmres"],
                rho_5band=fb["rho"], p_5band=fb["p"]),
        V3=dict(name="the honest statement", statement=dec,
                physical_share_statement=dec2,
                deciding_numbers=dict(
                    raw_pooled_rho=rho_g, raw_p=p_g,
                    rho_share_vs_logr=rho_sr, p_share_vs_logr=p_sr,
                    rho_logg_vs_logr=rho_gr, p_logg_vs_logr=p_gr,
                    partial_rho_control_logr=p_logr["rho"],
                    partial_p_control_logr=p_logr["p"],
                    shell_rho_pooled=fs["rho"], shell_p_pooled=fs["p"],
                    physical_share_partial_rho=rp2,
                    physical_share_partial_p=pp2,
                    physical_share_shell_rho=fs2["rho"],
                    physical_share_shell_p=fs2["p"]))),
    "checks": CHECKS,
    "n_checks": len(CHECKS),
}
with open(os.path.join(HERE, "G134_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print()
print("G134 COMPLETE: artifact written: G134_results.json")
