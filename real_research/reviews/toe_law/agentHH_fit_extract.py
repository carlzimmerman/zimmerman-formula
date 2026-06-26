#!/usr/bin/env python3
"""Two-component operator-model extraction of (ct, lock, K) from a printed Drho table.
The single-component VARPRO fit is ill-posed on the 16-point window (the subleading
(3/2+qF/2)cos-term rides at 30-60% with a different phase; the unbounded fit runs away —
bug log 7/11). The well-posed extraction: scan (ct, r) inside the FULL operator
prediction predO(nu; ct, r) = -nu[(3/2)F + (1/2)sF'], F the locked-pair profile with
constant ct and lock angle r, and fit only the overall scale K by least squares.

Usage: agentHH_fit_extract.py <logfile> <regex_tag> [AF qF phF wlo npow cval]
  regex matches lines 'nu = X: ... = Y'; defaults are the [3d-1]/[f] test profile.
"""
import sys
import re
import numpy as np
import mpmath as mp

logf = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else r'nu = +([0-9.]+): Born Drho_c = ([+-][0-9.e-]+)'
AF = float(sys.argv[3]) if len(sys.argv) > 3 else -2.0
qF = float(sys.argv[4]) if len(sys.argv) > 4 else -4.0 / 3
phF = float(sys.argv[5]) if len(sys.argv) > 5 else float(mp.pi / 8)
wlo = float(sys.argv[6]) if len(sys.argv) > 6 else 0.1
npow = int(sys.argv[7]) if len(sys.argv) > 7 else 6
cval = float(sys.argv[8]) if len(sys.argv) > 8 else 2.0

txt = open(logf).read()
rows = re.findall(tag, txt)
nus = [float(a) for a, b in rows]
yv = np.array([float(b) for a, b in rows])
print(f"[extract] {len(nus)} points from {logf}")
mp.mp.dps = 25
third = mp.mpf(1) / 3


def predf(nu, ct, r):
    def F(w):
        x = cval * w
        th = r * ct * x ** third + phF
        return (AF * x ** mp.mpf(qF) * mp.e ** (-ct * x ** third) * mp.cos(th)
                * (w / (w + mp.mpf(wlo))) ** npow)
    sv = mp.mpf(nu) / cval
    return float(-nu * (mp.mpf(3) / 2 * F(sv) + sv / 2 * mp.diff(F, sv)))


def ssr(ct, r):
    pr = np.array([predf(n, mp.mpf(ct), mp.mpf(r)) for n in nus])
    K = float(yv @ pr / (pr @ pr))
    res = (yv - K * pr) / (np.abs(yv) + 2e-5)
    return float(res @ res), K


s3 = float(np.sqrt(3))
grid = np.arange(1.95, 2.35, 0.02)
vals = [(c, *ssr(c, s3)) for c in grid]
cb = min(vals, key=lambda t: t[1])
g2 = np.arange(cb[0] - 0.02, cb[0] + 0.0201, 0.004)
vals2 = [(c, *ssr(c, s3)) for c in g2]
cb2 = min(vals2, key=lambda t: t[1])
print(f"[extract] ct scan (lock = sqrt3): ct_fit = {cb2[0]:.4f}  K = {cb2[2]:.4f}  "
      f"wssr = {cb2[1]:.5f}   [neighbors: "
      + ", ".join(f"{c:.3f}:{v:.2f}" for c, v, _ in vals2[::2]) + "]")
rg = [1.55, 1.65, 1.70, 1.716, 1.732, 1.748, 1.78, 1.85]
rvals = [(r, ssr(cb2[0], r)[0]) for r in rg]
rb = min(rvals, key=lambda t: t[1])
print(f"[extract] lock scan (ct = {cb2[0]:.4f}): r_fit = {rb[0]:.3f} (sqrt3 = {s3:.5f})   ["
      + ", ".join(f"{r:.3f}:{v:.2f}" for r, v in rvals) + "]")
pr = np.array([predf(n, mp.mpf(cb2[0]), mp.mpf(s3)) for n in nus])
K = float(yv @ pr / (pr @ pr))
print(f"[extract] pointwise |y/(K*predO) - 1| at the {len(nus)} points: "
      f"median = {np.median(np.abs(yv/(K*pr)-1)):.4f}, max = {np.max(np.abs(yv/(K*pr)-1)):.4f}")
