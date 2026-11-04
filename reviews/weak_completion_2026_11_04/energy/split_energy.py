"""Positive population / discrete-energy action split, with independent work.

No species count is fixed here. The injected model and number-operator factory
must share masses, derivatives, spin degeneracies and occupation conventions.
The collision substep conserves its physical Hamiltonian by solving the action
from E,Y, while expansion follows J'=−3J at fixed comoving populations. FRW
work is independently quadrature-integrated, never assigned from delta E.
"""
import sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/initial_solver'))
from log_number import QuantumState,implicit_step

def expansion_work(orbit):
 return 3*float(orbit['weights']@(orbit['kin2']+orbit['gas']['rho']+orbit['gas']['pressure']))

def covariance(events,state):
 C=np.array([state.rhs(local) for local in events.local_events]);avg=events.phase_weights@C;ee=np.array([local.energy for local in events.local_events]);de=ee-events.energy_average[None,:]
 return events.t**3*float(np.sum(events.phase_weights[:,None]*de*(C-avg))),avg

def expansion(model,N,state,J,dN):
 Y=state.numbers();a=model.orbit(N,Y,J=J)
 b=model.orbit(N+dN/2,Y,J=J*math.exp(-3*dN/2))
 c=model.orbit(N+dN,Y,J=J*math.exp(-3*dN))
 # This quadrature is independent of the reconstructed energy difference.
 work=dN*(expansion_work(a)+4*expansion_work(b)+expansion_work(c))/6
 return J*math.exp(-3*dN),c,float(work),dict(energy_change=float(c['E']-a['E']),work=float(work),independent_residual=float(c['E']-a['E']+work))

class MidpointNumberOperator:
 """Positive-domain implicit-midpoint population diagnostic, not unconditional.

 The Newton unknown remains the physical endpoint. A stiff interval may have
 no endpoint in the physical domain; that is a rejected step, not clipping.
 """
 def __init__(self,operator,oldstate):self.operator=operator;self.__dict__.update({k:v for k,v in operator.__dict__.items()});self.f0,self.a0=oldstate.arrays()
 def number_rhs(self,f,availability=None):
  a=1+self.eta*f if availability is None else availability;return self.operator.number_rhs((self.f0+f)/2,(self.a0+a)/2)
 def number_jacobian(self,f,availability=None):
  a=1+self.eta*f if availability is None else availability;return self.operator.number_jacobian((self.f0+f)/2,(self.a0+a)/2)/2
 def number_gross(self,f,availability=None):
  a=1+self.eta*f if availability is None else availability;return self.operator.number_gross((self.f0+f)/2,(self.a0+a)/2)

def collision(model,background,operator_factory,N,state,orbit,dN,geometry='old',population='BE',max_outer=5,outer_tol=2e-5):
 """Fixed-N collision with optional self-consistent midpoint orbit geometry.

 Old geometry is first-order. Midpoint geometry iterates the midpoint Y on
 the same E surface and always re-solves from the original old state, rather
 than accumulating fictitious extra reactions during nonlinear iteration.
 """
 oldY=state.numbers();energy=float(orbit['E']);geoorbit=orbit;previousY=None;previousJ=None;iterations=[];H=model.hubble(N);t=orbit.get('t',None)
 if t is None:
  # Model interface already fixes the hidden comoving temperature convention.
  from precise_orbit import T0
  t=T0*math.exp(-N)
 for outer in range(1 if geometry=='old' else max_outer):
  events=operator_factory(background,geoorbit['xs'],geoorbit['weights'],t,model.q,model.W)
  solve_events=events if population=='BE' else MidpointNumberOperator(events,state)
  nextstate,info=implicit_step(solve_events,state,dN/H,tol=2e-8,maxiter=60,number_floor=1e-14)
  Yn=nextstate.numbers();neworbit=model.orbit(N,Yn,E=energy);relative=None if previousY is None else float(sum(abs(Yn-previousY))/max(sum(abs(Yn)),1e-300));action_relative=None if previousJ is None else abs(neworbit['J']-previousJ)/max(orbit['J'],neworbit['J'],1e-300);iterations.append(dict(outer=outer+1,population_newton=info,relative_change=relative,action_relative_change=action_relative,action=float(neworbit['J']),minimum=float(neworbit['minimum'])))
  if geometry=='old' or (previousY is not None and relative<outer_tol and action_relative<outer_tol):break
  previousY=Yn.copy();previousJ=float(neworbit['J']);geoorbit=model.orbit(N,(oldY+Yn)/2,E=energy)
 else:raise RuntimeError('mid-orbit fixed point did not converge')
 f,a=nextstate.arrays();localenergy=np.array([local.energy@nextstate.rhs(local) for local in events.local_events]);gross=nextstate.gross(events);scale=max(float(max(events.energy))*sum(gross),1e-300)
 return nextstate,float(neworbit['J']),neworbit,dict(outer_iterations=iterations,operator_geometry=geometry,population_scheme=population,collision_energy_change=float(neworbit['E']-energy),local_energy_relative=float(max(abs(localenergy))/scale),entropy_change=float(nextstate.entropy()-state.entropy()),min_f=float(min(f)),max_fermion_f=float(max(f[model.eta<0])),number_change_L1=float(sum(abs(Yn-oldY))),physical_number_balance_L1=float(sum(abs(Yn-oldY-dN/H*nextstate.rhs(solve_events)))))

def step(model,background,operator_factory,N,state,J,dN,geometry='midpoint',population='BE',max_outer=5,outer_tol=2e-5):
 Ja,oa,wa,da=expansion(model,N,state,J,dN/2)
 ns,Jb,ob,db=collision(model,background,operator_factory,N+dN/2,state,oa,dN,geometry,population,max_outer,outer_tol)
 Jn,on,wb,dc=expansion(model,N+dN/2,ns,Jb,dN/2)
 return ns,Jn,on,float(wa+wb),dict(first_expansion=da,collision=db,second_expansion=dc,independent_step_energy_work=float(on['E']-model.orbit(N,state.numbers(),J=J)['E']+wa+wb))
