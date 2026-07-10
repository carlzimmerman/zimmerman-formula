#!/usr/bin/env python3
"""
ADVERSARIAL RE-DERIVATION of the lane-A load-bearing number: |Q2|(chi=1) for the named
Branch-B survivor (p=1.75, y_t=0.5, n=4, canonical a0), via a route INDEPENDENT of the
Milgrom-2009/Desmond-2024 (v, xi) integral used by laneA_family_scan.py.

Route here: phantom-density multipole in real space.
  rho_ph = (1/4 pi G) div[ F(|g_N|/a0) g_N ],   g_N = -(GM/r^2) rhat + gNe zhat,
  gNe = e_N a0,  e_N solves e_N (1 + F(e_N)) = g_ext/a0  (Newtonian-equivalent ext field).
  delta Phi l=2 interior coefficient:  Q2 = 3 G Int rho_ph P2(cos th) / r^3 dV
  (from delta Phi = -(Q2/3) r^2 P2 and the interior multipole expansion of -G Int rho/|x-x'|).
Integrate by parts (divergence theorem on r_min < r < R):
  Q2 = B(R) - B(r_min) - (3/2) Int dr dth  F(y) [3 P2 GM/r^2 - 3 gNe cos th (P2 - sin^2 th)]
                                             * sin th / r^2
  B(r) = (3/2)(1/r) Int F g_r P2 sin th dth,   g_r = -GM/r^2 + gNe cos th.
Checks: (a) reproduce the simple-nu AQUAL class baseline 4.78e-26 (repo aest_cassini_
quadrupole_full.py validation + Hees-class ~4e-26); (b) framework-nu-as-source 1.96e-26;
(c) the named survivor 1.41e-26 and its SIGN; (d) r_min / resolution / R convergence.
numpy only.
"""
import numpy as np
from scipy.optimize import brentq

c=2.99792458e8; G=6.674e-11; Msun=1.989e30; AU=1.495978707e11
GM=G*Msun
Z=np.sqrt(32*np.pi/3.0); A_DEEP=np.sqrt(Z/6.0)
A0_CANON=9.36e-11; A0_OBS=1.2e-10
Q2_CEIL=5.2e-27

def F_member(y, p=1.75, yt=0.5, n=4):
    return A_DEEP*y**(-0.5)*(1.0+(y/yt)**n)**(-(p-0.5)/n)

def F_simple(y):   # nu_simple - 1
    return 0.5*np.sqrt(1.0+4.0/y)-0.5+0.0*y  # 0.5+sqrt(0.25+1/y)-1

def F_fw(y):       # framework nu - 1
    return np.sqrt(1.0+1.0/y)-1.0

def solve_eN(Ffun, etilde):
    return brentq(lambda e: e*(1.0+Ffun(e))-etilde, 1e-9, 10*etilde, xtol=1e-15, rtol=1e-13)

def Q2_realspace(Ffun, a0, gext, nr=6000, nth=3000, rmin_AU=0.5, R_out_factor=3e3,
                 inner_boundary=True):
    etilde=gext/a0
    eN=solve_eN(Ffun, etilde)
    gNe=eN*a0
    rstar=np.sqrt(GM/gNe)                       # cancellation radius
    rmin=rmin_AU*AU; R=R_out_factor*rstar
    r=np.geomspace(rmin, R, nr)                 # (nr,)
    th=np.linspace(0.0, np.pi, nth)             # (nth,)
    ct=np.cos(th); st=np.sin(th)
    P2=0.5*(3*ct**2-1.0)
    rr=r[:,None]; ctb=ct[None,:]; stb=st[None,:]; P2b=P2[None,:]
    g_r=-GM/rr**2+gNe*ctb
    g_t=-gNe*stb
    gmag=np.sqrt(g_r**2+g_t**2)
    y=np.maximum(gmag/a0, 1e-300)
    Fv=Ffun(y)
    # volume integrand (after the -(3/2) prefactor): see docstring
    kern=Fv*(3.0*P2b*GM/rr**2 - 3.0*gNe*ctb*(P2b-stb**2))*stb/rr**2
    inner_th=np.trapz(kern, th, axis=1)
    vol=-1.5*np.trapz(inner_th, r)
    # boundary terms
    def B(ri):
        g_rb=-GM/ri**2+gNe*ct
        yb=np.maximum(np.sqrt(g_rb**2+(gNe*st)**2)/a0,1e-300)
        return 1.5/ri*np.trapz(Ffun(yb)*g_rb*P2*st, th)
    bt=B(R)-(B(rmin) if inner_boundary else 0.0)
    return vol+bt, eN, rstar/AU, dict(vol=vol, bR=B(R), brmin=B(rmin))

