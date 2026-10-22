#!/usr/bin/env python3
"""G208 exploration (stage 3): SPARC f_gas from corpus; p-values; residual spreads."""
import csv, json, math, statistics
import numpy as np

GN=6.674e-11; MSUN=1.98892e30; A0DE=9.3619e-11; KPC=3.0856775814913673e19
HERE="/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push"
REPO="/Users/carlzimmerman/new_physics/zimmerman-formula"

_crawl=json.load(open(REPO+"/glm53_push/data/rotation_curve_corpus_v7.json"))
_cmap={}
for g in _crawl["galaxies"]:
    n=g["galaxy"]; s=str(g.get("survey","")).strip().upper()
    if n not in _cmap or s=="SPARC":
        _cmap[n]=g
corpus=_cmap

rows=list(csv.DictReader(open(HERE+'/G114_data/G114_combined_sample.csv')))
hi=[]
for r in rows:
    V=float(r['V_obs_kms'])*1e3; Mb=float(r['M_b_Msun'])*MSUN
    hi.append(dict(name=r['name'],Mb=float(r['M_b_Msun']),a0e=V**4/(GN*Mb),
                   D=float(r['V_obs_kms'])/float(r['v_pred_kms']),f_gas=float(r['f_gas'])))
g071=json.load(open(HERE+'/G071_results.json'))
sp=[]
for pg in g071['per_galaxy']:
    rings=[r for r in pg['rings'] if r['v_b']>0 and r['v_obs']>0]
    if not rings: continue
    Mb=pg['Mb_Msun']*MSUN
    deep=[r for r in rings if (r['v_b']*1e3)**2/(r['R_kpc']*KPC)<0.2*A0DE]
    src=deep if deep else rings
    outer=max(rings,key=lambda r:r['R_kpc'])
    fg=None
    c=corpus.get(pg['name'])
    if c:
        data=c['data']; Rmax=max(d['Rad'] for d in data)
        d=[d for d in data if d['Rad']==Rmax][0]
        m2l=float(c['m2l_disk']) if str(c.get('m2l_disk')) not in ('','None') else 0.5
        Vg=float(d['Vgas']); Vd=float(d['Vdisk']); Vb=float(d['Vbul'])
        v2g=math.copysign(Vg*Vg, Vg); v2star=m2l*(Vd*Vd+Vb*Vb)
        if v2g+v2star>0 and v2g>=0:
            fg=v2g/(v2g+v2star)
    sp.append(dict(name=pg['name'],Mb=pg['Mb_Msun'],
                   a0e=float(np.median([(r['v_obs']*1e3)**4/(GN*Mb) for r in src])),
                   D=outer['v_obs']/outer['v_b'], f_gas=fg))

fg=[x['f_gas'] for x in sp if x['f_gas'] is not None]
print('SPARC f_gas coverage:', len(fg),'/',len(sp),' med %.3f range %.3f..%.3f'%(np.median(fg),min(fg),max(fg)))

def spear(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    return float(np.corrcoef(np.argsort(np.argsort(x)),np.argsort(np.argsort(y)))[0,1])

def perm_p(x,y,n=20000,seed=208):
    rng=np.random.default_rng(seed); x=np.asarray(x,float); y=np.asarray(y,float)
    r0=abs(spear(x,y)); cnt=0
    for _ in range(n):
        if abs(spear(x,rng.permutation(y)))>=r0: cnt+=1
    return (cnt+1)/(n+1)

print('SPARC rho(a0e,D)=%.3f p=%.2e'%(spear([x['a0e'] for x in sp],[x['D'] for x in sp]),
      perm_p([x['a0e'] for x in sp],[x['D'] for x in sp])))
print('SPARC rho(a0e,f_gas)=%.3f p=%.2e'%(spear([x['a0e'] for x in sp],[x['f_gas'] if x['f_gas'] is not None else 0.0 for x in sp]),
      perm_p([x['a0e'] for x in sp],[x['f_gas'] if x['f_gas'] is not None else 0.0 for x in sp])))
print('SPARC rho(a0e,Mb)=%.3f  rho(D,f_gas)=%.3f'%(spear([x['a0e'] for x in sp],[x['Mb'] for x in sp]),
      spear([x['D'] for x in sp],[x['f_gas'] if x['f_gas'] is not None else 0.0 for x in sp])))
print('POOLED rho(a0e,D)=%.3f p=%.2e'%(spear([x['a0e'] for x in hi]+[x['a0e'] for x in sp],[x['D'] for x in hi]+[x['D'] for x in sp]),
      perm_p([x['a0e'] for x in hi]+[x['a0e'] for x in sp],[x['D'] for x in hi]+[x['D'] for x in sp])))
print('POOLED rho(a0e,Mb)=%.3f'%spear([x['a0e'] for x in hi]+[x['a0e'] for x in sp],[x['Mb'] for x in hi]+[x['Mb'] for x in sp]))

def mad(xs): return statistics.median([abs(x-statistics.median(xs)) for x in xs])
ha=[math.log10(x['a0e']) for x in hi]; sa=[math.log10(x['a0e']) for x in sp]
print('total MAD log10 a0e: HI %.3f SPARC %.3f'%(mad(ha),mad(sa)))
logm=np.array([math.log10(x['a0e']/A0DE) for x in sp]); lod=np.array([math.log10(x['D']) for x in sp])
A=np.vstack([np.ones_like(lod),lod]).T; p_,*_=np.linalg.lstsq(A,logm,rcond=None)
res=logm-A@p_
print('SPARC power fit p=%.3f intercept=%.3f: residual MAD %.3f dex (total %.3f)'%(p_[1],p_[0],mad(list(res)),mad(sa)))
print('HI rho(a0e,D) =', spear([x['a0e'] for x in hi],[x['D'] for x in hi]))
h9=[x['a0e'] for x in hi if 8.5<=math.log10(x['Mb'])<=9.5]; s9=[x['a0e'] for x in sp if 8.5<=math.log10(x['Mb'])<=9.5]
print('overlap [8.5,9.5]: HI %.3f (n=%d) vs SPARC %.3f (n=%d) x1e-10'%(np.median(h9)/1e-10,len(h9),np.median(s9)/1e-10,len(s9)))
# F(D) prediction of the HI step from the SPARC fit
pred_hi=10**(p_[0]+p_[1]*np.median([math.log10(x['D']) for x in hi]))
pred_sp=10**(p_[0]+p_[1]*np.median([math.log10(x['D']) for x in sp]))
print('SPARC-fit F predicts a0e: at HI D med -> %.3f x1e-10 (measured 1.075); at SPARC D med -> %.3f x1e-10 (measured %.3f)'%(pred_hi*A0DE/1e-10,pred_sp*A0DE/1e-10,np.median(sa and [x['a0e']/1e-10 for x in sp])))
