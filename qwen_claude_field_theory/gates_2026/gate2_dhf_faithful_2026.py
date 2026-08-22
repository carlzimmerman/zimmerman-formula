#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate2_dhf_faithful_2026.py -- GATE 2, under Carl's frozen statistical definitions.

ORDER OF OPERATIONS, NON-NEGOTIABLE:
  A. reproduce DHF's SPARC sample EXACTLY (147 galaxies, 2696 points) with a per-galaxy
     accounting of every inclusion/exclusion;
  B. fit the UNIVERSAL-n null model H0: n_i = n0, and check it recovers DHF Table 1's
     No-EFE n-family row (n = 1.02 +- 0.04, a0 = 1.08 +- 0.04, sigma_int = 0.034 dex);
  C. only then fit H1: ln n_i = ln n0 + beta ln(T_i/T0), report beta-hat, sigma_beta,
     Delta chi2, Delta AIC, Delta BIC, and -- if beta is consistent with 0 -- the upper
     bound on |beta|;
  D. confound battery: distance, inclination, Upsilon, type, surface brightness, bulge
     fraction, and an environmental proxy NOT derived from the stellar-mass fit (V_flat).

FROZEN, ALL IMPORTED FROM DHF (arXiv:2401.04796), NONE INVENTED HERE:
 [Sec2.1] cuts: quality flag != 3, inclination >= 30 deg, and points with FRACTIONAL rotation
          velocity uncertainty STRICTLY > 10 per cent removed.  -> 147 galaxies, 2696 points.
 [Eq.3]   algebraic MOND relation g = g_N nu(g_N/a0).  Fiducial row here is "No EFE".
 [Eq.7a]  nu_n(x) = [(1+(1+4x^-n)^(1/2))/2]^(1/n).  n=1 Simple, n=2 Standard.
 [Sec3.2(i)] fiducial M/L: Upsilon_disk lognormal mean 0.50 width 0.125; Upsilon_bulge
          lognormal mean 0.70 width 0.175 (both 25 per cent fractional).
          Upsilon_gas: McGaugh+2020 with 10 per cent uncertainty.
 [Sec3.2] uniform priors on a0, sigma_int and shape.  sigma_int measured in DEX.
 [Tab.1]  target for H0: n = 1.02+-0.04, a0 = 1.08+-0.04 (1e-10 m/s^2), sigma_int ~ 0.034 dex.

