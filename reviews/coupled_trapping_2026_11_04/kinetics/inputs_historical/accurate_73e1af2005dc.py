"""Local coldpotential offset/derivative and harmonic-orbit precision controls."""
import sys
sys.dont_write_bytecode=True
import math,numpy as np
from scipy.optimize import brentq
from resolved_v2 import Resolved
from two_species import PREF,MASS
class LocalPotential:
 def __init__(self,original,local):
  self.original=original;self.x0=float(local['reference_x']);self.ref=float(local['reference_V_origin_subtracted_mu4']);self.co=np.array([float(local['fourth_derivative'])/24,float(local['third_derivative_mu'])/6,float(local['radial_curvature_mu2'])/2,0.,0.])
 def __call__(self,x,nu=0):
  x=np.asarray(x);dx=x-self.x0;local=np.polyval(np.polyder(self.co,nu),dx);far=self.original(x,nu)-(self.ref if nu==0 else 0);return np.where(abs(dx)<.0018,local,far)
class Accurate(Resolved):
 def force(self,x,t,f):
  p=t*self.q;F=float(self.mass(x));dF=float(self.mass(x,1));S=.003/2*math.sqrt(x*x+2/(31*.003));dS=.003*x/(2*math.sqrt(x*x+2/(31*.003)));en=np.r_[np.sqrt(F*F+p*p),np.sqrt(S*S+p*p)];num=np.r_[np.full(self.n,F*dF),np.full(self.n,S*dS)];return float(self.v(x,1))+PREF*t**3*float((np.tile(self.W,2)*f)@(num/en))
 def orbital(self,N,f,J=None,E=None):
  if E is not None or not hasattr(self,'J0') or J>self.J0*1e-6:return super().orbital(N,f,J=J,E=E)
  self.floor_count+=1;t=self.t0*math.exp(-N);ug=self.potential(self.grid,t,f);mins=np.where((ug[1:-1]<ug[:-2])&(ug[1:-1]<ug[2:]))[0]+1
  if not len(mins):raise RuntimeError('no localwell in derivative harmonic continuation')
  i=int(mins[0]);xm=brentq(lambda x:self.force(x,t,f),self.grid[i-1],self.grid[i+1],xtol=1e-13);emin=float(self.potential(xm,t,f)[0]);h=1e-5;k=(self.force(xm+h,t,f)-self.force(xm-h,t,f))/(2*h)
  if k<=0:raise RuntimeError('nonpositive localforce curvature')
  omega=math.sqrt(k/MASS);amp=math.sqrt(2*J*omega/k);xl=xm-amp;xr=xm+amp;bounds=[0.,math.pi]
  if amp>1e-12:
   for index,pole in enumerate(self.poles):
    dm=float(self.mass(pole,1)) if index==0 else .003*pole/(2*math.sqrt(pole*pole+2/(31*.003)));base=t*t/(2*math.sqrt(.006)/2*dm)
    for factor in (0.,.05,.2,1.,4.,16.,64.,256.):
     x=pole-factor*base
     if xl<x<xr:bounds.append(math.acos(max(-1,min(1,(xm-x)/amp))))
  bounds=sorted(set(bounds));theta=[];weights=[]
  for lo,hi in zip(bounds[:-1],bounds[1:]):theta.extend(((hi+lo)/2+(hi-lo)*self.rz/2).tolist());weights.extend(((hi-lo)*self.rw/2).tolist())
  theta=np.array(theta);weights=np.array(weights)/math.pi;xs=xm-amp*np.cos(theta);rho,pr,en=self.gas(xs,t,f);self.max_phase_nodes=max(self.max_phase_nodes,len(xs));return dict(E=emin+omega*J,J=J,xl=xl,xr=xr,xm=xm,period=2*math.pi/omega,xs=xs,weights=weights,rho=rho,pr=pr,en=en,kin2=2*J*omega*np.sin(theta)**2,t=t,minimum=emin)
