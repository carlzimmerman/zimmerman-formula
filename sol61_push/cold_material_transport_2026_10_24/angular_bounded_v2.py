"""Same Green recurrence, reverse accumulation in place, lower peak memory."""
import numpy as np
from angular_bounded import Angular as Base
class Angular(Base):
 def green(self,rho):
  r=self.r;ell=self.ell;shell=(self.w*r*r)[:,None]*rho;ans=np.empty_like(shell);ans[0]=shell[0]/r[0]
  for i in range(1,len(r)):ans[i]=(r[i-1]/r[i])**(ell+1)*ans[i-1]+shell[i]/r[i]
  outer=np.zeros(shell.shape[1],complex)
  for i in range(len(r)-2,-1,-1):
   outer=(r[i]/r[i+1])**ell*(outer+shell[i+1]/r[i+1]);ans[i]+=outer
  ans*=-4*np.pi/(2*ell+1);return ans
 def self_energy(self,v):
  cr=np.empty((len(self.r),self.density.nm),complex)
  for sl in self.chunks():
   va=self.field.forward(v[sl]);cr[sl]=self.density.back(abs(va)**2/(self.w[sl]*self.r[sl]**2)[:,None,None])
  co=self.green(cr);W=0.
  for sl in self.chunks():W+=.5*np.real(np.sum((self.w[sl]*self.r[sl]**2)[:,None]*cr[sl].conj()*co[sl]))
  return float(W)
