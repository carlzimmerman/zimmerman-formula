"""Odd Fourier padding, with physical variables and time integrator unchanged."""
import numpy as np
from evolve_projected import System as Fine

def transfer(x,m):
 n=len(x);a=np.fft.fftshift(np.fft.fft(x))/n
 if m>=n:
  z=np.zeros(m,dtype=complex);z[(m-n)//2:(m+n)//2]=a
 else:z=a[(n-m)//2:(n+m)//2]
 return np.fft.ifft(np.fft.ifftshift(z)*m).real

class Padded:
 def __init__(self,n,k=128,factor=3):
  self.n=n;self.fine=Fine(n*factor,k);self.k=k;self.factor=factor
 def lift(self,y,m):
  n=(len(y)-1)//3
  return np.concatenate([[y[0]],*[transfer(y[1+j*n:1+(j+1)*n],m)for j in range(3)]])
 def initial(self,homogeneous=False):return self.lift(self.fine.initial(homogeneous),self.n)
 def project(self,y):return self.lift(self.fine.project(self.lift(y,self.fine.n)),self.n)
 def rhs(self,y):return self.lift(self.fine.rhs(self.lift(y,self.fine.n)),self.n)
 def diagnostic(self,y,t):return self.fine.diagnostic(self.lift(y,self.fine.n),t)
