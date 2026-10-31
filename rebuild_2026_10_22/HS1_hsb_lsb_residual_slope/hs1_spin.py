#!/usr/bin/env python3
"""HS1 POST-RESULT, reported only. Line set before this script's first run: at fixed mass a disc's surface density goes as lambda^-2 (size ~ lambda R_vir), so for the zooms' scatter in S to flatten the tilt (rank correlation with SBeff about 0.9, hs1_scatter.out), S and spin need rho <= -0.8 at fixed mass. Measured on X48's own z_f snapshots, ng 64, nine seeds at each of 1e12, 1e13, 1e14.
Limit: an isolated Lagrangian sphere has no external tidal torque, so its spin is internal asymmetry only, and may not rank as a real halo's does.
    python3 hs1_spin.py   kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); X77P = os.path.join(REB, "X77_direct_core_surface_density", "x77_direct_eta.py"); _s = open(X77P).read(); _s = _s[:_s.index("# K2: formula vs direct integration")]; NS = dict(__file__=X77P, __name__="x77_prefix"); _a = sys.argv; sys.argv = [X77P]; exec(compile(_s, X77P, "exec"), NS); sys.argv = _a; FIT, XA = NS["fit"], NS["XA"]; G = 4.30091e-9; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("HS1 spin: S against spin at fixed mass, X48's z_f snapshots, ng 64; POST-RESULT, reported only; kappa = 1/2 FITTED; not theory closed"); T = {}
for M in ("1e12", "1e13", "1e14"):
    T[M] = []
    for s in range(1, 10):
        f = os.path.join(REB, "X48_native_cf_zoom", "runs", f"M{M}_s{s}_ng64", "snap_zf.npz")
        if not os.path.exists(f): continue
        Z = np.load(f, allow_pickle=False); x, v, m = Z["x"], Z["v"], float(Z["m"]); me = json.loads(str(Z["meta"])); rho = me["Mf"] / (4 / 3 * math.pi * me["qM"] ** 3) * (1 + me["zf"]) ** 3; o, r = FIT(x, m, rho, me["eps"])
        if r is None: continue
        c = XA.centre(x, m); d = x - c; rr = np.sqrt((d * d).sum(1)); rv = o["rvir"]; k = rr < rv; vc = v[k].mean(0); J = np.cross(d[k], v[k] - vc).sum(0) * m; Mv = m * k.sum(); Vv = math.sqrt(G * Mv / rv); lam = float(np.linalg.norm(J) / (math.sqrt(2) * Mv * Vv * rv)); dk = rr < 0.1 * rv; ain = float(np.linalg.norm(np.cross(d[dk], v[dk] - vc).sum(0)) * m / (math.sqrt(2) * m * dk.sum() * Vv * rv))
        T[M].append(dict(seed=s, lam=lam, lam_in=ain, eta=r["S"]["eta"], S=r["S"]["eta"] * 18 * math.pi ** 2 * rho * rv, c=o.get("c_nfw_fit"), zf=me["zf"]))
    q = T[M]; P(f"  M {M}: n {len(q)}; median lambda' {np.median([a['lam'] for a in q]):.4f}, sd lg lambda' {np.std(np.log10([a['lam'] for a in q]), ddof=1):.3f}; median eta {np.median([a['eta'] for a in q]):.2f}, sd lg eta {np.std(np.log10([a['eta'] for a in q]), ddof=1):.3f}; Spearman(eta, lambda') {spearmanr([a['eta'] for a in q], [a['lam'] for a in q])[0]:+.3f}")
res = lambda k: np.concatenate([np.log10([a[k] for a in T[M]]) - np.median(np.log10([a[k] for a in T[M]])) for M in T]); e, l, cc = res("eta"), res("lam"), res("c"); r1 = spearmanr(e, l); r2 = spearmanr(cc, l); rng = np.random.default_rng(1); bb = [spearmanr(e[i], l[i])[0] for i in (rng.integers(0, len(e), len(e)) for _ in range(5000))]
P(f"pooled residuals at fixed mass, n {len(e)}: Spearman(lg eta, lg lambda') {r1[0]:+.3f}, p {r1[1]:.2g}, bootstrap 68 % [{np.percentile(bb, 16):+.3f}, {np.percentile(bb, 84):+.3f}]; Spearman(lg c_nfw, lg lambda') {r2[0]:+.3f}, p {r2[1]:.2g}; sd lg lambda' residual {l.std(ddof=1):.3f} (real halos about 0.24)")
V = "RANKING NATIVE" if r1[0] <= -0.8 else "RANKING NOT NATIVE"; P(f"Line set before running, rho <= -0.8: {V}. Upper 68 % edge needed to reach it: {np.percentile(bb, 16):+.3f}")
json.dump(dict(table=T, rho=r1[0], p=r1[1], boot68=[float(np.percentile(bb, 16)), float(np.percentile(bb, 84))], line=V), open(os.path.join(HERE, "hs1_spin.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "hs1_spin.out"), "w").write("\n".join(OUT) + "\n")
