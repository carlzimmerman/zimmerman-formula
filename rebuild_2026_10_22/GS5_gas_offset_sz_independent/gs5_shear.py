#!/usr/bin/env python3
"""GS5 second route, NOT INDEPENDENT (FROZEN_CRITERIA.md): the 15 keys' shear on ZN3's path, eRASS1's gas x 10^d, one M200 scale along fair share. Consistency line only; takes no part in any class. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE5 = os.path.dirname(os.path.abspath(__file__)); RB5 = os.path.dirname(HERE5); ZN3 = os.path.join(RB5, "ZN3_native_shape_at_1e15"); SRC = open(os.path.join(ZN3, "zn3_grade.py")).read()
# zn3_grade.py with its main block cut at the exec: load the grader text the way its own --k1 does, without touching any ZN3 output
_i = SRC.index('if "--k1" in sys.argv:'); PRE = SRC[:_i]; NS = {"__file__": os.path.join(ZN3, "zn3_grade.py"), "__name__": "gs5"}; exec(compile(PRE, NS["__file__"], "exec"), NS); T3 = NS["T3"]
_k = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:'); exec(compile(T3[:_k], NS["__file__"], "exec"), NS); run, cells, HH = NS["run"], NS["cells"], NS["HH"]; G0 = NS["GAS"]; SH = os.path.join(ZN3, "zn3_shapes.json"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(ZN3, "zn3_results.json")))["runs"]; os.environ.pop("ZN3_TWO", None)
def go(fs, d):
    NS["GAS"] = G0.replace("10 ** 0.111", f"10 ** {d!r}"); assert (f"10 ** {d!r}" in NS["GAS"]) ; return cells(run(fs, "fs", True, SH))
P("GS5 shear line: NOT INDEPENDENT of the grader. kappa = 1/2 FITTED; not theory closed")
K = go("0.034", 0.111); C = J["f* 0.034, X-COP's gas"]["cells"]; dk = max(abs(K[h][k]["Z"] - C[h][k]["Z"]) for h in HH for k in C[h]); P(f"K4 d = +0.111 reproduces ZN3's Z's at f* 0.034: |d| {dk:.1e}: {'PASS' if dk <= 1e-9 else 'FAIL'}")
if dk > 1e-9: sys.exit(1)
GRID = [-0.05, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25]; RES = {}
for fs in ("0.034", "0.0615"):
    RES[fs] = {}
    for d in GRID:
        O = go(fs, d); RES[fs][str(d)] = {h: {k: O[h][k]["Z"] for k in O[h]} for h in HH}; P(f"  f* {fs} d {d:+.2f}: " + "; ".join(f"h {h}: chi2 {sum(v ** 2 for v in RES[fs][str(d)][h].values()):.1f}, worst {max(RES[fs][str(d)][h].items(), key=lambda t: abs(t[1]))[0]} {max(RES[fs][str(d)][h].values(), key=abs):+.2f}, all |Z|<=2 {all(abs(v) <= 2 for v in RES[fs][str(d)][h].values())}" for h in HH))
import numpy as np
for fs in RES:
    for h in HH:
        ch = np.array([sum(v ** 2 for v in RES[fs][str(d)][h].values()) for d in GRID]); fine = np.linspace(GRID[0], GRID[-1], 3001); from scipy.interpolate import CubicSpline; cs = CubicSpline(GRID, ch)(fine); m = fine[np.argmin(cs)]; ins = fine[cs <= cs.min() + 1]; allz = [d for d in GRID if all(abs(v) <= 2 for v in RES[fs][str(d)][h].values())]
        P(f"f* {fs} {h}: chi2 minimum at d {m:+.3f} ({cs.min():.1f}), dchi2 = 1 edges {ins[0]:+.3f} to {ins[-1]:+.3f} (Z's correlated: indicative); grid points with all |Z| <= 2: {allz}")
        RES[fs][h + "_min"] = dict(d=float(m), lo=float(ins[0]), hi=float(ins[-1]), allz=allz)
json.dump(RES, open(os.path.join(HERE5, "gs5_shear_results.json"), "w"), indent=1); open(os.path.join(HERE5, "gs5_shear.out"), "w").write("\n".join(OUT) + "\n")
