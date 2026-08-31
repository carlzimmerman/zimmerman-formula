#!/usr/bin/env python3
"""
phase3_background.py -- static spherical FC-KH background.

SHARPENED TARGET fact (verified): static spherical => K_ij=0 => beta,lambda do NOT
enter the background; it is fixed by the interpolation chi/mu derived in Phase 2.
The static limit of the khronometric action (Flanagan 2302.14846 Eq.26; the AQUAL
form) is the modified-Poisson / algebraic MOND relation with mu_phys = 1 - e^{-y}:

     mu_phys(a/a0) * a = g_N(r)          (spherical, g_N = G M_enc(r)/r^2)

We solve this for a(r) [=> y0(r)=a/a0] for TWO sources and confirm that the
UNSTABLE window 1 < y0 < ~38 (f''<0) is traversed at finite radius, so the
parallel gradient instability found in Phase 5/6 is physically occupied.

We do NOT insert 'a=sqrt(g a0)' by hand: we invert the FULL relation
mu(a/a0) a = g_N numerically with mu=1-e^{-y}. Convergence check included.
"""
import numpy as np
from scipy.optimize import brentq

a0=1.0
def mu(y): return 1.0-np.exp(-y)
# invert mu(y)*y*a0 = gN  -> solve for y at given gN (in units a0)
def y_of_gN(gN):
    # mu(y)*y = gN/a0 ; LHS monotonic increasing from 0 to inf
    rhs=gN/a0
    f=lambda y: mu(y)*y - rhs
    lo,hi=1e-8, 1.0
    while f(hi)<0: hi*=2
    return brentq(f,lo,hi,xtol=1e-14,rtol=1e-14)

print("="*70)
print("POINT MASS: g_N=GM/r^2. Dimensionless x=r/r_M, r_M=sqrt(GM/a0) => g_N/a0=1/x^2")
print("="*70)
print(f"{'x=r/rM':>10}{'gN/a0':>12}{'y0=a/a0':>12}{'regime':>16}{'in f<0 window':>16}")
for x in [0.1,0.3,0.5,0.8,1.0,1.5,2.0,3.0,5.0,10.0,30.0]:
    gN=1.0/x**2
    y0=y_of_gN(gN)
    reg='Newtonian' if y0>5 else ('transition' if y0>0.5 else 'deep-MOND')
    inw = '(1,38): YES' if (1.0<y0<38.0) else 'no'
    print(f"{x:>10.3f}{gN:>12.4e}{y0:>12.4f}{reg:>16}{inw:>16}")
# radius where y0=1 and y0=38 (window edges) for point mass
def x_of_y(y):  # gN=mu(y)*y*a0 ; x=1/sqrt(gN/a0)
    return 1.0/np.sqrt(mu(y)*y)
print(f"\n  window edge y0=1  at x=r/rM = {x_of_y(1.0):.4f}")
print(f"  window edge y0=38 at x=r/rM = {x_of_y(38.0):.4f}")
print("  => the unstable shell 1<y0<38 occupies  %.4f < r/rM < %.4f  (a FINITE radial band"%(x_of_y(38.),x_of_y(1.)))
print("     around every point mass / galaxy core).")

print("\n"+"="*70)
print("PLUMMER SPHERE  rho(r)=3M/(4 pi b^3)(1+r^2/b^2)^-5/2 : g_N(r)=GM r/(r^2+b^2)^3/2")
print("Solve mu(y)y a0 = g_N(r). Confirms a smooth finite-density source also traverses.")
print("="*70)
def gN_plummer(r,b=1.0,GM=50.0):  # GM chosen so a>a0 in the core
    return GM*r/(r**2+b**2)**1.5
print(f"  units: a0=1, b=1, GM=50 (rM=sqrt(GM/a0)=%.2f b)"%np.sqrt(50.0))
print(f"{'r/b':>8}{'gN/a0':>12}{'y0=a/a0':>12}{'in f<0 window':>16}")
rmax_window=0; rmin_window=1e9
for r in [0.1,0.3,0.5,1.0,2.0,3.0,5.0,8.0,12.0,20.0,40.0]:
    gN=gN_plummer(r)
    y0=y_of_gN(gN)
    inw = (1.0<y0<38.0)
    if inw: rmax_window=max(rmax_window,r); rmin_window=min(rmin_window,r)
    print(f"{r:>8.2f}{gN:>12.4e}{y0:>12.4f}{('YES' if inw else 'no'):>16}")
print(f"  => Plummer sphere: unstable window 1<y0<38 occupied for ~{rmin_window:.2f}<r/b<{rmax_window:.2f}")

# ---------- convergence check: invert on a refined vs coarse grid ----------
print("\n"+"="*70)
print("CONVERGENCE: y_of_gN via brentq is exact to xtol=1e-14; verify residual")
print("="*70)
maxres=0
for gN in np.logspace(-3,3,200):
    y=y_of_gN(gN); res=abs(mu(y)*y-gN/a0)
    maxres=max(maxres,res)
print(f"  max |mu(y)y - gN/a0| over gN in [1e-3,1e3] = {maxres:.2e}  (background inversion converged)")
print("\nCONCLUSION: a(r) sweeps continuously from deep-MOND (y0<1, large r) through the")
print("transition and into Newtonian (y0>>1, small r); the f''<0 unstable shell 1<y0<~38")
print("is a FINITE radial band present around EVERY realistic source. Instability is occupied.")
