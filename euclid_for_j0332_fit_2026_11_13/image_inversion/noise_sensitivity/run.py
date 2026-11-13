from pathlib import Path
import sys,json,time,hashlib,os
import numpy as np
from scipy.optimize import minimize
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(BASE/'image_inversion'),str(BASE)]
from inversion import Inversion
from lens_models import AqualLens,sie_parameters,sie_deflection
from fit_images import mass_logprior
class Correlated(Inversion):
 def __init__(self,r=.23,scale=1.,**kw):
  super().__init__(**kw);self.r=r;self.scale=scale;self.originalmask=self.mask.copy()
 def operator(self,fn):
  self.mask=self.originalmask.copy();super().operator(fn);r=self.r
  m=self.originalmask;valid=m.copy();valid[0,:]=False;valid[:,0]=False;valid[1:,1:]&=m[:-1,1:]&m[1:,:-1]&m[:-1,:-1];self.mask=valid
  D=np.column_stack([self.fullB.toarray(),self.lens.ravel(),np.ones(10000)]).reshape(100,100,-1)
  def whiten(a):return (a[1:,1:]-r*a[:-1,1:]-r*a[1:,:-1]+r*r*a[:-1,:-1])/((1-r*r)*self.scale)
  stdD=D/self.noise[:,:,None];stdy=(self.data-self.lens)/self.noise
  self.D=D[valid];self.WD=whiten(stdD)[valid[1:,1:]];self.y=whiten(stdy)[valid[1:,1:]];self.H0=self.WD.T@self.WD;self.b=self.WD.T@self.y
  return self
 def evaluate(self,*a,**kw):
  ret=super().evaluate(*a,**kw);corr=-ret['n_pixels']*np.log((1-self.r*self.r)*self.scale);ret['score']+=corr;ret['log_evidence']+=corr;return ret

def serial(r):return {k:v for k,v in r.items() if not isinstance(v,np.ndarray)}
def main():
 files=[BASE/'image_inversion/inversion.py',BASE/'lens_models.py',BASE/'image_fit_01/result.json'];hashes=lambda:{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 before=hashes();root=json.loads(files[-1].read_text());lens=AqualLens();sp=sie_parameters();p0=np.array(root['solutions'][-1]['parameters']);allresults=[]
 for scale in [1.,.674]:
  inv=Correlated(r=.23,scale=scale,supersample=2);baseline=inv.optimize_regularization(lambda X,N:sie_deflection(X,N,**sp));print('baseline',scale,serial(baseline),flush=True)
  start=time.time();trace=[]
  def evaluate(p):
   m,g1,g2,z=p
   if not valid_parameters(m,g1,g2,z):return -1e30,None
   fit=inv.evaluate(deflection=lambda X,N:lens.deflection(X,N,m,g1,g2),log_regularization=z,return_arrays=False);score=fit['score']-.5*((g1/.1)**2+(g2/.1)**2)+mass_logprior(m);return score,fit
  def obj(p):
   s,r=evaluate(p);trace.append({'p':list(p),'score':s});return -s
  opt=minimize(obj,p0,method='Nelder-Mead',options={'maxiter':300,'xatol':1e-5,'fatol':.003,'initial_simplex':np.vstack([p0,p0+[.008,0,0,0],p0+[0,.008,0,0],p0+[0,0,.008,0],p0+[0,0,0,.3]])});s,fit=evaluate(opt.x);rec=dict(scale=scale,correlation=.23,baseline=serial(baseline),optimized_parameters=opt.x.tolist(),posterior_objective=s,fit=serial(fit),delta_conditional_log_evidence=fit['score']-baseline['score'],delta_chi2=fit['chi2']-baseline['chi2'],success=bool(opt.success),seconds=time.time()-start)
  allresults.append(rec);print('RESULT',rec,flush=True);(OUT/'progress.json').write_text(json.dumps(allresults,indent=2));(OUT/f'trace_scale{scale}.json').write_text(json.dumps(trace))
 # diagonal-model best AQUAL counterimage holdout, identically defined to baseline benchmark
 inv=Inversion(supersample=2);hold=inv.mask&inv.source_mask&(inv.N<-.4)&(inv.X<0);inv.mask&=~hold;m,g1,g2,z=p0;fit=inv.optimize_regularization(lambda X,N:lens.deflection(X,N,m,g1,g2));pred=(inv.fullB@fit['source'].ravel()).reshape(100,100)+fit['lens_amplitude']*inv.lens+fit['sky'];v=((inv.data-pred)/inv.noise)[hold];cv=dict(parameters=p0.tolist(),heldout_pixels=int(hold.sum()),heldout_chi2=float(v@v),mean=float(v.mean()),std=float(v.std()),fit=serial(fit));(OUT/'aqual_counterimage_holdout.json').write_text(json.dumps(cv,indent=2))
 (OUT/'provenance.json').write_text(json.dumps(dict(before=before,after=hashes()),indent=2));(OUT/'result.json').write_text(json.dumps(allresults,indent=2))
def valid_parameters(m,g1,g2,z):return 11.56<m<12.39 and max(abs(g1),abs(g2))<.3 and -5<z<18
if __name__=='__main__':main()
