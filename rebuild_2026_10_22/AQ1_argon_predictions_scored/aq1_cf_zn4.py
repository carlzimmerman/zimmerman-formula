#!/usr/bin/env python3
"""AQ1: X48's c_f = r_vir / r_-2 estimator (x48_analyze.measure, read-only) on ZN4's ng 80 collapses at 1e14 and 1e15 (seeds 1-6) and on
ZN3's ng 64 1e15 collapses, against X48 A4's ng 64 1e14 median 10.07. Scores Argon's c_f(1e14, ng 80) 10.8 +- 0.4 and c_f(1e15, ng 80) 11.6 +- 0.6.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -I aq1_cf_zn4.py
kappa = 1/2 FITTED; not theory closed."""
import glob, importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
_s = importlib.util.spec_from_file_location("x48_analyze", os.path.join(RB, "X48_native_cf_zoom", "x48_analyze.py")); XA = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = [_a[0]]; _s.loader.exec_module(XA); sys.argv = _a
OUT = []; R = {}
def P(s): print(s, flush=True); OUT.append(s)
P("AQ1 c_f on ZN4's ng 80 collapses (X48's estimator, read-only); kappa = 1/2 FITTED; not theory closed")
for lab, pat in (("1e14 ng80 (ZN4)", os.path.join(RB, "ZN4_cluster_resolution", "runs_zf", "M1e14_s?_ng80")), ("1e15 ng80 (ZN4)", os.path.join(RB, "ZN4_cluster_resolution", "runs_zf", "M1e15_s?_ng80")), ("1e15 ng64 (ZN3)", os.path.join(RB, "ZN3_native_shape_at_1e15", "runs_zf", "M1e15_s?_ng64")), ("1e14 ng64 (X48 A4)", os.path.join(RB, "X48_native_cf_zoom", "runs", "M1e14_s?_ng64"))):
    v = []; nf = []
    for d in sorted(glob.glob(pat)):
        sn = os.path.join(d, "snap_zf.npz")
        if not os.path.exists(sn): continue
        Z = np.load(sn, allow_pickle=False); meta = json.loads(str(Z["meta"])); rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
        o = XA.measure(Z["x"], float(Z["m"]), rho, meta["eps"])
        if o.get("flag") == "ok": v.append(o["cf"]); nf.append(o["c_nfw_fit"])
    if not v: P(f"  {lab}: no finished run"); continue
    R[lab] = dict(n=len(v), cf=v, cf_med=float(np.median(v)), nfw_med=float(np.median(nf)))
    P(f"  {lab}: n {len(v)}, c_f median {np.median(v):.2f} (per seed {np.round(v, 2).tolist()}), NFW-fit median {np.median(nf):.2f}")
a4 = json.load(open(os.path.join(RB, "X48_native_cf_zoom", "x48_analyze_results_ng64_A4.json")))["cf_by_mass"].get("1e+14"); k = a4 is not None and abs(R["1e14 ng64 (X48 A4)"]["cf_med"] - a4) < 1e-9
P(f"  K: 1e14 ng 64 through this path {R['1e14 ng64 (X48 A4)']['cf_med']:.4f} against A4's {a4}: {'PASS' if k else 'FAIL'}")
c14, c15 = R["1e14 ng80 (ZN4)"]["cf_med"], R["1e15 ng80 (ZN4)"]["cf_med"]
P(f"  Argon: c_f(1e14, ng 80) 10.8 +- 0.4 -> {c14:.2f}: {'HIT' if abs(c14 - 10.8) <= 0.4 else 'MISS'}; c_f(1e15, ng 80) 11.6 +- 0.6 -> {c15:.2f}: {'HIT' if abs(c15 - 11.6) <= 0.6 else 'MISS'}")
json.dump(dict(runs=R, K=bool(k)), open(os.path.join(HERE, "aq1_cf_zn4.json"), "w"), indent=1); open(os.path.join(HERE, "aq1_cf_zn4.out"), "w").write("\n".join(OUT) + "\n")
