import numpy as np, os, math, json
from astropy.io import fits
from scipy.optimize import least_squares
XB='real_research/data/xcop'
G=6.674e-11; MSUN=1.98892e30; KPC=3.0857e19
H0=67.4e3/3.0857e22
rho_lam=0.685*3*H0**2/(8*math.pi*G)
sDE=2.99792458e8*math.sqrt(G*rho_lam)
A0={'canonical':sDE/2,'alt':1.1279e-10}
def loginterp(x,xp,fp):
    x=np.atleast_1d(np.asarray(x,float))
    ok=np.isfinite(xp)&(xp>0)&np.isfinite(fp)&(fp>0)
    xp,fp=np.asarray(xp)[ok],np.asarray(fp)[ok]
    o=np.argsort(xp); xp,fp=xp[o],fp[o]
    out=10**np.interp(np.log10(x),np.log10(xp),np.log10(fp))
    out[(x<xp[0])|(x>xp[-1])]=np.nan
    return out
names=sorted(d for d in os.listdir(XB) if os.path.isdir(os.path.join(XB,d)))
CL=[]
for n in names:
    h=fits.open(os.path.join(XB,n,n+'_hydro_mass.fits'))
    d=h[1].data; hed=h[1].header
    fg=fits.open(os.path.join(XB,n,n+'_fgas_profile.fits'))[1].data
    dd=dict(name=n,r=np.array(d['RADIUS'],float),M=np.array(d['M_FORW'],float),
            eM=np.array(d['EM_FORW'],float),Mnfw=np.array(d['M_NFW'],float),
            R500=float(hed['R500']),M500=float(hed['M500']),
            rg=np.array(fg['RADIUS'],float)*1e3,mg=np.array(fg['MGAS'],float))
    p2=h[2].data; dd['rs_nfw']=float(np.array(p2['RS'])[0])
    fs=os.path.join(XB,n,n+'_mstar.fits')
    if os.path.exists(fs):
        ms=fits.open(fs)[2].data
        dd['rs']=np.array(ms['RADIUS'],float); dd['mst']=np.array(ms['MSTAR'],float)
    CL.append(dd)
RG=np.array([50.,75.,100.,150.,210.,300.,420.,600.,900.,1200.])
ratio={}
for r in RG:
    v=[]
    for c in CL:
        if 'rs' not in c: continue
        a=loginterp([r],c['rg'],c['mg'])[0]; b=loginterp([r],c['rs'],c['mst'])[0]
        if np.isfinite(a) and np.isfinite(b) and b>0: v.append(b/a)
    if v: ratio[r]=float(np.median(v))
RK=sorted(ratio); RV=[ratio[k] for k in RK]
def bary(c,r):
    mg=loginterp(r,c['rg'],c['mg'])
    ms=loginterp(r,c['rs'],c['mst']) if 'rs' in c else mg*np.interp(r,RK,RV)
    return mg+ms,mg,ms
def rM_outer(c,a0):
    rr=np.sqrt(G*c['M']*MSUN/a0)/3.0857e22*1e3
    f=rr-c['r']; idx=np.where(np.sign(f[:-1])!=np.sign(f[1:]))[0]
    sol=[float(np.interp(0,[f[i],f[i+1]],[c['r'][i],c['r'][i+1]])) for i in idx]
    return (sol[-1] if sol else np.nan)
def M_nfw(r,M0,rs):
    x=np.asarray(r,float)/rs
    return M0*(np.log1p(x)-x/(1+x))
def M_phantom(r,ron,rg,mgas_b,a0):
    """enclosed phantom mass in Msun for r>ron:  M_ph(<r) = (sqrt(G a0)/G) int sqrt(Mb) dr
       Mb in kg, dr in m -> result kg -> Msun"""
    out=np.zeros(len(r))
    for i,ri in enumerate(r):
        if ri<=ron: continue
        m=(rg>ron)&(rg<=ri)
        if m.sum()<1: continue
        rr=np.concatenate(([ron],rg[m],[ri]))
        mm=loginterp(rr,rg,mgas_b)*MSUN   # kg
        integ=np.trapz(np.sqrt(mm),rr*KPC)
        out[i]=math.sqrt(G*a0)/G*integ/MSUN
    return out
print(f"{'cl':9s} {'rM':>6s} {'ron':>6s} {'ron/rM':>6s} {'chi2F':>8s} {'chi2N':>8s} {'dchi':>7s} {'rs_d':>6s} {'rs_xcop':>7s}")
for c in CL:
    fe=c['eM']/c['M']
    ok=(c['r']>=60)&(fe<=0.20)&(c['r']<=0.95*c['rg'].max())
    i=np.where(ok)[0]; r=c['r'][i]
    mb,mg,ms=bary(c,r); Md=c['M'][i]-mb
    e=np.sqrt(c['eM'][i]**2+(0.23*mb)**2)
    g=np.isfinite(Md)&(Md>0); r,Md,e,mb2=r[g],Md[g],e[g],mb[g]
    a0=A0['canonical']
    rm=rM_outer(c,a0)
    # fine grid of baryons for the integral
    rg2=np.logspace(np.log10(r.min()),np.log10(r.max()),400)
    mbg=bary(c,rg2)[0]
    def resN(p): return (M_nfw(r,10**p[0],10**p[1])-Md)/e
    bN=None
    for rs0 in [300,600,1200]:
        s=least_squares(resN,[np.log10(8*c['M500']*1e13),np.log10(rs0)],bounds=([11,1.5],[17,4]))
        if bN is None or s.cost<bN.cost: bN=s
    def resF(p):
        m0,lrs,lron=p
        mdl=M_nfw(r,10**m0,10**lrs)+M_phantom(r,10**lron,rg2,mbg,a0)
        return (mdl-Md)/e
    bF=None
    for fr in [0.5,1.0,2.0]:
        s=least_squares(resF,[bN.x[0],bN.x[1],np.log10(fr*rm if np.isfinite(rm) else 700)],
                        bounds=([11,1.5,1.5],[17,4,3.5]))
        if bF is None or s.cost<bF.cost: bF=s
    print(f"{c['name']:9s} {rm if np.isfinite(rm) else -1:6.0f} {10**bF.x[2]:6.0f} {10**bF.x[2]/rm if np.isfinite(rm) else -1:6.2f} {2*bF.cost:8.1f} {2*bN.cost:8.1f} {2*bN.cost-2*bF.cost:7.1f} {10**bF.x[1]:6.0f} {c['rs_nfw']:7.0f}  n={len(r)}")
