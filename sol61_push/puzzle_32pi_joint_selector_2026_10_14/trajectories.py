import numpy as np,json
from scipy.integrate import solve_ivp

def trial(z,y0,eps=1.,rtol=1e-9):
 def rhs(t,s):
  y,u,h=s
  ev=np.exp(np.clip(z*(y*y-1),-700,100))
  mat=np.array([[eps,-6*h*h/y],[2*z*h*h/y,2+4*z*h*u/y]])
  vec=np.array([-3*eps*h*u-6*y*ev+6*h**4/y,-eps*z*u*u+2*z*h**3*u/y+2*z*h*h*u*u/y**2])
  up,hp=np.linalg.solve(mat,vec)
  return [u,up,hp]
 def diagnostics(s):
  y,u,h=s;_,up,hp=rhs(0,s)
  qt=1+2*z*h*u/y;ft=1+2*z*(up/y-u*u/y**2)
  ct=ft/qt;we=-1-2*hp/(3*h*h)
  ks=eps*qt+6*z*h**4/y**2
  cs=(eps*qt-2*z*(2+ct+6*we)*h**4/y**2)/ks
  cons=3*h*h-(3*np.exp(z*(y*y-1))+eps*z*u*u/2-6*z*h**3*u/y)
  return np.array([qt,ft,ks,cs,cons])
 def bounds(t,s): return min(s[0]-.2,3-s[0],s[2]-.05)
 bounds.terminal=True;bounds.direction=-1
 def health(t,s): return float(np.min(diagnostics(s)[:4]))
 health.terminal=True;health.direction=-1
 h0=np.exp(z*(y0*y0-1)/2)
 sol=solve_ivp(rhs,(0,60),[y0,0,h0],method='DOP853',rtol=rtol,atol=rtol*1e-2,max_step=.05,events=[bounds,health],dense_output=True)
 assert sol.success,sol.message
 ts=np.linspace(0,sol.t[-1],5001);ss=sol.sol(ts).T
 ds=np.array([diagnostics(s) for s in ss])
 res={'z':z,'eps':eps,'initial_y':y0,'end_time':float(sol.t[-1]),'final_y_u_h':sol.y[:,-1].tolist(),'min_QT_FT_Ksbar_cs2':ds[:,:4].min(axis=0).tolist(),'max_constraint_abs':float(np.abs(ds[:,4]).max()),'linear_mass_over_H2':12*(1-z)/(eps+6*z),'event':'bound' if len(sol.t_events[0]) else ('health' if len(sol.t_events[1]) else None),'rtol':rtol}
 assert res['max_constraint_abs']<1e-6,res
 return res
rows=[trial(z,y) for z in [1e-12,.1,.5,.9,1.5] for y in [.98,1.02]]
# A tolerance refinement for one stable near-threshold and one unstable case.
ref=[trial(.9,1.02,rtol=3e-10),trial(1.5,1.02,rtol=3e-10)]
print(json.dumps({'trajectories':rows,'refinements':ref,'scope':'Finite homogeneous initial conditions with sampled short-wavelength signs and event stops; no global basin, local-source or full cosmology proof.'},indent=2))
