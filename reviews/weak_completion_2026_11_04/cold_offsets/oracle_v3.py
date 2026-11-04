"""Finite local spline orbit in excitation/displacement coordinates.

No harmonic branch and no subtraction of total particle/potential energies.
The exact local polynomial interval is a hard domain boundary.
"""
import math
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

MASS=62.

class OffsetOrbit:
 def __init__(self,model,N,Y,phase_nodes=64,mp_dps=70):
  self.model=model;self.N=float(N);self.Y=np.asarray(Y).reshape(model.ns,model.n)
  if np.any(self.Y<0) or not np.all(np.isfinite(self.Y)):raise ValueError('Invalid physical numbers')
  self.anchor,self.base_energy,_,_,_=model.well(N,Y)
  self.t=.004657258204883617*math.exp(-N);self.t3=self.t**3
  raw=np.asarray(model.bg.mass2(self.anchor),float)
  active=np.any(self.Y!=0,axis=1)
  if np.any((raw<0)&active):raise ValueError('An occupied mass-squared clipping branch requires a separate controlled representation')
  self.inactive_omitted=np.where(~active)[0].tolist();self.inactive_negative_mass2=[dict(group=int(i),mass2=float(raw[i])) for i in np.where((raw<0)&~active)[0]]
  raw=np.where(active,raw,0.)
  self.m=np.stack([raw]+[np.where(active,np.asarray(model.bg.mass2(self.anchor,j),float)/math.factorial(j),0.) for j in range(1,4)])
  self.v=np.array([float(model.v(self.anchor,j))/math.factorial(j) for j in range(1,5)])
  self.p2=(self.t*model.q)**2;self.e0=np.sqrt(raw[:,None]+self.p2[None,:])
  spline=model.bg.base.mass2
  i=np.searchsorted(spline.x,self.anchor)-1
  self.left=float(spline.x[i]-self.anchor);self.right=float(spline.x[i+1]-self.anchor)
  if abs(self.anchor-model.v.x0)<.0018:
   self.left=max(self.left,model.v.x0-.0018-self.anchor);self.right=min(self.right,model.v.x0+.0018-self.anchor)
  else:
   p=model.v.original;j=np.searchsorted(p.x,self.anchor)-1
   self.left=max(self.left,float(p.x[j]-self.anchor));self.right=min(self.right,float(p.x[j+1]-self.anchor))
   if self.anchor<model.v.x0-.0018:self.right=min(self.right,model.v.x0-.0018-self.anchor)
   if self.anchor>model.v.x0+.0018:self.left=max(self.left,model.v.x0+.0018-self.anchor)
  with mp.workdps(mp_dps):
   terms=[mp.mpf(float(self.Y[s,k]))*mp.mpf(float(self.m[1,s]))/(2*mp.sqrt(mp.mpf(float(raw[s]))+mp.mpf(float(self.p2[k])))) for s in range(model.ns) for k in range(model.n)]
   self.F0=float(mp.mpf(float(self.v[0]))+mp.mpf(float(self.t3))*mp.fsum(terms))
  self.center=0.
  for _ in range(5):self.center-=float(self.force(self.center))/self.curvature(self.center)
  self.u0=float(self.delta(self.center));self.k=self.curvature(self.center);self.omega=math.sqrt(self.k/MASS)
  if self.k<=0:raise ValueError('Nonpositive local curvature')
  z,w=leggauss(phase_nodes);self.theta=(z+1)*math.pi/2;self.tw=w*math.pi/2
 def _mass_delta(self,d):
  d=np.atleast_1d(d).astype(float)
  if np.any(d<self.left) or np.any(d>self.right):raise ValueError('Outside exact local spline interval')
  dm=d[:,None]*(self.m[1]+d[:,None]*(self.m[2]+d[:,None]*self.m[3]))
  remainder=d[:,None]**2*(self.m[2]+d[:,None]*self.m[3])
  if np.any(self.m[0]+dm<0):raise ValueError('Orbit crosses a mass-squared clipping branch')
  en=np.sqrt(self.e0[None,:,:]**2+dm[:,:,None])
  return d,dm,remainder,en
 def delta(self,d):
  d,dm,rem,en=self._mass_delta(d)
  gas=rem[:,:,None]/(2*self.e0)-dm[:,:,None]**2/(2*self.e0*(en+self.e0)**2)
  return self.F0*d+d*d*(self.v[1]+d*(self.v[2]+d*self.v[3]))+self.t3*np.einsum('ksq,sq->k',gas,self.Y)
 def force(self,d):
  d,dm,rem,en=self._mass_delta(d)
  derivative_rem=d[:,None]*(2*self.m[2]+3*d[:,None]*self.m[3]);derivative=self.m[1]+derivative_rem
  gas=derivative_rem[:,:,None]/(2*self.e0)-derivative[:,:,None]*dm[:,:,None]/(2*en*self.e0*(en+self.e0))
  return self.F0+d*(2*self.v[1]+d*(3*self.v[2]+d*4*self.v[3]))+self.t3*np.einsum('ksq,sq->k',gas,self.Y)
 def curvature(self,d):
  dm=d*(self.m[1]+d*(self.m[2]+d*self.m[3]));en=np.sqrt(self.e0**2+dm[:,None])
  derivative=self.m[1]+d*(2*self.m[2]+3*d*self.m[3]);second=2*self.m[2]+6*d*self.m[3]
  gas=second[:,None]/(2*en)-derivative[:,None]**2/(4*en**3)
  return float(2*self.v[1]+d*(6*self.v[2]+12*d*self.v[3])+self.t3*np.sum(gas*self.Y))
 def offset(self,d):return self.delta(self.center+np.asarray(d))-self.u0
 def orbit(self,J):
  J=float(J)
  if not math.isfinite(J) or J<=0:raise ValueError('This interface requires strictly positive action')
  scaleE=self.omega*J;scaleX=math.sqrt(2*scaleE/self.k)
  def evaluate(ratio,full=False):
   eps=scaleE*ratio
   limitL=(self.left-self.center)/scaleX;limitR=(self.right-self.center)/scaleX
   a=max(limitL,-2.);b=min(limitR,2.)
   if float(self.offset(a*scaleX))<eps or float(self.offset(b*scaleX))<eps:raise ValueError('Turning point outside supported scaled bracket')
   left=brentq(lambda z:float(self.offset(z*scaleX))/eps-1,a,0,xtol=1e-14,rtol=1e-14)
   right=brentq(lambda z:float(self.offset(z*scaleX))/eps-1,0,b,xtol=1e-14,rtol=1e-14)
   mid=(left+right)/2;half=(right-left)/2
   displacement=scaleX*(mid-half*np.cos(self.theta));dx=scaleX*half*np.sin(self.theta)
   kinetic=eps-self.offset(displacement)
   if np.any(kinetic<=0):raise ValueError('Nonpositive interior kinetic energy; no floor is permitted')
   action=math.sqrt(2*MASS)/math.pi*float(self.tw@(dx*np.sqrt(kinetic)))
   if not full:return action/J-1
   ww=self.tw*dx/np.sqrt(kinetic);period=math.sqrt(2*MASS)*sum(ww);ww/=sum(ww)
   return dict(J_requested=J,J=action,excitation=eps,minimum_energy_base=self.base_energy,minimum_offset_from_anchor=self.u0,
     anchor=self.anchor,minimum_displacement=self.center,left_displacement=scaleX*left,right_displacement=scaleX*right,
     period=period,omega=2*math.pi/period,phase_displacements=displacement,weights=ww,kin2=2*kinetic,
     harmonic=False,harmonic_excitation_relative_difference=eps/scaleE-1,
     excitation_lost_in_float_total=(self.base_energy+eps==self.base_energy))
  ratio=brentq(evaluate,.5,2.,xtol=1e-13,rtol=1e-13)
  return evaluate(ratio,True)
