#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate4b_joint_reconciliation_2026.py -- GATE 4 AS CARL DEFINES IT.

NOT "is Weyl unique".  The test is:

   can a Weyl/tidal environmental variable QUANTITATIVELY reconcile the RAR transition
   with the Cassini quadrupole, while leaving the deep-MOND limit and the BTFR unchanged?

ONE model, both endpoints, no separate comparison of independently-derived numbers:

   n_i = n0 (Z_i/Z_0)^beta ,   Z = c^4 sqrt(E_mu-nu E^mu-nu)/a0^2 = (c/v_f)^2 on the
   transition locus, v_f = (G M a0)^(1/4).   Deep-MOND limit and BTFR are untouched BY
   CONSTRUCTION (nu_n asymptotics are n-independent, and Z -> 0 as g -> 0).

For every (n0, beta):
   * SPARC  -2lnL  from the cached per-galaxy profile curves (exact, not a refit)
   * the SAME law extrapolated to the Sun gives n_sun, hence Q2 via Milgrom's exact q
     and DHF Eq.10.
The question is whether the two allowed regions INTERSECT, and what the RAR costs there.

RUN AT BOTH FOOTINGS: DHF's fitted a0, and the framework's own
   a0 = kappa c sqrt(G rho_Lambda) = c^2 sqrt(Lambda/32pi) = 9.3619e-11 m/s^2.
