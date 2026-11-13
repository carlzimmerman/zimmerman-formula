"""Proper-prior Gaussian source inversion. Coordinates arcsec WEST/NORTH."""
from pathlib import Path
import time,json
import numpy as np
from scipy import sparse,linalg,optimize
from astropy.io import fits

class Inversion:
 def __init__(self,inputs=None,nsource=25,source_pixel=.04,source_center=(-.03,-.05),supersample=1,ridge=.01):
  t=time.time();self.inputs=Path(inputs) if inputs else Path(__file__).resolve().parents[1]/'inputs';self.ns=nsource;self.h=source_pixel;self.center=source_center;self.ss=supersample
  I=self.inputs;h=fits.open(next((I/'dataset').glob('Tile*.fits')));self.data=np.array(h['VIS_BGSUB'].data,float);self.noise=np.array(h['VIS_RMS'].data,float);psf=np.array(h['VIS_PSF'].data,float);psf/=psf.sum();self.psf=psf
  j,i=np.meshgrid(np.arange(100),np.arange(100));self.X=(j-49.5)*.1;self.N=(i-49.5)*.1
  info=json.loads((I/'dataset/info.json').read_text());mask=((-self.N-info['mask_centre'][0])**2+(self.X-info['mask_centre'][1])**2<info['mask_radius']**2)
  art=fits.getdata(I/'dataset/segmentation/artefact_binary.fits');self.mask=mask&(art==0)&(self.noise>0);self.source_mask=fits.getdata(I/'dataset/segmentation/source_binary.fits')>0
  self.lens=np.array(fits.getdata(I/'results/model.fits','VIS_GALAXY_0'),float)
  # Full finite-image convolution, zero beyond 100x100. All21x21 PSF samples retained.
  rows=[];cols=[];vals=[];ii,jj=np.indices((100,100))
  for dy in range(-10,11):
   for dx in range(-10,11):
    v=psf[dy+10,dx+10]
    if v==0:continue
    src_i=ii-dy;src_j=jj-dx;ok=(src_i>=0)&(src_i<100)&(src_j>=0)&(src_j<100)
    rows.append((ii[ok]*100+jj[ok]).ravel());cols.append((src_i[ok]*100+src_j[ok]).ravel());vals.append(np.full(ok.sum(),v))
  self.P=sparse.coo_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(10000,10000)).tocsr()
  # First differences on edges: proper ridge prevents constant-mode improper prior.
  rr=[];cc=[];vv=[];k=0
  for a in range(nsource):
   for b in range(nsource):
    for da,db in [(1,0),(0,1)]:
     if a+da<nsource and b+db<nsource:rr.extend([k,k]);cc.extend([a*nsource+b,(a+da)*nsource+b+db]);vv.extend([1.,-1.]);k+=1
  L=sparse.coo_matrix((vv,(rr,cc)),shape=(k,nsource*nsource)).tocsr();self.R=(L.T@L).toarray()+ridge*np.eye(nsource*nsource);self.logdetR=np.linalg.slogdet(self.R)[1]
  self.setup_seconds=time.time()-t
 def operator(self,deflection):
  rows=[];cols=[];vals=[];inside=np.zeros(10000);ns=self.ns
  for a in range(self.ss):
   for b in range(self.ss):
    X=self.X+((b+.5)/self.ss-.5)*.1;N=self.N+((a+.5)/self.ss-.5)*.1;ax,an=deflection(X,N);u=(X-ax-self.center[0])/self.h+(ns-1)/2;v=(N-an-self.center[1])/self.h+(ns-1)/2
    ix=np.floor(u).astype(int);iy=np.floor(v).astype(int);fu=u-ix;fv=v-iy
    full=(u>=0)&(u<=ns-1)&(v>=0)&(v<=ns-1);inside+=full.ravel()/self.ss**2
    for dx,dy,w in [(0,0,(1-fu)*(1-fv)),(1,0,fu*(1-fv)),(0,1,(1-fu)*fv),(1,1,fu*fv)]:
     xx=ix+dx;yy=iy+dy;ok=full&(xx>=0)&(xx<ns)&(yy>=0)&(yy<ns);rows.append(np.flatnonzero(ok));cols.append((yy[ok]*ns+xx[ok]));vals.append(w[ok]/self.ss**2)
  A=sparse.coo_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(10000,ns*ns)).tocsr();self.footprint=inside.reshape(100,100);self.fullB=self.P@A;B=self.fullB[self.mask.ravel()].toarray();self.B=B
  D=np.column_stack([B,self.lens[self.mask],np.ones(self.mask.sum())]);self.D=D;self.WD=D/self.noise[self.mask,None];self.y=(self.data-self.lens)[self.mask]/self.noise[self.mask];self.H0=self.WD.T@self.WD;self.b=self.WD.T@self.y;return self
 def evaluate(self,deflection=None,log_regularization=0.,return_arrays=True,posterior_uncertainty=False):
  t=time.time()
  if deflection is not None:self.operator(deflection)
  lam=np.exp(log_regularization);n=self.ns*self.ns;Q=linalg.block_diag(lam*self.R,np.diag([4.,100.]));H=self.H0+Q;cf=linalg.cho_factor(H,lower=True);coef=linalg.cho_solve(cf,self.b);res=self.y-self.WD@coef;chi=float(res@res);pen=float(coef@Q@coef);logdetH=float(2*np.log(np.diag(cf[0])).sum());logdetQ=n*log_regularization+self.logdetR+np.log(400.);norm=float(np.log(2*np.pi*self.noise[self.mask]**2).sum());loge=-.5*(chi+pen+logdetH-logdetQ+norm)
  result=dict(score=loge,log_evidence=loge,chi2=chi,prior_penalty=pen,log_regularization=float(log_regularization),n_pixels=int(self.mask.sum()),n_source=n,lens_amplitude=float(1+coef[-2]),sky=float(coef[-1]),negative_source_fraction=float(np.mean(coef[:n]<0)),source_footprint_fraction=float(np.mean(self.footprint[self.mask])),seconds=time.time()-t)
  if return_arrays:result.update(source=coef[:n].reshape(self.ns,self.ns),model_valid=self.D@coef+self.lens[self.mask],coefficient=coef)
  if posterior_uncertainty:result["source_std"]=np.sqrt(np.diag(linalg.cho_solve(cf,np.eye(n+2)))[:n]).reshape(self.ns,self.ns)
  return result
 def optimize_regularization(self,deflection=None,bounds=(-5,18)):
  if deflection is not None:self.operator(deflection)
  opt=optimize.minimize_scalar(lambda z:-self.evaluate(log_regularization=z,return_arrays=False)['score'],bounds=bounds,method='bounded',options={'xatol':.05});return self.evaluate(log_regularization=opt.x)

def setup(**kwargs):return Inversion(**kwargs)
