#!/usr/bin/env python3
"""Conditional exact-mu cluster budgets and deep-limit pair likelihood audit.

No action is inferred from the inverse source and no significance is assigned.
Run with the repository scientific Python; writes only this new directory.
"""
import ast
import datetime as dt
import hashlib
import importlib.util
import json
import math
import platform
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import ndtr, expit
from scipy.spatial import cKDTree

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
AUDIT=HERE.parent/'cluster_measurement_audit_2026/cluster_audit.py'
spec=importlib.util.spec_from_file_location('audit',AUDIT)
audit=importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)
G,MSUN,KPC=audit.G,audit.MSUN,audit.KPC
A0=audit.A0
THIRD_SEARCH_KPC=8000.

def search_chord(radius_kpc,distance_mpc):
    return 2*np.sin(min(radius_kpc/(1000*distance_mpc),np.pi)/2)

def isolated(d3,rp,factor):
    threshold=np.maximum(factor*rp,300.)
    if np.any(threshold>THIRD_SEARCH_KPC):
        raise ValueError('Isolation threshold exceeds the searched radius')
    return d3>threshold

def pair_dependencies(i,j):
    parent={int(x):int(x) for x in np.r_[i,j]}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    for a,b in zip(i,j):parent[find(int(a))]=find(int(b))
    roots=[find(int(a)) for a in i]
    _,counts=np.unique(roots,return_counts=True)
    return dict(connected_pair_components=int(len(counts)),
        largest_component_pairs=int(max(counts,default=0)),
        pairs_in_shared_galaxy_components=int(sum(counts[counts>1])))

def piecewise(r,x,m):
    i=np.clip(np.searchsorted(x,r,side='right')-1,0,len(x)-2)
    return audit.loginterp(r,x,m), (np.diff(np.log(m))/np.diff(np.log(x)))[i]

def cluster_targets():
    rows=[]; signs=[]
    clusters=[audit.load_cluster(p.name) for p in sorted(audit.DATA.iterdir()) if p.is_dir()]
    # Primary targets use measured stellar files, avoiding imported star profiles.
    for c in clusters:
        if not c['has_star']: continue
        lower=max(40.,c['rh'][0],c['rg'][0],c['rs'][0])
        upper=min(1000.,c['rh'][-1],c['rg'][-1],c['rs'][-1])
        r=np.geomspace(lower,upper,1201)
        mh,ah=piecewise(r,c['rh'],c['M_FORW'])
        mg,ag=piecewise(r,c['rg'],c['mg'])
        ms,ass=piecewise(r,c['rs'],c['ms'])
        for foot,a0 in A0.items():
            y=G*mh*MSUN/(r*KPC)**2/a0; mu=-np.expm1(-y)
            missing=mu*mh-mg-ms
            dlog=mh*(mu*ah+y*np.exp(-y)*(ah-2))-mg*ag-ms*ass
            # Independent centered derivative excludes all interpolation knots.
            eps=1e-6
            def budget(rr):
                hh=audit.loginterp(rr,c['rh'],c['M_FORW'])
                return -np.expm1(-G*hh*MSUN/(rr*KPC)**2/a0)*hh-audit.loginterp(rr,c['rg'],c['mg'])-audit.loginterp(rr,c['rs'],c['ms'])
            numeric=(budget(r*np.exp(eps))-budget(r*np.exp(-eps)))/(2*eps)
            good=np.isfinite(numeric)
            for knots in (c['rh'],c['rg'],c['rs']):
                good &= np.min(np.abs(np.log(r[:,None]/knots[None,:])),axis=1)>2*eps
            # Normalize cancellation-prone derivatives by the cumulative source scale.
            err=np.max(abs(numeric[good]-dlog[good])/(mh[good]+mg[good]+ms[good]))
            assert err<2e-7,err
            neg=dlog<0
            signs.append(dict(cluster=c['name'],footing=foot,range_kpc=[lower,upper],
                missing_mass_positive_everywhere=bool(np.all(missing>0)),
                negative_effective_density_fraction=float(np.mean(neg)),
                negative_density_first_kpc=float(r[neg][0]) if np.any(neg) else None,
                negative_density_last_kpc=float(r[neg][-1]) if np.any(neg) else None,
                derivative_relative_check=float(err)))
            for rr in (100.,300.,1000.):
                if not lower<=rr<=upper: continue
                hh,aa=piecewise(np.array([rr]),c['rh'],c['M_FORW']);gg,bb=piecewise(np.array([rr]),c['rg'],c['mg']);ss,cc=piecewise(np.array([rr]),c['rs'],c['ms'])
                yy=G*hh*MSUN/(rr*KPC)**2/a0;mm=-np.expm1(-yy)
                dd=hh*(mm*aa+yy*np.exp(-yy)*(aa-2))-gg*bb-ss*cc
                rows.append(dict(cluster=c['name'],footing=foot,r_kpc=rr,relaxed=c['name'] in audit.RELAXED,
                    M_b_Msun=float((gg+ss)[0]),M_extra_required_Msun=float((mm*hh-gg-ss)[0]),
                    total_source_over_baryons=float((mm*hh/(gg+ss))[0]),
                    dM_extra_dlnr_Msun=float(dd[0]),rho_extra_required_kg_m3=float(dd[0]*MSUN/(4*np.pi*(rr*KPC)**3)),
                    g_HSE_over_a0=float(yy[0])))
    return {'rows':rows,'density_signs':signs}

