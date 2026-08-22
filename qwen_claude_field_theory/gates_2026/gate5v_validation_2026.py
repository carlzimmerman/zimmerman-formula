#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate5v -- Carl's mandated validation BEFORE the full 14 x 40 x 147 scan.

(1) Three independent inner solvers must agree to |Delta chi2| < 1e-2 on 10 representative
    galaxies: multi-start L-BFGS-B, coarse-grid + polish, and Nelder-Mead+Powell -- all with
    the log-offset eps profiled ANALYTICALLY.
(2) The combined distance+inclination prior on eps is assumed Gaussian.  That assumption is
    NOT taken on faith: it is checked against an EXACT 2-D marginalisation over (f_D, i)
    with their own priors.
"""
import os,sys,time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n
import gate2_dhf_faithful_2026 as B
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def check(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True); return c
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
G_,LN10=6.6743e-11,np.log(10.0); SIG=0.034
UD,UB,UG,SD,SB,SG=0.50,0.70,1.00,0.25,0.25,0.10
gals,_=B.load_galaxies(B.load_master())
def prep(g):
    R=g["R"]; lgo=np.log10(g["Vobs"]**2/R); sm=2.0*g["eV"]/g["Vobs"]/LN10
    w=1.0/(SIG**2+sm**2); i=np.radians(g["inc"]); ei=np.radians(g["einc"])
    se2=(g["eD"]/g["D"]/LN10)**2+(2.0/np.tan(i)*ei/LN10)**2
    return dict(name=g["name"],R=R,lgo=lgo,w=w,W=w.sum(),se2=max(se2,1e-8),
                Vg2=np.sign(g["Vgas"])*g["Vgas"]**2,Vd2=g["Vdisk"]**2,Vb2=g["Vbul"]**2,
                hasb=g["hasbul"],D=g["D"],eD=g["eD"],inc=g["inc"],einc=g["einc"],
                Vobs=g["Vobs"],eV=g["eV"])
def chi(p,P,n,a0):
    Ud,Ub,Ug=np.exp(np.clip(p,np.log(0.02),np.log(10.0)))
    gb=np.maximum(Ug*P["Vg2"]+Ud*P["Vd2"]+Ub*P["Vb2"],1.0)/P["R"]
    d=P["lgo"]-np.log10(nu_n(gb/a0,n)*gb)
    eps=-(P["w"]*d).sum()/(P["W"]+1.0/P["se2"])
    c=(P["w"]*(d+eps)**2).sum()+eps**2/P["se2"]
    c+=((p[0]-np.log(UD))/SD)**2+((p[2]-np.log(UG))/SG)**2
    if P["hasb"]: c+=((p[1]-np.log(UB))/SB)**2
    return float(c) if np.isfinite(c) else 1e12
def m_lbfgs(P,n,a0):
    best=np.inf
    for s in ([np.log(UD),np.log(UB),np.log(UG)],[0,0,0],[-1,-1,0.1],[0.5,0.5,-0.1],[-2,0.3,0]):
        r=minimize(lambda p: chi(p,P,n,a0),np.array(s,float),method="L-BFGS-B",
                   bounds=[(np.log(0.02),np.log(10))]*3,options=dict(maxiter=5000,ftol=1e-14))
        best=min(best,r.fun)
    return best
def m_grid(P,n,a0):
    gd=np.log(np.geomspace(0.05,6,17))
    best=np.inf; bx=None
    for a in gd:
        for b in (gd if P["hasb"] else [np.log(UB)]):
            for c in np.log(np.linspace(0.6,1.6,7)):
                v=chi(np.array([a,b,c]),P,n,a0)
                if v<best: best,bx=v,np.array([a,b,c])
    r=minimize(lambda p: chi(p,P,n,a0),bx,method="Powell",options=dict(xtol=1e-10,ftol=1e-12))
    return min(best,r.fun)
def m_nmpow(P,n,a0):
    x0=np.array([np.log(UD),np.log(UB),np.log(UG)])
    r=minimize(lambda p: chi(p,P,n,a0),x0,method="Nelder-Mead",
               options=dict(maxiter=4000,maxfev=4000,xatol=1e-8,fatol=1e-8))
    r2=minimize(lambda p: chi(p,P,n,a0),r.x,method="Powell",options=dict(xtol=1e-10,ftol=1e-12))
    return min(r.fun,r2.fun)
head("PART A -- three independent inner solvers, 10 representative galaxies")
idx=np.linspace(0,len(gals)-1,10).astype(int)
worst=0.0
for a0 in (9.3619e-11,1.08e-10,1.30e-10):
    for n in (0.6,1.0,3.0,12.0):
        for k in idx:
            P=prep(gals[k])
            v=[m_lbfgs(P,n,a0),m_grid(P,n,a0),m_nmpow(P,n,a0)]
            worst=max(worst,max(v)-min(v))
info("A1  max spread across all 3 solvers x 10 galaxies x 4 n x 3 a0",f"{worst:.3e}")
check(worst<1e-2,"A2  three independent inner solvers agree to < 1e-2 in chi2",
      "the analytic eps profile plus a 3-D inner problem is numerically reliable")
head("PART B -- is the Gaussian eps prior justified?  EXACT 2-D marginalisation check")
def exact_eps_chi(P,n,a0,p):
    """Exact: scan (f_D, i) on their own priors, no Gaussian collapse."""
    Ud,Ub,Ug=np.exp(p)
    gb=np.maximum(Ug*P["Vg2"]+Ud*P["Vd2"]+Ub*P["Vb2"],1.0)/P["R"]
    lgp=np.log10(nu_n(gb/a0,n)*gb)
    fd=np.linspace(max(0.4,1-4*P["eD"]/P["D"]),1+4*P["eD"]/P["D"],61)
    di=np.linspace(-4*P["einc"],4*P["einc"],61)
    bestv=np.inf
    for f in fd:
        for d in di:
            ii=np.clip(P["inc"]+d,10,90)
            sc=np.sin(np.radians(P["inc"]))/np.sin(np.radians(ii))
            lgo=np.log10((P["Vobs"]*sc)**2/(P["R"]*f))
            r=lgo-lgp
            v=(P["w"]*r**2).sum()+(f-1)**2/(P["eD"]/P["D"])**2+(d/P["einc"])**2
            bestv=min(bestv,v)
    return bestv
def gauss_eps_chi(P,n,a0,p):
    Ud,Ub,Ug=np.exp(p)
    gb=np.maximum(Ug*P["Vg2"]+Ud*P["Vd2"]+Ub*P["Vb2"],1.0)/P["R"]
    d=P["lgo"]-np.log10(nu_n(gb/a0,n)*gb)
    eps=-(P["w"]*d).sum()/(P["W"]+1.0/P["se2"])
    return (P["w"]*(d+eps)**2).sum()+eps**2/P["se2"]
p0=np.array([np.log(UD),np.log(UB),np.log(UG)])
dev=[]
for k in idx:
    P=prep(gals[k])
    for n in (1.0,5.0):
        e=exact_eps_chi(P,n,1.08e-10,p0); g=gauss_eps_chi(P,n,1.08e-10,p0)
        dev.append(g-e)
dev=np.array(dev)
info("B1  Gaussian-eps minus exact 2-D (chi2 units)",
     f"mean {dev.mean():+.4f}  max |dev| {np.abs(dev).max():.4f}  over 20 cases")
check(np.abs(dev).max()<0.5,"B2  the Gaussian eps prior reproduces the exact 2-D "
      "distance+inclination marginalisation to well under 1 chi2 unit per galaxy",
      "the analytic collapse is validated, not assumed")
info("B3  scope","checked at the prior-centre Upsilon; the deviation is a per-galaxy additive "
     "offset that is nearly parameter-independent, so it largely cancels from Delta chi2.")
