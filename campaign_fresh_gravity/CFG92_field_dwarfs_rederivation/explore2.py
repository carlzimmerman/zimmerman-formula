import numpy as np, pandas as pd
src=open('explore_gext.py').read()
exec(src.split("Mst=2*")[0].replace("for rk in","for rk in"))
def slope(x,y,lM,lr):
    X=np.column_stack([np.ones(len(x)),x,lM,lr,lM**2,lr**2,lM*lr]); b,*_=np.linalg.lstsq(X,y,rcond=None); return b[1]

def nu(y): return 1/(1-np.exp(-np.sqrt(y)))
Mst=2*10**(-0.4*(d.MV-4.83)); Mb=Mst+1.33*d.HI
lM=np.log10(Mb.values); ly=np.log10(d.sig.values); lr=np.log10(d.rh.values)
def gexf(MMW,MM31,a0,fieldrule):
    ge=[]
    for _,r in d.iterrows():
        if r['pop']=='mw': D_,M=r.dgc,MMW
        elif r['pop']=='m31': D_,M=r.dm31,MM31
        else:
            if fieldrule=='max': D_,M=max([(r.dgc,MMW),(r.dm31,MM31)],key=lambda t:t[1]/t[0]**2)
            elif fieldrule=='mw': D_,M=r.dgc,MMW
            elif fieldrule=='sum':
                y=G*Ms*(MMW/(r.dgc*kpc)**2+MM31/(r.dm31*kpc)**2)/a0; ge.append(y*nu(y)); continue
        y=G*M*Ms/(D_*kpc)**2/a0; ge.append(y*nu(y))
    return np.array(ge)
for fr in ('max','mw','sum'):
  for MMW in (6e10,7e10,7.6e10,8e10,9e10,1.0e11):
    gc=gexf(MMW,1.2e11,9.36e-11,fr); ga=gexf(MMW,1.2e11,1.13e-10,fr)
    print(fr,f"{MMW:.1e} c {gc.min():.4f}-{gc.max():.3f} med {np.median(gc):.4f} | a {ga.min():.4f}-{ga.max():.3f} med {np.median(ga):.4f} slope {slope(np.log10(gc),ly,lM,lr):+.4f} {slope(np.log10(ga),ly,lM,lr):+.4f}")
