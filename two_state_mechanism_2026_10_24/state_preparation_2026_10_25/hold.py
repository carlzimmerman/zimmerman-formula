"""Independent ODE preparation and exact finite-time averaging at fixed final field."""
import argparse,json
import numpy as np
from scipy.integrate import solve_ivp
CHI=11.220184543019636

def run(N,rtol):
 T=1000.;ef=.01;ti=.1;mi=1.;theta0=np.arctan(mi/ef)
 u,w=np.polynomial.legendre.leggauss(N);u=(u+1)/2;w=CHI*u*w/2
 b0=np.column_stack((u,np.full(N,mi),np.zeros(N)));mag=np.linalg.norm(b0,axis=1)
 L=np.tanh(mag/(2*ti));r=-b0/mag[:,None]*L[:,None]
 U0=w@np.sum(b0*r,axis=1)
 def fun(t,y):
  r=y[:-1].reshape(N,3);s=np.sin(np.pi*t/(2*T))**2;sd=np.pi/(2*T)*np.sin(np.pi*t/T)
  theta=theta0*(1-s);m=ef*np.tan(theta);e=ef*s
  md=-ef*theta0*sd/np.cos(theta)**2;ed=ef*sd
  b=np.column_stack((u,np.full(N,m),np.full(N,-e)))
  return np.r_[(2*np.cross(b,r)).ravel(),w@(md*r[:,1]-ed*r[:,2])]
 sol=solve_ivp(fun,(0,T),np.r_[r.ravel(),0.],method='DOP853',rtol=rtol,atol=rtol*.01,t_eval=[T])
 assert sol.success
 r=sol.y[:-1,-1].reshape(N,3);work=sol.y[-1,-1]
 b=np.column_stack((u,np.zeros(N),np.full(N,-ef)));omega=2*np.linalg.norm(b,axis=1);axis=b/(omega/2)[:,None]
 parallel=axis*np.sum(r*axis,axis=1)[:,None];transverse=r-parallel;cross=np.cross(axis,r)
 Pdiag=w@parallel[:,2];U=w@np.sum(b*r,axis=1)
 P0=CHI*ef/(np.hypot(1,ef)+ef);S0=CHI*ef-P0
 holds=[]
 for t1,t2 in [(0.,100.),(0.,1000.),(1000.,2000.),(0.,10000.)]:
  dt=t2-t1;c=(np.sin(omega*t2)-np.sin(omega*t1))/(omega*dt)
  s=(np.cos(omega*t1)-np.cos(omega*t2))/(omega*dt)
  Pmean=w@(parallel[:,2]+c*transverse[:,2]+s*cross[:,2])
  bound=w@(2*np.hypot(transverse[:,2],cross[:,2])/(omega*dt))
  holds.append(dict(start=t1,end=t2,mean_P=float(Pmean),source_relative_error=float((P0-Pmean)/S0),
   phase_independent_relative_bound_about_diagonal=float(bound/S0)))
 return dict(N=N,rtol=rtol,nfev=sol.nfev,work_on_medium=float(work),
  final_energy_work_residual=float(U-U0-work),maximum_final_length_error=float(max(abs(np.linalg.norm(r,axis=1)-L))),
  instantaneous_source_relative_error=float((P0-w@r[:,2])/S0),diagonal_source_relative_error=float((P0-Pdiag)/S0),holds=holds)

p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
rows=[run(N,tol) for N,tol in [(384,1e-9),(768,1e-9),(1536,1e-9),(768,1e-11)]]
with open(a.output,'w') as f:json.dump(dict(runs=rows),f,indent=2,allow_nan=False)
print(json.dumps(rows))
