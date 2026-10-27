"""Stable evaluations of the SAME Hamiltonian, not new physical terms."""
import numpy as np
from full import Full
from bo import BO

class StableNumerics:
 def f(self,u):
  u=np.asarray(u);v=np.minimum(u,.98);d=u-v;poly=np.zeros_like(v)+1/16
  for n in range(15,1,-1):poly=1/n+v*poly
  W=np.where(abs(v)<.05,v*v*poly,-np.log1p(-v)-v)+d*.98/.02+.5*d*d/.02**2
  F=v*v/(1-v)+d*.98*1.02/.02**2+d*d/.02**3;Wp=v/(1-v)+d/.02**2;Fp=v*(2-v)/(1-v)**2+2*d/.02**3
  return W,F,Wp,Fp
 def kinetic(self,a):
  psi=a/np.sqrt(self.vol)[None,:];return float(.5*self.k*np.sum(self.w*np.sum(abs(np.diff(psi,axis=1))**2,axis=0)))
 def energy(self,a,alpha,chi,pi):
  aligned=np.cos(alpha)*np.exp(1j*self.g*self.chi_m(chi)/self.sigma)*a[0]-np.sin(alpha)*a[1]
  return self.pot(a,alpha)+self.kinetic(a)+self.J*float(sum(abs(aligned)**2))+.5*(self.wvol@(pi*pi)+self.c**2*(self.ww@np.diff(chi)**2))

class StableFull(StableNumerics,Full):pass

class StableBO(StableNumerics,BO):
 def carrier_mid(self,*args,**kw):
  x,p,res=super().carrier_mid(*args,**kw);self.last_mid_alpha=x.copy();return x,p,res
