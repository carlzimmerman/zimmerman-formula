#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate2c_permcal_2026.py -- permutation calibration of beta-hat, vectorised.

Loads the cached per-galaxy profile curves L_i(n) and evaluates
    -2lnL(n0,beta) = SUM_i L_i(n0 exp(beta z_i))
on the full (n0,beta) grid for thousands of label permutations.  Gives the HONEST null
distribution of beta-hat and of Delta chi2, making no distributional assumption -- which
matters because the profile-likelihood error bar and the permutation spread disagree.
Also calibrates every control on the same footing.
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate2_dhf_faithful_2026 as B
HERE=os.path.dirname(os.path.abspath(__file__))
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
Z=np.load(os.path.join(HERE,"gate2b_curves.npz"),allow_pickle=True)
NGRID=Z["NGRID"]; lnN=np.log(NGRID)
CS=[Z[f"C{i}"] for i in range(3)]; mbar=Z["mbar"]; names=list(Z["names"])
A0G=[1.02e-10,1.08e-10,1.14e-10]; G_=6.6743e-11; MSUN=1.98892e30; M_PIVOT=1e10*MSUN
master=B.load_master(); gals,_=B.load_galaxies(master)
assert [g["name"] for g in gals]==names
N0=np.geomspace(0.5,4.0,90); BE=np.linspace(-0.35,0.35,141); lnN0=np.log(N0)
i0=int(np.argmin(np.abs(BE)))

def surface(z,C):
    """-2lnL on the (n0,beta) grid, vectorised over galaxies."""
    A=lnN0[:,None,None]+BE[None,:,None]*z[None,None,:]      # (i,j,k)
    idx=np.clip(np.searchsorted(lnN,A)-1,0,len(lnN)-2)
    x0=lnN[idx]; x1=lnN[idx+1]; t=(A-x0)/(x1-x0)
    out=np.zeros(A.shape[:2])
    for k in range(A.shape[2]):
        c=C[k]; out+=c[idx[:,:,k]]*(1-t[:,:,k])+c[idx[:,:,k]+1]*t[:,:,k]
    pen=np.where((A<lnN[0])|(A>lnN[-1]),1e3,0.0).sum(axis=2)
    return out+pen

def marg(z):
    acc=None
    for C in CS:
        G=surface(z,C)
        e=np.exp(-0.5*(G-G.min()))
        acc=e if acc is None else acc+e
    return -2*np.log(acc/acc.max())

def fit(z):
    S=marg(z); pr=S.min(axis=0); pr=pr-pr.min()
    return float(BE[np.argmin(pr)]), float(pr[i0]), pr

T=A0G[1]**1.5/np.sqrt(G_*mbar)
zmass=np.log(T/(A0G[1]**1.5/np.sqrt(G_*M_PIVOT))); zmass=zmass-zmass.mean()
bh,d2,pr=fit(zmass)
def band(pr,th):
    o=BE[pr<=th]; return (float(o.min()),float(o.max()))
head("PART A -- the mass model, re-derived on the cached curves")
info("A1  beta-hat",f"{bh:+.4f}   Delta chi2 = {d2:+.2f}")
info("A2  profile bands",f"1sigma {band(pr,1.0)}   2sigma {band(pr,4.0)}")

head("PART B -- permutation null (3000 label shuffles, identical grid)")
rng=np.random.default_rng(20260821)
nb=np.empty(3000); nd=np.empty(3000)
for it in range(3000):
    b_,d_,_=fit(rng.permutation(zmass)); nb[it]=b_; nd[it]=d_
p_b=float(np.mean(np.abs(nb)>=abs(bh))); p_d=float(np.mean(nd>=d2))
info("B1  null on beta-hat",f"mean {nb.mean():+.4f}  sd {nb.std(ddof=1):.4f}")
info("B2  null on Delta chi2",f"median {np.median(nd):.2f}  95th {np.percentile(nd,95):.2f}  "
                                f"99th {np.percentile(nd,99):.2f}")
info("B3  *** p-values ***",f"p(|beta| >= {abs(bh):.4f}) = {p_b:.4f}    "
                             f"p(Dchi2 >= {d2:.2f}) = {p_d:.4f}")
sig_prof=(band(pr,1.0)[1]-band(pr,1.0)[0])/2
info("B4  CALIBRATION",f"profile sigma_beta = {sig_prof:.4f}; permutation sd = {nb.std(ddof=1):.4f} "
     f"({nb.std(ddof=1)/sig_prof:.2f}x larger). The permutation number is the honest one.")
info("B5  Delta chi2 = 8.67 would be 2.9 sigma if chi2_1 applied",
     f"the permutation null says it is {p_d:.3f} -- i.e. {'NOT ' if p_d>0.05 else ''}significant")

head("PART C -- every control, permutation-calibrated on the same footing")
Vfl=np.array([max(g["Vflat"],1.0) for g in gals]); SBd=np.array([max(g["SBdisk"],1.0) for g in gals])
inc=np.array([g["inc"] for g in gals],float); D=np.array([g["D"] for g in gals],float)
Ty=np.array([g["T"] for g in gals],float); bul=np.array([1. if g["hasbul"] else 0. for g in gals])
CTRL=[("M_bar  (the theory variable, T ~ M^-1/2)",zmass),
      ("V_flat^-2  INDEPENDENT of the M/L fit",-2*np.log(Vfl/np.median(Vfl))),
      ("surface brightness SBdisk",np.log(SBd/np.median(SBd))),
      ("has bulge (0/1)",bul),
      ("distance D",np.log(D/np.median(D))),
      ("inclination sin i",np.log(np.sin(np.radians(inc)))),
      ("Hubble type T",(Ty-np.median(Ty))/5.0)]
res={}
print(f"  {'control':<42}{'beta':>9}{'Dchi2':>9}{'perm p':>9}{'null 95th':>11}")
for nm,zz in CTRL:
    zz=np.asarray(zz,float); zz=zz-zz.mean()
    if zz.std()>0: zz=zz/zz.std()*zmass.std()      # common scale so Dchi2 are comparable
    b_,d_,pp=fit(zz)
    nn=np.empty(800)
    for it in range(800): nn[it]=fit(rng.permutation(zz))[1]
    p=float(np.mean(nn>=d_))
    res[nm]=dict(beta=b_,dchi2=d_,p=p,null95=float(np.percentile(nn,95)))
    print(f"  {nm:<42}{b_:>+9.4f}{d_:>9.2f}{p:>9.3f}{np.percentile(nn,95):>11.2f}")

head("PART D -- is the mass variable even distinguishable from the controls?")
for nm,zz in CTRL[1:]:
    zz=np.asarray(zz,float)
    r=np.corrcoef(zmass,(zz-zz.mean())/max(zz.std(),1e-12))[0,1]
    info(f"D1  corr(z_mass, {nm[:38]:<38})",f"{r:+.3f}")
json.dump(dict(beta=bh,dchi2=d2,prof_1sig=band(pr,1.0),prof_2sig=band(pr,4.0),
               perm=dict(sd=float(nb.std(ddof=1)),p_beta=p_b,p_dchi2=p_d,n=3000,
                         null95=float(np.percentile(nd,95))),
               controls=res),
          open(os.path.join(HERE,"gate2c_result.json"),"w"),indent=1)
print("\n-> gate2c_result.json")
