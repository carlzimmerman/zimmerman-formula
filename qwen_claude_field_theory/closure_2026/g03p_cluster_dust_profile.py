#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03p -- the radial profile of the captured scalar dust inside the cluster, from the g03o collapse (N = 400): enclosed dust mass M_d(<r) at |K_2| in the
window (1e5, 3e5, 1e6) against the cold reference in the same well and against the baryons; the residual fraction profile eta_d(r) = M_d(<r)/M_b(<r).
Baryon profile assumption: gas + BCG of M_b(<R500) = 1e14 Msun distributed as M_b(<r) = M_b (r/R500)^1.2 (X-ray-like); the residual the framework needs is
32-46% of a CDM-like halo at R500 (repository standing); the question here is the SHAPE: does the dust sit in the core or the outskirts?"""
import math, sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g03o_dust_spherical_collapse.py")).read()
head = src[:src.index('print("=" * 100)')]
head = head.replace("    return float(np.sum(m[order][bound])/Mshare), float(np.sum(m[order][inner])/Mshare)",
                    "    return dict(rs=rs, rv=rv, E=E, m=m[order], Mshare=Mshare, bound_all=(E < 0) & (rs < R_edge))")
g = {"__file__": os.path.join(HERE, "g03o_dust_spherical_collapse.py")}; exec(compile(head, "g03ohead", "exec"), g)
run, kpc, MSUN = g["run"], g["kpc"], g["MSUN"]
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("=" * 100); print("g03p -- captured dust profile inside the cluster (from the g03o collapse)"); print("=" * 100)
Mb0, R500 = 1e14*MSUN, 1000*kpc; RR = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5])*R500
def enclosed(d):
    b = d["bound_all"]; return np.array([np.sum(d["m"][b & (d["rv"] < r)]) for r in RR])
ref = run(Mb0, R500, 1e30, cs_fixed=0.0, zc=0.3); Mref = enclosed(ref)
print("  r/R500:            " + " ".join(f"{r/R500:6.2f}" for r in RR))
print("  cold reference M_d(<r)/M_b(<R500): " + " ".join(f"{v/Mb0:6.3f}" for v in Mref))
PROF = {}
for K2 in (1e5, 3e5, 1e6):
    d = run(Mb0, R500, K2, zc=0.3); Md = enclosed(d); PROF[K2] = Md
    Mb_r = Mb0*(RR/R500)**1.2
    print(f"  |K_2| = {K2:.0e}: M_d(<r)/M_ref(<r): " + " ".join(f"{(a/b if b > 0 else float('nan')):6.2f}" for a, b in zip(Md, Mref)) + "  |  M_d(<r)/M_b(<r): " + " ".join(f"{a/b:6.2f}" for a, b in zip(Md, Mb_r)), flush=True)
K2c = 3e5; Md = PROF[K2c]; Mb_r = Mb0*(RR/R500)**1.2
inner = Md[1]/max(Mref[1], 1e-30); outer = Md[5]/max(Mref[5], 1e-30)
print(f"\n  at |K_2| = {K2c:.0e}: dust/cold-reference ratio inside 0.2 R500 = {inner:.2f}, inside R500 = {outer:.2f}; dust/baryon ratio at 0.2 R500 = {Md[1]/Mb_r[1]:.2f}, at R500 = {Md[5]/Mb_r[5]:.2f}")
check("P1 the captured dust is CDM-like in the outskirts (ratio to the cold reference within R500 between 0.7 and 2) at |K_2| = 3e5", 0.7 <= outer <= 2.0, f"{outer:.2f}")
check("P2 the dust is relatively depleted in the core (ratio to the cold reference inside 0.2 R500 below the ratio inside R500): the stiffness rises inward with the field, so the residual the theory supplies is outskirts-weighted", inner < outer, f"core {inner:.2f} vs R500 {outer:.2f}")
check("P3 the dust-to-baryon ratio at R500 lies in 0.3-3 for some |K_2| in the window (the residual scale the framework needs, 32-46% of a CDM-like halo, is of order the baryons at R500)", any(0.3 <= PROF[K][5]/Mb_r[5] <= 3 for K in PROF), f"{[round(PROF[K][5]/Mb_r[5], 2) for K in PROF]}")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
