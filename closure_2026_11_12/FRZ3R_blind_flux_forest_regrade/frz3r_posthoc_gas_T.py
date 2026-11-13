#!/usr/bin/env python3
"""FRZ3R post hoc (after RESULT_BLIND 292fe90b51; reported in RESULT.md only): gas-level Delta chi^2 of reading T (1D power
ratio of the smoothed gas skewers through the same flux-level gate). Usage: python3 frz3r_posthoc_gas_T.py <footing>
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, glob, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FOOT = sys.argv[1]
src = open(os.path.join(HERE, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(HERE, "frz3r_grade.py"), "__name__": "setup"}; sys.argv = ["x", FOOT]; exec(compile(src[:cut], "setup", "exec"), g)
FD, ZB, dchi2_sel, ALL = g["FD"], g["ZB"], g["dchi2_sel"], g["ALL"]
r = np.ones(FD["NB"])
for z in ZB:
    P = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "parts", f"turn_z{z:.1f}_s*_{FOOT}_N384.json")))]
    kv = np.array(P[0]["kv"]); R = np.mean([np.array(p["gas1d"]["gas_primary"]["B"]) / np.array(p["gas1d"]["gas_primary"]["R"]) for p in P], 0)
    s_ = FD["zs"] == round(z, 2); r[s_] = np.interp(FD["ks"][s_], kv[1:], R[1:])
    if z in (2.2, 3.0, 4.4): print(f"[{FOOT}] T gas 1D ratio z {z}: " + " ".join(f"{x}:{np.interp(x, kv[1:], R[1:]):.4f}" for x in (0.002, 0.005, 0.01, 0.02, 0.03)))
d = dchi2_sel(r, ALL); print(f"[{FOOT}] reading T gas-level Delta chi^2 (post hoc): {d:.1f}")
json.dump(dict(footing=FOOT, gas_level_dchi2_T=d, note="post hoc; kappa = 1/2 FITTED; not theory closed. Adopts nothing."), open(os.path.join(HERE, f"frz3r_posthoc_gas_T_{FOOT}.json"), "w"))
