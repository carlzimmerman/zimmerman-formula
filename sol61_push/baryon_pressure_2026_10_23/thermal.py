import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
class Thermal:
 def __init__(self,zi=1100,xe=2e-4,nodes=4097):
  self.zi=zi;self.xe=xe;self.H0=67.4*1000/3.085677581491367e22*365.25*86400 # yr^-1
  self.end=np.log((1+zi)/7);grid=np.linspace(0,self.end,nodes)
  def rhs(N,y):
   zp=(1+zi)*np.exp(-N);H=self.H0*np.sqrt(.315)*zp**1.5;rate=8.55e-13*xe*zp**4
   return [-2*y[0]+rate/H*(2.725*zp-y[0])]
  s=solve_ivp(rhs,(0,self.end),[2.725*(1+zi)],method='Radau',t_eval=grid,rtol=2e-10,atol=1e-9)
  assert s.success
  self.spline=CubicSpline(grid,np.log(s.y[0]));self.rhs=rhs
 def at(self,A):
  N=np.log(A);return float(np.exp(self.spline(N))),float(self.spline(N,1))
