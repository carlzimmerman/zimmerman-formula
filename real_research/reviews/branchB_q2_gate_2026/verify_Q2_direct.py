#!/usr/bin/env python3
"""
DIRECT closed-form real-space Q2 (no by-parts, no boundary terms, no numerical derivatives).
  rho_ph = -(1/4 pi G) div[F g_N] = -(1/4 pi G) g_N . grad F        (div g_N = 0 off-source)
  Q2 = 3 G Int rho_ph P2 / r^3 dV
     = -(3/2) Int dr Int dx  F'(y) * (G_s/(a0 r |g|)) [2(G_s - gNe x)^2 - gNe^2(1-x^2)]
                              * P2(x) / r  * r^2            (dV = 2 pi r^2 dr dx)
  with G_s = GM/r^2, |g|^2 = G_s^2 - 2 G_s gNe x + gNe^2, y = |g|/a0, x = cos th,
  gNe = e_N a0, e_N (1+F(e_N)) = g_ext/a0.
Gauss-Legendre in x (exact P2 orthogonality cancellation), log-r trapz.
Cross-checks laneA's Milgrom (v,xi) integral for: simple-nu, framework-nu, the named
survivor (p=1.75, y_t=0.5, n=4).
"""
import numpy as np
from scipy.optimize import brentq

G=6.674e-11; Msun=1.989e30; AU=1.495978707e11; GM=G*Msun
Z=np.sqrt(32*np.pi/3.0); A=np.sqrt(Z/6.0)
A0_CANON=9.36e-11; A0_OBS=1.2e-10; Q2_CEIL=5.2e-27

def F_mem(y,p=1.75,yt=0.5,n=4):
    return A*y**-0.5*(1+(y/yt)**n)**(-(p-0.5)/n)
def Fp_mem(y,p=1.75,yt=0.5,n=4):
    S=(1+(y/yt)**n)**(-(p-0.5)/n)
    Sp=S*(-(p-0.5))*(y/yt)**n/(y*(1+(y/yt)**n))
    return A*(-0.5*y**-1.5*S + y**-0.5*Sp)
def F_simple(y):  return 0.5*(np.sqrt(1+4/y)-1)
def Fp_simple(y): return -1.0/(y**2*np.sqrt(1+4/y))
def F_fw(y):  return np.sqrt(1+1/y)-1
def Fp_fw(y): return -0.5/(y**2*np.sqrt(1+1/y))

def solve_eN(F,et): return brentq(lambda e: e*(1+F(e))-et,1e-9,10*et,xtol=1e-15,rtol=1e-13)

def Q2_direct(F,Fp,a0,gext,nr=20000,nx=800,rmin_AU=0.01,Rfac=3e4):
    eN=solve_eN(F,gext/a0); gNe=eN*a0
    rstar=np.sqrt(GM/gNe)
    x,w=np.polynomial.legendre.leggauss(nx)
    P2=0.5*(3*x**2-1)
    r=np.geomspace(rmin_AU*AU,Rfac*rstar,nr)
    out=np.empty(nr)
    for i,ri in enumerate(r):      # loop r to keep memory small at high nx*nr
        Gs=GM/ri**2
        g2=Gs*Gs-2*Gs*gNe*x+gNe*gNe
        gm=np.sqrt(g2); y=gm/a0
        kern=Fp(y)*(Gs/(a0*ri*gm))*(2*(Gs-gNe*x)**2-gNe*gNe*(1-x*x))*P2/ri
        out[i]=np.dot(kern,w)
    Q2=-1.5*np.trapz(out,r)
    return Q2,eN,rstar,out,r

print("="*96)
print(" DIRECT closed-form real-space Q2 (independent of Milgrom v-xi integral AND of by-parts)")
print("="*96)
cases=[("simple-nu (laneA V5: 4.78e-26)",F_simple,Fp_simple,A0_OBS,2.32e-10),
       ("framework-nu (laneA V6: 1.96e-26)",F_fw,Fp_fw,A0_CANON,2.2e-10),
       ("SURVIVOR p=1.75,yt=0.5,n=4 (laneA: 1.41e-26, chi_max=0.37)",F_mem,Fp_mem,A0_CANON,2.2e-10)]
for lab,F,Fp,a0,gx in cases:
    Q2a,eN,rstar,_,_=Q2_direct(F,Fp,a0,gx,nr=10000,nx=400)
    Q2b,_,_,_,_    =Q2_direct(F,Fp,a0,gx,nr=20000,nx=800)
    Q2c,_,_,_,_    =Q2_direct(F,Fp,a0,gx,nr=20000,nx=800,rmin_AU=0.001,Rfac=3e5)
    print(f"\n  {lab}")
    print(f"    eN={eN:.4f}  r*={rstar/AU:.0f} AU")
    print(f"    Q2 = {Q2a:+.4e} | {Q2b:+.4e} | {Q2c:+.4e}  (res x2 | domain x10 -- convergence)")
    print(f"    -> {abs(Q2b)/Q2_CEIL:.2f}x ceiling, chi_max={min(1,Q2_CEIL/abs(Q2b)):.3f}")

# where the survivor's Q2 lives (cumulative)
Q2,eN,rstar,prof,r=Q2_direct(F_mem,Fp_mem,A0_CANON,2.2e-10,nr=20000,nx=800)
cum=-1.5*np.concatenate([[0],np.cumsum(0.5*(prof[1:]+prof[:-1])*np.diff(r))])
print(f"\n  survivor cumulative Q2(<r)/total  (r*={rstar/AU:.0f} AU):")
for f_ in (0.1,0.3,1,3,10,30):
    i=np.searchsorted(r,f_*rstar); print(f"    {f_:5.1f} r*: {cum[min(i,len(cum)-1)]/Q2:7.1%}")

# g_ext spread for the survivor
for gx in (1.9e-10,2.4e-10):
    Q2s,_,_,_,_=Q2_direct(F_mem,Fp_mem,A0_CANON,gx,nr=10000,nx=400)
    print(f"  survivor gext={gx:.1e}: Q2={Q2s:+.3e} -> chi_max={min(1,Q2_CEIL/abs(Q2s)):.3f}")
print("\nEXIT 0")
