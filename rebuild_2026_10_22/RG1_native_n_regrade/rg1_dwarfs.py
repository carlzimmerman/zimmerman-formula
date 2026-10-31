#!/usr/bin/env python3
"""RG1 P1: X49's script with the native-N rule. RG1_SHAPE smooth|burkert, RG1_RULE native|floor. floor + burkert is K1."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); P = os.path.join(REB, "X49_dwarfs_route_e_floor", "x49_dwarfs.py")
sys.path.insert(0, HERE); import rg1_lib as L
SHAPE, RULE = os.environ.get("RG1_SHAPE", "smooth"), os.environ.get("RG1_RULE", "native"); TAG = f"{RULE}_{SHAPE}" + ("_MUTATE" if L.MUT != 1 else "")
s = open(P).read(); a = "r0 = solve_r0(M200, R200, SIG[f]); Mh = math.pi * SIG[f] * r0 ** 2 * float(B(min(r12, R200) / r0))"; assert s.count(a) == 1
b = "S_ = SFN(M200 / MSUN, f); r0 = solve_r0(M200, R200, S_); Mh = math.pi * S_ * r0 ** 2 * float(B(min(r12, R200) / r0))"
s = s.replace(a, b)
a = "def B(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)"; assert s.count(a) == 1
s = s.replace(a, a + "\nB0 = B\nif SHAPE == 'smooth': B = BSM\ndef SFN(M, f): return SIG[f] if RULE == 'floor' else RSN(M) * MSUN / PC ** 2")
s = s.replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = os.path.dirname(os.path.abspath(__file__)); HERE_REAL = HERE').replace('os.path.join(HERE, f"x49_', f'os.path.join(RG1DIR, f"rg1_x49_{TAG}_')
g = {"__file__": P, "__name__": "__main__", "SHAPE": SHAPE, "RULE": RULE, "BSM": L.B_smooth, "RSN": L.S_nat, "RG1DIR": HERE}
sys.argv = [P]
try: exec(compile(s, P, "exec"), g)
except SystemExit: pass
R = g["RES"]; out = {f: {c: {k: v[k] for k in ("N", "median", "sd", "Z", "reproduced", "M200", "r0_kpc")} for c, v in R["footings"][f]["classes"].items()} for f in R["footings"]}
json.dump(dict(shape=SHAPE, rule=RULE, classes=out, verdict=R["verdict"], fair={f: R["footings"][f]["fair_share"] for f in R["footings"]}), open(os.path.join(HERE, f"rg1_p1_{TAG}.json"), "w"), indent=1, default=float)
