"""Also inverse-transform the disposable angular kinetic array without a copy."""
import numpy as np
from memory_gauss import Sphere as Base
class Sphere(Base):
 def angular(self,u,tau,apply=False):
  b=self.transform(u);freq=self.eta*self.lam[None,:,:]/(2*self.r[:,None,None]**2)
  b*=self.eta*freq if apply else np.exp(-1j*tau*freq)
  del freq
  for k,Q in enumerate(self.Q):b[:,:,k]=b[:,:,k]@Q.T
  return np.fft.ifft(b,axis=2,norm='ortho')
