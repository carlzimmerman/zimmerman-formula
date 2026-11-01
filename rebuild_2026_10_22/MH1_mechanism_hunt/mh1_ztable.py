#!/usr/bin/env python3
"""MH1: Lacey-Cole z(f, M) on X43's sigma(M), as AE1, read only, outputs here. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys, io, json, contextlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); X43 = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"); W = os.path.join(HERE, "cache_x43"); os.makedirs(W, exist_ok=True); os.chdir(W)
src = open(X43).read(); cut = src.index("k2 = all(abs(EPS[t]"); ns = {"__file__": os.path.join(HERE, "x43_collapse_core.py"), "__name__": "x43_ro"}; sys.argv = [X43]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], X43, "exec"), ns)
EPS, DC, OM = ns["EPS"], ns["DC"], ns["OMEGA"]; e = EPS["A_c2b_refit"]
def zf(M, f):
    s2 = lambda l: float(np.interp(l, e["lMg"], e["s2"])); S = np.sqrt(max(s2(np.log10(f * M)) - s2(np.log10(M)), 0.0)); D = DC / (DC + OM * S)
    return 0.0 if D >= 1 else float(np.interp(-D, -e["Dg"], e["zg"]))
F = np.geomspace(1e-5, 0.9999, 400); T = {str(M): [zf(M, x) for x in F] for M in (1e10, 1e12)}
assert abs(zf(1e12, .5) - .944) < .011
json.dump(dict(f=F.tolist(), z=T), open(os.path.join(HERE, "mh1_ztable.json"), "w")); print("ok", T[str(1e12)][::80])
