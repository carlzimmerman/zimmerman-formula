#!/usr/bin/env python3
"""Independent re-check of ABS1's key numbers by a second path (reported, not part of any word): linear-in-k interpolation, direct
np.linalg.solve with the full covariance, per-seed-half models, and SE for the data-at-uncovered variant."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
import numpy as np
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_14", "FWN1R_blind_split_f_ceiling"))
import fwn1r_lib as X
FD = X.forest_data(); cf, lower = FD["CF"]; Uc = np.tril(cf).T if lower else np.triu(cf); COV = Uc.T @ Uc
ZS, KS, PD = FD["zs"], FD["ks"], FD["Pd"]
PB = os.path.join(REPO, "closure_2026_11_14", "FWN2_forest_flux_split_f4", "parts_b")
def q(d): return float(d @ np.linalg.solve(COV, d))
for ft in ("canonical", "alt"):
    J = {(z, s): json.load(open(os.path.join(PB, f"prim_z{z:.1f}_s{s}_{ft}.json"))) for z in X.ZB for s in range(4)}
    kv = {z: np.array(J[(z, 0)]["kv"]) for z in X.ZB}
    def p(z, nm, ss): return sum(np.array(J[(z, s)]["flux"]["primary"][nm]["p"]) for s in ss)
    def model(ss, lin=False):
        m = np.empty(len(PD))
        for z in X.ZB:
            s_ = ZS == round(z, 2); P_ = p(z, "R", ss) / len(ss)
            m[s_] = np.interp(KS[s_], kv[z][1:], P_[1:]) if lin else np.exp(np.interp(np.log(KS[s_]), np.log(kv[z][1:]), np.log(P_[1:])))
        return m
    def r(nm, ss):
        out = np.ones(len(PD))
        for z in X.ZB:
            s_ = ZS == round(z, 2); out[s_] = np.interp(np.log(KS[s_]), np.log(kv[z][1:]), (p(z, nm, ss) / p(z, "R", ss))[1:])
        return out
    cover = np.array([KS[i] >= kv[round(float(ZS[i]), 1)][1] for i in range(len(PD))])
    m = model(range(4)); ml = model(range(4), True)
    C = COV[np.ix_(cover, cover)]; e = (m - PD)[cover]; el = (ml - PD)[cover]
    print(ft, "chi2_0 log-log", round(float(e @ np.linalg.solve(C, e)), 1), "linear-k", round(float(el @ np.linalg.solve(C, el)), 1),
          "seeds 0,1", round(float(((model([0, 1]) - PD)[cover]) @ np.linalg.solve(C, (model([0, 1]) - PD)[cover])), 1),
          "seeds 2,3", round(float(((model([2, 3]) - PD)[cover]) @ np.linalg.solve(C, (model([2, 3]) - PD)[cover])), 1))
    sel22 = (ZS == 2.2) & cover
    print(ft, "z 2.2 model/data, covered points (k, ratio):", " ".join(f"{k:.4f}:{v:.3f}" for k, v in zip(KS[sel22][::4], (m / PD)[sel22][::4])))
    for nm in ("J3.5", "J4", "J4.5", "J5"):
        rr = r(nm, range(4)); D = q((rr - 1) * PD)
        out = {}
        for tag, sc in (("model held", m), ("model linear-k held", ml), ("data at uncovered", np.where(cover, m, PD)), ("model seeds 0,1", model([0, 1])), ("model seeds 2,3", model([2, 3]))):
            Dp = q((rr - 1) * sc)
            Dj = np.array([q((r(nm, [s for s in range(4) if s != j]) - 1) * sc) for j in range(4)]); SE = math.sqrt(3 / 4 * np.sum((Dj - Dj.mean()) ** 2))
            out[tag] = f"{Dp:.4f} (SE {SE:.4f}; D+2SE {Dp + 2 * SE:.3f}, D-2SE {Dp - 2 * SE:.3f})"
        print(ft, nm, f"D {D:.4f};", "; ".join(f"{k}: {v}" for k, v in out.items()))
