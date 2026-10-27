"""Full existing CC Hamiltonian via canonical subflows, finite carrier retained."""
import numpy as np
from scipy.linalg import solve_banded
from central_collocated import Collocated

class Split(Collocated):
 def __init__(self,order=4,**kw):
  super().__init__(**kw);self.order=order;self.edge_sets=[np.arange(parity,self.n-1,2) for parity in (0,1)]
  self.far_edge=int(np.argmin(abs((self.wr[:-1]+self.wr[1:])/2-500/self.rm)))
 def deposit(self,z):return np.bincount(self.ids,weights=(1-self.frac)*z,minlength=len(self.wr))+np.bincount(self.ids+1,weights=self.frac*z,minlength=len(self.wr))
 def qdelta(self,old,new):return (self.g+self.g2*(old+new)/self.vol)*(new-old)
 def impulse(self,pi,extensive):
  delta=self.deposit(extensive)/self.wvol;pn=pi+delta;work=float(self.wvol@((pi+pn)/2*delta));far=float(self.wvol[self.far_edge+1:]@(((pi+pn)/2*delta)[self.far_edge+1:]));return pn,work,far
 def carrier_flow(self,a,x,p,dt):
  Z=self.Z(a);parts=list(self.vacuum_parts(a,np.zeros(len(self.wr))));parts[-1]=np.zeros(self.n);parts=tuple(parts);add=4*Z/dt**2;xm=x.copy()
  for it in range(24):
   g,hd,off,scale=self.carrier_force(xm,parts);r=g+add*(xm-x)-2*p/dt;err=float(np.max(abs(r)/(scale+add)))
   if err<2e-12:break
   ab=np.zeros((3,self.n));ab[0,1:]=off;ab[1]=hd+add;ab[2,:-1]=off;delta=solve_banded((1,1),ab,-r,check_finite=False);merit=float(np.sum(r*r/(scale+add)));rate=1.
   for ls in range(16):
    xn=xm+rate*delta;gn=self.carrier_force(xn,parts)[0]+add*(xn-x)-2*p/dt
    if np.sum(gn*gn/(scale+add))<merit+1e-30:break
    rate*=.5
   xm=xn
  pm=2*Z/dt*(xm-x);mu=self.pot(a,xm,True)[1];u=self.enclosed(abs(a[0])**2);omega=pm/Z
  mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*omega**2*self.f(u)[3]);mu[0]+=self.J*np.cos(xm)**2;mu[1]+=self.J*np.sin(xm)**2
  an=a*np.exp(-1j*dt/self.sigma*mu)
  return an,2*xm-x,2*pm-p,err,it+1
 def conversion_flow(self,a,x,p,pi,dt):
  old=abs(a[0])**2;theta=self.J*np.sin(x)*np.cos(x)*dt/self.sigma;cs=np.cos(theta);sn=np.sin(theta);an=np.array([cs*a[0]+1j*sn*a[1],cs*a[1]+1j*sn*a[0]])
  pn=p+2*self.J*np.cos(2*x)*np.real(np.conj(a[0])*a[1])*dt
  vin,work,far=self.impulse(pi,-self.qdelta(old,abs(an[0])**2))
  return an,pn,vin,work,far
 def edge_flow(self,a,chi,pi,dt,parity):
  i=self.edge_sets[parity];j=i+1;vi=self.vol[i];vj=self.vol[j];cm=self.true_chi_m(chi);d=cm[j]-cm[i];oldi=abs(a[0,i])**2;oldj=abs(a[0,j])**2
  Fi=-d*(self.g+self.g2*oldi/vi)/2;Fj=d*(self.g+self.g2*oldj/vj)/2
  z0=a[:,i].copy();z1=a[:,j].copy();z0[0]*=np.exp(-1j*Fi/self.sigma);z1[0]*=np.exp(-1j*Fj/self.sigma)
  ni=1/np.sqrt(vi);nj=-1/np.sqrt(vj);norm=ni*ni+nj*nj;phase=np.expm1(-1j*self.k*self.w[i]/2*norm*dt/self.sigma);coef=(ni*z0+nj*z1)/norm
  zn0=z0+phase*ni*coef;zn1=z1+phase*nj*coef;newi=abs(zn0[0])**2;newj=abs(zn1[0])**2
  Fin=-d*(self.g+self.g2*newi/vi)/2;Fjn=d*(self.g+self.g2*newj/vj)/2;zn0[0]*=np.exp(1j*Fin/self.sigma);zn1[0]*=np.exp(1j*Fjn/self.sigma)
  an=a.copy();an[:,i]=zn0;an[:,j]=zn1
  dqi=(self.g+self.g2*(oldi+newi)/vi)*(newi-oldi);dqj=(self.g+self.g2*(oldj+newj)/vj)*(newj-oldj)
  dC=self.g*((newj-oldj)-(newi-oldi))/2+self.g2/4*((newj+oldj)*(newj-oldj)/vj-(newi+oldi)*(newi-oldi)/vi)
  kick=np.zeros(self.n);kick[i]=-dC-dqi;kick[j]=dC-dqj;vin,work,far=self.impulse(pi,kick)
  return an,vin,work,far
 def wave_flow(self,a,chi,pi,dt):
  cn,pn,_,_=self.wave_source(chi,pi,np.zeros(self.n),dt);cm=(chi+cn)/2;vm=(pi+pn)/2;e=self.far_edge
  flux=float(-dt*self.c**2*self.ww[e]*(cm[e+1]-cm[e])*(vm[e+1]+vm[e])/2)
  an=a.copy();rho=abs(a[0])**2/self.vol;an[0]*=np.exp(1j*(self.g+2*self.g2*rho)*self.true_chi_m(cn-chi)/self.sigma)
  return an,cn,pn,flux
 def second(self,a,x,p,chi,pi,dt):
  work=bulk=conv=farwork=flux=0.;maxres=0.;iterations=0;mincap=1.
  for op,step,parity in [('A',dt/2,0),('B',dt/2,0),('C',dt/2,0),('C',dt/2,1),('D',dt,0),('C',dt/2,1),('C',dt/2,0),('B',dt/2,0),('A',dt/2,0)]:
   if op=='A':a,x,p,res,it=self.carrier_flow(a,x,p,step);maxres=max(maxres,res);iterations+=it
   elif op=='B':a,p,pi,w,fw=self.conversion_flow(a,x,p,pi,step);conv+=w;farwork+=fw
   elif op=='C':a,pi,w,fw=self.edge_flow(a,chi,pi,step,parity);bulk+=w;farwork+=fw
   else:a,chi,pi,f=self.wave_flow(a,chi,pi,step);flux+=f
   if op in ('B','C'):
    mincap=min(mincap,float(np.min(.9997-self.enclosed(abs(a[0])**2))))
    if mincap<=0:break
  return a,x,p,chi,pi,{'residual':maxres,'iterations':iterations,'cap':mincap,'bulk':bulk,'conversion':conv,'farwork':farwork,'flux':flux}
 def full_step(self,a,x,p,chi,pi,dt):
  gamma=self.gamma.copy();v0=pi.copy();pi=pi*np.exp(-gamma*dt/2);sink=float(.5*self.wvol@(v0*v0-pi*pi));qs=float(self.wvol@(v0-pi));self.gamma=np.zeros_like(gamma);infos=[]
  c=1/(2-2**(1/3));coeff=[c,1-2*c,c] if self.order==4 else [1.]
  try:
   for factor in coeff:
    a,x,p,chi,pi,info=self.second(a,x,p,chi,pi,dt*factor);infos.append(info)
    if info['residual']>1e-9 or info['cap']<=0:break
  finally:self.gamma=gamma
  v0=pi.copy();pi=pi*np.exp(-gamma*dt/2);sink+=float(.5*self.wvol@(v0*v0-pi*pi));qs+=float(self.wvol@(v0-pi));self.energy_chi=chi
  info={'integrator':'canonical Hamiltonian split, finite carrier midpoint, exact nonlinear edge flows','iterations':sum(z['iterations'] for z in infos),'fixed_point_error':max(z['residual'] for z in infos),'carrier_root_residual':max(z['residual'] for z in infos),'minimum_substep_cap_slack':min(z['cap'] for z in infos),'integrated_work':sum(z['bulk']+z['conversion'] for z in infos),'integrated_bulk_work':sum(z['bulk'] for z in infos),'integrated_conversion_work':sum(z['conversion'] for z in infos),'integrated_far_flux':sum(z['flux'] for z in infos),'integrated_far_work':sum(z['farwork'] for z in infos),'substep_failed':any(z['residual']>1e-9 or z['cap']<=0 for z in infos)}
  return a,x,p,chi,pi,sink,qs,info
