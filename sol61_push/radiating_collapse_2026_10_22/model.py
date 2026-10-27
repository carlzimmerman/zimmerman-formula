import numpy as np
from scipy.optimize import minimize
from scipy.stats import maxwell

class Model:
 def __init__(self,n=256,ns=128,L=16.,lam=1.,gap=.5,c=1.,spin=0.,mass_ratio=1.,sponge_start=10.):
  self.n=n;self.ns=ns;self.L=L;self.dx=L/n;self.soft=self.dx;self.rc=(np.arange(n)+.5)*self.dx;self.rf=np.arange(n+1)*self.dx
  self.vol=np.diff(self.rf**3)/3;self.dual=self.rf[1:-1]**2*self.dx
  self.eps=.005;self.a=1/(2*lam);self.b=self.a/gap**2;self.d=self.b*c*c
  self.sg=2*np.maximum(0,(self.rc-sponge_start)/(L-sponge_start))**2
  self.sgp=2*np.maximum(0,(self.rf[1:-1]-sponge_start)/(L-sponge_start))**2
  mass=.08408132497418408*mass_ratio;self.mi=np.full(ns,mass/ns)
  self.r0=.6*mass_ratio**(1/3)*maxwell.ppf((np.arange(ns)+.5)/ns)
  self.li=np.zeros(ns);ug=self.gravity(self.r0)[0];I=2/3*np.sum(self.mi*(self.r0**2+self.soft**2));omega=np.sqrt(2*spin*abs(ug)/I)
  self.li=2/3*self.mi*omega*(self.r0**2+self.soft**2)
 def dep(self,r):
  ar=np.abs(r);x=ar/self.dx-.5;j=np.floor(x+.5).astype(int);ids=j[:,None]+np.array([-1,0,1]);dist=x[:,None]-ids;ad=abs(dist)
  w=np.where(ad<.5,.75-dist**2,.5*(1.5-ad)**2)
  dw=np.where(ad<.5,-2*dist,-(1.5-ad)*np.sign(dist))*np.sign(r[:,None])/self.dx
  ids=np.where(ids<0,-ids-1,ids)
  if ids.max()>=self.n:raise ValueError('material reached grid edge')
  rho=np.bincount(ids.ravel(),weights=(self.mi[:,None]*w).ravel(),minlength=self.n)/self.vol
  return rho,ids,w,dw
 def gravity(self,r):
  ar=abs(r);ix=np.argsort(ar);m=self.mi[ix];rr=ar[ix];s=np.sqrt(rr**2+self.soft**2);prefix=np.cumsum(m)-m
  U=-np.sum(m*(prefix+.5*m)/s)
  force=np.empty(len(r));force[ix]=-(prefix+.5*m)*rr/s**3;force*=np.sign(r)
  phi=np.empty(len(r));phi[ix]=-(prefix+m)/s-(np.cumsum((m/s)[::-1])[::-1]-m/s)
  return U,force,phi
 def fields(self,r,w,z):
  rho,ids,weights,dw=self.dep(r);wf=np.r_[0.,w,0.];div=np.diff(self.rf**2*wf)/self.vol;e=rho-div;h=e/z
  return e,h,ids,weights,dw
 def potential(self,r,w,z,grad=False):
  if np.max(abs(w))>=1 or np.min(z)<=0:raise ValueError('field outside positive-energy domain')
  e,h,ids,weights,dw=self.fields(r,w,z);ug,fg,phi=self.gravity(r)
  dz=np.diff(z)/self.dx
  # Outer face pinned z=1 over half-cell; reflecting inner face.
  E=ug+np.sum(3*self.li**2/(4*self.mi*(r*r+self.soft**2)))+np.sum(self.dual*(-abs(w)-np.log1p(-abs(w))))+np.sum(self.vol*(.5*e*e/z+.5*self.a*(z-1)**2))+.5*self.d*np.sum(self.rf[1:-1]**2*self.dx*dz*dz)+self.d*self.rf[-1]**2*(z[-1]-1)**2/self.dx
  if not grad:return E
  gradw=self.dual*w/(1-abs(w))+self.rf[1:-1]**2*np.diff(h)
  flux=self.rf[1:-1]**2*dz
  gradz=self.vol*(-.5*h*h+self.a*(z-1))-self.d*np.diff(np.r_[0.,flux,2*self.rf[-1]**2*(1-z[-1])/self.dx])
  gradr=-self.mi*fg-3*self.li**2*r/(2*self.mi*(r*r+self.soft**2)**2)+self.mi*np.sum(h[ids]*dw,axis=1)
  return E,(gradr,gradw,gradz)
 def static(self,r):
  # Scale variables by volume square roots to avoid the radial volume condition number.
  sw=np.sqrt(self.dual);sz=np.sqrt(self.vol)
  def obj(Y):
   w=Y[:self.n-1]/sw;z=1+Y[self.n-1:]/sz
   E,(_,gw,gz)=self.potential(r,w,z,True)
   return E,np.r_[gw/sw,gz/sz]
  Y=np.zeros(2*self.n-1)
  bounds=list(zip(-.95*sw,.95*sw))+list(zip(-.9*sz,9*sz))
  opt=minimize(obj,Y,jac=True,method='L-BFGS-B',bounds=bounds,options={'maxiter':8000,'ftol':1e-14,'gtol':1e-9,'maxls':40,'maxcor':20})
  return opt.x[:self.n-1]/sw,1+opt.x[self.n-1:]/sz,dict(success=bool(opt.success),message=str(opt.message),gradient_max=float(max(abs(opt.jac))),iterations=int(opt.nit))
 def accel(self,r,w,z):
  E,(gr,gw,gz)=self.potential(r,w,z,True)
  return -gr/self.mi,-gw/(self.eps*self.dual),-gz/(self.b*self.vol)
 def energy(self,r,v,w,wp,z,zp):
  return self.potential(r,w,z)+.5*np.sum(self.mi*v*v)+.5*self.eps*np.sum(self.dual*wp*wp)+.5*self.b*np.sum(self.vol*zp*zp)
 def damp(self,wp,zp,dt):
  kinetic=.5*self.eps*np.sum(self.dual*wp*wp)+.5*self.b*np.sum(self.vol*zp*zp)
  wp=wp*np.exp(-self.sgp*dt);zp=zp*np.exp(-self.sg*dt)
  after=.5*self.eps*np.sum(self.dual*wp*wp)+.5*self.b*np.sum(self.vol*zp*zp)
  return wp,zp,kinetic-after

