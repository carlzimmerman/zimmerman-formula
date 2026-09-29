"""PRE-FREEZE data-side exploration (no model code, no S, no Moster): which reading of the external-field regressor and design reproduces
k_contrarian_dwarfefe.out's PRINTED observed-side numbers (range 0.0070-4.876 / 0.0064-4.163, median 0.0931 / 0.0844, statistic C observed +0.0800 +/- 0.0467)?
Only those printed numbers are targets. Nothing here touches the CFG58 files."""
import numpy as np, pandas as pd, math, itertools
D="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/dsph/"
G=6.674e-11; Ms=1.989e30; kpc=3.0857e19
A0={'c':9.36e-11,'a':1.13e-10}
mw=pd.read_csv(D+'lvd_dwarf_mw.csv'); m31=pd.read_csv(D+'lvd_dwarf_m31.csv'); lf=pd.read_csv(D+'lvd_dwarf_local_field.csv')
rows=[]
for pop,df in (('mw',mw),('m31',m31),('f',lf)):
    for _,r in df[df.vlos_sigma.notna()].iterrows():
        rows.append(dict(pop=pop,name=r['name'],host=r['host'],MV=r.M_V,rh=r.rhalf_sph_physical,rhm=r.rhalf_physical,sig=r.vlos_sigma,
                         HI=(10**r.mass_HI if pd.notna(r.mass_HI) else 0.0),dh=r.distance_host,dgc=r.distance_gc,dm31=r.distance_m31,dlg=r.distance_lg))
d=pd.DataFrame(rows); print(len(d), d['pop'].value_counts().to_dict())
def nu(y): return 1/(1-np.exp(-np.sqrt(y)))
def design(cols): return np.column_stack(cols)
def slope(x,y,lM,lr,quad=True):
    X=[np.ones(len(x)),x,lM,lr]+([lM**2,lr**2,lM*lr] if quad else [])
    b,*_=np.linalg.lstsq(np.column_stack(X),y,rcond=None); return b[1]
def boot(x,y,lM,lr,n=2000,seed=1):
    rng=np.random.default_rng(seed); N=len(x); s=[]
    for _ in range(n):
        i=rng.integers(0,N,N); s.append(slope(x[i],y[i],lM[i],lr[i]))
    return np.std(s,ddof=1)
Mst=2*10**(-0.4*(d.MV-4.83)); Mb=Mst+1.33*d.HI
lM=np.log10(Mb.values); lMs=np.log10(Mst.values); ly=np.log10(d.sig.values)
for rk in ('rh','rhm'):
  lr=np.log10(d[rk].values)
  for MM31 in (1.145e11,1.2e11,1.375e11,1.72e11):
    for boost in (False,True):
      for hostrule in ('near','mwgc'):
        out={}
        for f,a in A0.items():
            ge=[]
            for _,r in d.iterrows():
                if hostrule=='near':
                    if r['pop']=='mw': D_,M=r.dh if r.host in('mw',) else r.dgc,1.145e11
                    elif r['pop']=='m31': D_,M=r.dm31,MM31
                    else:
                        c=[(r.dgc,1.145e11),(r.dm31,MM31)]; D_,M=min(c,key=lambda t:G*t[1]/t[0]**2*-1)
                        # nearest-by-field
                        D_,M=max(c,key=lambda t:t[1]/t[0]**2)
                else:
                    D_,M=r.dgc,1.145e11
                    if r['pop']=='m31': D_,M=r.dm31,MM31
                y=G*M*Ms/(D_*kpc)**2/A0[f]
                ge.append(y*nu(y) if boost else y)
            ge=np.array(ge); out[f]=ge
        x=np.log10(out['c']); s=slope(x,ly,lM,lr); xa=np.log10(out['a']); sa=slope(xa,ly,lM,lr)
        print(f"{rk:3s} M31={MM31:.3e} boost={boost!s:5s} host={hostrule:4s} range {out['c'].min():.4f}-{out['c'].max():.3f} med {np.median(out['c']):.4f} | alt {out['a'].min():.4f}-{out['a'].max():.3f} med {np.median(out['a']):.4f} | slopeC {s:+.4f} alt {sa:+.4f}")
