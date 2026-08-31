#!/usr/bin/env python3
"""
phase5_numeric_dispersion.py

Numerically map the FULL reduced khronon dispersion
    omega^2(kx,kz; y0,beta,lambda) = V(kx,kz) / A
from the decisive reduction (decisive_reduction.py), using the PHYSICAL f_FC:
    W0=F(y0), W1=F'(y0), W2=F''(y0),  F=f_FC/a0^2,  alpha=2 beta.

Goal: determine WHERE (which k) any instability lives -- IR(k->0, super-horizon),
sub-horizon physical band (a0 << k << M_*), or true UV(k->inf) -- and whether the
parallel-mode negativity (sign = sign f'') sits in the PHYSICAL band.

Two independent numerical routes are cross-checked:
  route (I)  : V/A from the Hermitian Schur-complement reduction (this mission).
  route (II) : omega^2 = -D0/D1 from the EL-determinant route in the pre-existing
               wf_adm_scalar_reduction.py (adm_mond.pkl), with beta_script=-beta.
"""
import numpy as np, sympy as sp, pickle, os

# ---------- physical f_FC data ----------
def Wp_prim(y): return 0.5*y*y + (1+y)*np.exp(-y) - 1.0     # W(y) primitive
def F(y,al):    return 2*y*y - 2*(2-al)*Wp_prim(y)          # = f_FC/a0^2
def F1(y,al):   return 2*y*(al + (2-al)*np.exp(-y))          # F'(y)
def F2(y,al):   return 2*al + 2*(2-al)*(1-y)*np.exp(-y)      # F''(y) = f''

def Wdata(y0, beta):
    al = 2*beta
    return F(y0,al), F1(y0,al), F2(y0,al)

# ---------- route (I): V/A closed form (transcribed from decisive_reduction.out) ----------
def A_kin(beta,lam):
    return (1-beta)*(2+beta+3*lam)/(beta+lam)

def num_V(kx,kz,W0,W1,W2,y0,a0):
    return (-W0*W1*a0**4*y0**2 - 9*W0*W1*a0**2*kx**2 - W0*W2*a0**4*y0**3
            - 9*W0*W2*a0**2*kz**2*y0 + 20*W0*a0**2*kx**2*y0 + 20*W0*a0**2*kz**2*y0
            + W1**2*a0**4*y0**3 + 5*W1**2*a0**2*kx**2*y0 + 4*W1**2*a0**2*kz**2*y0
            - W1*W2*a0**2*kx**2*y0**2 + W1*W2*a0**2*kz**2*y0**2
            - 8*W1*a0**2*kx**2*y0**2 - 8*W1*a0**2*kz**2*y0**2
            - 4*W1*kx**4 - 4*W1*kx**2*kz**2 - 4*W2*kx**2*kz**2*y0 - 4*W2*kz**4*y0
            + 16*kx**4*y0 + 32*kx**2*kz**2*y0 + 16*kz**4*y0)

def den_V(kx,kz,W0,W1,W2,y0,a0):
    return 4*(W0*a0**2*y0 + W1*kx**2 + W2*kz**2*y0)

def omega2_I(kx,kz,y0,beta,lam,a0=1.0):
    W0,W1,W2 = Wdata(y0,beta)
    return num_V(kx,kz,W0,W1,W2,y0,a0)/(A_kin(beta,lam)*den_V(kx,kz,W0,W1,W2,y0,a0))

# ---------- route (II): reload EL-determinant dispersion, beta_script = -beta ----------
def route_II_lambdified():
    p = os.path.join(os.path.dirname(__file__),'..','khronometric_mond','adm_mond.pkl')
    d = pickle.load(open(p,'rb'))
    w2sol = sp.sympify(d['w2sol'])   # srepr string -> expr
    lam_ok = sp.Symbol('lam_ok')
    for sym in list(w2sol.free_symbols):     # rename any symbol literally named 'lambda'
        if sym.name == 'lambda':
            w2sol = w2sol.subs(sym, lam_ok)
    smap = {s.name: s for s in w2sol.free_symbols}
    beta_s = smap.get('beta', sp.Symbol('beta'))
    a0_s   = smap.get('a0',   sp.Symbol('a0'))
    y0_s   = smap.get('y0',   sp.Symbol('y0'))
    W0_s   = smap.get('W0',   sp.Symbol('W0'))
    W1_s   = smap.get('W1',   sp.Symbol('W1'))
    W2_s   = smap.get('W2',   sp.Symbol('W2'))
    kx_s   = smap.get('k_x',  sp.Symbol('k_x'))
    kz_s   = smap.get('k_z',  sp.Symbol('k_z'))
    return sp.lambdify((kx_s,kz_s,y0_s,beta_s,lam_ok,a0_s,W0_s,W1_s,W2_s), w2sol,'numpy')

