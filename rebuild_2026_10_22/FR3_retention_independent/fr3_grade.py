#!/usr/bin/env python3
"""FR3 grade: FR1's path (fr1.py's worker text, fr1_def.py, read only), own cache. python3 fr3_grade.py [--mutate]. Reinstates nothing. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys, math
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); FR1 = os.path.join(RB, "FR1_fair_share_retention")
T = open(os.path.join(FR1, "fr1.py")).read(); T = T[:T.index("def L(k, **w)")]; ns = {"__file__": os.path.join(FR1, "fr1.py"), "__name__": "fr1x"}; exec(compile(T, "fr1x", "exec"), ns)
ns["CC"] = os.path.join(HERE, "cache_jobs"); os.makedirs(ns["CC"], exist_ok=True); run = ns["run"]; LN = ns["LN"]
R = json.load(open(os.path.join(HERE, "fr3_results.json")))["R"]; Y = json.load(open(os.path.join(HERE, "fr3_y_ComptonY.json"))); A = dict(R["anchored"]); F = dict(R["fit"]); St = R["St"]; Hl = dict(mode="line", x="M", a=LN["H"]["a"], b=LN["H"]["b"], piv=LN["H"]["piv"]); J = []
for fs in ("0.034", "0.0615"):
    J += [(f"KH {fs}", fs, "0.005", Hl), (f"R {fs}", fs, "0.005", A), (f"Rfit {fs}", fs, "0.005", F), (f"Rup {fs}", fs, "0.005", dict(A, a=A["a"] + St)), (f"Rdn {fs}", fs, "0.005", dict(A, a=A["a"] - St)), (f"Rcarry {fs}", fs, "0.005", dict(A, carry=Y["c"])), (f"MUT flip {fs}", fs, "0.005", dict(A, b=-A["b"]))]
with ThreadPoolExecutor(2) as ex:
    for lab, _ in ex.map(lambda j: run(*j), J): print("done", lab, flush=True)
