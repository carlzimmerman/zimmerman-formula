"""Full-potential evaluation and finite control-volume wave-current moments."""
import json,numpy as np
from scipy.special import sph_harm
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss

def harmonics(lm,x):
 d=np.maximum(np.linalg.norm(x,axis=-1),1e-10);mu=np.clip(x[:,2]/d,-1+1e-12,1-1e-12);th=np.arccos(mu);ph=np.arctan2(x[:,1],x[:,0]);l=np.array([z[0] for z in lm]);m=np.array([z[1] for z in lm]);Y=sph_harm(m[None,:],l[None,:],ph[:,None],th[:,None]);dY=m[None,:]*mu[:,None]/np.sqrt(1-mu*mu)[:,None]*Y
 for j,(ll,mm) in enumerate(lm):
  if mm<ll:dY[:,j]+=np.sqrt((ll-mm)*(ll+mm+1))*np.exp(-1j*ph)*sph_harm(mm+1,ll,ph,th)
 er=x/d[:,None];et=np.c_[mu*np.cos(ph),mu*np.sin(ph),-np.sqrt(1-mu*mu)];ep=np.c_[-np.sin(ph),np.cos(ph),np.zeros_like(ph)]
 return d,mu,Y,dY,er,et,ep
class Potential:
 def __init__(self,r,co,lm):self.r=r;self.co=co;self.lm=lm;self.mass=-co[-1,0].real*r[-1]/np.sqrt(4*np.pi)
 def evaluate(self,x,gradient=False):
  x=np.atleast_2d(x);d,mu,Y,dY,er,et,ep=harmonics(self.lm,x);i=np.clip(np.searchsorted(self.r,d)-1,0,len(self.r)-2);h=self.r[i+1]-self.r[i];f=np.clip((d-self.r[i])/h,0,1);c=(1-f[:,None])*self.co[i]+f[:,None]*self.co[i+1];val=np.real(np.sum(c*Y,axis=1));outer=d>=self.r[-1];val[outer]=-self.mass/d[outer]
  if not gradient:return val
  cr=(self.co[i+1]-self.co[i])/h[:,None];dr=np.real(np.sum(cr*Y,axis=1));dt=np.real(np.sum(c*dY,axis=1))/d;dp=np.real(np.sum(c*Y*(1j*np.array([m for l,m in self.lm])[None,:]),axis=1))/(d*np.sqrt(1-mu*mu));grad=dr[:,None]*er+dt[:,None]*et+dp[:,None]*ep;grad[outer]=self.mass*x[outer]/d[outer,None]**3
  return grad
class Tracker:
 def __init__(self,ang,r,w,eta):self.ang=ang;self.r=r;self.w=w;self.eta=eta;self.rows=[];self.coeffs=[];self.c=None
 def moments(self,v,c,refine=1):
  L=self.ang.field.L;M=self.ang.field.M;mu,wm=leggauss((2*L+2)*refine);ph=np.arange((4*M+4)*refine)*2*np.pi/((4*M+4)*refine);mm,pp=np.meshgrid(mu,ph,indexing='ij');unit=np.c_[(np.sqrt(1-mm*mm)*np.cos(pp)).ravel(),(np.sqrt(1-mm*mm)*np.sin(pp)).ravel(),mm.ravel()];aw=np.repeat(wm,len(ph))*2*np.pi/len(ph);_,mui,Y,dY,er,et,ep=harmonics(self.ang.field.lm,unit);q=v/(np.sqrt(self.w)*self.r)[:,None];psi=q@Y.T;dr=np.gradient(q,self.r,axis=0,edge_order=2)@Y.T;dt=(q@dY.T)/self.r[:,None];dp=(q@(Y*1j*np.array([m for l,m in self.ang.field.lm])[None,:]).T)/(self.r[:,None]*np.sqrt(1-mui*mui)[None,:]);vol=(self.w*self.r*self.r)[:,None]*aw[None,:];mass=abs(psi)**2*vol;xyz=self.r[:,None,None]*unit[None,:,:];current=self.eta*np.imag(psi.conj()[:,:,None]*(dr[:,:,None]*er[None,:,:]+dt[:,:,None]*et[None,:,:]+dp[:,:,None]*ep[None,:,:]))*vol[:,:,None]
  # Smoothly weighted local centroid, independently seeded by the potential well.
  cc=np.array(c).copy()
  for _ in range(30):
   dist=np.linalg.norm(xyz-cc,axis=2);win=np.clip((1.2-dist)/.4,0,1);mc=mass*win;new=np.sum(mc[:,:,None]*xyz,axis=(0,1))/np.sum(mc)
   if np.linalg.norm(new-cc)<1e-5:cc=new;break
   cc=.5*(cc+new)
  mask=np.linalg.norm(xyz-cc,axis=2)<1;mc=mass*mask;ms=float(mc.sum());cm=np.sum(mc[:,:,None]*xyz,axis=(0,1))/ms;P=np.sum(current*mask[:,:,None],axis=(0,1));J=np.sum(np.cross(xyz,current)*mask[:,:,None],axis=(0,1));Jint=J-np.cross(cm,P)
  return dict(aperture_mass_code=ms,aperture_COM_code=cm.tolist(),aperture_velocity_code=(P/ms).tolist(),aperture_P_code=P.tolist(),aperture_J_origin_code=J.tolist(),aperture_J_intrinsic_code=Jint.tolist(),global_P_code=np.sum(current,axis=(0,1)).tolist(),quadrature_mass_error=float(mass.sum()-np.sum(abs(v)**2)),quadrature_Jz_error=float(np.sum(np.cross(xyz,current)[:,:,2])-self.eta*np.sum(abs(v)**2*self.ang.m[None,:])))
 def record(self,t,v):
  pa,co,_=self.ang.potential(v);pot=Potential(self.r,co,self.ang.density.lm)
  if self.c is None:
   i,j,k=np.unravel_index(np.argmin(pa),pa.shape);mu=self.ang.field.mu[j];ph=np.pi*k/self.ang.field.nphi;self.c=self.r[i]*np.array([np.sqrt(1-mu*mu)*np.cos(ph),np.sqrt(1-mu*mu)*np.sin(ph),mu])
  opt=minimize(lambda c:pot.evaluate(c)[0],self.c,method='Nelder-Mead',options={'maxiter':600,'xatol':1e-6,'fatol':1e-10});self.c=opt.x;row=dict(t=t,well_code=self.c.tolist(),well_search_success=bool(opt.success),**self.moments(v,self.c));self.rows.append(row);self.coeffs.append(co)
  if len(self.rows)==1:self.initial_refined=self.moments(v,self.c,2)
 def save(self,path):
  np.savez_compressed(str(path)+'_tracking.npz',times=[z['t'] for z in self.rows],potential_coefficients=self.coeffs,r=self.r,lm=self.ang.density.lm)
  open(str(path)+'_tracking.json','w').write(json.dumps(dict(scope='Eulerian aperture current and COM, not tagged material or bound mass; centered at locally tracked well',history=self.rows,initial_double_angular_quadrature=self.initial_refined),indent=2)+'\n')
