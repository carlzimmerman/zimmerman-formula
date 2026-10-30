#!/usr/bin/env python3
"""TL1 POST-RESULT, reported only: finer k scan (the frozen grid jumps from 3 to 5). kappa = 1/2 FITTED; not theory closed."""
import json, os
S = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tl1_tail.py")).read(); __file__ = os.path.abspath(__file__)
exec(compile(S[:S.index("LAB = {}")], "tl1_head", "exec"))
Q = {}
for foot in ("canonical", "alt"):
    for mode in ("base", "T2", "T1"):
        STATE.update(mode=mode, gam=2.25)
        for k in (2.5, 3, 3.5, 4, 4.5, 5, 6):
            g = kids(foot, k); Q[f"{foot}|{mode}|{k}"] = dict(H=g["H2H_b34"], L=g["L2H_b34"]); P(f"  [{foot} {mode} k={k}] H {g['H2H_b34']:.1f} L {g['L2H_b34']:.1f}")
json.dump(Q, open(os.path.join(HERE, "tl1_kscan.json"), "w"), indent=1)
