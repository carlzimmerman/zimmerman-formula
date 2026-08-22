#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate2b_profile_curves_2026.py -- GATE 2 by per-galaxy profile likelihood curves.

Same data, same priors, same likelihood as gate2_dhf_faithful_2026.py, but exact and fast:
for each galaxy compute the FULL profile curve  L_i(n) = min over its 5 nuisances of -2lnL,
on a dense n grid.  Then for ANY environmental model n_i = n0 exp(beta z_i),

        -2lnL(n0, beta) = SUM_i  L_i( n0 exp(beta z_i) )

is an interpolation, not a refit.  This is exact given (a0, sigma_int), and those two are
marginalised over a grid.  It also exposes, per galaxy, whether n is constrained AT ALL --
which the global fit hides.
"""
import os, sys, json, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate2_dhf_faithful_2026 as B
from gate2_dhf_faithful_2026 import load_master, load_galaxies, gal_m2lnL, gal_mbar, Fit, G_, MSUN, LN10
HERE=os.path.dirname(os.path.abspath(__file__))
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
NGRID=np.geomspace(0.35,40.0,34)
A0G=[1.02e-10,1.08e-10,1.14e-10]; SIG=0.034     # [DHF Tab.1] a0=1.08+-0.04, sigma_int=0.034 dex
M_PIVOT=1.0e10*MSUN

master=load_master(); gals,_=load_galaxies(master)
head("PART A -- per-galaxy profile curves L_i(n)")
t0=time.time(); CURVES={}; MBAR={}
for a0 in A0G:
    C=np.zeros((len(gals),len(NGRID))); w={x["name"]:Fit.P0.copy() for x in gals}
    for k,x in enumerate(gals):
        p=w[x["name"]].copy()
        for j,n in enumerate(NGRID):
            r=minimize(lambda pp: gal_m2lnL(x,pp,float(n),a0,SIG),p,method="Nelder-Mead",
                       options=dict(maxiter=700,xatol=3e-4,fatol=3e-4))
            p=r.x; C[k,j]=r.fun
        w[x["name"]]=p
        if a0==A0G[1]: MBAR[x["name"]]=gal_mbar(x,p)
    CURVES[a0]=C
    info(f"A1  a0={a0*1e10:.2f}e-10 done",f"{time.time()-t0:.0f} s cumulative")
np.savez(os.path.join(HERE,"gate2b_curves.npz"),NGRID=NGRID,
         **{f"C{i}":CURVES[a] for i,a in enumerate(A0G)},
         mbar=np.array([MBAR[x["name"]] for x in gals]),
         names=np.array([x["name"] for x in gals]))
C=CURVES[A0G[1]]
mb=np.array([MBAR[x["name"]] for x in gals])
T=A0G[1]**1.5/np.sqrt(G_*mb); z=np.log(T/(A0G[1]**1.5/np.sqrt(G_*M_PIVOT)))
head("PART B -- how many galaxies constrain n at all?")
d=C-C.min(axis=1,keepdims=True)
constr=np.array([ (d[k]>1.0).sum()>0 and (d[k].max()>4.0) for k in range(len(gals))])
info("B1  galaxies with Delta chi2 > 4 somewhere on the n grid",
     f"{int(constr.sum())} of {len(gals)}  -- the rest are effectively n-blind (deep-MOND only)")
nhat=NGRID[np.argmin(C,axis=1)]
info("B2  per-galaxy n-hat (constrained subset)",
     f"median {np.median(nhat[constr]):.2f}, 16-84 pct [{np.percentile(nhat[constr],16):.2f}, "
     f"{np.percentile(nhat[constr],84):.2f}]")
r=np.corrcoef(z[constr],np.log(nhat[constr]))[0,1]
info("B3  raw corr(ln n-hat, ln T) on the constrained subset",f"{r:+.3f}  (n = {int(constr.sum())})")

head("PART C -- the exact 2-D scan in (n0, beta), a0 and sigma_int marginalised")
def m2lnL(n0,beta,CC):
    tot=0.0
    for k in range(len(gals)):
        tot+=np.interp(np.log(n0)+beta*z[k],np.log(NGRID),CC[k],
                       left=CC[k][0]+1e3,right=CC[k][-1]+1e3)
    return tot
N0=np.geomspace(0.5,4.0,90); BE=np.linspace(-0.35,0.35,141)
S=np.zeros((len(N0),len(BE)))
for a0 in A0G:
    CC=CURVES[a0]
    G=np.array([[m2lnL(n0,b,CC) for b in BE] for n0 in N0])
    S+=np.exp(-0.5*(G-G.min()))
S=-2*np.log(S/S.max())
i,j=np.unravel_index(np.argmin(S),S.shape)
n0h,bh=N0[i],BE[j]
prof=S.min(axis=0)-S.min()
info("C1  best fit",f"n0 = {n0h:.3f}   beta = {bh:+.4f}")
info("C2  H0 (beta=0)",f"n0 = {N0[np.argmin(S[:,np.argmin(np.abs(BE))])]:.3f}   "
                        f"Delta chi2(H1-H0) = {prof[np.argmin(np.abs(BE))]:+.2f}")
def band(th):
    o=BE[prof<=th]; return (float(o.min()),float(o.max())) if len(o) else (np.nan,np.nan)
b1,b2,b3=band(1.0),band(4.0),band(9.0)
info("C3  beta 1sigma",f"[{b1[0]:+.4f}, {b1[1]:+.4f}]")
info("C4  beta 2sigma",f"[{b2[0]:+.4f}, {b2[1]:+.4f}]")
info("C5  beta 3sigma",f"[{b3[0]:+.4f}, {b3[1]:+.4f}]")
d2=prof[np.argmin(np.abs(BE))]
info("C6  model comparison",f"Delta chi2 = {d2:+.2f}  Delta AIC = {d2-2:+.2f}  "
                             f"Delta BIC = {d2-np.log(2696):+.2f}   (positive favours H1)")
info("C7  SPARC internal lever",f"ln T spans {z.max()-z.min():.2f} ({(z.max()-z.min())/np.log(10):.2f} decades)")

head("PART D -- controls with the SAME machinery (z replaced, curves reused)")
Vfl=np.array([max(x["Vflat"],1.0) for x in gals])
SBd=np.array([max(x["SBdisk"],1.0) for x in gals])
inc=np.array([x["inc"] for x in gals],float); D=np.array([x["D"] for x in gals],float)
Ty=np.array([x["T"] for x in gals],float); bul=np.array([1.0 if x["hasbul"] else 0.0 for x in gals])
CTRL=[("V_flat^-2  (INDEPENDENT of the M/L fit)",-2*np.log(Vfl/np.median(Vfl))),
      ("surface brightness SBdisk",np.log(SBd/np.median(SBd))),
      ("distance D",np.log(D/np.median(D))),
      ("inclination sin i",np.log(np.sin(np.radians(inc)))),
      ("Hubble type T",(Ty-np.median(Ty))/5.0),
      ("has bulge (0/1)",bul-bul.mean())]
zsave=z.copy(); ctrl={}
for nm,zz in CTRL:
    zz=np.asarray(zz,float); zz=zz-zz.mean(); z=zz
    acc=np.zeros((len(N0),len(BE)))
    for a0 in A0G:
        Gr=np.array([[m2lnL(n0,b,CURVES[a0]) for b in BE] for n0 in N0])
        acc+=np.exp(-0.5*(Gr-Gr.min()))          # <-- min subtracted: no overflow
    G=-2*np.log(acc/acc.max()); pr=G.min(axis=0)-G.min()
    bb=BE[np.argmin(pr)]; dc=pr[np.argmin(np.abs(BE))]
    ctrl[nm]=dict(beta=float(bb),dchi2=float(dc))
    info(f"D1  {nm[:44]:<44}",f"beta = {bb:+.4f}   Delta chi2 = {dc:+.2f}")
z=zsave
head("PART E -- permutation null (exact, since the curves are precomputed)")
rng=np.random.default_rng(20260821); nulls=[]; dnulls=[]
i0=int(np.argmin(np.abs(BE)))
for it in range(300):
    z=rng.permutation(zsave)
    pr=np.array([min(m2lnL(n0,b,C) for n0 in N0) for b in BE])
    pr=pr-pr.min()
    nulls.append(float(BE[np.argmin(pr)])); dnulls.append(float(pr[i0]))
z=zsave; nulls=np.array(nulls); dnulls=np.array(dnulls)
p_beta=float(np.mean(np.abs(nulls)>=abs(bh))); p_d=float(np.mean(dnulls>=d2))
info("E1  permutation null on beta-hat",f"mean {nulls.mean():+.4f}  sd {nulls.std(ddof=1):.4f}  "
     f"|beta_hat| = {abs(bh):.4f}  p(two-sided) = {p_beta:.4f}  (300 perms, SAME grid)")
info("E2  permutation null on Delta chi2",f"median {np.median(dnulls):.2f}  95th pct "
     f"{np.percentile(dnulls,95):.2f}  observed {d2:.2f}  p = {p_d:.4f}")
info("E3  CALIBRATION",f"profile 1sigma implies sigma_beta ~ {(b1[1]-b1[0])/2:.4f}; the "
     f"permutation null gives {nulls.std(ddof=1):.4f}, a factor "
     f"{nulls.std(ddof=1)/max((b1[1]-b1[0])/2,1e-9):.2f} LARGER. The permutation value is the "
     "honest one -- it assumes no distributional form. Quote it, not the profile.")
json.dump(dict(n0=float(n0h),beta=float(bh),beta_1sig=b1,beta_2sig=b2,beta_3sig=b3,
               dchi2=float(d2),dAIC=float(d2-2),dBIC=float(d2-np.log(2696)),
               lnT_lever=float(zsave.max()-zsave.min()),
               nconstrained=int(constr.sum()),ngal=len(gals),
               corr_lnn_lnT=float(r),controls=ctrl,
               perm=dict(sd=float(nulls.std(ddof=1)),p_beta=p_beta,p_dchi2=p_d,n=len(nulls),
                         dchi2_null_95=float(np.percentile(dnulls,95)))),
          open(os.path.join(HERE,"gate2b_result.json"),"w"),indent=1)
print(f"\nruntime {time.time()-t0:.0f} s -> gate2b_result.json")
