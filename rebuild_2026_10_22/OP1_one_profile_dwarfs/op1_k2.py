#!/usr/bin/env python3
"""OP1 K2: op1's E path, fed the smooth core's own m(x) at S 29.4, against SN1's Eof."""
import contextlib, io, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); s = open(os.path.join(HERE, "op1.py")).read(); s = s[:s.index("RES = {}")]
g = {"__file__": os.path.join(HERE, "op1.py"), "__name__": "x"}; sys.argv = ["op1.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s, g["__file__"], "exec"), g)
n = g["g"]; Q = n["systems"]("canonical"); d = []; U = n["U"]; X = np.exp(g["LX"])
for q in Q:
    Sig = 29.4 * U; r0 = n["solve_r0"](q["M200"], q["R200"], Sig, n["BS"]); M = math.pi * Sig * r0 ** 2 * np.array([float(n["BS"](x * q["R200"] / r0)) for x in (min(q["r12"] / q["R200"], 1.0),)])[0]
    lx = math.log(min(q["r12"], q["R200"]) / q["R200"]); ln = np.log(math.pi * Sig * r0 ** 2 * n["BS"](X * q["R200"] / r0) / q["M200"]); v = float(np.interp(lx, g["LX"], ln)) if lx >= g["LX"][0] else float(ln[0] + 2 * (lx - g["LX"][0]))
    d.append(abs(math.log10(q["gobs"] / (q["gN"] + n["G"] * q["M200"] * math.exp(v) / q["r12"] ** 2)) - n["Eof"](q, 29.4, n["BS"])))
print("K2 max", max(d), "median", float(np.median(d)), "PASS" if float(np.median(d)) < 0.005 else "FAIL")
