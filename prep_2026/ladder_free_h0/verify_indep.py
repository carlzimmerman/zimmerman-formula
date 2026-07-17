import numpy as np, sympy as sp, os, csv
g1,g2,a0,R=sp.symbols('g1 g2 a0 R',positive=True)
R_expr=(g1**2+g1*a0)/(g2**2+g2*a0)
a0_est=(g1**2-R*g2**2)/(R*g2-g1)
rec=sp.simplify(a0_est.subs(R,R_expr))
print("E4 algebra recovers a0 exactly?",sp.simplify(rec-a0)==0)
print("den(true a0)=",sp.simplify(R_expr*g2-g1)," (vanishes at g1=g2)")
C=2.99792458e8; Z=np.sqrt(32*np.pi/3); KPC=3.0856775814913673e19
KMSMPC=1e3/3.0856775814913673e22; H100=100*KMSMPC; UD,UB=0.5,0.7
DATA="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
MASTER="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_master_clean.csv"
A0C=9.36e-11; OL=0.6847; OMH2=0.1430
meta={}
for row in csv.DictReader(open(MASTER)):
    meta[row["name"]]=dict(Q=int(row["Q"]),inc=float(row["inc"]),fD=int(row["fD"]))
def load(n):
    fn=os.path.join(DATA,n+"_rotmod.dat")
    if not os.path.exists(fn): return None
    a=np.loadtxt(fn)
    if a.ndim==1 or a.shape[0]<5: return None
    r,vo,ev,vg,vd,vb=a[:,0],a[:,1],a[:,2],a[:,3],a[:,4],a[:,5]
    m=(r>0)&(vo>0); r,vo,ev,vg,vd,vb=r[m],vo[m],ev[m],vg[m],vd[m],vb[m]
    rm=r*KPC; gbar=(vg*np.abs(vg)+UD*vd**2+UB*vb**2)*1e6/rm; gobs=(vo*1e3)**2/rm
    return dict(r=r,rm=rm,vo=vo,ev=ev,gbar=gbar,gobs=gobs)
gal={}
for n in meta:
    if meta[n]["Q"]<=2 and 30<=meta[n]["inc"]<=85:
        d=load(n)
        if d is not None and np.all(d["gbar"]>0): gal[n]=d
print("loaded",len(gal),"galaxies (independent)")
def collect(subset=None,straddle=True,a0ref=A0C,sepmin=0.5,deepdeep=False):
    vals=[];prov=[];cond=[]
    for n in gal:
        if subset and meta[n]["fD"] not in subset: continue
        d=gal[n];gb=d["gbar"];vo=d["vo"];ev=d["ev"];r=d["r"]
        good=np.where(ev<0.08*vo)[0]
        for ia in range(len(good)):
            for ib in range(ia+1,len(good)):
                i,j=good[ia],good[ib];a,b=gb[i],gb[j]
                if abs(np.log10(a/b))<sepmin: continue
                if straddle and not (min(a,b)<a0ref<max(a,b)): continue
                if deepdeep and not (max(a,b)<a0ref): continue
                Rv=(vo[i]/vo[j])**4*(r[j]/r[i])**2; dn=Rv*b-a
                if abs(dn)<1e-16: continue
                a0h=(a**2-Rv*b**2)/dn; vals.append(a0h); prov.append(n)
                da=(a*b*(b-a))/dn**2
                cond.append(abs(da*0.01*Rv/a0h) if a0h!=0 else np.inf)
    return np.array(vals),np.array(prov),np.array(cond)
def med_phys(v):
    p=v[(v>0)&(v<1e-8)]; return (np.median(p),len(p)) if len(p) else (np.nan,0)
for tag,sub in [("ALL",None),("TRGB/Ceph",{2,3})]:
    v,p,c=collect(sub);m,nn=med_phys(v);cc=c[(v>0)&(v<1e-8)]
    print(f"[{tag}] median a0={m:.3e} n={nn} gals={len(np.unique(p))} medcond(1%R)={np.median(cc):.3f}")
vs,ps,cs=collect(None,straddle=True)
vd,pd,cd=collect(None,straddle=False,deepdeep=True)
def frac(c,v):
    cc=c[(v>0)&(v<1e-8)]; return np.median(cc),np.percentile(cc,84)
print("CONDITIONING (frac a0 err per 1% R err):")
print(f"  straddling: median={frac(cs,vs)[0]:.3f} 84th={frac(cs,vs)[1]:.3f} (kept)")
print(f"  deep-deep : median={frac(cd,vd)[0]:.3f} 84th={frac(cd,vd)[1]:.3f} (excluded)")
md,nd=med_phys(vd); print(f"  deep-deep median a0={md:.3e} n={nd}")
def HA(a0): return Z*a0/(C*np.sqrt(OL))/KMSMPC
def HB(a0): return np.sqrt((Z*a0/C)**2+OMH2*H100**2)/KMSMPC
print("E8 CIRCULARITY: a0_canon->HA=%.1f HB=%.1f (expect 67.4)"%(HA(A0C),HB(A0C)))
HL=67.4*KMSMPC*np.sqrt(OL); print("  c*H_Lambda/Z=%.3e vs 9.36e-11"%(C*HL/Z))
for tag,sub in [("ALL",None),("TRGB/Ceph",{2,3})]:
    v,p,c=collect(sub);m,_=med_phys(v)
    print(f"  a0_MEASURED[{tag}]={m:.3e} -> HA={HA(m):.1f} HB={HB(m):.1f}")
print("indep verify exit 0")
