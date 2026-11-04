"""Phase combination for physical-number backends with explicit availability.

Every local backend retains its own collision energy. energy_average is the
phase-averaged gas energy vector, whose collision change feeds scalar-action
covariance; it is not a local conserved collision energy.
"""
import numpy as np
from scipy.sparse import csr_matrix

class AveragedNumberEvents:
 def __init__(self,local_events,phase_weights,xs=None):
  if not local_events:raise ValueError('no local number operators')
  self.local_events=list(local_events);w=np.asarray(phase_weights,float)
  if len(w)!=len(local_events) or np.any(w<0) or sum(w)<=0:raise ValueError('invalid phase weights')
  self.phase_weights=w/sum(w);first=local_events[0];self.measure=np.asarray(first.measure);self.eta=np.asarray(first.eta)
  if any(not np.array_equal(a.measure,self.measure) or not np.array_equal(a.eta,self.eta) for a in local_events):raise ValueError('phase measures/statistics differ')
  self.energy_average=np.einsum('k,ki->i',self.phase_weights,[a.energy for a in local_events]);self.energy=self.energy_average
  for name in ('groups','by','q','W','t'):
   if hasattr(first,name):setattr(self,name,getattr(first,name))
  self.xs=np.asarray(xs if xs is not None else [getattr(a,'x',np.nan) for a in local_events]);self.local_energy_residual=max(getattr(a,'local_energy_residual',getattr(a,'energy_residual',0.)) for a in local_events)
  self.has_forward_omission=all(hasattr(a,'omitted_by_parent') and hasattr(a,'included_by_parent') for a in local_events)
  if self.has_forward_omission:
   self.omitted_by_parent=sum(w*a.omitted_by_parent for w,a in zip(self.phase_weights,local_events));self.included_by_parent=sum(w*a.included_by_parent for w,a in zip(self.phase_weights,local_events))
 def number_rhs(self,f,availability=None):return np.einsum('k,ki->i',self.phase_weights,[a.number_rhs(f,availability) for a in self.local_events])
 def number_jacobian(self,f,availability=None):
  result=csr_matrix((len(self.measure),len(self.measure)))
  for w,a in zip(self.phase_weights,self.local_events):result=result+w*a.number_jacobian(f,availability)
  return result.tocsr()
 def number_gross(self,f,availability=None):return np.einsum('k,ki->i',self.phase_weights,[a.number_gross(f,availability) for a in self.local_events])
 def local_energy_rates(self,f,availability=None):return np.array([a.energy@a.number_rhs(f,availability) for a in self.local_events],float)
 def forward_omission(self,f):
  if not self.has_forward_omission:return dict(available=False)
  out=float(self.omitted_by_parent@f);inside=float(self.included_by_parent@f)
  return dict(available=True,occupied_forward_omitted=out,occupied_forward_included=inside,occupied_forward_omitted_fraction=out/max(out+inside,1e-300))

def averaged_number_events(local_events,phase_weights,xs=None):return AveragedNumberEvents(local_events,phase_weights,xs)