"""
import os, sys, json, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq, minimize
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n
import gate2_dhf_faithful_2026 as B
from gate2_dhf_faithful_2026 import gal_m2lnL, gal_mbar, Fit
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def check(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True); return c
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
G_,MSUN,C=6.6743e-11,1.98892e30,2.99792458e8
GM_SUN=G_*MSUN
Q2_MU,Q2_SD=3.0e-27,3.0e-27
GEXT=2.00e-10                       # [DHF Sec3.3] conservative choice
SIG=0.034
NGRID=np.geomspace(0.35,60.0,38); lnN=np.log(NGRID)

def q_exact(nu,eN,nv=8000,nxi=192):
    xg,wg=leggauss(nxi); v=np.geomspace(1e-7,1e7,nv)
    V,X=np.meshgrid(v,xg,indexing="ij")
    w=np.sqrt(np.maximum(eN**2+V**4+2.0*eN*V**2*X,1e-24))
    return 3.0*np.trapz(((nu(w)-1.0)*(eN*0.5*(5*X**3-3.0*X)+V**2*0.5*(3*X**2-1.0)))@wg,v)
def eN_of(nu,et):
    f=lambda t: t*float(np.atleast_1d(nu(np.array([t])))[0])-et
    hi=max(4.0*et,4.0)
    while f(hi)<0: hi*=2.0
    return brentq(f,1e-10,hi,xtol=1e-14,rtol=1e-14)
def Q2_of(n,a0):
    nu=lambda y: nu_n(y,n)
    return 1.5*a0**1.5/np.sqrt(GM_SUN)*q_exact(nu,eN_of(nu,GEXT/a0))

gals,_=B.load_galaxies(B.load_master())
FOOT=[("DHF fitted",1.08e-10),("framework a0 = (c/2)sqrt(G rho_Lam)",9.3619e-11)]
OUT={}
for fname,a0 in FOOT:
    head(f"FOOTING: {fname}   a0 = {a0:.4e} m/s^2")
    t0=time.time()
    Cv=np.zeros((len(gals),len(NGRID))); w={x["name"]:Fit.P0.copy() for x in gals}
    for k,x in enumerate(gals):
        p=w[x["name"]].copy()
        for j,n in enumerate(NGRID):
            r=minimize(lambda pp: gal_m2lnL(x,pp,float(n),a0,SIG),p,method="Nelder-Mead",
                       options=dict(maxiter=700,xatol=3e-4,fatol=3e-4))
            p=r.x; Cv[k,j]=r.fun
        w[x["name"]]=p
    mb=np.array([gal_mbar(x,w[x["name"]]) for x in gals])
    vf=(G_*mb*a0)**0.25; Zg=(C/vf)**2
    vfS=(GM_SUN*a0)**0.25; ZS=(C/vfS)**2
    Z0=np.exp(np.mean(np.log(Zg)))
    zg=np.log(Zg/Z0); zS=float(np.log(ZS/Z0))
    info("A1  curves built",f"{time.time()-t0:.0f} s;  Z_sun/Z_pivot = {np.exp(zS):.3e}  "
                             f"(ln = {zS:.2f});  SPARC ln Z spans {zg.max()-zg.min():.2f}")
    def m2(ln_n0,beta):
        a=ln_n0+beta*zg
        idx=np.clip(np.searchsorted(lnN,a)-1,0,len(lnN)-2)
        t=np.clip((a-lnN[idx])/(lnN[idx+1]-lnN[idx]),0.0,1.0)
        pen=np.where((a<lnN[0])|(a>lnN[-1]),1e3,0.0)
        return float((Cv[np.arange(len(a)),idx]*(1-t)+Cv[np.arange(len(a)),idx+1]*t+pen).sum())
    LN0=np.log(np.geomspace(0.5,3.0,120)); BET=np.linspace(-0.05,0.45,101)
    S=np.array([[m2(l,b) for b in BET] for l in LN0])
    S-=S.min()
    head(f"  PART A -- the RAR-allowed region  ({fname})")
    i,j=np.unravel_index(np.argmin(S),S.shape)
    info("A2  joint best fit",f"n0 = {np.exp(LN0[i]):.3f}   beta = {BET[j]:+.4f}")
    b0=S[:,int(np.argmin(np.abs(BET)))].min()
    info("A3  universal-n (beta=0) cost",f"Delta chi2 = {b0:+.2f}")
    head(f"  PART B -- the SAME law extrapolated to the Sun  ({fname})")
    nsun=lambda l,b: float(np.clip(np.exp(l+b*zS),0.35,400.0))
    NS=sorted({round(nsun(l,b),3) for l in LN0[::4] for b in BET[::3]})
    NS=[x for x in NS if 0.4<x<300]
    qq={}
    for n in NS: qq[n]=Q2_of(n,a0)
    kn=np.array(sorted(qq)); kv=np.array([qq[x] for x in kn])
    Q2grid=np.exp(np.interp(np.log([[nsun(l,b) for b in BET] for l in LN0]),
                            np.log(kn),np.log(kv)))
    sig=(Q2grid-Q2_MU)/Q2_SD
    info("B1  Q2 at the RAR best fit",f"n_sun = {nsun(LN0[i],BET[j]):.2f}   "
         f"Q2 = {Q2grid[i,j]*1e27:.2f}e-27   ({sig[i,j]:+.1f} sigma vs Cassini)")
    info("B2  Q2 for universal n (beta=0, best n0)",
         f"{Q2grid[int(np.argmin(S[:,int(np.argmin(np.abs(BET)))])),int(np.argmin(np.abs(BET)))]*1e27:.2f}e-27")
    head(f"  PART C -- DO THE TWO REGIONS INTERSECT?  ({fname})")
    CAL=2.23      # permutation-measured: the profile Delta chi2 is optimistic by this factor
    for lab,thr in (("1 sigma",1.0*CAL**2),("2 sigma",4.0*CAL**2),("3 sigma",9.0*CAL**2)):
        rar=S<=thr
        cas=np.abs(sig)<=2.0
        both=rar&cas
        if both.any():
            bb=BET[np.where(both)[1]]; nn=np.exp(LN0[np.where(both)[0]])
            k=np.argmin(S[both])
            info(f"C1  RAR {lab} AND Cassini 2 sigma",
                 f"INTERSECT: {both.sum()} grid cells; beta in [{bb.min():+.3f}, {bb.max():+.3f}], "
                 f"n0 in [{nn.min():.2f}, {nn.max():.2f}]")
            si,sj=np.where(both); kk=np.argmin(S[si,sj])
            info(f"    cheapest reconciling point",
                 f"n0 = {np.exp(LN0[si[kk]]):.3f}, beta = {BET[sj[kk]]:+.4f}, "
                 f"n_sun = {nsun(LN0[si[kk]],BET[sj[kk]]):.2f}, "
                 f"Q2 = {Q2grid[si[kk],sj[kk]]*1e27:.2f}e-27, "
                 f"RAR cost Delta chi2 = {S[si[kk],sj[kk]]:.2f}")
        else:
            info(f"C1  RAR {lab} AND Cassini 2 sigma","NO INTERSECTION")
    rar1=S<=1.0*CAL**2
    info("C2  RAR 1sigma beta range",f"[{BET[np.where(rar1)[1]].min():+.3f}, "
                                      f"{BET[np.where(rar1)[1]].max():+.3f}]")
    cas=np.abs(sig)<=2.0
    info("C3  Cassini 2sigma requires",f"beta >= {BET[np.where(cas)[1]].min():+.3f} "
         f"(at some n0);  n_sun >= {min(nsun(LN0[a],BET[b]) for a,b in zip(*np.where(cas))):.2f}")
    OUT[fname]=dict(a0=a0,n0=float(np.exp(LN0[i])),beta=float(BET[j]),
                    lnZ_sun=zS,lnZ_span=float(zg.max()-zg.min()),
                    beta0_cost=float(b0),
                    intersect_2sig=bool(((S<=4*CAL**2)&(np.abs(sig)<=2.0)).any()),
                    intersect_1sig=bool(((S<=1*CAL**2)&(np.abs(sig)<=2.0)).any()))
json.dump(OUT,open("gate4b_result.json","w"),indent=1)
head("VERDICT")
for k,v in OUT.items():
    info(k,f"a0={v['a0']:.4e}  RAR best (n0={v['n0']:.3f}, beta={v['beta']:+.3f})  "
           f"beta=0 costs {v['beta0_cost']:.1f}  "
           f"intersect@1sig={v['intersect_1sig']}  @2sig={v['intersect_2sig']}")
