#!/usr/bin/env python3
"""UL1 corrected UR3 rows: UR3's and SP3's code unchanged, my own c200 from raw (ul1_c.json) and its seed range; output here only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
ME = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(ME); SP = os.path.join(RB, "SP3_starting_point")
s = open(os.path.join(SP, "sp3_post.py")).read(); s = s[:s.index('P("c: EM1 line')]; __file__ = os.path.join(SP, "sp3_post.py"); exec(s)
OUT.clear(); R = {}; C = json.load(open(os.path.join(ME, "ul1_c.json")))["c200"]
P(f"UL1 corrected weighing, own c200 {C} from raw, seed range 6.25-9.625. r target 0.90-1.10, n >= 27; MW FEASIBLE IN PRIORS. EM1, NFW on R200")
for c in (12.95, C, 6.25, 9.625):
    for mo in ("off", "fq"): show(f"NFW c200 {c} {mo}", shape="nfwc", c=c, mode=mo)
k = abs(R["NFW c200 12.95 off"]["r"] - 1.090) <= 0.002; P(f"K8 c 12.95 off reproduces UR3 1.090: {'PASS' if k else 'FAIL'}")
show("NFW c200 7.8 off (SP3)", shape="nfwc", c=7.8, mode="off"); k8 = k and abs(R["NFW c200 7.8 off (SP3)"]["r"] - 1.266) <= 0.002; P(f"K8 c 7.8 off reproduces SP3 1.266: {'PASS' if k8 else 'FAIL'}")
json.dump(R, open(os.path.join(ME, "ul1_weigh.json"), "w"), indent=1, default=float); open(os.path.join(ME, "ul1_weigh.out"), "w").write("\n".join(OUT) + "\n")
