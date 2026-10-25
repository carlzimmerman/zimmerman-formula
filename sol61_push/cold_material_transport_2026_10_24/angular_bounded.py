"""Same finite Hamiltonian; chunk angular transforms in radius to bound memory."""
import numpy as np
from angular_half import Angular as Base
class Angular(Base):
 def chunks(self):
  for lo in range(0,len(self.r),256):yield slice(lo,min(lo+256,len(self.r)))
 def potential(self,v):
  cr=np.empty((len(self.r),self.density.nm),complex)
  for sl in self.chunks():
   va=self.field.forward(v[sl]);cr[sl]=self.density.back(abs(va)**2/(self.w[sl]*self.r[sl]**2)[:,None,None])
  co=self.green(cr);pa=np.empty((len(self.r),len(self.field.mu),self.field.nphi));W=0.
  for sl in self.chunks():
   zz=self.density.forward(co[sl]);assert np.max(abs(zz.imag))<1e-8*max(1,np.max(abs(zz.real)));pa[sl]=zz.real;W+=.5*np.sum(self.field.integral(abs(self.field.forward(v[sl]))**2*pa[sl]))
  return pa,co,float(W)
 def self_energy(self,v):
  cr=np.empty((len(self.r),self.density.nm),complex)
  for sl in self.chunks():
   va=self.field.forward(v[sl]);cr[sl]=self.density.back(abs(va)**2/(self.w[sl]*self.r[sl]**2)[:,None,None])
  co=self.green(cr);return .5*float(np.real(np.sum((self.w*self.r*self.r)[:,None]*cr.conj()*co)))
 def multiply(self,v,pang):
  out=np.empty_like(v)
  for sl in self.chunks():out[sl]=self.field.back(self.field.forward(v[sl])*pang[sl])
  return out
