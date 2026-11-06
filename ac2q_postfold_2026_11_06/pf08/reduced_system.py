import numpy as np
from expanded_constraints import ExpandedSystem
from dealias import transfer

class ReducedSystem:
 def __init__(self,n,k=128,evaluation=None):
  self.n=n;self.k=k;self.m=evaluation or 2*n+1;self.fine=ExpandedSystem(self.m,k);self.cached_pl=None
 def unpack(self,y):
  n=self.n;return y[0],y[1:1+n],y[1+n],y[2+n:]
 def reduce(self,z):
  l,b,p,r=self.fine.unpack(z)
  return np.concatenate([[l],transfer(b,self.n),[p.mean()],transfer(r,self.n)])
 def expand(self,y):
  l,b,meanp,r=self.unpack(y);bf=transfer(b,self.m);rf=transfer(r,self.m)
  p=np.full(self.m,meanp) if self.cached_pl is None else self.cached_pl-self.cached_pl.mean()+meanp
  z=self.fine.project(np.concatenate([[l],bf,p,rf]));self.cached_pl=z[1+self.m:1+2*self.m].copy();return z
 def initial(self,homogeneous=False):return self.reduce(self.fine.initial(homogeneous))
 def rhs(self,y):return self.reduce(self.fine.rhs(self.expand(y)))
 def diagnostic(self,y,t,rate_check=True):
  z=self.expand(y);f=self.fine.constrain(z);l,b,p,r=self.fine.unpack(z);bx=self.fine.dx(b);S=2*self.fine.dxx(b)+3*bx*bx;C=2*self.fine.M**2*np.exp(4*b)/p
  mom=self.fine.dx(p)-bx*f['pb'];spectra={}
  for key,x in dict(q=f['q'],N=f['N'],b=b,r=r,pb=f['pb']).items():
   coeff=np.fft.fft(x-x.mean());tail=abs(self.fine.modes)>=self.n/3
   spectra[key]=float(np.sum(abs(coeff[tail])**2)/(np.sum(abs(coeff)**2)+1e-100))
  row=dict(time=t,q_min=float(f['q'].min()),q_max=float(f['q'].max()),q_gradient=float(max(abs(self.fine.dx(f['q'])))),X_min=float(f['X'].min()),lapse_max=float(f['N'].max()),cap=float(f['cap'].max()),momentum_abs=float(max(abs(mom))),polarization_residual=self.fine.max_res,spectra=spectra)
  if rate_check:
   native=self.fine.rhs(z);dot=self.reduce(native);L,bt,meanpt,rt=self.unpack(dot);bt=transfer(bt,self.m);rt=transfer(rt,self.m);bxt=self.fine.dx(bt)
   source=bxt*f['pb']+bx*(rt+4*C*bt*S+C*(2*self.fine.dxx(bt)+6*bx*bxt))+meanpt
   diagonal=bx*C*S/p;symbol=1j*self.k*self.fine.modes;symbol[0]=1
   inv=lambda v:np.fft.ifft(np.fft.fft(v)/symbol).real
   pt=self.fine.solve(lambda v:self.fine.dx(v)+diagonal*v+v.mean(),source,inv)
   reference=self.fine.unpack(native)[2];diff=pt-reference;scale=max(1e-10,float(max(abs(reference))))
   row['represented_rate_error']=float(max(abs(transfer(diff,self.n)))/scale);row['full_rate_error']=float(max(abs(diff))/scale)
  return row

def rk4(sys,y,dt):
 a=sys.rhs(y);b=sys.rhs(y+dt*a/2);c=sys.rhs(y+dt*b/2);d=sys.rhs(y+dt*c)
 return y+dt*(a+2*b+2*c+d)/6
