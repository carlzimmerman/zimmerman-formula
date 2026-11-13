"""Finite source representation and multistart checks, not posterior uncertainty.
Only the corrected continuous zero-padded bilinear source module is imported.
"""
import argparse
import json
import sys
import time
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens,sie_parameters,sie_deflection
from fit_images_v2 import mass_logprior,serial


def source_boundary_diagnostic(source):
    mask=np.zeros_like(source,dtype=bool)
    mask[:2]=True;mask[-2:]=True;mask[:,:2]=True;mask[:,-2:]=True
    absolute=np.abs(source)
    positive=np.maximum(source,0.)
    return {'outer_two_rings_absolute_coefficient_fraction':float(absolute[mask].sum()/max(absolute.sum(),1e-100)),
            'outer_two_rings_positive_coefficient_fraction':float(positive[mask].sum()/max(positive.sum(),1e-100)),
            'max_abs_boundary_over_peak':float(absolute[mask].max()/max(absolute.max(),1e-100))}


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    lens=AqualLens();sie=sie_parameters()
    reference=json.loads((BASE/'image_fit_02/result.json').read_text())
    p_ref=np.array(next(s['parameters'] for s in reference['solutions'] if s['name']=='stellar_prior'))
    cases=[('resolution33_h003',33,.03,3,(-.03,-.05)),
           ('window33_h004',33,.04,3,(-.03,-.05)),
           ('shifted25_h004',25,.04,3,(-.01,-.03)),
           ('original25_h004_multistart',25,.04,2,(-.03,-.05))]
    all_cases=[];trace=[];archive={};start_all=time.monotonic()
    for label,ns,h,ss,center in cases:
        start_case=time.monotonic()
        inv=setup(nsource=ns,source_pixel=h,supersample=ss,source_center=center)
        baseline=inv.optimize_regularization(deflection=lambda X,N:sie_deflection(X,N,**sie))
        base_score=float(baseline['score'])
        base_shear_penalty=.5*((sie['g1']/.1)**2+(sie['g2']/.1)**2)
        record={'case':label,'nsource':ns,'source_pixel_arcsec':h,'supersampling':ss,'source_center_arcsec':list(center),
                'outer_node_side_length_arcsec':(ns-1)*h,'basis_full_support_side_length_arcsec':(ns+1)*h,
                'baseline_SIE':serial(baseline),'baseline_SIE_parameters':sie,
                'baseline_SIE_shear_prior_penalty':float(base_shear_penalty),
                'baseline_source_boundary':source_boundary_diagnostic(baseline['source']),'optimizations':[]}
        archive[label+'_baseline_source']=baseline['source'];archive[label+'_baseline_model_valid']=baseline['model_valid']
        def evaluate(p,a0ratio=1.,arrays=False):
            m,g1,g2,z=p
            canonical_m=m-np.log10(a0ratio)
            if not 11.56<m<12.39 or not lens.logmass[0]<=canonical_m<=lens.logmass[-1] or max(abs(g1),abs(g2))>.3 or not -5<z<18:
                return -1e30,None
            r=inv.evaluate(deflection=lambda X,N:lens.deflection(X,N,m,g1,g2,a0_ratio=a0ratio),log_regularization=z,return_arrays=arrays)
            score=r['score']-.5*((g1/.1)**2+(g2/.1)**2)+mass_logprior(m)
            return float(score),r
        jobs=[]
        if label.startswith('original'):
            for m in [12.,12.08]:
                for shift in [-.03,.03]:
                    p=p_ref.copy();p[0]=m;p[1:3]+=shift
                    jobs.append((f'canonical_m{m:.2f}_shearshift{shift:+.2f}',p,1.))
        else:
            jobs=[('canonical',p_ref.copy(),1.)]
        for name,p0,a0ratio in jobs:
            start=time.monotonic();ncall=[0]
            def objective(p):
                value,_=evaluate(p,a0ratio)
                if ncall[0]%100==0:print(json.dumps({'case':label,'job':name,'evaluation':ncall[0],'p':p.tolist(),'score':value}),flush=True)
                ncall[0]+=1;trace.append({'case':label,'job':name,'p':p.tolist(),'score':value})
                return -value
            simplex=np.vstack([p0,p0+[.025,0,0,0],p0+[0,.02,0,0],p0+[0,0,.02,0],p0+[0,0,0,.5]])
            opt=minimize(objective,p0,method='Nelder-Mead',options={'maxiter':450,'xatol':1e-5,'fatol':.002,'initial_simplex':simplex})
            score,r=evaluate(opt.x,a0ratio,arrays=True)
            rr={'name':name,'a0_ratio':a0ratio,'start':p0.tolist(),'parameters':opt.x.tolist(),'score_including_mass_and_shear_priors':score,
                'success':bool(opt.success),'message':str(opt.message),'nfev':opt.nfev,'nit':opt.nit,'seconds':time.monotonic()-start,
                'fit':serial(r),'delta_conditional_image_score_vs_fixed_SIE':float(r['score']-base_score),
                'delta_chi2_vs_fixed_SIE':float(r['chi2']-baseline['chi2']),
                'shear_prior_penalty':float(.5*((opt.x[1]/.1)**2+(opt.x[2]/.1)**2)),
                'mass_logprior':float(mass_logprior(opt.x[0])),
                'source_boundary':source_boundary_diagnostic(r['source'])}
            record['optimizations'].append(rr)
            key=label+'_'+name;archive[key+'_source']=r['source'];archive[key+'_model_valid']=r['model_valid']
            print(json.dumps({'completed':label,**rr}),flush=True)
            (out/'progress.json').write_text(json.dumps({'completed_cases':all_cases,'current_case':record},indent=2)+'\n')
        if label.startswith('original'):
            # Alternative a0 via exact joint AQUAL homogeneity and canonical library.
            name='alternative_a0';a0ratio=1.1312e-10/9.3603e-11
            best=max(record['optimizations'],key=lambda r:r['score_including_mass_and_shear_priors'])
            p0=np.array(best['parameters']);p0[0]-=.02
            start=time.monotonic();ncall=[0]
            def objective(p):
                value,_=evaluate(p,a0ratio)
                if ncall[0]%100==0:print(json.dumps({'case':label,'job':name,'evaluation':ncall[0],'p':p.tolist(),'score':value}),flush=True)
                ncall[0]+=1;trace.append({'case':label,'job':name,'p':p.tolist(),'score':value});return -value
            opt=minimize(objective,p0,method='Nelder-Mead',options={'maxiter':450,'xatol':1e-5,'fatol':.002,
                'initial_simplex':np.vstack([p0,p0+[.025,0,0,0],p0+[0,.02,0,0],p0+[0,0,.02,0],p0+[0,0,0,.5]])})
            score,r=evaluate(opt.x,a0ratio,arrays=True)
            rr={'name':name,'a0_ratio':a0ratio,'start':p0.tolist(),'parameters':opt.x.tolist(),'score_including_mass_and_shear_priors':score,
                'success':bool(opt.success),'message':str(opt.message),'nfev':opt.nfev,'nit':opt.nit,'seconds':time.monotonic()-start,
                'fit':serial(r),'delta_conditional_image_score_vs_fixed_SIE':float(r['score']-base_score),
                'delta_chi2_vs_fixed_SIE':float(r['chi2']-baseline['chi2']),
                'shear_prior_penalty':float(.5*((opt.x[1]/.1)**2+(opt.x[2]/.1)**2)),
                'mass_logprior':float(mass_logprior(opt.x[0])),
                'source_boundary':source_boundary_diagnostic(r['source'])}
            record['optimizations'].append(rr);archive[label+'_'+name+'_source']=r['source'];archive[label+'_'+name+'_model_valid']=r['model_valid']
            print(json.dumps({'completed':label,**rr}),flush=True)
        record['seconds']=time.monotonic()-start_case
        all_cases.append(record)
        (out/'progress.json').write_text(json.dumps({'completed_cases':all_cases},indent=2)+'\n')
    # Same detector mask/data/noise across cases; store once and assert matched baseline counts.
    assert len(set(c['baseline_SIE']['n_pixels'] for c in all_cases))==1
    archive['data']=inv.data;archive['noise']=inv.noise;archive['mask']=inv.mask
    canonical=[max([r for r in c['optimizations'] if r['a0_ratio']==1.],key=lambda r:r['score_including_mass_and_shear_priors']) for c in all_cases]
    mass=np.array([r['parameters'][0] for r in canonical])
    result={'assertion_tested':'Finite source-resolution, finite-window, source-centering and multistart robustness of corrected continuous-basis conditional AQUAL image optimization.',
            'parameter_order':['log10_Mstar_Msun','shear_g1','shear_g2','log_source_precision'],
            'reference_image_fit02_parameters':p_ref.tolist(),'cases':all_cases,
            'summary':{'best_canonical_logmass_per_case':mass.tolist(),'canonical_mass_spread_dex':float(np.ptp(mass)),
                       'canonical_mass_max_to_min_ratio':float(10**np.ptp(mass)),
                       'canonical_max_abs_logmass_shift_from_reference':float(max(abs(mass-p_ref[0]))),
                       'all_optimization_success':all(r['success'] for c in all_cases for r in c['optimizations']),
                       'total_seconds':time.monotonic()-start_all},
            'non_claims':['Spread across representations is a robustness diagnostic, not a confidence/credible interval.','Fixed catalogue SIE parameters are not optimized or marginalized: score differences are not model Bayes factors.','Same conditional stellar-mass and Gaussian shear priors as fit_images_v2.py; no spectroscopic-redshift SED refit.','Source Gaussian prior allows negative coefficients; conditional source-marginal score depends on discretization and proper regularization.','Unscreened isolated edge-on constant-M/L model and diagonal released RMS only.','Finite multistart optimization does not establish a global maximum.']}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'trace.json').write_text(json.dumps(trace)+'\n')
    np.savez_compressed(out/'images_sources.npz',**archive)
    print(json.dumps(result['summary']),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
