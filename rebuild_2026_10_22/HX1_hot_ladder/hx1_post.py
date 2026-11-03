#!/usr/bin/env python3
"""HX1, reported only, written after the stage-1 read: L-ORDER without the inside-Re ellipticals (MaNGA; MaNGA and ATLAS), whose B_need carries
the stellar IMF (criteria, Limits). Same isotonic statistic and seed rule as hx1_ladder.py. Moves no label. kappa = 1/2 FITTED; not theory closed."""
import json, re
import numpy as np
S = open("hx1_ladder.py").read(); ns = {"np": np, "NB": 2000}; exec(S[S.index("def pava"):S.index("# ---------- run")], ns)
R = json.load(open("hx1_ladder.json")); OUT = open("hx1_post.out", "w")
for foot, F in R["footings"].items():
    for drop in (("MaNGA",), ("MaNGA", "ATLAS")):
        rng = np.random.default_rng(20261103); nm = sorted((r for r in F["rungs"] if not r.startswith(drop)), key=lambda r: F["rungs"][r]["key"])
        k, y, s = (np.array([F["rungs"][r][q] for r in nm]) for q in ("key", "y", "s")); o = ns["order_p"](k, y, s, rng)
        line = f"{foot}: without {' and '.join(drop)}: chi2 {o['chi2']:.2f}, p {o['p']:.3f} -> {'ORDERED' if o['p'] >= .05 else 'NOT ORDERED'}; fit " + ", ".join(f"{r} {v:+.3f}" for r, v in zip(nm, o["f"]))
        print(line); OUT.write(line + "\n")
    t = F["tests"]["L-FLAT X-COP"]; line = f"{foot}: X-COP points used in L-FLAT {t['n_used']}, rung n {F['rungs']['X-COP']['n']}"; print(line); OUT.write(line + "\n")
