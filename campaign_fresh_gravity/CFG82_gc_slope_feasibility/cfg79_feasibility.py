#!/usr/bin/env python3
"""CFG79 STEP 1 feasibility diagnostics (no estimate of gamma is claimed).
Question: can per-galaxy GC tracer density slopes be estimated UNBIASED from on-disk data?
Diagnostics only: (a) which columns exist, (b) per-galaxy Rgal range/N, (c) azimuthal coverage vs radius (mask footprint),
(d) naive truncated power-law MLE of the spectroscopic surface density and how it moves with the coverage cut.
Reuses the CFG76 sample definition by importing nothing from the repo (re-parses the two TSV files)."""
import math, numpy as np, re
DATA="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"
def read(f):
    L=[l.rstrip("\n") for l in open(f"{DATA}/{f}",encoding="latin-1") if l.strip() and not l.startswith("#")]
    i=next(k for k,l in enumerate(L) if set(l.replace("\t","").strip())<=set("- "))
    h=[x.strip() for x in L[i-2].split("\t")]; return h,[l.split("\t") for l in L[i+1:]]
hg,rg=read("sluggs_forbes2017_galaxies.tsv"); hv,rv=read("sluggs_forbes2017_gcvel.tsv")
print("galaxy table columns:",hg); print("GC velocity table columns:",hv)
G={}
for r in rg:
    d=dict(zip(hg,[x.strip() for x in r])); G[int(d["NGC"])]=dict(Re=float(d["Reff"])/60.,ra=float(d["RAJ2000"]),de=float(d["DEJ2000"]),N=int(d["N"]))
GC={n:[] for n in G}
for r in rv:
    d=dict(zip(hv,[x.strip() for x in r])); m=re.match(r"NGC(\d+)_",d["Star"]); n=int(m.group(1))
    try: ra=float(d["RAJ2000"]);de=float(d["DEJ2000"]);R=float(d["Rgal"])
    except: continue
    g=G[n]; dx=(ra-g["ra"])*math.cos(math.radians(de))*60; dy=(de-g["de"])*60
    GC[n].append((R,math.degrees(math.atan2(dy,dx))%360,math.hypot(dx,dy)))
print("\nNGC   N   Rmin  Rmed  Rmax(arcmin) Re(arcmin) | occupied 30deg-sector fraction in Rgal bins [<Re, Re-2Re, 2-4Re, >4Re] | naive MLE gamma (R>1.0Re,truncated at Rmax): all / occupied-sector-only")
def mle_gamma(R,Rlo,Rhi):
    R=R[(R>=Rlo)&(R<=Rhi)]
    if len(R)<10: return np.nan
    # projected density Sigma ~ R^-s, pdf(R) ~ R^(1-s) on [Rlo,Rhi]; s = gamma-1
    from scipy.optimize import brentq
    lr=np.log(R)
    def sc(s):
        a=2-s
        if abs(a)<1e-9: mean=(np.log(Rhi)+np.log(Rlo))/2
        else: mean=(Rhi**a*np.log(Rhi)-Rlo**a*np.log(Rlo))/(Rhi**a-Rlo**a)-1/a
        return -mean*len(R)+... if False else (-lr.sum()) - (-len(R)*mean)  # d/ds loglik = -sum(lnR)+n*mean
    f=lambda s: -lr.sum()+len(R)*((Rhi**(2-s)*np.log(Rhi)-Rlo**(2-s)*np.log(Rlo))/(Rhi**(2-s)-Rlo**(2-s))-1/(2-s) if abs(2-s)>1e-9 else (np.log(Rhi)+np.log(Rlo))/2)
    try: return brentq(f,-1.5,6.0)+1
    except: return np.nan
for n in sorted(G):
    a=np.array(GC[n]);
    if len(a)<30: continue
    R=a[:,0];th=a[:,1];Re=G[n]["Re"]
    occ=[]
    edges=[0,Re,2*Re,4*Re,1e9]
    for i in range(4):
        m=(R>=edges[i])&(R<edges[i+1])
        occ.append(len(np.unique((th[m]//30).astype(int)))/12 if m.sum() else np.nan)
    g_all=mle_gamma(R,Re,R.max())
    # occupied-sector-only: keep sectors that are occupied in the outermost bin (a crude coverage cut)
    m=R>=2*Re; sec=set((th[m]//30).astype(int)) if m.sum()>0 else set()
    keep=np.array([int(t//30) in sec for t in th]); g_occ=mle_gamma(R[keep],Re,R.max())
    print(f"{n:5d} {len(a):4d} {R.min():5.1f} {np.median(R):5.1f} {R.max():6.1f}   {Re:5.2f}  | "+" ".join("%.2f"%o for o in occ)+f" | {g_all:5.2f} / {g_occ:5.2f}")
