#!/usr/bin/env python3
"""DA1 K1: UR3's concentration row, by the lane's method. Source: raw ZN1 z = 0 snapshots at 1e12 and the two radius definitions; chain: UR3's formula M0 = M mu(r c/R)/mu(c), c 12.95, R = R200 (halo()). kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, os, re
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); OUT=[]
def P(s): print(s); OUT.append(s)
G=4.30091e-9; Om,h=0.2976016,0.6856427; rc=3*(100*h)**2/(8*math.pi*G); mu=lambda y:np.log1p(y)-y/(1+y)
def centre(x):
    c=x.mean(0); R=np.sqrt(((x-c)**2).sum(1)).max()
    while R>0.02:
        s=((x-c)**2).sum(1)<R*R
        if s.sum()<100: break
        c=x[s].mean(0); R*=0.9
    return c
def fit(r,M,lo,Rn):
    # own estimator, log-spaced shells in differential mass, Poisson weights; not UL1's cumulative shape fit
    e=np.geomspace(lo,Rn,25); n,_=np.histogram(r,e); mid=np.sqrt(e[1:]*e[:-1]); cs=np.linspace(1,40,3901)
    best=None
    for c in cs:
        p=mu(c*e[1:]/Rn)-mu(c*e[:-1]/Rn); p=p/p.sum(); ll=(n*np.log(p+1e-300)).sum()
        if best is None or ll>best[0]: best=(ll,c)
    return float(best[1])
rows=[]
for d in sorted(glob.glob(os.path.join(RB,'ZN1_zooms_to_z0','runs','M1e12_s?_ng64'))):
    A=np.load(os.path.join(d,'snap_z0.00.npz'),allow_pickle=False); x=A['x']; m=float(A['m']); me=json.loads(str(A['meta']))
    r=np.sort(np.sqrt(((x-centre(x))**2).sum(1))); M=np.arange(1,len(r)+1)*m; dn=M/(4/3*math.pi*r**3); rho_m=me['Mf']/(4/3*math.pi*me['qM']**3)
    R200=float(r[np.where(dn>=200*rc)[0].max()]); Rv=float(r[np.where(dn>=18*math.pi**2*rho_m)[0].max()]); lo=max(3*me['eps'],float(r[199]))
    rows.append(dict(seed=os.path.basename(d),R200=R200,rvir=Rv,c_on_rvir=fit(r,M,lo,Rv),c_on_R200=fit(r,M,lo,R200),M200=float(np.interp(R200,r,M)),m_at_0p04R200=float(np.interp(0.0412*R200,r,M)/np.interp(R200,r,M))))
med=lambda k:float(np.median([q[k] for q in rows]))
ratio=med('c_on_rvir')/med('c_on_R200'); P(f"K1. {len(rows)} seeds. Own centre and own shell fit. R200 {med('R200'):.4f}, r_vir {med('rvir'):.4f} Mpc, ratio {med('rvir')/med('R200'):.3f}; c on r_vir {med('c_on_rvir'):.2f}, c on R200 {med('c_on_R200'):.2f}, ratio {ratio:.2f}")
ur3=open(os.path.join(RB,'UR3_direct_weighing','ur3_mw.py')).read(); uses=bool(re.search(r"c = 12\.95;.*M0 = M \* mu\(rg / \(R / c\)\) / mu\(c\)",ur3))
x48=open(os.path.join(RB,'X48_native_cf_zoom','x48_analyze.py')).read(); uses_v='18 * math.pi ** 2' in x48 or '18*math.pi**2' in x48 or 'rvir' in x48
P(f"Chain text: UR3 applies c 12.95 with R / c: {uses}; the number's source (LC1 c_nfw, X48 c_nfw_fit) is fitted on rvir: {uses_v}")
xR=0.0412; a=mu(12.95*xR)/mu(12.95); b=mu(med('c_on_R200')*xR)/mu(med('c_on_R200')); P(f"Effect at R0/R200 {xR}: UR3 fraction of M200 {a:.4f}; on R200's own c {b:.4f}; raw {med('m_at_0p04R200'):.4f}; UR3/raw {a/med('m_at_0p04R200'):.2f}")
lab='DEFINITION WRONG' if uses and ratio>=1.3 else 'NOT FOUND'; P(f"K1 result: {lab} (must read DEFINITION WRONG). Line: c ratio >= 1.3, as UL1 froze it")
json.dump(dict(rows=rows,ratio=ratio,label=lab),open(os.path.join(HERE,'da1_k1.json'),'w'),indent=1); open(os.path.join(HERE,'da1_k1.out'),'w').write('\n'.join(OUT)+'\n')
