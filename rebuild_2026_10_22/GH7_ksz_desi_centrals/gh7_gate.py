#!/usr/bin/env python3
"""GH7 power gate: CAP scatter and velocity rms only. No T-hat is computed: CAP and v are never multiplied together per lens."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W = os.path.join(EXT, "gh7_work")
C_ = np.load(os.path.join(W, "gh7_cap.npz")); V = np.load(os.path.join(W, "gh7_vel.npz"))["v"]; J = json.load(open(os.path.join(HERE, "gh7_vel.json"))); R = J["R"]
g = C_["good"]; cap = C_["cap"][g]; iz, il = C_["iz"][g], C_["il"][g]; v = V[g] / 299792.458; TCMB = 2.72548e6
for i in range(10): cap[iz == i] -= cap[iz == i].mean(axis=0)
Cc = np.cov(cap.T); Ci = np.linalg.inv(Cc); su2 = float(np.sum(v * v)); w = np.array([[np.sum(v[(iz == i) & (il == j)] ** 2) for j in range(4)] for i in range(10)]) / su2
print(f"N {g.sum()}, rms v_rec {v.std() * 299792.458:.1f}, per-lens CAP rms (uK) {np.round(np.sqrt(np.diag(Cc)), 1)}, cond {np.linalg.cond(Cc):.1e}", flush=True)
mod = {k: np.einsum("ij,ijk", w, C_["m" + k]) * TCMB for k in ("1.0", "1.8", "3.0")}; S = lambda x: float(np.sqrt(su2 * x @ Ci @ x))
RES = {"N": int(g.sum()), "R_frozen": R, "su2": su2}
for lab, Rx in (("frozen R", R), ("context R (r 0.64, sigma 300 km/s, data rms)", .64 * 300 / (v.std() * 299792.458))):
    s = {k: S(mod[k] * Rx) for k in mod}; d = S((mod["1.8"] - mod["1.0"]) * Rx); RES[lab] = dict(R=Rx, S1=s["1.0"], S18=s["1.8"], S3=s["3.0"], S18m1=d, S3m1=S((mod["3.0"] - mod["1.0"]) * Rx))
    print(f"{lab}: R {Rx:.3f}; S(1) {s['1.0']:.2f} S(1.8) {s['1.8']:.2f} S(3) {s['3.0']:.2f}; S(1.8-1) {d:.2f} S(3-1) {RES[lab]['S3m1']:.2f}", flush=True)
print("model CAP at A=1, R=1 (uK), k=1.8:", np.round(mod["1.8"], 4), flush=True)
RES["G1"] = RES["frozen R"]["S18"] >= 3; RES["G2"] = RES["frozen R"]["S18m1"] >= 3; print("GATE (frozen R): G1", RES["G1"], "G2", RES["G2"], flush=True); json.dump(RES, open(os.path.join(HERE, "gh7_gate.json"), "w"), indent=1, sort_keys=True)
