#!/usr/bin/env python3
"""BK1 summary table from runs/. kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, numpy as np
from bk1_engine import bits_of
assert bits_of(.1) == 0 and abs(bits_of(.01) - -math.log2(.15)) < 1e-12; print("K4 bits arithmetic ok")
tr = dc = g2 = hits = ctrl = 0; rows = []; g3 = 0; n3 = 0; passA = passB = 0; mr = [0, 0]
for f in sorted(glob.glob("runs/*.json")):
    R = json.load(open(f)); s = R["stats"]; tr += sum(s["tried_formal"].values()); dc += sum(s["dimcorrect"].values()); g2 += s.get("G2_tried", 0) or 0
    if R.get("mech_rate_le3"): mr[0] += R["mech_rate_le3"]["mech"]; mr[1] += R["mech_rate_le3"]["sampled"]
    for k, g in R["targets"].items():
        if k.endswith("_2nd") or k.startswith("PLANT"): continue
        d = g["depth"]; hits += d["5"]["real"]; ctrl += d["5"]["ctrl_mean"]; b = g.get("bits"); passA += bool(b and b >= 10); n3 += len(g["hits_le3"]); g3 += g["g3_mech_le3"]
        L = g["hits_le3"][0] if g["hits_le3"] else None; rows.append((R["run"], k, g["dstar"], g.get("P"), b, g["ceiling_bits"], d["5"]["real"], d["5"]["ctrl_mean"], L and L["expr"], L and L["Z"], (g.get("span_null") or {}).get("bits")))
print(f"tried {tr:.4g}; dim-correct {dc:.4g}; G2 {g2:.4g}; hits depth<=5 {hits:.4g}; control mean {ctrl:.4g}; ratio {hits / ctrl:.3f}; gate 2 reading A pass {passA}; depth<=3 hits {n3}, mech gate 3 {g3}; all depth<=3 dimensionless trees mech {mr}")
for r in rows: print(r)
json.dump(dict(tried=tr, dim_correct=dc, G2_tried=g2, hits=hits, ctrl=ctrl, passA=passA, le3=n3, mech=g3, mech_all=mr, rows=rows), open("bk1_read.json", "w"), indent=0, default=str)
fr = (.46, 2 * math.log10(1 + 2 * .027)); print("Gate 4 overlap: XR window inside D5 window (canonical):", 5.35 - .29 > 5.37 - 2.63, 5.35 + .29 < 5.37 + 2.63)
r = np.random.default_rng(20261102); a = r.uniform(-1, 1, 200000); b = r.uniform(-1, 1, 200000); print("control, XR-sized and D5-sized windows overlap, scrambled +-1 dex:", float((np.abs(a - b) < .25).mean()))
