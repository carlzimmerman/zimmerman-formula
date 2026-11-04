"""Log-coordinate sparse Newton for positive number/Pauli-hole coordinates.

The traced linear-coordinate driver damped full corrections by 1/128 while
several soft holes changed by order-one relative factors. Logarithmic Newton
coordinates keep multiplicative hole changes natural and preserve positivity
without a global lower-bound step restriction. Accepted states are never
clipped. Final physical-number residuals remain an independent obligation.
"""
import numpy as np
from scipy.sparse import eye,diags
from scipy.sparse.linalg import spsolve
from holes_stable import QuantumState
from holes_v2 import implicit_step as first_boundary_step

def implicit_step(events,state,dt,tol=2e-8,maxiter=100):
 if np.any(state.Z<=0):
  new,info=first_boundary_step(events,state,dt,tol=tol,maxiter=maxiter)
  info['method']='linear first boundary step';return new,info
 old=state.copy();new=state.copy();ferm=events.eta<0;switches=0;minimum_alpha=1.;maximum_log_correction=0.
 for it in range(maxiter):
  zz=new.Z/new.measure;switch=ferm&(((~new.holes)&(zz>.65))|(new.holes&(zz>.65)))
  if np.any(switch):
   new.Z[switch]=new.measure[switch]-new.Z[switch];new.holes[switch]=~new.holes[switch]
   old.Z[switch]=old.measure[switch]-old.Z[switch];old.holes[switch]=~old.holes[switch];switches+=int(sum(switch))
  signs=np.where(new.holes,-1.,1.);rhs=signs*new.rhs(events);res=new.Z-old.Z-dt*rhs;F,R,_,_=new.products(events);gross=np.asarray(abs(events.S)@(events.coefficient*(F+R))).ravel();rounding=32*np.finfo(float).eps*dt*gross;scale=1e-30*events.measure+np.maximum(abs(old.Z),abs(new.Z))+rounding/tol;scale=np.maximum(scale,1e-300);norm=float(max(abs(res)/scale))
  if norm<tol:return new,dict(method='log number/hole Newton',iterations=it,residual=norm,coordinate_switches=switches,minimum_line_alpha=minimum_alpha,maximum_log_correction=maximum_log_correction)
  linear=eye(len(res),format='csr')-dt*new.jacobian(events);A=diags(1/scale)@linear@diags(new.Z);du=spsolve(A,-res/scale)
  if not np.all(np.isfinite(du)):raise RuntimeError('log hole nonfinite correction')
  maximum_log_correction=max(maximum_log_correction,float(max(abs(du))));du=np.clip(du,-20.,20.)
  alpha=1.;base=float(np.linalg.norm(res/scale))
  for ls in range(30):
   trial=new.copy();trial.Z=new.Z*np.exp(alpha*du)
   if np.any(trial.Z[ferm]>=trial.measure[ferm]):alpha*=.5;continue
   rr=trial.Z-old.Z-dt*signs*trial.rhs(events);score=float(np.linalg.norm(rr/scale))
   if score<base*(1-1e-6*alpha)+1e-15:break
   alpha*=.5
  else:raise RuntimeError('log hole line search; norm='+str(norm))
  minimum_alpha=min(minimum_alpha,alpha);new=trial
 raise RuntimeError('log hole iteration budget; norm='+str(norm)+' worst='+str(int(np.argmax(abs(res)/scale))))
