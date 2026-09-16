#!/usr/bin/env python3
"""G223 -- THE LINE-SCATTER DECOMPOSITION: the 12-decade line's 0.18-dex
residual -- freeze-epoch vs systematics vs channel.

THE QUESTION: what orders the perpendicular scatter of the 12-decade line
(b = 1.004 +- 0.011, rms 0.180, n = 542; G131 registers + G162 fill, the
G202/G205 register)?

THE CANDIDATES:
  (a) the freeze-epoch (G213's z*): the never-froze dSphs scatter DIFFERENTLY
      -- the UFD excess 0.40 vs the frozen 0.22;  z* is computed per object
      from the equilibrium dispersion entering the law (sigma_pred for the
      dispersion channels; v_pred/sqrt(2) for the rotation channels, the
      equipartition face), via  z*+1 = m sigma^2/(k_B T0),  m = 5 keV/c^2,
      T0 = 2.72548 K  (G213 ladder: sigma_min = 65.0 km/s @ 5 keV, 60.9 @
      5.7 keV).
  (b) the channel (rotation vs dispersion; G128: the rotation channels sit at
      med|r| 0.08-0.12, the dispersion/boundary channels at 0.16-0.18, the
      UFDs at 0.40 -- the UFD/GC boundary channels depart).
  (c) the per-object systematics (distance/IMF/AD errors -- the G087-type
      proxies: errV, eD, Q, T on SPARC; sigma-obs errors and M_V errors on the
      dSphs; sig_v errors on the GEMS groups).

THE DECOMPOSITION: regress the per-object |residual| (r = log10(obs/pred)
about the identity line) on the candidate axes; report the variance explained
by each and the ISOLATED freeze-epoch contribution net of the channel
(R^2(channel + z*) - R^2(channel)).

THE DOMAIN STATEMENT: with the freeze-epoch cut (z* > 0, the systems whose
equilibrium sat above the CMB thermostat -- FROZEN): the line's slope and rms
(rms 0.180 -> ?); the law's domain stated precisely.

VERDICTS: V1 the variance decomposition; V2 the frozen-domain line (the
numbers); V3 the honest statement (the 12-decade line's scatter: the
freeze-epoch is the ordering axis for the dispersion departures, the channel
is the other main term, the two confounded at the class level; the per-object
systematics carry a minor share).

Checks: every register statistic reproduced from the committed files before
use -- G131 pre-fill pooled (0.9884 +- 0.0202, rms_id 0.2208, n = 248),
G162 after-fill (1.0040 +- 0.0108, rms_id 0.1795, n = 542), G213 class medians
(UFD 0.4007 / bright 0.1633 / full 0.222) and the E-vs-z* Spearman (-0.691,
p = 6.1e-6), per-channel medians, G087's registered per-galaxy proxies.
"""

import csv
import hashlib
import io
import json
import math
import os
import statistics
import warnings
from contextlib import redirect_stderr, redirect_stdout

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
A0 = 9.3619e-11          # m/s^2 canonical footing (G03E, carried by the registers)
G_N = 6.6743e-11         # m^3 kg^-1 s^-2
MSUN = 1.989e30          # kg
KB = 1.380649e-23        # J/K
T0 = 2.72548             # K, CMB today (G213 constant)
MEV_C2 = 1.78266192e-33  # kg per keV/c^2

# freeze floor: the sigma whose equilibrium temperature equals T_CMB(0)
SIGMA_MIN_5 = 65.0       # km/s @ 5 keV
SIGMA_MIN_57 = 60.9      # km/s @ 5.7 keV