print("="*78)
print("CROSS-CHECK route (I) V/A  vs  route (II) -D0/D1 (EL-det, beta_script=-beta)")
print("="*78)
try:
    fII = route_II_lambdified()
    for (kx,kz,y0,beta,lam) in [(0.3,0.0,2.0,1e-15,1e-3),(0.0,0.7,2.0,1e-15,1e-3),
                                (1.0,1.0,0.5,1e-14,1e-2),(2.0,0.0,5.0,1e-16,1e-4)]:
        W0,W1,W2 = Wdata(y0,beta)
        oI = omega2_I(kx,kz,y0,beta,lam)
        # route II script used (1+beta_s)K^2 ; beta_script=-beta:
        oII = fII(kx,kz,y0,-beta,lam,1.0,W0,W1,W2)
        print(f"  kx={kx} kz={kz} y0={y0} beta={beta:.0e} lam={lam:.0e}: "
              f"omega2_I={oI:+.6e}  omega2_II={oII:+.6e}  rel.diff={abs(oI-oII)/(abs(oI)+1e-30):.2e}")
except Exception as e:
    print("  route II cross-check unavailable:", repr(e))

# ---------- FULL dispersion sweep in k, parallel and perpendicular ----------
print("\n"+"="*78)
print("FULL DISPERSION omega^2/k^2 vs k  (a0=1; physical band is k >> a0=1, i.e. k>~1)")
print("beta=1e-15, lambda=1e-3, alpha=2beta  (benchmark P1)")
print("="*78)
beta,lam = 1e-15,1e-3
kgrid = np.concatenate([np.logspace(-3,-0.001,60), np.logspace(0,6,120)])
for y0 in [0.5,1.0,1.5,2.0,3.0,5.0,10.0]:
    W0,W1,W2 = Wdata(y0,beta)
    # parallel (kx=0): omega^2/kz^2
    o2par = np.array([omega2_I(0.0,kz,y0,beta,lam) for kz in kgrid])/kgrid**2
    o2perp= np.array([omega2_I(kx,0.0,y0,beta,lam) for kx in kgrid])/kgrid**2
    # find sign in physical band k>=1
    phys = kgrid>=1.0
    par_phys_min = o2par[phys].min(); par_phys_max=o2par[phys].max()
    perp_phys_min= o2perp[phys].min()
    # locate any pole (den zero) parallel: kz^2 = -W0/W2 (a0=1)
    pole = np.sqrt(-W0/W2) if W2<0 else np.nan
    print(f"\n y0={y0:5.2f}  W0(F)={W0:+.4f} W1(F')={W1:+.4f} W2(f'')={W2:+.4f}  pole_kz(par)={pole if not np.isnan(pole) else 'none'}")
    print(f"   c_par^2  physical-band (k>=1): min={par_phys_min:+.4e} max={par_phys_max:+.4e}  "
          f"{'UNSTABLE(par)' if par_phys_min<0 else 'ok'}")
    print(f"   c_perp^2 physical-band (k>=1): min={perp_phys_min:+.4e}  {'UNSTABLE(perp)' if perp_phys_min<0 else 'ok'}")
    # clean deep-physical-band values, well ABOVE any super-horizon pole (k>>a0=1)
    for kk in [1e2,1e3,1e4,1e6]:
        cp = omega2_I(0.0,kk,y0,beta,lam)/kk**2
        cq = omega2_I(kk,0.0,y0,beta,lam)/kk**2
        print(f"     k={kk:8.0e}:  c_par^2={cp:+.4e}  c_perp^2={cq:+.4e}")
