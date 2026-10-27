"""Actual inherited potential/carrier with a new regular mediator sector.

Canonical chart: complex psi, alpha,p_alpha, chi, integrated P_chi, s,P_s.
No scalar absorber; Hamiltonian and charge checks require a closed system.
"""
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'compression_current_2026_10_25'))
from compression import Compression

class Matched:
 def __init__(self,length_kpc=.01,alpha_factor=2.):
  self.m=m=Compression(eta=.01,wave_R_kpc=10000.)
  self.reference=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz')
  rhomax=np.max(abs(self.reference['a'][0])**2/m.vol)
  # Sensitivity family, NOT coefficients predicted by framework.
  self.alpha=alpha_factor*m.g2**2*rhomax/m.c**2
  self.M=m.c/(length_kpc/m.rm);self.h=self.M*np.sqrt(self.alpha);self.lam=m.g2/self.h
  self.length_kpc=length_kpc
 def deposit(self,q):
  m=self.m
  return np.bincount(m.ids,weights=(1-m.frac)*q,minlength=len(m.wr))+np.bincount(m.ids+1,weights=m.frac*q,minlength=len(m.wr))
 def lapgrad(self,w,y):
  out=np.zeros_like(y);e=w*np.diff(y);out[:-1]-=e;out[1:]+=e;return out
 def geometry(self,z):
  m=self.m;a,x,p,c,P,s,ps=z;rho=abs(a[0])**2/m.vol;A=m.g+self.h*s
  v=(P-self.deposit(A*abs(a[0])**2))/m.wvol;cm=m.chi_m(c);vm=m.chi_m(v)
  face=(A[1:]+A[:-1])/2;dc=np.diff(cm);U=np.exp(-1j*face*dc/m.sigma)
  psi=a/np.sqrt(m.vol);D=m.k*m.w*np.imag(np.conj(psi[0,:-1])*U*psi[0,1:])
  return rho,A,v,cm,vm,face,dc,U,psi,D
 def align(self,a,x):
  c=np.cos(x);s=np.sin(x)
  return np.array([c*c*a[0]-s*c*a[1],s*s*a[1]-s*c*a[0]])
 def parts(self,a):
  m=self.m;mt=abs(a[0])**2;mf=abs(a[1])**2;u=m.enclosed(mt)
  return mt,mf,m.f(u)[1],(2/np.pi)**2*m.w*(m.ell2*m.f((u[1:]+u[:-1])/2)[1]+m.vac),np.real(np.conj(a[1])*a[0])
 def energy(self,z):
  m=self.m;a,x,p,c,P,s,ps=z;rho,A,v,cm,vm,face,dc,U,psi,D=self.geometry(z)
  old=m.pot(a,x)+.5*m.k*np.sum(m.w*(abs(U*psi[0,1:]-psi[0,:-1])**2+abs(np.diff(psi[1]))**2))
  old+=m.J*np.sum(abs(np.cos(x)*a[0]-np.sin(x)*a[1])**2)+.5*np.sum(p*p/m.Z(a))
  wave=.5*np.sum(m.wvol*v*v)+.5*m.c*m.c*np.sum(m.ww*np.diff(c)**2)
  mediator=.5*np.sum(ps*ps/m.vol)+.5*m.c*m.c*np.sum(m.w*np.diff(s)**2)+.5*self.M**2*np.sum(m.vol*(s-self.lam*rho)**2)
  return float(old+wave+mediator)
 def gradient(self,z):
  m=self.m;a,x,p,c,P,s,ps=z;rho,A,v,cm,vm,face,dc,U,psi,D=self.geometry(z)
  mu=m.pot(a,x,True)[1];xd=p/m.Z(a);u=m.enclosed(abs(a[0])**2)
  mu[0]-=(2/np.pi)**2*m.ell2/m.c**2*m.transpose(.5*m.vol*xd*xd*m.f(u)[3])
  mu[0]+=-A*vm-self.M**2*self.lam*(s-self.lam*rho)
  ga=(m.kd+mu)*a+m.J*self.align(a,x)
  ga[0,:-1]+=m.ko*U*a[0,1:];ga[0,1:]+=m.ko*np.conj(U)*a[0,:-1]
  ga[1,:-1]+=m.ko*a[1,1:];ga[1,1:]+=m.ko*a[1,:-1]
  gx=m.carrier_force(x,self.parts(a))[0]
  edge=face*D/m.sigma;gc0=np.zeros(m.n);gc0[:-1]+=edge;gc0[1:]-=edge
  gc=m.c*m.c*self.lapgrad(m.ww,c)+self.deposit(gc0)
  gs=m.c*m.c*self.lapgrad(m.w,s)+self.M**2*m.vol*(s-self.lam*rho)-self.h*abs(a[0])**2*vm
  se=-self.h*D*dc/(2*m.sigma);gs[:-1]+=se;gs[1:]+=se
  return ga,gx,xd,gc,v,gs,ps/m.vol
 def field(self,z):
  ga,gx,gp,gc,gP,gs,gps=self.gradient(z)
  return -1j*ga/self.m.sigma,gp,-gx,gP,-gc,gps,-gs
 def relaxed_s(self,a):
  m=self.m;rho=abs(a[0])**2/m.vol
  # Solve s=lambda*t to avoid cancellation/conditioning from small lambda.
  L2=(m.c/self.M)**2
  diag=m.vol+L2*np.r_[m.w[0],m.w[:-1]+m.w[1:],m.w[-1]]
  ab=np.zeros((3,m.n));ab[1]=diag;ab[0,1:]=-L2*m.w;ab[2,:-1]=-L2*m.w
  t=solve_banded((1,1),ab,m.vol*rho)
  return self.lam*t
 def static(self,a,x):
  m=self.m;s=self.relaxed_s(a);c=np.zeros(len(m.wr));P=self.deposit((m.g+self.h*s)*abs(a[0])**2)
  return a,x,np.zeros(m.n),c,P,s,np.zeros(m.n)
