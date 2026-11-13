"""Fixed-model nonnegative source MAP sensitivity, NOT marginal evidence."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np
from scipy import linalg,optimize

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path[:0]=[str(BASE),str(BASE/"image_inversion")]
from inversion_continuous import setup
from lens_models import AqualLens,sie_parameters,sie_deflection


def main(output):
    output.mkdir(parents=True,exist_ok=True)
    fit=json.loads((BASE/"image_fit_02/result.json").read_text())
    parameters=fit['solutions'][-1]['parameters']
    lens=AqualLens()
    m,g1,g2,z=parameters
    sie=sie_parameters()
    configs=[('AQUAL_image_fit02',lambda X,N:lens.deflection(X,N,m,g1,g2),z),
             ('fixed_published_SIE',lambda X,N:sie_deflection(X,N,**sie),
              fit['baseline']['log_regularization'])]
    results=[]
    for name,deflect,loglam in configs:
        start=time.monotonic()
        obj=setup(nsource=25,source_pixel=.04,supersample=2)
        unconstrained=obj.evaluate(deflect,log_regularization=loglam,posterior_uncertainty=True)
        n=obj.ns**2
        Q=linalg.block_diag(np.exp(loglam)*obj.R,np.diag([4.,100.]))
        H,b=obj.H0+Q,obj.b
        # A diagonal change of coordinates conditions the same exact QP.
        d=1/np.sqrt(np.diag(H))
        Hp=H*d[:,None]*d[None,:]
        bp=b*d
        c0=unconstrained['coefficient'].copy()
        c0[:n]=np.maximum(c0[:n],0)
        x0=c0/d
        def fg(x):
            return .5*x@Hp@x-bp@x,Hp@x-bp
        opt=optimize.minimize(fg,x0,jac=True,method='L-BFGS-B',
            bounds=[(0.,None)]*n+[(None,None)]*2,
            options={'gtol':1e-9,'ftol':1e-15,'maxiter':10000,'maxls':50,'maxcor':40})
        c=opt.x*d
        grad=Hp@opt.x-bp
        active=np.r_[opt.x[:n]<=1e-10,[False,False]]
        projected=np.where(active& (grad>=0),0.,grad)
        kkt=float(np.max(np.abs(projected)))
        residual=obj.y-obj.WD@c
        chi=float(residual@residual)
        penalty=float(c@Q@c)
        before=float(unconstrained['chi2']+unconstrained['prior_penalty'])
        after=chi+penalty
        # Relative stationarity is also recorded because optimizers can stop
        # on finite objective tolerance before their requested gradient target.
        relative_kkt=kkt/max(1.,float(np.max(np.abs(bp))))
        assert np.min(c[:n])>=-1e-14
        assert after>=before-1e-7
        assert kkt<2e-4 and relative_kkt<1e-7
        row={'name':name,'fixed_log_regularization':float(loglam),
            'fixed_AQUAL_parameters':parameters if name.startswith('AQUAL') else None,
            'optimizer_success':bool(opt.success),'optimizer_message':str(opt.message),
            'iterations':int(opt.nit),'evaluations':int(opt.nfev),
            'scaled_projected_gradient_inf':kkt,'relative_scaled_KKT_inf':relative_kkt,
            'active_source_coefficients':int(active[:n].sum()),
            'min_source_coefficient':float(c[:n].min()),
            'unconstrained_chi2':float(unconstrained['chi2']),
            'positive_MAP_chi2':chi,'chi2_change':chi-unconstrained['chi2'],
            'unconstrained_prior_penalty':float(unconstrained['prior_penalty']),
            'positive_MAP_prior_penalty':penalty,
            'total_quadratic_cost_change':after-before,
            'unconstrained_negative_count':int((unconstrained['source']<0).sum()),
            'unconstrained_negative_gt3_conditional_std_count':int(((unconstrained['source']<0)&
                (-unconstrained['source']/unconstrained['source_std']>3)).sum()),
            'positive_MAP_lens_amplitude':float(1+c[-2]),'positive_MAP_sky':float(c[-1]),
            'unconstrained_lens_amplitude':float(unconstrained['lens_amplitude']),
            'unconstrained_sky':float(unconstrained['sky']),
            'seconds':time.monotonic()-start}
        results.append(row)
        np.savez_compressed(output/(name+'.npz'),
            positive_source=c[:n].reshape(obj.ns,obj.ns),
            unconstrained_source=unconstrained['source'],
            unconstrained_source_std=unconstrained['source_std'],
            positive_model_valid=obj.D@c+obj.lens[obj.mask],
            unconstrained_model_valid=unconstrained['model_valid'],
            mask=obj.mask,data=obj.data,noise=obj.noise,positive_coefficients=c,
            scaled_gradient=grad)
        print(json.dumps(row),flush=True)
    result={'assertion_tested':'At two fixed nonlinear lens models and their previously optimized regularizations, compare Gaussian MAP with source>=0 constrained quadratic MAP and test KKT stationarity',
        'non_claims':['No truncated-Gaussian marginal evidence or Bayes factor','No lens or regularization reoptimization','Not final gated-posterior source physicality','No empirical theory pass/fail'],
        'scope':'Corrected continuous 25x25 source basis,.04arcsec spacing,2x2image rays,same proper source/lens/sky priors and released diagonal noise',
        'gating_note':'AQUAL parameters are frozen image_fit_02 values; later association-gated fits/posteriors are not substituted or certified here',
        'runs':results,'status':'completed'}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