def pair_sample():
    # Reuse only the four coordinate/photometric functions, never an old kernel.
    path=ROOT/'hunt_2026/h48_h69b_relative_isolation.py'
    tree=ast.parse(path.read_text())
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('unitvec','ang_sep_deg','cmb_frame','LK_from_mag')]
    ns={'np':np,'math':math,'MK_SUN':3.28}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),'exec'),ns)
    d=np.genfromtxt(ROOT/'real_research/data/2mrs_catalog.csv',delimiter=',',names=True)
    good=np.isfinite(d['RAJ2000'])&np.isfinite(d['Ktmag'])&np.isfinite(d['cz'])
    ra,de,K,cz=(d[x][good] for x in ('RAJ2000','DEJ2000','Ktmag','cz'))
    u=ns['unitvec'](ra,de);tree=cKDTree(u);v=ns['cmb_frame'](ra,de,cz)
    cand=tree.query_pairs(2*np.sin(.5/(3000/67.4)),output_type='ndarray')
    i,j=cand.T;vm=(v[i]+v[j])/2;dist=vm/67.4
    rp=np.radians(ns['ang_sep_deg'](u[i],u[j]))*dist*1000;dv=v[i]-v[j]
    keep=(abs(dv)<2000)&(vm>3000)&(vm<12000)&(rp<1000)&(rp>10)
    i,j,vm,dist,rp,dv=(x[keep] for x in (i,j,vm,dist,rp,dv))
    m1=.6*ns['LK_from_mag'](K[i],dist);m2=.6*ns['LK_from_mag'](K[j],dist)
    keep=np.maximum(m1,m2)/np.minimum(m1,m2)<6
    i,j,vm,dist,rp,dv,m1,m2=(x[keep] for x in (i,j,vm,dist,rp,dv,m1,m2))
    mid=u[i]+u[j];mid/=np.linalg.norm(mid,axis=1)[:,None];d3=np.full(len(i),np.inf)
    for n in range(len(i)):
        nb=np.array(tree.query_ball_point(mid[n],search_chord(THIRD_SEARCH_KPC,dist[n])),dtype=int)
        nb=nb[(nb!=i[n])&(nb!=j[n])&(abs(v[nb]-vm[n])<1000)]
        if len(nb): d3[n]=np.min(2*np.arcsin(np.clip(np.linalg.norm(u[nb]-mid[n],axis=1)/2,0,1))*dist[n]*1000)
    return dict(i=i,j=j,vm=vm,rp=rp,dv=dv,m1=m1,m2=m2,d3=d3)

def vdeep(m1,m2,a0):
    total=(m1+m2)*MSUN;f=m1/(m1+m2)
    B=(2/3)*(1-f**1.5-(1-f)**1.5)/(f*(1-f))
    return np.sqrt(B*np.sqrt(G*a0*total))/1000

