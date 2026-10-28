#!/usr/bin/env python3
"""Independent fixed interpolation-support bound; no observational scoring."""
import argparse, hashlib, json, math, resource, sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; REB=ROOT/'rebuild_2026_10_22'
FILES=[HERE/'SUPPORT_BOUND_CRITERIA.md',HERE/'lens_support_bound.py',
       REB/'X53_outer_lensing_law_vs_halos/x53_outer_lensing.py',REB/'F2_outer_lensing/f2_outer_lensing.py',
       REB/'EM1_emergent_dust_law/em1_emergent_results.json',REB/'X43_collapse_core_floor/x43_collapse_core_results.json',
       REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',
       ROOT/'real_research/data/lensing_rar/lr_lenses.npz',ROOT/'real_research/data/lensing_rar/cfg110_perlens.npz']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
    hashes={str(p.relative_to(ROOT)):sha(p) for p in FILES};args.output.mkdir(parents=True,exist_ok=True)
    out=dict(mutate=args.mutate,checks={},input_sha256=hashes)
    def check(k,ok,d):
        out['checks'][k]=dict(pass_=bool(ok),detail=d);print(k,'PASS' if ok else 'FAIL',json.dumps(d,sort_keys=True),flush=True)
    ln=np.load(FILES[-2]);pl=np.load(FILES[-1]);lm70=ln['logM'];z=ln['z'];w=np.asarray(pl['WW'].sum(axis=1),float)
    check('K0_weights',np.all(np.isfinite(w)) and np.all(w>=0),dict(rows=len(w),positive=int(np.sum(w>0)),negative=int(np.sum(w<0)),zero=int(np.sum(w==0))))
    if not out['checks']['K0_weights']['pass_']:raise RuntimeError('Nonnegative-weight assumption fails')
    def chi(z,om):
        zz=np.linspace(0,1,4001);ee=np.sqrt(om*(1+zz)**3+1-om)
        cc=np.r_[0,np.cumsum(.5*(1/ee[1:]+1/ee[:-1])*np.diff(zz))]
        return np.interp(z,zz,cc)
    qda=chi(z,.3085)/chi(z,.3);native=lm70+2*np.log10(.70/.679)+2*np.log10(qda)
    bins=np.digitize(lm70,[8.5,10.3,10.6,10.8,11.0001])-1;grid=np.round(np.arange(6.8,11.81,.02),2)
    used=(bins>=0)&(bins<4)&(w>0)
    check('K1_distances',np.all(np.isfinite(native[used])),dict(used_lenses=int(np.sum(used))))
    supports={};worst=0.;sumworst=0.
    for b in range(4):
        take=(bins==b)&(w>0);x=native[take];ww=w[take];right=np.searchsorted(grid,x,side='right');right=np.clip(right,1,len(grid)-1);left=right-1
        frac=np.clip((x-grid[left])/(grid[right]-grid[left]),0,1)
        agg=np.bincount(left,weights=ww*(1-frac),minlength=len(grid))+np.bincount(right,weights=ww*frac,minlength=len(grid))
        if args.mutate and b==0:agg[int(np.argmax(agg))]*=1.1
        diffs=[]
        for v in (np.ones(len(grid)),np.arange(len(grid),dtype=float),np.arange(len(grid),dtype=float)**2):
            direct=float(np.sum(np.interp(x,grid,v)*ww));sparse=float(np.dot(agg,v));diffs.append(abs(direct-sparse)/max(1.,abs(direct)))
        worst=max(worst,max(diffs));sumworst=max(sumworst,abs(float(agg.sum()/ww.sum())-1))
        supports[str(b)]=dict(bin_lenses=int(np.sum(bins==b)),positive_weight_lenses=int(np.sum(take)),total_weight=float(ww.sum()),
                              support_indices=np.flatnonzero(agg>0).tolist(),support_weights=agg[agg>0].tolist(),
                              native_logMs_min=float(x.min()),native_logMs_max=float(x.max()))
    check('K2_interpolation_support',worst<=1e-12,dict(max_relative_error=worst))
    check('K3_weight_conservation',sumworst<=1e-12,dict(max_relative_error=sumworst))
    jj=sorted(set(j for v in supports.values() for j in v['support_indices']));out['support']=supports
    rel=json.loads(FILES[4].read_text())['rows']['A_c2b_refit']['R1'];aa,bb=rel['a'],rel['b']
    lm=grid[np.array(jj)];lmcat=lm-2*np.log10(.70/.679);lmc=lm+(-.69*lmcat+6.63);lmb=np.log10(10**lm+10**lmc);lhalo=aa+bb*(lmb-10)
    a2=json.loads(FILES[6].read_text())['cf_by_mass'];shape=[a2[k] for k in ('1e+12','1e+13','1e+14')]
    q=np.interp(lhalo,[12.,13.,14.],shape)/shape[2];amp=4/(3*(3*math.log(2)-math.pi/2))
    ss=sorted((math.log10(float(k)),math.log10(v[0])) for k,v in json.loads(FILES[5].read_text())['sigma_coll_table'].items());sx,sy=np.array(ss).T
    sig=np.interp(lhalo,sx,sy);lo=lhalo<sx[0];hi=lhalo>sx[-1]
    sig[lo]=sy[0]+(sy[1]-sy[0])/(sx[1]-sx[0])*(lhalo[lo]-sx[0]);sig[hi]=sy[-1]+(sy[-1]-sy[-2])/(sx[-1]-sx[-2])*(lhalo[hi]-sx[-1]);sig=10**sig
    bound={};above=[];below=[]
    for f,a0 in (('canonical',9.3603e-11),('alt',1.1312e-10)):
        floor=a0*3.0857e16/1e6/(2*math.pi*4.30091e-3);crit=(floor/(amp*sig))**.8/q;ix=int(np.argmax(crit));val=float(crit[ix])
        above.append(bool(np.all(amp*(val*(1+1e-6)*q)**1.25*sig>floor)));below.append(bool(np.any(amp*(val*(1-1e-6)*q)**1.25*sig<floor)))
        bound[f]=dict(necessary_L_upper_bound=val,witness_stellar_grid_index=jj[ix],witness_logMstar=float(lm[ix]),witness_logM200=float(lhalo[ix]),floor=floor,
                      support_critical_levels=crit.tolist())
    out['bound']=bound;out['support_halo_logmass']=[float(x) for x in lhalo];out['union_support_indices']=jj
    check('K4_above_bound_all_halo',all(above),dict(by_footing=above))
    check('K5_below_bound_has_floor',all(below),dict(by_footing=below))
    check('K6_inputs_stable',hashes=={str(p.relative_to(ROOT)):sha(p) for p in FILES},'All declared inputs unchanged')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=='darwin' else 1e6)
    check('K7_RSS',peak<1.,'Measured RSS <1GB; no enforced address-space cap');print('PEAK_RSS_GB',peak)
    out['scope']='Necessary upper bound for inherited strict ENV-vs-pureHalo comparison; not sufficient, not a continuous-L or all-data exclusion.'
    (args.output/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n')
    n=sum(v['pass_'] for v in out['checks'].values());print(f'CSM1_SUPPORT_BOUND COMPLETE: {n}/{len(out["checks"])} checks PASS.')
    return 0 if n==len(out['checks']) else 1
if __name__=='__main__':raise SystemExit(main())
