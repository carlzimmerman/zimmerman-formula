import numpy as np
from radial_base import Radial as Base
from thermal import Thermal
class Radial(Base):
 gamma=5/3;xe=2e-4;baryon_ratio=1.;pressure=True
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.thermal=Thermal(self.zi,self.xe)
  self.vunit=self.ell*3.085677581491367e19/(self.t0*1e9*365.25*86400)
  self.kT=1.380649e-23/(1.22*1.67262192369e-27*self.vunit**2)
 def gas_terms(self,xb,A):
  rho,ids,dw=self.dep(xb,self.mb);mean=self.mb.sum()/self.vol.sum();x=rho/mean
  if min(x)<=0:raise ValueError('gas_vacuum')
  T,beta=self.thermal.at(A);cT=self.kT*T if self.pressure else 0.;g=self.gamma
  if g==1: F=x*np.log(x)-x+1;h=cT*np.log(x)
  else: F=(x**g-g*x+g-1)/(g-1);h=cT*g/(g-1)*(x**(g-1)-1)
  U=mean*cT*np.sum(self.vol*F);force=-np.sum(h[ids]*dw,axis=1)
  return force,U,beta*U,dict(Tmean_K=T,Tmax_closure_K=float(T*max(x)**(g-1)),gas_pressure_energy=float(U),gas_crossings=int(sum(np.diff(xb)<0)))
 def evaluate(self,xc,xb,P,c,A,pc,pb,Q,V):
  s=list(super().evaluate(xc,xb,P,c,A,pc,pb,Q,V));f,U,work,d=self.gas_terms(xb,A);s[1]=s[1]+f;s[4]+=U;s[5]+=work;s[6].update(d);s[6]['energy']=float(s[4]);s[6]['scale']+=abs(U);return tuple(s)
