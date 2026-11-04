"""Phase-averaged actual 25-group quantum collision interface for GenericOrbit.

Local events conserve their own E(x). Their sum changes orbit-averaged gas
energy; this is balanced by scalar action covariance, never a radiation sink.
"""
import numpy as np
from scipy.sparse import diags
from reaction import full_events,ReactionEvents

def averaged_events(background,xs,weights,t,q,W,angles=2):
 xs=np.asarray(xs);phasew=np.asarray(weights);phasew=phasew/phasew.sum();locals=[]
 for x in xs:
  d=background.at(float(x));locals.append(full_events(d,t,q,W,angles=angles,source=d['current_source']))
 first=locals[0];index=np.concatenate([ev.index for ev in locals]);weights=np.concatenate([ev.weights for ev in locals]);coefficient=np.concatenate([w*ev.coefficient for w,ev in zip(phasew,locals)]);Eavg=np.einsum('k,ki->i',phasew,[ev.energy for ev in locals]);ev=ReactionEvents(index,weights,coefficient,first.measure,Eavg,first.eta)
 ev.groups=first.groups;ev.by=first.by;ev.q=np.asarray(q);ev.W=np.asarray(W);ev.t=t;ev.xs=xs;ev.phase_weights=phasew;ev.local_events=locals;ev.energy_average=Eavg;ev.omitted_by_parent=sum(w*a.omitted_by_parent for w,a in zip(phasew,locals));ev.included_by_parent=sum(w*a.included_by_parent for w,a in zip(phasew,locals));ev.local_energy_residual=max(a.energy_residual for a in locals)
 return ev

def number_rhs(events,Y):return np.asarray(events.S@events.flux(np.asarray(Y)/events.measure)).ravel()
def number_jacobian(events,Y):return diags(events.measure)@events.rhs_jacobian(np.asarray(Y)/events.measure)@diags(1/events.measure)

def covariance(events,Y):
 """Return physical action numerator <E C>-<E><C> in mu^5.

 d lnJ/dN = -3 + covariance/(omega H J), omega=2pi/period.
 Y is comoving number coordinates g W f/(2pi²); C is dY/dtau.
 Local 1<->2 collisions conserve *all* included particle energy.
 """
 f=np.asarray(Y)/events.measure;C=number_rhs(events,Y);local_energy=sum(w*float(ev.energy@np.asarray(ev.S@ev.flux(f)).ravel()) for w,ev in zip(events.phase_weights,events.local_events));value=events.t**3*(local_energy-float(events.energy_average@C))
 return float(value),dict(local_collision_energy=events.t**3*local_energy,averaged_gas_energy_change=events.t**3*float(events.energy_average@C),occupied_forward_omission=float(events.omitted_by_parent@f),included_forward_measure=float(events.included_by_parent@f))

def grid(order=8,qmax=80.):
 from numpy.polynomial.legendre import leggauss
 q=[];W=[]
 panels=[0.,.1,1.,5.,20.,float(qmax)]
 for left,right in zip(panels[:-1],panels[1:]):
  z,w=leggauss(order);nodes=(right+left)/2+(right-left)*z/2;q.extend(nodes);W.extend((right-left)*w*nodes*nodes/2)
 return np.array(q),np.array(W)
