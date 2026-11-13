"""Conditional source-association gates, explicitly not independent new data."""
import argparse,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens,sie_parameters,sie_deflection
from fit_images_v2 import mass_logprior,serial
from run_robustness import source_boundary_diagnostic


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    lens=AqualLens();sie=sie_parameters()
    positions=np.asarray(json.loads((BASE/'inputs/dataset/positions.json').read_text())['arguments']['values']['array'])
    meta=json.loads((BASE/'inputs/dataset/positions_meta.json').read_text())
    assert meta['threshold']==.3 and np.allclose(positions,np.asarray(meta['positions_used']))
    X,N=positions[:,1],-positions[:,0]  # released pipeline (south,west) -> (west,north)
    pairs=np.array([(i,j) for i in range(len(X)) for j in range(i)])
    def position_stat(p,kappa=0.):
        ax,an=lens.deflection(X,N,*p[:3],kappa_external=kappa);beta=np.column_stack([X-ax,N-an])
        d2=np.sum((beta[pairs[:,0]]-beta[pairs[:,1]])**2,axis=1)
        return {'max_pair_separation_arcsec':float(np.sqrt(d2.max())),'pair_separation_squared_arcsec2':d2.tolist(),'beta_west_north_arcsec':beta.tolist()}
    bounds=[(11.56001,12.38999),(-.29999,.29999),(-.29999,.29999),(-4.999,17.999)]
    ref=np.array([12.04148047885273,-.020224029220632385,-.15843063089888157,6.262865391698387])
    cases=[];archive={};trace=[]
    for label,ns,h in [('wide33_h006',33,.06),('compact25_h004',25,.04)]:
        inv=setup(nsource=ns,source_pixel=h,supersample=2,source_center=(-.03,-.05))
        baseline=inv.optimize_regularization(deflection=lambda x,y:sie_deflection(x,y,**sie))
        archive[label+'_SIE_source']=baseline['source'];archive[label+'_SIE_model_valid']=baseline['model_valid']
        case={'name':label,'nsource':ns,'source_pixel_arcsec':h,'supersampling':2,'source_center_arcsec':[-.03,-.05],
              'baseline_fixed_SIE':serial(baseline),'optimizations':[]}
        def evaluate(p,arrays=False):
            m,g1,g2,z=p
            r=inv.evaluate(deflection=lambda x,y:lens.deflection(x,y,m,g1,g2),log_regularization=z,return_arrays=arrays)
            return float(r['score']-.5*((g1/.1)**2+(g2/.1)**2)+mass_logprior(m)),r
        for threshold in [.3,.5]:
            # A cushion is used so the final reported parameters satisfy the published <= gate.
            effective=threshold-1e-6
            con=lambda p:effective**2-np.array(position_stat(p)['pair_separation_squared_arcsec2'])
            seeds=[('high',ref.copy())]
            if label.startswith('wide'):seeds.append(('low',np.array([11.85,sie['g1'],sie['g2'],6.3])))
            for seedname,seed in seeds:
                name=f'{label}_gate{threshold:.1f}_{seedname}';start=time.monotonic()
                # Cheap feasibility projection changes only mass/shear before image optimization.
                proj=minimize(lambda q:float(np.sum(((q-seed[:3])/.05)**2)),seed[:3],method='SLSQP',bounds=bounds[:3],
                    constraints=[{'type':'ineq','fun':lambda q:con(np.r_[q,seed[3]])}],options={'ftol':1e-10,'maxiter':150})
                p0=np.r_[proj.x,seed[3]]
                if min(con(p0)) < -1e-7:raise RuntimeError('Could not construct feasible position-gate start')
                calls=[0];best={'score':-np.inf,'p':None}
                def objective(p):
                    score,_=evaluate(p)
                    dmax=position_stat(p)['max_pair_separation_arcsec']
                    if dmax<=threshold and score>best['score']:best.update(score=score,p=p.copy())
                    if calls[0]%100==0:print(json.dumps({'case':name,'evaluation':calls[0],'parameters':p.tolist(),'score':score,'position_dmax':dmax}),flush=True)
                    calls[0]+=1;trace.append({'case':name,'parameters':p.tolist(),'score':score,'position_dmax':dmax})
                    return -(score-baseline['score'])/100
                opt=minimize(objective,p0,method='SLSQP',bounds=bounds,constraints=[{'type':'ineq','fun':con}],
                             options={'maxiter':180,'ftol':1e-7,'eps':1e-5})
                final=opt.x;final_score,_=evaluate(final)
                final_dmax=position_stat(final)['max_pair_separation_arcsec']
                selection='optimizer_final'
                if final_dmax>threshold or best['score']>final_score+1e-6:
                    if best['p'] is None:raise RuntimeError('No feasible image evaluation found')
                    final=best['p'];selection='best_feasible_evaluated_point'
                score,r=evaluate(final,True);positions_out=position_stat(final)
                assert positions_out['max_pair_separation_arcsec']<=threshold+1e-12
                rec={'name':name,'gate_arcsec':threshold,'start_type':seedname,'raw_seed':seed.tolist(),'feasible_start':p0.tolist(),
                     'parameters':final.tolist(),'score_including_mass_and_shear_priors':score,
                     'score_image_and_shear_prior':float(r['score']-.5*((final[1]/.1)**2+(final[2]/.1)**2)),
                     'fit':serial(r),'position_statistics':positions_out,'source_boundary':source_boundary_diagnostic(r['source']),
                     'selection':selection,'optimizer_success':bool(opt.success),'optimizer_message':str(opt.message),'optimizer_nfev':opt.nfev,'optimizer_nit':opt.nit,
                     'optimizer_final_parameters':opt.x.tolist(),'optimizer_final_position_dmax':final_dmax,
                     'delta_conditional_image_score_vs_fixed_SIE':float(r['score']-baseline['score']),
                     'delta_chi2_vs_fixed_SIE':float(r['chi2']-baseline['chi2']),'seconds':time.monotonic()-start}
                case['optimizations'].append(rec);archive[name+'_source']=r['source'];archive[name+'_model_valid']=r['model_valid']
                print(json.dumps({'completed':name,**rec}),flush=True)
                (out/'progress.json').write_text(json.dumps({'completed_cases':cases,'current_case':case},indent=2)+'\n')
        cases.append(case)
    archive['data']=inv.data;archive['noise']=inv.noise;archive['mask']=inv.mask
    best=[]
    for case in cases:
        for threshold in [.3,.5]:
            r=max([x for x in case['optimizations'] if x['gate_arcsec']==threshold],key=lambda x:x['score_including_mass_and_shear_priors'])
            best.append({'representation':case['name'],'gate_arcsec':threshold,'name':r['name'],'parameters':r['parameters'],
                         'max_pair_separation_arcsec':r['position_statistics']['max_pair_separation_arcsec'],
                         'score_including_mass_and_shear_priors':r['score_including_mass_and_shear_priors'],
                         'delta_conditional_image_score_vs_fixed_SIE':r['delta_conditional_image_score_vs_fixed_SIE']})
    environment=position_stat(np.array([11.8310873126,-.0138249,-.11248273,0.]),kappa=.30879265)
    environment.update(logmass=11.8310873126,kappa_external=.30879265,g1=-.0138249,g2=-.11248273,parameters_from='root-provided rounded fixed-SED environment fit',passes_03=environment['max_pair_separation_arcsec']<=.3,passes_05=environment['max_pair_separation_arcsec']<=.5)
    result={'assertion_tested':'Local four-parameter image optimization under released source-position association gate dmax<=.3arcsec and .5 sensitivity, on matched wide/compact continuous source grids.',
            'positions_pipeline_south_west_arcsec':positions.tolist(),'positions_west_north_arcsec':np.column_stack([X,N]).tolist(),
            'released_positions_method':meta['method'],'released_positions_threshold_arcsec':meta['threshold'],
            'parameter_order':['log10_Mstar_Msun','shear_g1','shear_g2','log_source_precision'],
            'cases':cases,'fixed_SED_environment_position_check':environment,'best_per_gate_and_representation':best,'seconds':time.monotonic()-started,
            'non_claims':['The four-point source association is a released pipeline consistency condition, not independent new observations or proof of exact source-point identity.','These are conditional strongly-lensed branch fits, not a global posterior over unconstrained extended-source models.','A hard gate has no calibrated likelihood meaning; .5arcsec is a declared sensitivity choice.','Local SLSQP and finite starts do not establish global optima.','Fixed catalogue SIE comparisons are not model Bayes factors.','No full screened-v3s theory certificate or systematics-complete stellar-mass inference.']}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(out/'trace.json').write_text(json.dumps(trace)+'\n')
    np.savez_compressed(out/'images_sources.npz',**archive);print(json.dumps(best,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
