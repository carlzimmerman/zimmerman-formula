"""Event-local entropy-dissipating implicit sweeps for extreme soft-bin stiffness.

Frozen quantum.py is imported unchanged. This splitting solver advances the
same finite ODE, with a finite-step splitting error that must be tested.
"""
import math
import numpy as np
from scipy.optimize import brentq
from quantum import *

def event_sweep(events,f,dt,reverse=False):
 """One backward-Euler scalar-extent update per event, without state clipping.

 Every event update conserves its stoichiometric invariants and has positive
 entropy production. Event order and dt are discretization parameters.
 No giant unphysical bath floor is required at the exactly empty state.
 """
 out=np.asarray(f,float).copy();order=range(len(events.coefficient)-1,-1,-1) if reverse else range(len(events.coefficient));solves=0
 for r in order:
  idx=events.index[r];weights=events.weights[r];s=events.stoich[r];nu=events.measure[idx];eta=events.eta[idx];base=out[idx].copy()
  if len(set(idx[weights>0]))!=sum(weights>0):
   raise ValueError('event_sweep currently requires distinct nonzero-weight nodes')
  def factor(z):
   v=base+s*z/nu;av=1+eta*v
   # Roundoff only inside trial function at the exact analytic endpoint.
   v=np.maximum(v,0.);av=np.maximum(av,0.)
   return v[0]*float(np.prod(av[1:]**weights[1:]))-av[0]*float(np.prod(v[1:]**weights[1:]))
  value=factor(0.)
  if value==0.:continue
  upper=math.inf;lower=-math.inf
  for j in range(5):
   if s[j]>0:
    lower=max(lower,-base[j]*nu[j]/s[j])
    if eta[j]<0:upper=min(upper,(1-base[j])*nu[j]/s[j])
   elif s[j]<0:
    upper=min(upper,-base[j]*nu[j]/s[j])
    if eta[j]<0:lower=max(lower,(1-base[j])*nu[j]/s[j])
  edge=upper if value>0 else lower
  if edge==0.:continue
  if not math.isfinite(edge):raise RuntimeError('unbounded event extent')
  scale=abs(edge);sign=1 if value>0 else -1;lam=dt*events.coefficient[r]/scale
  def residual(a):return sign*a-lam*factor(sign*a*scale)
  # At the allowed endpoint the original-sign forward flux is zero or
  # reversed. Keeping its exact endpoint is necessary for arbitrarily stiff
  # Pauli filling; Brent never evaluates outside the physical interval.
  root=brentq(residual,0.,1.,xtol=2e-14,rtol=1e-14,maxiter=100)
  extent=sign*root*scale
  # Assign each nonzero stoichiometric node once; zero interpolation weights
  # can share an unused index without changing the update.
  for j in range(5):
   if s[j]!=0:out[idx[j]]=base[j]+s[j]*extent/nu[j]
  solves+=1
 if min(out)<-1e-13 or max(out[events.eta<0])>1+1e-13:raise RuntimeError('scalar extent domain error')
 return out,dict(solves=solves)

def symmetric_sweep(events,f,dt):
 first,a=event_sweep(events,f,dt/2,False)
 last,b=event_sweep(events,first,dt/2,True)
 return last,dict(solves=a['solves']+b['solves'])
