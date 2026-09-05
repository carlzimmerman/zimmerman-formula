#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g02d -- cross-check of two_body_frequency_2026's leading isolated compact-pair result with the G02c machinery:
for an isolated Gaussian-filtered pair with d << xi and the filtered field deep (xi >> r_M), the mutual anomalous force is
-mu h r with h ~ (2/9) sqrt(G M a0)/xi^2, M = m1 + m2  =>  F_ph/F_N = (2/9) (d/xi)^2 (d/r_M(M))."""
import math, sys, os, io, contextlib, numpy as np, warnings; warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g02c_two_body_force.py")).read()
head = src[:src.index('print("=" * 110)')]
g = {"__file__": os.path.join(HERE, "g02c_two_body_force.py")}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(head, "g02chead", "exec"), g)
IMPORTED_FAILS = list(g.get("FAILS", []))   # failures of the executed G02c/G02 prefix are NOT discarded
PC, MSUN, G, A0, forces = g["PC"], g["MSUN"], g["G"], g["A0"], g["forces"]
FAILS = list(IMPORTED_FAILS)
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("g02d -- isolated compact filtered pair: F_ph/F_N against (2/9)(d/xi)^2 (d/r_M), the lead's leading harmonic coefficient")
rat = {}
for foot, a0 in A0.items():
    for (Mt, xi_pc) in ((0.1*MSUN, 0.1), (0.1*MSUN, 0.3), (1.0*MSUN, 0.3)):
        xi = xi_pc*PC; rM = math.sqrt(G*Mt/a0)
        for f in (0.1, 0.2):
            d = f*xi; r = forces(Mt/2, Mt/2, d, xi, a0)
            pred = (2/9)*(d/xi)**2*(d/rM); got = r["F2"]/r["FN2"]; rat[(foot, Mt, xi_pc, f)] = got/pred
            print(f"  {foot:9s} M = {Mt/MSUN:.1f} Msun  xi = {xi_pc:.1f} pc (xi/r_M = {xi/rM:5.1f})  d = {f:.1f} xi:  F_ph/F_N = {got:+.4e}  (2/9)(d/xi)^2(d/r_M) = {pred:.4e}  ratio {got/pred:.3f}")
deep = [v for k, v in rat.items() if k[2]/ (math.sqrt(G*k[1]/A0[k[0]])/PC) > 7 and k[3] == 0.1]
check("H1 the sign is attractive (F_ph/F_N > 0) and the ratio to the lead's coefficient is within 25% of 1 in the deep, compact regime (xi/r_M > 7, d = 0.1 xi)",
      all(abs(v - 1) < 0.25 for v in deep) and all(v > 0 for v in rat.values()), f"ratios {[round(v, 3) for v in deep]}")
far = [v for k, v in rat.items() if k[2] == 0.3 and k[1] < 0.5*MSUN]; near = [v for k, v in rat.items() if k[2] == 0.1 or k[1] > 0.5*MSUN]
dind = max(abs(rat[(f, M, x, 0.2)]/rat[(f, M, x, 0.1)] - 1) for (f, M, x, ff) in rat if ff == 0.1)
check("H2 the ratio approaches 1 as xi/r_M grows (mean 0.95-0.96 at xi/r_M = 8-9, 0.98 at 25-27: the coefficient is leading order in r_M/xi) and is independent of d/xi between 0.1 and 0.2 to 0.5%",
      min(far) > max(near) and dind < 5e-3, f"near {min(near):.3f}-{max(near):.3f}, far {min(far):.3f}-{max(far):.3f}, d-dependence {dind:.1e}")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
