#!/usr/bin/env python3
"""CFG79 step-1 toy (diagnostic, not a result): what a naive truncated-power-law MLE returns from a footprint-limited
spectroscopic sample when the true gamma=3 (Sigma ~ R^-2), for three assumed footprints. Shows the size/sign of the
selection bias and that it depends on footprint knowledge not on disk. Fixed seed, declared before running."""
import numpy as np
from scipy.optimize import brentq
rng=np.random.default_rng(79)
def mle_s(R,lo,hi):
    lr=np.log(R); n=len(R)
    def f(s):
        a=2-s
        m=(hi**a*np.log(hi)-lo**a*np.log(lo))/(hi**a-lo**a)-1/a if abs(a)>1e-9 else (np.log(hi)+np.log(lo))/2
        return -lr.sum()+n*m
    return brentq(f,-3,8)   # Sigma ~ R^-s
def samp(gamma,N,lo,hi):
    # pdf(R) ~ R * R^-(gamma-1) = R^(2-gamma) on [lo,hi]
    p=3-gamma; u=rng.random(N)
    if abs(p)<1e-9: return lo*(hi/lo)**u
    return (lo**p+u*(hi**p-lo**p))**(1/p)
def inrect(x,y,pa,L=16.,W=4.):
    c,s=np.cos(pa),np.sin(pa); u=x*c+y*s; v=-x*s+y*c
    return (abs(u)<L/2)&(abs(v)<W/2)
def sim(gamma,foot,lo=0.8,hi=8.0,N=400000,pas=None):
    # 3D power law, projected: sample R directly from Sigma ~ R^-(gamma-1) in [0.05,60] arcmin, random angle
    R=samp(gamma,N,0.05,60.); th=rng.random(N)*2*np.pi
    x,y=R*np.cos(th),R*np.sin(th)
    if foot=="full": m=np.ones(N,bool)
    elif foot=="strip": m=inrect(x,y,0.0)
    elif foot=="3masks": m=inrect(x,y,0.0)|inrect(x,y,np.radians(20))|inrect(x,y,np.radians(-20))
    elif foot=="3masks_wide": m=inrect(x,y,0.0,16,6)|inrect(x,y,np.radians(60),16,6)|inrect(x,y,np.radians(-60),16,6)
    Rs=R[m&(R>lo)&(R<hi)]
    return mle_s(Rs,lo,hi)+1, len(Rs)
for foot in ("full","strip","3masks","3masks_wide"):
    for g in (2.0,3.0):
        out=[sim(g,foot,N=6000000//20) for _ in range(5)]
        print(f"footprint {foot:11s} true gamma {g}: naive MLE gamma {np.mean([o[0] for o in out]):.2f} (N/sample~{int(np.mean([o[1] for o in out]))})")
# Poisson-only error at the samples sizes found on disk
for N in (40,100,250,600):
    est=[mle_s(samp(3.0,N,0.8,8.0),0.8,8)+1 for _ in range(400)]
    print(f"Poisson-only sigma(gamma) for N={N} in 0.8-8 arcmin (full azimuth, no incompleteness): {np.std(est):.2f}")
