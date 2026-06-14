#!/usr/bin/env python3
"""
AUDIT cross-check (rar_sparc front): re-state the RAR a0 verdict on the framework's
OWN footing and compare to the footing each Fable script actually used.

The candidate FALSE DEFICIT: real_research/reviews/redteam_rar_framework_a0.py VERDICT
says framework a0 is "~22% LOW vs canonical / 18% below the data's free-fit best / at the
low edge of the allowed band". That free-fit + zero-param test is computed at McGaugh
M/L (Upsilon_disk=0.5). The framework's OWN footing is Upsilon~0.70 + its dS-Unruh
interpolation g_obs=sqrt(g_bar^2 + g_bar a0).

This script re-derives, on the real 175 SPARC curves, the UNWEIGHTED-dex-optimal a0 at
each (interpolation x Upsilon) cell, and reports where 9.36e-11 lands. Both ways.
No synthetic data. Points to the REAL data dir explicitly.
"""
import glob, os, math
import numpy as np
from scipy.optimize import minimize_scalar

KPC = 3.0856775814913673e19
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
A0_FW = 9.36e-11          # framework: c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)
A0_CANON = 1.20e-10       # McGaugh canonical

def load(ml_d, ml_b):
    gb, go = [], []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        Rm = R*KPC
        vbar2 = np.sign(Vg)*Vg**2 + ml_d*Vd**2 + ml_b*Vb**2
        g_b = vbar2*1e6/Rm; g_o = (Vo*1e3)**2/Rm
        ok = (g_b>0)&(g_o>0)&np.isfinite(g_b)&np.isfinite(g_o)&(Vo>0)&(eV>0)&(eV/Vo<0.10)
        gb += list(g_b[ok]); go += list(g_o[ok])
    return np.array(gb), np.array(go)

# interpolations
def nu_mcgaugh(gb, a0): return gb/(1-np.exp(-np.sqrt(gb/a0)))
def nu_simple(gb, a0):  return gb*(0.5+np.sqrt(0.25+a0/gb))
def nu_dsu(gb, a0):     return np.sqrt(gb**2 + gb*a0)   # framework dS-Unruh shape
FORMS = {"McGaugh": nu_mcgaugh, "simple": nu_simple, "dSU(framework)": nu_dsu}

def dex(gb, go, model, a0):
    r = np.log10(go) - np.log10(model(gb, a0))
    return float(np.sqrt(np.mean(r**2)))

def opt(gb, go, model):
    f = lambda la: dex(gb, go, model, 10**la)
    res = minimize_scalar(f, bounds=(math.log10(5e-11), math.log10(3e-10)),
                          method="bounded", options={"xatol":1e-7})
    return 10**res.x, res.fun

print("="*86)
print("RAR a0 footing recheck on the REAL 175 SPARC curves (unweighted dex scatter)")
print("="*86)
print(f"  framework a0 = {A0_FW:.3e}   canonical = {A0_CANON:.3e}")
for ml in [0.50, 0.70]:
    gb, go = load(ml, ml if ml==0.70 else 0.70)
    print(f"\n--- Upsilon_disk = {ml:.2f}  ({'McGaugh footing' if ml==0.5 else 'FRAMEWORK footing'}),  "
          f"{len(gb)} points ---")
    print(f"  {'interpolation':18}{'optimal a0':>14}{'9.36e-11 offset':>18}{'penalty(dex)':>14}{'penalty%':>10}")
    for nm, fn in FORMS.items():
        a0o, so = opt(gb, go, fn)
        sfw = dex(gb, go, fn, A0_FW)
        off = (A0_FW/a0o - 1)*100
        pen = sfw - so
        print(f"  {nm:18}{a0o:>14.3e}{off:>+17.1f}%{pen:>+14.4f}{pen/so*100:>+9.2f}%")
print("="*86)
print("READ: the red-team verdict ('~22% low / low edge of band') is the McGaugh-nu +")
print("Upsilon=0.5 cell. On the framework's own footing (dSU nu + Upsilon=0.70) read the")
print("dSU(framework) row at Upsilon=0.70 -- that is the framework-footing offset+penalty.")
print("="*86)
