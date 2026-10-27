"""Exact fixed-density carrier potential divided differences, no energy projection."""
import numpy as np
from momentum import Momentum

def sincprime(z):
 z=np.asarray(z);small=abs(z)<1e-3;safe=np.where(small,1.,z);regular=(safe*np.cos(safe)-np.sin(safe))/safe**2
 return np.where(small,-z/3+z**3/30-z**5/840,regular)
class TrigDG(Momentum):
 def carrier_mid(self,a,chi,x0,p0,dt,guess):
  self.endpoint0=x0
  try:return super().carrier_mid(a,chi,x0,p0,dt,guess)
  finally:self.endpoint0=None
 def carrier_force(self,x,parts):
  if getattr(self,'endpoint0',None) is None:return super().carrier_force(x,parts)
  mt,mf,F,d,cross=parts;delta=2*(x-self.endpoint0);s1=np.sinc(delta/np.pi);s2=np.sinc(2*delta/np.pi);A=2*self.beta*self.vol*F/np.pi**2;B=self.B*self.vol+self.J*(mf-mt);C=2*self.J*cross;U=B*np.sin(2*x)-C*np.cos(2*x);G=A*np.sin(4*x)*s2+U*s1;hd=4*A*(np.cos(4*x)*s2+np.sin(4*x)*sincprime(2*delta))+(2*B*np.cos(2*x)+2*C*np.sin(2*x))*s1+2*U*sincprime(delta);dx=np.diff(x);G[:-1]-=d*dx;G[1:]+=d*dx;hd+=np.r_[d[0],d[:-1]+d[1:],d[-1]];scale=1e-18+np.r_[d[0],d[:-1]+d[1:],d[-1]]+2*self.J*(mt+mf)+2*self.B*self.vol+8*self.beta*self.vol*F/np.pi**2;return G,hd,-d,scale
