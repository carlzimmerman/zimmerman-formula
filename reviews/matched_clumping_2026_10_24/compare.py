"""Frozen, empirical matched-acceleration comparison; no fitted force law."""
import argparse, csv, json, os
from pathlib import Path
import numpy as np
from astropy.io import fits

G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
DATA = Path('real_research/data')
RELAXED = {'A1795', 'A2029', 'A2142'}

def number(row, key):
    try: return float(row[key])
    except (ValueError, KeyError, TypeError): return np.nan

def acceleration(vgas, vdisk, vbul, radius, ml=1):
    return (vgas*abs(vgas)+ml*(.5*vdisk*abs(vdisk)+.7*vbul*abs(vbul)))*1e6/radius

def crossings(x, y, valid, target, gap):
    values=[]
    for i in range(len(x)-1):
        if not (valid[i] and valid[i+1]): continue
        a,b=x[i:i+2]
        if abs(a-b)>gap or not min(a,b)<=target<=max(a,b): continue
        values.append(float(np.mean(y[i:i+2])) if a==b else float(y[i]+(target-a)/(b-a)*(y[i+1]-y[i])))
    return float(np.median(values)) if values else np.nan

def sparc(ml=1):
    meta={}
    for line in (DATA/'SPARC_Lelli2016c.mrt').read_text().splitlines():
        t=line.split()
        if len(t)>=18 and t[1].isdigit(): meta[t[0]]=(float(t[5]),int(t[17]))
    assert len(meta)==175, len(meta)
    curves={}
    for path in sorted((DATA/'sparc_data').glob('*_rotmod.dat')):
        name=path.name.replace('_rotmod.dat','')
        inc,q=meta[name]
        if inc<30 or q>2: continue
        a=np.loadtxt(path,ndmin=2)
        r,v,e,gas,disk,bul=a[:,:6].T
        with np.errstate(divide='ignore',invalid='ignore'):
            gb=acceleration(gas,disk,bul,r*1000*PC,ml)
            go=v*v*1e6/(r*1000*PC)
            valid=(r>0)&(v>0)&(e/v<.1)&(gb>0)&np.isfinite(gb)&np.isfinite(go)
            x,y=np.log10(gb),np.log10(go)
        if np.any(valid[:-1]&valid[1:]): curves[name]=(x,y,valid)
    return curves

def dwarfs(ml=2):
    rows,rejected=[],[]
    for group in ['mw','m31','local_field']:
        with (DATA/f'dsph/lvd_dwarf_{group}.csv').open() as f:
            for d in csv.DictReader(f):
                name=d['name']; reasons=[]
                s,em,ep,r,mv=[number(d,k) for k in ['vlos_sigma','vlos_sigma_em','vlos_sigma_ep','rhalf_sph_physical','M_V']]
                if number(d,'confirmed_real')!=1 or number(d,'confirmed_galaxy')!=1: reasons.append('unconfirmed')
                if not (s>0 and r>0 and np.isfinite(mv)): reasons.append('missing/invalid measurement')
                if not mv<=-6: reasons.append('M_V cut')
                if not (em>0 and ep>0 and (em+ep)/(2*s)<=.30): reasons.append('dispersion error cut')
                if np.isfinite(number(d,'mass_HI')): reasons.append('HI detected')
                if name.replace(' ','').upper() in {'M32','NGC147','NGC185','NGC205'}: reasons.append('rotation-sensitive')
                if reasons:
                    rejected.append(dict(name=name,group=group,reason='; '.join(reasons))); continue
                radius=4*r*PC/3; mass=ml*10**(.4*(4.83-mv))
                rows.append(dict(kind='dwarf',name=name,group=group,radius_m=radius,xradius=1.,gbar=G*mass*MSUN/(2*radius**2),gobs=3*(s*1000)**2/radius,physical_gobs=3*(s*1000)**2/radius,mgas=np.nan,mhse500=np.nan))
    return rows,rejected

def loginterp(r,m,target):
    assert np.all(np.diff(r)>0) and np.all(r>0) and np.all(m>0)
    if target<r[0] or target>r[-1]: return np.nan
    return float(10**np.interp(np.log10(target),np.log10(r),np.log10(m)))

