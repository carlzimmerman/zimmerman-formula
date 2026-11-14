"""Targeted controls and finite conditional noise injections after run_02.

No population posterior and no empirical systematic error is manufactured.
The simulations condition on the best shared stellar mixture, smooth continuum,
native DESI diagonal noise and instrument response, all from the same photons.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/forj0332-mpl-cache')
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fit_dispersion_v3 import Engine,Fit,fit_one,HERE,Z

def quick_fit(engine,config,synthetic,guess):
    f=Fit(engine,config,synthetic)
    opts=[]
    for sigma in [guess-25,guess+25]:
        o=minimize(f.evaluate,[sigma,15.],method='Nelder-Mead',options={
            'initial_simplex':[[sigma,15.],[sigma+15.,15.],[sigma,40.]],
            'maxiter':130,'xatol':.12,'fatol':.0001})
        opts.append(o)
    best=min(opts,key=lambda o:o.fun)
    return {'sigma':float(best.x[0]),'velocity':float(best.x[1]),'chi2':float(best.fun),
        'success':bool(best.success),'start_sigma_difference':float(abs(opts[0].x[0]-opts[1].x[0])),
        'boundary':bool(best.x[0]<100.5 or best.x[0]>449.5),'evaluations':f.count}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True,parents=True);start=time.monotonic()
    previous=json.loads((HERE/'run_02/result.json').read_text())
    primary=previous['results'][0]
    engine=Engine()
    base={'windows':[['B',3800,4380],['R',4950,5500]],'degree':4}
    configs=[dict(base,name='poly2',degree=2),dict(base,name='poly6',degree=6),dict(base,name='poly8',degree=8),
        dict(base,name='old_templates',age_min=3.),
        *[dict(base,name='broad_mask_'+str(width),windows=[['B',3800,4380],['R',4400,5500]],degree=6,mgii_halfwidth=width)
          for width in [100,200,300]],
        dict(base,name='no_mgb',windows=[['B',3800,4380],['R',5220,5500]],degree=4)]
    results=[fit_one(engine,cfg,out) for cfg in configs]
    refined=fit_one(Engine(refine=3),dict(base,name='sampling_0p3A'),out,False)
    weights=np.array([x['weight'] for x in primary['template_weights']])
    poly=np.array(primary['additive_polynomial'])
    A=engine.design(primary['sigma'],primary['velocity'])
    synthetic={}
    for i,(b,lo,hi) in enumerate(base['windows']):
        d=engine.bands[b];rest=d['w']/(1+Z)
        P=np.polynomial.legendre.legvander(2*(rest-lo)/(hi-lo)-1,base['degree'])
        synthetic[b]=A[b]@weights+d['R']@(P@poly[i*5:(i+1)*5])
    # Orthogonal reconstruction check against the stored fitted good-pixel model.
    original=np.load(HERE/'run_02/primary_split_model.npz')
    match=Fit(engine,base)
    rebuilt=np.concatenate([synthetic[b][m] for b,m in match.blocks])
    reconstruction_error=float(np.max(abs(rebuilt-original['best_model'])))
    assert reconstruction_error<1e-10
    seed=20261113;rng=np.random.default_rng(seed);simulations=[]
    for k in range(48):
        draw={}
        for b,d in engine.bands.items():
            scale=np.zeros_like(d['ivar']);good=d['ivar']>0
            scale[good]=1/np.sqrt(d['ivar'][good])
            draw[b]=synthetic[b]+rng.normal(size=len(scale))*scale
        row={'draw':k}
        for b,name,window in [('B','blue',['B',3800,4380]),('R','red',['R',4950,5500])]:
            row[name]=quick_fit(engine,dict(base,windows=[window]),draw,primary['sigma'])
        row['blue_minus_red']=row['blue']['sigma']-row['red']['sigma']
        simulations.append(row)
        if (k+1)%8==0:print('completed conditional noise draws',k+1,flush=True)
    observed=previous['results'][1]['sigma']-previous['results'][2]['sigma']
    differences=np.array([x['blue_minus_red'] for x in simulations])
    residual_diagnostics={}
    for b in 'BR':
        m=original['band']==b
        w=original['wave'][m];r=(original['flux'][m]-original['best_model'][m])*original['weight'][m]
        adjacent=np.abs(np.diff(w)-.8)<1e-5
        lag1=float(np.mean(r[:-1][adjacent]*r[1:][adjacent]))
        residual_diagnostics[b]={'n':int(m.sum()),'mean':float(r.mean()),'rms':float(np.sqrt(np.mean(r*r))),
            'adjacent_lag1_mean_product':lag1,'fraction_abs_gt3':float(np.mean(abs(r)>3))}
    result={'controls':results,'sampling_control':refined,'sampling_delta_sigma_kms':refined['sigma']-primary['sigma'],
        'conditional_noise':{'seed':seed,'generator':'numpy PCG64 default_rng','draws':48,'truth_sigma':primary['sigma'],
        'truth_velocity':primary['velocity'],'full_model_reconstruction_max_error':reconstruction_error,
        'observed_blue_minus_red_kms':observed,'simulated_difference_quantiles':dict(zip(['q025','q16','q50','q84','q975'],np.quantile(differences,[.025,.16,.5,.84,.975]).tolist())),
        'count_abs_difference_at_least_observed':int(np.sum(abs(differences)>=abs(observed))),
        'count_positive_difference_at_least_observed':int(np.sum(differences>=observed)),
        'unsuccessful_optimizers':sum(not row[b]['success'] for row in simulations for b in ['blue','red']),
        'boundaries':sum(row[b]['boundary'] for row in simulations for b in ['blue','red']),
        'max_start_sigma_disagreement':max(row[b]['start_sigma_difference'] for row in simulations for b in ['blue','red']),
        'simulations':simulations,'interpretation':'Finite conditional parametric injection frequency, not calibrated astrophysical p-value or complete uncertainty.'},
        'primary_residual_diagnostics':residual_diagnostics,'elapsed_seconds':time.monotonic()-start,
        'non_claims':['No complete uncertainty or systematic-error estimate','No independent significance against Guo or FastSpec','No full quasar/FeII model','No stellar mass, aperture correction or theory fit']}
    (out/'result.json').write_text(json.dumps(result,indent=2))
    fig,axes=plt.subplots(1,2,figsize=(12,5),constrained_layout=True)
    ref=np.array(primary['profile']);axes[0].plot(ref[:,0],ref[:,2]-primary['chi2'],'k',lw=2,label='run02 primary')
    for r in results:
        p=np.array(r['profile']);axes[0].plot(p[:,0],p[:,2]-r['chi2'],label=r['config']['name'])
    axes[0].axhline(1,color='grey',lw=.5);axes[0].axhline(4,color='grey',lw=.5)
    axes[0].set(xlim=(150,350),ylim=(0,12),xlabel='Stellar dispersion (km/s)',ylabel='Profile delta chi-square')
    axes[0].legend(fontsize=7,ncol=2)
    axes[1].hist(differences,bins=12,color='grey',label='48 conditional noise injections')
    axes[1].axvline(observed,color='tab:red',label='Observed blue minus red')
    axes[1].set(xlabel='Blue minus red fitted dispersion (km/s)',ylabel='Draw count');axes[1].legend(fontsize=8)
    fig.savefig(out/'controls_and_noise.png',dpi=150);plt.close(fig)
    print('noise difference quantiles',result['conditional_noise']['simulated_difference_quantiles'],flush=True)
    print('noise exceedance count',result['conditional_noise']['count_abs_difference_at_least_observed'],'/48',flush=True)

if __name__=='__main__':main()
