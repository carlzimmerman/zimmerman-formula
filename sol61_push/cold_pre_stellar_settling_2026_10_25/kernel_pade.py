"""Unitary high-linear-order rational map, same nonlinear energy identity."""
import math,numpy as np
from scipy.linalg import solve_banded
from kernel import Solver as Base
class Solver(Base):
 degree=8
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw);m=self.degree;c=[math.factorial(2*m-k)*math.factorial(m)/(math.factorial(2*m)*math.factorial(k)*math.factorial(m-k)) for k in range(m+1)];roots=list(np.polynomial.polynomial.polyroots(c));ordered=[]
  while roots:
   r=roots.pop(0);ordered.append(r)
   if abs(r.imag)>1e-8:
    j=int(np.argmin([abs(z-r.conjugate()) for z in roots]));ordered.append(roots.pop(j))
  self.factors=-1/np.array(ordered)
 def rational(self,u,p,dt):
  n=len(u);v=u.copy()
  for b in self.factors:
   c=1j*b*dt/self.eta;rhs=v-c*(self.apply(v)+p*v);ab=np.zeros((7,n),complex);ab[3]=1+c*(self.diag+p)
   for d,h in enumerate(self.upper,1):ab[3-d,d:]=c*h;ab[3+d,:-d]=c*h.conj()
   v=solve_banded((3,3),ab,rhs,overwrite_ab=True,check_finite=False)
  return v
 def step(self,old,phi,dt):
  M=np.vdot(old,old).real;Ko=self.apply(old);mu0=float((np.vdot(old,Ko).real+np.sum(abs(old)**2*(self.pb+phi)))/M);mu=mu0;guess=phi.copy();last=None;prior=float('inf');res=float('inf')
  for it in range(60):
   sol=self.rational(old,self.pb+.5*(phi+guess)-mu,dt);pn=self.phi(sol);mn=abs(sol)**2;target=.5*(mu0+float((np.vdot(sol,self.apply(sol)).real+np.sum(mn*(self.pb+pn)))/mn.sum()));delta=max(float(np.max(abs(pn-guess))*abs(dt)/self.eta),abs(target-mu)*abs(dt)/self.eta)
   if delta<1e-10:
    witness=self.rational(old,self.pb+.5*(phi+pn)-target,dt);res=float(np.linalg.norm(witness-sol)/np.sqrt(M))
    if res<=1e-10:return sol*np.exp(-1j*target*dt/self.eta),pn,dict(converged=True,residual=res,iterations=it+1)
   mix=.5 if delta>prior*1.2 else 1.;guess=(1-mix)*guess+mix*pn;mu=(1-mix)*mu+mix*target;prior=delta
  return old,phi,dict(converged=False,residual=max(res,delta),iterations=it+1)
