import numpy as np
from gradient_constraints import GradientSystem,GradientPadded
from expanded_rate import rate as expanded_rate
class ExpandedSystem(GradientSystem):
 def rhs(self,y):
  y=self.project(y);self.calls+=1;f=self.constrain(y)
  l,b,pl,pb,vol,bx,hk,d,X,N,T,W=[f[z]for z in ['lam','b','pl','pb','vol','bx','hk','d','X','N','T','W']]
  r=self.unpack(y)[3];gauge_rate=N*(pl-pb)/(2*self.M*vol);ldot=gauge_rate.mean()
  ws=self.inverse_theta(ldot-gauge_rate);w=ws/self.k;Nx=self.dx(N)
  Lsp=self.M*np.exp(-l+2*b)*(2*Nx*bx+N*bx*bx)
  F=-d+X-self.V-W-self.g*d*d/2-2*self.g*d*X;FD=-T
  bdot=-N*pl/(2*self.M*vol)+w*bx
  pldot=N*hk+N*vol*(F-FD*d)-Lsp+(ldot-gauge_rate)*pl+w*bx*pb
  rdot=expanded_rate(self.M,np.exp(l),np.exp(2*b),pl,r,bx,self.dxx(b),N,Nx,w,ldot,self.P,self.gvar-self.gvar.mean(),F,FD,-self.g*self.dx(f['q']),d,self.dx(r))
  return np.concatenate([[ldot],bdot,pldot,rdot])
class ExpandedPadded(GradientPadded):
 def __init__(self,n,k=128,evaluation=None):
  self.n=n;self.k=k;self.fine=ExpandedSystem(evaluation or 2*n+1,k)
