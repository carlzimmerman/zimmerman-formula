#!/usr/bin/env python3
"""WA1: real rows at each cell's fitted shifts: closure of the quadratic and line-only gates. Keys aren't rerun here. python3 wa1_hat.py cid foot. kappa = 1/2 FITTED; not theory closed."""
import json, sys, warnings
warnings.filterwarnings("ignore")
from wa1_rows import *
cid, foot = sys.argv[1:3]; T = json.load(open(os.path.join(HERE, "wa1_thetahat.json")))[f"{cid}|{foot}"]; c = load_cand(cid); os.makedirs(os.path.join(HERE, "hat"), exist_ok=True)
th = {k: NUIS[k][0] + NUIS[k][1] * T[k] for k in ("ups", "gas_abs", "dist", "lens", "hse")}
l, g, s = evaluate(cid, c, foot, th, mw_cache={}); json.dump(dict(l=l, g=g, B23=s.get("B23")), open(os.path.join(HERE, "hat", f"{cid}_{foot}.json"), "w"), indent=0, sort_keys=True, default=float); print("done", cid, foot, flush=True)
