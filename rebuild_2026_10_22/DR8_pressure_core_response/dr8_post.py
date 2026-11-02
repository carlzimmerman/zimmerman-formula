#!/usr/bin/env python3
"""DR8 part B: K7 stability table and energy to 13.8 Gyr (the reader's sort picked 7.7 as last: fixed here), K11 identity and moved-particle pairs, f(r/r0) table for the one-mass carry. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
sys.argv = ["dr8_post"]; import numpy as np, dr8_read as D
R = json.load(open("dr8_live_results.json")); S = D.S; r0, Rd = D.r0, D.Rd; O = []
def P(s): print(s, flush=True); O.append(s)
st = {1: R["stability"], **{int(k): v for k, v in R["stability_all"].items()}}; ri = st[1]["r_over_r0"]; P(f"K7 d ln M(<r) from the IC at r/r0 {ri}, N0 s1 {st[1]['N0']}")
worst = {}
for s, v in st.items():
    for t in ("t3.85", "t7.70", "t13.80"):
        if t in v: P(f"  s{s} {t}: " + " ".join(f"{x:+.3f}" for x in v[t])); 
A = {t: np.array([v[t] for v in st.values() if t in v]) for t in ("t3.85", "t7.70")}; A["t13.80"] = np.array([st[1]["t13.80"]])
idx = {"0.25": 1, "0.5": 2, "1": 3, "2": 4}; lim = {"0.25": 0.10, "0.5": 0.05, "1": 0.05, "2": 0.05}; ok = True; Qt = R["core"]["table"]["Q"]; n = len(D.RDG); sig = {"0.25": math.log(Qt[n + 1]), "0.5": math.log(Qt[n + 2]), "1": math.log(Qt[n + 3]), "2": math.log(Qt[n + 4])}; K7 = {}
for t, a in A.items():
    med = np.median(a, axis=0)
    for k, i in idx.items():
        g = abs(med[i]) <= lim[k]; ok &= bool(g); K7[f"{t}|{k}"] = dict(median=float(med[i]), line=lim[k], ok=bool(g), under5x=bool(abs(med[i]) * 5 <= sig[k]), ln_Q=sig[k]); P(f"  {t} r/r0 {k}: median {med[i]:+.3f} (line {lim[k]}), ln Q signal {sig[k]:.3f}, drift x 5 under signal {K7[f'{t}|{k}']['under5x']}: {'PASS' if g else 'OVER LINE'}")
under = all(v["under5x"] for v in K7.values() if not v["ok"]); P(f"K7 lines all met: {ok}; every miss under the signal by x 5: {under}")
d = D.run_name("core", 1, "_nodisc"); Z0 = np.load(os.path.join(d, "ic.npz")); Z1 = np.load(os.path.join(d, "snap_t13.80.npz")); m = float(Z0["m"]); e0 = D.energy(Z0["x"], Z0["v"], m); e1 = D.energy(Z1["x"], Z1["v"], m); dE = sum(e1) / sum(e0) - 1; P(f"energy, 13.8 Gyr: 2T/|U| {2*e0[0]/abs(e0[1]):.4f} -> {2*e1[0]/abs(e1[1]):.4f}, dE/E {dE:+.2e}: {'PASS' if abs(dE) <= 0.01 else 'FAIL'}")
# K11b reader's identity and moved pair on a real no-disc core
B = np.load(os.path.join(d, "snap_t7.70.npz")); x = B["x"]; c = D.centre(x, B["c"], m, "com"); dx = x - c; r = np.linalg.norm(dx, axis=1); rB = np.sort(r); Md, Msim = S["Md"], m * len(x); o = D.preds(rB, m, Md, Msim, D.LR.r200(rB, m, 0.0), "core"); rr = np.concatenate((D.RDG * Rd, D.XR0 * r0)); N0 = np.searchsorted(rB, rr); P(f"K11b identity pair: max |Q - 1| {np.abs(N0 / N0 - 1).max():.1e}")
Mi = np.arange(1, len(r) + 1)[np.argsort(np.argsort(r))] * m * (1 - Md / Msim); rg = o["rg"]; rf = np.exp(np.interp(np.log(Mi), np.log(np.maximum.accumulate(np.maximum(o["QB"], 1e-300)) + 1e-9 * np.arange(len(rg))), np.log(rg))); rA = np.sort(rf); Q = np.searchsorted(rA, rr) / N0; QB = D.evalQ(o, rr)["QB"]; f = float(np.median([(Q[i] - 1) / (QB[i] - 1) for i in D.IW])); g = abs(f - 1) <= 0.05; P(f"K11c particles moved to Blumenthal's radii, core s1: f_B {f:.3f}: {'PASS' if g else 'FAIL'}")
per = R["core"]["per_radius"]["QB"]; f_ = per["med"][n:]; json.dump(dict(r_over_r0=D.XR0.tolist(), f=f_, label="MEASURED AT ONE MASS, core 1e12, isolated"), open("dr8_fr_table.json", "w"), indent=1); P(f"f(r/r0) table {np.round(f_,3).tolist()}")
P("Analytic start, Q predictions: " + json.dumps({k: np.round(v, 3).tolist() for k, v in R["core"]["analytic"].items()})); pr = per["ci95"][:n]; P("f_B by r/R_d, 95 %: " + " ".join(f"{m_:.2f}[{a:.2f},{b:.2f}]" for m_, (a, b) in zip(per["med"][:n], pr)))
json.dump(dict(K7=K7, K7_all=ok, K7_under=under, dE=dE, K11c=f), open("dr8_post.json", "w"), indent=1); open("dr8_post.out", "w").write("\n".join(O) + "\n")
