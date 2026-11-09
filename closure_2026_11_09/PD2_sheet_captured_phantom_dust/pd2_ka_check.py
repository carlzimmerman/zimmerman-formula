#!/usr/bin/env python3
"""PD2 post-run KA check (disclosed; criteria 98a5315562): KA-Q3 with the cancellation-free form x = 1/(sqrt(1/4 + 1/y) + 1/2); KA-Q1's deviation
against the analytic offset of the full phantom M_ph = sqrt(M a0/G) r - M/2 (deep limit), R_trunc,full = R_closed + r_M/2, r_M = sqrt(G M/a0).
kappa = 1/2 FITTED; not theory closed."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(HERE, "pd2.json")))
ys = np.geomspace(1e-4, 1e4, 20); x = 1 / (np.sqrt(0.25 + 1 / ys) + 0.5); dev = float(np.max(np.abs(x * x / (1 - x) / ys - 1)))
out = dict(KA_Q3_stable=dict(max_rel_dev=dev, pass_=bool(dev < 1e-10)))
G, MS, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
for f in ("canonical", "alt"):
    rows = []
    for r in R[f]["KA_Q1"]["rows"]:
        rM = math.sqrt(G * 10 ** r["logMb"] * MS / A0[f]) / MPC; pred = r["closed_Mpc"] + rM / 2; rows.append(dict(logMb=r["logMb"], numeric=r["R_trunc_Mpc"], closed_plus_rM_half=pred, rel=r["R_trunc_Mpc"] / pred - 1))
    out[f] = dict(KA_Q1_with_offset=rows, max_abs_rel=max(abs(x["rel"]) for x in rows))
    print(f"[{f}] KA-Q1 numeric vs closed + r_M/2: " + "; ".join(f"{x['logMb']}: {x['numeric']:.4f} vs {x['closed_plus_rM_half']:.4f}" for x in rows) + f" (max rel {out[f]['max_abs_rel']:.1e})")
print(f"KA-Q3 stable form: max rel dev {dev:.1e} -> {'PASS' if dev < 1e-10 else 'FAIL'}")
json.dump(out, open(os.path.join(HERE, "pd2_ka_check.json"), "w"), indent=1)