print("="*96)
print(" INDEPENDENT real-space phantom-density Q2 (adversarial check of laneA)")
print("="*96)

# (a) simple-nu AQUAL baseline: laneA V5 / repo baseline = +4.78e-26 (a0=1.2e-10, gext=2.32e-10)
for nr,nth,rmin in [(3000,1500,0.5),(6000,3000,0.5),(6000,3000,0.05),(12000,6000,0.5)]:
    Q2,eN,rs,parts=Q2_realspace(F_simple, A0_OBS, 2.32e-10, nr,nth,rmin)
    print(f"  simple-nu  nr={nr:5d} nth={nth:4d} rmin={rmin:4.2f}AU: Q2={Q2:+.3e}  (eN={eN:.3f}, r*={rs:.0f} AU)")
print("  target (laneA V5 & repo aest_cassini_quadrupole_full.py): |Q2|=4.78e-26, POSITIVE per Desmond sign")

# (b) framework-nu as source: laneA V6 = 1.96e-26 (canonical a0, gext=2.2e-10)
Q2f,_,_,_=Q2_realspace(F_fw, A0_CANON, 2.2e-10, 6000, 3000, 0.5)
print(f"\n  framework-nu-as-source: Q2={Q2f:+.3e}   (laneA V6: |Q2|=1.96e-26)")

# (c) the LOAD-BEARING number: named survivor p=1.75, y_t=0.5, n=4, canonical, gext=2.2e-10
print()
for nr,nth,Rf in [(6000,3000,3e3),(12000,6000,3e3),(12000,6000,1e4)]:
    Q2b,eN,rs,parts=Q2_realspace(F_member, A0_CANON, 2.2e-10, nr,nth,0.5,Rf,
                                 inner_boundary=False)  # F dies as y^-1.75: no inner div
    print(f"  survivor(p=1.75,yt=0.5,n=4) nr={nr} nth={nth} R={Rf:.0e}r*: Q2={Q2b:+.4e}"
          f"  -> {abs(Q2b)/Q2_CEIL:.2f}x ceiling, chi_max={min(1,Q2_CEIL/abs(Q2b)):.3f}")
print("  laneA (Milgrom v-xi integral): |Q2|=1.41e-26, chi_max=0.37")

# (d) g_ext spread for the survivor
for gx in (1.9e-10, 2.4e-10):
    Q2b,_,_,_=Q2_realspace(F_member, A0_CANON, gx, 6000,3000,0.5,3e3,inner_boundary=False)
    print(f"  survivor gext={gx:.1e}: Q2={Q2b:+.3e} -> chi_max={min(1,Q2_CEIL/abs(Q2b)):.3f}")

# (e) where does the quadrupole live? cumulative Q2(<r) for the survivor
Q2tot,eN,rs,_=Q2_realspace(F_member, A0_CANON, 2.2e-10, 12000,6000,0.5,3e3,inner_boundary=False)
etilde=2.2e-10/A0_CANON; eNv=solve_eN(F_member, etilde); gNe=eNv*A0_CANON
r=np.geomspace(0.5*AU, 3e3*np.sqrt(GM/gNe), 12000)
th=np.linspace(0,np.pi,6000); ct=np.cos(th); st=np.sin(th); P2=0.5*(3*ct**2-1)
rr=r[:,None]; g_r=-GM/rr**2+gNe*ct[None,:]; g_t=-gNe*st[None,:]
y=np.sqrt(g_r**2+g_t**2)/A0_CANON
kern=F_member(y)*(3*P2[None,:]*GM/rr**2-3*gNe*ct[None,:]*(P2[None,:]-st[None,:]**2))*st[None,:]/rr**2
prof=-1.5*np.trapz(kern, th, axis=1)
cum=np.concatenate([[0],np.cumsum(0.5*(prof[1:]+prof[:-1])*np.diff(r))])
rstar=np.sqrt(GM/gNe)
print(f"\n  cumulative Q2(<r)/Q2_tot for the survivor (r* = {rstar/AU:.0f} AU):")
for f_ in (0.1,0.3,1.0,3.0,10.0,100.0):
    i=np.searchsorted(r, f_*rstar)
    print(f"    r = {f_:6.1f} r* ({f_*rstar/AU:9.0f} AU): {cum[min(i,len(cum)-1)]/Q2tot:6.1%}")
print("\nEXIT 0")
