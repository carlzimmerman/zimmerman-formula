#!/usr/bin/env python3
"""TX1: key and cheap-gate lists by the frozen rule: top 10 T-effective by Z per arm and footing; real adds the run's best T-free by Z and BK2's row (a). python3 -I tx1_lists.py. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); BK2A = "I5(gb,a0)*(((8*pi/3)*(a0**-0.5*gg*gb**-0.5))+sq((gs**2*gb**-2)))"; os.makedirs(os.path.join(H, "chunks", "lists"), exist_ok=True)
for f in ("canonical", "alt"):
    for a in ("real", "c1", "c2", "c3", "label"):
        p = os.path.join(H, f"tx1_train_TL0_{f}_{a}.json")
        if not os.path.exists(p): print("missing", p); continue
        J = json.load(open(p)); L = [r["F"] for r in J["T"][:10]]
        if a == "real": L += [J["F"][0]["F"], BK2A]
        json.dump(L, open(os.path.join(H, "chunks", "lists", f"{f}_{a}.json"), "w"), indent=0); print(f, a, len(L))
