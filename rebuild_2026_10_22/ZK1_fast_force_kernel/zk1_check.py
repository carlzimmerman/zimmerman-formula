#!/usr/bin/env python3
"""ZK1 K1, K2, MUTATE (criteria in FROZEN_CRITERIA.md). K3 is zk1_k3.py. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(os.path.dirname(HERE), "X48_native_cf_zoom", "runs")
sys.path.insert(0, HERE); import x48_fast as F
X = F.X; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
OLH2 = 1.0; C = None
P("ZK1 K1, K2: compiled kernel against x48_zoom.accel; kappa = 1/2 FITTED; not theory closed")
C = X.cosmology(); OLH2 = C["OL"] * C["H0"] ** 2
good = True
for run in ("M1e13_s1_ng48", "M1e14_s3_ng64", "M1e12_s1_ng64"):
    Z = np.load(os.path.join(RUNS, run, "snap_zf.npz"), allow_pickle=False); meta = json.loads(str(Z["meta"])); x = Z["x"]; m = float(Z["m"]); eps = meta["eps"]
    t0 = time.time(); a0 = F.NUMPY_ACCEL(x, m, eps, OLH2); t1 = time.time(); a1 = F.accel(x, m, eps, OLH2); t2 = time.time()
    d = np.sqrt(((a1 - a0) ** 2).sum(1)); na = np.sqrt((a0 ** 2).sum(1)); mx = float(d.max() / np.median(na)); md = float(np.median(d / na)); ok = mx <= 1e-10 and md <= 1e-12; good &= ok
    P(f"K1 {run}, N {len(x)}: max |da|/median |a| {mx:.2e}, median |da|/|a| {md:.2e}: {'PASS' if ok else 'FAIL'}; numpy {t1 - t0:.1f} s, compiled {t2 - t1:.2f} s, x {(t1 - t0) / (t2 - t1):.0f}")
    if "--mutate" in sys.argv: break
if "--mutate" in sys.argv: P("MUTATE: " + ("FAILS K1 as it must" if not good else "PASSES K1: the check doesn't bite")); sys.exit(0 if not good else 1)
Z = np.load(os.path.join(RUNS, "M1e13_s1_ng48", "snap_zf.npz"), allow_pickle=False); meta = json.loads(str(Z["meta"])); m = float(Z["m"]); eps = meta["eps"]; GYR = 1 / X.KMS_MPC_TO_GYR
def run(acc):
    x, v = Z["x"].copy(), Z["v"].copy(); a = acc(x, m, eps, OLH2); t = 0.0
    for _ in range(20):
        amax = float(np.sqrt((a * a).sum(1)).max()); dt = meta["eta"] * math.sqrt(eps / max(amax, 1e-30)) / GYR; dts = dt * GYR
        v += 0.5 * dts * a; x += dts * v; a = acc(x, m, eps, OLH2); v += 0.5 * dts * a; t += dt
    return x, v, t
x0, v0, t0 = run(F.NUMPY_ACCEL); x1, v1, t1 = run(F.accel); dx = float(np.abs(x1 - x0).max() / np.abs(x0).max()); dv = float(np.abs(v1 - v0).max() / np.abs(v0).max()); ok = dx <= 1e-9 and dv <= 1e-9; good &= ok
P(f"K2 20 steps from M1e13_s1_ng48's snapshot: max |dx| {dx:.2e}, max |dv| {dv:.2e}, dt sums {t0:.9f}, {t1:.9f}: {'PASS' if ok else 'FAIL'}")
open(os.path.join(HERE, "zk1_check.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if good else 1)
