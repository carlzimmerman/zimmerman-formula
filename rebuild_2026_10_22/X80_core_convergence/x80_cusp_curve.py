#!/usr/bin/env python3
"""X80 reported (post-result, not graded): eta of X77's smooth-core fit to an exact NFW, vs the inner cut x_c and c.
    python3 x80_cusp_curve.py"""
import os, sys
sys.argv = [sys.argv[0]]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "x80_core_convergence.py")).read(); src = src[:src.index("# K1: exact smooth core")]
NS = dict(__file__=os.path.join(HERE, "x80_core_convergence.py"), __name__="x80_prefix"); exec(src, NS)
OUT = ["X80 cusp curve: eta(smooth-core fit to exact NFW on [x_c, 1]); SPARC limit 21.2; kappa = 1/2 FITTED; not theory closed"]
xcs = (0.1, 0.05, 0.03, 0.01, 0.003, 0.001)
OUT.append("   c   | " + "  ".join(f"x_c {x:<6}" for x in xcs))
for c in (4.0, 5.0, 6.0, 7.75, 9.0):
    OUT.append(f"  {c:4.2f} | " + "  ".join(f"{float(NS['eta_of'](NS['a_fit_profile'](NS['M_nfw'](c), x))):10.2f}" for x in xcs))
print("\n".join(OUT)); open(os.path.join(HERE, "x80_cusp_curve.out"), "w").write("\n".join(OUT) + "\n")
# per ng 64 run: its own c_nfw, eta at its own cut (cusp model) and at x_c -> 0.001 (cut removed)
import json, numpy as np
R = json.load(open(os.path.join(HERE, "x80_results.json")))["runs"]
e_cut, e_0 = [], []
for k, r in sorted(R.items()):
    if r.get("ng") != 64 or not r.get("c_nfw"): continue
    e_cut.append(float(NS["eta_of"](NS["a_fit_profile"](NS["M_nfw"](r["c_nfw"]), r["xc"]))))
    e_0.append(float(NS["eta_of"](NS["a_fit_profile"](NS["M_nfw"](r["c_nfw"]), 0.001))))
e_cut, e_0 = np.array(e_cut), np.array(e_0); i = np.random.default_rng(20261030).integers(0, len(e_0), (10000, len(e_0)))
b = np.median(e_0[i], axis=1)
L = [f"ng 64 (n {len(e_0)}): median eta at own cut {np.median(e_cut):.2f} (measured X77 20.83); cut removed (x_c 0.001) {np.median(e_0):.2f} "
     f"[68% {np.percentile(b, 16):.2f}, {np.percentile(b, 84):.2f}]; over SPARC limit 21.2 by x{np.median(e_0) / 21.2:.2f}; runs under 21.2: {int((e_0 <= 21.2).sum())}/{len(e_0)}"]
print(L[0]); open(os.path.join(HERE, "x80_cusp_curve.out"), "a").write(L[0] + "\n")