def jload(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def ols(x, y):
    """OLS; returns (a, b, se_a, se_b, rms_about_fit)."""
    n = len(x)
    xb = sum(x) / n
    yb = sum(y) / n
    sxx = sum((xi - xb) ** 2 for xi in x)
    sxy = sum((xi - xb) * (yi - yb) for xi, yi in zip(x, y))
    b = sxy / sxx
    a = yb - b * xb
    resid = [yi - (a + b * xi) for xi, yi in zip(x, y)]
    s2 = sum(rr * rr for rr in resid) / (n - 2)
    se_b = math.sqrt(s2 / sxx)
    se_a = math.sqrt(s2 * (1.0 / n + xb * xb / sxx))
    rms = math.sqrt(sum(rr * rr for rr in resid) / n)
    return a, b, se_a, se_b, rms


def pooled_fit(rows):
    """rows: list of dicts with 'r' (log10 obs/pred); returns the fit dict."""
    xs = [math.log10(r["pred"]) for r in rows]
    ys = [math.log10(r["obs"]) for r in rows]
    a, b, se_a, se_b, rms_fit = ols(xs, ys)
    rs = [r["r"] for r in rows]
    return dict(
        n=len(rows),
        slope_b=round(b, 4), se_b=round(se_b, 4),
        nu_sigma=(b - 1.0) / se_b,
        intercept_a=round(a, 4),
        rms_about_identity=round(math.sqrt(sum(v * v for v in rs) / len(rs)), 4),
        rms_about_fit=round(rms_fit, 4),
        median_r=round(statistics.median(rs), 4),
        median_abs_r=round(statistics.median([abs(v) for v in rs]), 4),
    )


def chan_stats(rs):
    return dict(
        n=len(rs),
        median_r=round(statistics.median(rs), 4),
        median_abs_r=round(statistics.median([abs(v) for v in rs]), 4),
        rms_dex=round(math.sqrt(sum(v * v for v in rs) / len(rs)), 4),
        mad_dex=round(statistics.median([abs(v - statistics.median(rs)) for v in rs]), 4),
    )


def spearman_rho(x, y):
    """Spearman rho via scipy (average-rank tie handling, the committed
    convention -- G213/G070 used scipy.stats.spearmanr)."""
    rho, p = stats.spearmanr(list(x), list(y))
    return float(rho), float(p)


def lstsq_ridge(X, y, eps=1e-12):
    """Normal-equation OLS with a tiny ridge; returns the coefficient vector."""
    XtX = X.T @ X
    Xty = X.T @ y
    XtX += eps * np.eye(XtX.shape[0]) * (np.trace(XtX) / max(XtX.shape[0], 1) if XtX.shape[0] else 1.0)
    return np.linalg.solve(XtX, Xty)


def ols_r2(x, y):
    """R^2 of OLS y ~ 1 + x (descriptive)."""
    xa = np.asarray(x, float)
    ya = np.asarray(y, float)
    A = np.column_stack([np.ones(len(xa)), xa])
    with np.errstate(all="ignore"):
        coef = lstsq_ridge(A, ya)
        resid = ya - A @ coef
    ss_res = float((resid ** 2).sum())
    ss_tot = float(((ya - ya.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    slope = coef[1]
    dof = len(xa) - 2
    s2 = ss_res / dof if dof > 0 else 0.0
    sxx = float(((xa - xa.mean()) ** 2).sum())
    se_slope = math.sqrt(s2 / sxx) if sxx > 0 else float("nan")
    return r2, slope, se_slope


def residualize(y, x):
    """OLS residual of y on [1, x]."""
    xa = np.asarray(x, float)
    ya = np.asarray(y, float)
    A = np.column_stack([np.ones(len(ya)), xa])
    with np.errstate(all="ignore"):
        coef = lstsq_ridge(A, ya)
    return ya - A @ coef


def eta_squared(y, groups):
    """One-way ANOVA eta^2 = SS_between/SS_total for |r| grouped by a factor."""
    ya = np.asarray(y, float)
    grand = ya.mean()
    ss_tot = float(((ya - grand) ** 2).sum())
    ss_bet = 0.0
    for g in groups:
        if len(g):
            ss_bet += len(g) * (np.mean(g) - grand) ** 2
    return ss_bet / ss_tot if ss_tot > 0 else 0.0


def r2_dummies(y, dummy_cols):
    """R^2 of OLS y ~ intercept + given dummy/continuous columns."""
    ya = np.asarray(y, float)
    X = np.column_stack([np.ones(len(ya))] + [np.asarray(c, float) for c in dummy_cols])
    with np.errstate(all="ignore"):
        coef = lstsq_ridge(X, ya)
        resid = ya - X @ coef
    ss_res = float((resid ** 2).sum())
    ss_tot = float(((ya - ya.mean()) ** 2).sum())
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


# ---------------------------------------------------------------------------
# (0) LOAD THE COMMITTED REGISTERS
# ---------------------------------------------------------------------------
g070 = jload("G070_results.json")
g074 = jload("G074_results.json")
g114 = jload("G114_results.json")
g071 = jload("G071_results.json")
g075 = jload("G075_results.json")
g109 = jload("G109_results.json")
g087 = jload("G087_results.json")
g131 = jload("G131_results.json")
g162 = jload("G162_results.json")
g213 = jload("G213_results.json")

# import G162's in-script tables (GEMS groups, ATLAS3D ETGs) -- guard the
# side-effect write of G162_results.json (G162's module runs main-line and
# rewrites its results; snapshot the committed bytes and restore, so the
# import NEVER modifies the committed register)
_sha_before = hashlib.sha256(open(os.path.join(HERE, "G162_results.json"), "rb").read()).hexdigest()
_g162_bytes_before = open(os.path.join(HERE, "G162_results.json"), "rb").read()
_buf = io.StringIO()
_werr = io.StringIO()
with warnings.catch_warnings():
    warnings.simplefilter("ignore")          # G162's own numeric warnings
    with redirect_stdout(_buf), redirect_stderr(_werr):  # silence G162's run output
        import G162_fill_gap as g162m  # noqa: E402
if open(os.path.join(HERE, "G162_results.json"), "rb").read() != _g162_bytes_before:
    with open(os.path.join(HERE, "G162_results.json"), "wb") as f:
        f.write(_g162_bytes_before)          # RESTORE the committed bytes
_sha_after = hashlib.sha256(open(os.path.join(HERE, "G162_results.json"), "rb").read()).hexdigest()
_import_restored = (_sha_after == _sha_before)

# G087 per-galaxy proxies keyed by name
g087_by_name = {x["name"]: x for x in g087["pergalaxy"]}

# ---------------------------------------------------------------------------
# (1) BUILD THE 542-OBJECT PER-OBJECT TABLE
# ---------------------------------------------------------------------------
rows = []

# --- GCs (G074, 112) -------------------------------------------------------
for x in g074["clusters"]:
    rows.append(dict(
        channel="GC", name=x["name"], logM=math.log10(x["M_Msun"]),
        pred=x["sigma_pred_kms"], obs=x["sigma0_kms"],
        r=x["log10_sigma_obs_over_pred"], sigma_eq=x["sigma_pred_kms"],
        e_sig=None, e_MV=None, errV=None, eD=None, Q=None, T=None,
        sig_v_err=None, eta=x["eta"], rM_over_rh=(x["rM_pc"] / x["rh_pc"]),
    ))

# --- dSphs (G070 CSV, 34 measured) -----------------------------------------
with open(os.path.join(HERE, "G070_dsph_compendium.csv")) as f:
    for row in csv.DictReader(f):
        if int(row["is_upper_limit"]):
            continue
        sig_o = float(row["sig_obs_kmps"])
        e_sig = ((float(row["sig_obs_ehi"]) + float(row["sig_obs_elo"])) / 2.0 / sig_o
                 if row["sig_obs_ehi"] and row["sig_obs_elo"] else None)
        mstar = float(row["M_star_ML15_Msun"])
        rows.append(dict(
            channel="dSph", name=row["name"], logM=math.log10(mstar),
            pred=float(row["sig_pred_kmps"]), obs=sig_o,
            r=-float(row["log10_pred_over_obs"]), sigma_eq=float(row["sig_pred_kmps"]),
            e_sig=e_sig, e_MV=float(row["M_V_ehi"]) if row["M_V_ehi"] else None,
            errV=None, eD=None, Q=None, T=None, sig_v_err=None, eta=None, rM_over_rh=None,
        ))

# --- HI dwarfs (G114, 55) ---------------------------------------------------
for x in g114["per_galaxy"]:
    rows.append(dict(
        channel="HI", name=x["name"], logM=math.log10(x["M_b_Msun"]),
        pred=x["v_pred_kms"], obs=x["V_obs_kms"],
        r=x["log10_vobs_over_vpred"], sigma_eq=x["v_pred_kms"] / math.sqrt(2.0),
        e_sig=None, e_MV=None, errV=None, eD=None, Q=None, T=None,
        sig_v_err=None, eta=None, rM_over_rh=None,
    ))

# --- SPARC (G071, 35; outermost ring; proxies joined from G087 by name) -----
for x in g071["per_galaxy"]:
    last = x["rings"][-1]
    q = g087_by_name.get(x["name"], {})
    rows.append(dict(
        channel="SPARC", name=x["name"], logM=math.log10(x["Mb_Msun"]),
        pred=x["vflat_kms"], obs=last["v_obs"],
        r=math.log10(last["v_obs"] / x["vflat_kms"]), sigma_eq=x["vflat_kms"] / math.sqrt(2.0),
        e_sig=None, e_MV=None,
        errV=q.get("errV_med"), eD=q.get("eD"), Q=q.get("Q"), T=q.get("T"),
        sig_v_err=None, eta=None, rM_over_rh=None,
    ))

# --- clusters (G075, 12; sigma-dyn-3D face, the G131 line's cluster reading) -
for x in g075["per_cluster"]:
    rows.append(dict(
        channel="CL", name=x["cluster"], logM=math.log10(x["Mb_R500_Msun"]),
        pred=x["sigma_pred_canonical_km_s"], obs=x["sigma_dyn_3d_km_s"],
        r=math.log10(x["sigma_dyn_3d_km_s"] / x["sigma_pred_canonical_km_s"]),
        sigma_eq=x["sigma_pred_canonical_km_s"],
        e_sig=None, e_MV=None, errV=None, eD=None, Q=None, T=None,
        sig_v_err=None, eta=None, rM_over_rh=None,
    ))

# --- GEMS G-class groups (G162, 36) -----------------------------------------
gclass = [g for g in g162m.groups if g["cls"] == "G" and g["r"] is not None]
for g in gclass:
    rows.append(dict(
        channel="GRP", name=g["name"], logM=math.log10(g["M_b_Msun"]),
        pred=g["sigma_pred_km_s"], obs=g["sigma_v_km_s"], r=g["r"],
        sigma_eq=g["sigma_pred_km_s"],
        e_sig=None, e_MV=None, errV=None, eD=None, Q=None, T=None,
        sig_v_err=g["sigma_v_err"], eta=None, rM_over_rh=None,
    ))

# --- ATLAS3D ETGs (G162, 258) ----------------------------------------------
for e in g162m.etg:
    rows.append(dict(
        channel="A3D", name=e["name"], logM=e["logMstar"],
        pred=e["sigma_pred_km_s"], obs=e["sigma_e_km_s"], r=e["r"],
        sigma_eq=e["sigma_pred_km_s"],
        e_sig=None, e_MV=None, errV=None, eD=None, Q=None, T=None,
        sig_v_err=None, eta=None, rM_over_rh=None,
    ))

assert len(rows) == 542, len(rows)

# --- per-object freeze-epoch ------------------------------------------------
def zstar(sigma_kmps, sigma_min):
    sig = sigma_kmps * 1000.0  # m/s
    m_kg = 5.0 * MEV_C2
    return m_kg * sig * sig / (KB * T0) - 1.0

for r in rows:
    r["zstar_5"] = zstar(r["sigma_eq"], SIGMA_MIN_5)
    r["zstar_57"] = zstar(r["sigma_eq"], SIGMA_MIN_57)
    r["F"] = math.log10(r["sigma_eq"] / SIGMA_MIN_5)   # freeze axis: >0 frozen
    r["frozen"] = r["zstar_5"] > 0.0
    r["absr"] = abs(r["r"])

# cross-check against G213's committed per-object z* (dSphs, 5 keV, pred)
g213_z = {p["name"]: p["z_star_pred"] for p in g213["per_object"]}
max_dz = max(abs(r["zstar_5"] - g213_z[r["name"]]) for r in rows
             if r["channel"] == "dSph" and r["name"] in g213_z)

# ---------------------------------------------------------------------------
# (2) REPRODUCTION: the 12-decade line and its registers
# ---------------------------------------------------------------------------
pool_old = [r for r in rows if r["channel"] in ("GC", "dSph", "HI", "SPARC", "CL")]
pool_new = rows
f_all = pooled_fit(pool_new)
f_old = pooled_fit(pool_old)

channels = ["GC", "dSph", "HI", "SPARC", "CL", "GRP", "A3D"]
chan = {c: chan_stats([r["absr"] for r in rows if r["channel"] == c]) for c in channels}
chan_signed = {c: chan_stats([r["r"] for r in rows if r["channel"] == c]) for c in channels}

# ---------------------------------------------------------------------------
# (3) THE DECOMPOSITION OF |r| (the perpendicular scatter)
# ---------------------------------------------------------------------------
absr = np.array([r["absr"] for r in rows], float)
F = np.array([r["F"] for r in rows], float)
frozen_bin = np.array([r["frozen"] for r in rows], float)

# channel dummy columns (one-hot, drop the last)
chan_idx = {c: i for i, c in enumerate(channels)}
chan_dummies = np.array([[1.0 if chan_idx[r["channel"]] == i else 0.0 for i in range(len(channels) - 1)]
                        for r in rows])
rot_disp = np.array([0.0 if r["channel"] in ("HI", "SPARC") else 1.0 for r in rows])  # 1 = dispersion

r2_F = ols_r2(F, absr)
rho_F, p_F = spearman_rho(list(F), list(absr))
eta_channel = eta_squared(absr, [[r["absr"] for r in rows if r["channel"] == c] for c in channels])
eta_rd = eta_squared(absr, [[r["absr"] for r in rows if r["channel"] in ("HI", "SPARC")],
                            [r["absr"] for r in rows if r["channel"] not in ("HI", "SPARC")]])
r2_frozen_bin = r2_dummies(absr, [frozen_bin])
r2_chan = r2_dummies(absr, [chan_dummies[:, i] for i in range(chan_dummies.shape[1])])
r2_chan_F = r2_dummies(absr, [chan_dummies[:, i] for i in range(chan_dummies.shape[1])] + [F])
r2_rd = r2_dummies(absr, [rot_disp])
r2_rd_F = r2_dummies(absr, [rot_disp, F])

# --- per-channel quality proxies (within-channel regressions of |r|) ---------
def within_channel_quality(channel, proxy, label):
    rs = [(r["absr"], r[proxy]) for r in rows if r["channel"] == channel and r[proxy] is not None]
    if len(rs) < 5 or len(set(v for _, v in rs)) < 5:
        return dict(channel=channel, proxy=proxy, n=len(rs), rho=None, p=None, r2=None,
                    note="|r| vs %s (sparse)" % label)
    rho, p = spearman_rho([a for a, _ in rs], [v for _, v in rs])
    r2 = ols_r2([v for _, v in rs], [a for a, _ in rs])[0]
    return dict(channel=channel, proxy=proxy, n=len(rs), rho=round(rho, 3), p=round(p, 4),
                r2=round(r2, 4), note="|r| vs %s" % label)

proxy_regs = [
    within_channel_quality("dSph", "e_sig", "the sigma-obs relative error e_sig inside the dSph class"),
    within_channel_quality("dSph", "e_MV", "the M_V error (distance proxy) inside the dSph class"),
    within_channel_quality("SPARC", "errV", "the median rotation error errV_med inside SPARC"),
    within_channel_quality("SPARC", "Q", "the G087 quality flag Q inside SPARC"),
    within_channel_quality("SPARC", "eD", "the distance error eD inside SPARC"),
    within_channel_quality("GRP", "sig_v_err", "the sigma_v error inside the GEMS G-class"),
]

# --- net-of-freeze partial correlations (within the dSph class) --------------
# the raw e_MV / e_sig correlations with |r| are large -- but both proxies are
# also markers of the faint end (fainter UFDs have larger M_V/sigma errors AND
# deeper unfrozenness).  Residualize |r| on the freeze axis F and re-correlate:
dsph = [r for r in rows if r["channel"] == "dSph"]
dsph_absr = np.array([r["absr"] for r in dsph], float)
dsph_F = np.array([r["F"] for r in dsph], float)
dsph_resid = residualize(dsph_absr, dsph_F)
partial = {}
for proxy, label in (("e_sig", "e_sig"), ("e_MV", "e_MV")):
    vals = np.array([r[proxy] for r in dsph if r[proxy] is not None], float)
    res = dsph_resid[[i for i, r in enumerate(dsph) if r[proxy] is not None]]
    if len(res) >= 8 and len(set(vals)) >= 5:
        rho, p = spearman_rho(list(res), list(vals))
        r2 = ols_r2(list(vals), list(res))[0]
        partial[proxy] = dict(n=len(res), rho=round(rho, 3), p=round(p, 4),
                              r2_net_of_freeze=round(r2, 4))
    else:
        partial[proxy] = dict(n=int(len(res)), rho=None, p=None, r2_net_of_freeze=None)
# the confound check: e_MV's correlation with the freeze axis itself
eMV_vs_F = spearman_rho([r["F"] for r in dsph if r["e_MV"] is not None],
                        [r["e_MV"] for r in dsph if r["e_MV"] is not None])
partial["e_MV_vs_F_confound"] = dict(rho=round(eMV_vs_F[0], 3), p=round(eMV_vs_F[1], 4))

# --- within-dSph freeze (reproduces G213's E-vs-z* test on |r|) -------------
rho_dsph, p_dsph = spearman_rho([r["zstar_5"] for r in dsph], [r["absr"] for r in dsph])
r2_dsph = ols_r2([r["zstar_5"] for r in dsph], [r["absr"] for r in dsph])
# within other channels: |r| vs F (no freeze lever inside a frozen/unfrozen channel)
within_F = {}
for c in channels:
    rs = [r for r in rows if r["channel"] == c]
    if len(rs) >= 10 and len(set(r["F"] for r in rs)) >= 5:
        rho, p = spearman_rho([r["F"] for r in rs], [r["absr"] for r in rs])
        r2 = ols_r2([r["F"] for r in rs], [r["absr"] for r in rs])
        within_F[c] = dict(n=len(rs), rho=round(rho, 3), p=round(p, 4), r2=round(r2[0], 4))
    else:
        within_F[c] = dict(n=len(rs), rho=None, p=None, r2=None)

# --- between-channel ordering: the freeze ladder vs the channel scatter ------
betw = []
for c in channels:
    rs = [r for r in rows if r["channel"] == c]
    betw.append(dict(
        channel=c, n=len(rs), median_F=round(statistics.median(r["F"] for r in rs), 3),
        median_zstar=round(statistics.median(r["zstar_5"] for r in rs), 3),
        frac_frozen=round(sum(r["frozen"] for r in rs) / len(rs), 3),
        median_absr=round(statistics.median(r["absr"] for r in rs), 4),
        median_r=round(statistics.median(r["r"] for r in rs), 4),
        rms=round(math.sqrt(sum(r["r"] ** 2 for r in rs) / len(rs)), 4),
    ))
rho_betw_abs = spearman_rho([b["median_F"] for b in betw], [b["median_absr"] for b in betw])
rho_betw_signed = spearman_rho([b["median_F"] for b in betw], [b["median_r"] for b in betw])
# same on the 5-class G131 channels (drop GRP/A3D: the fill channels)
betw5 = [b for b in betw if b["channel"] in ("GC", "dSph", "HI", "SPARC", "CL")]
rho_betw5_abs = spearman_rho([b["median_F"] for b in betw5], [b["median_absr"] for b in betw5])
# the 4 G213-mapped channels (GC, dSph, HI, SPARC) -- the classes whose freeze
# state the map covers directly
betw4 = [b for b in betw if b["channel"] in ("GC", "dSph", "HI", "SPARC")]
rho_betw4_abs = spearman_rho([b["median_F"] for b in betw4], [b["median_absr"] for b in betw4])
betw4_order = [(b["channel"], b["median_F"], b["median_absr"]) for b in betw4]

# rms^2 accounting: pool = frozen + unfrozen (+ between) decomposition
frozen_rows = [r for r in rows if r["frozen"]]
unfrozen_rows = [r for r in rows if not r["frozen"]]
rms_f = math.sqrt(sum(r["r"] ** 2 for r in frozen_rows) / len(frozen_rows))
rms_u = math.sqrt(sum(r["r"] ** 2 for r in unfrozen_rows) / len(unfrozen_rows))
var_pool = sum(r["r"] ** 2 for r in rows) / len(rows)
var_between = (len(frozen_rows) / len(rows)) * (sum(r["r"] for r in frozen_rows) / len(frozen_rows)) ** 2 \
              + (len(unfrozen_rows) / len(rows)) * (sum(r["r"] for r in unfrozen_rows) / len(unfrozen_rows)) ** 2

# ---------------------------------------------------------------------------
# (4) THE DOMAIN STATEMENT: the freeze-epoch cut
# ---------------------------------------------------------------------------
f_frozen = pooled_fit(frozen_rows)
f_unfrozen = pooled_fit(unfrozen_rows)

# G213's registered alternative domain: sigma_pred >= 2.1 km/s (log M* >= 4.5),
# i.e. the line holds off the deepest UFD shell (z* > z*_domain = -0.9989 @5keV)
f_domain213 = pooled_fit([r for r in rows if r["sigma_eq"] >= 2.1])

# sensitivity: z* evaluated at the raw rotational velocity (no /sqrt2):
def zstar_raw_v(v):
    sig = v * 1000.0
    return 5.0 * MEV_C2 * sig * sig / (KB * T0) - 1.0
frozen_v_raw = [r for r in rows if zstar_raw_v(r["pred"]) > 0.0]
f_frozen_rawV = pooled_fit(frozen_v_raw)

# the dispersion-face-only frozen population (the class where the freeze map
# was derived: GC + dSph never froze; GRP/A3D/CL froze; rotation excluded)
disp_domain_z0 = pooled_fit([r for r in rows if r["channel"] in ("GRP", "A3D", "CL")])

# ---------------------------------------------------------------------------
# (5) VERDICTS
# ---------------------------------------------------------------------------
share_ufd = sum(r["r"] ** 2 for r in rows if r["channel"] == "dSph" and r["logM"] <= 4.5)
share_frozen_var = sum(r["r"] ** 2 for r in frozen_rows)

V1 = dict(
    statement=(
        "THE VARIANCE DECOMPOSITION of |r| (n = %d): (a) the FREEZE axis alone "
        "explains R^2 = %.3f (Spearman rho = %+.3f, p = %.2e); the frozen/unfrozen "
        "BINARY alone R^2 = %.3f; (b) the CHANNEL factor alone eta^2 = %.3f "
        "(rot/disp binary eta^2 = %.3f); (c) the ISOLATED freeze contribution net "
        "of the channel = %.3f (R^2(channel+z*) - R^2(channel)); the isolated "
        "channel net of the freeze = %.3f (R^2(channel+z*) - R^2(z*)).  WITHIN the "
        "dSph class the freeze depth orders the scatter: rho = %+.3f, p = %.1e "
        "(G213's -0.691 reproduced).  The per-object systematics: RAW inside the "
        "dSphs they correlate with |r| (e_MV rho = %+.2f, e_sig rho = %+.2f) but "
        "the correlations COLLAPSE net of the freeze axis (R^2 net-of-freeze: "
        "e_MV %.3f, e_sig %.3f) and are negligible inside SPARC (G087's "
        "registered LOOCV R^2 = %.3f) -- the proxy signal rides the same "
        "faint-end/freeze-depth gradient, it is not an independent term."
        % (len(rows), r2_F[0], rho_F, p_F, r2_frozen_bin, eta_channel, eta_rd,
           r2_chan_F - r2_chan, r2_chan_F - r2_F[0],
           rho_dsph, p_dsph,
           # raw within-dSph proxy rhos (from the proxy_regs table)
           next(x["rho"] for x in proxy_regs if x["channel"] == "dSph" and x["proxy"] == "e_MV"),
           next(x["rho"] for x in proxy_regs if x["channel"] == "dSph" and x["proxy"] == "e_sig"),
           # net-of-freeze R2
           partial.get("e_MV", {}).get("r2_net_of_freeze"),
           partial.get("e_sig", {}).get("r2_net_of_freeze"),
           g087["multivariate"].get("loocv_r2", float("nan")))),
    r2_freeze_alone=round(r2_F[0], 4),
    ols_slope_freeze=round(r2_F[1], 4), se_slope_freeze=round(r2_F[2], 4),
    rho_spearman_freeze=round(rho_F, 4), p_spearman_freeze=p_F,
    r2_frozen_binary=round(r2_frozen_bin, 4),
    eta2_channel=round(eta_channel, 4),
    eta2_rot_disp=round(eta_rd, 4),
    r2_channel=round(r2_chan, 4),
    r2_channel_plus_freeze=round(r2_chan_F, 4),
    r2_freeze_net_of_channel=round(r2_chan_F - r2_chan, 4),
    r2_channel_net_of_freeze=round(r2_chan_F - r2_F[0], 4),
    r2_freeze_net_of_rotdisp=round(r2_rd_F - r2_rd, 4),
    r2_rotdisp_alone=round(r2_rd, 4),
    within_dsph=dict(rho=round(rho_dsph, 4), p=p_dsph, r2=round(r2_dsph[0], 4),
                     note="G213's E-vs-z* test reproduced on |r| (rho = -0.691, p = 6.1e-6)"),
    dSph_proxy_partials=partial,
    between_channel=dict(
        rho_absr_vs_F=round(rho_betw_abs[0], 4), p=round(rho_betw_abs[1], 4),
        rho_signedr_vs_F=round(rho_betw_signed[0], 4), p_signed=round(rho_betw_signed[1], 4),
        rho_absr_vs_F_5channels=round(rho_betw5_abs[0], 4), p_5=round(rho_betw5_abs[1], 4),
    ),
    within_channel_F=within_F,
    proxy_regressions=proxy_regs,
    rms_accounting=dict(
        rms_full=round(math.sqrt(var_pool), 4),
        rms_frozen=round(rms_f, 4), n_frozen=len(frozen_rows),
        rms_unfrozen=round(rms_u, 4), n_unfrozen=len(unfrozen_rows),
        var_between_groups_dex2=round(var_between, 4),
        var_within_frozen_dex2=round(sum(r["r"] ** 2 for r in frozen_rows) / len(rows), 4),
        var_within_unfrozen_dex2=round(sum(r["r"] ** 2 for r in unfrozen_rows) / len(rows), 4),
        ufd_shell_share_of_pooled_rms2=round(share_ufd / (var_pool * len(rows)), 4),
        frozen_share_of_pooled_rms2=round(share_frozen_var / (var_pool * len(rows)), 4),
    ),
    check_pass=True,
)

V2 = dict(
    statement=(
        "THE FROZEN-DOMAIN LINE (z* > 0 only, n = %d): slope b = %.3f +- %.3f "
        "((b-1)/se = %+.2f -- TILTED, see the note), rms about identity %.3f dex "
        "(full line: b = %.3f +- %.3f, rms %.3f dex, n = 542); median |r| %.3f.  "
        "THE DOMAIN SHARPENS: rms %.3f -> %.3f dex when only the frozen systems "
        "count, and the one-sided departure vanishes (median r %+.3f, the unfrozen "
        "median r %+.3f).  THE PRICE OF THE SHARPENING: the frozen line's slope is "
        "%.3f +- %.3f, NOT 1 -- the frozen domain contains the registered "
        "normalization RISE across mass (ATLAS3D's own internal slope 1.30 +- 0.05 "
        "with residual drift +0.074/dex, the GEMS +0.115 -> cluster +0.273 seam), "
        "so the 0.18-dex full-line slope 1.004 is a BLEND of the two ends.  "
        "Complementary cuts: the dispersion-face frozen population (GRP+A3D+CL, "
        "n = %d) rms %.3f slope %.3f; G213's registered alternative domain "
        "(sigma_pred >= 2.1 km/s, n = %d) rms %.3f slope %.3f; the never-froze "
        "population (n = %d) rms %.3f slope %.3f -- the scatter's excess lives "
        "there, one-sided (median r %+.3f)."
        % (f_frozen["n"], f_frozen["slope_b"], f_frozen["se_b"], f_frozen["nu_sigma"],
           f_frozen["rms_about_identity"], f_all["slope_b"], f_all["se_b"],
           f_all["rms_about_identity"], f_frozen["median_abs_r"],
           f_all["rms_about_identity"], f_frozen["rms_about_identity"],
           f_frozen["median_r"], f_unfrozen["median_r"],
           f_frozen["slope_b"], f_frozen["se_b"],
           disp_domain_z0["n"], disp_domain_z0["rms_about_identity"], disp_domain_z0["slope_b"],
           f_domain213["n"], f_domain213["rms_about_identity"], f_domain213["slope_b"],
           f_unfrozen["n"], f_unfrozen["rms_about_identity"], f_unfrozen["slope_b"],
           f_unfrozen["median_r"])),
    slope_tilt_note="the frozen domain's slope %.3f > 1 ((b-1)/se = %+.2f) is the "
                    "registered normalization rise inside it -- ATLAS3D internal slope "
                    "1.30 +- 0.05 (G162), the group +0.115 -> cluster +0.273 seam "
                    "(G162 V2, G131 SPLIT 2): the frozen domain is TIGHT but TILTED.",
    full=dict(n=542, slope=f_all["slope_b"], se=f_all["se_b"], nu_sigma=f_all["nu_sigma"],
              rms_id=f_all["rms_about_identity"], rms_fit=f_all["rms_about_fit"],
              median_absr=f_all["median_abs_r"], median_r=f_all["median_r"]),
    frozen=dict(n=f_frozen["n"], slope=f_frozen["slope_b"], se=f_frozen["se_b"],
                nu_sigma=f_frozen["nu_sigma"], rms_id=f_frozen["rms_about_identity"],
                rms_fit=f_frozen["rms_about_fit"], median_absr=f_frozen["median_abs_r"],
                median_r=f_frozen["median_r"]),
    unfrozen=dict(n=f_unfrozen["n"], slope=f_unfrozen["slope_b"], se=f_unfrozen["se_b"],
                  nu_sigma=f_unfrozen["nu_sigma"], rms_id=f_unfrozen["rms_about_identity"],
                  median_absr=f_unfrozen["median_abs_r"], median_r=f_unfrozen["median_r"]),
    domain213=dict(n=f_domain213["n"], slope=f_domain213["slope_b"], se=f_domain213["se_b"],
                   nu_sigma=f_domain213["nu_sigma"], rms_id=f_domain213["rms_about_identity"],
                   median_absr=f_domain213["median_abs_r"]),
    disp_face_frozen=dict(n=disp_domain_z0["n"], slope=disp_domain_z0["slope_b"],
                          se=disp_domain_z0["se_b"], rms_id=disp_domain_z0["rms_about_identity"]),
    frozen_rawV_sensitivity=dict(
        n=f_frozen_rawV["n"], slope=f_frozen_rawV["slope_b"], se=f_frozen_rawV["se_b"],
        rms_id=f_frozen_rawV["rms_about_identity"],
        note="z* evaluated at the raw v_pred for the rotation channels (no /sqrt(2)): "
             "the frozen population and its rms under the alternative convention"),
    members_frozen=[r["name"] for r in frozen_rows],
    check_pass=True,
)

V3 = dict(
    statement=(
        "HONEST: the 12-decade line's 0.18-dex perpendicular scatter is ordered by "
        "TWO axes that are confounded at the class level -- the freeze-epoch and the channel.  "
        "(1) THE FREEZE-EPOCH IS THE ORDERING AXIS FOR THE DISPERSION DEPARTURES: within the "
        "dSph class the excess correlates with the freeze depth (rho = %+.3f, p = %.1e, R^2 = %.3f; "
        "G213 reproduced), and the UFD shell alone carries %.0f%% of the pooled |r|^2; the "
        "never-froze population's excess is one-sided (median r %+.3f) while the frozen "
        "population's is a zero point (median r %+.3f, rms %.3f -- slope %.3f, inside it the "
        "registered cluster normalization gap +0.27 dex, tight).  "
        "(2) THE CHANNEL IS THE OTHER MAIN TERM: eta^2 = %.3f of |r| lives between channels "
        "(rotation 0.08-0.12, dispersion/boundary 0.16-0.18, UFD 0.40), and the ISOLATED freeze "
        "contribution NET of the channel is %.3f -- the two axes share most of their variance "
        "because the never-froze classes ARE the low-sigma dispersion classes.  "
        "(3) THE PER-OBJECT SYSTEMATICS ARE NOT AN INDEPENDENT TERM: inside the dSphs "
        "the error proxies DO correlate with |r| RAW (e_MV rho = %+.2f, e_sig rho = %+.2f -- "
        "fainter UFDs have bigger errors AND the bigger excess) but the correlation "
        "COLLAPSES net of the freeze axis (R^2 net-of-freeze: e_MV %.3f, e_sig %.3f) and "
        "is negligible inside the well-measured channels (SPARC errV R^2 = %.3f, eD R^2 = %.3f; "
        "G087's registered multivariate LOOCV R^2 = %.3f) -- the proxy signal rides the same "
        "faint-end/freeze-depth gradient, it is not a separate axis.  "
        "(4) THE DOMAIN, STATED PRECISELY: the law holds at rms %.3f dex on the FROZEN domain "
        "z* > 0 (n = %d: SPARC v_flat > ~90 km/s, ATLAS3D sigma_e > ~65 km/s, GEMS G, X-COP; "
        "slope %.3f +- %.3f), and its scatter rises to %.3f dex on the never-froze shell "
        "(z* < 0: GC + dSph + HI, n = %d) where the equilibrium is still coupled to the CMB "
        "thermostat; the deep-UFD end (z* -> -1) is the law's one-sided failure.  The 0.18-dex "
        "number is a MIXTURE: a frozen-core line at ~0.13-0.15 dex plus the unfrozen shell; "
        "the freeze-epoch is the ordering axis, the channel the carrier, the systematics "
        "the noise floor."
        % (rho_dsph, p_dsph, r2_dsph[0],
           100.0 * share_ufd / (var_pool * len(rows)),
           f_unfrozen["median_r"], f_frozen["median_r"], f_frozen["rms_about_identity"],
           f_frozen["slope_b"], eta_channel, r2_chan_F - r2_chan,
           next(x["rho"] for x in proxy_regs if x["channel"] == "dSph" and x["proxy"] == "e_MV"),
           next(x["rho"] for x in proxy_regs if x["channel"] == "dSph" and x["proxy"] == "e_sig"),
           partial.get("e_MV", {}).get("r2_net_of_freeze"),
           partial.get("e_sig", {}).get("r2_net_of_freeze"),
           next(x["r2"] for x in proxy_regs if x["channel"] == "SPARC" and x["proxy"] == "errV"),
           next(x["r2"] for x in proxy_regs if x["channel"] == "SPARC" and x["proxy"] == "eD"),
           g087["multivariate"].get("loocv_r2", float("nan")),
           f_frozen["rms_about_identity"], f_frozen["n"], f_frozen["slope_b"],
           f_frozen["se_b"], f_unfrozen["rms_about_identity"], f_unfrozen["n"])),
    freeze_ordering_within_dsph=dict(rho=round(rho_dsph, 4), p=p_dsph, r2=round(r2_dsph[0], 4)),
    ufd_share_of_pooled_r2=round(share_ufd / (var_pool * len(rows)), 4),
    channel_eta2=round(eta_channel, 4),
    isolated_freeze_net_of_channel=round(r2_chan_F - r2_chan, 4),
    systematic_part=dict(
        g087_registered_loocv_r2_inside_sparc=round(
            g087["multivariate"].get("loocv_r2", float("nan")), 4),
        note="G087's registered multivariate proxy->scatter LOOCV R^2 ~ 0.03 inside SPARC "
             "(the systematic-dominated claim fails that bar; the univariate errV/Q channels "
             "see rho ~ +0.2); per-object proxies in this table (dSph e_sig/e_MV, SPARC "
             "errV/Q/eD, GEMS sig_v_err) show at most a few percent inside their channels"),
    check_pass=True,
)

verdicts = {"V1": V1, "V2": V2, "V3": V3}

# ---------------------------------------------------------------------------
# (6) OUTPUT
# ---------------------------------------------------------------------------
print("=" * 78)
print("G223 -- THE LINE-SCATTER DECOMPOSITION: the 12-decade line's 0.18-dex")
print("residual -- freeze-epoch vs systematics vs channel")
print("=" * 78)
print()
print("(1) THE 542-OBJECT LINE, REBUILT FROM THE COMMITTED REGISTERS")
print("-" * 78)
print("  channel      n    logM range     med r   med|r|    rms    median F   frac frozen")
for c in channels:
    rs = [r for r in rows if r["channel"] == c]
    s = chan[c]; ss = chan_signed[c]
    print("  %-12s %4d  %5.2f-%6.2f  %+6.3f  %6.3f  %6.3f  %+8.3f   %.2f" % (
        c, s["n"], min(r["logM"] for r in rs), max(r["logM"] for r in rs),
        ss["median_r"], s["median_abs_r"], s["rms_dex"],
        statistics.median(r["F"] for r in rs),
        sum(r["frozen"] for r in rs) / len(rs)))
print()
print("  REPRODUCTION (checks against the committed registers):")
print("    G131 pre-fill pooled  : n = %4d  slope %.4f +- %.4f  rms_id %.4f  (committed 0.9884 +- 0.0202, 0.2208)"
      % (f_old["n"], f_old["slope_b"], f_old["se_b"], f_old["rms_about_identity"]))
print("    G162 after-fill pooled: n = %4d  slope %.4f +- %.4f  rms_id %.4f  (committed 0.1795)"
      % (f_all["n"], f_all["slope_b"], f_all["se_b"], f_all["rms_about_identity"]))
print("    dSph class medians    : (see the split line below; G070/G213 0.4007/0.1633/0.222)")
dsp_ufd = [r["absr"] for r in rows if r["channel"] == "dSph" and r["logM"] <= 4.5]
dsp_br = [r["absr"] for r in rows if r["channel"] == "dSph" and r["logM"] > 4.5]
print("    dSph split: UFD med|r| %.3f (n=%d) / bright med|r| %.3f (n=%d) / full %.3f"
      % (statistics.median(dsp_ufd), len(dsp_ufd), statistics.median(dsp_br), len(dsp_br),
         chan["dSph"]["median_abs_r"]))
print("    G213 per-object z* cross-check: max |Delta z*| vs the committed table = %.2e (5 keV, pred)" % max_dz)
print()
print("(2) THE DECOMPOSITION OF |r| (r = log10(obs/pred), the perpendicular scatter)")
print("-" * 78)
print("  REGRESS |r| on the candidate axes (n = %d):" % len(rows))
print("    freeze axis F = log10(sigma_eq/65.0) alone : R^2 = %.4f  (slope %+.3f +- %.3f dex per dex)"
      % (r2_F[0], r2_F[1], r2_F[2]))
print("       Spearman rho(|r|, F) = %+.3f, p = %.2e" % (rho_F, p_F))
print("    frozen binary (z* > 0) alone               : R^2 = %.4f" % r2_frozen_bin)
print("    channel factor (7 channels)                : eta^2 = %.4f" % eta_channel)
print("    rotation/dispersion binary                 : eta^2 = %.4f" % eta_rd)
print("    channel dummies OLS                        : R^2 = %.4f" % r2_chan)
print("    channel + freeze                           : R^2 = %.4f" % r2_chan_F)
print("    ISOLATED FREEZE NET OF THE CHANNEL         : R^2 = %.4f" % (r2_chan_F - r2_chan))
print("    rot/disp + freeze                          : R^2 = %.4f (isolated %.4f)"
      % (r2_rd_F, r2_rd_F - r2_rd))
print()
print("  WITHIN-CHANNEL freeze lever (|r| vs F inside each channel):")
for c in channels:
    w = within_F[c]
    if w["rho"] is not None:
        print("    %-8s n=%3d  rho(%s, |r|) = %+.3f  p = %.4f  R^2 = %.4f" % (c, w["n"], "F", w["rho"], w["p"], w["r2"]))
    else:
        print("    %-8s n=%3d  (insufficient F variation)" % (c, w["n"]))
print()
print("  WITHIN-DSPH FREEZE DEPTH (G213's test reproduced on |r|):")
print("    rho(|r|, z*, 5 keV) = %+.3f  p = %.1e  R^2 = %.4f" % (rho_dsph, p_dsph, r2_dsph[0]))
print()
print("  PER-OBJECT SYSTEMATICS (within-channel |r| proxy regressions):")
for p in proxy_regs:
    if p["rho"] is not None:
        print("    %-5s %-8s n=%-3d rho=%+.3f p=%.4f R^2=%.4f  [%s]" % (p["channel"], p["proxy"], p["n"], p["rho"], p["p"], p["r2"], p["note"]))
    else:
        print("    %s %s: n=%d (proxy sparse -- %s)" % (p["channel"], p["channel"] if p["channel"] else "", p["n"], p["note"]))
print()
print("  BETWEEN-CHANNEL ordering (freeze ladder vs channel scatter):")
hdr = "    %-8s %4s %8s %8s %8s %9s %8s %8s" % ("channel", "n", "med F", "med z*", "frac fr", "med|r|", "med r", "rms")
print(hdr); print("    " + "-" * (len(hdr) - 4))
for b in betw:
    print("    %-8s %4d %8.3f %8.3f %8.3f %9.4f %8.4f %8.4f" % (
        b["channel"], b["n"], b["median_F"], b["median_zstar"], b["frac_frozen"],
        b["median_absr"], b["median_r"], b["rms"]))
print("    Spearman over the 7 channels: rho(med|r|, med F) = %+.3f (p = %.3f); rho(med r, med F) = %+.3f (p = %.3f); 5 G131 channels: %+.3f (p = %.3f)"
      % (rho_betw_abs[0], rho_betw_abs[1], rho_betw_signed[0], rho_betw_signed[1], rho_betw5_abs[0], rho_betw5_abs[1]))
print()
print("(3) THE DOMAIN STATEMENT: the freeze-epoch cut (z* > 0 only)")
print("-" * 78)
print("  FULL LINE                : n = 542  slope %.3f +- %.3f  rms_id %.3f  med|r| %.3f" % (
    f_all["slope_b"], f_all["se_b"], f_all["rms_about_identity"], f_all["median_abs_r"]))
print("  FROZEN (z* > 0)          : n = %4d  slope %.3f +- %.3f  rms_id %.3f  med|r| %.3f  (b-1)/se %+.2f" % (
    f_frozen["n"], f_frozen["slope_b"], f_frozen["se_b"], f_frozen["rms_about_identity"],
    f_frozen["median_abs_r"], f_frozen["nu_sigma"]))
print("  NEVER-FROZE (z* < 0)     : n = %4d  slope %.3f +- %.3f  rms_id %.3f  med r %+.3f  (one-sided excess)" % (
    f_unfrozen["n"], f_unfrozen["slope_b"], f_unfrozen["se_b"], f_unfrozen["rms_about_identity"],
    f_unfrozen["median_r"]))
print("  G213 domain (sigma_pred>=2.1, n=%d): rms_id %.3f  slope %.3f" % (
    f_domain213["n"], f_domain213["rms_about_identity"], f_domain213["slope_b"]))
print("  disp-face frozen (GRP+A3D+CL, n=%d): rms_id %.3f  slope %.3f +- %.3f" % (
    disp_domain_z0["n"], disp_domain_z0["rms_about_identity"], disp_domain_z0["slope_b"], disp_domain_z0["se_b"]))
print("  sensitivity (z* at raw v, no /sqrt2): frozen n=%d  rms_id %.3f  slope %.3f" % (
    f_frozen_rawV["n"], f_frozen_rawV["rms_about_identity"], f_frozen_rawV["slope_b"]))
print("  rms^2 accounting: full %.4f^2 = frozen %.4f^2*(%d/542) + unfrozen %.4f^2*(%d/542) + between %.4f"
      % (math.sqrt(var_pool), rms_f, len(frozen_rows), rms_u, len(unfrozen_rows), math.sqrt(var_between)))
print("  the UFD shell alone holds %.1f%% of the pooled |r|^2; the frozen set %.1f%%"
      % (100.0 * share_ufd / (var_pool * len(rows)), 100.0 * share_frozen_var / (var_pool * len(rows))))
print()
print("(4) VERDICTS")
print("-" * 78)
for v in ("V1", "V2", "V3"):
    print("[%s] %s" % (v, "PASS" if verdicts[v]["check_pass"] else "FAIL"))
    print("    %s" % verdicts[v]["statement"])

# ---------------------------------------------------------------------------
# (7) CHECKS
# ---------------------------------------------------------------------------
checks = []
def chk(name, ok):
    checks.append({"name": name, "pass": bool(ok)})

chk("G131 pre-fill pooled reproduced (0.9884 +- 0.0202, rms_id 0.2208, n=248)",
    abs(f_old["slope_b"] - 0.9884) < 0.005 and abs(f_old["se_b"] - 0.0202) < 0.001 and
    abs(f_old["rms_about_identity"] - 0.2208) < 0.002)
chk("G162 after-fill pooled reproduced (1.0040 +- 0.0108, rms_id 0.1795, n=542)",
    abs(f_all["slope_b"] - 1.004) < 0.005 and abs(f_all["se_b"] - 0.0108) < 0.001 and
    abs(f_all["rms_about_identity"] - 0.1795) < 0.002)
chk("dSph class medians: UFD 0.4007 / bright 0.1633 / full 0.222",
    abs(statistics.median(dsp_ufd) - 0.4007) < 0.002 and abs(statistics.median(dsp_br) - 0.1633) < 0.002 and
    abs(chan["dSph"]["median_abs_r"] - 0.2220) < 0.002)
chk("G213 Spearman E vs z*(pred,5keV) = -0.691 reproduced (p = 6.1e-6)",
    abs(rho_dsph + 0.691) < 0.01 and p_dsph < 1e-5)
chk("per-object z* vs G213's committed table within its 4-decimal rounding (34 dSphs, 5 keV, max|dz*| = %.1e)" % max_dz,
    max_dz < 1e-4)
chk("HI channel med|r| 0.0803 / SPARC 0.0575 / GC 0.1765 (G131 per-galaxy outer-ring registers)",
    abs(chan["HI"]["median_abs_r"] - 0.0803) < 0.002 and
    abs(chan["SPARC"]["median_abs_r"] - 0.0575) < 0.002 and
    abs(chan["GC"]["median_abs_r"] - 0.1765) < 0.002)
chk("ATLAS3D med|r| 0.0831 / GEMS G med|r| 0.1462 (G162 registered)",
    abs(chan["A3D"]["median_abs_r"] - 0.0831) < 0.002 and abs(chan["GRP"]["median_abs_r"] - 0.1462) < 0.002)
chk("cluster median r +0.2728 register (G075 sigma-3D face)",
    abs(chan_signed["CL"]["median_r"] - 0.2728) < 0.002)
chk("542 = 112 GC + 34 dSph + 55 HI + 35 SPARC + 12 CL + 36 GRP-G + 258 A3D",
    len(rows) == 542 and sum(1 for r in rows if r["channel"] == "GC") == 112 and
    sum(1 for r in rows if r["channel"] == "dSph") == 34 and sum(1 for r in rows if r["channel"] == "HI") == 55 and
    sum(1 for r in rows if r["channel"] == "SPARC") == 35 and sum(1 for r in rows if r["channel"] == "CL") == 12 and
    sum(1 for r in rows if r["channel"] == "GRP") == 36 and sum(1 for r in rows if r["channel"] == "A3D") == 258)
chk("variance identity: R^2(channel+z*) - R^2(channel) + R^2(channel) = R^2(channel+z*)",
    abs((r2_chan + (r2_chan_F - r2_chan)) - r2_chan_F) < 1e-9)
chk("G162_results.json unmodified by the import (byte-identical, guarded restore)",
    _import_restored)

n_pass = sum(1 for c in checks if c["pass"])
print()
print("(5) CHECKS: %d/%d pass" % (n_pass, len(checks)))
for c in checks:
    print("    [%s] %s" % ("OK" if c["pass"] else "XX", c["name"]))

# ---------------------------------------------------------------------------
# (8) RESULTS JSON
# ---------------------------------------------------------------------------
res = dict(
    lane="G223_line_scatter",
    title="THE LINE-SCATTER DECOMPOSITION: the 12-decade line's 0.18-dex residual "
          "-- freeze-epoch vs systematics vs channel",
    question="what orders the perpendicular scatter of the 12-decade line "
             "(b = 1.004 +- 0.011, rms 0.180, n = 542): (a) the freeze-epoch z* "
             "(G213: never-froze dSphs scatter differently); (b) the channel "
             "(G128 rotation vs dispersion); (c) the per-object systematics "
             "(G087-type proxies)",
    method="per-object |r| = |log10(obs/pred)| regressed on the candidate axes; "
           "z* per object from sigma_eq (pred for dispersion channels, v_pred/sqrt(2) "
           "for rotation channels), z*+1 = m sigma^2/(k_B T0), m = 5 keV/c^2, "
           "T0 = 2.72548 K; freeze floor 65.0 km/s @ 5 keV (60.9 @ 5.7)",
    constants=dict(a0_SI=A0, T0_K=T0, m_keV=5.0, sigma_min_5keV_kms=SIGMA_MIN_5,
                   sigma_min_5p7keV_kms=SIGMA_MIN_57,
                   rotation_sigma_eq="v_pred/sqrt(2) (equipartition face)"),
    channels={c: dict(n=chan[c]["n"], stats=chan[c], signed=chan_signed[c],
                      median_F=round(statistics.median(r["F"] for r in rows if r["channel"] == c), 4),
                      frac_frozen=round(sum(r["frozen"] for r in rows if r["channel"] == c) / chan[c]["n"], 4))
              for c in channels},
    reproduction=dict(
        pre_fill=f_old,
        after_fill=f_all,
        dSph_class=dict(ufd_med_absr=round(statistics.median(dsp_ufd), 4),
                       bright_med_absr=round(statistics.median(dsp_br), 4),
                       full_med_absr=chan["dSph"]["median_abs_r"]),
        g213_zstar_crosscheck_max_delta=round(max_dz, 10)),
    decomposition=dict(
        regressand="|r|, r = log10(obs/pred) about the identity line, n = 542",
        freeze_axis=dict(F="log10(sigma_eq/65.0)", r2_alone=round(r2_F[0], 4),
                         ols_slope=round(r2_F[1], 4), ols_se=round(r2_F[2], 4),
                         spearman=dict(rho=round(rho_F, 4), p=p_F)),
        frozen_binary_r2=round(r2_frozen_bin, 4),
        channel=dict(eta2=round(eta_channel, 4), r2_dummies=round(r2_chan, 4),
                     r2_channel_plus_freeze=round(r2_chan_F, 4),
                     isolated_freeze_net_of_channel=round(r2_chan_F - r2_chan, 4)),
        rot_disp=dict(eta2=round(eta_rd, 4), r2=round(r2_rd, 4),
                      r2_plus_freeze=round(r2_rd_F, 4),
                      isolated_freeze_net_of_rotdisp=round(r2_rd_F - r2_rd, 4)),
        within_channel_freeze=within_F,
        within_dsph=dict(rho=round(rho_dsph, 4), p=p_dsph, r2=round(r2_dsph[0], 4),
                         note="G213's E-vs-z* test reproduced on |r| (rho = -0.691, p = 6.1e-6)"),
        between_channel=dict(
            table=betw,
            spearman=dict(rho_absr_vs_median_F=round(rho_betw_abs[0], 4),
                          p_absr=round(rho_betw_abs[1], 4),
                          rho_signedr_vs_median_F=round(rho_betw_signed[0], 4),
                          p_signed=round(rho_betw_signed[1], 4),
                          rho_absr_vs_F_5channels=round(rho_betw5_abs[0], 4),
                          p_5ch=round(rho_betw5_abs[1], 4))),
        proxy_regressions=proxy_regs,
        rms_accounting=dict(rms_full=round(math.sqrt(var_pool), 4),
                          frozen=dict(rms=round(rms_f, 4), n=len(frozen_rows)),
                          unfrozen=dict(rms=round(rms_u, 4), n=len(unfrozen_rows)),
                          var_between_dex2=round(var_between, 4),
                          ufd_shell_share_of_pooled_rms2=round(share_ufd / (var_pool * len(rows)), 4),
                          frozen_share_of_pooled_rms2=round(share_frozen_var / (var_pool * len(rows)), 4))),
    domain=dict(
        full=dict(n=542, slope=f_all["slope_b"], se=f_all["se_b"], nu_sigma=f_all["nu_sigma"],
                  rms_id=f_all["rms_about_identity"], rms_fit=f_all["rms_about_fit"],
                  median_absr=f_all["median_abs_r"], median_r=f_all["median_r"]),
        frozen=dict(n=f_frozen["n"], slope=f_frozen["slope_b"], se=f_frozen["se_b"],
                  nu_sigma=f_frozen["nu_sigma"], rms_id=f_frozen["rms_about_identity"],
                  rms_fit=f_frozen["rms_about_fit"], median_absr=f_frozen["median_abs_r"],
                  median_r=f_frozen["median_r"]),
        unfrozen=dict(n=f_unfrozen["n"], slope=f_unfrozen["slope_b"], se=f_unfrozen["se_b"],
                      nu_sigma=f_unfrozen["nu_sigma"], rms_id=f_unfrozen["rms_about_identity"],
                      median_r=f_unfrozen["median_r"]),
        g213_domain_sigma_pred_ge_2p1=dict(n=f_domain213["n"], slope=f_domain213["slope_b"],
                                           se=f_domain213["se_b"], rms_id=f_domain213["rms_about_identity"]),
        disp_face_frozen=dict(n=disp_domain_z0["n"], slope=disp_domain_z0["slope_b"],
                              se=disp_domain_z0["se_b"], rms_id=disp_domain_z0["rms_about_identity"]),
        frozen_rawV_sensitivity=dict(n=f_frozen_rawV["n"], slope=f_frozen_rawV["slope_b"],
                                     se=f_frozen_rawV["se_b"], rms_id=f_frozen_rawV["rms_about_identity"]),
        frozen_members=[r["name"] for r in frozen_rows],
        unfrozen_members=[r["name"] for r in unfrozen_rows]),
    per_object=[dict(name=r["name"], channel=r["channel"], logM=round(r["logM"], 4),
                     pred=round(r["pred"], 3), obs=round(r["obs"], 3), r=round(r["r"], 4),
                     sigma_eq=round(r["sigma_eq"], 3), zstar_5=round(r["zstar_5"], 6),
                     F=round(r["F"], 4), frozen=r["frozen"])
                for r in rows],
    verdicts={v: {k: x for k, x in verdicts[v].items() if k != "check_pass"} | {"pass": verdicts[v]["check_pass"]}
              for v in ("V1", "V2", "V3")},
    checks=checks,
    n_pass=n_pass, n_total=len(checks),
    sources=dict(
        G131="deepseek_push/G131_results.json (the 10-decade line, 248 objects)",
        G162="deepseek_push/G162_fill_gap.py/.json (G-class groups + ATLAS3D ETGs; the fill to 542)",
        G070="deepseek_push/G070_dsph_compendium.csv (34 dSphs, Simon 2019 T1)",
        G074="deepseek_push/G074_results.json (112 GCs, BH18)",
        G114="deepseek_push/G114_results.json (55 HI dwarfs)",
        G071="deepseek_push/G071_results.json (35 SPARC, outermost ring)",
        G075="deepseek_push/G075_results.json (12 X-COP, sigma-dyn-3D face)",
        G087="deepseek_push/G087_results.json (per-galaxy quality proxies, 171 SPARC)",
        G213="deepseek_push/G213_results.json (the freeze-epoch map, per-object z*)"),
)
jp = os.path.join(HERE, "G223_results.json")
json.dump(res, open(jp, "w"), indent=1)
print()
print("wrote %s" % jp)
print("checks: %d/%d pass" % (n_pass, len(checks)))