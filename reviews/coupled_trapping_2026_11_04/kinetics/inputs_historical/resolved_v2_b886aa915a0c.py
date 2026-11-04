"""Resolve the narrow late scalarresonance along the fast field orbit."""
import sys
sys.dont_write_bytecode=True
import math,numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
from two_species import Two,MASS
class Resolved(Two):
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw);self.poles=(brentq(lambda x:float(self.mass(x))-math.sqrt(.006)/2,20,30),math.sqrt(.006/.003**2-2/(31*.003)));self.rz,self.rw=leggauss(4);self.max_phase_nodes=0;self.max_period_relative_change=0
 def orbital(self,N,f,J=None,E=None):
  orb=super().orbital(N,f,J=J,E=E);xl=orb['xl'];xr=orb['xr'];t=orb['t']
  if xr<23 or xr-xl<1e-5:return orb
  mid=(xl+xr)/2;half=(xr-xl)/2;bounds=[0.,math.pi]
  for index,pole in enumerate(self.poles):
   m=math.sqrt(.006)/2;dm=float(self.mass(pole,1)) if index==0 else .003*pole/(2*math.sqrt(pole*pole+2/(31*.003)));base=t*t/(2*m*dm)
   for factor in (0.,.05,.2,1.,4.,16.,64.,256.):
    x=pole-factor*base
    if xl<x<xr:bounds.append(math.acos(max(-1,min(1,(mid-x)/half))))
  if len(bounds)==2:return orb
  bounds=sorted(set(bounds));theta=[];weights=[]
  for lo,hi in zip(bounds[:-1],bounds[1:]):theta.extend(((hi+lo)/2+(hi-lo)*self.rz/2).tolist());weights.extend(((hi-lo)*self.rw/2).tolist())
  theta=np.array(theta);qw=np.array(weights);xs=mid-half*np.cos(theta);rho,pr,en=self.gas(xs,t,f);delta=np.maximum(orb['E']-self.v(xs)-rho,1e-35);w=qw*half*np.sin(theta)/np.sqrt(delta);period=math.sqrt(2*MASS)*sum(w);self.max_period_relative_change=max(self.max_period_relative_change,abs(period/orb['period']-1));self.max_phase_nodes=max(self.max_phase_nodes,len(xs));orb.update(period=period,xs=xs,weights=w/sum(w),rho=rho,pr=pr,en=en,kin2=2*delta);return orb
