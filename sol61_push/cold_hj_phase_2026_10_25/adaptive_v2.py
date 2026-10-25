"""Adaptive real radial reference with explicitly compensated changes of gauge."""
import pathlib,sys,numpy as np
from scipy.interpolate import CubicSpline
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/'cold_lens_phase_2026_10_25'))
from lens import Grid,VariableAxis

class Radial:
 def __init__(self,g,nr=1025):
  self.g=g;self.R=np.linspace(0,np.sqrt(3)*g.box,nr);self.dr=self.R[1];self.bin=np.minimum(np.rint(g.r/self.dr).astype(int),nr-1)
 def reference(self,u):
  dm=np.bincount(self.bin.ravel(),weights=abs(u.ravel())**2,minlength=len(self.R));inv=np.divide(1,self.R,out=np.zeros_like(self.R),where=self.R>0);cum=np.cumsum(dm);outer=np.sum(dm*inv)-np.cumsum(dm*inv)
  pot=-(cum*inv+outer);pot[0]=-np.sum(dm*inv);return pot
 def rhs(self,S,ref):
  dm=np.r_[(S[0]-S[1])/self.dr,np.diff(S)/self.dr];dp=np.r_[np.diff(S)/self.dr,(S[-1]-S[-2])/self.dr]
  H=np.where(dm<=dp,np.where((dm<=0)&(dp>=0),0,np.minimum(dm*dm,dp*dp)),np.maximum(dm*dm,dp*dp))/2
  return -H-ref
 def advance(self,S,ref,dt):
  v=np.max(abs(np.diff(S)/self.dr))+dt*np.max(abs(np.diff(ref)/self.dr));n=max(1,int(np.ceil(dt*v/(.35*self.dr))))
  if n>128:raise RuntimeError('HJ substep cap128')
  h=dt/n;s=S.copy()
  for _ in range(n):
   b=s+h*self.rhs(s,ref);s=.5*s+.5*(b+h*self.rhs(b,ref))
  return s,n
 def evaluate(self,S):
  spl=CubicSpline(self.R,S);value=spl(self.g.r);speed=spl(self.g.r,1)
  return value,[speed*x/self.g.r for x in self.g.xyz]

class DynamicAxis(VariableAxis):
 def set_p(self,g,p,tau):
  v=np.moveaxis(p,self.axis,0);den=(2*np.sqrt(g.w[:-1]*g.w[1:])).reshape((-1,1,1))
  self.h[:]=self.eta**2/2*g.o[:,None,None]-1j*self.eta*(v[:-1]+v[1:])/2/den
  self.set_tau(tau)

class Adaptive:
 def __init__(self,g,eta,radial,S,gravity=True,omit_gauge=False):
  self.g=g;self.eta=eta;self.radial=radial;self.S=S.copy();self.value,self.p=radial.evaluate(S);self.gravity=gravity;self.omit=omit_gauge
  self.ops=[DynamicAxis(g,eta,self.p[k],k,.01) for k in range(3)]
 def potential(self,u):return self.g.poisson(abs(u)**2) if self.gravity else np.zeros_like(self.g.r)
 def kinetic(self,u,p):
  g=self.g;eta=self.eta;m=abs(u)**2;total=float(.5*np.sum(m*sum(v*v for v in p)))
  for k in range(3):
   z=np.moveaxis(u,k,0);v=np.moveaxis(p[k],k,0);den=(2*np.sqrt(g.w[:-1]*g.w[1:])).reshape((-1,1,1));h=eta**2/2*g.o[:,None,None]-1j*eta*(v[:-1]+v[1:])/2/den
   total+=float(eta**2/2*np.sum(g.d[:,None,None]*abs(z)**2)+2*np.real(np.sum(z[:-1].conj()*h*z[1:])))
  return total
 def moments(self,u,phi):
  g=self.g;m=abs(u)**2;K=self.kinetic(u,self.p);W=float(.5*np.sum(m*phi));cur=[]
  for k in range(3):
   z=np.moveaxis(u,k,0);den=(2*np.sqrt(g.w[:-1]*g.w[1:])).reshape((-1,1,1));d=np.zeros_like(z);d[:-1]+=z[1:]/den;d[1:]-=z[:-1]/den
   cur.append(np.moveaxis(self.eta*np.imag(z.conj()*d),0,k)+m*self.p[k])
  return dict(M=float(m.sum()),K=K,W=W,E=K+W,P=[float(v.sum()) for v in cur],J=[float(np.sum(g.xyz[(k+1)%3]*cur[(k+2)%3]-g.xyz[(k+2)%3]*cur[(k+1)%3])) for k in range(3)])
 def step(self,u,q,phi,t,dt,analytic=None):
  u=np.asarray(u,dtype=np.complex128)
  oldS=self.S;oldV=self.value;oldp=self.p
  if analytic is None:
   ref0=self.radial.reference(u) if self.gravity else np.zeros_like(oldS);pred,n=self.radial.advance(oldS,ref0,dt);midS=(oldS+pred)/2
  else:midS=analytic(t+dt/2,self.radial.R);n=0
  midV,midp=self.radial.evaluate(midS);Kold=self.kinetic(u,oldp)
  if not self.omit:u=u*np.exp(1j*(oldV-midV)/self.eta)
  Kpre=self.kinetic(u,midp);potential=phi+sum(v*v for v in midp)/2
  u*=np.exp(-1j*dt/(2*self.eta)*potential);bond=0.
  for k in (0,1,2,1,0):
   op=self.ops[k];op.set_p(self.g,midp[k],dt*(1 if k==2 else .5));u,q,e=op.apply(u,q);bond=max(bond,e)
  phi=self.potential(u);potential=phi+sum(v*v for v in midp)/2;u*=np.exp(-1j*dt/(2*self.eta)*potential)
  Kpost=self.kinetic(u,midp)
  if analytic is None:
   ref1=self.radial.reference(u) if self.gravity else np.zeros_like(oldS);newS,n2=self.radial.advance(oldS,(ref0+ref1)/2,dt);n=max(n,n2)
  else:newS=analytic(t+dt,self.radial.R)
  newV,newp=self.radial.evaluate(newS)
  if not self.omit:u*=np.exp(1j*(midV-newV)/self.eta)
  self.S=newS;self.value=newV;self.p=newp;Knew=self.kinetic(u,newp)
  return u,q,phi,dict(bond=bond,gauge_signed=Kpre-Kold+Knew-Kpost,gauge_absolute=abs(Kpre-Kold)+abs(Knew-Kpost),HJ_substeps=n)
