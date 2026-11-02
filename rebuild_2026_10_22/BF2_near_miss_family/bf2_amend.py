#!/usr/bin/env python3
"""BF2 Amendment A1 selection. kappa = 1/2 FITTED; not theory closed."""
import json, os
from bf2_common import *
d = json.load(open(os.path.join(LANE, "bf2_scan.json"))); R = [r for r in d["rows"] if "err" not in r]
def Sf(r, ft): c = r[ft]; return max(c["rms"] / .110, abs(c["U"] - .65) / .15, abs(c["tilt"]) / .15, abs(c["LT"]) / .10)
def lines(r, ft): c = r[ft]; return c["rms"] <= .11 and .5 <= c["U"] <= .8 and abs(c["tilt"]) <= .15
V = [r for r in R if lines(r, "canonical") and lines(r, "alt") and abs(r["xa"]) <= .05 and r["xar"] <= .10]; print("clearing", len(V)); V.sort(key=lambda r: (max(r["S"], Sf(r, "alt")), r["nodes"], r["s"])); seen = set(); o = {}
for r in V:
    if r["sig"] in seen: continue
    seen.add(r["sig"]); t = f"P{5 + len(o)}"; o[t] = r; write_cand(t, r["s"], r["w"], "Amendment A1 selection."); print(t, f"W{r['w']}", r["s"], f"S {r['S']:.3f}, {Sf(r, 'alt'):.3f} h0 {r['h0min']:.3f}-{r['h0max']:.3f}", r["canonical"], r["alt"], r["xa"], r["xar"])
    if len(o) == 4: break
json.dump(o, open(os.path.join(LANE, "bf2_amend.json"), "w"), indent=0, sort_keys=True)
