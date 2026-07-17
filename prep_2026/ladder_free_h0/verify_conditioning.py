import numpy as np, os, csv
C=2.99792458e8; Z=np.sqrt(32*np.pi/3); KPC=3.0856775814913673e19; UD,UB=0.5,0.7
DATA="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
MASTER="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_master_clean.csv"
A0C=9.36e-11
meta={r["name"]:dict(Q=int(r["Q"]),inc=float(r["inc"]),fD=int(r["fD"])) for r in csv.DictReader(open(MASTER))}
def load(n):
    fn=os.path.join(DATA,n+"_rotmod.dat")
    if not os.path.exists(fn): return None
    a=np.loadtxt(fn)
    if a.ndim==1 or a.shape[0]<5: return None
    r,vo,ev,vg,vd,vb=a[:,0],a[:,1],a[:,2],a[:,3],a[:,4],a[:,5]
    m=(r>0)&(vo>0)
    rm=r[m]*KPC; gbar=(vg[m]*np.abs(vg[m])+UD*vd[m]**2+UB*vb[m]**2)*1e6/rm
    return dict(r=r[m],vo=vo[m],ev=ev[m],gbar=gbar)
gal={}
for n in meta:
    if meta[n]["Q"]<=2 and 30<=meta[n]["inc"]<=85:
        d=load(n)
        if d is not None and np.all(d["gbar"]>0): gal[n]=d
# classify pairs by regime, record a0hat + theoretical sensitivity dlnR/dlna0
rows={"straddle":[],"deepdeep":[],"highhigh":[]}
for n in gal:
    d=gal[n];gb=d["gbar"];vo=d["vo"];ev=d["ev"];r=d["r"]
    good=np.where(ev<0.08*vo)[0]
    for ia in range(len(good)):
        for ib in range(ia+1,len(good)):
            i,j=good[ia],good[ib];a,b=gb[i],gb[j]
            if abs(np.log10(a/b))<0.5: continue
            Rv=(vo[i]/vo[j])**4*(r[j]/r[i])**2; dn=Rv*b-a
            if abs(dn)<1e-16: continue
            a0h=(a**2-Rv*b**2)/dn
            sens=abs(A0C*(b-a)/((a+A0C)*(b+A0C)))  # |dlnR/dlna0| at canonical a0
            lo,hi=min(a,b),max(a,b)
            if lo<A0C<hi: cls="straddle"
            elif hi<A0C: cls="deepdeep"
            else: cls="highhigh"
            rows[cls].append((a0h,sens))
for cls in ("straddle","deepdeep","highhigh"):
    arr=np.array(rows[cls]); v=arr[:,0]; s=arr[:,1]
    ph=(v>0)&(v<1e-8); vp=v[ph]
    print(f"{cls:9s} n={len(v):5d} phys={ph.sum():5d} | med a0={np.median(vp):.3e} "
          f"MAD/med={np.median(np.abs(vp-np.median(vp)))/np.median(vp):.2f} "
          f"| median |dlnR/dlna0|={np.median(s):.3f}")
print("\nInterpretation: |dlnR/dlna0|~O(1) => well-conditioned; ~0 => a0 drops out of R (singular).")
