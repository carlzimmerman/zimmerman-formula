#!/usr/bin/env python3
"""VW1 Stage A2 (AMENDMENT_A1): HF1 gate 3's SPARC line against m, so against Q. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HF = os.path.join(os.path.dirname(HERE), "HF1_hybrid_fermion"); sys.path.insert(0, HF); sys.dont_write_bytecode = True
import hf1_g23 as H
import numpy as np
EV, CL, HJ = H.FM.EV, H.FM.C_L, H.FM.H_J; FAIR = 5.2715; RHO = 0.13 * 1.8784e-26; FD_I = 45.3
G = H.SP.load_gal(); res = {}; out = []
def P(s): print(s, flush=True); out.append(s)
P("VW1 Stage A2, AMENDMENT_A1, post-result. law on baryons + fermion, R4, fair share 5.2715")
for ft in H.FEET:
    for m in (3.74, 7.0, 11.0, 20.0, 50.0, 300.0):
        r, t, fr = H.sparc_fit(G, FAIR, m, H.A0[ft]); Q = (m * EV / CL ** 2) ** 4 / HJ ** 3; v = 3.15137 * (RHO / (FD_I * Q)) ** (1 / 3) / 1e3
        rat = float(np.median([x["ratio"] for x in fr])); ok = bool(r["rms"] <= 0.110 and 0.50 <= r["Y_med"] <= 0.80 and abs(t["tilt"]) <= 0.15)
        res[f"{ft}_{m:g}"] = dict(m=m, rms=r["rms"], Y=r["Y_med"], tilt=t["tilt"], median_Mf_over_Mb=rat, v0_km_s=v, passed=ok)
        P(f"{ft} m {m:g}: rms {r['rms']:.4f} Y {r['Y_med']:.3f} tilt {t['tilt']:+.3f}; median M_f/M_b at R_last {rat:.3f}; v0 {v:.2f} km/s; {'PASS' if ok else 'FAIL'}")
        json.dump(res, open(os.path.join(HERE, "vw1_a2.json"), "w"), indent=1); open(os.path.join(HERE, "vw1_a2.out"), "w").write("\n".join(out) + "\n")
P("kappa = 1/2 FITTED. Not theory closed."); open(os.path.join(HERE, "vw1_a2.out"), "w").write("\n".join(out) + "\n")
