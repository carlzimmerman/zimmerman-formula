#!/usr/bin/env python3
"""W4-16 -- what drives the outward a0 decline inside SPARC galaxies? Declared signatures D1-D6 (FROZEN_CRITERIA.md, e8e80f10f).
Light: numpy/scipy, one process. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_16_what_drives_the_decline/w4_16.py > .../w4_16.out
    W4_16_MUTATE=1 ... > .../w4_16_MUTATE.out   (M1 planted pressure support; M2 planted radial M/L; exit 1 when both bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, io, json, math, os, sys
import numpy as np
from scipy.stats import rankdata, mannwhitneyu

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("W4_16_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
KPC = 3.0857e19
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


def slope(g, U=0.5, gas_only=False, vobs=None, star_mult=None, nmin=8):
    R = g["R"] * KPC
    V = g["Vobs"] if vobs is None else vobs
    vs2 = U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
    if star_mult is not None:
        vs2 = vs2 * star_mult
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    gb = (vg2 + vs2) * 1e6 / R
    go = (V * 1e3) ** 2 / R
    m = (gb > 0) & (go > gb) & (V > 0)
    if gas_only:
        vb2_f = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2       # classification at the fiducial, as p64
        m &= vg2 >= 0.7 * vb2_f
    if m.sum() < nmin:
        return None
    gb, go = gb[m], go[m]
    a0 = go * (go - gb) / gb
    lev = 1 + go / (go - gb)
    sl = 2 * np.clip(g["eV"][m], 1, None) / (np.clip(V[m], 1, None) * math.log(10))
    w = 1 / (lev * sl) ** 2
    x, y = np.log10(gb), np.log10(a0)
    xm, ym = np.sum(w * x) / w.sum(), np.sum(w * y) / w.sum()
    return float(np.sum(w * (x - xm) * (y - ym)) / np.sum(w * (x - xm) ** 2))


def perm_rho(a, b, n=10000, seed=64):
    ra, rb = rankdata(a), rankdata(b)
    r0 = float(np.corrcoef(ra, rb)[0, 1])
    rng = np.random.default_rng(seed)
    cnt = sum(abs(np.corrcoef(ra, rng.permutation(rb))[0, 1]) >= abs(r0) - 1e-12 for _ in range(n))
    return r0, (cnt + 1) / (n + 1)


def med_boot(v, seed=64, n=2000):
    v = np.asarray(v); rng = np.random.default_rng(seed)
    return float(np.median(v)), float(np.std([np.median(rng.choice(v, len(v))) for _ in range(n)]))


GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Inc"] >= 30]


def run(label, vobs_fn=None, star_fn=None):
    rows = []
    for g in GAL:
        vo = vobs_fn(g) if vobs_fn else None
        sm = star_fn(g) if star_fn else None
        s = slope(g, vobs=vo, star_mult=sm)
        if s is None:
            continue
        sg = slope(g, gas_only=True, vobs=vo, star_mult=sm, nmin=5)
        m = g["meta"]
        rows.append(dict(name=g["name"], s=s, s_gas=sg, Vflat=m["Vflat"], D=m["D"], Inc=m["Inc"], Q=m["Q"]))
    s = np.array([r["s"] for r in rows])
    P(f"\n[{label}] {len(rows)} galaxies; median s {np.median(s):+.3f}")
    out = {"n": len(rows)}
    okV = np.array([r["Vflat"] > 0 for r in rows])
    out["D1"] = perm_rho(s[okV], np.log10([r["Vflat"] for r in rows if r["Vflat"] > 0]))
    out["D3"] = perm_rho(s, np.log10([r["D"] for r in rows]))
    out["D4"] = perm_rho(s, np.array([r["Inc"] for r in rows]))
    q1 = s[np.array([r["Q"] == 1 for r in rows])]; q2 = s[np.array([r["Q"] == 2 for r in rows])]
    out["D5"] = (float(np.median(q1) - np.median(q2)), float(mannwhitneyu(q1, q2).pvalue))
    sg = [r["s_gas"] for r in rows if r["s_gas"] is not None]
    out["D2"] = dict(s=med_boot(s), s_gas=med_boot(sg), n_gas=len(sg))
    P(f"  D1 pressure support: rho(s, log V_flat) = {out['D1'][0]:+.3f}, p {out['D1'][1]:.4f}  (signature: rho < 0)")
    P(f"  D2 radial M/L: median s {out['D2']['s'][0]:+.3f} +- {out['D2']['s'][1]:.3f}; median s_gas {out['D2']['s_gas'][0]:+.3f} +- "
      f"{out['D2']['s_gas'][1]:.3f} ({out['D2']['n_gas']} galaxies with >= 5 gas points)  (signature: s_gas ~ 0 while s > 0)")
    P(f"  D3 beam smearing: rho(s, log D) = {out['D3'][0]:+.3f}, p {out['D3'][1]:.4f}  (signature: rho != 0; smearing predicts rho < 0)")
    P(f"  D4 warps/inclination: rho(s, i) = {out['D4'][0]:+.3f}, p {out['D4'][1]:.4f}")
    P(f"  D5 quality: median s(Q1) - s(Q2) = {out['D5'][0]:+.3f}, Mann-Whitney p {out['D5'][1]:.4f}")
    met = []
    if out["D1"][0] < 0 and out["D1"][1] < 0.01: met.append("D1")
    sgv, sgs = out["D2"]["s_gas"]; sv, ss = out["D2"]["s"]
    if sv > 2 * ss and abs(sgv) < 2 * sgs: met.append("D2")
    if out["D3"][1] < 0.01: met.append("D3")
    if out["D4"][1] < 0.01: met.append("D4")
    if out["D5"][1] < 0.01: met.append("D5")
    if len(met) == 1:
        verdict = f"ATTRIBUTED to {met[0]}"
    elif len(met) > 1:
        verdict = "MIXED (" + ", ".join(met) + ")"
    elif sv > 0 and sgv > 0 and abs(sv - sgv) < 2 * math.hypot(ss, sgs):
        verdict = "D6 (UNIVERSAL SLOPE) LIKELY"
    else:
        verdict = "UNRESOLVED"
    out["met"], out["verdict"] = met, verdict
    if verdict.startswith("D6"):
        beta = (1 + sv) / 2
        P(f"  D6: beta = (1 + s)/2 = {beta:.3f}; a global beta this far from 1/2 would tilt the BTFR slope, which the record bounds"
          f" at b = 1.004 +- 0.011 -> an RC-internal effect, not a global law change")
        out["beta"] = beta
    P(f"  verdict: {verdict}")
    return out, rows


res = {}
if not MUT:
    res["data"], rows = run("data")
    for U in (0.3, 0.5, 0.8):
        ss = [slope(g, U=U) for g in GAL]
        ss = [x for x in ss if x is not None]
        P(f"  Upsilon robustness: Upsilon_d {U}: median s {np.median(ss):+.3f} ({len(ss)} galaxies)")
        res[f"U{U}"] = float(np.median(ss))
    lane = res["data"]["verdict"]
    P(f"\nLANE VERDICT: {lane}")
else:
    def press(g):                                          # M1: V'^2 = V^2 - 2 sigma^2 beyond R_disk, sigma = 10 km/s
        V = g["Vobs"].copy(); Rd = g["meta"]["Rdisk"]
        out = g["R"] > Rd
        V[out] = np.sqrt(np.clip(V[out] ** 2 - 2 * 10.0 ** 2, 1.0, None))
        return V
    def mlgrad(g):                                          # M2: inner stellar terms x (1 + (R_disk/R)^0.5)
        return 1 + np.sqrt(g["meta"]["Rdisk"] / np.clip(g["R"], 1e-3, None))
    res["M1"], _ = run("M1 planted pressure support", vobs_fn=press)
    res["M2"], _ = run("M2 planted radial M/L gradient", star_fn=mlgrad)
    lane = None
json.dump(dict(mutate=MUT, results=res, lane_verdict=lane), open(os.path.join(HERE, f"w4_16_results{SUF}.json"), "w"), indent=1, default=float)
if MUT:
    try:
        base = json.load(open(os.path.join(HERE, "w4_16_results.json")))["results"]["data"]
        m1 = res["M1"]["D1"][0] < 0 and res["M1"]["D1"][1] < 0.01
        ds = abs(res["M2"]["D2"]["s"][0] - base["D2"]["s"][0]) > base["D2"]["s"][1]
        dsg = abs(res["M2"]["D2"]["s_gas"][0] - base["D2"]["s_gas"][0]) <= base["D2"]["s_gas"][1]
        P(f"\nMUTATE: M1 makes D1's signature appear {m1}; M2 moves median s {ds} while median s_gas stays within 1 sigma {dsg}")
        sys.exit(1 if (m1 and ds and dsg) else 2)
    except OSError:
        sys.exit(2)
sys.exit(0)
