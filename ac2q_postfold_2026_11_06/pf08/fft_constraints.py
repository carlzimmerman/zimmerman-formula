"""Matrix-free implementation of the unchanged PF07 adapted constraints."""
import sys
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator,gmres
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pf07'))
from evolve_projected import System as Dense
from dealias import Padded

class FFTSystem(Dense):
 def __init__(self,n,k):
  assert n%2==1
  self.n=n;self.k=k;self.g=.1;self.s2=.01;self.V=.01;self.M=1.;self.K=.5;self.a0=.3
  self.modes=np.fft.fftfreq(n,1/n);self.P=np.zeros(n);self.max_res=0.;self.calls=0;self.newton=0;self.linear_iterations=0
 def dx(self,q):return np.fft.ifft(1j*self.k*self.modes*np.fft.fft(q-q.mean())).real
 def dxx(self,q):return np.fft.ifft(-(self.k*self.modes)**2*np.fft.fft(q-q.mean())).real
 def dtheta(self,q):return self.dx(q)/self.k
 def solve(self,apply,rhs,precondition):
  J=LinearOperator((self.n,self.n),matvec=apply,dtype=float)
  M=LinearOperator((self.n,self.n),matvec=precondition,dtype=float)
  def cb(res):self.linear_iterations+=1
  sol,info=gmres(J,rhs,M=M,tol=1e-10,atol=1e-11,restart=30,maxiter=8,callback=cb,callback_type='pr_norm')
  residual=float(np.max(abs(apply(sol)-rhs)))
  if info or residual>max(2e-11,1e-8*float(np.max(abs(rhs)))):raise RuntimeError(f'GMRES {info} residual {residual}')
  return sol
 def project(self,y):
  lam,b,pl,r=self.unpack(y);pl=pl.copy();target=pl.mean();bx=self.dx(b)
  cs=2*self.M**2*np.exp(4*b)*(2*self.dxx(b)+3*bx*bx)
  symbol=1j*self.k*self.modes;symbol[0]=1
  inv=lambda v:np.fft.ifft(np.fft.fft(v)/symbol).real
  for _ in range(8):
   residual=self.dx(pl)-bx*(r+cs/pl)+(pl.mean()-target)
   if np.max(abs(residual))<1e-11:break
   diagonal=bx*cs/pl**2
   pl-=self.solve(lambda v:self.dx(v)+diagonal*v+v.mean(),residual,inv)
  actual=self.dx(pl)-bx*(r+cs/pl)
  if np.max(abs(actual))>1e-8:raise RuntimeError('FFT momentum projection')
  z=y.copy();z[1+self.n:1+2*self.n]=pl;return z
 def fields(self,y,P,jac=False):
  lam,b,pl,r=self.unpack(y);vol=np.exp(lam+2*b);bx=self.dx(b);bxx=self.dxx(b)
  if np.min(abs(pl))<1e-6:raise ValueError('momentum coordinate singular')
  cc=2*self.M**2*np.exp(4*b)/pl;pb=r+cc*(2*bxx+3*bx*bx)
  hk=(pl*pl-2*pl*pb)/(4*self.M*vol);h=(pl*pl-2*pl*r)/(4*self.M*vol*vol)
  op=lambda v:np.exp(-lam)*(self.dx(v)+2*bx*v)
  d=op(P);cap=self.K*abs(P)/self.a0
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
    dv=op(v);xv=((-1-self.g*d+2*self.g*X)*dv-Wp*v)/den
    nv=-N*xv/(2*X);tv=self.g*(dv+2*xv)
    return np.exp(-lam)*self.dx(T*nv+N*tv)-Wp*nv-N*Wpp*v
   c=1+self.g*d-2*self.g*X
   coef=float(np.mean(np.exp(-2*lam)*N*(self.g+c*c/(2*X*den))))
   mass=float(np.mean(N*Wpp));symbol=-coef*(self.k*self.modes)**2-mass
   inv=lambda v:np.fft.ifft(np.fft.fft(v)/symbol).real
   J=(apply,inv)
  return R,J,dict(lam=lam,b=b,pl=pl,pb=pb,vol=vol,bx=bx,hk=hk,d=d,X=X,N=N,q=q,T=T,W=W,cap=cap)
 def constrain(self,y):
  P=self.P.copy()
  for it in range(20):
   R,J,f=self.fields(y,P,True);norm=float(np.max(abs(R)))
   if norm<2e-9:
    self.P=P;self.max_res=max(self.max_res,norm);self.newton+=it;return f
   apply,inv=J;step=self.solve(apply,-R,inv);accepted=False
   for j in range(20):
    pp=P+step*2.**(-j)
    try:rr,_,_=self.fields(y,pp)
    except ValueError:continue
    if np.max(abs(rr))<norm:P=pp;accepted=True;break
   if not accepted:raise RuntimeError(f'FFT Newton line search {norm}')
  raise RuntimeError('FFT Newton limit')

class FFTPadded(Padded):
 def __init__(self,n,k=128,evaluation=None):
  self.n=n;self.k=k;self.fine=FFTSystem(evaluation or 2*n+1,k)