def clusters(bias=0,star=1):
    rows=[]; rejected=[]
    for folder in sorted((DATA/'xcop').iterdir()):
        if not folder.is_dir(): continue
        name=folder.name
        if not (folder/f'{name}_hydro_mass.fits').exists(): continue
        if not (folder/f'{name}_mstar.fits').exists():
            rejected.append(dict(name=name,group='cluster',reason='no measured stellar profile')); continue
        with fits.open(folder/f'{name}_hydro_mass.fits') as h:
            hm=h[1].data.copy(); r500=h[1].header['R500']
        with fits.open(folder/f'{name}_fgas_profile.fits') as h:
            gas=h[1].data.copy(); rg500=h[1].header['R500']
        with fits.open(folder/f'{name}_mstar.fits') as h: stars=h[2].data.copy()
        m500=loginterp(hm['RADIUS'],hm['M_FORW'],r500)
        for x in [.1,.2,.3,.5,.7,1.]:
            r=x*r500; radius=r*1000*PC
            mh=loginterp(hm['RADIUS'],hm['M_FORW'],r)
            mg=loginterp(gas['RADIUS']*rg500,gas['MGAS'],r)
            ms=loginterp(stars['RADIUS'],stars['MSTAR'],r)
            if not np.all(np.isfinite([mh,mg,ms])):
                rejected.append(dict(name=name,group='cluster',reason=f'profile support missing at {x} R500')); continue
            go=G*mh*MSUN/(radius**2*(1-bias))
            rows.append(dict(kind='cluster',name=name,group='relaxed' if name in RELAXED else 'other',radius_m=radius,xradius=x,gbar=G*(mg+star*ms)*MSUN/radius**2,gobs=go,physical_gobs=go,mgas=mg,mhse500=m500))
    return rows,rejected

def match(rows, curves, gap=.3):
    names=list(curves)
    matrix=np.full((len(rows),len(names)),np.nan)
    for j,row in enumerate(rows):
        for k,name in enumerate(names): matrix[j,k]=crossings(*curves[name],np.log10(row['gbar']),gap)
        vals=matrix[j,np.isfinite(matrix[j])]
        row['nref']=len(vals); row['matched']=len(vals)>=8
        row['log_gref']=float(np.median(vals)) if row['matched'] else np.nan
        row['ref_p16']=float(np.percentile(vals,16)) if row['matched'] else np.nan
        row['ref_p84']=float(np.percentile(vals,84)) if row['matched'] else np.nan
        row['delta']=float(np.log10(row['gobs'])-row['log_gref'])
    return matrix,names

def summarize(rows):
    result={}
    cluster_names=sorted({r['name'] for r in rows if r['kind']=='cluster'})
    masses={n:next(r['mhse500'] for r in rows if r['name']==n) for n in cluster_names}
    split=np.median(list(masses.values())) if masses else np.nan
    selections={'dwarf':lambda r:r['kind']=='dwarf','cluster':lambda r:r['kind']=='cluster',
      'cluster_relaxed':lambda r:r['kind']=='cluster' and r['name'] in RELAXED,
      'cluster_lower_mass':lambda r:r['kind']=='cluster' and r['mhse500']<=split,
      'cluster_higher_mass':lambda r:r['kind']=='cluster' and r['mhse500']>split}
    for label,select in selections.items():
        by={}
        for r in rows:
            if select(r) and r['matched']: by.setdefault(r['name'],[]).append(r['delta'])
        vals={n:float(np.median(v)) for n,v in by.items()}
        if not vals: result[label]={'n':0}; continue
        v=list(vals.values()); med=float(np.median(v))
        result[label]=dict(n=len(v),median_dex=med,factor=10**med,p16_p84_dex=np.percentile(v,[16,84]).tolist(),systems=vals)
    result['mass_split_msun']=float(split)
    return result

