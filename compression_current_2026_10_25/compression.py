"""Positive canonical completion of a density-weighted T current."""
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'nonlinear_transfer_2026_10_25'))
from physical_branch import PhysicalFull

class Compression(PhysicalFull):
 def __init__(self,eta=1.,**kw):
  super().__init__(**kw);self.rho_coupling=None;self.eta=eta;s=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');mt=abs(s['a'][0])**2;mass=np.sum(abs(s['a'])**2,axis=0);rho=mt/self.vol;L=200/self.rm;u=(self.r/L)**4;vel=self.r*np.exp(-u);source=-rho*rho*np.exp(-u)*(3-4*u);fm=source*self.vol;prev=np.cumsum(fm)-fm;D=float(sum((fm*fm+2*fm*prev)/self.r));I=float(mass@(vel*vel));assert D>0 and I>0;self.g2=self.c*np.sqrt(eta*I/D);self.calibration={'eta':eta,'g1':self.g,'g2':self.g2,'mode_transport_inertia':I,'mode_source_Poisson_norm':D,'added_inertia':self.g2**2/self.c**2*D,'convention':'v=r exp[-(r/200kpc)^4]; pure transport of both species, Gamma=0; source=-rhoT² div v. This matches one quasistatic added inertia, not a fundamental coefficient or a law fit.'}
 def geometry(self,a,chi,rho=None):
  if rho is None:rho=self.rho_coupling if self.rho_coupling is not None else abs(a[0])**2/self.vol
  cm=self.chi_m(chi);beta=(self.g+2*self.g2*rho)*cm/self.sigma;face=.5*(rho[1:]+rho[:-1]);b=self.g2/self.sigma*(2*rho[1:]*cm[1:]-2*rho[:-1]*cm[:-1]-face*np.diff(cm));return rho,cm,beta,np.exp(1j*b)
 def alignment(self,a,alpha,chi):
  beta=self.geometry(a,chi)[2];ph=np.exp(-1j*beta);c=np.cos(alpha);s=np.sin(alpha);return np.array([c*c*a[0]-s*c*ph*a[1],s*s*a[1]-s*c*np.conj(ph)*a[0]])
 def vacuum_parts(self,a,chi):
  mt=abs(a[0])**2;mf=abs(a[1])**2;u=self.enclosed(mt);F=self.f(u)[1];fc=self.f((u[1:]+u[:-1])/2)[1];coeff=(2/np.pi)**2*self.w*(self.ell2*fc+self.vac);cross=np.real(np.exp(1j*self.geometry(a,chi)[2])*np.conj(a[1])*a[0]);return mt,mf,F,coeff,cross
 def kinetic(self,a,chi=None):
  if chi is None:chi=getattr(self,'energy_chi',np.zeros(len(self.wr)))
  U=self.geometry(a,chi,rho=abs(a[0])**2/self.vol)[3];psi=a/np.sqrt(self.vol)[None,:];return float(.5*self.k*sum(self.w*(abs(U*psi[0,1:]-psi[0,:-1])**2+abs(np.diff(psi[1]))**2)))
 def energy(self,a,alpha,chi,pi):
  beta=self.geometry(a,chi,rho=abs(a[0])**2/self.vol)[2];B=np.cos(alpha)*np.exp(1j*beta)*a[0]-np.sin(alpha)*a[1];return self.pot(a,alpha)+self.kinetic(a,chi)+self.J*float(sum(abs(B)**2))+.5*(self.wvol@(pi*pi)+self.c**2*(self.ww@np.diff(chi)**2))
 def transfer(self,a,x,chi):
  rho,cm,beta,U=self.geometry(a,chi);psi=a[0]/np.sqrt(self.vol);D=self.k*self.w*np.imag(np.conj(psi[:-1])*U*psi[1:]);rate=2*self.J/self.sigma*np.imag(np.conj(a[0])*self.alignment(a,x,chi)[0]);mu=2*self.g2*cm*rate/self.vol
  mu[:-1]+=D*self.g2/self.sigma*(-.5*cm[1:]-1.5*cm[:-1])/self.vol[:-1];mu[1:]+=D*self.g2/self.sigma*(1.5*cm[1:]+.5*cm[:-1])/self.vol[1:]
  bulk=np.zeros(self.n);bulk[:-1]+=D*self.g2/self.sigma*(-1.5*rho[:-1]+.5*rho[1:]);bulk[1:]+=D*self.g2/self.sigma*(1.5*rho[1:]-.5*rho[:-1]);conv=(self.g+2*self.g2*rho)*rate
  return mu,bulk+conv,bulk,conv,U,rate
 def material_cn(self,a0,mu,x,chi,dt):
  fac=1j*dt/(2*self.sigma);diag=(self.kd+mu).T.copy();diag[:,0]+=self.J*np.cos(x)**2;diag[:,1]+=self.J*np.sin(x)**2;local=-self.J*np.sin(x)*np.cos(x)*np.exp(-1j*self.geometry(a0,chi)[2]);U=self.geometry(a0,chi)[3];edges=np.array([self.ko*U,self.ko]).T.ravel();ab=np.zeros((5,2*self.n),complex);ab[2]=1+fac*diag.ravel();ab[1,1::2]=fac*local;ab[3,::2]=fac*np.conj(local);ab[0,2:]=fac*edges;ab[4,:-2]=fac*np.conj(edges)
  Ha=(self.kd+mu)*a0+self.J*self.alignment(a0,x,chi);Ha[0,:-1]+=self.ko*U*a0[0,1:];Ha[0,1:]+=self.ko*np.conj(U)*a0[0,:-1];Ha[1,:-1]+=self.ko*a0[1,1:];Ha[1,1:]+=self.ko*a0[1,:-1];ans=solve_banded((2,2),ab,(a0-fac*Ha).T.ravel(),check_finite=False);return ans.reshape(self.n,2).T
 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  a1=a0.copy();chi1=chi0.copy();xm=x0.copy();err=np.inf
  for it in range(60):
   self.rho_coupling=(abs(a0[0])**2+abs(a1[0])**2)/(2*self.vol);amid=(a0+a1)/2;cmid=(chi0+chi1)/2;xm,pm,res=self.carrier_mid(amid,cmid,x0,p0,dt,xm);mu=self.pot(amid,xm,True)[1];u=self.enclosed(abs(amid[0])**2);omega=pm/self.Z(amid);mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*omega**2*self.f(u)[3]);mu[0]+=self.transfer(amid,xm,cmid)[0];an=self.material_cn(a0,mu,xm,cmid,dt);am=(a0+an)/2;_,source,bulk,conv,U,rate=self.transfer(am,xm,cmid);cn,pn,sink,qs=self.wave_source(chi0,pi0,source/self.g,dt)
   err=max(float(max(abs(an-a1).ravel())),float(max(abs(cn-chi1)))*max(self.g+2*self.g2*max(self.rho_coupling),1)/self.sigma);a1=an;chi1=cn
   if err<2e-12 and res<1e-9:break
  self.rho_coupling=None;self.energy_chi=chi1
  return a1,2*xm-x0,2*pm-p0,chi1,pn,sink,qs,{'iterations':it+1,'fixed_point_error':err,'carrier_root_residual':res,'source_cell':source,'source_bulk':bulk,'source_conversion':conv}
 def charge(self,a,pi):
  mt=abs(a[0])**2;return float(self.wvol@pi+self.g*sum(mt)+self.g2*sum(mt*mt/self.vol))