def fit_velocity(dv,v,kind='gaussian',verr=40.):
    # Both component densities explicitly normalized in the selected |dv|<2000 window.
    def objective(par):
        amp=np.exp(par[0]);f=expit(par[1]);speed=amp*v
        if kind=='gaussian':
            s=np.sqrt(speed**2/3+verr**2)
            density=np.exp(-.5*(dv/s)**2)/(np.sqrt(2*np.pi)*s)/(2*ndtr(2000/s)-1)
        else:
            density=(ndtr((dv+speed)/verr)-ndtr((dv-speed)/verr))/(2*speed)
            def H(x): return x*ndtr(x)+np.exp(-x*x/2)/np.sqrt(2*np.pi)
            def cdf(x):return verr*(H((x+speed)/verr)-H((x-speed)/verr))/(2*speed)
            density/=cdf(2000)-cdf(-2000)
        return -float(np.sum(np.log(np.maximum(f*density+(1-f)/4000,1e-300))))
    opt=min((minimize(objective,[np.log(a),z],method='L-BFGS-B',bounds=[(np.log(.1),np.log(12)),(-8,8)]) for a in (1.,2.,4.) for z in (0.,2.)),key=lambda r:r.fun)
    assert opt.success,opt.message
    amp=float(np.exp(opt.x[0]))
    return dict(amplitude=amp,additional_co_scaled_mass_over_stellar=amp**4-1,
        total_co_scaled_mass_over_stellar=amp**4,interloper_fraction=float(1-expit(opt.x[1])),nll=float(opt.fun),optimizer_success=bool(opt.success))

def pairs():
    p=pair_sample();out=[]
    # Reconstruct the old censored distances for a reproducible correction audit.
    old_d3=np.where(p['d3']<=4000.,p['d3'],np.inf)
    for fac in (2,5,8):
        masks={f'relative_{fac}':isolated(p['d3'],p['rp'],fac)}
        old_masks={f'relative_{fac}':old_d3>np.maximum(fac*p['rp'],300)}
        if fac==5:
            mask=masks['relative_5']
            subsets={'relative_5_near':p['vm']<6000,'relative_5_far':p['vm']>=9000,
                'relative_5_deep':G*(p['m1']+p['m2'])*MSUN/(p['rp']*KPC)**2/A0['canonical']<.01}
            masks.update({key:mask&sub for key,sub in subsets.items()})
            old_masks.update({key:old_masks['relative_5']&sub for key,sub in subsets.items()})
            near_ids=np.r_[p['i'][masks['relative_5_near']],p['j'][masks['relative_5_near']]]
            far_ids=np.r_[p['i'][masks['relative_5_far']],p['j'][masks['relative_5_far']]]
            assert len(np.intersect1d(near_ids,far_ids))==0
        for label,mask in masks.items():
            oldmask=old_masks[label]
            assert not np.any(mask&~oldmask)
            for foot,a0 in A0.items():
                v=vdeep(p['m1'][mask],p['m2'][mask],a0)
                inds=np.r_[p['i'][mask],p['j'][mask]]
                row=dict(selection=label,footing=foot,n=int(mask.sum()),median_rp_kpc=float(np.median(p['rp'][mask])),
                    legacy_4Mpc_capped_n=int(oldmask.sum()),legacy_false_passes_removed=int(np.sum(oldmask&~mask)),
                    legacy_4Mpc_uncovered_cut_n=int(np.sum(oldmask&(np.maximum(fac*p['rp'],300)>4000))),
                    dependency_groups=pair_dependencies(p['i'][mask],p['j'][mask]),
                    median_stellar_mass_Msun=float(np.median(p['m1'][mask]+p['m2'][mask])),
                    repeated_galaxy_entries=int(len(inds)-len(np.unique(inds))),
                    median_testparticle_deep_y_at_projected_radius=float(np.median(np.sqrt(G*(p['m1'][mask]+p['m2'][mask])*MSUN/a0)/(p['rp'][mask]*KPC))),
                    gaussian=fit_velocity(p['dv'][mask],v),circular_top_hat=fit_velocity(p['dv'][mask],v,'tophat'))
                if np.any(oldmask&~mask):
                    oldv=vdeep(p['m1'][oldmask],p['m2'][oldmask],a0)
                    row['legacy_4Mpc_capped_fits']={'gaussian':fit_velocity(p['dv'][oldmask],oldv),
                        'circular_top_hat':fit_velocity(p['dv'][oldmask],oldv,'tophat')}
                out.append(row)
    return out

