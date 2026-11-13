"""Wide-window mass-profile checks; no low-mass exclusion from compact window."""
import argparse,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens,sie_parameters,sie_deflection
from fit_images_v2 import mass_logprior,serial
from run_robustness import source_boundary_diagnostic


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);startall=time.monotonic()
    inv=setup(nsource=33,source_pixel=.06,supersample=2,source_center=(-.03,-.05))
    lens=AqualLens();sie=sie_parameters();trace=[];records=[];archive={}
    baseline=inv.optimize_regularization(deflection=lambda X,N:sie_deflection(X,N,**sie))
    archive['SIE_source']=baseline['source'];archive['SIE_model_valid']=baseline['model_valid']
    p_ref=np.array([12.04148047885273,-.020224029220632385,-.15843063089888157,6.262865391698387])
    def evaluate(p,arrays=False):
        m,g1,g2,z=p
        if not 11.56<m<12.39 or max(abs(g1),abs(g2))>.3 or not -5<z<18:return -1e30,None
        r=inv.evaluate(deflection=lambda X,N:lens.deflection(X,N,m,g1,g2),log_regularization=z,return_arrays=arrays)
        return float(r['score']-.5*((g1/.1)**2+(g2/.1)**2)+mass_logprior(m)),r
    def optimize(name,p0,fixed=None):
        start=time.monotonic();ncall=[0]
        if fixed is not None:p0=np.array(p0)[1:]
        def unpack(x):return np.r_[fixed,x] if fixed is not None else x
        def objective(x):
            p=unpack(x);score,_=evaluate(p)
            if ncall[0]%100==0:print(json.dumps({'job':name,'ncall':ncall[0],'parameters':p.tolist(),'score':score}),flush=True)
            ncall[0]+=1;trace.append({'job':name,'parameters':p.tolist(),'score':score});return -score
        steps=np.array([.03,.03,.5]) if fixed is not None else np.array([.04,.03,.03,.5])
        simplex=np.vstack([p0,*[p0+np.eye(len(p0))[j]*steps[j] for j in range(len(p0))]])
        opt=minimize(objective,p0,method='Nelder-Mead',options={'maxiter':450,'xatol':1e-5,'fatol':.002,'initial_simplex':simplex})
        p=unpack(opt.x);score,r=evaluate(p,True)
        shear=.5*((p[1]/.1)**2+(p[2]/.1)**2)
        rec={'name':name,'fixed_logmass':fixed,'start':unpack(p0).tolist(),'parameters':p.tolist(),
             'score_including_mass_and_shear_priors':score,'score_image_and_shear_prior':float(r['score']-shear),
             'mass_logprior':float(mass_logprior(p[0])),'shear_prior_penalty':float(shear),
             'fit':serial(r),'success':bool(opt.success),'message':str(opt.message),'nfev':opt.nfev,'nit':opt.nit,'seconds':time.monotonic()-start,
             'source_boundary':source_boundary_diagnostic(r['source']),
             'delta_conditional_image_score_vs_fixed_SIE':float(r['score']-baseline['score']),
             'delta_chi2_vs_fixed_SIE':float(r['chi2']-baseline['chi2'])}
        records.append(rec);archive[name+'_source']=r['source'];archive[name+'_model_valid']=r['model_valid']
        print(json.dumps({'completed':name,**rec}),flush=True)
        (out/'progress.json').write_text(json.dumps({'baseline_SIE':serial(baseline),'optimizations':records},indent=2)+'\n')
        return rec
    high=p_ref.copy();high[0]=12.04
    rhigh=optimize('free_start_high',high)
    low=np.array([11.85,sie['g1'],sie['g2'],6.3])
    rlow=optimize('free_start_low',low)
    best=max([rhigh,rlow],key=lambda r:r['score_including_mass_and_shear_priors'])
    med=11.8310873126;sig=.0863788677
    # At the SED median use two distinct shear/precision starts to expose local modes.
    rmed1=optimize('fixed_SED_median_from_high',np.array(best['parameters']),fixed=med)
    rmed2=optimize('fixed_SED_median_from_catalogue_shear',np.array([med,sie['g1'],sie['g2'],6.3]),fixed=med)
    rmed=max([rmed1,rmed2],key=lambda r:r['score_image_and_shear_prior'])
    p=np.array(rmed['parameters'])
    rone=optimize('fixed_SED_upper_1sigma',p,fixed=med+sig)
    # Highest-mass profile start closer to best free branch is an explicit choice.
    rtwo=optimize('fixed_SED_upper_2sigma',np.array(best['parameters']),fixed=med+2*sig)
    for rec in records:
        rec['delta_image_and_shear_score_from_best_free']=rec['score_image_and_shear_prior']-best['score_image_and_shear_prior']
        rec['delta_total_score_from_best_free']=rec['score_including_mass_and_shear_priors']-best['score_including_mass_and_shear_priors']
        rec['delta_chi2_from_best_free']=rec['fit']['chi2']-best['fit']['chi2']
    archive['data']=inv.data;archive['noise']=inv.noise;archive['mask']=inv.mask
    result={'assertion_tested':'A 1.92arcsec outer-node source square permits deflected low-mass source positions; optimize all four parameters from high/low mass and profile shear/precision at three fixed SED masses using that same source representation.',
            'representation':{'nsource':33,'source_pixel_arcsec':.06,'supersampling':2,'source_center_arcsec':[-.03,-.05],'outer_node_side_length_arcsec':1.92,'basis_full_support_side_length_arcsec':2.04},
            'parameter_order':['log10_Mstar_Msun','shear_g1','shear_g2','log_source_precision'],
            'baseline_SIE':serial(baseline),'baseline_SIE_parameters':sie,'baseline_source_boundary':source_boundary_diagnostic(baseline['source']),
            'optimizations':records,'best_free_name':best['name'],
            'summary':{'free_high_logmass':rhigh['parameters'][0],'free_low_logmass':rlow['parameters'][0],
                       'free_objective_difference_high_minus_low':rhigh['score_including_mass_and_shear_priors']-rlow['score_including_mass_and_shear_priors'],
                       'best_free_logmass':best['parameters'][0],'all_optimization_success':all(r['success'] for r in records),'seconds':time.monotonic()-startall},
            'interpretation':'All score comparisons here are conditional on this same wide source grid, proper Gaussian source regularization, fixed light geometry and diagonal RMS. Fixed-mass profiles are finite local optimizations, not a calibrated significance or posterior interval.',
            'non_claims':['No exclusion from a compact source window.','No source-prior-independent mass measurement: regularization may penalize extended or multiply disconnected source reconstructions.','SIE mass parameters remain fixed; matched score differences are not model Bayes factors.','Finite low/high starts and profiles do not establish global maxima.','No full screened-v3s test, stellar population/IMF systematics, or physical-theory pass/fail.']}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(out/'trace.json').write_text(json.dumps(trace)+'\n')
    np.savez_compressed(out/'images_sources.npz',**archive)
    print(json.dumps(result['summary']),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
