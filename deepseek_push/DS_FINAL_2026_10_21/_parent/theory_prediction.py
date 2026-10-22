#!/usr/bin/env python3
"""End-to-end prediction from the theory's postulates — zero free parameters.

Postulates used (nothing else):
  P1  a0 = kappa c sqrt(G rho_bare), kappa = 1/2, rho_bare = rho_DE/Omega_Lambda
      -> a0 = 1.132e-10 m/s^2   (A33's background constraint; NOT fitted to galaxies)
  P2  the law  g_N = g^2/(g + a0)   (the frozen S2 rest state; A2/A35 Langmuir)
  P3  lensing = dynamics (A12/A3); irrelevant for a rotation curve but stated
  P4  the cold sector sources the law's phantom; no extra mass is added by hand
  P5  L* = 24 pc, so the elastic core is confined to r < ~50 pc and does not
      touch any SPARC datum (r_first >= 80 pc)

So the rotation curve of a galaxy is FULLY PREDICTED once its baryonic
components are given: there is no fit parameter except the stellar M/L, which
is a property of the stars, not of the theory. We report both a fixed-M/L
(zero-parameter) prediction and a one-parameter fit, and the same for the
rival n=2 law, on the same data.

Data: real_research/data/sparc_data/*_rotmod.dat (columns Rad, Vobs, errV,
Vgas, Vdisk, Vbul, SBdisk, SBbul).

Run: python3 theory_prediction.py [--mutate]
"""
import sys
import glob
import os
import numpy as np

MUTATE = "--mutate" in sys.argv
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"

c = 2.99792458e8
G = 6.67430e-11
KPC = 3.0856775814913673e19
A0 = 1.132e-10          # P1: the theory's own footing (A33), NOT fitted
A0_CAN = 9.36e-11       # the observed-vacuum reading, for comparison
FLOOR = 0.05

res = []


def check(cid, ok, val, thr, note=""):
    ok = bool(ok)
    res.append(ok)
    print(f"{cid} {'PASS' if ok else 'FAIL'} measured={val} threshold={thr} {note}")


def load(name):
    p = os.path.join(DATA, name + "_rotmod.dat")
    d = np.loadtxt(p, comments="#")
    return dict(r=d[:, 0] * KPC, Vobs=d[:, 1], eV=d[:, 2],
                Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5])


def law_canon(gN, a0):
    return 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / np.maximum(gN, 1e-30)))


def law_n2(gN, a0):
    return np.sqrt(gN**2 + a0 * gN)


def chi2(g, d, ups):
    Vb2 = d["Vg"]**2 + ups * (d["Vd"]**2 + d["Vb"]**2)
    gN = Vb2 * 1e6 / d["r"]
    gp = g(gN, A0)
    Vp = np.sqrt(gp * d["r"]) / 1e3
    s = np.sqrt(d["eV"]**2 + (FLOOR * d["Vobs"])**2)
    return float(np.sum(((d["Vobs"] - Vp) / s) ** 2)), Vp, gN


def scan(d, g):
    us = np.linspace(0.05, 2.5, 500)
    cs = [chi2(g, d, u)[0] for u in us]
    i = int(np.argmin(cs))
    return us[i], cs[i]


# ------------------------------------------------------------------ galaxies
names = ["NGC3198", "NGC2403", "UGC02885", "NGC7331", "UGC01281"]
rows = []
for nm in names:
    d = load(nm)
    if MUTATE:
        d["Vd"] = d["Vd"] * 0  # sabotage: drop the disk
    c1_fix, Vp1, gN = chi2(law_canon, d, 0.5)
    c2_fix, Vp2, _ = chi2(law_n2, d, 0.5)
    u1, c1 = scan(d, law_canon)
    u2, c2 = scan(d, law_n2)
    n = len(d["r"])
    rows.append(dict(gal=nm, n=n, chi2_canon_fix=c1_fix, chi2_n2_fix=c2_fix,
                     chi2_canon_fit=c1, chi2_n2_fit=c2, ups1=u1, ups2=u2,
                     dof=n - 1))
    print(f"{nm:10s} N={n:3d}  U=0.5: canon {c1_fix:8.2f}  n2 {c2_fix:8.2f}   "
          f"free U: canon {c1:8.2f} (U={u1:.2f})  n2 {c2:8.2f} (U={u2:.2f})")

tot1 = sum(r["chi2_canon_fix"] for r in rows)
tot2 = sum(r["chi2_n2_fix"] for r in rows)
totdof = sum(r["dof"] for r in rows)
print(f"\nFIXED U=0.5 (ZERO free parameters beyond the theory):")
print(f"  canonical chi2 = {tot1:.1f} / {totdof} dof = {tot1/totdof:.2f}")
print(f"  n=2       chi2 = {tot2:.1f} / {totdof} dof = {tot2/totdof:.2f}")

totf1 = sum(r["chi2_canon_fit"] - 1 for r in rows)
totf2 = sum(r["chi2_n2_fit"] - 1 for r in rows)
dof_f = totdof - len(rows)
print(f"ONE U per galaxy:")
print(f"  canonical chi2 = {totf1:.1f} / {dof_f} = {totf1/dof_f:.2f}")
print(f"  n=2       chi2 = {totf2:.1f} / {dof_f} = {totf2/dof_f:.2f}")

check("K1", tot1 / totdof < 3.0, round(tot1 / totdof, 2), "< 3",
      "zero-parameter canonical prediction is not catastrophic on 5 galaxies")
check("K2", totf1 / dof_f < 1.5, round(totf1 / dof_f, 2), "< 1.5",
      "with one M/L per galaxy the canonical law describes the data")
check("K3", totf1 < totf2, round(totf1 - totf2, 1), "> 0",
      "canonical beats n=2 at equal freedom on this subset")

# --------------------------------------------- the footing comparison (P1)
d = load("NGC3198")
u, c_theory = scan(d, law_canon)
c_can = chi2(law_canon, d, u)[0]
# refit with a0 = canonical value, same U
def chi2_a0(g, d, ups, a0):
    Vb2 = d["Vg"]**2 + ups * (d["Vd"]**2 + d["Vb"]**2)
    gN = Vb2 * 1e6 / d["r"]
    gp = g(gN, a0)
    Vp = np.sqrt(gp * d["r"]) / 1e3
    s = np.sqrt(d["eV"]**2 + (FLOOR * d["Vobs"])**2)
    return float(np.sum(((d["Vobs"] - Vp) / s) ** 2))

best = None
for a0 in np.linspace(0.7e-10, 1.6e-10, 400):
    cb = chi2_a0(law_canon, d, u, a0)
    if best is None or cb < best[1]:
        best = (a0, cb)
print(f"\nNGC3198, U={u:.2f} fixed, a0 free: best a0 = {best[0]:.3e} (chi2 {best[1]:.1f})")
print(f"  theory's footing P1  a0 = {A0:.3e} -> chi2 {chi2_a0(law_canon, d, u, A0):.1f}")
print(f"  observed-vacuum     a0 = {A0_CAN:.3e} -> chi2 {chi2_a0(law_canon, d, u, A0_CAN):.1f}")
check("K4", abs(best[0] - A0) / A0 < 0.25, f"{best[0]:.3e}", "within 25% of 1.132e-10",
      "the a0 the data prefer on this galaxy is near the footing the action forces (P1)")

n = sum(res)
print(f"\nTHEORY-PREDICTION {'COMPLETE' if n == len(res) else 'INCOMPLETE'}: {n}/{len(res)}")
sys.exit(0 if n == len(res) else 1)
