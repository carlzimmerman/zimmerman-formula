#!/usr/bin/env python3
"""
MINE 2b -- a0 universality done the PUBLISHED way (Li+2018/Lelli+2017 method).
The per-galaxy a0 fit in mine2 is degenerate with M/L (slope artifact). The honest,
in-hand universality statistic is the RAR ORTHOGONAL/vertical residual scatter and
whether the OPTIMAL per-galaxy a0 correlates with galaxy properties once you control
for M/L freedom. Here: bin galaxies by an in-hand property and ask if the binned
best-fit a0 moves -- the clean 'is a0 universal' test.
"""
import glob, math, os
import numpy as np
from scipy.optimize import minimize_scalar
KPC_M=3.0856775814913673e19; KMS=1e3
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","real_research","data","sparc_data")
A0=9.36e-11
def gds(gb,a0): return np.sqrt(gb*gb+gb*a0)
def load(ml=0.70):
    gals=[]
    for p in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
        gb,go,w,vflat=[],[],[],[]
        rows=[]
        for line in open(p):
            s=line.strip()
            if not s or s.startswith("#"): continue
            q=s.split()
            if len(q)<6: continue
            try: r,vo,ev,vg,vd,vb=(float(q[i]) for i in range(6))
            except: continue
            if r<=0 or vo<=0 or ev<=0 or ev/vo>0.10: continue
            vbar2=vg*abs(vg)+ml*vd*abs(vd)+ml*vb*abs(vb)
            if vbar2<=0: continue
            rm=r*KPC_M
            gb.append(vbar2*KMS**2/rm); go.append((vo*KMS)**2/rm)
            w.append((math.log(10)*ev/vo)**-2); vflat.append(vo)
        if len(gb)>=4:
            gals.append((os.path.basename(p)[:-11],np.array(gb),np.array(go),np.array(w),np.max(vflat)))
    return gals
gals=load(0.70)
# bin by Vflat (mass proxy) into 5 bins; fit one a0 per bin (proper: M/L fixed, a0 shared)
vmax=np.array([g[4] for g in gals])
edges=np.percentile(vmax,[0,20,40,60,80,100])
print("a0 universality across mass (Vmax) bins -- shared-a0 weighted dex fit, Y=0.70 dS-Unruh:")
bina0=[]
for i in range(5):
    sel=[g for g in gals if edges[i]<=g[4]<=edges[i+1]+(1e-9 if i==4 else 0)]
    GB=np.concatenate([g[1] for g in sel]); GO=np.concatenate([g[2] for g in sel]); W=np.concatenate([g[3] for g in sel])
    def chi2(la0):
        m=np.log10(gds(GB,10**la0)); return np.sum(W*(np.log10(GO)-m)**2)
    r=minimize_scalar(chi2,bounds=(math.log10(3e-11),math.log10(3e-10)),method="bounded")
    # error via delta-chi2=1
    c0=r.fun
    from scipy.optimize import brentq
    f=lambda x:chi2(x)-c0-1
    lo=brentq(f,math.log10(3e-11),r.x); hi=brentq(f,r.x,math.log10(3e-10))
    a0b=10**r.x; sg=(hi-lo)/2
    bina0.append((10**r.x,sg))
    print(f"  Vmax {edges[i]:5.0f}-{edges[i+1]:5.0f} km/s ({len(sel):3d} gal): a0={a0b:.3e}  +/-{100*(10**sg-1):.1f}%")
a0v=np.array([b[0] for b in bina0]); a0e=np.array([b[1] for b in bina0])
la0=np.log10(a0v)
# chi2 of constant-a0 hypothesis across bins
wm=np.sum(la0/a0e**2)/np.sum(1/a0e**2)
chi2_const=np.sum(((la0-wm)/a0e)**2)
print(f"\n  constant-a0 across 5 mass bins: chi2={chi2_const:.2f} (4 dof) -> {'CONSISTENT' if chi2_const<9.49 else 'TENSION'}")
print(f"  max/min binned a0 ratio = {a0v.max()/a0v.min():.2f}  (universal if ~1)")
# spread of binned a0 in dex
print(f"  rms spread of binned log10(a0) = {np.std(la0,ddof=1):.4f} dex (= {100*(10**np.std(la0,ddof=1)-1):.1f}%)")
