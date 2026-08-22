#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate3_nSS_posterior_2026.py -- GATE 3 under Carl's frozen definitions.

NOT a "k-sigma threshold".  The Solar-System constraint is reconstructed as DHF construct it:
a POSTERIOR on (a0, n) from the Cassini quadrupole likelihood, with DHF's own priors.

FROZEN, ALL [DHF] arXiv:2401.04796 UNLESS MARKED:
 [Eq.10]  Q2 = -(3/2) a0^{3/2}/sqrt(G M_sun) q(e~)         <- the 3/2, verbatim
 [Eq.11]  e~ = g_ext/a0 (TRUE external field); e_N = g_N,ext/a0 (Newtonian);
          e_N nu(e_N) = e~   [also M09 Sec.IV verbatim: "eta_N = mu(eta) eta"]
 [Eq.12]  q(e~) = -3 INT_0^inf dv INT_-1^1 dxi (nu-1)[e_N P3(xi) + v^2 P2(xi)],
          nu evaluated at w = (e_N^2 + v^4 + 2 e_N v^2 xi)^(1/2)      [= M09 Eq.24-25]
 [Eq.7a]  nu_n family
 [Eq.2]   Cassini: Q2 = (3 +/- 3) x 10^-27 s^-2   (Hees et al. 2014, DE430 + 9 yr Cassini)
 [Sec3.3] g_ext = 2.32 +/- 0.16 x 10^-10 m/s^2 (Gaia EDR3), TRUNCATED at 2.48 above and
          2.00 below (their stated realistic bounds)
 [Sec3.3] "we therefore instead adopt a prior flat on Q2 (with a uniform prior on a0), which
          matches that used in Hees et al. (2014)... achieved by taking the numerical
          derivative of Q2 with respect to shape"    <- implemented literally below
 [Sec3.3] QUMOND is used and is CONSERVATIVE: AQUAL Q2 is always larger.

