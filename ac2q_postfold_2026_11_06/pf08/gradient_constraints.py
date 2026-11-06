import numpy as np
from fft_constraints import FFTSystem,FFTPadded
class GradientSystem(FFTSystem):
 def recover(self,gvar):
  symbol=1j*self.k*self.modes;symbol[0]=1
  return np.fft.ifft(np.fft.fft(gvar)/symbol).real
 def gradient_fields(self,y,gvar,jac=False):
  P=self.recover(gvar)
  lam,b,pl,r=self.unpack(y);vol=np.exp(lam+2*b);bx=self.dx(b);bxx=self.dxx(b)
  if np.min(abs(pl))<1e-6:raise ValueError('momentum coordinate singular')
  cc=2*self.M**2*np.exp(4*b)/pl;pb=r+cc*(2*bxx+3*bx*bx)
  hk=(pl*pl-2*pl*pb)/(4*self.M*vol);h=(pl*pl-2*pl*r)/(4*self.M*vol*vol)
  op=lambda v:np.exp(-lam)*(self.dx(v)+2*bx*v)
  d=np.exp(-lam)*(gvar-gvar.mean()+2*bx*P);cap=self.K*abs(P)/self.a0
  if np.max(cap)>=1:raise ValueError('flux cap')
  W=self.a0**2/self.K*(-cap-np.log1p(-cap));Wp=self.K*P/(1-cap);Wpp=self.K/(1-cap)**2
  den=1-2*self.g*d
  if np.min(den)<=0:raise ValueError('lapse branch')
  X=-(h+d+self.V+W+self.g*d*d/2)/den
  if np.min(X)<=0:raise ValueError('X nonpositive')
  N=np.sqrt(self.s2/(2*X));q=d+2*X
  if np.min(q)<=0:raise ValueError('switch reached')
  T=1+self.g*q;R=np.exp(-lam)*self.dx(N*T)-N*Wp;J=None
  if jac:
   def apply(v):
    pv=self.recover(v);dv=np.exp(-lam)*(v-v.mean()+2*bx*pv);xv=((-1-self.g*d+2*self.g*X)*dv-Wp*pv)/den
    nv=-N*xv/(2*X);tv=self.g*(dv+2*xv)
    return np.exp(-lam)*self.dx(T*nv+N*tv)-Wp*nv-N*Wpp*pv
   c=1+self.g*d-2*self.g*X
   coef=float(np.mean(np.exp(-2*lam)*N*(self.g+c*c/(2*X*den))))
   mass=float(np.mean(N*Wpp));symbol=-coef*(self.k*self.modes)**2-mass
   mult=1j*self.k*self.modes;mult[0]=1
   inv=lambda v:np.fft.ifft(np.fft.fft(v)*mult/symbol).real
   J=(apply,inv)
  return R,J,dict(lam=lam,b=b,pl=pl,pb=pb,vol=vol,bx=bx,hk=hk,d=d,X=X,N=N,q=q,T=T,W=W,cap=cap)
 def constrain(self,y):
  P=getattr(self,'gvar',self.dx(self.P)+self.P.mean()).copy()
  for it in range(20):
   R,J,f=self.gradient_fields(y,P,True);norm=float(np.max(abs(R)))
   if norm<2e-9:
    self.gvar=P;self.P=self.recover(P);self.max_res=max(self.max_res,norm);self.newton+=it;return f
   apply,inv=J;step=self.solve(apply,-R,inv);accepted=False
   for j in range(20):
    pp=P+step*2.**(-j)
    try:rr,_,_=self.gradient_fields(y,pp)
    except ValueError:continue
    if np.max(abs(rr))<norm:P=pp;accepted=True;break
   if not accepted:raise RuntimeError(f'FFT Newton line search {norm}')
  raise RuntimeError('FFT Newton limit')

class GradientPadded(FFTPadded):
 def __init__(self,n,k=128,evaluation=None):
  self.n=n;self.k=k;self.fine=GradientSystem(evaluation or 2*n+1,k)