def evolve(model,dt=.001,end=30.,sample=.1):
 r=model.r0.copy();v=np.zeros(model.ns);w,z,stat=model.static(r);wp=np.zeros_like(w);zp=np.zeros_like(z);E0=model.energy(r,v,w,wp,z,zp);removed=0.;rows=[];ar,aw,az=model.accel(r,w,z);maxerr=0.
 for step in range(round(end/dt)+1):
  if step%max(1,round(sample/dt))==0:
   ee=model.energy(r,v,w,wp,z,zp);maxerr=max(maxerr,abs(ee+removed-E0)/max(abs(E0),1e-12));phi=model.gravity(r)[2]
   spec=.5*v*v+3*model.li**2/(4*model.mi**2*(r*r+model.soft**2))+phi
   rows.append(dict(time=step*dt,energy=ee,removed=removed,balance_error=ee+removed-E0,masses=[float(np.sum(model.mi[abs(r)<cut])) for cut in [.5,1.,1.5,2.,3.,4.]],candidate_ejecta=float(np.sum(model.mi[(abs(r)>4)&(r*v>0)&(spec>0)])),max_r=float(max(abs(r))),min_z=float(min(z)),max_z=float(max(z)),max_w=float(max(abs(w)))))
  if step==round(end/dt):break
  wp,zp,lost=model.damp(wp,zp,dt/2);removed+=lost
  v+=dt/2*ar;wp+=dt/2*aw;zp+=dt/2*az
  r+=dt*v;w+=dt*wp;z+=dt*zp
  ar,aw,az=model.accel(r,w,z)
  v+=dt/2*ar;wp+=dt/2*aw;zp+=dt/2*az
  wp,zp,lost=model.damp(wp,zp,dt/2);removed+=lost
 return dict(static=stat,initial_energy=E0,mass=float(sum(model.mi)),max_relative_energy_error=maxerr,rows=rows,final_r=r.tolist(),final_v=v.tolist(),shell_mass=model.mi.tolist(),final_w=w.tolist(),final_z=z.tolist(),grid_r=model.rc.tolist(),phase=dict(a=model.a,b=model.b,d=model.d),dt=dt)