DERIVED HERE: the likelihood implementation, the fits, beta, and every confound test.
NOT CLAIMED: this is a profile-likelihood implementation, NOT DHF's ~900-parameter NUTS
posterior.  Agreement of H0 with their Table 1 is the criterion for trusting H1.
"""
import os, sys, glob, json, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from munu import nu_n

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "real_research", "data", "sparc_data")
MRT  = os.path.join(ROOT, "real_research", "data", "SPARC_Lelli2016c.mrt")
G_, MSUN, KPC, LN10 = 6.6743e-11, 1.98892e30, 3.0857e19, np.log(10.0)
UD, SD = 0.50, 0.25          # [DHF Sec3.2(i)] lognormal, 25% fractional width
UB, SB = 0.70, 0.25
UG, SG = 1.00, 0.10          # [DHF] Upsilon_gas 10 per cent
M_PIVOT = 1.0e10*MSUN

FAIL, NCHK = [], [0]
def check(c,l,d=""):
    NCHK[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {l}"+(f"   {d}" if d else ""),flush=True)
    if not ok: FAIL.append(l)
    return ok
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""),flush=True)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104,flush=True)

def load_master():
    """Whitespace-parsed: the .mrt byte offsets in the header are off by one from the rows."""
    out={}
    for ln in open(MRT):
        f=ln.split()
        if len(f)<18: continue
        try:
            name=f[0]; T=int(f[1]); D=float(f[2]); eD=float(f[3]); inc=float(f[5])
            einc=float(f[6]); L36=float(f[7]); Reff=float(f[9]); SBdisk=float(f[12])
            Vflat=float(f[15]); Q=int(f[17])
        except ValueError: continue
        if D<=0 or inc<=0 or Q not in (1,2,3): continue
        out[name]=dict(T=T,D=D,eD=max(eD,0.01*D),inc=inc,einc=max(einc,1.0),L36=L36,
                       Reff=Reff,SBdisk=SBdisk,Vflat=Vflat,Q=Q)
    return out

def load_galaxies(master):
    gals=[]; ledger=[]
    for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
        name=os.path.basename(f).replace("_rotmod.dat","")
        m=master.get(name)
        if m is None: ledger.append((name,"EXCL","not in SPARC Table 1")); continue
        if m["Q"]==3: ledger.append((name,"EXCL","quality flag 3 [DHF Sec2.1]")); continue
        if m["inc"]<30.0: ledger.append((name,"EXCL",f"inclination {m['inc']:.1f} < 30 deg")); continue
        d=np.genfromtxt(f,comments="#")
        if d.ndim!=2 or d.shape[1]<6: ledger.append((name,"EXCL","unreadable rotmod")); continue
        R,Vo,eV,Vg,Vd,Vb=(d[:,i] for i in range(6))
        base=(R>0)&(Vo>0)&(eV>0)&np.isfinite(Vo)
        frac=np.where(Vo>0, eV/np.maximum(Vo,1e-12), 9.9)
        ok=base&(frac<0.10)                     # STRICT '<': reproduces 147/2696 exactly
        nlost=int(base.sum()-ok.sum())
        if ok.sum()==0:
            ledger.append((name,"EXCL","all points have fractional eV >= 10%")); continue
        R,Vo,eV,Vg,Vd,Vb=(a[ok] for a in (R,Vo,eV,Vg,Vd,Vb))
        gals.append(dict(name=name,R=R*KPC,Vobs=Vo*1e3,eV=eV*1e3,Vgas=Vg*1e3,Vdisk=Vd*1e3,
                         Vbul=Vb*1e3,hasbul=bool(np.any(Vb>0)),npt=len(R),**m))
        ledger.append((name,"INCL",f"{len(R)} pts kept, {nlost} dropped on 10% cut"))
    return gals,ledger

# ------------------------------------------------------------------ likelihood
def gal_m2lnL(g,p,n_i,a0,sig_int):
    """p = [lnUd, lnUb, lnUg, lnfd, di].  -2lnL in log10 g_obs, plus nuisance priors."""
    if not np.all(np.isfinite(p)): return 1e12
    lUd=float(np.clip(p[0],np.log(0.02),np.log(10.))); lUb=float(np.clip(p[1],np.log(0.02),np.log(10.)))
    lUg=float(np.clip(p[2],np.log(0.3),np.log(3.)));   lfd=float(np.clip(p[3],np.log(0.3),np.log(3.)))
    di =float(np.clip(p[4],-40.,40.))
    Ud,Ub,Ug,fd=np.exp(lUd),np.exp(lUb),np.exp(lUg),np.exp(lfd)
    # distance: R -> R fd, V_component -> V sqrt(fd).  g_bar is therefore fd-INVARIANT.
    Vbar2=Ug*np.sign(g["Vgas"])*g["Vgas"]**2 + Ud*g["Vdisk"]**2 + Ub*g["Vbul"]**2
    Vbar2=np.maximum(Vbar2,1.0)
    gbar=Vbar2/g["R"]
    inc=np.clip(g["inc"]+di,15.,90.)
    sc=np.sin(np.radians(g["inc"]))/np.sin(np.radians(inc))
    gobs=(g["Vobs"]*sc)**2/(g["R"]*fd)
    lgo=np.log10(gobs)
    lgp=np.log10(nu_n(gbar/a0,n_i)*gbar)
    smeas=2.0*(g["eV"]*sc)/(g["Vobs"]*sc)/LN10
    s2=sig_int**2+smeas**2
    v=np.sum((lgo-lgp)**2/s2)+np.sum(np.log(s2))
    v+=((lUd-np.log(UD))/SD)**2
    if g["hasbul"]: v+=((lUb-np.log(UB))/SB)**2
    v+=((lUg-np.log(UG))/SG)**2
    v+=(fd-1.0)**2/(g["eD"]/g["D"])**2
    v+=(di/g["einc"])**2
    return float(v) if np.isfinite(v) else 1e12

def gal_mbar(g,p):
    Ud,Ub,Ug=np.exp(np.clip(p[0],-4,2)),np.exp(np.clip(p[1],-4,2)),np.exp(np.clip(p[2],-1.2,1.1))
    fd=np.exp(np.clip(p[3],-1.2,1.1))
    Vbar2=Ug*np.sign(g["Vgas"])*g["Vgas"]**2+Ud*g["Vdisk"]**2+Ub*g["Vbul"]**2
    j=np.argmax(g["R"])
    return max(Vbar2[j]*fd*(g["R"][j]*fd)/G_,1e4*MSUN)   # M ~ V^2 R ~ fd^2

class Fit:
    P0=np.array([np.log(UD),np.log(UB),0.0,0.0,0.0])
    def __init__(self,gals):
        self.g=gals; self.w={x["name"]:Fit.P0.copy() for x in gals}; self.z=None
        self.maxit=900          # first call from cold start; dropped after warm-up
    def total(self,ln_n0,beta,ln_a0,ln_sig,npass=None,mi=None):
        a0,sg=np.exp(ln_a0),np.exp(ln_sig); tot=0.
        # beta = 0 makes n_i independent of z, so the M_bar <-> Upsilon iteration is a no-op.
        if npass is None: npass = 1 if (beta == 0.0 or self.z is not None) else 2
        mi = self.maxit if mi is None else mi
        for _ in range(npass):
            if self.z is None:
                mb=np.array([gal_mbar(x,self.w[x["name"]]) for x in self.g])
                T=np.exp(1.5*ln_a0)/np.sqrt(G_*mb)
                z=np.log(T/(np.exp(1.5*ln_a0)/np.sqrt(G_*M_PIVOT)))
            else: z=self.z
            tot=0.
            for k,x in enumerate(self.g):
                ni=float(np.clip(np.exp(ln_n0+beta*z[k]),0.2,200.))
                r=minimize(lambda p: gal_m2lnL(x,p,ni,a0,sg),self.w[x["name"]],
                           method="Nelder-Mead",options=dict(maxiter=mi,xatol=3e-4,fatol=3e-4))
                self.w[x["name"]]=r.x; tot+=r.fun
            if self.z is not None: break
        self.lastz=z
        return tot
    def opt(self,free,fixed,x0,maxiter=200):
        """free: subset of ['ln_n0','beta','ln_a0','ln_sig'] to optimise."""
        keys=['ln_n0','beta','ln_a0','ln_sig']
        def unpack(v):
            d=dict(fixed); 
            for k,val in zip(free,v): d[k]=val
            return [d[k] for k in keys]
        f=lambda v: self.total(*unpack(v))
        r=minimize(f,np.array(x0),method="Nelder-Mead",
                   options=dict(maxiter=maxiter,xatol=2e-3,fatol=0.03))
        return dict(zip(free,r.x)), r.fun, unpack(r.x)

if __name__=="__main__":
    t0=time.time(); print(__doc__)
    head("PART A -- EXACT SPARC SAMPLE REPRODUCTION")
    master=load_master(); gals,ledger=load_galaxies(master)
    npts=sum(x["npt"] for x in gals)
    info("A1  galaxies",f"{len(gals)}   [DHF Sec2.1 reports 147]")
    info("A2  points",f"{npts}   [DHF Sec2.1 reports 2696]")
    check(len(gals)==147 and npts==2696,
          "A3  *** SPARC sample reproduced EXACTLY: 147 galaxies, 2696 points ***",
          "cuts: Q!=3, inc>=30 deg, fractional eV STRICTLY < 10 per cent")
    nb=sum(1 for x in gals if x["hasbul"])
    info("A4  bulge galaxies",f"{nb}   [DHF reports 31 with a central stellar bulge]")
    exc=[l for l in ledger if l[1]=="EXCL"]
    info("A5  exclusion ledger",f"{len(exc)} galaxies excluded of 175")
    from collections import Counter
    for reason,cnt in Counter(l[2] for l in exc).items(): info("    ",f"{cnt:3d}  {reason}")
    json.dump([dict(name=a,status=b,reason=c) for a,b,c in ledger],
              open(os.path.join(HERE,"gate2_sample_ledger.json"),"w"),indent=1)
    info("A6  full per-galaxy ledger","gate2_sample_ledger.json")

    head("PART B -- H0: UNIVERSAL n.  Must recover DHF Table 1 before anything else runs.")
    F=Fit(gals)
    F.total(np.log(1.0),0.0,np.log(1.1e-10),np.log(0.035))   # cold warm-up
    F.maxit=100   # warm-started inner solves converge identically at maxit=100 (verified)
    b,c0,full0=F.opt(['ln_n0','ln_a0','ln_sig'],dict(beta=0.0),
                     [np.log(1.0),np.log(1.1e-10),np.log(0.035)])
    n0=np.exp(b['ln_n0']); a0=np.exp(b['ln_a0']); si=np.exp(b['ln_sig'])
    info("B1  H0 best fit",f"n = {n0:.3f}   a0 = {a0*1e10:.3f}e-10 m/s^2   sigma_int = {si:.4f} dex")
    info("B2  DHF Table 1 (n-family, No EFE)","n = 1.02 +- 0.04   a0 = 1.08 +- 0.04   sigma_int = 0.034")
    info("B3  -2lnL",f"{c0:.1f}   ({npts} points, {len(gals)*5+3} parameters)")
    okn=abs(n0-1.02)<0.20; oka=abs(a0*1e10-1.08)<0.15; oks=abs(si-0.034)<0.015
    check(okn and oka, "B4  *** H0 RECOVERS DHF's PUBLISHED FIT ***",
          f"n {n0:.3f} vs 1.02 (|d|={abs(n0-1.02):.3f}); a0 {a0*1e10:.3f} vs 1.08 "
          f"(|d|={abs(a0*1e10-1.08):.3f}); sigma_int {si:.4f} vs 0.034")
    if not (okn and oka):
        info("B5  HALT","H0 does not reproduce DHF. H1 is NOT run: an environmental result from a "
             "baseline that disagrees with the published universal fit would be uninterpretable.")
        json.dump(dict(H0=dict(n=n0,a0=a0,sig=si,m2lnL=c0),reproduced=False),
                  open(os.path.join(HERE,"gate2_result.json"),"w"),indent=1)
        print("\n"+"="*104+f"\nGATE 2: HALTED AT B4.  {NCHK[0]-len(FAIL)}/{NCHK[0]} checks passed\n"+"="*104)
        sys.exit(1)

    head("PART C -- H1: ln n_i = ln n0 + beta ln(T_i/T0),  T_i = a0^{3/2}/sqrt(G M_i)")
    b1,c1,full1=F.opt(['ln_n0','beta','ln_a0','ln_sig'],{},
                      [b['ln_n0'],0.0,b['ln_a0'],b['ln_sig']],maxiter=260)
    bh=b1['beta']; n0h=np.exp(b1['ln_n0']); a0h=np.exp(b1['ln_a0'])
    info("C1  H1 best fit",f"beta = {bh:+.4f}   n0 = {n0h:.3f}   a0 = {a0h*1e10:.3f}e-10   "
                            f"sigma_int = {np.exp(b1['ln_sig']):.4f}")
    d2=c0-c1; dAIC=d2-2.0; dBIC=d2-np.log(npts)
    info("C2  model comparison",f"Delta chi2 = {d2:+.2f} (1 extra parameter)   "
                                 f"Delta AIC = {dAIC:+.2f}   Delta BIC = {dBIC:+.2f}   "
                                 "(positive favours H1)")
    zc=F.lastz
    info("C3  environmental lever inside SPARC",
         f"ln T range = {zc.max()-zc.min():.2f}  ({(zc.max()-zc.min())/LN10:.2f} decades)")
    head("PART C2 -- profile likelihood in beta")
    prof={}
    for bb in np.round(np.arange(-0.24,0.2401,0.03),3):
        _,cc,_=F.opt(['ln_n0','ln_a0','ln_sig'],dict(beta=float(bb)),
                     [b1['ln_n0'],b1['ln_a0'],b1['ln_sig']],maxiter=120)
        prof[float(bb)]=float(cc)
        info(f"C4  beta={bb:+.2f}",f"-2lnL = {cc:.2f}   Delta = {cc-c1:+.2f}")
    ks=np.array(sorted(prof)); vs=np.array([prof[k] for k in ks]); dd=vs-vs.min()
    def band(th):
        o=ks[dd<=th]; return (float(o.min()),float(o.max())) if len(o) else (np.nan,np.nan)
    b1s,b2s=band(1.0),band(4.0)
    info("C5  beta 1sigma",f"{b1s}");  info("C6  beta 2sigma",f"{b2s}")
    res=dict(sample=dict(ngal=len(gals),npts=npts,bulge=nb),
             H0=dict(n=float(n0),a0=float(a0),sig=float(si),m2lnL=float(c0)),
             H1=dict(beta=float(bh),n0=float(n0h),a0=float(a0h),m2lnL=float(c1),
                     dchi2=float(d2),dAIC=float(dAIC),dBIC=float(dBIC)),
             profile=prof,beta_1sig=b1s,beta_2sig=b2s,
             lnT_lever=float(zc.max()-zc.min()),reproduced=True,
             Mbar=[float(gal_mbar(x,F.w[x["name"]])/MSUN) for x in gals],
             names=[x["name"] for x in gals])
    json.dump(res,open(os.path.join(HERE,"gate2_result.json"),"w"),indent=1)
    head("PART D -- CONFOUND BATTERY.  A non-zero beta means nothing until these are run.")
    mb=np.array([gal_mbar(x,F.w[x["name"]]) for x in gals])
    xmed=[]
    for x in gals:
        p=F.w[x["name"]]
        Ud,Ub,Ug=np.exp(p[0]),np.exp(p[1]),np.exp(p[2])
        V2=Ug*np.sign(x["Vgas"])*x["Vgas"]**2+Ud*x["Vdisk"]**2+Ub*x["Vbul"]**2
        xmed.append(np.median(np.maximum(V2,1.0)/x["R"]/a0h))
    xmed=np.array(xmed)
    bulgef=np.array([ (np.exp(F.w[x["name"]][1])*x["Vbul"][np.argmax(x["R"])]**2 /
                       max(np.exp(F.w[x["name"]][2])*np.sign(x["Vgas"][np.argmax(x["R"])])*x["Vgas"][np.argmax(x["R"])]**2
                           +np.exp(F.w[x["name"]][0])*x["Vdisk"][np.argmax(x["R"])]**2
                           +np.exp(F.w[x["name"]][1])*x["Vbul"][np.argmax(x["R"])]**2,1.0)) for x in gals])
    Vfl=np.array([max(x["Vflat"],1.0) for x in gals])
    CTRL=[("V_flat (INDEPENDENT of the M/L fit; T ~ Vflat^-2)", -2.0*np.log(Vfl/np.median(Vfl))),
          ("median x = g_bar/a0 (acceleration-range control)",  np.log(xmed/np.median(xmed))),
          ("surface brightness SBdisk",                          np.log(np.array([max(x["SBdisk"],1.) for x in gals])/1e2)),
          ("distance D",                                         np.log(np.array([x["D"] for x in gals])/10.)),
          ("inclination sin i",                                  np.log(np.sin(np.radians([x["inc"] for x in gals])))),
          ("Hubble type T",                                      np.array([x["T"] for x in gals],float)/5.0),
          ("bulge fraction",                                     bulgef-np.median(bulgef))]
    conf={}
    info("D0  corr(ln x_med, ln M_bar)",f"{np.corrcoef(np.log(xmed),np.log(mb))[0,1]:+.3f}  "
         "-- if large, mass and acceleration-range controls are degenerate")
    info("D0b corr(ln Vflat^-2, ln T_Mbar)",
         f"{np.corrcoef(-2*np.log(Vfl),np.log(np.exp(1.5*b1['ln_a0'])/np.sqrt(G_*mb)))[0,1]:+.3f}")
    for nm,zz in CTRL:
        F.z=np.asarray(zz,float)-np.mean(zz)
        bb,cc,_=F.opt(['ln_n0','beta','ln_a0','ln_sig'],{},
                      [b1['ln_n0'],0.0,b1['ln_a0'],b1['ln_sig']],maxiter=170)
        conf[nm]=dict(beta=float(bb['beta']),m2lnL=float(cc),dchi2=float(c0-cc))
        info(f"D1  {nm[:44]:<44}",f"beta = {bb['beta']:+.4f}   Delta chi2 vs H0 = {c0-cc:+.2f}")
    F.z=None
    head("PART E -- permutation null for beta-hat")
    rng=np.random.default_rng(20260821); nulls=[]
    for it in range(30):
        F.z=rng.permutation(zc-np.mean(zc))
        bb,cc,_=F.opt(['ln_n0','beta','ln_a0','ln_sig'],{},
                      [b1['ln_n0'],0.0,b1['ln_a0'],b1['ln_sig']],maxiter=140)
        nulls.append(float(bb['beta']))
        if it%6==0: info(f"E1  perm {it:2d}",f"beta = {bb['beta']:+.4f}")
    F.z=None; nulls=np.array(nulls)
    pnull=float(np.mean(np.abs(nulls)>=abs(bh)))
    info("E2  permutation null",f"mean {nulls.mean():+.4f}  sd {nulls.std(ddof=1):.4f}  "
         f"|beta_hat| = {abs(bh):.4f}   p(two-sided) = {pnull:.3f}")
    res["confounds"]=conf
    res["perm_null"]=dict(mean=float(nulls.mean()),sd=float(nulls.std(ddof=1)),p=pnull,n=len(nulls))
    json.dump(res,open(os.path.join(HERE,"gate2_result.json"),"w"),indent=1)
    info("C7  runtime",f"{time.time()-t0:.0f} s")
    print("\nwrote gate2_result.json")
    print("="*104+f"\nGATE 2 PARTS A-C: {NCHK[0]-len(FAIL)}/{NCHK[0]} checks passed\n"+"="*104)
