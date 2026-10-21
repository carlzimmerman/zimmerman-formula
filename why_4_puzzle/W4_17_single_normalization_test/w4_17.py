#!/usr/bin/env python3
"""W4-17 -- is the within-galaxy a0 residual a single stellar-M/L normalisation error?
Criteria: FROZEN_CRITERIA.md (b0e8bee92, with the synthetic pre-freeze calibration). Statistics as the calibration code.
Light: numpy, one process. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_17_single_normalization_test/w4_17.py > .../w4_17.out
    W4_17_MUTATE=1 ... > .../w4_17_MUTATE.out   (worlds A and B through the same pipeline; exit 1 when both behave)
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, io, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("W4_17_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
KPC = 3.0857e19
A0 = 0.5 * 2.99792458e8 * math.sqrt(6.67430e-11 * 0.685 * 8.533238720309458e-27)
UG = np.round(np.arange(0.3, 1.401, 0.1), 2)
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Inc"] >= 30]


def world(grad):
    out = []
    for g in GAL:
        h = dict(g); R = g["R"] * KPC
        mult = (1 + np.sqrt(g["meta"]["Rdisk"] / np.clip(g["R"], 1e-3, None))) if grad else 1.0
        gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + mult * (0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2)) * 1e6 / R
        m = gb > 0
        gt = np.where(m, gb * 0.5 * (1 + np.sqrt(1 + 4 * A0 / np.where(m, gb, 1.0))), 1e-12)
        h["Vobs"] = np.where(m, np.sqrt(gt * R) / 1e3, g["Vobs"]); out.append(h)
    return out


def per_galaxy(g, U):
    R = g["R"] * KPC
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2; vs2f = 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    gb = (vg2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2) * 1e6 / R; go = (g["Vobs"] * 1e3) ** 2 / R
    v = (gb > 0) & (go > gb)
    if v.sum() < 8:
        return None
    la = np.full(len(gb), np.nan); la[v] = np.log10(go[v] * (go[v] - gb[v]) / gb[v])
    gm = (vg2 >= 0.7 * (vg2 + vs2f)) & v; sm = (vs2f >= 0.7 * (vg2 + vs2f)) & v
    dg = (np.nanmedian(la[gm]) - np.nanmedian(la[sm])) if (gm.sum() >= 3 and sm.sum() >= 3) else np.nan
    s = np.polyfit(np.log10(gb[v]), la[v], 1)[0]
    rv = g["R"][v]; med = np.median(rv)
    dr = np.median(la[v][rv > med]) - np.median(la[v][rv <= med])
    return dg, s, dr


def table(gals):
    """per galaxy x Upsilon grid x statistic"""
    T = np.full((len(gals), len(UG), 3), np.nan)
    for i, g in enumerate(gals):
        for j, U in enumerate(UG):
            r = per_galaxy(g, U)
            if r is not None:
                T[i, j] = r
    return T


def in_S11(gals):
    keep = []
    for i, g in enumerate(gals):
        r = per_galaxy(g, 0.5)
        keep.append(r is not None and np.isfinite(r[0]))
    return np.array(keep)


def zero(vals):
    for i in range(len(UG) - 1):
        a, b = vals[i], vals[i + 1]
        if np.isfinite(a) and np.isfinite(b) and a * b <= 0:
            return UG[i] + (UG[i + 1] - UG[i]) * (a / (a - b) if a != b else 0.0)
    return np.nan


def analyse(gals, label):
    T = table(gals)
    s11 = in_S11(gals)
    res = {}
    for sname, idx in (("S11", np.where(s11)[0]), ("S_all", np.where(np.isfinite(T[:, :, 1]).any(axis=1))[0])):
        stats = ["Delta_g", "s", "Delta_r"] if sname == "S11" else ["s", "Delta_r"]
        cols = {"Delta_g": 0, "s": 1, "Delta_r": 2}
        row = {}
        rng = np.random.default_rng(64)
        boots = [rng.choice(idx, len(idx)) for _ in range(500)]
        for st in stats:
            c = cols[st]
            med = [np.nanmedian(T[idx, j, c]) for j in range(len(UG))]
            z = zero(med)
            bz = [zero([np.nanmedian(T[b, j, c]) for j in range(len(UG))]) for b in boots]
            bz = np.array([x for x in bz if np.isfinite(x)])
            row[st] = dict(ustar=float(z), sd=float(np.std(bz)) if len(bz) > 5 else float("nan"), n_cross=int(len(bz)),
                           curve=[float(x) for x in med])
        res[sname] = dict(n=int(len(idx)), stats=row)
        P(f"[{label}] {sname} ({len(idx)} galaxies): " + "; ".join(
            f"{st} Upsilon* {row[st]['ustar']:.3f} +- {row[st]['sd']:.3f} ({row[st]['n_cross']}/500 cross)" for st in stats))
    r = res["S11"]["stats"]
    us = {k: (v["ustar"], v["sd"]) for k, v in r.items()}
    pairs = [("Delta_g", "s"), ("Delta_g", "Delta_r"), ("s", "Delta_r")]
    disagree = []
    for a, b in pairs:
        (ua, sa), (ub, sb) = us[a], us[b]
        if not (np.isfinite(ua) and np.isfinite(ub)):
            disagree.append(f"{a}/{b} (no crossing)")
        elif abs(ua - ub) > 2 * math.hypot(sa, sb):
            disagree.append(f"{a}/{b} ({ua:.2f} vs {ub:.2f})")
    high = [k for k in ("Delta_g", "Delta_r") if not np.isfinite(us[k][0]) or us[k][0] > 1.0]
    plaus = all(np.isfinite(u) and 0.4 <= u <= 1.0 for u, _ in us.values())
    if not disagree and plaus:
        verdict = "SINGLE NORMALISATION"
    elif disagree or high:
        verdict = "NOT A SINGLE NORMALISATION (gradient-like)"
    else:
        verdict = "UNDETERMINED"
    P(f"  [{label}] S11 disagreements: {disagree or 'none'}; Delta_g/Delta_r above 1.0 or not crossing: {high or 'none'} -> {verdict}")
    res["verdict"] = verdict
    return res


P("W4-17  single-normalisation test (Upsilon* where Delta_g, s, Delta_r vanish; grid 0.3-1.4; bootstrap 500 seed 64)"
  + ("  [MUTATE: planted worlds A and B]" if MUT else ""))
P("obs lane. kappa = 1/2 FITTED. Not theory closed.\n")
if not MUT:
    out = {"data": analyse(GAL, "data")}
    lane = out["data"]["verdict"]
    P(f"\nLANE VERDICT: {lane}")
else:
    out = {"A": analyse(world(False), "world A exact law"), "B": analyse(world(True), "world B planted radial M/L")}
    lane = None
json.dump(dict(mutate=MUT, results=out, lane_verdict=lane), open(os.path.join(HERE, f"w4_17_results{SUF}.json"), "w"), indent=1, default=float)
if MUT:
    okA = out["A"]["verdict"] == "SINGLE NORMALISATION" and abs(out["A"]["S11"]["stats"]["s"]["ustar"] - 0.5) < 0.05
    okB = out["B"]["verdict"].startswith("NOT A SINGLE")
    P(f"\nMUTATE: world A -> SINGLE NORMALISATION at 0.5 {okA}; world B -> NOT A SINGLE NORMALISATION {okB}")
    sys.exit(1 if (okA and okB) else 2)
sys.exit(0)
