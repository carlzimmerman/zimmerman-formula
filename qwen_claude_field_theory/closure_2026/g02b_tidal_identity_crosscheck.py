#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g02b -- independent cross-check of filtered_tidal_relation_2026's central identity Q2/D = 2y/(5[3 lambda(y) - y]),
lambda = 1 + (y-1)e^{-y}, y = g_obs/a0, with the G02 machinery (different code: log-r x theta phantom density + mode-wise
output filter).  The identity's structural content -- independence of xi and of source mass -- and its value are both tested.
This check also caught G02's first-run error in the external-field conversion (the relation solved in the wrong direction)."""
import math, sys, os, numpy as np, warnings; warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g02_filtered_efe.py")).read()
head = src[:src.index("# ---------------------------------------------------------------- 3. the scans")]
g = {}; exec(compile(head, "g02head", "exec"), g)
PC, MSUN, G, A0, GM = g["PC"], g["MSUN"], g["G"], g["A0"], g["GM"]
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("=" * 100); print("g02b -- cross-check of the central tidal identity"); print("=" * 100)
ratios = {}
for foot, a0 in A0.items():
    y = 2.32e-10/a0; eN = y*(1 - math.exp(-y))*a0; lam = 1 + (y - 1)*math.exp(-y); pred = 2*y/(5*(3*lam - y)); rM = math.sqrt(GM/a0)
    for xi_pc in (0.3, 1.0, 3.0, 10.0):
        for M in (MSUN, 1e-3*MSUN):
            xi = xi_pc*PC
            r, th, rho = g["phantom_density"](M, xi, "gauss", eN, a0, min(1e-4*rM, 1e-3*xi), max(1e4*rM, 60*xi))
            ob = g["observables"](r, th, rho, xi, "gauss", a0)
            D = 4*math.pi*G*float(np.mean(ob["rho0"][r < 0.02*xi])); ratios[(foot, xi_pc, M)] = (ob["Q2"]/D, pred)
            print(f"  {foot:9s} xi = {xi_pc:5.1f} pc  M = {M/MSUN:.0e} Msun:  Q2/D = {ob['Q2']/D:+.5f}   identity {pred:.5f}   ratio {ob['Q2']/D/pred:.4f}")
vals = np.array([v[0]/v[1] for v in ratios.values()])
check("T1 the ratio Q2/D is independent of xi (0.3-10 pc) and of source mass (1 and 1e-3 Msun) to 0.1% in this machinery -- the identity's structural claim",
      float(np.std(vals)/np.mean(vals)) < 1e-3, f"spread {float(np.std(vals)/np.mean(vals)):.1e}")
check("T2 its value agrees with the closed form 2y/(5[3 lambda - y]) to 3% on both footings (this machinery's own accuracy is ~1-5%)",
      float(np.max(np.abs(vals - 1))) < 0.03, f"max deviation {float(np.max(np.abs(vals - 1)))*100:.2f}%")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
