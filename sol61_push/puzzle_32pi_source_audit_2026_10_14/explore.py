import numpy as np
from scipy.integrate import solve_bvp
for d in [.2,1.,5.]:
 for L in [50.,200.]:
  x=np.unique(np.r_[0,np.geomspace(1e-5,L,700),d])
  def fun(x,y):
   ratio=np.full_like(x,1/d**3); np.divide(1.,x**3,out=ratio,where=x>d)
   return np.array([y[1], x*y[0]*np.abs(y[0])-ratio])
  def bc(a,b): return np.array([a[1],3*b[0]+L*b[1]])
  v=1/(x*x+d*d)
  sol=solve_bvp(fun,bc,x,np.array([v,-2*x/(x*x+d*d)**2]),S=np.array([[0,0],[0,-4]]),tol=1e-7,max_nodes=30000)
  pts=np.array([5.,10.,20.,30.]);h=pts*sol.sol(pts)[0]
  print(d,L,sol.status,len(sol.x),max(sol.rms_residuals),'h*x',pts*h,'origin',sol.sol(0)[0],flush=True)
