"""Sensitivity only: free uniform external convergence, no environmental data."""
import argparse,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens
from fit_images_v2 import mass_logprior,serial

def main(out):
    out=Path(out);out.mkdir(exist_ok=True,parents=True);inv=setup(nsource=25,source_pixel=.04,supersample=2);lens=AqualLens();records=[]
    def evaluate(p,arrays=False):
        m,g1,g2,z,k=p
        if not 11.56<m<12.39 or max(abs(g1),abs(g2))>.3 or not -5<z<18 or not -.2<k<.5:return -1e30,None
        r=inv.evaluate(deflection=lambda X,N:lens.deflection(X,N,m,g1,g2,kappa_external=k),log_regularization=z,return_arrays=arrays)
        return r['score']+mass_logprior(m)-.5*((g1/.1)**2+(g2/.1)**2),r
    for p0 in [np.array([11.84,-.015,-.12,6.,.3]),np.array([12.04,-.02,-.158,6.26,0.])]:
        t=time.monotonic();opt=minimize(lambda p:-evaluate(p)[0],p0,method='Nelder-Mead',options={'maxiter':600,'xatol':2e-5,'fatol':.003,
            'initial_simplex':np.vstack([p0]+[p0+np.eye(5)[i]*s for i,s in enumerate([.03,.02,.02,.3,.03])])})
        score,r=evaluate(opt.x,arrays=True);rec=dict(parameters=opt.x.tolist(),score=score,fit=serial(r),success=bool(opt.success),message=str(opt.message),seconds=time.monotonic()-t);records.append(rec);print(json.dumps(rec),flush=True)
        np.savez_compressed(out/('solution_'+str(len(records))+'.npz'),source=r['source'],model=r['model_valid'],mask=inv.mask)
    (out/'result.json').write_text(json.dumps(dict(scope='Sensitivity to free uniform external convergence. Flat kappa in[-.2,.5] is a numerical search domain, NOT measured environmental prior; mass/shear priors retained',parameter_order=['logM','g1','g2','loglambda','kappa_external'],records=records,non_claims=['Not evidence that required mass sheet exists','Not self-consistent nonlinear AQUAL external-field effect','Not a full multilevel line-of-sight model','No model comparison Bayes factor']),indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
