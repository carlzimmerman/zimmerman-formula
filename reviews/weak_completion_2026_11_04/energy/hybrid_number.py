"""Same physical BE equation with linear/log Newton coordinate selection.

The N=0 packet is dominated by empty/seed-sized coordinates. A linear-number
solve avoids the large log predictor there; populated states use the validated
log route. Both use the same explicit vacancies and absolute residual budget.
Zero populations affect only a positive Newton GUESS, never the old state.
"""
import numpy as np
from scipy.sparse import eye
from scipy.sparse.linalg import spsolve
from seeded_number_v2 import QuantumState,implicit_step as logarithmic_step

def linear_step(events,state,dt,tol=2e-8,maxiter=100,number_floor=1e-14,guess=None,zero_guess_occupation=1e-40):
 old=state.copy();new=state.copy() if guess is None else guess.copy();ferm=events.eta<0;changes=old.holes!=new.holes
 if np.any(changes):old.Z[changes]=old.measure[changes]-old.Z[changes];old.holes[changes]=new.holes[changes]
 zeros=new.Z==0;new.Z[zeros]=zero_guess_occupation*new.measure[zeros];switches=0
 for it in range(maxiter):
  switch=ferm&(new.Z/new.measure>.65)
  if np.any(switch):
   new.Z[switch]=new.measure[switch]-new.Z[switch];new.holes[switch]=~new.holes[switch];old.Z[switch]=old.measure[switch]-old.Z[switch];old.holes[switch]=~old.holes[switch];switches+=int(sum(switch))
  signs=np.where(new.holes,-1.,1.);res=new.Z-old.Z-dt*signs*new.rhs(events);gross=new.gross(events);rounding=32*np.finfo(float).eps*dt*gross;scale=1e-30*events.measure+number_floor*(~new.holes)+np.maximum(abs(old.Z),abs(new.Z))+rounding/tol;scale=np.maximum(scale,1e-300);norm=float(max(abs(res)/scale))
  if norm<tol:return new,dict(method='linear-number Newton',iterations=it,residual=norm,coordinate_switches=switches,initial_zero_guess_coordinates=int(sum(zeros)),physical_coordinate_residual_L1=float(sum(abs(res))),nonrounding_number_floor_budget_L1=float(tol*number_floor*sum(~new.holes)),gross_roundoff_allowance_L1=float(sum(rounding)))
  delta=spsolve(eye(len(res),format='csr')-dt*new.jacobian(events),-res)
  if not np.all(np.isfinite(delta)):raise RuntimeError('linear-number nonfinite correction')
  alpha=1.;lo=delta<0
  if np.any(lo):alpha=min(alpha,float(min(-.995*new.Z[lo]/delta[lo])))
  hi=ferm&(delta>0)
  if np.any(hi):alpha=min(alpha,float(min(.995*(new.measure[hi]-new.Z[hi])/delta[hi])))
  if alpha<=1e-18:raise RuntimeError('linear-number boundary blocked')
  base=float(np.linalg.norm(res/scale))
  for ls in range(24):
   trial=new.copy();trial.Z+=alpha*delta;rr=trial.Z-old.Z-dt*signs*trial.rhs(events);score=float(np.linalg.norm(rr/scale))
   if score<base*(1-1e-6*alpha)+1e-15:break
   alpha*=.5
  else:raise RuntimeError('linear-number merit line search')
  new=trial
 raise RuntimeError('linear-number iteration budget norm='+str(norm))

def implicit_step(events,state,dt,tol=2e-8,maxiter=60,number_floor=1e-14,predict=True,guess=None,zero_guess_occupation=1e-40):
 fraction=float(np.mean((~state.holes)&(state.Z<number_floor)));failure=None
 if fraction<=.75:
  try:
   new,info=logarithmic_step(events,state,dt,tol=tol,maxiter=min(maxiter,30),number_floor=number_floor,predict=predict,guess=guess,zero_guess_occupation=zero_guess_occupation);info['method']='log-number Newton';info['rare_coordinate_fraction']=fraction;return new,info
  except RuntimeError as exc:failure=str(exc)
 new,info=linear_step(events,state,dt,tol=tol,maxiter=max(60,maxiter),number_floor=number_floor,guess=guess,zero_guess_occupation=zero_guess_occupation);info['rare_coordinate_fraction']=fraction;info['log_route_failure']=failure;return new,info
