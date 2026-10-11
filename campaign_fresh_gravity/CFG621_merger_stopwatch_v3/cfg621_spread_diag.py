#!/usr/bin/env python3
"""CFG621 post-run diagnosis (2026-10-11; README disclosure B-D1).  No verdict is changed.  For every grid cell, at the two
diagnostics bracketing the Bullet epoch: the distance of each E-2 lensing variant from the primary lensing peak, which variants
exceed T_L, the primary lensing-galaxy and gas-galaxy vectors, and the sub-main galaxy distance.  Reads runs_B/ only.
Run: python3 cfg621_spread_diag.py -> cfg621_spread_diag.out, cfg621_spread_diag_results.json"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg621_sim as S
T_L = json.load(open(os.path.join(HERE, "cfg621_stageA_results.json")))["T_L"]
VAR = ["(300,60)", "(300,90)", "(200,75)", "(400,75)"]
OUT, RES = [], {}
for fn in sorted(glob.glob(os.path.join(HERE, "runs_B", "a*_v2666.7_eta1.132.json"))):
    r = json.load(open(fn)); nm = os.path.basename(fn)[:-5]
    ep = S.epoch(r["diag"], r["t_peri"]); rows = []
    for i in (ep["i_obs"] - 1, ep["i_obs"]):
        d = r["diag"][i]["sub"]; L = np.array(d["lens"]); g = np.array(d["gal"])
        dist = [float(np.hypot(*(np.array(a) - L))) for a in d["lens_alts"]]
        rows.append(dict(i=i, lens_minus_gal=(L - g).tolist(), gas_minus_gal=(np.array(d["gas"]) - g).tolist(), variant_dist=dist,
                         variants_over_TL=[VAR[k] for k, x in enumerate(dist) if x > T_L],
                         main_sub=float(np.hypot(*(np.array(r["diag"][i]["main"]["gal"]) - g)))))
    RES[nm] = rows
    OUT.append(f"{nm}: " + " | ".join(f"lens-gal {np.round(x['lens_minus_gal'], 1).tolist()} gas-gal {np.round(x['gas_minus_gal'], 1).tolist()} "
                                      f"variants {np.round(x['variant_dist'], 1).tolist()} over T_L {x['variants_over_TL']}" for x in rows))
cnt = {v: sum(v in x["variants_over_TL"] for rows in RES.values() for x in rows) for v in VAR}
RES["count_over_TL_by_variant"] = cnt
OUT.append(f"T_L = {T_L:.2f} kpc; bracketing epochs with a variant over T_L, by variant: {cnt}")
print("\n".join(OUT))
open(os.path.join(HERE, "cfg621_spread_diag.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg621_spread_diag_results.json"), "w"), indent=1)
