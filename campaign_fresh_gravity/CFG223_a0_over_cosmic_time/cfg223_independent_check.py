#!/usr/bin/env python3
"""CFG223 independent recomputation (written after the main run; reported only): the eight figure points' implied a0 ratios s* recomputed with scipy's brentq on the scalar median delta(s) = 0
(no vectorised bisection), from the same rows, against the committed values in cfg223_results.json.  LambdaCDM has no a0; author decompositions; not a detection; kappa = 1/2 FITTED."""
import os, sys, io, json, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg223_a0_over_time.py")).read()
stop = src.index('P("\\nCONTROLS")')
ns = {"__file__": os.path.join(LANE, "cfg223_a0_over_time.py"), "__name__": "cfg223_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:stop], "cfg223_a0_over_time.py", "exec"), ns)
PTS, _, _ = ns["build_points"](mut=False)
NU, A0 = ns["NU"], ns["A0L"]
J = json.load(open(os.path.join(LANE, "cfg223_results.json")))["points"]
OUT = [__doc__.strip(), ""]
worst = 0.0
for p, r in zip(PTS[:8], J[:8]):
    D, gb = p["D"], p["gb"]
    ls = brentq(lambda l: float(np.median(np.log10(D / np.atleast_1d(NU(gb / (A0 * 10 ** l)))))), -3, 3, xtol=1e-14, rtol=1e-14)
    d = abs(ls - r["log_s"]); worst = max(worst, d)
    OUT.append(f"  {p['short']:13s} s* brentq {10 ** ls:.6f}   committed {r['s']:.6f}   |delta log10 s*| {d:.1e}")
ok = worst < 1e-9
OUT.append(f"\n  [{'PASS' if ok else 'FAIL'}] the committed s* equal the independent brentq values: max |delta log10 s*| {worst:.1e}")
print("\n".join(OUT))
open(os.path.join(LANE, "cfg223_independent_check.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
