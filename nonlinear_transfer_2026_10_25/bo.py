"""Asymptotic zero-carrier-inertia Hamiltonian, solved implicitly.

This is not the failed explicit split relaxation. All material, scalar and
instantaneous carrier force equations are jointly solved at the midpoint.
Finite carrier dynamics remains a separate obligation.
"""
import numpy as np
from scipy.linalg import solve_banded
from full import Full

class BO(Full):
 def root_alpha(self,a,chi,guess):
  parts=self.vacuum_parts(a,chi);x=guess.copy();res=np.inf
  for it in range(40):
   g,hd,off,scale=self.carrier_force(x,parts);res=max(abs(g)/scale)
   if res<1e-12:break
   ab=np.zeros((3,self.n));ab[0,1:]=off;ab[1]=hd;ab[2,:-1]=off
   try:d=solve_banded((1,1),ab,-g,check_finite=False)
   except np.linalg.LinAlgError:break
   merit=np.sum(g*g/scale);rate=1.
   for ls in range(20):
    xx=x+rate*d;gg=self.carrier_force(xx,parts)[0]
    if sum(gg*gg/scale)<=merit+1e-30:break
    rate*=.5
   x=xx
  return x,float(res)
 def carrier_mid(self,a,chi,x0,p0,dt,guess):
  x,res=self.root_alpha(a,chi,guess);return x,np.zeros(self.n),res
 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  a,x,p,chi,pi,sink,qs,info=super().full_step(a0,x0,np.zeros(self.n),chi0,pi0,dt);xe,res=self.root_alpha(a,chi,(x+x0)/2);info['carrier_root_residual']=max(info['carrier_root_residual'],res);return a,xe,np.zeros(self.n),chi,pi,sink,qs,info
