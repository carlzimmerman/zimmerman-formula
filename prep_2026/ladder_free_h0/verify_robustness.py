import numpy as np, os, csv
Z=np.sqrt(32*np.pi/3); KPC=3.0856775814913673e19; UD,UB=0.5,0.7; A0C=9.36e-11
DATA="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
MASTER="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_master_clean.csv"
meta={r["name"]:dict(Q=int(r["Q"]),inc=float(r["inc"]),fD=int(r["fD"])) for r in csv.DictReader(open(MASTER))}
def load(n,scaleD=1.0):
    fn=os.path.join(DATA,n+"_rotmod.dat")
    if not os.path.exists(fn): return None
    a=np.loadtxt(fn)
    if a.ndim==1 or a.shape[0]<5: return None
    r,vo,ev,vg,vd,vb=a[:,0],a[:,1],a[:,2],a[:,3],a[:,4],a[:,5]
    m=(r>0)&(vo>0); r=r[m];vo=vo[m];ev=ev[m];vg=vg[m];vd=vd[m];vb=vb[m]
    # PHYSICAL distance perturbation: r_phys->L*r, v_newton^2 -> L*v^2 (M~D^2,r~D)
    L=scaleD; rm=r*L*KPC
    gbar=(np.sign(vg)*(vg**2*L)+UD*vd**2*L+UB*vb**2*L)*1e6/rm  # vgas signed
    return dict(r=r*L,rm=rm,vo=vo,ev=ev,gbar=gbar)
def pairs(n,scaleD=1.0):
    d=load(n,scaleD)
    if d is None or not np.all(d["gbar"]>0): return []
    gb=d["gbar"];vo=d["vo"];ev=d["ev"];r=d["r"];out=[]
    good=np.where(ev<0.08*vo)[0]
    for ia in range(len(good)):
        for ib in range(ia+1,len(good)):
            i,j=good[ia],good[ib];a,b=gb[i],gb[j]
            if abs(np.log10(a/b))<0.5: continue
            if not(min(a,b)<A0C<max(a,b)): continue
            Rv=(vo[i]/vo[j])**4*(r[j]/r[i])**2; dn=Rv*b-a
            if abs(dn)<1e-16: continue
            a0h=(a**2-Rv*b**2)/dn
            if 0<a0h<1e-8: out.append(a0h)
    return out
gal=[n for n in meta if meta[n]["Q"]<=2 and 30<=meta[n]["inc"]<=85 and load(n) is not None and np.all(load(n)["gbar"]>0)]
# per-galaxy medians -> median of medians (robust to per-galaxy pair count)
permed=[]; allp=[]
for n in gal:
    pp=pairs(n)
    if len(pp)>=3: permed.append(np.median(pp)); allp+=pp
print("pooled median a0 (all pairs)      = %.3e (n=%d pairs)"%(np.median(allp),len(allp)))
print("median-of-per-galaxy-medians a0   = %.3e (n=%d galaxies)"%(np.median(permed),len(permed)))
# top galaxy pair-count share
import collections
cnt={n:len(pairs(n)) for n in gal}; tot=sum(cnt.values())
top=sorted(cnt.values(),reverse=True)[:3]
print("top-3 galaxies contribute %.0f%% of pairs (concentration check)"%(100*sum(top)/tot))
# FULL physical D-perturbation test (rescale v_newton AND rm consistently)
p0=[]; p20=[]
for n in gal: p0+=pairs(n,1.0); p20+=pairs(n,1.2)
print("physical D+20%% test: median a0 %.4e -> %.4e (%.2f%% shift)"
      %(np.median(p0),np.median(p20),100*(np.median(p20)/np.median(p0)-1)))
