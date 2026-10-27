import numpy as np
from scipy.integrate import solve_ivp
import json

def trial(eps,nu,x0,rtol=1e-9,step=.05):
 def pot(x): return 3*x*x+(eps+6)*nu*(x-1)**2/2
 def rhs(t,y):
  x,u,h=y
  fx=1/(4*x**3); fxx=-3/(4*x**4)
  ux=6*x+(eps+6)*nu*(x-1)
  mat=np.array([[eps,-24*fx*h*h],[8*h*h*fx,2+16*h*fx*u]])
  b=np.array([-3*eps*h*u-ux+24*fx*h**4,-eps*u*u+8*h**3*fx*u-8*h*h*fxx*u*u])
  up,hp=np.linalg.solve(mat,b)
  return np.array([u,up,hp])
 y0=[x0,0.,np.sqrt(pot(x0)/3)]
 def stop(t,y): return min(y[0]-.05,5-y[0],y[2]-.01,5-y[2])
 stop.terminal=True
 sol=solve_ivp(rhs,[0,30],y0,rtol=rtol,atol=rtol*.01,max_step=step,events=stop,dense_output=True)
 x,u,h=sol.y; fx=1/(4*x**3); fxx=-3/(4*x**4)
 up=np.array([rhs(t,y)[1] for t,y in zip(sol.t,sol.y.T)])
 qt=1+8*h*fx*u; ft=1+8*(fx*up+fxx*u*u)
 con=3*h*h-(.5*eps*u*u+pot(x)-24*h**3*fx*u)
 return {'eps':eps,'nu':nu,'initial_x':x0,'success':bool(sol.success),'end_t':float(sol.t[-1]),'final_x':float(x[-1]),'final_u':float(u[-1]),'final_h':float(h[-1]),'max_constraint_relative':float(np.max(np.abs(con)/(3*h*h))),'min_tensor_kinetic':float(qt.min()),'min_tensor_gradient':float(ft.min()),'max_tensor_speed_squared_deviation':float(np.max(abs(ft/qt-1))),'samples':len(sol.t)}
rows=[trial(e,n,x) for e in [1e-120,1e-6] for n in [1.,10.] for x in [.9,1.1]]
for row in rows:
 assert row['success'] and row['end_t']==30
 assert max(abs(row['final_x']-1),abs(row['final_h']-1),abs(row['final_u']))<1e-4,row
 assert row['max_constraint_relative']<1e-7,row
# Numeric convergence for one named corner; not more parameter discovery.
fine=trial(1e-120,10.,1.1,rtol=1e-11,step=.025)
coarse=rows[3]
assert abs(fine['final_x']-coarse['final_x'])<1e-7
neutral=trial(1e-120,0.,1.1)
assert abs(neutral['final_x']-1.1)<1e-8
unstable=trial(1e-120,-1.,1.1)
assert abs(unstable['final_x']-1)>abs(1.1-1)
print(json.dumps({'trajectories':rows,'refinement':fine,'neutral_control':neutral,'negative_restoring_control':unstable,'scope':'Finite homogeneous FRW evolution only. Tensor coefficients monitored; scalar gradients and nonlinear spatial health not established.'},indent=2))
