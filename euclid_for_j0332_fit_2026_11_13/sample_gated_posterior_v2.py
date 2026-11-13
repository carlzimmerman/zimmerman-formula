"""Four independent MH chains with a frozen Gaussian independence proposal.

The published 0.3 arcsec source-position association gate is an explicit prior.
The proposal density enters the Hastings ratio; it is not a Laplace posterior.
"""
import argparse,json,sys,time,multiprocessing as mp
from pathlib import Path
import numpy as np
import emcee
BASE=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens
from fit_images_v2 import mass_logprior

def worker(arg):
    index,nsteps=arg;rng=np.random.RandomState(33024000+index)
    inv=setup(nsource=25,source_pixel=.04,supersample=2);lens=AqualLens()
    xy=np.array(json.loads((BASE/'inputs/dataset/positions.json').read_text())['arguments']['values']['array'])
    X=xy[:,1];N=-xy[:,0]
    proposal=np.load(BASE/"gated_proposal.npz");center=proposal["center"];cov=proposal["cov"];chol=np.linalg.cholesky(cov);precision=np.linalg.inv(cov)
    def q(p):
        d=p-center
        return -.5*float(d@precision@d)
    def lp(p):
        m,g1,g2,z=p
        if not 11.56<m<12.39 or max(abs(g1),abs(g2))>.3 or not -5<z<18:return -np.inf
        ax,an=lens.deflection(X,N,m,g1,g2);b=np.array([X-ax,N-an]).T
        if np.sqrt(np.max(np.sum((b[:,None]-b[None,:])**2,axis=-1)))>.3:return -np.inf
        r=inv.evaluate(deflection=lambda x,y:lens.deflection(x,y,m,g1,g2),log_regularization=z,return_arrays=False)
        return r['score']+mass_logprior(m)-.5*((g1/.1)**2+(g2/.1)**2)
    p=center.copy();f=lp(p)
    while not np.isfinite(f):p=center+chol@rng.normal(size=4);f=lp(p)
    chain=[];logvalues=[];naccept=0;t=time.monotonic()
    for j in range(nsteps):
        new=center+chol@rng.normal(size=4);fn=lp(new)
        if np.log(rng.uniform())<fn-f+q(p)-q(new):p=new;f=fn;naccept+=1
        chain.append(p.copy());logvalues.append(f)
    return dict(index=index,seed=33024000+index,chain=np.array(chain),logprob=np.array(logvalues),acceptance=naccept/nsteps,seconds=time.monotonic()-t)

def main(out,nsteps=3000):
    out=Path(out);out.mkdir(exist_ok=True,parents=True)
    with mp.get_context('spawn').Pool(4) as pool:res=pool.map(worker,[(k,nsteps) for k in range(4)])
    chain=np.stack([r['chain'] for r in res],axis=1);burn=500;post=chain[burn:];flat=post.reshape(-1,4)
    tau=emcee.autocorr.integrated_time(post,tol=0)
    # Classical split R-hat on eight half chains; rank-normalized diagnostic
    # is not claimed. Independent kernels/seeds make cross-chain check meaningful.
    half=post.shape[0]//2;split=np.concatenate([post[:half],post[-half:]],axis=1)
    W=np.mean(np.var(split,axis=0,ddof=1),axis=0);B=half*np.var(np.mean(split,axis=0),axis=0,ddof=1)
    rhat=np.sqrt(((half-1)/half*W+B/half)/W)
    criterion=bool(np.all(rhat<1.01) and np.all(len(post)>50*tau))
    result=dict(scope='Compact-source conditional posterior with published0.3arcsec maximum source-separation gate; same mass/shear/linear-source priors as image_fit_02',nchains=4,nsteps=nsteps,burn=burn,proposal_source='gated_proposal.npz fitted to completed pilot then frozen; exact Hastings correction retained',seeds=[r['seed'] for r in res],acceptance=[r['acceptance'] for r in res],seconds=[r['seconds'] for r in res],tau=tau.tolist(),classical_split_rhat=rhat.tolist(),registered_convergence_criterion_met=criterion,quantile_levels=[.025,.16,.5,.84,.975],parameter_order=['logM','g1','g2','loglambda'],quantiles=np.quantile(flat,[.025,.16,.5,.84,.975],axis=0).tolist(),mass_solar_quantiles=np.quantile(10**flat[:,0],[.025,.16,.5,.84,.975]).tolist(),shear_quantiles=np.quantile(np.hypot(flat[:,1],flat[:,2]),[.025,.16,.5,.84,.975]).tolist(),non_claims=['No proof of global convergence','Source association gate is conditional modelling information not new independent spectroscopy','No covariance IMF light shape inclination or external convergence marginalized','No physical-theory pass probability'])
    np.savez_compressed(out/'chains.npz',chain=chain,logprob=np.stack([r['logprob'] for r in res],axis=1));(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--nsteps',type=int,default=3000);a=p.parse_args();main(a.output,a.nsteps)
