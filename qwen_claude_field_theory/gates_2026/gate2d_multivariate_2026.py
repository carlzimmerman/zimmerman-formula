#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate2d_multivariate_2026.py -- Carl's decisive regression.

    ln n_i = c + beta_M ln M_i + beta_S ln Sigma_i + beta_B B_i + beta_V ln Vflat_i

evaluated against the cached per-galaxy profile curves L_i(n), so this is an exact
profile likelihood, not a refit.  The question is ONLY:

        is beta_M != 0 CONDITIONAL on surface brightness, bulge status, and an
        M/L-independent kinematic quantity?

Significance is permutation-calibrated, never chi2_1, because the two disagree here.
Note the conversion to the environmental exponent: T ~ M^{-1/2}, so n ~ T^beta means
beta = -2 beta_M.
"""
import os, sys, json
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import gate2_dhf_faithful_2026 as B
HERE=os.path.dirname(os.path.abspath(__file__))
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)
print(__doc__)
Z=np.load(os.path.join(HERE,"gate2b_curves.npz"),allow_pickle=True)
NGRID=Z["NGRID"]; lnN=np.log(NGRID); CS=[Z[f"C{i}"] for i in range(3)]
mbar=Z["mbar"]; names=list(Z["names"])
master=B.load_master(); gals,_=B.load_galaxies(master)
assert [g["name"] for g in gals]==names
MSUN=1.98892e30
lnM=np.log(mbar/MSUN)
lnS=np.log(np.array([max(g["SBdisk"],1.0) for g in gals]))
Bul=np.array([1.0 if g["hasbul"] else 0.0 for g in gals])
lnV=np.log(np.array([max(g["Vflat"],1.0) for g in gals]))
NAMES=["ln M_bar","ln Sigma_disk","bulge flag","ln V_flat"]
X=np.vstack([lnM,lnS,Bul,lnV]).T
Xs=(X-X.mean(0))/X.std(0)                     # standardised: coefficients comparable

def m2(theta,Xu,C):
    a=theta[0]+Xu@theta[1:]
    idx=np.clip(np.searchsorted(lnN,a)-1,0,len(lnN)-2)
    t=(a-lnN[idx])/(lnN[idx+1]-lnN[idx])
    t=np.clip(t,0.0,1.0)      # *** BUG FIX: idx was clipped but t was NOT, so arguments below
    # the n-grid were LINEARLY EXTRAPOLATED into steeply falling curves and the optimizer
    # manufactured unbounded likelihood.  That produced a spurious Delta chi2 = 155 against
    # the grid scan's 8.7.  With t clipped, the two implementations agree.
    v=C[np.arange(len(a)),idx]*(1-t)+C[np.arange(len(a)),idx+1]*t
    pen=np.where((a<lnN[0])|(a>lnN[-1]),1e3,0.0)
    return float(np.sum(v+pen))
def m2marg(theta,Xu):
    vs=np.array([m2(theta,Xu,C) for C in CS]); m=vs.min()
    return float(-2*np.log(np.exp(-0.5*(vs-m)).sum())+m)
_RNG=np.random.default_rng(7)
def _opt(f,x0):
    """Multi-start Nelder-Mead then Powell polish.  A single NM from zeros in 5-D was NOT
    converged -- it returned a joint optimum WORSE than its own profile, which is the
    signature of a stuck simplex.  This is the fix."""
    bestx,bestf=None,np.inf
    starts=[np.asarray(x0,float)]
    starts.append(np.zeros_like(starts[0]))
    for _ in range(10):
        starts.append(starts[0]+_RNG.normal(0,0.25,size=len(starts[0])))
    for s0 in starts:
        r=minimize(f,s0,method="Nelder-Mead",
                   options=dict(maxiter=20000,maxfev=20000,xatol=1e-6,fatol=1e-6))
        r=minimize(f,r.x,method="Powell",options=dict(maxiter=20000,xtol=1e-7,ftol=1e-7))
        if r.fun<bestf: bestx,bestf=r.x,r.fun
    return bestx,bestf

def best(Xu,fixed=None,x0=None):
    k=Xu.shape[1]
    if fixed is None:
        return _opt(lambda th: m2marg(th,Xu), x0 if x0 is not None else np.zeros(k+1))
    j,val=fixed
    def f(th):
        full=np.concatenate([th[:j+1],[val],th[j+1:]]); return m2marg(full,Xu)
    z0=np.zeros(k) if x0 is None else np.delete(np.asarray(x0,float),j+1)
    return _opt(f,z0)

head("PART A -- univariate, each predictor alone (standardised)")
uni={}
for j,nm in enumerate(NAMES):
    th,c=best(Xs[:,[j]]); _,c0=best(Xs[:,[j]],fixed=(0,0.0))
    uni[nm]=dict(beta=float(th[1]),dchi2=float(c0-c))
    info(f"A1  {nm:<16}",f"beta_std = {th[1]:+.4f}   Delta chi2 = {c0-c:+.2f}")

head("PART B -- THE MULTIVARIATE FIT (all four together)")
th,cF=best(Xs)
info("B1  intercept",f"{th[0]:+.4f}  -> n0 = {np.exp(th[0]):.3f}")
for j,nm in enumerate(NAMES): info(f"B2  beta_std[{nm:<14}]",f"{th[j+1]:+.4f}")
cond={}
for j,nm in enumerate(NAMES):
    _,c0=best(Xs,fixed=(j,0.0),x0=None)
    cond[nm]=float(c0-cF)
    info(f"B3  drop {nm:<16}",f"Delta chi2 = {c0-cF:+.2f}   <- CONDITIONAL evidence for this term")

bad=[n for n,v in cond.items() if v< -1e-6]
if bad:
    info("B4  *** CONVERGENCE FAILURE ***",f"dropping {bad} IMPROVED the fit -- the joint "
         "optimum is not the optimum. Results below are void.")
    sys.exit(2)
info("B4  convergence guard","every conditional Delta chi2 >= 0: the joint optimum is "
     "genuinely the optimum, so the conditional numbers are interpretable")

head("PART C -- permutation calibration of the CONDITIONAL beta_M")
rng=np.random.default_rng(20260821)
nulls=np.empty(250)
for it in range(250):
    Xp=Xs.copy(); Xp[:,0]=Xs[rng.permutation(len(Xs)),0]
    thp,cp=best(Xp); _,cp0=best(Xp,fixed=(0,0.0))
    nulls[it]=cp0-cp
obs=cond["ln M_bar"]
p=float(np.mean(nulls>=obs))
info("C1  null on conditional Delta chi2 for ln M_bar",
     f"median {np.median(nulls):.2f}  95th {np.percentile(nulls,95):.2f}  observed {obs:.2f}")
info("C2  *** conditional p-value for beta_M ***",f"{p:.4f}")

head("PART D -- collinearity: can these predictors even be separated?")
Cm=np.corrcoef(Xs.T)
print("        "+"".join(f"{n[:12]:>14}" for n in NAMES))
for i,n in enumerate(NAMES): print(f"  {n[:12]:<12}"+"".join(f"{Cm[i,j]:>14.3f}" for j in range(4)))
head("PART E -- conversion to the environmental exponent")
bM=float(th[1])/X.std(0)[0]                    # de-standardise: per unit ln M
beta_env=-2.0*bM
info("E1  beta_M (raw, per unit ln M_bar)",f"{bM:+.5f}")
info("E2  beta = -2 beta_M  (n ~ T^beta, T ~ M^-1/2)",f"{beta_env:+.5f}")
json.dump(dict(univariate=uni,multivariate={n:float(th[j+1]) for j,n in enumerate(NAMES)},
               conditional_dchi2=cond,perm_p_betaM=p,
               null95=float(np.percentile(nulls,95)),beta_M_raw=bM,beta_env=beta_env,
               corr=Cm.tolist()),
          open(os.path.join(HERE,"gate2d_result.json"),"w"),indent=1)
print("\n-> gate2d_result.json")
