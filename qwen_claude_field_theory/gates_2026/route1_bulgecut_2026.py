#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ROUTE 1: does the eps=0 khronometric-MOND theory survive Cassini after DHF's bulge cut?

THEORY FROZEN.  eps = 0 => mu(x) = x/(1+x) EXACTLY (derived from
F_MOND = -2 sqrt(X) + 2 ln(1+sqrt(X))).  NO shape freedom: the only free quantities are a0
and the per-galaxy M/L.  eta_K = 0, lam_K > 1, DOF 2+1, c_T = c, gamma_PPN = 1.

MACHINERY, all previously validated, nothing refitted:
  * SPARC sample = DHF exactly: Q!=3, i>=30 deg, fractional eV < 10%  -> 147 gal / 2696 pts
  * exact 1-D nuisance prior P(eps_off) (gate6; 1-D vs 2-D agreement 2.0e-3)
  * AQUAL Q2 from the nonlinear solver (validated 1.9% vs Blanchet-Novak 2011)
  * |Q2| = (3/2)|q_zz| a0^{3/2}/sqrt(GM_sun)   [DHF Eq.10, frozen]
  * QUMOND q(eta) kept ONLY as control
"""
import os,sys,json,time
import numpy as np
from scipy.optimize import minimize, minimize_scalar, brentq
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","theory_2026"))
import gate2_dhf_faithful_2026 as B
from munu import nu_n
def head(t): print("\n"+"="*98+f"\n{t}\n"+"="*98,flush=True)
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
G_,MSUN,C,LN10=6.6743e-11,1.98892e30,2.99792458e8,np.log(10.0)
GM_SUN=G_*MSUN; SIG=0.034
UD,UB,UG,SD,SB,SG=0.50,0.70,1.00,0.25,0.25,0.10
GEXT=2.00e-10; Q2_MU,Q2_SD=3.0e-27,3.0e-27

gals,_=B.load_galaxies(B.load_master())
def eps_table(g,neps=481,ni=8001,emax=1.2):
    ic=g["inc"]; sf=g["eD"]/g["D"]; si=g["einc"]
    ig=np.linspace(0.05,89.995,ni); sr=np.sin(np.radians(ic))/np.sin(np.radians(ig))
    pi_=((ig-ic)/si)**2; eg=np.linspace(-emax,emax,neps); P=np.empty(neps)
    for k,e in enumerate(eg):
        fr=10**(-e)*sr**2; okm=fr>1e-8
        p=np.where(okm,((fr-1)/sf)**2+pi_,np.inf); P[k]=p.min()
    return eg,P
PRE=[]
for g in gals:
    R=g["R"]; lgo=np.log10(g["Vobs"]**2/R); sm=2.0*g["eV"]/g["Vobs"]/LN10
    w=1.0/(SIG**2+sm**2); eg,P=eps_table(g)
    PRE.append(dict(name=g["name"],R=R,lgo=lgo,w=w,W=w.sum(),eg=eg,P=P,sqP=np.sqrt(P),
                    Vg2=np.sign(g["Vgas"])*g["Vgas"]**2,Vd2=g["Vdisk"]**2,Vb2=g["Vbul"]**2,
                    hasb=g["hasbul"]))
NB=sum(1 for p in PRE if p["hasb"])
info("sample",f"{len(PRE)} galaxies, {sum(len(p['R']) for p in PRE)} points, {NB} with bulges")

MU1=lambda x: x/(1.0+x)                      # THE THEORY: eps=0, no freedom
def gchi(p,P,a0):
    Ud,Ub,Ug=np.exp(np.clip(p,np.log(0.02),np.log(10.0)))
    gb=np.maximum(Ug*P["Vg2"]+Ud*P["Vd2"]+Ub*P["Vb2"],1.0)/P["R"]
    x=gb/a0
    gobs=gb/MU1(x)                            # g = g_bar/mu(g/a0) solved: see note
    # solve mu(g/a0) g = g_bar exactly for g:  g/(1+g/a0)*... -> g^2/(a0+g) = g_bar
    # => g^2 - g_bar g - g_bar a0 = 0  => g = (g_bar + sqrt(g_bar^2+4 g_bar a0))/2
    gpred=0.5*(gb+np.sqrt(gb*gb+4*gb*a0))
    d=P["lgo"]-np.log10(gpred)
    A_=P["W"]; Bc=(P["w"]*d).sum(); Cc=(P["w"]*d*d).sum()
    tot=Cc+2*Bc*P["eg"]+A_*P["eg"]**2+P["P"]
    k=int(np.argmin(tot))
    lo,hi=P["eg"][max(k-2,0)],P["eg"][min(k+2,len(P["eg"])-1)]
    ef=np.linspace(lo,hi,2001)
    v=min(tot.min(),float(np.min(Cc+2*Bc*ef+A_*ef**2+np.interp(ef,P["eg"],P["sqP"])**2)))
    v+=((p[0]-np.log(UD))/SD)**2+((p[2]-np.log(UG))/SG)**2
    if P["hasb"]: v+=((p[1]-np.log(UB))/SB)**2
    return float(v)
def chi_tot(a0,subset):
    t=0.0
    for P in subset:
        x0=np.array([np.log(UD),np.log(UB),np.log(UG)])
        r=minimize(lambda p: gchi(p,P,a0),x0,method="Nelder-Mead",
                   options=dict(maxiter=3000,xatol=1e-7,fatol=1e-7))
        r2=minimize(lambda p: gchi(p,P,a0),r.x,method="Powell",options=dict(xtol=1e-9,ftol=1e-10))
        t+=min(r.fun,r2.fun)
    return t
def fit_a0(subset,lo=0.6e-10,hi=1.8e-10):
    r=minimize_scalar(lambda A: chi_tot(A,subset),bounds=(lo,hi),method="bounded",
                      options=dict(xatol=1e-13))
    a0=r.x; c0=r.fun
    # 1-sigma from delta chi2 = 1
    f=lambda A: chi_tot(A,subset)-c0-1.0
    try: lo1=brentq(f,lo,a0,xtol=1e-13)
    except Exception: lo1=np.nan
    try: hi1=brentq(f,a0,hi,xtol=1e-13)
    except Exception: hi1=np.nan
    return a0,c0,lo1,hi1

head("A -- fit a0 with the theory's OWN mu = x/(1+x), exact nuisances")
t0=time.time()
FULL=PRE; NOB=[p for p in PRE if not p["hasb"]]
res={}
for lab,sub in (("full 147",FULL),("bulge-free 116",NOB)):
    a0,c0,l1,h1=fit_a0(sub)
    res[lab]=dict(a0=a0,chi=c0,lo=l1,hi=h1,n=len(sub))
    info(f"A1 {lab:<16}",f"a0 = {a0*1e10:.4f} +{(h1-a0)*1e10:.4f}/-{(a0-l1)*1e10:.4f} e-10 m/s^2  "
                          f"({len(sub)} galaxies, {time.time()-t0:.0f}s)")
json.dump({k:{kk:float(vv) for kk,vv in v.items()} for k,v in res.items()},
          open("route1_a0.json","w"),indent=1)
