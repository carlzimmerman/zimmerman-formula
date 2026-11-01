#!/usr/bin/env python3
"""DR1 post-result stress, not graded: 5-point running mean of dM/dr along each curve. Does noise in the derivative carry SPARC's result? kappa = 1/2 FITTED; not theory closed."""
import os, runpy, sys
import numpy as np
sys.argv = ["x"]; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "dr1_offline.py")).read(); src = src[:src.index("R = dict(sparc=")]; __file__ = os.path.join(HERE, "dr1_offline.py"); exec(src)
_s0 = sparc_gs
def sparc_gs(q, c):
    R, GB = q["Rm"], q["GB"]
    if c == 0: return GB.copy()
    dM = np.gradient(R[:, None] ** 2 * GB, R, axis=0); k = np.ones(5) / 5; n = len(R)
    if n >= 5: dM = np.apply_along_axis(lambda v: np.convolve(np.pad(v, 2, mode="edge"), k, "valid"), 0, dM)
    return GB + c * np.maximum(dM, 0.0) / (3 * R[:, None])
for f in ("canonical", "alt"):
    s = sparc(f, 1, "R1"); print(f, f"rms {s['rms']:.4f} U {s['U']:.2f} tilt {s['tilt']:+.2f} line {s['line']} chi {s['chi2']:.0f}")
