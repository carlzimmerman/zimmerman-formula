"""Bounded adaptive collision advance in stable positive hole coordinates.

Substeps solve the same fixed-background ODE. They are recorded explicitly;
the result is not claimed to be one giant backward-Euler step. Integrated
physical-number flux is returned for conservative field/action bookkeeping.
"""
import numpy as np
from log_holes import QuantumState,implicit_step as one_step

def implicit_step(events,state,dt,tol=2e-8,maxiter=35):
 current=state.copy();elapsed=0.;step=dt;accepted=0;rejected=0;iterations=0;minimum_step=dt;messages=[];integral=np.zeros(len(state.Z));roundoff=0.;minimum_alpha=1.
 while elapsed<dt*(1-1e-14):
  step=min(step,dt-elapsed)
  try:new,diag=one_step(events,current,step,tol=tol,maxiter=maxiter)
  except RuntimeError as exc:
   rejected+=1;messages.append(str(exc));step*=.25
   if rejected>32 or step<dt*1e-10:raise RuntimeError('adaptive holes exhausted: '+str(exc))
   continue
  F,R,_,_=new.products(events);rhs=new.rhs(events);integral+=step*rhs;gross=np.asarray(abs(events.S)@(events.coefficient*(F+R))).ravel();roundoff+=float(32*np.finfo(float).eps*step*sum(gross));current=new;elapsed+=step;accepted+=1;iterations+=diag['iterations'];minimum_step=min(minimum_step,step);minimum_alpha=min(minimum_alpha,diag.get('minimum_line_alpha',1.));step*=1.5
  if accepted>512:raise RuntimeError('adaptive holes internal step budget')
 return current,dict(method='adaptive log number/hole Newton',iterations=iterations,residual=None,internal_steps=accepted,rejected_internal_steps=rejected,minimum_internal_dt=minimum_step,minimum_line_alpha=minimum_alpha,failed_attempts=messages,integrated_number_flux=integral.tolist(),integrated_gross_roundoff_allowance_L1=roundoff)
