#!/usr/bin/env python3
"""CFG623 post-run robustness checks (POST HOC, reported only; change no frozen score, status or verdict).
R-1 Harvey-threshold sensitivity: beta-bar and Z_H of the seed-599 grid cells (alpha 0, 0.03, 0.1, 0.3, inf) if the d_SG
    threshold were 150/175/200/225/250 kpc (stability rule as frozen; counting rule as frozen).
R-2 Bullet-epoch majority margin at alpha = 0: number of agreeing variants at the two bracketing epochs, grid + 3 control seeds.
Run: python3 cfg623_diag.py -> cfg623_diag.out, cfg623_diag_results.json (reads runs/ only)"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg623_main as M
OUT, RES = [], {}
P = lambda s="": (print(s), OUT.append(s))
TH = [150.0, 175.0, 200.0, 225.0, 250.0]
r1 = {}
for f in M.FEET:
    for a in (0.0, 0.03, 0.1, 0.3, math.inf):
        run = json.load(open(os.path.join(HERE, "runs", M.name_of(dict(alpha=a, foot=f, **M.BASE)) + ".json"))); tp = run["t_peri"]
        row = {}
        for th in TH:
            win = [d for d in run["diag"] if 0.1 - 1e-9 <= d["t"] - tp <= 0.6 + 1e-9 and M.beta_of(d)[1] >= th]
            good = [d for d in win if M.stable(d)]
            bb = float(np.mean([M.beta_of(d)[0] for d in good])) if good else None
            ok = len(good) >= 10 and len(good) >= 0.5 * len(win)
            row[str(int(th))] = dict(n=f"{len(good)}/{len(win)}", scorable=ok, beta_bar=bb, Z_H=None if bb is None else (bb - M.HARV_B) / M.HARV_S)
        r1[f"{M.astr(a)}_{f}"] = row
        P(f"R-1 alpha {M.astr(a):>4s} {f}: " + "  ".join(f"{k}: Z_H {v['Z_H']:+.2f}{'' if v['scorable'] else '(unsc)'}" for k, v in row.items() if v["Z_H"] is not None))
RES["R1_threshold_sensitivity"] = r1
r2 = {}
for f in M.FEET:
    for sd in [599] + M.CTRL_SEEDS:
        run = json.load(open(os.path.join(HERE, "runs", M.name_of(dict(alpha=0.0, foot=f, seed=sd, **M.BASE)) + ".json")))
        ep = M.S.epoch(run["diag"], run["t_peri"]); i = ep["i_obs"]
        r2[f"{f}_seed{sd}"] = [M.n_agree(run["diag"][j]) for j in (i - 1, i)]
    P(f"R-2 alpha 0 {f}: agreeing variants at the Bullet bracketing epochs: " + ", ".join(f"seed {k.split('seed')[1]} {v}" for k, v in r2.items() if k.startswith(f)))
RES["R2_alpha0_bullet_majority"] = r2
open(os.path.join(HERE, "cfg623_diag.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg623_diag_results.json"), "w"), indent=1)
