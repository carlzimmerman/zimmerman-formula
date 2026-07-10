#!/usr/bin/env python3
"""Where is the Cassini ell=2 (1/R^3-weighted interior moment) actually sourced, and what is
mu_s/K_t there? This explains w. Prints the radial distribution of the Q2 integrand and the local
shear/bulk stiffness ratio, plus the cumulative fraction of Q2 vs radius and the shell-resolved w."""
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve
import importlib.util
spec=importlib.util.spec_from_file_location("mb","/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/bc6058d7-6ce0-4f8c-8635-25bfd772ff6d/scratchpad/vector_elastic_w/methodB_fem.py")
mb=importlib.util.module_from_spec(spec); spec.loader.exec_module(mb)
G=mb.G;Msun=mb.Msun;AU=mb.AU;Z=mb.Z
a0=9.36e-11; gx=2.2; Keff=a0**2/(16*np.pi*G)
NR,NT=900,1200
r=np.logspace(np.log10(5*AU),np.log10(5e5*AU),NR); th=np.linspace(1e-4,np.pi-1e-4,NT)
c=np.cos(th);s=np.sin(th);P2=0.5*(3*c**2-1);wsin=s*np.gradient(th)
rho_ph=mb.rho_phantom(a0,gx,r,th)
rho_ph2=np.sum(rho_ph*P2[None,:]*wsin[None,:],axis=1)     # ell=2 moment(r)
y0=(G*Msun/r**2)/a0
S=np.array([mb.S_of(v) for v in y0])
Kt=Keff*S
# Q2 interior integrand ~ (1/r) rho_ph2 (from project: 2pi sum (1/r)dr Jr G_pp, Jr~rho_ph2/G_pp)
integ=np.abs(rho_ph2)/r
dr=np.gradient(r); cum=np.cumsum(integ*dr); cum/=cum[-1]
r_t=np.sqrt(2*G*Msun/(Z*a0*1.0))    # where eps_M=1 (2GM/(a0V r^2)=1)
print(f"r_t (eps_M=1, saturation) = {r_t/AU:.0f} AU ; mask=5 AU")
print(f"{'r[AU]':>10} {'y0=gSun/a0':>11} {'S(y0)':>9} {'mu_s/K_t(b=2)':>12} {'Q2integ(norm)':>13} {'cumQ2':>7}")
imax=np.argmax(integ)
for frac in (0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.99):
    i=np.searchsorted(cum,frac)
    i=min(i,NR-1)
    print(f"{r[i]/AU:>10.1f} {y0[i]:>11.2e} {S[i]:>9.2e} {6.0/S[i]:>12.2e} {integ[i]/integ[imax]:>13.3f} {cum[i]:>7.2f}")
print(f"\n peak of Q2 integrand at r={r[imax]/AU:.0f} AU: y0={y0[imax]:.3e}, S={S[imax]:.3e}, mu_s/K_t(b=2)={6/S[imax]:.3e}")
# median radius of Q2
imed=np.searchsorted(cum,0.5)
print(f" MEDIAN Q2 radius = {r[imed]/AU:.0f} AU (S={S[imed]:.2e}, mu_s/K_t={6/S[imed]:.2e} at beta=2)")
print(f" fraction of Q2 sourced INSIDE r_t (saturated/stiff, w~1): {cum[np.searchsorted(r,r_t)]:.3f}")
print(f" fraction sourced OUTSIDE 10x r_t (soft, w<1): {1-cum[np.searchsorted(r,10*r_t)]:.3f}")

# robustness: recompute w with CONSTANT K_t = K_eff*S(g_ext/a0)  (shell-value footing)
print("\n[robustness] w with radial K_t vs constant shell-value K_t=K_eff*S(2.2):")
for lab,radial in (("radial K_t(r)",True),("const K_t=K_eff S(2.2)",False)):
    out,sc=mb.solve_modal(a0,gx,[0.0,0.33,0.95,2.0],radial_Kt=radial)
    ws=[out[b]/out[0.0] for b in (0.33,0.95,2.0)]
    print(f"   {lab:26s}: w(0.33)={ws[0]:.3f} w(0.95)={ws[1]:.3f} w(2.0)={ws[2]:.3f}   S(2.2)={mb.S_of(2.2):.3f}")
print("exit 0")
