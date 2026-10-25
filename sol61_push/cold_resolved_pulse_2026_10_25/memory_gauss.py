"""Unchanged Green recurrence with shorter-lived arrays and owned real output."""
import numpy as np
from gauss import Sphere as Gauss
class Sphere(Gauss):
 def poisson_mass(self,m):
  src=m/(self.w*self.r*self.r)[:,None,None]/self.sa[None,:,:];coef=self.transform(src);del src
  out=np.empty_like(coef);A=np.zeros_like(coef[0]);r=self.r;ell=self.ell
  for i in range(len(r)):
   if i:A*=np.exp(ell*np.log(r[i-1]/r[i]))
   A+=self.w[i]*r[i]**2*coef[i];out[i]=A/r[i]
  B=np.zeros_like(A)
  for i in range(len(r)-1,-1,-1):
   if i+1<len(r):B*=np.exp(ell*np.log(r[i]/r[i+1]))
   f=self.w[i]*r[i]*coef[i];B+=f;out[i]+=B-f
  del coef
  out*=-4*np.pi/(2*ell[None,:,:]+1)
  for k,Q in enumerate(self.Q):out[:,:,k]=out[:,:,k]@Q.T
  pot=np.fft.ifft(out,axis=2,norm='ortho');del out
  pot/=self.sa[None,:,:];assert np.max(abs(pot.imag))<1e-8*max(1,np.max(abs(pot.real)))
  return pot.real.copy()
