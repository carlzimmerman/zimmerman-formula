"""cm01: can the cold mass be 'expelled where MOND is active', i.e. can its retained fraction be ANY function f(y) of the local MOND activity y = g_bar/a0?
Record anchors (ledger, fable_independent_2026 L166/L172; KiDS X3): spirals tolerate f <= 0.105 over their rotation curves; clusters need f = 0.58 inside R500.
Test: compare y at the SPARC rotation-curve edge (last measured point, Upsilon_disk 0.5, Upsilon_bul 0.7, Q <= 2) with y at cluster R500.
Cluster inputs (literature-level, PROVISIONAL, X-COP-like): M500 = 3e14 .. 1e15 Msun, baryon fraction at R500 0.13 .. 0.16, R500 from 500 rho_crit (h = 0.7).
Logic: if spirals sit at the SAME y as cluster R500, a gate f(y) must give <= 0.105 and >= 0.58 at that y -- impossible for any function of y alone.
Checks: O count of SPARC galaxies whose edge-y lies inside the cluster R500 y-range (reported; the no-go needs >= 10);
  N the no-go holds on both footings (a0 = 9.36e-11 and 1.13e-10) -- y ratios are footing-independent, so this is a consistency check.
Run: python3 cm01_mond_activity_gate.py | MUTATE=1 multiplies cluster baryon masses by 100 (pushes clusters out of the spiral range -> O must fail)
"""
import os, sys, math, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "puzzle_32pi", "agents", "V_evidence_for_the_coefficient"))
from v_common import load_sparc
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
G, Msun, Mpc = 6.674e-11, 1.989e30, 3.0857e22
rho_c = 3 * (70e3 / Mpc)**2 / (8 * math.pi * G)
gals = [g for g in load_sparc() if g.get("Q") is not None and g["Q"] <= 2]
def ybar_edge(g, a0):
    R = g["Rm"][-1]; vb2 = (g["Vgas"][-1] * abs(g["Vgas"][-1]) + 0.5 * g["Vdisk"][-1]**2 + 0.7 * g["Vbul"][-1]**2) * 1e6
    return max(vb2, 1e-30) / R / a0
ok_all = True
for a0 in (9.3603e-11, 1.1312e-10):
    ys = np.array([ybar_edge(g, a0) for g in gals])
    yc = []
    for M500 in (3e14, 1e15):
        for fb in (0.13, 0.16):
            Mb = fb * M500 * Msun * (100 if MUTATE else 1)
            R500 = (3 * M500 * Msun / (4 * math.pi * 500 * rho_c))**(1 / 3)
            yc.append(G * Mb / R500**2 / a0)
    lo, hi = min(yc), max(yc)
    inside = int(np.sum((ys >= lo) & (ys <= hi)))
    print(f"   a0 = {a0:.3e}: SPARC edge y (N = {len(ys)}) 16/50/84% = {np.percentile(ys,16):.3f}/{np.median(ys):.3f}/{np.percentile(ys,84):.3f};"
          f" cluster R500 y = {lo:.3f} .. {hi:.3f}; SPARC galaxies inside that range: {inside}")
    ok_all &= inside >= 10
check("O >= 10 SPARC galaxies sit at the same MOND activity y as cluster R500 on both footings (spirals need f <= 0.105 there, clusters f = 0.58)", ok_all)
print("   => no function f(y) of local MOND activity can expel the cold mass from spirals while keeping 58% in clusters" if ok_all else "   => the ranges separate; a y-gate is not excluded by this test")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
