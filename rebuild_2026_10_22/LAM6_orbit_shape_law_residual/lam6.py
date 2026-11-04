"""LAM6 (criteria 16e2226f95): does KU2's law residual at r_half track LAM4's integrated h4 at fixed cell and class?
Run: python3 -I lam6.py [MUTATE]. Seconds, single thread. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"
KU2 = os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.py"); L4 = os.path.join(RB, "LAM4_whole_galaxy_absorption")
L2 = os.path.join(RB, "LAM2_gas_poor_lambda_estimator"); OUT = []; RES = {"lane": "LAM6", "mode": MODE}
def P(s=""): print(s, flush=True); OUT.append(s)
# KU2's data block, exactly, up to its footing loop (nothing written)
argv = sys.argv; sys.argv = ["ku2.py"]; src = open(KU2).read().split("ok1 = slow.sum()")[0]
K = {"__file__": KU2, "__name__": "ku2"}; exec(compile(src, "ku2.py", "exec"), K); sys.argv = argv
dprow = np.flatnonzero(K["sel"]); pos = {int(r): i for i, r in enumerate(dprow)}
# LAM4 h4_int and LAM2 fibre h4, keyed by DynPop row
S = [l.strip().split(",") for l in open(os.path.join(L4, "lam4_sample.csv")).readlines()[1:]]
F = {json.loads(l)["plateifu"]: json.loads(l) for l in open(os.path.join(L4, "lam4_fit.jsonl"))}
sys.argv = ["lam2_grade.py"]; s2 = open(os.path.join(L2, "lam2_grade.py")).read().split("# ---- K1")[0]
G2 = {"__file__": os.path.join(L2, "lam2_grade.py"), "__name__": "lam2"}; exec(compile(s2, "lam2_grade.py", "exec"), G2); sys.argv = argv
ki, h4, h4f = [], [], []
for s in S:
    r = int(s[2])
    if r in pos and F[s[3]]["status"] == "ok": ki.append(pos[r]); h4.append(F[s[3]]["h4"]); h4f.append(G2["X"]["h4"][int(s[1])])
ki, h4, h4f = np.array(ki), np.array(h4), np.array(h4f, float)
P(f"LAM6 mode {MODE}. LAM4 galaxies {len(S)}, in KU2's sample {len(ki)}")
rng = np.random.default_rng(20261104)
def demean(v, grp):
    out = np.full(len(v), np.nan)
    for g in np.unique(grp):
        m = grp == g
        if m.sum() >= 3: out[m] = v[m] - v[m].mean()
    return out
def effect(r, h, grp, iqr):
    a, b = demean(r, grp), demean(h, grp); m = np.isfinite(a) & np.isfinite(b)
    return float(np.sum(a[m] * b[m]) / np.sum(b[m] ** 2) * iqr), int(m.sum())
for foot, a0 in K["A0"].items():
    go, gb = K["accel"](K["mtm"], K["rhm"], K["lm"]); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    rall = np.where(ok, K["resid"](np.where(ok, go, 1), np.where(ok, gb, 1), a0), np.nan); g = np.isfinite(rall)
    Dv, nc = K["Dstat"](rall[g], K["slow"][g], K["cell"][g]); ref = json.load(open(os.path.join(os.path.dirname(KU2), "ku2.json")))
    Dref = ref[foot]["D"] if foot in ref else ref.get("results", {}).get(foot, {}).get("D", float("nan")); c2 = abs(Dv - Dref) <= 1e-6
    P(f"[{foot}] C2 KU2 D reproduced: {Dv:+.6f} vs ku2.json {Dref:+.6f}: {'PASS' if c2 else 'FAIL'}")
    r = rall[ki]; grp = K["cell"][ki] * 2 + K["slow"][ki].astype(int); m = np.isfinite(r) & np.isfinite(h4)
    r, h, hf, grp, sl = r[m], h4[m], h4f[m], grp[m], K["slow"][ki][m]
    if MODE == "MUTATE":
        h = h.copy()
        for gg in np.unique(grp): j = np.flatnonzero(grp == gg); h[j] = h[j][rng.permutation(len(j))]
    iqr = float(np.subtract(*np.percentile(h4[m], [75, 25]))); E, N = effect(r, h, grp, iqr); c1 = N >= 800
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(r), len(r)); bs.append(effect(r[i], h[i], grp[i], iqr)[0])
    lo, hi = (float(x) for x in np.nanpercentile(bs, [2.5, 97.5]))
    P(f"[{foot}] C1 N in groups {N} (>= 800): {'PASS' if c1 else 'FAIL'}; IQR(h4_int) {iqr:.4f}")
    P(f"[{foot}] E = slope x IQR {E:+.4f} ln [95 % {lo:+.4f}, {hi:+.4f}]")
    R = dict(N=N, iqr=iqr, E=E, lo=lo, hi=hi, C1=bool(c1), C2=bool(c2))
    if MODE == "MUTATE":
        m1 = lo <= 0 <= hi; R["M1_pass"] = bool(m1); P(f"[{foot}] M1 interval includes 0: {'PASS' if m1 else 'FAIL'}")
    else:
        mp = os.path.join(HERE, "lam6_MUTATE.json"); M1 = json.load(open(mp))[foot]["M1_pass"] if os.path.exists(mp) else None
        if not (c1 and c2) or M1 is False: lab = "NO VERDICT"
        elif abs(E) >= 0.05 and (lo > 0 or hi < 0): lab = "TRACKS ORBIT SHAPE"
        elif lo > -0.05 and hi < 0.05: lab = "NO ORBIT DEPENDENCE"
        else: lab = "NO VERDICT"
        if M1 is None: lab += " (PROVISIONAL: M1 not run)"
        Ef = effect(r, hf, grp, float(np.subtract(*np.nanpercentile(hf, [75, 25]))))[0]
        Es = effect(r[sl], h[sl], grp[sl], iqr)[0]; Eq = effect(r[~sl], h[~sl], grp[~sl], iqr)[0]
        P(f"[{foot}] rows: fibre h4 E {Ef:+.4f}; within slow {Es:+.4f}, within fast {Eq:+.4f}")
        P(f"[{foot}] LABEL: {lab}"); R.update(label=lab, E_fibre=Ef, E_slow=Es, E_fast=Eq)
    RES[foot] = R
sfx = "" if MODE == "REAL" else f"_{MODE}"
open(os.path.join(HERE, f"lam6{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"lam6{sfx}.json"), "w"), indent=1)
