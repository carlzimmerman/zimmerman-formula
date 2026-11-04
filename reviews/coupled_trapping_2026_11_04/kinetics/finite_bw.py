"""Conditional static coherent Breit-Wigner pairkernel in two-species transport."""
import sys
sys.dont_write_bytecode=True
import math,numpy as np
from numpy.polynomial.legendre import leggauss
from accurate import Accurate
from two_species import ROOT,PREF,MASS
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance'))
import pole_api as pole

def pair_fast(x,t,q,n=12,blocked=False):
 p=t*np.asarray(q);m=float(pole.mass(x));en=np.sqrt(m*m+p*p);center=2*m*m+2*en[:,None]*en[None,:];span=2*p[:,None]*p[None,:];lo=center-span;hi=center+span;gg=pole.GAMMA_BOSON if blocked else pole.GAMMA;width=pole.M*float(max(gg));a=np.arctan((lo-pole.M*pole.M)/width);b=np.arctan((hi-pole.M*pole.M)/width);z,w=leggauss(n);theta=(a+b)[None,:,:]/2+(b-a)[None,:,:]*z[:,None,None]/2;ss=pole.M*pole.M+width*np.tan(theta);jac=width/np.cos(theta)**2;values=pole.sigma_cm(x,ss,blocked)*ss/(4*en[None,:,None]*en[None,None,:]);answer=np.sum(w[:,None,None]*values*jac,axis=0)*(b-a)/2/np.maximum(hi-lo,1e-300);small=(hi-lo<1e-20)|(b-a<1e-11);answer[small]=pole.sigma_cm(x,center[small],blocked)*center[small]/(4*(en[:,None]*en[None,:])[small]);return (answer+answer.T)/2

class Finite(Accurate):
 def __init__(self,*a,blocked=False,angular=12,**kw):
  super().__init__(*a,**kw);self.blocked=blocked;self.angular=angular;self.all_scalar=self.scalar;self.nonpole_scalar=[dict(row,parents=[[M,W] for M,W in row['parents'] if abs(M-pole.M)>1e-8]) for row in self.scalar]
 def scalar_kernel(self,x,t):
  if abs(x-self.poles[1])>.05:return super().scalar_kernel(x,t)
  self.scalar=self.nonpole_scalar;other=super().scalar_kernel(x,t);self.scalar=self.all_scalar;sig=pair_fast(x,t,self.q,self.angular,self.blocked);return other+PREF*t**6/2*(self.W[:,None]*self.W[None,:])*sig
 def orbital(self,N,f,J=None,E=None):
  orb=super().orbital(N,f,J=J,E=E);xl=orb['xl'];xr=orb['xr'];xp=self.poles[1]
  if xr<xp-.06 or xl>xp+.06 or xr-xl<1e-12:return orb
  mid=(xl+xr)/2;half=(xr-xl)/2;bounds=[0.,math.pi];t=orb['t'];dm=.003*xp/(2*math.sqrt(xp*xp+2/(31*.003)));thermal=t*t/(pole.M*dm);width=float(max(pole.GAMMA))/(4*dm)
  for scale,factors,signs in ((thermal,(0.,.05,.2,1.,4.,16.,64.,256.),(-1,)),(width,(.1,1.,3.,10.,30.,100.,300.,1000.),(-1,1))):
   for fac in factors:
    for sign in signs:
     x=xp+sign*fac*scale
     if xl<x<xr:bounds.append(math.acos(max(-1,min(1,(mid-x)/half))))
  bounds=sorted(set(bounds));theta=[];qw=[]
  for a,b in zip(bounds[:-1],bounds[1:]):theta.extend(((a+b)/2+(b-a)*self.rz/2).tolist());qw.extend(((b-a)*self.rw/2).tolist())
  theta=np.array(theta);qw=np.array(qw);xs=mid-half*np.cos(theta);rho,pr,en=self.gas(xs,t,f);harmonic=J is not None and hasattr(self,'J0') and J<=self.J0*1e-6
  if harmonic:weights=qw/math.pi;period=orb['period'];kin2=4*math.pi*J/period*np.sin(theta)**2
  else:
   delta=np.maximum(orb['E']-self.v(xs)-rho,1e-35);ww=qw*half*np.sin(theta)/np.sqrt(delta);period=math.sqrt(2*MASS)*sum(ww);weights=ww/sum(ww);kin2=2*delta;self.max_period_relative_change=max(self.max_period_relative_change,abs(period/orb['period']-1))
  self.max_phase_nodes=max(self.max_phase_nodes,len(xs));orb.update(period=period,xs=xs,weights=weights,rho=rho,pr=pr,en=en,kin2=kin2);return orb
