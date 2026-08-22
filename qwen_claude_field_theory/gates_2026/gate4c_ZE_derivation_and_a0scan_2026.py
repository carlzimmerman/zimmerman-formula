#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate4c -- (i) DERIVE Z_E from the invariant, not from a fitted velocity;
          (ii) the price the Solar System imposes on the galaxy fit, exactly;
          (iii) the a0 scan, because beta and a0 are degenerate and that must be shown.

Carl's correction, taken literally: Z_E = c^4 sqrt(E_mu-nu E^mu-nu)/a0^2, with E the
ELECTRIC WEYL tensor, and the (c/v_inf)^2 scaling must COME OUT, not be put in.
"""
import os, sys, json, time
import numpy as np, sympy as sp
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
G_,MSUN,C=6.6743e-11,1.98892e30,2.99792458e8; GM_SUN=G_*MSUN
Q2_MU,Q2_SD=3.0e-27,3.0e-27; GEXT=2.00e-10; SIG=0.034
NGRID=np.geomspace(0.35,60.0,38); lnN=np.log(NGRID)

head("PART A -- Z_E DERIVED from the electric Weyl tensor (sympy, weak-field vacuum)")
x,y,z,GMs,cs=sp.symbols('x y z GM c',positive=True)
r=sp.sqrt(x**2+y**2+z**2); Phi=-GMs/r
X=[x,y,z]
H=sp.Matrix(3,3,lambda i,j: sp.simplify(sp.diff(Phi,X[i],X[j])))
lap=sp.simplify(sum(H[i,i] for i in range(3)))
check(sp.simplify(lap)==0,"A1  vacuum: Laplacian Phi = 0, so E_ij = d_i d_j Phi / c^2 is already trace-free",
      "no trace subtraction needed outside the source")
E=H/cs**2
EE=sp.simplify(sum(E[i,j]**2 for i in range(3) for j in range(3)))
info("A2  E_ij E^ij",f"= {sp.simplify(EE)}")
target=6*GMs**2/(cs**4*r**6)
check(sp.simplify(EE-target)==0,"A3  E_mu-nu E^mu-nu = 6 (GM)^2/(c^4 r^6)  -- DERIVED",
      "so sqrt(E.E) = sqrt(6) GM/(c^2 r^3): the tide, with an exact sqrt(6)")
a0s,RMs=sp.symbols('a_0 R_M',positive=True)
ZE=sp.simplify((cs**4*sp.sqrt(target)/a0s**2).subs(r,sp.sqrt(GMs/a0s)))
info("A4  Z_E at the MOND radius R_M = sqrt(GM/a0)",f"= {sp.simplify(ZE)}")
vinf=(GMs*a0s)**sp.Rational(1,4)
check(sp.simplify(ZE-sp.sqrt(6)*cs**2/vinf**2)==0,
      "A5  *** Z_E(R_M) = sqrt(6) (c/v_inf)^2 EXACTLY, with v_inf^4 = G M a0 ***",
      "the mass dependence is a CONSEQUENCE of the invariant, not an empirical definition. "
      "The sqrt(6) is a constant and is absorbed into Z_0, so beta is unaffected.")

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
def Q2_of(n,a0):
    nu=lambda yy: nu_n(yy,n)
    return 1.5*a0**1.5/np.sqrt(GM_SUN)*q_exact(nu,eN_of(nu,GEXT/a0))

gals,_=B.load_galaxies(B.load_master())
A0LIST=[9.3619e-11,1.00e-10,1.05e-10,1.08e-10,1.12e-10,1.18e-10,1.25e-10]
LN0=np.log(np.geomspace(0.5,3.5,110)); BET=np.linspace(-0.05,0.50,112)
head("PART B -- a0 scan.  beta and a0 ARE degenerate; this shows by how much.")
print(f"  {'a0/1e-10':>9} {'-2lnL(abs)':>12} {'D vs best':>10} {'n0':>7} {'beta':>8} "
      f"{'b=0 cost':>9} {'n_sun':>8} {'Q2/1e-27':>9} {'sig':>6}")
RES=[]
for a0 in A0LIST:
    Cv=np.zeros((len(gals),len(NGRID))); w={g["name"]:Fit.P0.copy() for g in gals}
    for k,g in enumerate(gals):
        p=w[g["name"]].copy()
        for j,n in enumerate(NGRID):
            rr=minimize(lambda pp: gal_m2lnL(g,pp,float(n),a0,SIG),p,method="Nelder-Mead",
                        options=dict(maxiter=700,xatol=3e-4,fatol=3e-4))
            p=rr.x; Cv[k,j]=rr.fun
        w[g["name"]]=p
    mb=np.array([gal_mbar(g,w[g["name"]]) for g in gals])
    ZEg=np.sqrt(6)*(C/(G_*mb*a0)**0.25)**2; ZES=np.sqrt(6)*(C/(GM_SUN*a0)**0.25)**2
    Z0=np.exp(np.mean(np.log(ZEg))); zg=np.log(ZEg/Z0); zS=float(np.log(ZES/Z0))
    def m2(l,b):
        a=l+b*zg; idx=np.clip(np.searchsorted(lnN,a)-1,0,len(lnN)-2)
        t=np.clip((a-lnN[idx])/(lnN[idx+1]-lnN[idx]),0,1)
        pen=np.where((a<lnN[0])|(a>lnN[-1]),1e3,0.0)
        return float((Cv[np.arange(len(a)),idx]*(1-t)+Cv[np.arange(len(a)),idx+1]*t+pen).sum())
    S=np.array([[m2(l,b) for b in BET] for l in LN0])
    i,j=np.unravel_index(np.argmin(S),S.shape); absmin=S.min()
    b0cost=S[:,int(np.argmin(np.abs(BET)))].min()-absmin
    nsun=float(np.clip(np.exp(LN0[i]+BET[j]*zS),0.35,400))
    Q2=Q2_of(nsun,a0)
    RES.append(dict(a0=a0,absmin=absmin,n0=float(np.exp(LN0[i])),beta=float(BET[j]),
                    b0cost=float(b0cost),nsun=nsun,Q2=float(Q2),zS=zS,
                    S=S,LN0=LN0,BET=BET,Cv=Cv,zg=zg))
    print(f"  {a0*1e10:9.4f} {absmin:12.1f} {'--':>10} {np.exp(LN0[i]):7.3f} {BET[j]:+8.3f} "
          f"{b0cost:9.1f} {nsun:8.2f} {Q2*1e27:9.2f} {(Q2-Q2_MU)/Q2_SD:+6.1f}")
best=min(r["absmin"] for r in RES)
for r in RES: r["dabs"]=r["absmin"]-best
head("PART B2 -- absolute fit quality across a0 (this is the honest footing comparison)")
for r in RES:
    info(f"B2  a0={r['a0']*1e10:.4f}e-10",f"Delta(-2lnL) vs the best a0 = {r['dabs']:+.1f}   "
         f"beta_best = {r['beta']:+.3f}")
info("B3  the degeneracy",f"beta_best runs {min(r['beta'] for r in RES):+.3f} to "
     f"{max(r['beta'] for r in RES):+.3f} across a0 in "
     f"[{min(A0LIST)*1e10:.2f}, {max(A0LIST)*1e10:.2f}]e-10 -- beta and a0 are STRONGLY degenerate")

head("PART C -- the exact price: RAR cost at the Cassini-compatible point")
for r in RES:
    if r["a0"] not in (9.3619e-11,1.08e-10): continue
    S,zS=r["S"],r["zS"]; Sm=S-S.min()
    NS=np.clip(np.exp(LN0[:,None]+BET[None,:]*zS),0.35,400)
    kn=np.geomspace(0.4,300,90); kv=np.array([Q2_of(n,r["a0"]) for n in kn])
    Q2g=np.exp(np.interp(np.log(NS),np.log(kn),np.log(kv)))
    head(f"  a0 = {r['a0']:.4e}")
    info("C1  unrestricted SPARC optimum",f"(n0, beta) = ({r['n0']:.3f}, {r['beta']:+.3f}), "
         f"Q2 = {r['Q2']*1e27:.2f}e-27 ({(r['Q2']-Q2_MU)/Q2_SD:+.1f} sigma)")
    for lab,cap in (("Q2 <= 9.0e-27 (Cassini +2sig)",9.0e-27),
                    ("Q2 <= 6.0e-27 (Cassini +1sig)",6.0e-27),
                    ("Q2 <= 3.0e-27 (Cassini central)",3.0e-27)):
        ok=Q2g<=cap
        if not ok.any(): info(f"C2  {lab:<34}","UNREACHABLE"); continue
        k=np.argmin(np.where(ok,Sm,np.inf))
        ii,jj=np.unravel_index(k,Sm.shape)
        info(f"C2  {lab:<34}",f"cheapest (n0, beta) = ({np.exp(LN0[ii]):.3f}, {BET[jj]:+.3f}); "
             f"n_sun = {NS[ii,jj]:.2f};  RAR PRICE Delta chi2 = {Sm[ii,jj]:.2f}")
json.dump([{k:v for k,v in r.items() if k not in ("S","LN0","BET","Cv","zg")} for r in RES],
          open("gate4c_result.json","w"),indent=1)
print("\n-> gate4c_result.json")
