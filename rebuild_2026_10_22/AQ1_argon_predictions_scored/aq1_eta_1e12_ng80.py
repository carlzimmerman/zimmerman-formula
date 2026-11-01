#!/usr/bin/env python3
"""AQ1: X80's converged-cusp eta estimator (X81 fit, exact NFW at each run's c_nfw, x_c 0.001), read-only on the nine 1e12 ng 80 seeds (A5) against the nine ng 64 seeds; ratio with X80's bootstrap. Scores Argon's 1.035 +- 0.025. X48's files are read only.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -I aq1_eta_1e12_ng80.py
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
REB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); X48 = os.path.join(REB, "X48_native_cf_zoom")
X81P = os.path.join(REB, "X81_core_convergence", "x80_core_convergence.py"); sys.argv = [X81P]
src = open(X81P).read(); src = src[:src.index("# K1: exact smooth core")]; NS = dict(__file__=X81P, __name__="x81_prefix"); exec(compile(src, X81P, "exec"), NS)
import numpy as np
fit, a_fit, M_nfw, eta_of = NS["fit"], NS["a_fit_profile"], NS["M_nfw"], NS["eta_of"]
out = {}
for ng in (80, 64):
    v = []; cs = []; ec = []
    for s in range(1, 10):
        sn = os.path.join(X48, "runs", f"M1e12_s{s}_ng{ng}", "snap_zf.npz")
        if not os.path.exists(sn): continue
        Z = np.load(sn); x, m = Z["x"], float(Z["m"]); meta = json.loads(str(Z["meta"])); rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
        o, res = fit(x, m, rho, meta["eps"]); c = o.get("c_nfw_fit") if res is not None else None
        if not c: print(ng, s, "flagged", o.get("flag")); continue
        v.append(float(eta_of(a_fit(M_nfw(c), 0.001)))); cs.append(c); ec.append(res["S"]["eta"])
    v = np.array(v); b = np.median(v[np.random.default_rng(20261030).integers(0, len(v), (10000, len(v)))], axis=1)
    out[ng] = dict(n=len(v), eta_conv_med=float(np.median(v)), p16=float(np.percentile(b, 16)), p84=float(np.percentile(b, 84)), c_nfw_med=float(np.median(cs)), eta_cut_med=float(np.median(ec)), per_run=v.tolist(), c_per_run=cs)
    print(f"1e12 ng {ng}: n {len(v)}, eta_conv {np.median(v):.2f} [{np.percentile(b,16):.2f}, {np.percentile(b,84):.2f}], c_nfw med {np.median(cs):.2f}, eta_cut med {np.median(ec):.2f}; per run eta_conv {np.round(v,2).tolist()}")
G = np.random.default_rng(20261030); med = lambda A: np.median(np.array(A)[G.integers(0, len(A), (10000, len(A)))], axis=1)
r = out[80]["eta_conv_med"] / out[64]["eta_conv_med"]; rb = med(out[80]["per_run"]) / med(out[64]["per_run"])
print(f"ratio eta_conv(ng80)/eta_conv(ng64) {r:.4f} [{np.percentile(rb,16):.4f}, {np.percentile(rb,84):.4f}]; K ng64 vs 25.94: {out[64]['eta_conv_med']:.4f}")
out["ratio"] = dict(r=r, p16=float(np.percentile(rb, 16)), p84=float(np.percentile(rb, 84)))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "aq1_eta_1e12_ng80.json"), "w"), indent=1)
