#!/usr/bin/env python3
"""W4-13 -- is p64's within-galaxy gas/star gap a law-shape effect?
Declared laws: L_n (g^2 - g_N^n g^(2-n) = a0 g_N) for n = 0.5, 1 (simple), 1.5, 2 (AG4's quadratic), and RAR (exponential).
Criteria: FROZEN_CRITERIA.md (committed alone, 117727995). p64's sample/classes/statistic copied (K1 reproduces -0.408 / -0.406).
Light: numpy, one process. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_13_gap_vs_law_shape/w4_13.py > why_4_puzzle/W4_13_gap_vs_law_shape/w4_13.out
    W4_13_MUTATE=1 ... > .../w4_13_MUTATE.out    (planted n = 0.5 world; exit 1 when the control bites)
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, io, json, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("W4_13_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
KPC = 3.0857e19
G_SI, C_SI = 6.67430e-11, 2.99792458e8
S_RHO = C_SI * math.sqrt(G_SI * 0.685 * 8.533238720309458e-27)    # c sqrt(G rho_L), GF1 registers (converts a0 -> kappa only)
LAWS = ["n=0.5", "n=1 (simple)", "n=1.5", "n=2 (AG4 quadratic)", "RAR (exponential)"]
NVAL = {"n=0.5": 0.5, "n=1 (simple)": 1.0, "n=1.5": 1.5, "n=2 (AG4 quadratic)": 2.0}
OUT, checks = [], []


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": detail, "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def a0_inv(law, go, gb):
    if law.startswith("RAR"):
        return gb / np.log(1 - gb / go) ** 2
    n = NVAL[law]
    return (go ** 2 - gb ** n * go ** (2 - n)) / gb


def forward(law, gN, a0):
    if law.startswith("RAR"):
        return gN / (-np.expm1(-np.sqrt(gN / a0)))
    n = NVAL[law]
    lo = gN.copy(); hi = gN + 2 * np.sqrt(a0 * gN) + 2 * a0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        h = mid ** 2 - gN ** n * mid ** (2 - n) - a0 * gN
        lo = np.where(h < 0, mid, lo); hi = np.where(h < 0, hi, mid)
    return 0.5 * (lo + hi)


def accel(g):
    R = g["R"] * KPC
    gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
    go = (g["Vobs"] * 1e3) ** 2 / R
    return go, gb


def classes(g):                                                # p64's, copied
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vs2 = 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    vb2 = vg2 + vs2
    ok = (vb2 > 0) & (g["Vobs"] > 0) & (g["R"] > 0)
    return ok & (vg2 >= 0.7 * vb2), ok & (vs2 >= 0.7 * vb2)


def la_pts(g, mask, law="n=1 (simple)"):
    go, gb = accel(g)
    m = mask & (gb > 0) & (go > gb)
    return np.log10(a0_inv(law, go[m], gb[m]))


GAL = [g for g in C.load_sparc() if g["meta"]]
if MUT:                                                        # M1: planted n = 0.5 world at a0 = 1/2 c sqrt(G rho_L)
    for g in GAL:
        go, gb = accel(g)
        m = gb > 0
        gm = np.where(m, forward("n=0.5", np.where(m, gb, 1e-14), 0.5 * S_RHO), go)
        g["Vobs"] = np.where(m, np.sqrt(gm * g["R"] * KPC) / 1e3, g["Vobs"])
P("W4-13  is the within-galaxy gas/star gap a law-shape effect?" + ("  [MUTATE: planted n = 0.5 world at kappa = 1/2]" if MUT else ""))
P("obs lane. kappa = 1/2 FITTED. Not theory closed.\n")

A_S = []
for g in GAL:
    if g["meta"]["Q"] > 2 or g["meta"]["Inc"] < 30:
        continue
    gm, sm = classes(g)
    if len(la_pts(g, gm)) >= 3 and len(la_pts(g, sm)) >= 3:
        A_S.append((g, gm, sm))

res = {}
P(f"Delta_g per law (p64 sample {len(A_S)} galaxies, fiducial Upsilon_d 0.5, f_gas 1; bootstrap 2000 seed 64)")
for law in LAWS:
    dg = []
    for g, gm, sm in A_S:
        a, b = la_pts(g, gm, law), la_pts(g, sm, law)
        if len(a) >= 2 and len(b) >= 2:
            dg.append(float(np.median(a) - np.median(b)))
    dg = np.array(dg)
    rng = np.random.default_rng(64)
    bs = [np.median(dg[rng.integers(0, len(dg), len(dg))]) for _ in range(2000)]
    res[law] = dict(delta=float(np.median(dg)), sd=float(np.std(bs)), n=len(dg))
    P(f"  {law:22s} Delta_g {res[law]['delta']:+.3f} +- {res[law]['sd']:.3f}  (n {len(dg)})  -> {'closes (|z| < 2)' if abs(res[law]['delta']) < 2 * res[law]['sd'] else 'gap'}")
if not MUT:
    check("K1 reproduce p64 (n=1 -0.408, RAR -0.406)", f"{res['n=1 (simple)']['delta']:+.4f}, {res['RAR (exponential)']['delta']:+.4f}",
          abs(res["n=1 (simple)"]["delta"] + 0.408) < 2e-3 and abs(res["RAR (exponential)"]["delta"] + 0.406) < 2e-3)

# SPARC RAR fit per law (one free a0)
pts = []
for g in GAL:
    if g["meta"]["Q"] > 2 or g["meta"]["Inc"] < 30:
        continue
    go, gb = accel(g)
    m = (go > 0) & (gb > 0) & (g["Vobs"] > 0)
    sig = 2 * np.clip(g["eV"][m], 1, None) / (np.clip(g["Vobs"][m], 1, None) * math.log(10))
    pts.append((gb[m], go[m], sig))
gN = np.concatenate([p[0] for p in pts]); gO = np.concatenate([p[1] for p in pts]); sg = np.concatenate([p[2] for p in pts])
P(f"\nSPARC RAR fit per law ({len(gN)} points, Q <= 2, i >= 30; Upsilon_d 0.5 / Upsilon_b 0.7; one free a0)")
for law in LAWS:
    f = lambda la: float(np.sum(((np.log10(gO) - np.log10(forward(law, gN, 10 ** la))) / sg) ** 2))
    grid = np.linspace(-10.8, -9.0, 181)
    v = [f(x) for x in grid]
    i = int(np.argmin(v))
    r = minimize_scalar(f, bounds=(grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]), method="bounded", options={"xatol": 1e-5})
    res[law].update(log_a0=float(r.x), chi2=float(r.fun), kappa_L=float(10 ** r.x / S_RHO))
best = min(res[l]["chi2"] for l in LAWS)
for law in LAWS:
    res[law]["dchi2"] = res[law]["chi2"] - best
    P(f"  {law:22s} chi2 {res[law]['chi2']:9.1f}  dchi2 {res[law]['dchi2']:+8.1f}  best a0 {10 ** res[law]['log_a0']:.3e} (kappa_L {res[law]['kappa_L']:.3f})")
closing = [l for l in LAWS if abs(res[l]["delta"]) < 2 * res[l]["sd"]]
allowed = [l for l in closing if res[l]["dchi2"] <= 9]
trend = np.sign(res["n=2 (AG4 quadratic)"]["delta"] - res["n=0.5"]["delta"])
lane = "GAP IS LAW-SHAPE" if allowed else "GAP NOT LAW-SHAPE"
P(f"\nlaws closing the gap: {closing or 'none'}; of those, RAR-allowed (dchi2 <= 9): {allowed or 'none'}")
P(f"trend of Delta_g with n: {'more negative as n rises (sharper transitions widen the gap)' if trend < 0 else 'less negative as n rises'}")
P(f"LANE VERDICT: {lane}")
json.dump(dict(mutate=MUT, laws=res, closing=closing, allowed=allowed, lane_verdict=lane, checks=checks),
          open(os.path.join(HERE, f"w4_13_results{SUF}.json"), "w"), indent=1, default=float)
if MUT:
    ok05 = abs(res["n=0.5"]["delta"]) <= 2 * res["n=0.5"]["sd"] + 1e-9    # first MUTATE run used '<' and failed on a noiseless plant (sd = 0)
    gap1 = abs(res["n=1 (simple)"]["delta"]) > 2 * res["n=1 (simple)"]["sd"]
    P(f"MUTATE: planted n = 0.5 world -> n = 0.5 closes {ok05}; n = 1 shows a gap {gap1}")
    sys.exit(1 if (ok05 and gap1) else 2)
P(f"\nchecks: {sum(c['pass'] for c in checks)}/{len(checks)} pass")
sys.exit(0 if all(c["pass"] for c in checks) else 1)
