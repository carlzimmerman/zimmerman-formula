#!/usr/bin/env python3
"""W4-14 -- gas versus star points at the SAME g_bar, pooled across SPARC: is the within-galaxy gap about baryons or acceleration?
Criteria: FROZEN_CRITERIA.md (committed alone, 9ffc65ac7). Point classes and the simple-mu inversion as p64 (fiducial Upsilon_d 0.5).
Light: numpy, one process. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_14_gas_star_matched_acceleration/w4_14.py > .../w4_14.out
    W4_14_MUTATE=1 ... > .../w4_14_MUTATE.out   (M1 label shuffle; M2 planted acceleration-only world; exit 1 when both bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, io, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("W4_14_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
KPC = 3.0857e19
S_RHO = 2.99792458e8 * math.sqrt(6.67430e-11 * 0.685 * 8.533238720309458e-27)
EDGES = np.round(np.arange(-12.0, -9.4999, 0.25), 3)
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


def accel(g):
    R = g["R"] * KPC
    gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
    go = (g["Vobs"] * 1e3) ** 2 / R
    return go, gb


def classes(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vs2 = 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    vb2 = vg2 + vs2
    ok = (vb2 > 0) & (g["Vobs"] > 0) & (g["R"] > 0)
    return ok & (vg2 >= 0.7 * vb2), ok & (vs2 >= 0.7 * vb2)


def a0_simple(go, gb):
    return go * (go - gb) / gb


def a0_rar(go, gb):
    return gb / np.log(1 - gb / go) ** 2


def build(gals, inv=a0_simple):
    """per galaxy: arrays of (log g_bar, log a0, class) for valid points"""
    rows = []
    for gi, g in enumerate(gals):
        go, gb = accel(g)
        gm, sm = classes(g)
        v = (gb > 0) & (go > gb)
        for cls, m in (("gas", gm & v), ("star", sm & v)):
            if m.sum():
                rows.append((gi, cls, np.log10(gb[m]), np.log10(inv(go[m], gb[m]))))
    return rows


def bin_table(rows, gal_weights=None):
    """table[bin][class] = {galaxy: median log a0 of its points in the bin}"""
    tab = [{"gas": {}, "star": {}} for _ in range(len(EDGES) - 1)]
    for gi, cls, lgb, la in rows:
        idx = np.digitize(lgb, EDGES) - 1
        for b in range(len(EDGES) - 1):
            sel = idx == b
            if sel.any():
                tab[b][cls][gi] = float(np.median(la[sel]))
    return tab


def delta_bins(tab, resample=None):
    out = []
    for b, t in enumerate(tab):
        if resample is None:
            gs, ss = list(t["gas"].values()), list(t["star"].values())
        else:
            gs = [t["gas"][g] for g in resample if g in t["gas"]]
            ss = [t["star"][g] for g in resample if g in t["star"]]
        out.append(float(np.median(gs) - np.median(ss)) if len(gs) and len(ss) else np.nan)
    return np.array(out)


def analyse(gals, label, shuffle=False):
    rows = build(gals)
    tab = bin_table(rows)
    usable = [b for b, t in enumerate(tab) if len(t["gas"]) >= 3 and len(t["star"]) >= 3]
    if shuffle:
        rng = np.random.default_rng(64)
        for b in usable:
            items = list(tab[b]["gas"].items()) + [(k + 10 ** 6, v) for k, v in tab[b]["star"].items()]
            ng = len(tab[b]["gas"])
            perm = rng.permutation(len(items))
            tab[b]["gas"] = {items[i][0]: items[i][1] for i in perm[:ng]}
            tab[b]["star"] = {items[i][0]: items[i][1] for i in perm[ng:]}
    d0 = delta_bins(tab)
    gal_ids = sorted({r[0] for r in rows} | {k for b in usable for c in ("gas", "star") for k in tab[b][c]})
    rng = np.random.default_rng(64)
    boots = np.array([delta_bins(tab, rng.choice(gal_ids, len(gal_ids))) for _ in range(2000)])
    sig_b = np.nanstd(boots, axis=0)
    w = np.array([1 / sig_b[b] ** 2 if (b in usable and sig_b[b] > 0) else 0.0 for b in range(len(d0))])
    dm = float(np.nansum(w * np.nan_to_num(d0)) / w.sum()) if w.sum() > 0 else float("nan")
    bm = [float(np.nansum(w * np.nan_to_num(bb)) / np.sum(w * np.isfinite(bb))) for bb in boots if np.sum(w * np.isfinite(bb)) > 0]
    sm = float(np.std(bm)) if bm else float("nan")
    P(f"\n[{label}] usable bins (>= 3 galaxies per class): {len(usable)}")
    for b in usable:
        P(f"  log g_bar [{EDGES[b]:+.2f}, {EDGES[b + 1]:+.2f}): n_gas {len(tab[b]['gas']):3d}  n_star {len(tab[b]['star']):3d}  "
          f"Delta_bin {d0[b]:+.3f} +- {sig_b[b]:.3f}")
    P(f"  Delta_match = {dm:+.3f} +- {sm:.3f} dex (z {dm / sm if sm > 0 else float('nan'):+.2f})")
    # within-galaxy gap on the same galaxies and acceleration range
    lo = EDGES[min(usable)] if usable else None
    hi = EDGES[max(usable) + 1] if usable else None
    wg = []
    if usable:
        by_gal = {}
        for gi, cls, lgb, la in rows:
            sel = (lgb >= lo) & (lgb < hi)
            by_gal.setdefault(gi, {})[cls] = la[sel]
        for gi, d in by_gal.items():
            if len(d.get("gas", [])) >= 2 and len(d.get("star", [])) >= 2:
                wg.append(float(np.median(d["gas"]) - np.median(d["star"])))
    wg = np.array(wg)
    rngw = np.random.default_rng(64)
    wsd = float(np.std([np.median(wg[rngw.integers(0, len(wg), len(wg))]) for _ in range(2000)])) if len(wg) else float("nan")
    wmed = float(np.median(wg)) if len(wg) else float("nan")
    P(f"  within-galaxy gap restricted to the same range ({len(wg)} galaxies with >= 2 points of each class): {wmed:+.3f} +- {wsd:.3f} dex")
    if len(usable) < 3:
        verdict = "NOT DIAGNOSTIC"
    elif dm < 0 and abs(dm) > 3 * sm:
        verdict = "BARYON-TYPE"
    elif abs(dm) < 2 * sm:
        verdict = "ACCELERATION"
    else:
        verdict = "INTERMEDIATE"
    P(f"  verdict: {verdict}")
    return dict(usable=len(usable), delta_match=dm, sigma=sm, within=wmed, within_sd=wsd, n_within=len(wg), verdict=verdict,
                bins={f"{EDGES[b]:+.2f}": dict(dg=float(d0[b]), sd=float(sig_b[b]), n_gas=len(tab[b]["gas"]), n_star=len(tab[b]["star"])) for b in usable})


GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Inc"] >= 30]
P("W4-14  gas vs star points at matched g_bar (SPARC Q <= 2, i >= 30; simple mu; galaxy-level bin medians; bootstrap 2000 seed 64)"
  + ("  [MUTATE]" if MUT else ""))
P("obs lane. kappa = 1/2 FITTED. Not theory closed.")
res = {}
if not MUT:
    res["data"] = analyse(GAL, "data, simple mu")
    rows_r = build(GAL, a0_rar)
    tab_r = bin_table(rows_r)
    us_r = [b for b, t in enumerate(tab_r) if len(t["gas"]) >= 3 and len(t["star"]) >= 3]
    dr = delta_bins(tab_r)
    P(f"\n[RAR cross-check] usable bins {len(us_r)}; Delta_bin: " + ", ".join(f"{EDGES[b]:+.2f}: {dr[b]:+.3f}" for b in us_r))
    res["rar_bins"] = {f"{EDGES[b]:+.2f}": float(dr[b]) for b in us_r}
    lane = res["data"]["verdict"]
else:
    res["M1_shuffle"] = analyse(GAL, "M1: labels shuffled within bins", shuffle=True)
    planted = []
    for g in GAL:
        h = dict(g)
        go, gb = accel(g)
        m = gb > 0
        a0g = 0.5 * S_RHO * (np.where(m, gb, 1e-11) / 1e-11) ** 0.25
        gp = np.where(m, gb * 0.5 * (1 + np.sqrt(1 + 4 * a0g / np.where(m, gb, 1.0))), go)
        h["Vobs"] = np.where(m, np.sqrt(gp * g["R"] * KPC) / 1e3, g["Vobs"])
        planted.append(h)
    res["M2_planted"] = analyse(planted, "M2: planted acceleration-only a0(g_bar) world")
    lane = None
json.dump(dict(mutate=MUT, results=res, lane_verdict=lane), open(os.path.join(HERE, f"w4_14_results{SUF}.json"), "w"), indent=1, default=float)
if MUT:
    try:
        base = json.load(open(os.path.join(HERE, "w4_14_results.json")))["results"]["data"]
        m1 = abs(res["M1_shuffle"]["delta_match"]) < 2 * base["sigma"]
        m2 = abs(res["M2_planted"]["within"]) > 2 * res["M2_planted"]["within_sd"] and \
            abs(res["M2_planted"]["delta_match"]) < 2 * max(res["M2_planted"]["sigma"], 1e-9)
        P(f"\nMUTATE: M1 shuffle Delta_match within 2 sigma of 0 {m1}; M2 planted world: within-galaxy gap appears and matched "
          f"Delta stays near 0 {m2}")
        sys.exit(1 if (m1 and m2) else 2)
    except OSError:
        sys.exit(2)
P(f"\nLANE VERDICT: {lane}")
sys.exit(0)
