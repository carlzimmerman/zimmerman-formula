#!/usr/bin/env python3
"""CFG152 POST-HOC (written after all frozen runs and after reading CFG124_G1_target.py; reported only, no pass line).

Resolves the reported row 'fall-time range: 3.765 Gyr (CFG152, x0 = 30) against 3.7 Gyr (CFG124 README)' and the split of
CFG124's count 2624.  It evaluates CFG152's OWN point-mass formula and constants (identical to cfg152_S_shells.py) on
CFG124's shell grid, reconstructed from its script: s = geomspace(0.05, 40, 240), scored where 0.3 <= s <= 30,
cases = 2 footings x 4 masses x 2 profiles (point, exponential sphere).  The exponential sphere itself stays untested here.
"""
import json
import sys

import numpy as np

import cfg152_common as C

NAME = "cfg152_S_posthoc_cfg124grid"
rep = C.Report(NAME, "main")
C.header(rep)
GM_SUN, GYR = 1.32712440018e20, 3.15576e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MASSES = [1e9, 1e10, 1e11, 1e12]


def t_fall(x0, Mb, a0):                      # same formula as cfg152_S_shells.py
    GM = GM_SUN * Mb
    rM = np.sqrt(GM / a0)
    r0 = x0 * rM
    return 0.5 * np.pi * np.sqrt(r0**3 / (2.0 * GM * np.sqrt(1.0 + x0**2)))


s_sh = np.geomspace(0.05, 40.0, 240)           # CFG124_G1_target.py, G1.2 (read after the CFG152 runs)
xs = s_sh[(s_sh >= 0.3) & (s_sh <= 30)]
rep.p(f"CFG124 grid: {xs.size} scored points per case, x from {xs[0]:.4f} to {xs[-1]:.4f}; "
      f"cases 2 footings x 4 masses x 2 profiles = 16; total {16 * xs.size}")
rows = {}
for f, a0 in A0.items():
    for M in MASSES:
        tf = t_fall(xs, M, a0) / GYR
        rows[f"{f}_{M:.0e}"] = [float(tf.min()), float(tf.max())]
        rep.p(f"   {f:9s} M_b = {M:.0e}: point-mass t_fall on CFG124's grid = {tf.min():.4f} ... {tf.max():.4f} Gyr "
              f"(at x = 30 exactly: {t_fall(30.0, M, a0) / GYR:.4f} Gyr)")
mx = max(v[1] for v in rows.values())
mn = min(v[0] for v in rows.values())
rep.p(f"overall point-mass range on CFG124's grid: {mn:.4f} - {mx:.4f} Gyr (CFG124 prints 0.003 ... 3.69, README 0.003-3.7)")
rep.p(f"ratio of the last scored x to 30 = {xs[-1] / 30:.5f}; 3.765 Gyr x that ratio ~ {3.765 * xs[-1] / 30:.3f} Gyr "
      f"(t_fall grows ~ linearly in x at large x)")
rep.results.update(n_scored_per_case=int(xs.size), total_cases=int(16 * xs.size), x_last=float(xs[-1]),
                   x_first=float(xs[0]), range_on_cfg124_grid_Gyr=[mn, mx], rows=rows)
rep.check("POST-HOC (reported): CFG124's count 2624 = 16 cases x 164 scored points", 16 * xs.size == 2624,
          kind="reported, post-hoc")
rep.check("POST-HOC (reported): my formula on CFG124's grid gives a maximum that rounds to 3.69 Gyr", round(mx, 2) == 3.69,
          f"{mx:.4f}", kind="reported, post-hoc")
sys.exit(rep.finish())
