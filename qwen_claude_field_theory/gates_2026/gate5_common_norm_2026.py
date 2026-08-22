#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate5_common_norm_2026.py -- PHASE 12 + 13 with ONE common likelihood normalisation.

WHY THIS REBUILD.  The a0 scan in gate4c reported absolute -2lnL of -12412.9, -12354.6,
-12380.5, -12186.6, -12436.6, ... -- non-monotonic in a0 with O(100) jumps.  That is not a
likelihood profile; it is inner-optimiser noise, because each a0 built its per-galaxy curves
from an independently warm-started 5-D Nelder-Mead chain.  Any a0 profile read off it is void.

THE FIX, which is structural rather than a bigger optimiser:
  * distance and inclination BOTH act on the data only as a per-galaxy LOG-OFFSET of g_obs:
        g_bar = V_bar^2/R is distance-INVARIANT   (V^2 ~ D and R ~ D)
        g_obs = V_obs^2/R  ->  scales as 1/D and as 1/sin^2 i
    so define eps_i = Delta log10 g_obs, with Gaussian prior width
        sigma_eps^2 = (e_D/D / ln10)^2 + (2 cot(i) e_i[rad] / ln10)^2 .
  * eps enters the residual LINEARLY, so it is profiled in CLOSED FORM.  No optimiser touches it.
  * the weights w_j = 1/(sigma_int^2 + sigma_meas^2) with sigma_meas = 2 e_V/(V ln10) are then
    INDEPENDENT of every parameter, so the sum(log s^2) term is a CONSTANT.  It cancels
    identically from every Delta chi2 and the normalisation is common BY CONSTRUCTION.
  * the inner problem collapses to 3-D (Upsilon_disk, Upsilon_bulge, Upsilon_gas), 2-D without
    a bulge -- small enough to solve reliably.

