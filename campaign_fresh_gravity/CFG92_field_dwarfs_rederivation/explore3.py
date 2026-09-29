import numpy as np, pandas as pd, itertools
src=open('explore_gext.py').read()
exec(src.split("Mst=2*")[0])
def nu(y): return 1/(1-np.exp(-np.sqrt(y)))
def slopeX(x,y,cols):
    X=np.column_stack([np.ones(len(x)),x]+cols); b,*_=np.linalg.lstsq(X,y,rcond=None); return b[1]
Mst=2*10**(-0.4*(d.MV-4.83)); ly=np.log10(d.sig.values)
def gex(a0,MMW=6e10,MM31=1.2e11,rule='mw',lmc=False,MLMC=1.5e10):
    ge=[]
    for _,r in d.iterrows():
        if r['pop']=='mw':
            if lmc and r.host=='lmc': D_,M=r.dh,MLMC
            else: D_,M=r.dgc,MMW
        elif r['pop']=='m31': D_,M=r.dm31,MM31
        else:
            D_,M=(r.dgc,MMW) if rule=='mw' else max([(r.dgc,MMW),(r.dm31,MM31)],key=lambda t:t[1]/t[0]**2)
        y=G*M*Ms/(D_*kpc)**2/a0; ge.append(y*nu(y))
    return np.array(ge)
for rk,mk,rule,lmc in itertools.product(('rh','rhm'),('Mb','Mst'),('mw','max'),(False,True)):
    Mx=(Mst+1.33*d.HI) if mk=='Mb' else Mst
    lM=np.log10(Mx.values); lr=np.log10(d[rk].values)
    for quad in (True,):
        cols=[lM,lr,lM**2,lr**2,lM*lr]
        sc=slopeX(np.log10(gex(9.36e-11,rule=rule,lmc=lmc)),ly,cols); sa=slopeX(np.log10(gex(1.13e-10,rule=rule,lmc=lmc)),ly,cols)
        g=gex(9.36e-11,rule=rule,lmc=lmc)
        print(rk,mk,rule,'lmc' if lmc else '   ',f"{sc:+.4f} {sa:+.4f} range {g.min():.4f}-{g.max():.3f} med {np.median(g):.4f}")
