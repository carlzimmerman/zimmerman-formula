#!/usr/bin/env python3
"""SP3: mass-rule tables, RET1's lines and AM1's curve, unchanged. Reads only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H); R = json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_results.json")))["lines"]; Q = json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_post_results.json")))["lines"]; A = json.load(open(os.path.join(RB, "AM1_native_abundance_match", "am1_results.json")))["curve"]; TG = ("A_c2b_refit", "B_cfg886_bg"); O = dict(E1={}, C1={}, AM1={})
for t in TG:
    for n, D in (("E1", R[t]["E1"]), ("C1", Q[t]["C1"])):
        x = sorted(D, key=float); O[n][t] = dict(x=[float(k) for k in x], y=[D[k] for k in x])
    O["AM1"][t] = dict(x=A["lMb"], y=A["lM200"])
json.dump(O, open(os.path.join(H, "sp3_tables.json"), "w"))
