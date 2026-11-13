"""Conditional SIE+host photometric control; zero convergence, independent quasar fluxes."""
import sys,json,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy import linalg,optimize
from astropy.io import fits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent;T=B.parent;ROOT=T.parents[1]
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13/image_inversion'))
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13'))
sys.path.insert(0,str(T));from inversion_continuous import Inversion
from fit_point_light import Renderer,point,physical
from lens_models import sie_deflection

class Host(Inversion):
 def __init__(self,ns=17,step=.06):
  super().__init__(inputs=T/'inputs',nsource=ns,source_pixel=step,source_center=(0,0))
  self.mask &= np.hypot(self.X+.15,self.N-.05)<3
  light=json.loads((T/'light_01/result.json').read_text())['fits'][0]
  self.startlight=np.array(light['parameters'][:6]);self.A=np.array(light['quasar_A_west_north_arcsec']);self.C=np.array(light['quasar_B_west_north_arcsec'])
  self.points=np.stack([point(self.psf,*self.A),point(self.psf,*self.C)]);self.renderer=Renderer(self.psf)
  c=json.loads((T/'inputs/results/coolest.json').read_text());m=c['lensing_entities'][0]['mass_model'][0]['parameters'];v=lambda k:m[k]['point_estimate']['value']
  self.masscenter=(v('center_x'),v('center_y'));self.seedmass=[v('theta_E'),v('q'),np.pi/2+np.deg2rad(v('phi'))];self.count=0
 def rays(self,p):
  theta,q,ang=p[4:7];cx,cy=self.masscenter
  def pure(x,y):return sie_deflection(x,y,theta,q,ang,cx,cy,0,0)
  a=np.array(pure(*self.A));b=np.array(pure(*self.C));d=self.A-self.C;v=d-(a-b);dx,dy=d;g1=(dx*v[0]-dy*v[1])/(d@d);g2=(dy*v[0]+dx*v[1])/(d@d)
  def fn(x,y):return sie_deflection(x,y,theta,q,ang,cx,cy,g1,g2)
  self.center=tuple(self.A-np.array(fn(*self.A)))
  return fn,(g1,g2)
 def run(self,p,arrays=False):
  self.count+=1;fn,g=self.rays(p);super().operator(fn)
  lp=self.startlight.copy();lp[2:6]=p[:4];lens=self.renderer.render(lp)
  D=np.column_stack([self.B,lens[self.mask],self.points[0,self.mask],self.points[1,self.mask],np.ones(self.mask.sum())]);W=D/self.noise[self.mask,None];y=self.data[self.mask]/self.noise[self.mask];n=self.ns**2;lam=np.exp(p[7]);Q=linalg.block_diag(lam*self.R,np.diag([1e-8,1e-8,1e-8,.01]));cf=linalg.cho_factor(W.T@W+Q,lower=True);coef=linalg.cho_solve(cf,W.T@y);res=y-W@coef;chi=float(res@res);pen=float(coef@Q@coef);ldh=2*np.log(np.diag(cf[0])).sum();ldq=n*p[7]+self.logdetR+3*np.log(1e-8)+np.log(.01);score=-.5*(chi+pen+ldh-ldq)
  r={'score':float(score),'chi2':chi,'prior_penalty':pen,'params':p.tolist(),'physical_light':physical(lp),'shear':list(g),'shear_magnitude':float(np.hypot(*g)),'source_center':self.center,'linear_flux_lens_A_B_sky':coef[-4:].tolist(),'negative_source_fraction':float(np.mean(coef[:n]<0)),'source_edge_abs_fraction':float(np.abs(coef[:n].reshape(self.ns,self.ns)[np.pad(np.zeros((self.ns-2,self.ns-2),bool),1,constant_values=True)]).sum()/max(np.abs(coef[:n]).sum(),1e-30)),'mask_pixels':int(self.mask.sum()),'source_grid':{'n':self.ns,'step':self.h},'source_quasar_mapping_error':float(np.linalg.norm(self.C-np.array(fn(*self.C))-self.center))}
  if arrays:r.update(source=coef[:n].reshape(self.ns,self.ns),model=(D@coef),lens=lens,coef=coef)
  return r

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);start=time.time();obj=Host();p=np.r_[obj.startlight[2:6],obj.seedmass,5.]
 bounds=[(np.log(.2),np.log(3)),(np.log(.8),np.log(9)),(.3,.95),(-np.pi,np.pi),(.5,1.2),(.35,.95),(0,2*np.pi),(-2,13)]
 p[6]%=2*np.pi;best=[None];history=[]
 def fun(v):
  r=obj.run(v)
  if best[0] is None or r['score']>best[0]['score']:best[0]=r;(out/'progress.json').write_text(json.dumps({'seconds':time.time()-start,'evaluations':obj.count,'best':r},indent=2))
  return -r['score']
 # Explicit finite derivative controls: independently shifted starts, finite bounded optimizer.
 previous=json.loads((B/'run_02/result.json').read_text())['starts'];starts=[np.array(z['params']) for z in previous]
 for z in starts:
  opt=optimize.minimize(fun,z,method='Powell',bounds=bounds,options={'maxiter':18,'maxfev':2500,'ftol':2e-5,'xtol':.001});r=obj.run(opt.x);r.update(optimizer_success=bool(opt.success),optimizer_message=str(opt.message),nit=int(opt.nit),nfev=int(opt.nfev));history.append(r);(out/'starts.json').write_text(json.dumps(history,indent=2))
 # Results are never called converged solely for having the smallest objective.
 accepted=[r for r in history if r['optimizer_success']];chosen=max(accepted or history,key=lambda r:r['score']);p=np.array(chosen['params']);r=obj.run(p,True)
 # Fixed-geometry source representation/precision checks, not new nonlinear optimum.
 checks=[]
 for ns,step in [(21,.06),(21,.045)]:
  alt=Host(ns,step);checks.append(alt.run(p))
 for dl in [-2.,2.]:
  z=p.copy();z[7]+=dl;checks.append(obj.run(z))
 np.savez_compressed(out/'reconstruction.npz',source=r['source'],model_valid=r['model'],mask=obj.mask,data=obj.data,noise=obj.noise,lens=r['lens'],coefficient=r['coef'])
 fig,ax=plt.subplots(1,4,figsize=(15,4));mod=np.zeros((100,100));mod[obj.mask]=r['model'];stretch=np.percentile(obj.data[obj.mask],99)/8
 for a,im,title in zip(ax,[np.arcsinh(obj.data/stretch),np.arcsinh(mod/stretch),np.where(obj.mask,(obj.data-mod)/obj.noise,np.nan),r['source']],['RawVIS','SIE+Sersic+2PSF+host','Residual/RMS','Gaussian hostsource']):
  a.imshow(im,origin='lower',cmap='magma' if title!='Residual/RMS' else 'RdBu_r');a.set_title(title)
 fig.tight_layout();fig.savefig(out/'host_fit.png',dpi=140)
 result={'purpose':'Conditional standardSIE extendedhost control, not theory fit','seconds':time.time()-start,'evaluations':obj.count,'chosen':chosen,'any_optimizer_converged':bool(accepted),'starts':history,'representation_and_precision_checks':checks,'non_claims':['No gravitytheory or stellarmass test','No globalconvergence proof; optimizer success reported explicitly','Fixedquasarpositions/lightcenter/masscenter; singleSersic and diagonalnoise','Gaussian source can negative; proper weakGaussian nuisance priors, no formal evidence calibrated against data covariance','Exacttwoimage association eliminates arbitraryshear; massnotinferredfromtwopoints alone']};(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
