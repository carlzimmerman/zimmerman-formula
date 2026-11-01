#!/usr/bin/env python3
"""BR1, reported after the result: bars are hard to see edge-on, so repeat at inclination < 75 deg. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
import numpy as np
from scipy.stats import fisher_exact
H = os.path.dirname(os.path.abspath(__file__)); G = json.load(open(os.path.join(H, "br1_matched.json"))); OUT = []
for hi in (75, 91):
    L = [g for g in G if 150 <= g["vf"] < 250 and g["inc"] < hi]; a = [g for g in L if g["fam"] == "SB"]; b = [g for g in L if g["fam"] == "SA"]; x, y = np.array([g["ub"] for g in a]), np.array([g["ub"] for g in b]); t = [[int((x <= .3).sum()), int((x > .3).sum())], [int((y <= .3).sum()), int((y > .3).sum())]]; OUT.append(f"i<{hi}: SB n {len(x)} med {np.median(x):.2f}; SA n {len(y)} med {np.median(y):.2f}; at floor {t}; Fisher two-sided p {fisher_exact(t)[1]:.3f}; off SB {np.median([g['uo'] for g in a]):.2f} SA {np.median([g['uo'] for g in b]):.2f}")
print("\n".join(OUT)); open(os.path.join(H, "br1_inc.out"), "w").write("\n".join(OUT) + "\n")
