#!/usr/bin/env python3
"""X48 AMENDMENT A2 grade: nine-seed median c_f per mass at ng 48 against the frozen window [3.3, 4.6]; bootstrap 68 % interval
(10 000 resamples, seed 20261026); NFW-fit median reported. Reads x48_analyze_results_ng48_A2.json. Writes x48_grade_A2.out/json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "x48_analyze_results_ng48_A2.json")))
W = (3.3, 4.6); OUT = ["X48 A2 grade (ng 48; convergence beyond ng 48 not tested); kappa = 1/2 FITTED; not theory closed"]
by = {}
for k, o in R["runs"].items():
    if o.get("flag") == "ok" and o.get("ng") == 48: by.setdefault(o["M"], []).append((o["seed"], o["cf"], o["c_nfw_fit"], o["rm2"], o.get("n_inside_rm2")))
res = {}; rng = np.random.default_rng(20261026)
for M, rows in sorted(by.items()):
    cf = np.array([r[1] for r in rows]); nfw = np.array([r[2] for r in rows]); med = float(np.median(cf))
    bs = np.median(cf[rng.integers(0, len(cf), (10000, len(cf)))], axis=1); lo, hi = (float(x) for x in np.percentile(bs, [16, 84]))
    lab = "IN WINDOW" if W[0] <= med <= W[1] else ("ABOVE WINDOW" if med > W[1] else "BELOW WINDOW")
    nsoft = int(sum(1 for r in rows if r[3] <= 0.0105 * (M / 1e12) ** (1 / 3)))
    res[f"{M:.0e}"] = dict(n=len(cf), seeds=sorted(r[0] for r in rows), median=med, boot68=[lo, hi], nfw_median=float(np.median(nfw)), label=lab,
                           per_seed={int(r[0]): r[1] for r in rows}, n_rm2_at_floor=nsoft)
    OUT.append(f"  M {M:.0e}: N {len(cf)} seeds; c_f median {med:.2f} (68 % {lo:.2f}-{hi:.2f}); NFW-fit median {float(np.median(nfw)):.2f} (reported); {lab}; "
               f"runs with r_-2 at the smallest resolved radius (~0.010 (M/1e12)^1/3 Mpc): {nsoft}")
labs = {v["label"] for v in res.values()}
V = "IN WINDOW" if labs == {"IN WINDOW"} else "ABOVE WINDOW" if labs == {"ABOVE WINDOW"} else f"MIXED {sorted(labs)}"
OUT.append(f"A2 VERDICT (frozen window [3.3, 4.6], nine-seed medians): {V}")
print("\n".join(OUT)); open(os.path.join(HERE, "x48_grade_A2.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(window=W, masses=res, verdict=V), open(os.path.join(HERE, "x48_grade_A2.json"), "w"), indent=1)
