"""Symmetric centered discrete-gradient steps; fourth-order composition."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'cold_formation_data_2026_10_25'))
from radial_v4 import Radial,phi_shell
import numpy as np
from scipy.linalg import solve_banded
class Solver(Radial):
 def __init__(self,*a,strength=1.,**kw):super().__init__(*a,**kw);self.strength=strength
 def phi(self,u):return self.strength*phi_shell(self.r,abs(u)**2)
 def step(self,old,phi,dt):
  n=len(old);M=np.vdot(old,old).real;Ko=self.apply(old);mu0=float((np.vdot(old,Ko).real+np.sum(abs(old)**2*(self.pb+phi)))/M);mu=mu0;guess=phi.copy();c=1j*dt/(2*self.eta);prior=float('inf')
  for it in range(100):
   p=self.pb+.5*(phi+guess)-mu;rhs=old-c*(Ko+p*old);ab=np.zeros((7,n),complex);ab[3]=1+c*(self.diag+p)
   for d,h in enumerate(self.upper,1):ab[3-d,d:]=c*h;ab[3+d,:-d]=c*h.conj()
   sol=solve_banded((3,3),ab,rhs,overwrite_ab=True,check_finite=False);Kn=self.apply(sol);pn=self.phi(sol);mn=abs(sol)**2;target=.5*(mu0+float((np.vdot(sol,Kn).real+np.sum(mn*(self.pb+pn)))/mn.sum()));res=sol-old+c*(Kn+Ko+(self.pb+.5*(phi+pn)-target)*(sol+old));error=max(float(np.linalg.norm(res)/np.sqrt(M)),abs(target-mu)*abs(dt)/self.eta)
   if error<1e-11:return sol*np.exp(-1j*target*dt/self.eta),pn,dict(converged=True,residual=error,iterations=it+1)
   mix=.5 if error>prior*1.2 else 1.;guess=(1-mix)*guess+mix*pn;mu=(1-mix)*mu+mix*target;prior=error
  if error<=1e-10:return sol*np.exp(-1j*target*dt/self.eta),pn,dict(converged=True,residual=error,iterations=it+1)
  return old,phi,dict(converged=False,residual=error,iterations=it+1)
 def order4(self,old,phi,dt):
  x=1/(2-2**(1/3));u=old;p=phi;its=0;res=0.
  for a in [x,1-2*x,x]:
   u,p,info=self.step(u,p,a*dt);its+=info['iterations'];res=max(res,info['residual'])
   if not info['converged']:return old,phi,dict(converged=False,residual=res,iterations=its)
  return u,p,dict(converged=True,residual=res,iterations=its)
 def doubled(self,u,p,dt):
  coarse,_,a=self.order4(u,p,dt)
  if not a['converged']:return u,p,float('inf'),a
  mid,pm,b=self.order4(u,p,dt/2)
  if not b['converged']:return u,p,float('inf'),b
  fine,pf,c=self.order4(mid,pm,dt/2)
  if not c['converged']:return u,p,float('inf'),c
  return fine,pf,float(np.linalg.norm(fine-coarse)/15),dict(converged=True,residual=max(a['residual'],b['residual'],c['residual']),iterations=a['iterations']+b['iterations']+c['iterations'])
