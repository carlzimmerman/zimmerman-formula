#!/usr/bin/env python3
"""ZN4 verdict's c200: NFW fit to the median m(x), x 0.05-1, z = 0, as ZN1's README defines it; ng 64 (ZN3's table) against ng 80. kappa = 1/2 FITTED; not theory closed."""
import json, os
import numpy as np
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); A = json.load(open(os.path.join(RB, "ZN3_native_shape_at_1e15", "zn3_shapes.json"))); B = json.load(open(os.path.join(HERE, "zn4_shapes.json"))); X = np.array(A["x"]); s = (X >= 0.05) & (X <= 1); mu = lambda y: np.log1p(y) - y / (1 + y); OUT = []
def c(ln): return minimize_scalar(lambda q: float(((np.log(mu(np.exp(q) * X[s]) / mu(np.exp(q))) - np.array(ln)[s]) ** 2).sum()), bounds=(np.log(.5), np.log(40)), method="bounded").x
ok = True
for M in ("1e14", "1e15"):
    a, b = float(np.exp(c(A[M]["0.00"]["lnm"]))), float(np.exp(c(B[M]["0.00"]["lnm"]))); cs = [float(np.exp(c(q["lnm"]))) for q in B[M]["0.00"]["seeds"]]; ok &= abs(b / a - 1) <= 0.10; OUT.append(f"M {M}: c200 ng 64 {a:.3f}, ng 80 {b:.3f}, ratio {b / a:.3f}; ng 80 seeds {min(cs):.2f}-{max(cs):.2f}; lg M200 {A[M]['0.00']['lgM']:.3f} vs {B[M]['0.00']['lgM']:.3f}")
OUT.append(f"c200 within 10 % at both masses: {ok}"); print("\n".join(OUT)); open(os.path.join(HERE, "zn4_c200.out"), "w").write("\n".join(OUT) + "\n")
