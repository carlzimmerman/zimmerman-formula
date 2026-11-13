"""Conditional image inference: oblate unscreened AQUAL plus external shear.

Integrate Gaussian source/light/sky coefficients analytically. Optimize or
sample the proper source regularization along with mass and shear. Catalogue
mass prior is a two-half-normal quantile surrogate, not a rerun of stellar SEDs.
"""
import argparse,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens,sie_parameters,sie_deflection

def mass_logprior(m):
    med=11.8310873126;sd=.1041923878 if m<med else .0863788677
    return -.5*((m-med)/sd)**2-np.log(sd)

def serial(r):
    return {k:v for k,v in r.items() if k not in ['source','model_valid','coefficient']}

def main(out,nsource=25,source_pixel=.04,ss=2):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    inv=setup(nsource=nsource,source_pixel=source_pixel,supersample=ss)
    lens=AqualLens();sie=sie_parameters();trace=[]
    baseline=inv.optimize_regularization(deflection=lambda X,N:sie_deflection(X,N,**sie))
    np.savez_compressed(out/'baseline.npz',source=baseline['source'],model_valid=baseline['model_valid'],mask=inv.mask,data=inv.data,noise=inv.noise)
    def evaluate(p,prior=True,arrays=False,a0ratio=1.):
        m,g1,g2,z=p
        if not 11.56<m<12.39 or max(abs(g1),abs(g2))>.3 or not -5<z<18:return -1e30,None
        fn=lambda X,N:lens.deflection(X,N,m,g1,g2,a0_ratio=a0ratio)
        r=inv.evaluate(deflection=fn,log_regularization=z,return_arrays=arrays)
        # Gaussian shear prior: each component mean0 sigma.10. No catalogue
        # shear constraint is recycled as independent data.
        score=r['score']-.5*((g1/.1)**2+(g2/.1)**2)
        if prior:score+=mass_logprior(m)
        return score,r
    solutions=[]
    for name,use_prior in [('image_only',False),('stellar_prior',True)]:
        start=time.monotonic()
        if solutions:p0=np.array(solutions[0]['parameters'])
        else:p0=np.array([12.05,sie['g1'],sie['g2'],6.5])
        def objective(p):
            score,r=evaluate(p,prior=use_prior)
            if len(trace)%50==0:print(name,len(trace),p.tolist(),score,flush=True)
            trace.append(dict(kind=name,p=p.tolist(),score=float(score)))
            return -score
        opt=minimize(objective,p0,method='Nelder-Mead',options={'maxiter':450,'xatol':1e-5,'fatol':.002,
              'initial_simplex':np.vstack([p0,p0+[.025,0,0,0],p0+[0,.02,0,0],p0+[0,0,.02,0],p0+[0,0,0,.5]])})
        score,r=evaluate(opt.x,prior=use_prior,arrays=True)
        rec=dict(name=name,parameters=opt.x.tolist(),score=score,success=bool(opt.success),message=str(opt.message),evaluations=opt.nfev,seconds=time.monotonic()-start,fit=serial(r))
        solutions.append(rec)
        np.savez_compressed(out/(name+'.npz'),source=r['source'],model_valid=r['model_valid'],mask=inv.mask,data=inv.data,noise=inv.noise,source_mask=inv.source_mask)
        print(json.dumps(rec),flush=True)
        (out/'progress.json').write_text(json.dumps(dict(baseline=serial(baseline),solutions=solutions),indent=2)+'\n')
    # Finite-difference curvature is diagnostic, not a replacement for sampling.
    p=np.array(solutions[-1]['parameters']);steps=np.array([.0008,.0008,.0008,.035]);H=np.zeros((4,4));f=lambda x:-evaluate(x,prior=True)[0];f0=f(p)
    for i in range(4):
        ei=np.eye(4)[i]*steps[i];H[i,i]=(f(p+ei)-2*f0+f(p-ei))/steps[i]**2
        for j in range(i):
            ej=np.eye(4)[j]*steps[j];H[i,j]=H[j,i]=(f(p+ei+ej)-f(p+ei-ej)-f(p-ei+ej)+f(p-ei-ej))/(4*steps[i]*steps[j])
    result=dict(scope='Conditional isolated edge-on smooth unscreened AQUAL, constant stellar M/L, fixed observed light shape, fitted external shear; diagonal released RMS likelihood',parameter_order=['logMstar','shear_g1','shear_g2','log_source_precision'],nsource=nsource,source_pixel=source_pixel,supersampling=ss,baseline=serial(baseline),solutions=solutions,hessian=H.tolist(),hessian_eigenvalues=np.linalg.eigvalsh(H).tolist(),non_claims=['Not screened-v3s completion','No calibrated physical-theory p-value','No independent source-redshift/dark-energy measurement','Not final marginalized posterior yet'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(out/'trace.json').write_text(json.dumps(trace)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--nsource',type=int,default=25);p.add_argument('--source-pixel',type=float,default=.04);p.add_argument('--ss',type=int,default=2);a=p.parse_args();main(a.output,a.nsource,a.source_pixel,a.ss)
