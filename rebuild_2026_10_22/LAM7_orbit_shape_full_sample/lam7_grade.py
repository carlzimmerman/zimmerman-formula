"""LAM7 grade (criteria f10b6db28c): LAM6's statistic on the NEW sample; K1, K2, M1, C1, C2; rows.
Run: python3 -I lam7_grade.py [MUTATE]. Seconds, single thread. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"
KU2 = os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.py"); L4 = os.path.join(RB, "LAM4_whole_galaxy_absorption")
OUT = []; RES = {"lane": "LAM7", "mode": MODE}
def P(s=""): print(s, flush=True); OUT.append(s)
argv = sys.argv; sys.argv = ["ku2.py"]; src = open(KU2).read().split("ok1 = slow.sum()")[0]
K = {"__file__": KU2, "__name__": "ku2"}; exec(compile(src, "ku2.py", "exec"), K); sys.argv = argv
pos = {int(r): i for i, r in enumerate(np.flatnonzero(K["sel"]))}
def load(csvf, fitf):
    S = [l.strip().split(",") for l in open(csvf).readlines()[1:]]; F = {json.loads(l)["plateifu"]: json.loads(l) for l in open(fitf)}
    rows = [(int(s[2]), F.get(s[3])) for s in S]
    return rows, len(S)
def arrays(rows):
    ki, h4, sg, sn, drop, miss = [], [], [], [], 0, 0
    for r, f in rows:
        if f is None or f["status"] != "ok" or r not in pos: miss += 1; continue
        if f["sigma"] <= 0 or abs(f["h4"]) >= 0.3: drop += 1; continue
        ki.append(pos[r]); h4.append(f["h4"]); sg.append(f["sigma"]); sn.append(f["sn"])
    return np.array(ki), np.array(h4), np.array(sg), np.array(sn), drop, miss
new, nn = load(os.path.join(HERE, "lam7_sample.csv"), os.path.join(HERE, "lam7_fit.jsonl"))
old, _ = load(os.path.join(L4, "lam4_sample.csv"), os.path.join(L4, "lam4_fit.jsonl"))
ki, h4, sg, sn, drop, miss = arrays(new)
P(f"LAM7 mode {MODE}. NEW sample {nn}; usable {len(ki)}; dropped (sigma <= 0 or |h4| >= 0.3) {drop}; missing/error fits {miss}")
gas = {}
for l in open(os.path.join(RB, "LAM2_gas_poor_lambda_estimator", "lam2_sample.csv")).readlines()[1:]:
    a = l.strip().split(","); gas[int(a[0])] = int(a[5])
dprow = np.flatnonzero(K["sel"])
lr = np.log10(sg / K["sig"][ki]); k1 = abs(np.median(lr)) <= 0.03 and np.sqrt(np.mean(lr**2)) <= 0.06
P(f"K1 median log(sigma_int/Sigma_Re) {np.median(lr):+.4f}, rms {np.sqrt(np.mean(lr**2)):.4f}: {'PASS' if k1 else 'FAIL'}")
k2p = os.path.join(HERE, "lam7_k2.json"); K2 = json.load(open(k2p)) if os.path.exists(k2p) else None
P(f"K2: {'NOT RUN' if K2 is None else ('PASS' if K2['pass_'] else 'FAIL')}" + ("" if K2 is None else f" (rms {K2['rms']:.4f})"))
rng = np.random.default_rng(20261104)
def demean(v, grp):
    out = np.full(len(v), np.nan)
    for g in np.unique(grp):
        m = grp == g
        if m.sum() >= 3: out[m] = v[m] - v[m].mean()
    return out
def effect(r, h, grp, iqr):
    a, b = demean(r, grp), demean(h, grp); m = np.isfinite(a) & np.isfinite(b)
    return (float(np.sum(a[m] * b[m]) / np.sum(b[m] ** 2) * iqr) if m.sum() > 2 else float("nan")), int(m.sum())
def boot(r, h, grp, iqr, n=2000):
    bs = []
    for _ in range(n): i = rng.integers(0, len(r), len(r)); bs.append(effect(r[i], h[i], grp[i], iqr)[0])
    return tuple(float(x) for x in np.nanpercentile(bs, [2.5, 97.5]))
def resid_for(mt, rh, a0):
    go, gb = K["accel"](mt, rh, K["lm"]); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    return np.where(ok, K["resid"](np.where(ok, go, 1), np.where(ok, gb, 1), a0), np.nan)
ref = json.load(open(os.path.join(os.path.dirname(KU2), "ku2.json")))
for foot, a0 in K["A0"].items():
    rall = resid_for(K["mtm"], K["rhm"], a0); g = np.isfinite(rall); Dv, _ = K["Dstat"](rall[g], K["slow"][g], K["cell"][g]); c2 = abs(Dv - ref[foot]) <= 1e-6
    r = rall[ki]; grp = K["cell"][ki] * 2 + K["slow"][ki].astype(int); m = np.isfinite(r)
    r, h, gr, sl, snv, kk = r[m], h4[m].copy(), grp[m], K["slow"][ki][m], sn[m], ki[m]
    iqr = float(np.subtract(*np.percentile(h, [75, 25])))
    if MODE == "MUTATE":
        for gg in np.unique(gr): j = np.flatnonzero(gr == gg); h[j] = h[j][rng.permutation(len(j))]
    E, N = effect(r, h, gr, iqr); lo, hi = boot(r, h, gr, iqr); c1 = N >= 3000
    P(f"\n[{foot}] C2 KU2 D {Dv:+.6f} vs {ref[foot]:+.6f}: {'PASS' if c2 else 'FAIL'}; C1 N in groups {N} (>= 3000): {'PASS' if c1 else 'FAIL'}; IQR(h4) {iqr:.4f}")
    P(f"[{foot}] E = {E:+.4f} ln [95 % {lo:+.4f}, {hi:+.4f}]")
    R = dict(N=N, iqr=iqr, E=E, lo=lo, hi=hi, C1=bool(c1), C2=bool(c2), K1=bool(k1))
    if MODE == "MUTATE":
        R["M1_pass"] = bool(lo <= 0 <= hi); P(f"[{foot}] M1 interval includes 0: {'PASS' if R['M1_pass'] else 'FAIL'}")
    else:
        mp = os.path.join(HERE, "lam7_grade_MUTATE.json"); M1 = json.load(open(mp))[foot]["M1_pass"] if os.path.exists(mp) else None
        if not (c1 and c2 and k1) or M1 is False: lab = "NO VERDICT"
        elif K2 is not None and not K2["pass_"]: lab = "h4 NOT MEASURABLE"
        elif abs(E) >= 0.05 and (lo > 0 or hi < 0): lab = "TRACKS ORBIT SHAPE"
        elif lo > -0.05 and hi < 0.05: lab = "NO ORBIT DEPENDENCE"
        else: lab = "NO VERDICT"
        if K2 is None or M1 is None: lab += " (PROVISIONAL: " + ", ".join(x for x, v in (("K2", K2), ("M1", M1)) if v is None) + " not run)"
        P(f"[{foot}] LABEL: {lab}"); R["label"] = lab; rows = {}
        oki, oh4, *_ = arrays(old); ro = rall[oki]; go_ = K["cell"][oki] * 2 + K["slow"][oki].astype(int)
        rc, hc, gc = np.r_[r, ro], np.r_[h, oh4], np.r_[gr, go_]; mc = np.isfinite(rc)
        rows["combined"] = effect(rc[mc], hc[mc], gc[mc], iqr)[0]
        rows["within slow"] = effect(r[sl], h[sl], gr[sl], iqr)[0]; rows["within fast"] = effect(r[~sl], h[~sl], gr[~sl], iqr)[0]
        gf = np.array([gas.get(int(dprow[k]), -1) for k in kk])
        for nm, v in (("gas-poor (LAM2 flag)", 1), ("gas-bearing (LAM2 flag)", 0)): mm = gf == v; rows[nm + f" n={int(mm.sum())}"] = effect(r[mm], h[mm], gr[mm], iqr)[0]
        t = np.percentile(snv, [100 / 3, 200 / 3])
        for i, mm in enumerate((snv < t[0], (snv >= t[0]) & (snv < t[1]), snv >= t[1])): rows[f"S/N tercile {i}"] = effect(r[mm], h[mm], gr[mm], iqr)[0]
        r2 = resid_for(K["mt2"], K["rh2"], a0)[kk]; m2 = np.isfinite(r2); rows["second-best JAM model"] = effect(r2[m2], h[m2], gr[m2], iqr)[0]
        P(f"[{foot}] rows (ungraded): " + "; ".join(f"{k} {v:+.4f}" for k, v in rows.items())); R["rows"] = rows
    RES[foot] = R
sfx = "" if MODE == "REAL" else f"_{MODE}"
open(os.path.join(HERE, f"lam7_grade{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"lam7_grade{sfx}.json"), "w"), indent=1)
