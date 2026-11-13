"""Sample mass/shear/regularization; Gaussian source+light+sky integrated out."""
import argparse,json,sys,time,multiprocessing as mp
from pathlib import Path
import numpy as np
import emcee
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens
from fit_images_v2 import mass_logprior

def init_worker():
    global inv,lens
    inv=setup(nsource=25,source_pixel=.04,supersample=2);lens=AqualLens()

def logprob(p):
    m,g1,g2,z=p
    if not 11.56<m<12.39 or abs(g1)>.3 or abs(g2)>.3 or not -5<z<18:return -np.inf
    r=inv.evaluate(deflection=lambda X,N:lens.deflection(X,N,m,g1,g2),log_regularization=z,return_arrays=False)
    return r['score']+mass_logprior(m)-.5*((g1/.1)**2+(g2/.1)**2)

def main(out,maxsteps=1800):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);rng=np.random.RandomState(33022026)
    prior=json.loads((BASE/'image_fit_02/result.json').read_text())
    best=np.array(prior['solutions'][-1]['parameters']);start=best+rng.normal(size=(24,4))*[.008,.008,.008,.25]
    t0=time.monotonic();history=[];oldtau=None;converged=False
    with mp.get_context('spawn').Pool(4,initializer=init_worker) as pool:
        sampler=emcee.EnsembleSampler(24,4,logprob,pool=pool)
        sampler.random_state=rng.get_state();state=start
        for stop in range(200,maxsteps+1,200):
            state=sampler.run_mcmc(state,200,progress=False)
            chain=sampler.get_chain();burn=max(100,stop//3)
            tau=sampler.get_autocorr_time(tol=0)
            stability=None if oldtau is None else float(np.max(abs(tau/oldtau-1)))
            oldtau=tau
            rec=dict(steps=stop,seconds=time.monotonic()-t0,tau=tau.tolist(),tau_change=stability,
                     acceptance=float(np.mean(sampler.acceptance_fraction)),burn=burn,
                     q16_q50_q84=np.quantile(chain[burn:].reshape(-1,4),[.16,.5,.84],axis=0).tolist())
            history.append(rec);print(json.dumps(rec),flush=True)
            np.savez_compressed(out/'chain.npz',chain=chain,logprob=sampler.get_log_prob(),acceptance=sampler.acceptance_fraction)
            (out/'progress.json').write_text(json.dumps(history,indent=2)+'\n')
            if stop>=800 and np.all((stop-burn)>40*tau) and stability is not None and stability<.08:
                converged=True;break
    samples=chain[burn:].reshape(-1,4);gamma=np.hypot(samples[:,1],samples[:,2])
    result=dict(scope='Conditional posterior, canonical a0, fixed light shape/edge-on/isolated branch/diagonal RMS; marginalized Gaussian source and nuisance coefficients',converged_by_registered_criterion=converged,maxsteps=maxsteps,steps=stop,seed=33022026,workers=4,nwalkers=24,burn=burn,history=history,parameter_order=['logM','g1','g2','log_source_precision'],quantiles=np.quantile(samples,[.025,.16,.5,.84,.975],axis=0).tolist(),mass_solar_quantiles=np.quantile(10**samples[:,0],[.025,.16,.5,.84,.975]).tolist(),shear_quantiles=np.quantile(gamma,[.025,.16,.5,.84,.975]).tolist(),non_claims=['No posterior marginalization over light shape inclination IMF screening environment or covariance','Not a full-theory pass','Sampling criterion is finite diagnostic, not proof of global convergence'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--maxsteps',type=int,default=1800);a=p.parse_args();main(a.output,a.maxsteps)
