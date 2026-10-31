#!/usr/bin/env python3
"""ZK1 K3: full reruns from the ICs of three finished X48 runs with the compiled kernel, compared with X48's own snapshots. The differences also measure the zooms' chaos noise. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); X48 = os.path.join(REB, "X48_native_cf_zoom"); WK = os.path.join(HERE, "k3_runs"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
X77P = os.path.join(REB, "X77_direct_core_surface_density", "x77_direct_eta.py"); src = open(X77P).read(); src = src[:src.index("# K2: formula vs direct integration")]
NS = dict(__file__=X77P, __name__="x77_prefix"); a0 = sys.argv; sys.argv = [X77P]; exec(compile(src, X77P, "exec"), NS); sys.argv = a0; fit, XA = NS["fit"], NS["XA"]
def rerun(s):
    W = os.path.join(WK, f"M1e13_s{s}_ng48"); os.makedirs(W, exist_ok=True); t = time.time()
    with open(os.path.join(W, "run.log"), "a") as f: rc = subprocess.run(["nice", "-n", "5", sys.executable, os.path.join(HERE, "x48_fast.py"), "--mass", "1e13", "--seed", str(s), "--ng", "48", "--work", W, "--resume"], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, env=dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")).returncode
    return s, rc, time.time() - t
with ThreadPoolExecutor(3) as ex: R = list(ex.map(rerun, (1, 2, 3)))
for s, rc, dt in R: P(f"rerun seed {s}: exit {rc}, {dt:.0f} s")
if any(r[1] != 0 for r in R): P("A RERUN FAILED: no K3"); sys.exit(1)
P("K3 M1e13 ng 48 from the ICs, compiled kernel against X48's snapshot:")
dE, dC, dM = [], [], []; ok_ic = True
for s in (1, 2, 3):
    A = np.load(os.path.join(X48, "runs", f"M1e13_s{s}_ng48", "snap_zf.npz"), allow_pickle=False); B = np.load(os.path.join(WK, f"M1e13_s{s}_ng48", "snap_zf.npz"), allow_pickle=False)
    ma, mb = json.loads(str(A["meta"])), json.loads(str(B["meta"])); ic = all(ma[k] == mb[k] for k in ("nu", "xbar", "gamma", "qM", "RG", "L", "N", "mpart", "zf", "Mf", "eps", "t_end", "constraint_check")); ok_ic &= ic
    rho = ma["Mf"] / (4 / 3 * math.pi * ma["qM"] ** 3) * (1 + ma["zf"]) ** 3; oa, ra = fit(A["x"], float(A["m"]), rho, ma["eps"]); ob, rb = fit(B["x"], float(B["m"]), rho, mb["eps"])
    e = math.log(rb["S"]["eta"] / ra["S"]["eta"]); c = math.log(ob["c_nfw_fit"] / oa["c_nfw_fit"]); dE.append(abs(e)); dC.append(abs(c))
    ca, cb = XA.centre(A["x"], float(A["m"])), XA.centre(B["x"], float(B["m"])); ra_, rb_ = np.sort(np.sqrt(((A["x"] - ca) ** 2).sum(1))), np.sort(np.sqrt(((B["x"] - cb) ** 2).sum(1)))
    g = np.geomspace(oa["rconv"], oa["rvir"], 40); ln = lambda rr: np.log(np.maximum(np.searchsorted(rr, g), 1)); d = np.abs(ln(rb_) - ln(ra_)); dM += d.tolist()
    P(f"  seed {s}: ICs identical {ic}; steps {ma['steps']} vs {mb['steps']}; eta_S {ra['S']['eta']:.2f} vs {rb['S']['eta']:.2f}; c_nfw {oa['c_nfw_fit']:.2f} vs {ob['c_nfw_fit']:.2f}; r_vir {oa['rvir']:.4f} vs {ob['rvir']:.4f}; median |d ln M(<r)| {np.median(d):.4f}, max {d.max():.4f}")
me, mc, mm = float(np.median(dE)), float(np.median(dC)), float(np.median(dM)); ok = ok_ic and me <= 0.05 and mc <= 0.05 and mm <= 0.02
P(f"K3 median |d ln eta_S| {me:.4f} (limit 0.05), |d ln c_nfw| {mc:.4f} (0.05), |d ln M(<r)| {mm:.4f} (0.02): {'PASS' if ok else 'FAIL'}")
json.dump(dict(d_eta=dE, d_c=dC, d_M_med=mm, ok=ok), open(os.path.join(HERE, "zk1_k3.json"), "w"), indent=1); open(os.path.join(HERE, "zk1_k3.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
