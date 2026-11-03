#!/usr/bin/env python3
"""MB1, reported only: the factor lambda on M_x that sets X-COP's mean to zero, per arm F, E, N and footing (criteria: SHORT / OVER
report the factor needed). lambda multiplies R inside the rule, so F's tide feeds back. Moves no label. kappa = 1/2 FITTED; not theory closed."""
import json, math, types
import numpy as np
import mb1_core as C, mb1_acc
n = mb1_acc.load(); R0 = C.ratio; OUT = open("mb1_lambda.out", "w"); res = {}
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
def rows(arm, f, lam):
    C.ratio = lambda *a, **k: lam * R0(*a, **k)
    try: return n["rows_xcop"](types.SimpleNamespace(g=lambda Q: C.g(Q, arm)), f)
    finally: C.ratio = R0
for arm in ("F", "E", "N"):
    res[arm] = {}
    for f in n["FEET"]:
        lo, hi = math.log(0.25), math.log(400.0); mlo, mhi = rows(arm, f, math.exp(lo))["B23"]["value"], rows(arm, f, math.exp(hi))["B23"]["value"]; side = 0
        for _ in range(30):
            x = hi - mhi * (hi - lo) / (mhi - mlo); X = rows(arm, f, math.exp(x)); m = X["B23"]["value"]
            if abs(m) < 2e-3: break
            if m > 0:
                lo, mlo = x, m
                if side == 1: mhi *= .5
                side = 1
            else:
                hi, mhi = x, m
                if side == -1: mlo *= .5
                side = -1
        res[arm][f] = dict(lam=math.exp(x), mean=m, rms=X["B24"]["value"], B25=X["B25"]["Z"])
        say(arm, f, f"lambda {math.exp(x):.2f}: X-COP mean {m:+.4f}, rms {X['B24']['value']:.3f}, B25 Z {X['B25']['Z']:+.2f}")
json.dump(res, open("mb1_lambda.json", "w"), indent=1)
