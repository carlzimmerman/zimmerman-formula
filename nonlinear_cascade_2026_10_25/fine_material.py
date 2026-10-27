"""Same physical model on a grid that carries short material waves outward.
Generated explicit vectorized copies of inherited methods; no changed forces.
"""
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'nonlinear_transfer_2026_10_25'))
from physical_branch import PhysicalFull
class FineMaterial(PhysicalFull):
 def __init__(self,material_h_kpc=.125,**kw):
  super().__init__(**kw);oldedges=self.edges.copy();inner=oldedges[oldedges*self.rm<.5];ed=np.r_[inner,.5/self.rm,np.arange(.5+material_h_kpc,320+material_h_kpc*.1,material_h_kpc)/self.rm,np.geomspace(320/self.rm,self.R,97)[1:]];self.edges=ed;self.r=(ed[1:]+ed[:-1])/2;self.vol=np.diff(ed**3)/3;self.n=len(self.r);self.w=((self.r[1:]+self.r[:-1])/2)**2/np.diff(self.r);self.gb=self.r/(self.r**2+self.b**2)**1.5;self.kd=.5*self.k*np.r_[self.w[0],self.w[:-1]+self.w[1:],self.w[-1]]/self.vol;self.ko=-.5*self.k*self.w/np.sqrt(self.vol[1:]*self.vol[:-1]);self.ids=np.clip(np.searchsorted(self.wr,self.r)-1,0,len(self.wr)-2);self.frac=np.clip((self.r-self.wr[self.ids])/(self.wr[self.ids+1]-self.wr[self.ids]),0,1);self.kcache={};self.wcache={};self.material_h_kpc=material_h_kpc
 def pot(self,a,alpha,grad=False):
  mt=abs(a[0])**2;mf=abs(a[1])**2;mass=mt+mf;u=self.enclosed(mt);gd=self.enclosed(mass);W,F,Wp,Fp=self.f(u);qv=np.sin(alpha)**2;s=np.sin(2*alpha)**2/np.pi**2;uf=(u[1:]+u[:-1])/2;_,ff,_,fp=self.f(uf);x=2*alpha/np.pi;dx=np.diff(x);Mt=np.sum(mt);M=np.sum(mass);wt,_,wpt,_=self.f(Mt*self.tt**2)
  E=np.sum(self.vol*(W+self.beta*s*F)) +np.sum(self.tw*wt/self.tt**4)+.5*np.sum(self.w*(self.ell2*ff+self.vac)*dx*dx)+self.B*(self.vol@qv)-self.eps*Mt+1.5*self.K*np.sum(self.vol*(mf/self.vol)**(5/3))-np.sum(self.vol*(.5*gd*gd+self.gb*gd))-.5*M*M/self.R-M/np.sqrt(self.R*self.R+self.b*self.b)
  if not grad:return float(E)
  response=self.vol*(Wp+self.beta*s*Fp);face=.25*self.ell2*self.w*fp*dx*dx;response[:-1]+=face;response[1:]+=face;muR=self.transpose(response)+np.sum(self.tw*wpt/self.tt**2);muG=-self.transpose(self.vol*(gd+self.gb))-M/self.R-1/np.sqrt(self.R*self.R+self.b*self.b)
  return float(E),np.array([muG+muR-self.eps,muG+2.5*self.K*(mf/self.vol)**(2/3)])

 def carrier_mid(self,a,chi,x0,p0,dt,guess):
  Z=self.Z(a);parts=self.vacuum_parts(a,chi);x=guess.copy();add=4*Z/dt**2
  for it in range(35):
   gg,hh,off,scale=self.carrier_force(x,parts);g=gg+add*(x-x0)-2*p0/dt;hd=hh+add;res=np.max(abs(g)/(scale+add))
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

 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  a1=a0.copy();chi1=chi0.copy();xm=x0.copy();maxres=0.;err=np.inf
  for it in range(45):
   amid=(a0+a1)/2;cmid=(chi0+chi1)/2;xm,pm,res=self.carrier_mid(amid,cmid,x0,p0,dt,xm);maxres=max(maxres,res);mu=self.pot(amid,xm,True)[1];u=self.enclosed(abs(amid[0])**2);angular_rate=pm/self.Z(amid);mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*angular_rate**2*self.f(u)[3]);an=self.material_cn(a0,mu,xm,cmid,dt);am=(a0+an)/2;align=self.alignment(am,xm,cmid);rate=2*self.J/self.sigma*np.imag(np.conj(am[0])*align[0]);cn,pn,sink,qs=self.wave_source(chi0,pi0,rate,dt)
   err=max(float(np.max(abs(an-a1))),float(np.max(abs(cn-chi1)))*max(self.g,1)/self.sigma)
   a1=an;chi1=cn
   if err<2e-12 and res<1e-9:break
  # Final midpoint p is the kinematically consistent canonical momentum.
  return a1,2*xm-x0,2*pm-p0,chi1,pn,sink,qs,{'iterations':it+1,'fixed_point_error':err,'carrier_root_residual':res,'max_carrier_trial_residual':maxres}

 def energy(self,a,alpha,chi,pi):
  aligned=np.cos(alpha)*np.exp(1j*self.g*self.chi_m(chi)/self.sigma)*a[0]-np.sin(alpha)*a[1]
  return self.pot(a,alpha)+self.kinetic(a)+self.J*float(np.sum(abs(aligned)**2))+.5*(self.wvol@(pi*pi)+self.c**2*(self.ww@np.diff(chi)**2))

 def full_energy(self,a,x,p,chi,pi):return self.energy(a,x,chi,pi)+float(.5*np.sum(p*p/self.Z(a)))

