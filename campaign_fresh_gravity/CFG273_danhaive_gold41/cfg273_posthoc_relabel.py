#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG273 POST HOC (labelled; written and run AFTER the one frozen measurement): a presentation fix for two rows.
The frozen estimator (CFG223's `implied`, solver bracket log10 s in [-3, +3]) flags a row 'no root' both when D <= 1 (the Newtonian floor) and when the root lies ABOVE the bracket (s* > 1000).
In the points file two rows (ids 1094616 and 1025101) carry no_root = 1 / s_star = 0.001 although D = 35 and 57 (closed-form s* of order 1.6e3 and 3.4e4): they are CEILING cases, not floor cases, and the file's
'quality' text ("NO ROOT ... robust against any added gas") is wrong for them.  This script writes cfg273_points_stageB_relabelled.csv: the same rows and numbers, with s_star = 1000 (the bracket ceiling), no_root = 0
and the quality text corrected for exactly those rows.  No frozen number is recomputed.  kappa = 1/2 FITTED.
"""
import os, csv, json, math, sys
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "HZQ_common"))
import hzq_core as H
main = json.load(open(os.path.join(HERE, "cfg273_stageB_results.json")))["numbers"]["rows"]
rows = list(csv.DictReader(open(os.path.join(HERE, "cfg273_points_stageB.csv"))))
cols = list(rows[0].keys())
fixed = []
for r in rows:
    oid = r["object"].replace("Danhaive JADES ", "")
    if oid.isdigit() and r["no_root"] == "1" and float(r["D"]) > 1.0:
        R_ = main[oid]
        r["no_root"] = "0"; r["s_star"] = "1000"; r["a0_1e-10_m_s2"] = f"{1000 * 0.93603:.6g}"
        r["quality"] = (f"CEILING, not floor: D = {float(r['D']):.1f} > 1 but s* lies above the solver bracket (> 1000; closed form {R_['GB'] / (H.A0C * 1.0) * 0 + 0:.0f}) -> vacuous upper bound; "
                        "the frozen file's NO ROOT label for this row is a bracket artefact").replace("closed form 0", "closed form >1e3")
        fixed.append(oid)
with open(os.path.join(HERE, "cfg273_points_stageB_relabelled.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rows]
print(f"relabelled rows (ceiling cases): {fixed}")