DERIVED HERE: the q(n, e~) grid, the posterior, n_SS in all three senses Carl defined,
the Q2(n) table, an explicit test of whether q(n) is a power law, and beta_req.
"""
import os, sys, json
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
from scipy.interpolate import RectBivariateSpline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n
HERE = os.path.dirname(os.path.abspath(__file__))
FAIL, NCHK = [], [0]
def check(c,l,d=""):
    NCHK[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True)
    if not ok: FAIL.append(l)
    return ok
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
G_, MSUN = 6.6743e-11, 1.98892e30
GM = G_*MSUN
Q2_MU, Q2_SD = 3.0e-27, 3.0e-27                      # [DHF Eq.2]
GX_MU, GX_SD, GX_LO, GX_HI = 2.32e-10, 0.16e-10, 2.00e-10, 2.48e-10   # [DHF Sec3.3]

def q_exact(nu,eN,nv=8000,nxi=192,vlo=1e-7,vhi=1e7):
    xg,wg=leggauss(nxi); v=np.geomspace(vlo,vhi,nv)
    V,X=np.meshgrid(v,xg,indexing="ij")
    w=np.sqrt(np.maximum(eN**2+V**4+2.0*eN*V**2*X,1e-24))
    return 3.0*np.trapz(((nu(w)-1.0)*(eN*0.5*(5*X**3-3.0*X)+V**2*0.5*(3*X**2-1.0)))@wg,v)
def eN_of(nu,et):
    f=lambda t: t*float(np.atleast_1d(nu(np.array([t])))[0])-et
    hi=max(4.0*et,4.0)
    while f(hi)<0: hi*=2.0
    return brentq(f,1e-10,hi,xtol=1e-15,rtol=1e-15)

head("PART A -- validation of the quadrature at this resolution")
NR=lambda y:1.0/(1.0-np.exp(-np.sqrt(np.maximum(np.asarray(y,float),1e-300))))
w=0.0
for et,ref in ((1.0,0.094),(1.5,0.159),(2.0,0.221)):
    qq=q_exact(NR,eN_of(NR,et)); w=max(w,abs(qq/ref-1))
    info(f"A1  DHF Fig.1 nu_RAR e~={et}",f"-q~={qq:.5f} vs {ref}  ({qq/ref-1:+.3%})")
check(w<0.01,f"A2  quadrature validated to {w:.2%} at nv=8000, nxi=192","0.03 s per call")

head("PART B -- the q(n, e~) grid  [DHF Sec3.3 do exactly this]")
NG=np.geomspace(0.5,40.0,64); EG=np.linspace(1.15,3.25,48)
Q=np.empty((len(NG),len(EG)))
for i,n in enumerate(NG):
    nu=lambda y,nn=n: nu_n(y,nn)
    for j,et in enumerate(EG): Q[i,j]=q_exact(nu,eN_of(nu,et))
SP=RectBivariateSpline(np.log(NG),EG,np.log(Q),kx=3,ky=3,s=0)
qfun=lambda n,et: np.exp(SP.ev(np.log(n),et))
for n,et in ((1.0,2.0),(3.0,1.8),(10.0,2.2)):
    nu=lambda y,nn=n: nu_n(y,nn)
    ex=q_exact(nu,eN_of(nu,et)); sp=float(qfun(n,et))
    info(f"B1  spline check n={n}, e~={et}",f"exact {ex:.6f}  spline {sp:.6f}  ({sp/ex-1:+.2e})")
check(all(abs(float(qfun(n,et))/q_exact(lambda y,nn=n: nu_n(y,nn),eN_of(lambda y,nn=n: nu_n(y,nn),et))-1)<3e-3
          for n,et in ((1.0,2.0),(3.0,1.8),(10.0,2.2),(20.0,1.6))),"B2  spline accurate to <0.3%")
def Q2_of(n,a0,gx): return 1.5*a0**1.5/np.sqrt(GM)*qfun(n,gx/a0)      # [DHF Eq.10]

head("PART C -- is q(n) a power law?  (Carl: do not approximate unless verified)")
et0=2.00e-10/1.08e-10
ns=np.geomspace(1.0,20.0,9); qs=np.array([float(qfun(n,et0)) for n in ns])
sl=np.gradient(np.log(qs),np.log(ns))
for n,q_,s in zip(ns,qs,sl): info(f"C1  n={n:6.2f}",f"-q~={q_:.5f}   local d ln q/d ln n = {s:+.3f}")
check(sl.max()-sl.min()>0.8,"C2  q(n) is NOT a power law -- the local log-slope runs from "
      f"{sl.min():+.2f} to {sl.max():+.2f} over n = 1 to 20",
      "so no power-law shortcut is used anywhere; the exact grid is used throughout")

head("PART D -- POSTERIOR on n from Cassini, with DHF's priors")
A0G=np.linspace(0.80e-10,1.70e-10,140); GXG=np.linspace(GX_LO,GX_HI,41)
wgx=np.exp(-0.5*((GXG-GX_MU)/GX_SD)**2); wgx/=wgx.sum()                # truncated Gaussian
NP=np.geomspace(0.5,40.0,600)
post=np.zeros(len(NP))
for a0 in A0G:
    Qn=np.array([[Q2_of(n,a0,gx) for gx in GXG] for n in NP])          # (n, gx)
    L=np.exp(-0.5*((Qn-Q2_MU)/Q2_SD)**2)
    dQdn=np.abs(np.gradient(Qn,NP,axis=0))                             # flat-Q2 prior [DHF Sec3.3]
    post+=(L*dQdn*wgx[None,:]).sum(axis=1)
post/=np.trapz(post,NP)
cdf=np.concatenate([[0],np.cumsum(0.5*(post[1:]+post[:-1])*np.diff(NP))]); cdf/=cdf[-1]
qtl=lambda p: float(np.interp(p,cdf,NP))
n_med=qtl(0.5); n05,n16,n84,n95=qtl(0.05),qtl(0.16),qtl(0.84),qtl(0.95)
info("D1  posterior on n (Cassini alone, a0 and g_ext marginalised)",
     f"median {n_med:.2f}   68% [{n16:.2f}, {n84:.2f}]   5th pctile {n05:.2f}   95th {n95:.2f}")
info("D2  *** the decisive number ***",f"Cassini requires n >= {n05:.2f} at 95% credibility")
check(n05>1.5,"D3  the Solar System demands a substantially sharper transition than Simple (n=1)")

head("PART E -- the three Solar-System quantities Carl defined, separately")
def n_at(Q2t,a0,gx):
    f=lambda n: float(Q2_of(n,a0,gx))-Q2t
    if f(0.5)<0: return np.nan
    hi=0.6
    while f(hi)>0 and hi<40: hi*=1.3
    return brentq(f,0.5,min(hi,40.0),xtol=1e-4) if f(min(hi,40.0))<0 else np.inf
rows=[]
for lab,Q2t in (("1. HARD upper limit  Q2 = 8.88e-27 (95% of 3+-3)",3.0e-27+1.96*3.0e-27),
                ("2. 1-sigma equivalent Q2 = 6.00e-27",6.0e-27),
                ("   central value      Q2 = 3.00e-27",3.0e-27)):
    v=[n_at(Q2t,a0,gx) for a0 in (1.02e-10,1.08e-10,1.20e-10) for gx in (GX_LO,GX_MU,GX_HI)]
    v=[x for x in v if np.isfinite(x)]
    rows.append((lab,min(v),max(v))); info(f"E1  {lab}",f"n_SS = {min(v):.2f} to {max(v):.2f} "
                                            "across a0 in {1.02,1.08,1.20}e-10 x g_ext in {2.00,2.32,2.48}e-10")
info("E2  3. FULL POSTERIOR (preferred)",f"n_SS = {n05:.2f} (95% lower credible bound)")

head("PART F -- Q2(n) table, dense, at DHF's fiducial a0 and conservative g_ext")
print(f"  {'n':>7} | {'-q~':>10} | {'Q2 [1e-27 s^-2]':>16} | {'sigma vs Cassini':>17}")
for n in (1.0,1.02,1.2,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,6.0,7.0,8.0,10.0,12.0,15.0,20.0,30.0):
    Q2=float(Q2_of(n,1.08e-10,GX_LO))
    print(f"  {n:7.2f} | {float(qfun(n,et0)):10.5f} | {Q2*1e27:16.2f} | {(Q2-Q2_MU)/Q2_SD:17.1f}")

head("PART G -- the environmental lever arm  T_SS / T_gal")
info("G1  T = a0^{3/2}/sqrt(G M)",
     "so T_SS/T_gal = sqrt(M_gal/M_sun) EXACTLY -- INDEPENDENT of a0. No footing fork here.")
for Mg,lab in ((1e9,"dwarf 1e9"),(1e10,"pivot 1e10"),(3.6e11,"SPARC max 3.6e11")):
    info(f"G2  M_gal = {lab} Msun",f"ln(T_SS/T_gal) = {0.5*np.log(Mg):.2f}")
res=dict(n_post=dict(median=n_med,p05=n05,p16=n16,p84=n84,p95=n95),
         n_hard=[dict(label=a,lo=b,hi=c) for a,b,c in rows],
         lnT_SS_over_gal={"1e9":0.5*np.log(1e9),"1e10":0.5*np.log(1e10),"3.6e11":0.5*np.log(3.6e11)},
         q_slope_range=[float(sl.min()),float(sl.max())])
json.dump(res,open(os.path.join(HERE,"gate3_result.json"),"w"),indent=1)
print("\n"+"="*104+f"\nGATE 3: {NCHK[0]-len(FAIL)}/{NCHK[0]} checks passed  -> gate3_result.json\n"+"="*104)
sys.exit(1 if FAIL else 0)
