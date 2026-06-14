#!/usr/bin/env python3
"""
HOSTILE independent re-check of the rar_sparc a0-footing audit.
Fully independent of AUDIT_rar_footing_recheck.py (different loader, different optimizer,
adds BOTH unweighted AND inverse-variance-weighted scatter, and a per-galaxy median metric).

Question 1 (under-audit check): is there a footing the auditor MISSED that inflates a
deficit OR a win? -> scan a grid of (Upsilon_disk, Upsilon_bul, nu) and report optimal a0
+ where 9.36e-11 lands. If the SIGN of the offset flips inside Upsilon in [0.5,0.7], the
"too low" verdict is a convention artifact (FALSE DEFICIT confirmed). If it ALSO flips to a
"win" only at a cherry-picked footing, flag the FALSE WIN.

Question 2 (over-audit check): is the framework a0 actually fine where the red-team said
it was low? -> reproduce the red-team's OWN cell (McGaugh nu, Upsilon=0.5, weighted) and
confirm the offset/penalty.
"""
import glob, os, math
import numpy as np
from scipy.optimize import minimize_scalar

KPC = 3.0856775814913673e19
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
A0_FW = 9.36e-11
A0_CANON = 1.20e-10

def load(ml_d, ml_b, vcut=0.10):
    """Return per-galaxy lists so we can do both pooled and per-galaxy metrics."""
    gals = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        Rm = R*KPC
        vbar2 = np.sign(Vg)*Vg**2 + ml_d*Vd**2 + ml_b*Vb**2
        g_b = vbar2*1e6/Rm; g_o = (Vo*1e3)**2/Rm
        ok = (g_b>0)&(g_o>0)&np.isfinite(g_b)&np.isfinite(g_o)&(Vo>0)&(eV>0)&(eV/Vo<vcut)
        if ok.sum()==0: continue
        # weight ~ 1/(2 dV/V / ln10)^2  (the same dominant term the red-team uses)
        elgo = (2*(eV[ok]/Vo[ok]))/np.log(10)
        gals.append((g_b[ok], g_o[ok], 1.0/elgo**2))
    return gals

def nu_mcgaugh(gb, a0): return gb/(1-np.exp(-np.sqrt(gb/a0)))
def nu_simple(gb, a0):  return gb*(0.5+np.sqrt(0.25+a0/gb))
def nu_dsu(gb, a0):     return np.sqrt(gb**2 + gb*a0)
FORMS = {"McGaugh": nu_mcgaugh, "simple": nu_simple, "dSU": nu_dsu}

def pooled(gals):
    gb=np.concatenate([g[0] for g in gals]); go=np.concatenate([g[1] for g in gals])
    w =np.concatenate([g[2] for g in gals]); return gb,go,w

def scat_unw(gb,go,model,a0):
    r=np.log10(go)-np.log10(model(gb,a0)); r=r-np.median(r)
    return float(np.sqrt(np.mean(r**2)))
def scat_w(gb,go,w,model,a0):
    r=np.log10(go)-np.log10(model(gb,a0))
    off=np.sum(w*r)/np.sum(w); r=r-off
    return float(np.sqrt(np.sum(w*r**2)/np.sum(w)))

def opt(fn_obj):
    res=minimize_scalar(fn_obj,bounds=(math.log10(4e-11),math.log10(3e-10)),
                        method="bounded",options={"xatol":1e-8})
    return 10**res.x,res.fun

print("="*94)
print("HOSTILE independent RAR a0-footing recheck (own loader/optimizer; unweighted + weighted)")
print("="*94)
print(f"  framework a0 = {A0_FW:.4e}   canonical = {A0_CANON:.4e}")

# grid of footings. Include the framework's Ub=1.4*Ud (mlfit) AND McGaugh Ub=0.7 flat.
footings = [
    ("Up=0.50, Ub=0.70 (McGaugh)",      0.50, 0.70),
    ("Up=0.50, Ub=0.70 (mlfit-style)",  0.50, 0.70),
    ("Up=0.60, Ub=0.84 (1.4x)",         0.60, 0.84),
    ("Up=0.70, Ub=0.70 (flat)",         0.70, 0.70),
    ("Up=0.70, Ub=0.98 (1.4x, framework)",0.70, 0.98),
    ("Up=0.80, Ub=1.12 (1.4x)",         0.80, 1.12),
]
for label, ud, ub in footings:
    gals=load(ud,ub); gb,go,w=pooled(gals)
    print(f"\n--- {label}   ({len(gals)} gal, {len(gb)} pts) ---")
    print(f"  {'nu':8}{'opt_a0(unw)':>14}{'off%':>8}{'pen%':>8}   {'opt_a0(wtd)':>14}{'off%':>8}{'pen%':>8}")
    for nm,fn in FORMS.items():
        a0u,su=opt(lambda la: scat_unw(gb,go,fn,10**la)); penu=scat_unw(gb,go,fn,A0_FW)-su
        a0w,sw=opt(lambda la: scat_w(gb,go,w,fn,10**la)); penw=scat_w(gb,go,w,fn,A0_FW)-sw
        print(f"  {nm:8}{a0u:>14.3e}{(A0_FW/a0u-1)*100:>+7.1f}{penu/su*100:>+7.2f}   "
              f"{a0w:>14.3e}{(A0_FW/a0w-1)*100:>+7.1f}{penw/sw*100:>+7.2f}")

# Reproduce the red-team's exact reported cell: McGaugh nu, Up=0.5/Ub=0.7, weighted, free-fit
print("\n"+"="*94)
print("REPRO of red-team cell (McGaugh nu, Up=0.5, Ub=0.7, weighted free-fit):")
gals=load(0.50,0.70); gb,go,w=pooled(gals)
a0w,sw=opt(lambda la: scat_w(gb,go,w,nu_mcgaugh,10**la))
print(f"  free-fit best a0 = {a0w:.3e} (red-team reported 1.145e-10)")
print(f"  framework offset = {(A0_FW/a0w-1)*100:+.1f}%   penalty = {scat_w(gb,go,w,nu_mcgaugh,A0_FW)-sw:+.4f} dex")
print("="*94)

# SIGN-FLIP test: at what Upsilon_disk does the McGaugh-nu optimal a0 cross 9.36e-11?
print("SIGN-FLIP: McGaugh-nu unweighted-optimal a0 vs Upsilon_disk (Ub=1.4*Ud):")
for ud in [0.45,0.50,0.55,0.60,0.65,0.70,0.75]:
    gals=load(ud,1.4*ud); gb,go,w=pooled(gals)
    a0u,_=opt(lambda la: scat_unw(gb,go,nu_mcgaugh,10**la))
    print(f"  Up={ud:.2f}: opt_a0={a0u:.3e}  -> 9.36e-11 is {(A0_FW/a0u-1)*100:+.1f}%  "
          f"{'BELOW(deficit-side)' if a0u>A0_FW else 'ABOVE(win-side)'}")
print("="*94)
