#!/usr/bin/env python3
"""16th/84th percentile of M_b/M200 over the canonical BE1 active set, BE1's loader."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
B1 = os.path.join(REB, "BE1_baryon_energy_budget", "be1_energy.py"); T1 = open(B1).read().replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {HERE!r}', 1)
D = {"__file__": B1, "__name__": "be1_ro"}; sys.argv = [B1]; exec(compile(T1.split("K2rows = run(")[0], B1, "exec"), D)
by = {q["name"]: q for q in D["GALS"]}; f = [10 ** by[r["name"]]["lMb"] / 10 ** r["lM200"] for r in D["run"]("canonical") if r["active"]]
json.dump(dict(LO=float(np.percentile(f, 16)), HI=float(np.percentile(f, 84)), n=len(f)), open(os.path.join(HERE, "fb_percentiles.json"), "w"), indent=1)
