"""Does a hypothetical mass sheet allow the catalogue median stellar mass?"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE/'image_inversion'))
from inversion_continuous import setup
from lens_models import AqualLens
from fit_images_v2 import serial

def main(out):
 out=Path(out);out.mkdir(exist_ok=True,parents=True);inv=setup(nsource=25,source_pixel=.04,supersample=2);lens=AqualLens();mass=11.8310873126
 def evaluate(p,arrays=False):
  g1,g2,z,k=p
  if max(abs(g1),abs(g2))>.3 or not -5<z<18 or not -.2<k<.5:return -1e30,None
  r=inv.evaluate(deflection=lambda X,N:lens.deflection(X,N,mass,g1,g2,kappa_external=k),log_regularization=z,return_arrays=arrays)
  return r['score']-.5*((g1/.1)**2+(g2/.1)**2),r
 p0=np.array([-.015,-.10,6.5,.30]);opt=minimize(lambda p:-evaluate(p)[0],p0,method='Nelder-Mead',options={'maxiter':600,'xatol':2e-5,'fatol':.003,'initial_simplex':np.vstack([p0]+[p0+np.eye(4)[i]*s for i,s in enumerate([.02,.02,.3,.03])])})
 score,r=evaluate(opt.x,True);result=dict(fixed_logM=mass,parameters=opt.x.tolist(),parameter_order=['g1','g2','loglambda','kappa_external'],score=score,fit=serial(r),success=bool(opt.success),non_claims=['Hypothetical convergence, no environmental measurement','Not full AQUAL external-field solution','Not posterior model comparison'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(out/'fit.npz',source=r['source'],model_valid=r['model_valid'],mask=inv.mask,data=inv.data,noise=inv.noise);print(json.dumps(result))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
