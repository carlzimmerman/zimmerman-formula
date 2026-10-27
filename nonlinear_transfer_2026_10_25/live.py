"""Free complex T/F matter and reciprocal waves; adiabatic free carrier.

The carrier is independently minimized, not locked to a material angle or a
translated profile. Its finite inertia is explicitly omitted in this limit.
All material cells, common and relative phases, and densities evolve.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg.lapack import dgttrf,dgttrs,zgttrf,zgttrs
from scipy.linalg import solve_banded
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from free_formation import FreeVacuum

class Live:
 def __init__(self,wave_h_kpc=2.,wave_R_kpc=8000.,coupling=True):
  m=self.m=FreeVacuum();self.n=m.n;self.r=m.r.numpy();self.vol=m.vol.numpy();self.rm=m.rm;self.M=5.364;self.J=30.;self.K=m.K;self.eps=m.eps;self.B=m.volume_cost;self.beta=m.beta*.95;self.ell2=m.ell2;self.k=(m.material_length/m.rm)**2;self.sigma=np.sqrt(self.k);self.vac=(m.vacuum_length/m.rm)**2
  self.w=m.rf.numpy()**2/m.dr.numpy();self.gb=self.r/(self.r**2+m.b**2)**1.5;self.tt=m.tt.numpy();self.tw=m.tw.numpy();self.R=m.R;self.b=m.b
  edges=[0.]
  for r in self.r:edges.append(2*r-edges[-1])
  self.edges=np.array(edges);kpc=3.085677581491367e19;v=np.sqrt(9.3603e-11*m.rm*kpc);self.tdyn=m.rm*kpc/v/(365.25*86400*1e6);self.c=299792458/v
  si=json.loads(Path('selective_stress_2026_10_25/run_spinor_inertia/results.json').read_text());halo=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());self.g=(np.sqrt(si['cases'][0]['conversion_potential_Eunit']/.25)*3*(halo['scaled_boundary_kpc']/m.rm)**1.5/si['converted_mass_Mb']) if coupling else 0.
  # Exact positive complex-gradient discretization. Unlike the older real
  # angle arithmetic-mean formula, its unitary dynamics is defined directly.
  kd=.5*self.k*np.r_[self.w[0],self.w[:-1]+self.w[1:],self.w[-1]]/self.vol;ko=-.5*self.k*self.w/np.sqrt(self.vol[1:]*self.vol[:-1]);self.kd=kd;self.ko=ko
  ed=np.arange(0,wave_R_kpc+wave_h_kpc*.1,wave_h_kpc)/m.rm;self.wr=(ed[1:]+ed[:-1])/2;self.wvol=np.diff(ed**3)/3;self.ww=((self.wr[1:]+self.wr[:-1])/2)**2/np.diff(self.wr);self.wdiag=np.r_[self.ww[0],self.ww[:-1]+self.ww[1:],self.ww[-1]];self.gamma=(.8*self.c/(1000/m.rm))*np.maximum((self.wr-6000/m.rm)/(2000/m.rm),0)**2
  ids=np.clip(np.searchsorted(self.wr,self.r)-1,0,len(self.wr)-2);frac=np.clip((self.r-self.wr[ids])/(self.wr[ids+1]-self.wr[ids]),0,1);self.ids=ids;self.frac=frac;self.kcache={};self.wcache={};self.alpha_iterations=0
 def enclosed(self,m):return (np.cumsum(m)-.5*m)/self.r**2
 def transpose(self,x):
  a=x/self.r**2;return np.cumsum(a[::-1])[::-1]-.5*a
 def f(self,u):
  # The old stable continuation is not a physical cap enforcement.
  v=np.minimum(u,.98);d=u-v
  W=-np.log1p(-v)-v+d*.98/.02+.5*d*d/.02**2
  F=v*v/(1-v)+d*.98*1.02/.02**2+d*d/.02**3
  Wp=v/(1-v)+d/.02**2;Fp=v*(2-v)/(1-v)**2+2*d/.02**3
  return W,F,Wp,Fp
 def chi_m(self,chi):return (1-self.frac)*chi[self.ids]+self.frac*chi[self.ids+1]
 def alignment(self,a,alpha,chi):
  phase=np.exp(-1j*self.g*self.chi_m(chi)/self.sigma);c=np.cos(alpha);s=np.sin(alpha);b0=c*c*a[0]-s*c*phase*a[1];b1=s*s*a[1]-s*c*np.conj(phase)*a[0]
  return np.array([b0,b1])
 def vacuum_parts(self,a,chi):
  mt=abs(a[0])**2;mf=abs(a[1])**2;u=self.enclosed(mt);F=self.f(u)[1];fc=self.f((u[1:]+u[:-1])/2)[1];coeff=(2/np.pi)**2*self.w*(self.ell2*fc+self.vac);cross=np.real(np.exp(1j*self.g*self.chi_m(chi)/self.sigma)*np.conj(a[1])*a[0]);return mt,mf,F,coeff,cross
 def alpha_energy(self,x,parts):
  mt,mf,F,d,cross=parts;return float(sum(self.beta*self.vol*F*np.sin(2*x)**2/np.pi**2+self.B*self.vol*np.sin(x)**2+self.J*(mt*np.cos(x)**2+mf*np.sin(x)**2-cross*np.sin(2*x)))+.5*(d@np.diff(x)**2))
 def minimize_alpha(self,a,chi,x,maxit=30):
  x=x.copy();parts=self.vacuum_parts(a,chi);mt,mf,F,d,cross=parts;diag=np.r_[d[0],d[:-1]+d[1:],d[-1]]
  for it in range(maxit):
   grad=2*self.beta*self.vol*F*np.sin(4*x)/np.pi**2+self.B*self.vol*np.sin(2*x)+self.J*((mf-mt)*np.sin(2*x)-2*cross*np.cos(2*x));dx=np.diff(x);grad[:-1]-=d*dx;grad[1:]+=d*dx
   hh=8*self.beta*self.vol*F*np.cos(4*x)/np.pi**2+2*self.B*self.vol*np.cos(2*x)+2*self.J*((mf-mt)*np.cos(2*x)+2*cross*np.sin(2*x))+diag
   active=((x<=1e-12)&(grad>=0))|((x>=np.pi/2-1e-12)&(grad<=0));pg=grad.copy();pg[active]=0;scale=1e-15+diag+2*self.J*(mt+mf)+2*self.B*self.vol+8*self.beta*self.vol*F/np.pi**2;res=max(abs(pg)/scale)
   if res<2e-10:break
   off=-d.copy();off[active[:-1]|active[1:]]=0;hd=hh.copy();hd[active]=1;shift=max(0,float(max(np.r_[abs(off[0]),abs(off[:-1])+abs(off[1:]),abs(off[-1])]-hd)))+1e-14;hd[~active]+=shift
   ab=np.zeros((3,self.n));ab[0,1:]=off;ab[1]=hd;ab[2,:-1]=off;step=solve_banded((1,1),ab,-pg,check_finite=False);E=self.alpha_energy(x,parts);rate=1.
   for ls in range(25):
    xn=np.clip(x+rate*step,0,np.pi/2)
    if self.alpha_energy(xn,parts)<=E+1e-14:break
    rate*=.5
   x=xn
  self.alpha_iterations+=it+1
  return x,float(res),it+1
 def pot(self,a,alpha,grad=False):
  mt=abs(a[0])**2;mf=abs(a[1])**2;mass=mt+mf;u=self.enclosed(mt);gd=self.enclosed(mass);W,F,Wp,Fp=self.f(u);qv=np.sin(alpha)**2;s=np.sin(2*alpha)**2/np.pi**2;uf=(u[1:]+u[:-1])/2;_,ff,_,fp=self.f(uf);x=2*alpha/np.pi;dx=np.diff(x);Mt=sum(mt);M=sum(mass);wt,_,wpt,_=self.f(Mt*self.tt**2)
  E=sum(self.vol*(W+self.beta*s*F)) +sum(self.tw*wt/self.tt**4)+.5*sum(self.w*(self.ell2*ff+self.vac)*dx*dx)+self.B*(self.vol@qv)-self.eps*Mt+1.5*self.K*sum(self.vol*(mf/self.vol)**(5/3))-sum(self.vol*(.5*gd*gd+self.gb*gd))-.5*M*M/self.R-M/np.sqrt(self.R*self.R+self.b*self.b)
  if not grad:return float(E)
  response=self.vol*(Wp+self.beta*s*Fp);face=.25*self.ell2*self.w*fp*dx*dx;response[:-1]+=face;response[1:]+=face;muR=self.transpose(response)+sum(self.tw*wpt/self.tt**2);muG=-self.transpose(self.vol*(gd+self.gb))-M/self.R-1/np.sqrt(self.R*self.R+self.b*self.b)
  return float(E),np.array([muG+muR-self.eps,muG+2.5*self.K*(mf/self.vol)**(2/3)])
 def kinetic(self,a):return np.sum(self.kd*(abs(a[0])**2+abs(a[1])**2))+2*np.real(np.sum(self.ko*(np.conj(a[0,:-1])*a[0,1:]+np.conj(a[1,:-1])*a[1,1:])))
 def energy(self,a,alpha,chi,pi):
  return self.pot(a,alpha)+float(self.kinetic(a))+self.J*float(np.real(np.sum(np.conj(a)*self.alignment(a,alpha,chi))))+.5*(self.wvol@(pi*pi)+self.c**2*(self.ww@np.diff(chi)**2))
 def kstep(self,a,dt):
  if dt not in self.kcache:
   fac=1j*dt/(2*self.sigma);lu=zgttrf((fac*self.ko).astype(complex),1+fac*self.kd,(fac*self.ko).astype(complex));assert lu[-1]==0;self.kcache[dt]=lu
  fac=1j*dt/(2*self.sigma);rhs=(1-fac*self.kd)*a;rhs[:,:-1]-=fac*self.ko*a[:,1:];rhs[:,1:]-=fac*self.ko*a[:,:-1];out,info=zgttrs(*self.kcache[dt][:-1],np.asfortranarray(rhs.T));assert info==0;return out.T
 def wstep(self,chi,pi,dt):
  if dt not in self.wcache:
   lo=-dt*dt*self.c*self.c/4*self.ww/self.wvol[1:];hi=-dt*dt*self.c*self.c/4*self.ww/self.wvol[:-1];dg=1+dt*dt*self.c*self.c/4*self.wdiag/self.wvol+dt*self.gamma/2;lu=dgttrf(lo.copy(),dg.copy(),hi.copy());assert lu[-1]==0;self.wcache[dt]=lu
  lap=-self.wdiag*chi;lap[:-1]+=self.ww*chi[1:];lap[1:]+=self.ww*chi[:-1];rhs=pi+dt*self.c*self.c/2*lap/self.wvol;v,info=dgttrs(*self.wcache[dt][:-1],np.asfortranarray(rhs[:,None]));assert info==0;v=v[:,0];sink=dt*(self.wvol@(self.gamma*v*v));charge=dt*(self.wvol@(self.gamma*v));return chi+dt*v,2*v-pi,float(sink),float(charge)
 def fixed_step(self,a,alpha,chi,pi,dt):
  chi,pi,sink,charge=self.wstep(chi,pi,dt/2);a=self.kstep(a,dt/2);mu=self.pot(a,alpha,True)[1];a=a*np.exp(-1j*dt/(2*self.sigma)*mu)
  old=abs(a[0])**2;a=a+(np.exp(-1j*self.J*dt/self.sigma)-1)*self.alignment(a,alpha,chi);delta=abs(a[0])**2-old;weights=np.bincount(self.ids,weights=(1-self.frac)*delta,minlength=len(pi))+np.bincount(self.ids+1,weights=self.frac*delta,minlength=len(pi));pi=pi-self.g*weights/self.wvol
  mu=self.pot(a,alpha,True)[1];a=a*np.exp(-1j*dt/(2*self.sigma)*mu);a=self.kstep(a,dt/2);chi,pi,ds,dc=self.wstep(chi,pi,dt/2);return a,chi,pi,sink+ds,charge+dc
 def step(self,a,x,chi,pi,dt):
  # Midpoint carrier avoids first-order energy removal by endpoint relaxation.
  ah,ch,ph,_,_=self.fixed_step(a,x,chi,pi,dt/2);xm,res,_=self.minimize_alpha(ah,ch,x);a1,c1,p1,sink,charge=self.fixed_step(a,xm,chi,pi,dt);x1,res1,_=self.minimize_alpha(a1,c1,xm);return a1,x1,c1,p1,sink,charge,max(res,res1)
 def diagnostics(self,a,x,chi,pi):
  mt=abs(a[0])**2;mf=abs(a[1])**2;mass=mt+mf;rho=mass/self.vol;q=mt/np.maximum(mass,1e-300);rr=self.r*self.rm;gt=self.gb+self.enclosed(mass);law=(self.gb+np.sqrt(self.gb**2+4*self.gb))/2;err=np.log10(gt/law);sel=(rr>=1.5)&(rr<=50);error=(10**max(max(abs(err[sel])),max(abs(np.interp([1.5,50],rr,err))))-1)*100;cross=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0];rads=[float(rr[i]+(.5-q[i])*(rr[i+1]-rr[i])/(q[i+1]-q[i])) for i in cross];R=rads[-1] if rads else None
  d={'mass':float(sum(mass)),'T_mass':float(sum(mt)),'law_error_percent':float(error),'boundary_kpc':R,'crossings':len(rads),'cap_slack':float(min(.9997-self.enclosed(mt))),'wave_energy':float(.5*(self.wvol@(pi*pi)+self.c**2*(self.ww@np.diff(chi)**2))),'kinetic_energy':float(self.kinetic(a))}
  if R is not None:
   near=(rr>15)&(rr<1.2*R);out=rr>1.2*R;den=rho[near];d.update(density_rebound=float(max(den/np.minimum.accumulate(den))) if len(den) else None,outer_T_fraction=float(sum(mt[out])/sum(mass[out])),outer_mass=float(sum(mass[out])),transition_min_density=float(min(rho[(q>.01)&(q<.99)])) if np.any((q>.01)&(q<.99)) else None)
  return d
