# POST-HOC (after reading CFG52's feas.py): my own code, but with CFG52's *conventions* swapped in one at a time, to attribute each difference.
import sys, math, numpy as np, pandas as pd
import importlib.util
spec=importlib.util.spec_from_file_location('c','cfg90.py'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
from astropy.cosmology import Planck18, FlatLambdaCDM
REPO=c.REPO
def gas52(M): return M*(1+(M/1e10)**-0.4)
def load(gas52_msa=False, gas52_kross=False, kmos_unique=False, planck18=False, cos70_muse=False, vfloor=False, f1311=False):
    R,aux=c.load()
    # MSA gas recipe
    if gas52_msa:
        m=R.survey=="MSA3D"
        R.loc[m,"logM"]=np.log10(gas52(10**R.loc[m,"logMstar"]))
    # KROSS: 'stars+gas' via CFG52 recipe (stars-only baseline in my loader)
    if gas52_kross:
        m=R.survey=="KROSS"
        R.loc[m,"logM"]=np.log10(gas52(10**R.loc[m,"logM"]))
    if f1311:
        R.loc[R.survey.isin(["KMOS3D","KROSS"]),"xn"]=1.311*1.68
    # KMOS3D unique match at M* tol 0.006 (drop others); Planck18 scale
    if kmos_unique or planck18:
        u=pd.read_csv(f"{REPO}/real_research/data/kmos3d_ubler2017.csv")
        cat=pd.read_csv(f"{REPO}/data_assembly/kmos3d_phibss/kmos3d_catalog.csv"); cat=cat[(cat.Z>0)&(cat.LMSTAR>0)].reset_index(drop=True)
        keep=[]; Re=[]
        for i,r in u.iterrows():
            sel=cat[(abs(cat.Z-r.z)<0.002)&(abs(cat.LMSTAR-r.logMstar)<(0.006 if kmos_unique else 0.02))]
            if kmos_unique and len(sel)!=1: keep.append(False); Re.append(np.nan); continue
            if len(sel)==0: keep.append(False); Re.append(np.nan); continue
            j=sel.index[0] if len(sel)==1 else ((cat.Z-r.z)/0.002)**2*0+np.hypot((sel.Z-r.z)/0.002,(sel.LMSTAR-r.logMstar)/0.02).idxmin()
            rh=cat.loc[j,"RHALF"]; ok=rh>0
            keep.append(ok); Re.append(rh*(Planck18.kpc_proper_per_arcmin(r.z).value/60 if planck18 else c.dA_kpc_per_arcsec(r.z)))
        k=R[R.survey=="KMOS3D"].copy()
        # rebuild KMOS3D rows in order of u
        rows=[]
        for i,r in u.iterrows():
            if keep[i]:
                rows.append(dict(survey="KMOS3D",name=f"K{i}",z=r.z,logM=r.logMbar,Re=Re[i],V=r.Vcirc_kms,sigV=0.10,xn=(1.311*1.68 if f1311 else 2.2),fDM=np.nan,gas="table"))
        R=pd.concat([R[R.survey!="KMOS3D"],pd.DataFrame(rows)],ignore_index=True)
    if cos70_muse:
        m=pd.read_csv(f"{REPO}/prep_2026/jeanneau_refit/jeanneau26_catalog_cds.csv"); cos=FlatLambdaCDM(H0=70,Om0=0.3)
        mm=(R.survey=="MUSE2").values
        R.loc[mm,"Re"]=[r.Reff*cos.kpc_proper_per_arcmin(r.zR21).value/60 for _,r in m.iterrows()]
    if vfloor:
        mm=R.survey.isin(["MSA3D","MUSE2"]); R.loc[mm,"sigV"]=np.maximum(R.loc[mm,"sigV"],0.05)
    return R
def summarize(R,lab):
    SUR=["RC100","MSA3D","KMOS3D","KROSS","MUSE2"]
    x,gb,y=c.per_object(R,"can"); R=R.assign(y=y,gb=gb)
    Rv=R.xn*R.Re*c.KPC/1.68; gobs=(R.V*1e3)**2/Rv
    slope=c.slope_flat(gb,"can"); sig=np.sqrt((2*R.sigV/c.LN10)**2+(slope*0.2)**2)
    gf=c.law_pred(gb,R.z.values,"can"); gr=c.law_pred(gb,R.z.values,"can",rival=True)
    gap=np.abs(np.log10(gf/gr)); R=R.assign(gapsig=gap/sig,df=np.log10(gobs)-np.log10(gf),dr=np.log10(gobs)-np.log10(gr))
    cnt={s:(int(((R.survey==s)&(R.y<1)).sum()),int(((R.survey==s)&(R.y<.3)).sum()),int(((R.survey==s)&(R.y<1)&(R.z>=1.5)).sum())) for s in SUR}
    sel=R[R.y<1]; pool=R[(R.y<1)&(R.z>=1.5)]
    print(f"{lab:38s} counts {cnt}  sum<a0 {sum(v[0] for v in cnt.values())} (+1 ledger); n>1s {int((sel.gapsig>1).sum())} n>2s {int((sel.gapsig>2).sum())}; pool N={len(pool)} flat {pool.df.mean():+.3f} rival {pool.dr.mean():+.3f}")
    return R
print("CFG52 targets: RC100 26/4/9, MSA 19/4/3, KMOS 16/5/2, KROSS(+gas) 106/15/0, MUSE 74/43/0; n>1s 16, n>2s 0; pool N=14 +0.135 -0.037 (excludes the ledger object)")
summarize(load(),"baseline (frozen convention)")
summarize(load(kmos_unique=True),"+ KMOS3D unique match tol 0.006")
summarize(load(kmos_unique=True,planck18=True),"+ Planck18 scale")
summarize(load(kmos_unique=True,planck18=True,f1311=True),"+ r_v = 1.311 R_e")
summarize(load(kmos_unique=True,planck18=True,f1311=True,cos70_muse=True),"+ MUSE cosmology H0=70 Om=0.3")
summarize(load(kmos_unique=True,planck18=True,f1311=True,cos70_muse=True,vfloor=True),"+ 5% velocity-error floor (MSA, MUSE)")
summarize(load(kmos_unique=True,planck18=True,f1311=True,cos70_muse=True,vfloor=True,gas52_msa=False,gas52_kross=True),"+ KROSS gas recipe Ms(1+(Ms/1e10)^-0.4)")
R=summarize(load(kmos_unique=True,planck18=True,f1311=True,cos70_muse=True,vfloor=True,gas52_msa=True,gas52_kross=True),"+ MSA same gas recipe (all CFG52 conv.)")

# ---- pooled statistic: 2x2x2 attribution (CFG52 pool = RC100 excl. GS4 01529 + MSA(gas) + KMOS3D + ledger DSFG850.95, inverse-variance weighted)
print("\nPOOLED z>=1.5, g_bar<a0 attribution (all CFG52 conventions swapped in; ledger row DSFG850.95 from the ledger JSON: M*=3.8e10, Mmol=8.88e10, R_out=14.1 kpc, V=285, 15% error)")
R=load(kmos_unique=True,planck18=True,f1311=True,cos70_muse=True,vfloor=True,gas52_msa=True,gas52_kross=True)
led=pd.DataFrame([dict(survey="LEDGER",name="DSFG850.95",z=1.555,logM=math.log10(3.8e10+8.88e10),Re=14.1/1.311,V=285.0,sigV=0.15,xn=1.311*1.68,fDM=np.nan)])
R=pd.concat([R,led],ignore_index=True)
x,gb,y=c.per_object(R,"can"); Rv=R.xn*R.Re*c.KPC/1.68; gobs=(R.V*1e3)**2/Rv
slope=c.slope_flat(gb,"can"); sig=np.sqrt((2*R.sigV/c.LN10)**2+(slope*0.2)**2); sobs=2*R.sigV/c.LN10
gf=c.law_pred(gb,R.z.values,"can"); gr=c.law_pred(gb,R.z.values,"can",rival=True)
R=R.assign(y=y,sig=sig,sobs=sobs,slope=slope,df=np.log10(gobs)-np.log10(gf),dr=np.log10(gobs)-np.log10(gr),sep=np.abs(np.log10(gf/gr)))
print("ledger row: g_bar/a0 = %.3f  (CFG52 .out: 0.81)  Df %+.3f (CFG52 +0.16) Dr %+.3f (CFG52 +0.03)"%(R[R.survey=='LEDGER'].y.iloc[0],R[R.survey=='LEDGER'].df.iloc[0],R[R.survey=='LEDGER'].dr.iloc[0]))
base=R[(R.z>=1.5)&(R.y<1)&R.survey.isin(["RC100","MSA3D","KMOS3D","LEDGER"])]
print(f"{'GS4':>4s} {'ledger':>7s} {'weights':>10s} | N   <Df>    <Dr>   sigma_corr  Df/sig  Dr/sig")
for gs4 in (True,False):
    for led_ in (False,True):
        for wt in ("inv-var","unweighted"):
            S=base.copy()
            if not gs4: S=S[S.name!="GS4 01529"]
            if not led_: S=S[S.survey!="LEDGER"]
            w=1/S.sig**2 if wt=="inv-var" else np.ones(len(S))
            mf=(w*S.df).sum()/w.sum(); mr=(w*S.dr).sum()/w.sum()
            sc=math.sqrt(1/np.sum(1/S.sobs**2)+(S.slope.mean()*0.2)**2)
            print(f"{str(gs4):>4s} {str(led_):>7s} {wt:>10s} | {len(S):2d} {mf:+.3f} {mr:+.3f}   {sc:.3f}    {mf/sc:+.2f}  {mr/sc:+.2f}")

# ---- leave-one-out of the 14-object pool, and sensitivity grid under CFG52 conventions (KROSS with its gas recipe; ledger row included as its own column)
S=base[(base.name!="GS4 01529")]
w=1/S.sig**2
full=((w*S.df).sum()/w.sum(),(w*S.dr).sum()/w.sum())
lo=[]
for i in S.index:
    T=S.drop(i); ww=1/T.sig**2
    lo.append((S.loc[i,"name"],(ww*T.df).sum()/ww.sum(),(ww*T.dr).sum()/ww.sum()))
print("\nleave-one-out (14-object CFG52-type pool, inverse-variance): full %+.3f / %+.3f"%full)
print("  Df range %+.3f .. %+.3f ; Dr range %+.3f .. %+.3f"%(min(l[1] for l in lo),max(l[1] for l in lo),min(l[2] for l in lo),max(l[2] for l in lo)))
print("  most influential:",sorted(lo,key=lambda t:-abs(t[1]-full[0]))[:3])
print("\nSENSITIVITY GRID under CFG52 conventions (counts: RC100,MSA,KMOS,KROSS+gas,MUSE,ledger-DSFG | total ; z>=1.5 same order | total)")
names=["RC100","MSA3D","KMOS3D","KROSS","MUSE2","LEDGER"]
for xm in ("native","1.31rh","rpeak","rpeak_tot","rflat"):
    for key in ("can","alt"):
        x_,gb_,y_=c.per_object(R,key,xm)
        for thr in (0.3,0.5,1.0):
            s=y_<thr
            a=[int((s&(R.survey==n).values).sum()) for n in names]; h=[int((s&(R.survey==n).values&(R.z>=1.5).values).sum()) for n in names]
            print(f"{xm:9s} {key} thr {thr:3.1f} | {a} {sum(a):4d} | {h} {sum(h):3d}")