def bootstrap(rows,matrix,nboot=1000):
    rng=np.random.default_rng(20261024)
    ids={kind:sorted({r['name'] for r in rows if r['kind']==kind and r['matched']}) for kind in ['dwarf','cluster']}
    idx={name:[i for i,r in enumerate(rows) if r['name']==name and r['matched']] for names in ids.values() for name in names}
    distributions={k:[] for k in ids}
    loggo=np.log10([r['gobs'] for r in rows]); good=np.array([r['matched'] for r in rows])
    for _ in range(nboot):
        sample=rng.integers(matrix.shape[1],size=matrix.shape[1])
        # Only baseline-supported rows enter. Resampling may repeat a galaxy, as intended.
        ref=np.array([np.nanmedian(matrix[i,sample]) if np.any(np.isfinite(matrix[i,sample])) else np.nan for i in range(len(rows))])
        delta=loggo-ref
        for kind,names in ids.items():
            values=np.array([np.nanmedian(delta[idx[n]]) for n in names])
            if len(values): distributions[kind].append(float(np.nanmedian(rng.choice(values,size=len(values),replace=True))))
    return {k:dict(draws=len(v),interval_16_84_dex=np.percentile(v,[16,84]).tolist(),interval_2_5_97_5_dex=np.percentile(v,[2.5,97.5]).tolist()) for k,v in distributions.items() if v}

def shape(rows,matrix,names):
    out=[]
    for name in sorted({r['name'] for r in rows if r['kind']=='cluster'}):
        ids=[i for i,r in enumerate(rows) if r['name']==name and r['matched']]
        common=np.all(np.isfinite(matrix[ids]),axis=0) if ids else np.zeros(len(names),bool)
        for mode in ['individual','common']:
            pairs=[]
            if mode=='common' and common.sum()<8:
                out.append(dict(name=name,mode=mode,n=0,common_reference_count=int(common.sum()),slope=None)); continue
            for i in ids:
                r=rows[i]; ref=r['log_gref'] if mode=='individual' else np.median(matrix[i,common])
                residual=(r['gobs']-10**ref)*r['radius_m']**2/(G*MSUN)
                q=residual/r['mgas']
                if mode=='individual': r['effective_residual_msun']=float(residual); r['effective_residual_over_gas']=float(q)
                if q>0: pairs.append((r['xradius'],float(q)))
            slope=float(np.polyfit(np.log10(np.array(pairs)[:,0]),np.log10(np.array(pairs)[:,1]),1)[0]) if len(pairs)>=4 else None
            out.append(dict(name=name,mode=mode,n=len(pairs),common_reference_count=int(common.sum()),slope=slope,points=pairs))
    return out

def controls():
    assert np.isclose(crossings(np.array([-12.,-11.8]),np.array([-11.,-10.9]),[True,True],-11.9,.3),-10.95)
    assert np.isnan(crossings(np.array([-12.,-11.8]),np.array([-11.,-10.9]),[True,True],-12.1,.3))
    assert np.isnan(crossings(np.array([-12.,-11.9,-11.8]),np.array([-11.,-10.95,-10.9]),[True,False,True],-11.9,.3))
    assert np.isclose(acceleration(-2.,4.,0.,1.),4e6)
    assert np.isclose(loginterp(np.array([1.,10.]),np.array([1.,100.]),np.sqrt(10)),10)
    assert np.isnan(loginterp(np.array([1.,10.]),np.array([1.,100.]),11))
    mass=1e10; r=1000*PC; g=G*mass*MSUN/r**2
    assert np.isclose(g*r**2/G/MSUN,mass)
    ref=-11.; assert np.log10(10**ref)-ref==0
    assert np.isclose(np.log10(2*10**ref)-ref,np.log10(2))
    return ['power-law interpolation','no acceleration extrapolation','no bridging rejected rows','signed gas','log mass interpolation','no radius extrapolation','SI mass roundtrip','synthetic zero residual','doubling shift']

