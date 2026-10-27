"""Finite-carrier canonical Hamiltonian: implicit coupled midpoint evolution.

No density manifold, locked angle, carrier relaxation or physical damping is
used in time evolution. Positive scalar absorption is confined to far radii.
"""
import numpy as np
from scipy.linalg import solve_banded
from scipy.linalg.lapack import dgttrf,dgttrs
from live import Live

class Full(Live):
 def Z(self,a):
  u=self.enclosed(abs(a[0])**2);return (2/np.pi)**2*self.vol*(self.ell2*self.f(u)[1]+self.vac)/self.c**2
 def carrier_force(self,x,parts):
  mt,mf,F,d,cross=parts
  grad=2*self.beta*self.vol*F*np.sin(4*x)/np.pi**2+self.B*self.vol*np.sin(2*x)+self.J*((mf-mt)*np.sin(2*x)-2*cross*np.cos(2*x));dx=np.diff(x);grad[:-1]-=d*dx;grad[1:]+=d*dx
  diag=np.r_[d[0],d[:-1]+d[1:],d[-1]];hh=8*self.beta*self.vol*F*np.cos(4*x)/np.pi**2+2*self.B*self.vol*np.cos(2*x)+2*self.J*((mf-mt)*np.cos(2*x)+2*cross*np.sin(2*x))+diag
  scale=1e-18+diag+2*self.J*(mt+mf)+2*self.B*self.vol+8*self.beta*self.vol*F/np.pi**2
  return grad,hh,-d,scale
 def carrier_mid(self,a,chi,x0,p0,dt,guess):
  Z=self.Z(a);parts=self.vacuum_parts(a,chi);x=guess.copy();add=4*Z/dt**2
  for it in range(35):
   gg,hh,off,scale=self.carrier_force(x,parts);g=gg+add*(x-x0)-2*p0/dt;hd=hh+add;res=max(abs(g)/(scale+add))
   if res<1e-12:break
   ab=np.zeros((3,self.n));ab[0,1:]=off;ab[1]=hd;ab[2,:-1]=off
   try:d=solve_banded((1,1),ab,-g,check_finite=False)
   except np.linalg.LinAlgError:break
   merit=np.sum(g*g/(scale+add));rate=1.
   for k in range(20):
    xx=x+rate*d;ng=self.carrier_force(xx,parts)[0]+add*(xx-x0)-2*p0/dt
    if np.sum(ng*ng/(scale+add))<=merit+1e-30:break
    rate*=.5
   x=xx
  pmid=2*Z/dt*(x-x0)
  return x,pmid,float(res)
 def material_cn(self,a0,mu,x,chi,dt):
  fac=1j*dt/(2*self.sigma);diag=(self.kd+mu).T.copy();diag[:,0]+=self.J*np.cos(x)**2;diag[:,1]+=self.J*np.sin(x)**2;diag=diag.ravel();local=-self.J*np.sin(x)*np.cos(x)*np.exp(-1j*self.g*self.chi_m(chi)/self.sigma);ab=np.zeros((5,2*self.n),complex);ab[2]=1+fac*diag;ab[1,1::2]=fac*local;ab[3,::2]=fac*np.conj(local);ab[0,2:]=fac*np.repeat(self.ko,2);ab[4,:-2]=fac*np.repeat(self.ko,2)
  Ha=(self.kd+mu)*a0+self.J*self.alignment(a0,x,chi);Ha[:,:-1]+=self.ko*a0[:,1:];Ha[:,1:]+=self.ko*a0[:,:-1];rhs=(a0-fac*Ha).T.ravel();ans=solve_banded((2,2),ab,rhs,check_finite=False);return ans.reshape(self.n,2).T
 def wave_source(self,chi0,pi0,rate,dt):
  if dt not in self.wcache:
   lo=-dt*dt*self.c*self.c/4*self.ww/self.wvol[1:];hi=-dt*dt*self.c*self.c/4*self.ww/self.wvol[:-1];dg=1+dt*dt*self.c*self.c/4*self.wdiag/self.wvol+dt*self.gamma/2;lu=dgttrf(lo.copy(),dg.copy(),hi.copy());assert lu[-1]==0;self.wcache[dt]=lu
  dep=np.bincount(self.ids,weights=(1-self.frac)*rate,minlength=len(pi0))+np.bincount(self.ids+1,weights=self.frac*rate,minlength=len(pi0));lap=-self.wdiag*chi0;lap[:-1]+=self.ww*chi0[1:];lap[1:]+=self.ww*chi0[:-1];rhs=pi0+dt*self.c**2/2*lap/self.wvol-dt*self.g/2*dep/self.wvol;v,info=dgttrs(*self.wcache[dt][:-1],np.asfortranarray(rhs[:,None]));assert info==0;v=v[:,0]
  return chi0+dt*v,2*v-pi0,float(dt*(self.wvol@(self.gamma*v*v))),float(dt*(self.wvol@(self.gamma*v)))
 def full_energy(self,a,x,p,chi,pi):return self.energy(a,x,chi,pi)+float(.5*sum(p*p/self.Z(a)))
 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  a1=a0.copy();chi1=chi0.copy();xm=x0.copy();maxres=0.;err=np.inf
  for it in range(45):
   amid=(a0+a1)/2;cmid=(chi0+chi1)/2;xm,pm,res=self.carrier_mid(amid,cmid,x0,p0,dt,xm);maxres=max(maxres,res);mu=self.pot(amid,xm,True)[1];u=self.enclosed(abs(amid[0])**2);angular_rate=pm/self.Z(amid);mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*angular_rate**2*self.f(u)[3]);an=self.material_cn(a0,mu,xm,cmid,dt);am=(a0+an)/2;align=self.alignment(am,xm,cmid);rate=2*self.J/self.sigma*np.imag(np.conj(am[0])*align[0]);cn,pn,sink,qs=self.wave_source(chi0,pi0,rate,dt)
   err=max(float(max(abs(an-a1).ravel())),float(max(abs(cn-chi1)))*max(self.g,1)/self.sigma)
   a1=an;chi1=cn
   if err<2e-12 and res<1e-9:break
  # Final midpoint p is the kinematically consistent canonical momentum.
  return a1,2*xm-x0,2*pm-p0,chi1,pn,sink,qs,{'iterations':it+1,'fixed_point_error':err,'carrier_root_residual':res,'max_carrier_trial_residual':maxres}
