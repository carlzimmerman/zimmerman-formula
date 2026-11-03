#!/usr/bin/env python3
"""CX1 POST-RESULT sensitivity, written after cx1_real.out was read; changes no verdict. L|S line pair in L3 (and L3+E) with lensing radii or bins
dropped, and the conditional gap of the frozen criteria for comparison. Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 10 python3 -I cx1_post.py. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
sys.dont_write_bytecode = True; sys.argv = ["cx1", "post"]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cx1 as X
out = {}
for foot in X.FEET:
    D, _ = X.load(foot)
    for arm in ("L3", "L3+E"):
        base = X.rows_for(D, arm, "all")
        for lab, drop in (("none", D.line == "_"), ("drop lensing innermost radius (35 kpc)", (D.line == "L") & (D.k == 0)), ("drop lensing two innermost", (D.line == "L") & (D.k <= 1)),
                          ("drop bin4", D.name == "bin4"), ("drop bin3", D.name == "bin3"), ("drop bin2", D.name == "bin2")):
            R = X.scan(D, arm, base & ~drop); LL = X.line_level(D, R, MU=D.MU, arm=arm); out[f"{foot}|{arm}|{lab}"] = dict(L_S=LL.get("L|S"), LT_S=LL.get("LT|S"))
            X.P(f"{foot} {arm:5s} {lab:42s} L|S {LL.get('L|S')}")
        X.GAP = "conditional"; R = X.scan(D, arm, base); LL = X.line_level(D, R, MU=D.MU, arm=arm); X.GAP = "marginal"
        out[f"{foot}|{arm}|conditional gap"] = dict(L_S=LL.get("L|S"), IC1613_S=LL.get("IC1613|S")); X.P(f"{foot} {arm:5s} conditional gap (frozen, reported)        L|S {LL.get('L|S')}")
json.dump(out, open(os.path.join(HERE, "cx1_post.json"), "w"), indent=1); open(os.path.join(HERE, "cx1_post.out"), "w").write("\n".join(X.OUT) + "\n")