Priors are DHF's fiducial [Sec3.2(i)]: lognormal Upsilon_disk 0.50, Upsilon_bulge 0.70, both
25 per cent; Upsilon_gas 1.0 +- 10 per cent.  sigma_int = 0.034 dex [DHF Tab.1].
Environmental variable is the DERIVED Weyl one: Z_E = sqrt(6)(c/v_inf)^2, v_inf=(G M a0)^(1/4).
"""
import os, sys, json, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq, minimize
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n
import gate2_dhf_faithful_2026 as B
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def check(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True); return c
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
G_,MSUN,C,LN10=6.6743e-11,1.98892e30,2.99792458e8,np.log(10.0)
GM_SUN=G_*MSUN; SIG_INT=0.034
UD,UB,UG,SD,SB,SG=0.50,0.70,1.00,0.25,0.25,0.10
Q2_MU,Q2_SD=3.0e-27,3.0e-27; GEXT=2.00e-10
A0_CAN=9.3619e-11

gals,_=B.load_galaxies(B.load_master())
PRE=[]
for g in gals:
    R=g["R"]; lgo=np.log10(g["Vobs"]**2/R)
    sm=2.0*g["eV"]/g["Vobs"]/LN10
    w=1.0/(SIG_INT**2+sm**2)
    i=np.radians(g["inc"]); ei=np.radians(g["einc"])
    se2=(g["eD"]/g["D"]/LN10)**2+(2.0/np.tan(i)*ei/LN10)**2
    PRE.append(dict(name=g["name"],R=R,lgo=lgo,w=w,
                    Vg2=np.sign(g["Vgas"])*g["Vgas"]**2,Vd2=g["Vdisk"]**2,Vb2=g["Vbul"]**2,
                    hasb=g["hasbul"],se2=max(se2,1e-8),W=w.sum()))
info("A0  constant term",f"sum(log s^2) is parameter-independent and cancels from every "
     f"Delta chi2 -- normalisation is common by construction")

def gchi2(p,P,n,a0):
    Ud,Ub,Ug=np.exp(np.clip(p,np.log(0.02),np.log(10.0)))
    Vb2=np.maximum(Ug*P["Vg2"]+Ud*P["Vd2"]+Ub*P["Vb2"],1.0)
    gb=Vb2/P["R"]
    lgp=np.log10(nu_n(gb/a0,n)*gb)
    d=P["lgo"]-lgp
    # closed-form profile of the log-offset eps with its Gaussian prior
    eps=-(P["w"]*d).sum()/(P["W"]+1.0/P["se2"])
    c2=(P["w"]*(d+eps)**2).sum()+eps**2/P["se2"]
    c2+=((p[0]-np.log(UD))/SD)**2+((p[2]-np.log(UG))/SG)**2
    if P["hasb"]: c2+=((p[1]-np.log(UB))/SB)**2
    return float(c2)
def gmin(P,n,a0,x0):
    r=minimize(lambda p: gchi2(p,P,n,a0),x0,method="Nelder-Mead",
               options=dict(maxiter=4000,maxfev=4000,xatol=1e-7,fatol=1e-7))
    r2=minimize(lambda p: gchi2(p,P,n,a0),r.x,method="Powell",
                options=dict(maxiter=4000,xtol=1e-8,ftol=1e-9))
    return (r2.x,r2.fun) if r2.fun<r.fun else (r.x,r.fun)

NG=np.geomspace(0.35,80.0,40); lnNG=np.log(NG)
A0S=np.array(sorted(set(list(np.linspace(0.85e-10,1.45e-10,13))+[A0_CAN])))
head("PART A -- build chi2_i(n) on a common normalisation, for every a0")
t0=time.time(); CUBE={}; MB={}
for a0 in A0S:
    Cv=np.zeros((len(PRE),len(NG))); mb=np.zeros(len(PRE))
    for k,P in enumerate(PRE):
        x0=np.array([np.log(UD),np.log(UB),np.log(UG)])
        for j,n in enumerate(NG):
            x0,v=gmin(P,float(n),a0,x0); Cv[k,j]=v
        Ud,Ub,Ug=np.exp(x0)
        Vb2=np.maximum(Ug*P["Vg2"]+Ud*P["Vd2"]+Ub*P["Vb2"],1.0)
        jj=np.argmax(P["R"]); mb[k]=Vb2[jj]*P["R"][jj]/G_
    CUBE[a0]=Cv; MB[a0]=mb
    info(f"A1  a0={a0*1e10:.4f}e-10",f"chi2 min over the n grid = {Cv.min(axis=1).sum():.2f}   "
         f"({time.time()-t0:.0f} s)")
head("PART A2 -- smoothness check: is the a0 profile now physical?")
raw=np.array([CUBE[a]. min(axis=1).sum() for a in A0S])
d2=np.diff(raw,2)
check(np.max(np.abs(d2))<0.35*max(1.0,np.ptp(raw)),
      "A2  the per-a0 minimum is now SMOOTH in a0 (2nd differences small vs the range)",
      f"range {np.ptp(raw):.1f}, max |2nd diff| {np.max(np.abs(d2)):.2f} -- contrast gate4c, "
      "where 2nd differences were comparable to the whole range")

def build(a0):
    mb=MB[a0]; ZE=np.sqrt(6)*(C/(G_*mb*a0)**0.25)**2
    ZES=np.sqrt(6)*(C/(GM_SUN*a0)**0.25)**2
    Z0=np.exp(np.mean(np.log(ZE)))
    return np.log(ZE/Z0), float(np.log(ZES/Z0))
def chi2(a0,ln_n0,beta,zg,Cv):
    a=ln_n0+beta*zg
    idx=np.clip(np.searchsorted(lnNG,a)-1,0,len(lnNG)-2)
    t=np.clip((a-lnNG[idx])/(lnNG[idx+1]-lnNG[idx]),0.0,1.0)
    pen=np.where((a<lnNG[0])|(a>lnNG[-1]),1e4,0.0)
    return float((Cv[np.arange(len(a)),idx]*(1-t)+Cv[np.arange(len(a)),idx+1]*t+pen).sum())

def q_exact(nu,eN,nv=8000,nxi=192):
    xg,wg=leggauss(nxi); v=np.geomspace(1e-7,1e7,nv)
    V,XX=np.meshgrid(v,xg,indexing="ij")
    w=np.sqrt(np.maximum(eN**2+V**4+2.0*eN*V**2*XX,1e-24))
    return 3.0*np.trapz(((nu(w)-1.0)*(eN*0.5*(5*XX**3-3.0*XX)+V**2*0.5*(3*XX**2-1.0)))@wg,v)
def eN_of(nu,et):
    f=lambda t: t*float(np.atleast_1d(nu(np.array([t])))[0])-et
    hi=max(4.0*et,4.0)
    while f(hi)<0: hi*=2.0
    return brentq(f,1e-10,hi,xtol=1e-14,rtol=1e-14)
QC={}
def Q2_of(n,a0):
    k=(round(float(n),3),round(a0,14))
    if k not in QC:
        nu=lambda yy: nu_n(yy,k[0])
        QC[k]=1.5*a0**1.5/np.sqrt(GM_SUN)*q_exact(nu,eN_of(nu,GEXT/a0))
    return QC[k]

head("PART B -- the full (a0, n0, beta) surface, ONE normalisation")
LN0=np.log(np.geomspace(0.5,4.0,80)); BET=np.linspace(-0.10,0.55,66)
GLOB=np.inf; TAB=[]
SURF={}
for a0 in A0S:
    zg,zS=build(a0); Cv=CUBE[a0]
    S=np.array([[chi2(a0,l,b,zg,Cv) for b in BET] for l in LN0])
    SURF[a0]=(S,zS)
    GLOB=min(GLOB,S.min())
for a0 in A0S:
    S,zS=SURF[a0]; i,j=np.unravel_index(np.argmin(S),S.shape)
    ns=float(np.clip(np.exp(LN0[i]+BET[j]*zS),0.35,400))
    TAB.append(dict(a0=float(a0),dchi2=float(S.min()-GLOB),n0=float(np.exp(LN0[i])),
                    beta=float(BET[j]),nsun=ns,Q2=float(Q2_of(ns,a0))))
print(f"  {'a0/1e-10':>9} {'Dchi2(a0)':>10} {'n0':>7} {'beta':>8} {'n_sun':>8} {'Q2/1e-27':>9} {'sig':>6}")
for r in TAB:
    mark="  <-- CANONICAL" if abs(r["a0"]-A0_CAN)<1e-14 else ""
    print(f"  {r['a0']*1e10:9.4f} {r['dchi2']:10.2f} {r['n0']:7.3f} {r['beta']:+8.3f} "
          f"{r['nsun']:8.2f} {r['Q2']*1e27:9.2f} {(r['Q2']-Q2_MU)/Q2_SD:+6.1f}{mark}")
head("PART C -- PHASE 13: absolute a0 profile (n0, beta profiled out)")
aa=np.array([r["a0"] for r in TAB]); dd=np.array([r["dchi2"] for r in TAB])
info("C1  best a0",f"{aa[np.argmin(dd)]*1e10:.4f}e-10")
can=[r for r in TAB if abs(r["a0"]-A0_CAN)<1e-14][0]
info("C2  canonical a0 = 9.3619e-11",f"Delta chi2 = {can['dchi2']:.2f}  "
     f"-> {'INSIDE' if can['dchi2']<=4 else ('MARGINAL' if can['dchi2']<=9 else 'OUTSIDE')} "
     "the 2-sigma region (1 d.o.f., before permutation inflation)")
info("C3  CAVEAT",f"the permutation calibration measured the profile Delta chi2 to be "
     "optimistic by 2.23x in variance; inflating, the canonical point sits at effective "
     f"Delta chi2 = {can['dchi2']/2.23**2:.2f}")
head("PART D -- PHASE 12: joint SPARC x Cassini, per a0")
CAL=2.23
for a0 in A0S:
    S,zS=SURF[a0]; Sm=S-S.min()
    NS=np.clip(np.exp(LN0[:,None]+BET[None,:]*zS),0.35,400)
    kn=np.geomspace(0.4,320,80); kv=np.array([Q2_of(n,a0) for n in kn])
    Q2g=np.exp(np.interp(np.log(NS),np.log(kn),np.log(kv)))
    ok=(Sm<=4.0*CAL**2)&(Q2g<=9.0e-27)
    if ok.any():
        bb=BET[np.where(ok)[1]]
        k=np.argmin(np.where(ok,Sm,np.inf)); ii,jj=np.unravel_index(k,Sm.shape)
        msg=(f"NON-EMPTY: beta in [{bb.min():+.3f}, {bb.max():+.3f}]; cheapest "
             f"(n0={np.exp(LN0[ii]):.3f}, beta={BET[jj]:+.3f}), RAR price {Sm[ii,jj]:.2f}")
    else: msg="EMPTY"
    m="  <-- CANONICAL" if abs(a0-A0_CAN)<1e-14 else ""
    info(f"D1  a0={a0*1e10:.4f}e-10",msg+m)
json.dump(dict(table=TAB,global_min=float(GLOB),canonical=can),open("gate5_result.json","w"),indent=1)
print("\n-> gate5_result.json")
