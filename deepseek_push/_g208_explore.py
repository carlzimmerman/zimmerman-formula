#!/usr/bin/env python3
"""G208 exploration (stage 2): overlap control, MIGHTEE D-at-deep, F fits."""
import csv, json, math, re, statistics
import numpy as np
GN=6.674e-11; MSUN=1.98892e30; A0DE=9.3619e-11; KPC=3.0856775814913673e19
HERE="/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push"

rows=list(csv.DictReader(open(HERE+'/G114_data/G114_combined_sample.csv')))
hi=[]
for r in rows:
    V=float(r['V_obs_kms'])*1e3; Mb=float(r['M_b_Msun'])*MSUN
    hi.append(dict(name=r['name'],Mb=float(r['M_b_Msun']),a0e=V**4/(GN*Mb),D=float(r['V_obs_kms'])/float(r['v_pred_kms'])))
g071=json.load(open(HERE+'/G071_results.json'))
sp=[]
for pg in g071['per_galaxy']:
    rings=[r for r in pg['rings'] if r['v_b']>0 and r['v_obs']>0]
    if not rings: continue
    Mb=pg['Mb_Msun']*MSUN
    deep=[r for r in rings if (r['v_b']*1e3)**2/(r['R_kpc']*KPC)<0.2*A0DE]
    src=deep if deep else rings
    outer=max(rings,key=lambda r:r['R_kpc'])
    sp.append(dict(name=pg['name'],Mb=pg['Mb_Msun'],a0e=float(np.median([(r['v_obs']*1e3)**4/(GN*Mb) for r in src])),D=outer['v_obs']/outer['v_b']))

# ---- overlap control ----
h9=[x['a0e'] for x in hi if 8.5<=math.log10(x['Mb'])<=9.5]
sw=[x['a0e'] for x in sp if 8.5<=math.log10(x['Mb'])<=9.5]
print('overlap logMb [8.5,9.5]: HI n=%d med=%.3f x1e-10 | SPARC n=%d med=%.3f x1e-10'
      %(len(h9), np.median(h9)/1e-10, len(sw), np.median(sw)/1e-10 if sw else float('nan')))

# ---- MIGHTEE table 5 ----
t=list(csv.DictReader(open(HERE+'/data2/mightee2025_rar_galaxy_sample_table5.csv')))
mstar=[]; zz=[]
for r in t:
    mstar.append(float(re.match(r'([0-9.]+)',r['log10_Mstar_Msun']).group(1))); zz.append(float(r['z']))
print('MIGHTEE: logMstar min %.2f max %.2f med %.2f | z min %.4f max %.4f med %.4f'
      %(min(mstar),max(mstar),np.median(mstar),min(zz),max(zz),np.median(zz)))
print('MIGHTEE in [8.5,9.5] window: n=%d'%sum(1 for m in mstar if 8.5<=m<=9.5))

# ---- G011 factor ----
E044=math.sqrt(1+0.0443)
print('G011 E(0.0443)=%.5f -> +%.2f%%'%(E044,(E044-1)*100))
print('needed staircase factor 1.8746/0.643 = %.2fx'%(1.8746e-10/0.643e-10))

# ---- MIGHTEE D at deepest ring per group (circular, stated) ----
pts=list(csv.DictReader(open(HERE+'/data2/mightee2025_rar_digitized_points.csv')))
grp={}
for p in pts:
    k=(p['color_r'],p['color_g'],p['color_b']); grp.setdefault(k,[]).append(p)
Dm=[]
for k,ix in grp.items():
    ds=[10**float(p['log10_gobs'])/10**float(p['log10_gbar']) for p in ix]
    Dm.append(ds[-1])
print('MIGHTEE per-group D at deepest ring n=%d: med %.1f range %.1f..%.1f'%(len(Dm),np.median(Dm),min(Dm),max(Dm)))

# ---- F fits ----
spa=np.array([math.log10(x['a0e']/A0DE) for x in sp]); spd=np.array([math.log10(x['D']) for x in sp])
A=np.vstack([np.ones_like(spd),spd]).T
p_,_,_,_=np.linalg.lstsq(A,spa,rcond=None)
print('SPARC fit log10(a0e/a0DE)=%.3f+%.3f log10D, rms %.3f dex'%(p_[0],p_[1],np.sqrt(np.mean((spa-A@p_)**2))))
pa=np.array([math.log10(x['a0e']/A0DE) for x in hi+sp]); pd=np.array([math.log10(x['D']) for x in hi+sp])
q,_,_,_=np.linalg.lstsq(np.vstack([np.ones_like(pd),pd]).T,pa,rcond=None)
print('POOLED fit p=%.3f offset=%.3f'%(q[1],q[0]))
# exp-eq-fraction: log10(a0e/a0DE)=gamma*x_eq, x_eq=1-1/D
for lab,xs,ys in (('SPARC',sp,spa),('POOL',hi+sp,pa)):
    xe=np.array([1-1.0/x['D'] for x in xs]); y=ys*1.0
    g=np.sum(xe*y)/np.sum(xe*xe)
    rms=np.sqrt(np.mean((y-g*xe)**2))
    print('%s eq-fraction gamma=%.3f rms %.3f dex'%(lab,g,rms))

# MIGHTEE groups D vs a0eff per group (circular-by-construction, shown for the record)
print('HI MAD log10 a0e %.3f dex | SPARC MAD %.3f dex'
      %(mad([math.log10(x['a0e']) for x in hi]), mad([math.log10(x['a0e']) for x in sp])))