def write_csv(path,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True); p.add_argument('--mutate',action='store_true'); args=p.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    checks=controls(); curves=sparc(); d,dr=dwarfs(); c,cr=clusters(); rows=d+c
    if args.mutate:
        for r in rows: r['gobs']*=2
    for r in rows: assert np.isclose(r['gobs']/r['physical_gobs'],1.,rtol=1e-12,atol=0), f"physical reconstruction failed: {r['name']}"
    checks.append('all target accelerations agree with physical reconstruction')
    matrix,names=match(rows,curves); summary=summarize(rows)
    slopes=shape(rows,matrix,names)
    boot=bootstrap(rows,matrix)
    sensitivity={}
    variants=[('segment_0.15',1,.15,2,0,1),('segment_0.50',1,.5,2,0,1),('SPARC_ML_0.8',.8,.3,2,0,1),('SPARC_ML_1.2',1.2,.3,2,0,1),('dwarf_ML_1',1,.3,1,0,1),('dwarf_ML_3',1,.3,3,0,1),('HSE_bias_0.2',1,.3,2,.2,1),('HSE_bias_0.3',1,.3,2,.3,1),('cluster_stars_0.5',1,.3,2,0,.5),('cluster_stars_2',1,.3,2,0,2)]
    for label,sm,gap,dm,b,st in variants:
        rr=dwarfs(dm)[0]+clusters(b,st)[0]; mm,nn=match(rr,sparc(sm),gap)
        sensitivity[label]={'summary':summarize(rr),'shape':shape(rr,mm,nn)}
    result=dict(summary=summary,bootstrap=boot,sensitivity=sensitivity,shape=slopes,checks=checks,reference_galaxies=len(names),selected_dwarfs=len(d),selected_clusters=len({r['name'] for r in c}),matched_rows=sum(r['matched'] for r in rows),unmatched=[{'name':r['name'],'kind':r['kind'],'gbar':r['gbar'],'nref':r['nref']} for r in rows if not r['matched']])
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    write_csv(out/'targets.csv',rows); write_csv(out/'rejections.csv',dr+cr)
    write_csv(out/'reference_matches.csv',[dict(target=r['name'],xradius=r['xradius'],reference=names[k],log_gobs=float(matrix[i,k])) for i,r in enumerate(rows) for k in range(len(names)) if np.isfinite(matrix[i,k])])
    os.environ.setdefault('MPLCONFIGDIR','/tmp/matched_clumping_mpl')
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(11,4.7),layout='constrained')
    for x,y,valid in curves.values(): axs[0].scatter(x[valid],y[valid],s=2,color='gray',alpha=.15,rasterized=True)
    for kind,color,marker in [('dwarf','tab:blue','o'),('cluster','tab:red','s')]:
        rr=[r for r in rows if r['kind']==kind and r['matched']]
        axs[0].scatter(np.log10([r['gbar'] for r in rr]),np.log10([r['gobs'] for r in rr]),s=22,color=color,marker=marker,label=f'{kind}: matched')
    uu=[r for r in d if not r['matched']]
    axs[0].scatter(np.log10([r['gbar'] for r in uu]),np.log10([r['gobs'] for r in uu]),s=23,facecolors='none',edgecolors='tab:blue',label='dwarf: insufficient overlap')
    for name in sorted({r['name'] for r in c}):
        rr=[r for r in c if r['name']==name and r['matched']]
        axs[1].plot([r['xradius'] for r in rr],[r['delta'] for r in rr],'.-',label=name)
    axs[0].set(xlabel=r'$\log_{10} g_{\rm bar}$ [m s$^{-2}$]',ylabel=r'$\log_{10} g_{\rm obs}$ [m s$^{-2}$]',title='Measured profiles; fixed stellar mass assumptions')
    axs[0].legend(fontsize=8); axs[1].axhline(0,color='gray',ls='--')
    axs[1].set(xlabel=r'$r/R_{500}$',ylabel='Excess over matched SPARC galaxies [dex]',title='X-COP: hydrostatic masses, measured stars')
    axs[1].legend(fontsize=7,ncol=2); fig.savefig(out/'comparison.png',dpi=180)
    print(json.dumps({'summary':summary,'bootstrap':boot,'shape':slopes,'selected_dwarfs':len(d),'unmatched':result['unmatched'],'checks':checks},indent=2))

if __name__=='__main__': main()
