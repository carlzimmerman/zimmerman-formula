#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG166 -- referee re-derivation of CFG164 (a measured PHIBSS gas prior for the KURVS discs; decision-cell verdict
marginalised over it).  Written from CFG166_FROZEN_CRITERIA.md alone; no CFG164 script/.out/.json was open.

Main:    ZF_REPO=<repo> python3 CFG166_gas_prior_referee.py            -> CFG166_main.out / CFG166_main_results.json ; rc 0 iff C1-C3 + counts pass
MUTATE:  MUTATE={0a,0b,1,2,3,4,5,6} python3 ...                        -> CFG166_MUTATE_<k>.out/_results.json ; rc 1 iff the control bites (6: always 0)

SHARED, NOT INDEPENDENT: the CFG165 referee module (decision-cell map: load_kurvs, load_sparc_anchor, cell, classify, spec,
alpha_K, which imports CFG4_common nu_mono) and all data tables.  Re-derived here: the prior, the marginalisation, P1-P3, R0, H1.
"""
import os
import sys
import json
import math
import time
import hashlib

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "data_assembly")):
        return r
    d = HERE
    for _ in range(10):
        if os.path.isdir(os.path.join(d, "data_assembly")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO")


REPO = find_repo()
_MUT = os.environ.pop("MUTATE", None)          # the CFG165 module reads MUTATE at import; keep it out of that
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG165_kurvs_referee"))
os.environ["ZF_REPO"] = REPO
import CFG165_referee_kurvs_p4 as M165           # noqa: E402  (SHARED: map code)
MODE = _MUT if _MUT is not None else "0"

LN15, LN13 = math.log(1.5), math.log(1.3)
S_PLACED = (1.00, 1.42, 1.62, 1.69, 3.00)
WIN_R = (0.6, 1.7)
WIN_F = (2.1, 3.7)
ULIRG = 0.8 / 4.36
NKURVS = 10
KURVS15_POS = None


def P(*a):
    print(" ".join(str(x) for x in a), flush=True)


def rel(p):
    return os.path.relpath(p, REPO).replace(os.sep, "/")


# ------------------------------------------------------------------------------------------------- data
class Rows:
    pass


def load_phibss():
    import csv
    with open(os.path.join(REPO, "data_assembly/kmos3d_phibss/phibss13_joined.csv"), newline="") as f:
        R = list(csv.DictReader(f))

    def fn(x):
        try:
            return float(x)
        except Exception:
            return float("nan")
    allr = []
    for r in R:
        allr.append(dict(name=r["name"], comp=r["comp"], type=r["type"], mmol=fn(r["mmol_msun"]), mstar=fn(r["mstar_msun"]),
                         z=fn(r["z_co"]), sfr=fn(r["sfr_msun_yr"]), ul=r["co_upper_limit"] == "1",
                         inc=r["fgas_inconsistent_in_source"] == "1", fgas_re=fn(r["fgas_recomputed"]), fgas_q=fn(r["fgas_quoted"])))
    clean = [r for r in allr if (not r["ul"]) and (not r["inc"]) and r["comp"] != "se"
             and all(math.isfinite(r[k]) for k in ("mmol", "mstar", "z"))]
    C = Rows()
    C.name = [r["name"] for r in clean]
    C.z = np.array([r["z"] for r in clean])
    C.lm = np.log10([r["mstar"] for r in clean])
    C.mu = np.array([r["mmol"] / r["mstar"] for r in clean])
    C.sfr = np.array([r["sfr"] for r in clean])
    C.mmol = np.array([r["mmol"] for r in clean])
    C.mstar = np.array([r["mstar"] for r in clean])
    C.fgas_re = np.array([r["fgas_re"] for r in clean])
    C.n_all = len(allr)
    C.allrows = allr
    return C


def win(C, zlo=1.0, zhi=1.7, mlo=9.5, mhi=10.8):
    return np.where((C.z >= zlo) & (C.z <= zhi) & (C.lm >= mlo) & (C.lm <= mhi))[0]


def load_kurvs_extra():
    import csv
    with open(os.path.join(REPO, "data_assembly/arxiv_tables/kurvs2023_integrated.csv"), newline="") as f:
        I = {int(r["kurvs_id"]): r for r in csv.DictReader(f)}
    return I


def ols(x, y):
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    n = len(y)
    s2 = float(res @ res) / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    return dict(a=float(beta[0]), b=float(beta[1]), scatter=math.sqrt(s2), scatter0=math.sqrt(float(res @ res) / n),
                se_b=float(math.sqrt(cov[1, 1])), se_a=float(math.sqrt(cov[0, 0])), n=n)


# ------------------------------------------------------------------------------------------------- draws
def sysfac(rng, N, on=True):
    if not on:
        return np.ones(N)
    n1 = rng.standard_normal(N)
    n2 = rng.standard_normal(N)
    return np.exp(LN15 * n1) / np.exp(LN13 * n2)


def draw_rows(rng, N, mu_rows, sys=True, mode="indep", zrows=None, zK=None, expo=None, nd=NKURVS):
    """returns (N, nd) total-gas-over-M* draws at h=0.  mode: indep | hyper | lognormal | coherent | median"""
    f = sysfac(rng, N, sys)
    n = len(mu_rows)
    if mode == "indep":
        idx = rng.integers(0, n, (N, nd))
        mu = mu_rows[idx]
        if zrows is not None:
            mu = mu * ((1 + zK[None, :]) / (1 + zrows[idx])) ** expo
    elif mode == "hyper":
        hb = rng.integers(0, n, (N, n))
        pick = rng.integers(0, n, (N, nd))
        mu = mu_rows[np.take_along_axis(hb, pick, axis=1)]
    elif mode == "lognormal":
        lg = np.log10(mu_rows)
        mu = 10.0 ** (lg.mean() + lg.std(ddof=1) * rng.standard_normal((N, nd)))
    elif mode == "coherent":
        idx = rng.integers(0, n, (N, 1))
        mu = np.repeat(mu_rows[idx], nd, axis=1)
    elif mode == "median":
        mu = np.full((N, nd), np.median(mu_rows))
    else:
        raise ValueError(mode)
    return mu * f[:, None]


def draw_M(rng, N, fit, lmK, sys=True, slope=None, nd=NKURVS):
    f = sysfac(rng, N, sys)
    b = fit["b"] if slope is None else slope
    eps = fit["scatter"] * rng.standard_normal((N, nd))
    mu = 10.0 ** (fit["a"] + b * (lmK[None, :] - 10.5) + eps)
    return mu * f[:, None]


# ------------------------------------------------------------------------------------------------- pipeline
class Pipe:
    def __init__(self, inc_col="inc_star_deg"):
        self.S = M165.load_kurvs(inc_col=inc_col)
        self.AS = M165.load_sparc_anchor()
        self.spec = {}

    def sp(self, s, kind="P4"):
        k = (s, kind)
        if k not in self.spec:
            self.spec[k] = M165.spec("P4", scale=float(s)) if kind == "P4" else M165.SP["P2"]
        return self.spec[k]

    def cellz(self, mu, s, kind="P4"):
        r = M165.cell(self.S, self.AS, self.sp(s, kind), mu, 0.0, "canonical")
        return r["flat"]["z"], r["H"]["z"], r["flat"]["dprime"], r["H"]["dprime"], r["flat"]["sigma"], r["H"]["sigma"]

    def eval(self, mus, s, kind="P4"):
        n = len(mus)
        zf = np.empty(n)
        zh = np.empty(n)
        for i in range(n):
            a = self.cellz(mus[i], s, kind)
            zf[i], zh[i] = a[0], a[1]
        return zf, zh


def classes(zf, zh, swap=False):
    if swap:
        zf, zh = zh, zf
    fw, rw = np.abs(zf) <= 2.0, np.abs(zh) <= 2.0
    flat = fw & (zh < -2.0)
    riv = (~flat) & rw & (zf > 2.0)
    both = (~flat) & (~riv) & fw & rw
    neither = ~(flat | riv | both)
    return dict(flat=float(flat.mean()), rival=float(riv.mean()), both=float(both.mean()), neither=float(neither.mean()))


def pct(x, q):
    return float(np.percentile(x, q))


def summarise(pipe, mu, svals=S_PLACED, swap=False, with_p2spec=False):
    """mu: (N,10).  returns dict"""
    mbar = np.median(mu, axis=1)
    out = dict(N=int(len(mu)), median=pct(mbar, 50), p16=pct(mbar, 16), p84=pct(mbar, 84))
    out["width_dex"] = math.log10(out["p84"] / out["p16"])
    out["P1_mbar"] = dict(rival=float(np.mean((mbar >= WIN_R[0]) & (mbar <= WIN_R[1]))),
                          between=float(np.mean((mbar > WIN_R[1]) & (mbar < WIN_F[0]))),
                          flat=float(np.mean((mbar >= WIN_F[0]) & (mbar <= WIN_F[1]))),
                          below=float(np.mean(mbar < WIN_R[0])), above=float(np.mean(mbar > WIN_F[1])))
    fl = mu.ravel()
    out["P1_disc"] = dict(rival=float(np.mean((fl >= WIN_R[0]) & (fl <= WIN_R[1]))), flat=float(np.mean((fl >= WIN_F[0]) & (fl <= WIN_F[1]))))
    out["P2"] = {}
    for s in svals:
        zf, zh = pipe.eval(mu, s)
        c = classes(zf, zh, swap)
        c["zf_med"], c["zf_16"], c["zf_84"] = pct(zf, 50), pct(zf, 16), pct(zf, 84)
        c["zh_med"], c["zh_16"], c["zh_84"] = pct(zh, 50), pct(zh, 16), pct(zh, 84)
        out["P2"][f"{s:.2f}"] = c
    if with_p2spec:
        zf, zh = pipe.eval(mu, 3.0, kind="P2")
        out["P2spec_s3"] = classes(zf, zh)
    return out


def fmt_sum(name, o):
    P(f"  {name:34s} N={o['N']:6d} mu-bar median {o['median']:.3f} (16-84: {o['p16']:.3f}-{o['p84']:.3f}) width {o['width_dex']:.3f} dex"
      f" | P1 rival {o['P1_mbar']['rival']:.3f} flat {o['P1_mbar']['flat']:.3f} between {o['P1_mbar']['between']:.3f} below {o['P1_mbar']['below']:.3f} above {o['P1_mbar']['above']:.3f}")
    for s, c in o["P2"].items():
        P(f"      s={s}: flat {c['flat']:.3f} rival {c['rival']:.3f} both {c['both']:.3f} neither {c['neither']:.3f} | zf med {c['zf_med']:+.2f} ({c['zf_16']:+.2f},{c['zf_84']:+.2f}) zH med {c['zh_med']:+.2f} ({c['zh_16']:+.2f},{c['zh_84']:+.2f})")


def all_priors(pipe, C, N, seed, svals=S_PLACED, verbose=True):
    """the six frozen priors on common draws where the frozen text says so (h and alpha_CO are rescalings of the primary draws)"""
    S = pipe.S
    sel = win(C)
    mrows = C.mu[sel]
    lmK, zK = S.logM, S.z
    fit = ols(C.lm[C.z < 1.7] - 10.5, np.log10(C.mu[C.z < 1.7]))
    res = {}
    rng = np.random.default_rng(seed)
    mu = draw_rows(rng, N, mrows)
    res["primary"] = summarise(pipe, mu, svals, with_p2spec=True)
    p3 = dict(mu15_med=pct(mu[:, KURVS15_POS], 50), frac_gt_1p90=float(np.mean(mu[:, KURVS15_POS] > 1.90)),
              frac_gt_3p79=float(np.mean(mu[:, KURVS15_POS] > 3.79)))
    for h in (0.5, 1.0):
        m2 = mu * (1 + h)
        res[f"h={h}"] = summarise(pipe, m2, svals)
        res[f"h={h}"]["P3"] = dict(mu15_med=pct(m2[:, KURVS15_POS], 50), frac_gt_1p90=float(np.mean(m2[:, KURVS15_POS] > 1.90)),
                                   frac_gt_3p79=float(np.mean(m2[:, KURVS15_POS] > 3.79)))
    res["primary"]["P3"] = p3
    rngM = np.random.default_rng(seed)
    res["variantM"] = summarise(pipe, draw_M(rngM, N, fit, lmK), svals)
    res["variantM"]["fit"] = fit
    rngZ = np.random.default_rng(seed)
    muZ = draw_rows(rngZ, N, mrows, zrows=C.z[sel], zK=zK, expo=2.5)
    res["variantZ"] = summarise(pipe, muZ, svals)
    res["alphaCO_ULIRG"] = summarise(pipe, mu * ULIRG, svals)
    if verbose:
        for k, v in res.items():
            fmt_sum(k, v)
    return res, fit, mrows


# ------------------------------------------------------------------------------------------------- README targets
TARGET = {
    "primary": dict(median=1.01, p16=0.60, p84=1.69, rival_win=0.68, flat_win=0.07, s1=(0.21, 0.55, 0.24), rival_hi=(0.70, 0.81)),
    "h=0.5": dict(median=1.57, p16=0.91, p84=2.57, s1=(0.47, 0.24, 0.25), rival_hi=(0.58, 0.68)),
    "h=1.0": dict(median=2.05, p16=1.19, p84=3.47, s1=(0.59, 0.11, 0.19), rival_hi=(0.37, 0.52)),
    "variantM": dict(median=1.30, p16=0.75, p84=2.26, s1=(0.37, 0.32, 0.29), rival_hi=(0.67, 0.70)),
    "variantZ": dict(median=1.31, p16=0.75, p84=2.19, s1=(0.33, 0.31, 0.34), rival_hi=(0.65, 0.71)),
    "alphaCO_ULIRG": dict(median=0.18, p16=0.11, p84=0.31, s1=(0.00, 1.00, 0.00), rival_hi=(0.01, 0.06)),
}


def rel_ok(m, t, rel_tol, floor=0.0):
    return abs(m - t) <= max(rel_tol * abs(t), floor)


def compare(res, tag):
    """returns list of (row, mine, target, tol, verdict)"""
    rows = []

    def add(row, mine, tgt, tol, ok):
        rows.append(dict(row=row, mine=mine, target=tgt, tol=tol, ok=bool(ok)))
    for k, T in TARGET.items():
        o = res[k]
        prim = (k == "primary")
        add(f"{k}: median mu-bar", o["median"], T["median"], "4% (min .03)", rel_ok(o["median"], T["median"], 0.04, 0.03))
        add(f"{k}: 16th pct", o["p16"], T["p16"], "7%", rel_ok(o["p16"], T["p16"], 0.07))
        add(f"{k}: 84th pct", o["p84"], T["p84"], "7%", rel_ok(o["p84"], T["p84"], 0.07))
        c = o["P2"]["1.00"]
        tol = 0.03 if prim else 0.04
        for nm, mv, tv in zip(("lean flat", "lean rival", "both"), (c["flat"], c["rival"], c["both"]), T["s1"]):
            add(f"{k}: s=1.00 {nm}", mv, tv, f"{tol} abs", abs(mv - tv) <= tol)
        rv = [o["P2"][f"{s:.2f}"]["rival"] for s in (1.42, 1.62, 1.69)]
        add(f"{k}: rival min over s=1.42/1.62/1.69", min(rv), T["rival_hi"][0], "0.04 abs", abs(min(rv) - T["rival_hi"][0]) <= 0.04)
        add(f"{k}: rival max over s=1.42/1.62/1.69", max(rv), T["rival_hi"][1], "0.04 abs", abs(max(rv) - T["rival_hi"][1]) <= 0.04)
    o = res["primary"]
    add("P1 primary: fraction in rival window", o["P1_mbar"]["rival"], 0.68, "0.03 abs", abs(o["P1_mbar"]["rival"] - 0.68) <= 0.03)
    add("P1 primary: fraction in flat window", o["P1_mbar"]["flat"], 0.07, "0.03 abs", abs(o["P1_mbar"]["flat"] - 0.07) <= 0.03)
    add("R0 primary: width (dex)", o["width_dex"], 0.45, "0.03 dex", abs(o["width_dex"] - 0.45) <= 0.03)
    add("P3 primary: frac mu_15 > 1.90", o["P3"]["frac_gt_1p90"], 0.16, "0.04 abs", abs(o["P3"]["frac_gt_1p90"] - 0.16) <= 0.04)
    add("P3 primary: median mu_15", o["P3"]["mu15_med"], 1.00, "4% (min .03)", rel_ok(o["P3"]["mu15_med"], 1.00, 0.04, 0.03))
    add("P3 h=1: frac mu_15 > 1.90", res["h=1.0"]["P3"]["frac_gt_1p90"], 0.53, "0.04 abs", abs(res["h=1.0"]["P3"]["frac_gt_1p90"] - 0.53) <= 0.04)
    add("Variant M slope", res["variantM"]["fit"]["b"], -0.22, "0.02", abs(res["variantM"]["fit"]["b"] + 0.22) <= 0.02)
    add("Variant M scatter (ddof 2)", res["variantM"]["fit"]["scatter"], 0.28, "0.02 dex", abs(res["variantM"]["fit"]["scatter"] - 0.28) <= 0.02)
    mx = max(o["P2"]["1.00"][k] for k in ("flat", "rival", "both"))
    add("H1: max class at s=1 < 0.68 -> NON-DIAGNOSTIC", mx, "<0.68", "label", mx < 0.68)
    return rows


# ------------------------------------------------------------------------------------------------- main
def main():
    global KURVS15_POS
    t0 = time.time()
    outj = dict(mode=MODE, checks={}, numbers={})
    checks = []

    def check(name, ok, meas):
        checks.append((name, bool(ok)))
        outj["checks"][name] = dict(ok=bool(ok), measured=str(meas))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {meas}")

    P("=" * 110)
    P(f"CFG166 referee re-derivation of CFG164.  MODE={MODE}.  repo=<repo>")
    P("=" * 110)
    pipe = Pipe("inc_star_deg")
    S = pipe.S
    KURVS15_POS = S.ids.index(15)
    C = load_phibss()
    sel = win(C)
    z17 = C.z < 1.7
    P("\n-- counts and controls")
    check("C2 counts: 73 rows, 51 clean, 17 matched, 38 clean z<1.7", (C.n_all, len(C.mu), len(sel), int(z17.sum())) == (73, 51, 17, 38),
          (C.n_all, len(C.mu), len(sel), int(z17.sum())))
    check("C2b every clean z<1.7 row has log M* >= 10.40 (rounded 2dp); KURVS discs below 10.40: 8 of 10",
          bool(np.all(np.round(C.lm[z17], 2) >= 10.40)) and int(np.sum(S.logM < 10.40)) == 8, (float(C.lm[z17].min()), int(np.sum(S.logM < 10.40))))
    fg = C.mmol / (C.mmol + C.mstar)
    check("C3 fgas_recomputed = Mmol/(Mmol+M*) on the clean rows to 1e-6", float(np.max(np.abs(fg - C.fgas_re))) < 1e-6, float(np.max(np.abs(fg - C.fgas_re))))
    r = pipe.cellz(np.full(10, 0.67), 1.0)
    check("C1 mu=0.67 for all discs reproduces CFG160's cell (+0.1441 / -0.0060) within 0.0005", abs(r[2] - 0.1441) < 5e-4 and abs(r[3] + 0.0060) < 5e-4,
          (round(r[2], 4), round(r[3], 4)))
    r2 = pipe.cellz(np.full(10, 0.67), 1.0)
    outj["numbers"]["decision_cell_mu067"] = dict(dflat=r[2], dH=r[3], zf=r[0], zh=r[1])
    mrows = C.mu[sel]
    P(f"  17 matched rows: mu_mol median {np.median(mrows):.3f}, 16-84 {np.percentile(mrows,16):.3f}-{np.percentile(mrows,84):.3f}, sd log10 {np.log10(mrows).std(ddof=1):.3f}")
    outj["numbers"]["matched_rows"] = dict(median=float(np.median(mrows)), sdlog=float(np.log10(mrows).std(ddof=1)), n=len(mrows))
    fit = ols(C.lm[z17] - 10.5, np.log10(C.mu[z17]))
    P(f"  Variant M fit (38 rows): a={fit['a']:.4f} (mu at 10.5 = {10**fit['a']:.3f}) b={fit['b']:.4f} se_b={fit['se_b']:.4f} scatter(ddof2)={fit['scatter']:.4f} (ddof0 {fit['scatter0']:.4f})")

    if MODE == "0":
        return main_run(pipe, C, outj, checks, t0)
    return mutate_run(pipe, C, outj, checks, t0, fit)


def main_run(pipe, C, outj, checks, t0):
    P("\n-- PARITY run: N=4000, seed 164, one generator per prior")
    res4, fit, mrows = all_priors(pipe, C, 4000, 164)
    P("\n-- CONVERGED run: N=40000, seed 166")
    res40, _, _ = all_priors(pipe, C, 40000, 166)
    P("\n-- R0 power: width of mu-bar (dex) vs break-even separation")
    sep = math.log10(2.11 / 0.62)
    P(f"  primary width {res40['primary']['width_dex']:.3f} dex (parity {res4['primary']['width_dex']:.3f}) vs separation {sep:.3f} dex")
    P("\n-- H1: class probabilities at s=1, primary, h=0 (converged)")
    c = res40["primary"]["P2"]["1.00"]
    mx = max(c["flat"], c["rival"], c["both"])
    P(f"  lean flat {c['flat']:.3f} lean rival {c['rival']:.3f} both {c['both']:.3f} neither {c['neither']:.3f}; max class {mx:.3f} -> "
      f"{'DIAGNOSTIC' if mx >= 0.68 else 'NON-DIAGNOSTIC'}")
    P("\n-- s=3 diagnostic: true P2 spec vs alpha x 3.0 (primary, converged)")
    P("  alpha x 3.0:", {k: round(v, 3) for k, v in res40["primary"]["P2"]["3.00"].items() if k in ("flat", "rival", "both", "neither")})
    P("  P2 spec     :", {k: round(v, 3) for k, v in res40["primary"]["P2spec_s3"].items()})
    P("\n-- MC-consistency of the parity run vs the converged run (frozen: within 4 sqrt(p(1-p)/4000) + 0.01)")
    bad = 0
    for k in res40:
        for s in res40[k]["P2"]:
            for cl in ("flat", "rival", "both", "neither"):
                p40, p4 = res40[k]["P2"][s][cl], res4[k]["P2"][s][cl]
                lim = 4 * math.sqrt(max(p40 * (1 - p40), 1e-4) / 4000) + 0.01
                if abs(p40 - p4) > lim:
                    bad += 1
                    P(f"  MC-INCONSISTENT {k} s={s} {cl}: converged {p40:.3f} parity {p4:.3f} lim {lim:.3f}")
    P(f"  inconsistent entries: {bad}")
    rows40 = compare(res40, "converged")
    rows4 = compare(res4, "parity")
    P("\n-- PASS-LINE TABLE (converged run vs README target; parity run in the last column)")
    npass = 0
    for a, b in zip(rows40, rows4):
        tm = a["mine"]
        P(f"  [{'PASS' if a['ok'] else 'FAIL'}] {a['row']:52s} mine {tm if isinstance(tm, str) else format(tm, '.3f')}  target {a['target']}  tol {a['tol']}  | parity {'PASS' if b['ok'] else 'fail'} ({b['mine'] if isinstance(b['mine'], str) else format(b['mine'], '.3f')})")
        npass += a["ok"]
    P(f"  {npass}/{len(rows40)} converged-run rows within their pass lines")
    P("\n-- inc_sfr_deg diagnostic (primary, s=1, N=4000 seed 164; the frozen main uses inc_star_deg)")
    pipe2 = Pipe("inc_sfr_deg")
    pipe2.S = pipe2.S
    o = summarise(pipe2, draw_rows(np.random.default_rng(164), 4000, mrows), (1.0,))
    P("  inc_sfr:", {k: round(v, 3) for k, v in o["P2"]["1.00"].items() if k in ("flat", "rival", "both", "neither")})
    outj["parity"] = res4
    outj["converged"] = res40
    outj["pass_table_converged"] = rows40
    outj["pass_table_parity"] = rows4
    outj["inc_sfr_diag"] = o["P2"]["1.00"]
    outj["R0"] = dict(width_dex=res40["primary"]["width_dex"], separation_dex=sep)
    outj["elapsed_s"] = round(time.time() - t0, 1)
    okc = all(ok for _, ok in checks)
    P(f"\n{sum(ok for _, ok in checks)}/{len(checks)} controls pass; H1 = {'DIAGNOSTIC' if mx >= 0.68 else 'NON-DIAGNOSTIC'}; elapsed {outj['elapsed_s']} s")
    with open(os.path.join(HERE, "CFG166_main_results.json"), "w") as f:
        json.dump(outj, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    return 0 if okc else 1


def mutate_run(pipe, C, outj, checks, t0, fit):
    S = pipe.S
    sel = win(C)
    mrows = C.mu[sel]
    N = 10000
    seed = 166
    svals = (1.0,)
    prim = summarise(pipe, draw_rows(np.random.default_rng(seed), N, mrows), svals)
    pc = prim["P2"]["1.00"]
    P(f"\n-- primary at N={N}, seed {seed}: flat {pc['flat']:.3f} rival {pc['rival']:.3f} both {pc['both']:.3f}")
    rng = np.random.default_rng(seed)
    bites = False
    info = {}
    if MODE == "0a":
        o = summarise(pipe, 4.0 * draw_rows(rng, N, mrows), svals)
        v = o["P2"]["1.00"]["rival"]
        bites = v < 0.32
        P(f"MUTATE 0a: mu x 4; P(lean rival, s=1) = {v:.3f} (bites if < 0.32; README 0.01)")
    elif MODE == "0b":
        o = summarise(pipe, 0.25 * draw_rows(rng, N, mrows), svals)
        v = o["P2"]["1.00"]["flat"]
        bites = v < 0.05
        P(f"MUTATE 0b: mu x 0.25; P(lean flat, s=1) = {v:.3f} (bites if < 0.05; README 0.00)")
    elif MODE == "1":
        s1 = win(C, 2.0, 2.5, 9.5, 11.5)
        P(f"  window z[2.0,2.5], logM[9.5,11.5]: {len(s1)} rows, mu median {np.median(C.mu[s1]):.3f}")
        o = summarise(pipe, draw_rows(rng, N, C.mu[s1]), svals)
        cc = o["P2"]["1.00"]
        tv = 0.5 * sum(abs(cc[k] - pc[k]) for k in ("flat", "rival", "both", "neither"))
        bites = tv >= 0.15
        info = dict(n_rows=len(s1), median_mu_row=float(np.median(C.mu[s1])), classes=cc, tv=tv)
        P(f"MUTATE 1: classes flat {cc['flat']:.3f} rival {cc['rival']:.3f} both {cc['both']:.3f} neither {cc['neither']:.3f}; mu-bar median {o['median']:.3f}; TV vs primary {tv:.3f} (bites if >= 0.15)")
    elif MODE == "2":
        o = summarise(pipe, 2.0 * draw_rows(rng, N, mrows), svals)
        cc = o["P2"]["1.00"]
        bites = cc["rival"] < 0.25 and cc["flat"] > 0.45
        P(f"MUTATE 2: h=1; rival {cc['rival']:.3f} flat {cc['flat']:.3f} (bites if rival<0.25 and flat>0.45; README 0.11/0.59)")
    elif MODE == "3":
        o = summarise(pipe, draw_M(rng, N, fit, S.logM, slope=+0.22), svals)
        cc = o["P2"]["1.00"]
        bites = cc["rival"] > pc["rival"] + 0.08
        P(f"MUTATE 3: slope +0.22; rival {cc['rival']:.3f} flat {cc['flat']:.3f} both {cc['both']:.3f}; primary rival {pc['rival']:.3f} (bites if rival > primary+0.08); median mu-bar {o['median']:.3f}")
        o2 = summarise(pipe, draw_M(np.random.default_rng(seed), N, fit, S.logM), svals)
        P(f"          (true Variant M at same N: rival {o2['P2']['1.00']['rival']:.3f} flat {o2['P2']['1.00']['flat']:.3f})")
        info = dict(variantM_true=o2["P2"]["1.00"])
    elif MODE == "4":
        z17 = C.z < 1.7
        lm, mu = C.lm[z17], C.mu[z17]
        prng = np.random.default_rng(166)
        Ps, bs = [], []
        for i in range(200):
            perm = prng.permutation(len(mu))
            f = ols(lm - 10.5, np.log10(mu[perm]))
            bs.append(f["b"])
            o = summarise(pipe, draw_M(np.random.default_rng(1000 + i), 2000, f, S.logM), svals)
            Ps.append(o["P2"]["1.00"]["rival"])
        med = float(np.median(Ps))
        pval = float(np.mean(np.abs(bs) >= abs(fit["b"])))
        bites = med >= pc["rival"] - 0.06
        P(f"MUTATE 4: 200 permutations; median P(lean rival, s=1) {med:.3f} (16-84: {np.percentile(Ps,16):.3f}-{np.percentile(Ps,84):.3f}); primary {pc['rival']:.3f}; "
          f"bites if median >= primary-0.06; permutation p(|b|>={abs(fit['b']):.3f}) = {pval:.3f}; median |b_perm| {np.median(np.abs(bs)):.3f}")
        info = dict(median_rival=med, p16=float(np.percentile(Ps, 16)), p84=float(np.percentile(Ps, 84)), perm_p=pval, med_abs_b=float(np.median(np.abs(bs))))
    elif MODE == "5":
        o = summarise(pipe, draw_rows(rng, N, mrows), svals, swap=True)
        v = o["P2"]["1.00"]["rival"]
        bites = v < 0.05
        P(f"MUTATE 5: labels swapped; P(lean rival, s=1) = {v:.3f} (bites if < 0.05); classes {o['P2']['1.00']}")
    elif MODE == "6":
        o = summarise(pipe, draw_rows(rng, N, mrows, sys=False), svals)
        cc = o["P2"]["1.00"]
        mx = max(cc["flat"], cc["rival"], cc["both"])
        P(f"MUTATE 6 (negative control, informational): systematics off; width {o['width_dex']:.3f} dex (<=0.20 expected); classes flat {cc['flat']:.3f} rival {cc['rival']:.3f} both {cc['both']:.3f} neither {cc['neither']:.3f}; label {'DIAGNOSTIC' if mx>=0.68 else 'NON-DIAGNOSTIC'}")
        info = dict(width=o["width_dex"], classes=cc, width_ok=o["width_dex"] <= 0.20)
        bites = False
    else:
        raise SystemExit("unknown MUTATE")
    P(f"\nMUTATE={MODE}: {'CONTROL BITES (exit 1)' if bites else 'CONTROL DID NOT BITE (exit 0)'}")
    outj["bites"] = bool(bites)
    outj["info"] = info
    outj["primary_ref"] = pc
    outj["elapsed_s"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, f"CFG166_MUTATE_{MODE}_results.json"), "w") as f:
        json.dump(outj, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    return 1 if bites else 0


if __name__ == "__main__":
    sys.exit(main())
