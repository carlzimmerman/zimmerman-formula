import numpy as np
from scipy.integrate import solve_bvp

def cold_reference(tol=1e-8):
 t=np.linspace(1e-6,1,600);edge=2.
 m=2.5*t**3-1.5*t**5;rho=7.5*(1-t*t)/edge**3
 def fun(t,y,p):
  R=p[0];r=R*t;q=y[0]/r**2
  return np.array([R*r*r*y[1],R/.01*(q*q/(1-q)-r/(1+r*r)**1.5)])
 def bc(a,b,p):return np.array([a[0]-a[1]*(p[0]*1e-6)**3/3,b[0]-1,b[1]])
 sol=solve_bvp(fun,bc,t,np.array([m,rho]),p=[edge],tol=tol,max_nodes=20000)
 grid=np.linspace(1e-6,1,1000);y=sol.sol(grid);edge=sol.p[0]
 out=dict(status=sol.status,edge=float(edge),central_density=float(y[1,0]),min_density=float(y[1].min()),max_q=float((y[0]/(edge*grid)**2).max()),profile=[])
 for r in [.1,.3,.5,1.]:
  mm,dd=sol.sol(r/edge);out['profile'].append(dict(r=r,q=float(mm/r**2),rho=float(dd)))
 return out
if __name__=='__main__':
 import json
 print(json.dumps(cold_reference(),indent=2))