def checks():
    a=A0['canonical'];m=1e11
    # Equal-mass exact coefficient and test-body limit, symmetry and co-scaling.
    assert np.isclose(vdeep(m,m,a)**4*1e12/(G*m*MSUN*a),((4/3)*(2**1.5-2))**2)
    assert np.isclose(vdeep(m,m*.001,a),vdeep(m*.001,m,a))
    assert np.isclose(vdeep(m*16,m*8,a),2*vdeep(m,m/2,a))
    assert abs(vdeep(m,m*1e-7,a)**4*1e12/(G*m*MSUN*a)-1)<.001
    # Constructed noiseless circular uniform LOS sample recovers amplitude, not a planted result flag.
    vv=np.full(3001,180.);dv=np.linspace(-179.9,179.9,3001)
    fit=fit_velocity(dv,vv,'tophat',1.)
    assert abs(fit['amplitude']-1)<.01
    # Regression: a third body at 6 Mpc must be seen and veto an 8 Mpc cut.
    D=100.;theta=6./D;third=np.array([[np.cos(theta),np.sin(theta),0.]])
    assert cKDTree(third).query_ball_point([1.,0.,0.],search_chord(THIRD_SEARCH_KPC,D))==[0]
    assert not isolated(np.array([6000.]),np.array([1000.]),8)[0]
    assert isolated(np.array([6000.]),np.array([1000.]),5)[0]
    assert pair_dependencies(np.array([0,1,3]),np.array([1,2,4]))==dict(connected_pair_components=2,largest_component_pairs=2,pairs_in_shared_galaxy_components=2)
    return ['equal masses','mass exchange','16-fold mass gives 2-fold speed','test-body limit','constructed circular likelihood recovery','analytic-vs-numerical cluster derivatives','6 Mpc third body vetoes 8 Mpc isolation','search covers every isolation threshold','shared-galaxy connected components','near and far samples have disjoint galaxy IDs']

def main():
    start=time.monotonic();stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    checked=checks();result={'scope':'conditional inverse source targets, not action prediction or observational exclusion','a0_m_s2':A0,'checks':checked,'clusters':cluster_targets(),'pairs':pairs()}
    output=HERE/'results.json';output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    inputs=[Path(__file__),AUDIT,ROOT/'hunt_2026/h48_h69b_relative_isolation.py',ROOT/'real_research/data/2mrs_catalog.csv']+sorted(audit.DATA.glob('*/*.fits'))
    hashed=lambda p:{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    manifest=dict(schema_version=1,claim_id='exact-law-cluster-and-pair-source-targets',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),dirty=bool(subprocess.check_output(['git','status','--porcelain'],text=True))),
        command=str(sys.executable)+' -B '+str(Path(__file__).relative_to(ROOT)),
        environment=dict(software=['Python '+platform.python_version(),'NumPy '+np.__version__,'SciPy '+scipy.__version__,'Astropy '+audit.astropy.__version__],hardware=platform.machine()),
        mathematics=dict(assertion_tested='Exact exponential spherical inverse source; derivative; mass-ratio deep-MOND two-body likelihood targets',coefficient_domain='IEEE754 float64',conventions='SI, Msun, kpc; normalized gas FITS decoded using its own R500; K-band M/L 0.6; no gas for pairs',inputs=[hashed(p) for p in inputs],bounds={'cluster_grid':1201,'cluster_range_kpc':[40,1000],'pair_cz_kms':[3000,12000],'pair_rp_kpc':[10,1000],'pair_dvmax_kms':2000,'pair_third_search_kpc':THIRD_SEARCH_KPC,'relative_isolation':[2,5,8]},non_claims=['No inferred clock action, pressure law or stable solution','No covariance-aware or orbit-selection-independent exclusion','No finite-acceleration two-body AQUAL solution','No diffuse-clock mass inversion from binary amplitude']),
        randomness=dict(used=False,generator='',seed=None),run=dict(started_at=stamp,runtime_seconds=time.monotonic()-start,exit_status=0),outputs=[hashed(output)],checks=[dict(name=s,passed=True) for s in checked],result='Required source targets under stated observational and population assumptions',residual_risks=['Hydrostatic central profiles with unknown radial covariance','Log-linear profile derivative kinks and stellar incompleteness','Flux-limited third-galaxy catalog and velocity-window contamination','Pair orbital phase and projected-separation selection','Deep-limit and co-scaled compact-source assumptions for binary mass multiplier','Version 1 manifest lacks enforced resource/input-freshness record'])
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for row in result['pairs']:print(row['selection'],row['footing'],row['n'],'Gaussian A',row['gaussian']['amplitude'],'circular A',row['circular_top_hat']['amplitude'])
    for row in result['clusters']['density_signs']:print('density sign',row)
if __name__=='__main__':main()
