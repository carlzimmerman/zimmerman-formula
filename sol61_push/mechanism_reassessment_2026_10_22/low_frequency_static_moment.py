import json,sys
import numpy as np
from scipy.integrate import solve_bvp,simpson,cumulative_trapezoid
import sympy as sp
from backreaction_response import background,run,G

def static(end):
 bg=background(end)
 def hh(r):
  q,_=bg.sol(r);return (1-q)**-2-1
 def fun(r,y):
  p,d=y;g=-r*np.exp(-r*r/2)/(2*np.pi)**1.5
  return np.array([d,(hh(r)*p-g)/G-2*d/r+2*p/r**2])
 mesh=np.geomspace(1e-5,end,1000)
 sol=solve_bvp(fun,lambda a,b:np.array([a[1]-a[0]/1e-5,b[0]]),mesh,np.zeros((2,len(mesh))),tol=2e-9,max_nodes=10000)
 r=np.linspace(1e-5,end,60000);p,d=sol.sol(r)
 integ=cumulative_trapezoid(p,r,initial=0);sigma=integ-integ[-1]
 rho=(r*r-3)*np.exp(-r*r/2)/(2*np.pi)**1.5
 chi=simpson(-r*r*rho*sigma,x=r)
 energy=simpson(r*r*(hh(r)*p*p+G*(d+2*p/r)**2),x=r)
 # Endpoint term from integrating sigma L sigma; outer sigma=p=0.
 # Remaining inner contributions are tiny and recorded by raw comparison.
 return dict(S0=float(simpson(r*r*sigma,x=r)),outer=end,status=sol.status,background_status=bg.status,chi=float(chi),energy=float(energy),identity_error=float(abs(chi/energy-1)))

if __name__=='__main__': print(json.dumps([static(30),static(60)],indent=2))
