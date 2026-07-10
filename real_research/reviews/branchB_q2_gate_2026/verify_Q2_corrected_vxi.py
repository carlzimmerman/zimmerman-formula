#!/usr/bin/env python3
"""
CORRECTED (v,xi) Milgrom-2009-eq(23) quadrupole vs the laneA implementation.
Milgrom 2009 (arXiv:0906.4817v2) eq (23), verbatim:
  qtilde(eta) = -(1/4pi) Int (nu-1)/|u|^4 [6 g^N_z n_z + 3 g_N.n (1-5 n_z^2)] d^3u,
  g_N = -a0 (eta_N e_z + uhat/|uhat|^2)  [eq 21; u in R_M, g in a0 units]
Angular reduction (xi = cos th, v^2 = 1/uhat^2 = solar g_N/a0):
  q = (3/2) Int_0^inf dv Int_-1^1 dxi (nu-1)(Y) [eta_N (3 xi - 5 xi^3) + v^2 (1 - 3 xi^2)]
  Y = sqrt(eta_N^2 + v^4 + 2 eta_N v^2 xi)     <-- Y is ONLY the nu argument.
laneA/repo divide the integrand by sqrt(D)=Y: WRONG per the primary source.
Check: corrected (v,xi) must match the independent real-space values
  simple-nu 3.515e-26, framework-nu 2.237e-26, survivor 1.923e-26,
then recompute chi_max for every laneA passer on both footings.
"""
import numpy as np
from scipy.optimize import brentq
from scipy import integrate
import warnings; warnings.filterwarnings("ignore")

G=6.674e-11; Msun=1.989e30; GM=G*Msun
Z=np.sqrt(32*np.pi/3.0); A=np.sqrt(Z/6.0)
A0_CANON=9.36e-11; A0_ALT=1.13e-10; A0_OBS=1.2e-10
Q2_CEIL=5.2e-27; GEXT=2.2e-10

def F_mem(y,p,yt,n): return A*y**-0.5*(1+(y/yt)**n)**(-(p-0.5)/n)
def F_simple(y): return 0.5*(np.sqrt(1+4/y)-1)
def F_fw(y): return np.sqrt(1+1/y)-1

def solve_eN(F,et): return brentq(lambda e: e*(1+F(e))-et,1e-9,10*et,xtol=1e-15)

def q_corr(F,etilde,vmax=200.0):
    eN=solve_eN(F,etilde)
    def ig(xi,v):
        D=eN*eN+v**4+2*eN*v*v*xi
        if D<=1e-30: return 0.0
        return F(np.sqrt(D))*(eN*(3*xi-5*xi**3)+v*v*(1-3*xi*xi))   # NO /sqrt(D)
    val,_=integrate.dblquad(ig,0.0,vmax,lambda v:-1.0,lambda v:1.0,epsabs=1e-12,epsrel=1e-9)
    return 1.5*val,eN

def Q2_corr(F,a0,gext,vmax=200.0):
    q,eN=q_corr(F,gext/a0,vmax)
    return -(3.0*a0**1.5)/(2.0*np.sqrt(GM))*q,q,eN

print(" corrected (v,xi) vs independent real-space:")
for lab,F,a0,gx,target in [("simple-nu",F_simple,A0_OBS,2.32e-10,3.515e-26),
                           ("framework-nu",F_fw,A0_CANON,GEXT,2.237e-26),
                           ("survivor p1.75",lambda y:F_mem(y,1.75,0.5,4),A0_CANON,GEXT,1.923e-26)]:
    Q2,q,eN=Q2_corr(F,a0,gx)
    Q2b,_,_=Q2_corr(F,a0,gx,vmax=400.0)
    print(f"  {lab:16s}: Q2={Q2:+.4e} (vmax400: {Q2b:+.4e})  real-space {target:.3e}"
          f"  ratio {abs(Q2)/target:.4f}")

# recompute chi_max for laneA's passer sets (from laneA_output.txt tables)
passers_canon=[(1.75,0.5,2),(1.75,0.5,4),(1.75,1.0,1),(2.0,0.5,1),(2.0,0.5,2),(2.0,0.5,4),
               (2.0,1.0,1),(2.0,1.0,2),(2.0,1.0,4),(2.0,1.5,1),(2.0,1.5,2),(2.25,0.5,1),
               (2.25,0.5,2),(2.25,0.5,4),(2.25,1.0,1),(2.25,1.0,2),(2.25,1.0,4),(2.25,1.5,1),
               (2.25,1.5,2),(2.5,0.5,1),(2.5,0.5,2),(2.5,0.5,4),(2.5,1.0,1),(2.5,1.0,2),
               (2.5,1.0,4),(2.5,1.5,1),(2.5,1.5,2),(3.0,0.5,1),(3.0,0.5,2),(3.0,1.0,1),
               (3.0,1.0,2),(3.0,1.0,4),(3.0,1.5,2)]
print("\n corrected Q2(chi=1) and chi_max, CANONICAL footing (laneA passer list):")
print(f"  {'p':>5}{'y_t':>5}{'n':>3}{'|Q2| corr':>12}{'x ceiling':>10}{'chi_max corr':>13}")
best=None
for (p,yt,n) in passers_canon:
    F=lambda y,p=p,yt=yt,n=n: F_mem(y,p,yt,n)
    try:
        Q2,q,eN=Q2_corr(F,A0_CANON,GEXT)
    except Exception as e:
        print(f"  {p:>5.2f}{yt:>5.1f}{n:>3d}  FAILED {e}"); continue
    cm=min(1.0,Q2_CEIL/abs(Q2))
    if best is None or cm>best[3]: best=(p,yt,n,cm,Q2)
    print(f"  {p:>5.2f}{yt:>5.1f}{n:>3d}{abs(Q2):>12.2e}{abs(Q2)/Q2_CEIL:>10.2f}{cm:>13.3f}")
print(f"\n  best corrected canonical member: p={best[0]}, y_t={best[1]}, n={best[2]}, "
      f"chi_max={best[3]:.3f}, |Q2|(chi=1)={abs(best[4]):.3e}")

# g_ext spread for corrected best
for gx in (1.9e-10,2.4e-10):
    F=lambda y: F_mem(y,best[0],best[1],best[2])
    Q2,_,_=Q2_corr(F,A0_CANON,gx)
    print(f"  best member gext={gx:.1e}: chi_max={min(1.0,Q2_CEIL/abs(Q2)):.3f}")

# alt footing best from laneA (p=2.25,0.5,4) and a few others
print("\n ALT footing (a0=1.13e-10) spot checks:")
for (p,yt,n) in [(1.75,0.5,4),(2.25,0.5,4),(2.0,1.0,2),(3.0,1.5,2)]:
    F=lambda y,p=p,yt=yt,n=n: F_mem(y,p,yt,n)
    Q2,_,_=Q2_corr(F,A0_ALT,GEXT)
    print(f"  p={p}, yt={yt}, n={n}: |Q2|={abs(Q2):.2e}, chi_max={min(1.0,Q2_CEIL/abs(Q2)):.3f}")
print("\nEXIT 0")
