"""Hamiltonian mass-shell cold assembly; prescribed baryonic ramp."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import root
p=Path(__file__).parent

def continuum(target):
 x=np.linspace(1e-6,1,600);Rguess=2.;guess=np.array([2.5*x**3-1.5*x**5,7.5*(1-x*x)/8]);previous=1.
 for beta in [1.,.7,.5,.3,.2,.1]:
  scale=np.sqrt(previous/beta);Rguess*=scale;guess[1]/=scale**3
  def fun(t,y,a):
   R=a[0];r=R*t;q=y[0]/r**2
   return np.array([R*r*r*y[1],R/.01*(q*q/(1-q)-beta*r/(1+r*r)**1.5)])
  def bc(a,b,z):return np.array([a[0]-a[1]*(z[0]*1e-6)**3/3,b[0]-1,b[1]])
  sol=solve_bvp(fun,bc,x,guess,p=[Rguess],tol=2e-8,max_nodes=30000)
  if sol.status:raise ValueError('BVP failure')
  if beta==target:
   xx=np.linspace(1e-6,1,10001);return sol.sol(xx)[0],xx*sol.p[0]
  guess=sol.sol(x);Rguess=sol.p[0];previous=beta
backgrounds={b:continuum(b) for b in [.1,1.]}
rows=[]
for N,dt in [(64,.002),(128,.001)]:
 dm=1/N;m=np.arange(1,N+1)*dm;w=np.full(N,dm);w[-1]=dm/2
 def acceleration(r,beta):
  volumes=np.diff(np.r_[0,r**3])/3
  if min(volumes)<=0 or min(r*r-m)<=0:raise ValueError('shell crossing or q cap')
  rho=dm/volumes;pressure=.01*rho*rho/2
  return r*r*(pressure-np.r_[pressure[1:],0])/w+(m/r**2)**2/(1-m/r**2)-beta*r/(1+r*r)**1.5
 def energy(r,v,beta):
  volumes=np.diff(np.r_[0,r**3])/3
  field=np.sum(w*(np.sqrt(m)*np.arctanh(np.sqrt(m)/r)-m/r))
  pressure=.005*np.sum(dm*dm/volumes)
  baryon=-np.sum(w/np.sqrt(1+r*r))-.5*dm
  return float(.5*np.sum(w*v*v)+field+pressure+beta*baryon),float(baryon)
 eq={};residuals={}
 for beta in [.1,1.]:
  mm,rr=backgrounds[beta];initial=np.interp(m,mm,rr)
  solution=root(lambda r:acceleration(r,beta),initial,tol=1e-10)
  if not solution.success or max(abs(acceleration(solution.x,beta)))>1e-7:raise ValueError('discrete equilibrium failure')
  eq[beta]=solution.x;residuals[str(beta)]=float(max(abs(acceleration(solution.x,beta))))
 # Independent finite difference of the complete discrete energy.
 r=eq[.1]*1.001;direction=np.sin(np.arange(N)+.4);eps=1e-6
 numerical=(energy(r+eps*direction,np.zeros(N),.1)[0]-energy(r-eps*direction,np.zeros(N),.1)[0])/(2*eps)
 analytic=-np.sum(w*acceleration(r,.1)*direction);force_error=abs(numerical-analytic)/max(abs(analytic),1e-8)
 for duration in [20.,100.,400.]:
  steps=int(round(duration/dt));h=duration/steps;r=eq[.1].copy();v=np.zeros(N);work=0.;E0,_=energy(r,v,.1);min_gap=np.inf
  def ramp(t):
   s=min(max(t/duration,0),1);f=10*s**3-15*s**4+6*s**5;der=(30*s*s-60*s**3+30*s**4)/duration
   return .1+.9*f,.9*der
  a=acceleration(r,.1)
  for k in range(steps):
   b0,db0=ramp(k*h);b1,db1=ramp((k+1)*h)
   B0=-np.sum(w/np.sqrt(1+r*r))-.5*dm
   v+=.5*h*a;r+=h*v;a=acceleration(r,b1);v+=.5*h*a
   B1=-np.sum(w/np.sqrt(1+r*r))-.5*dm;work+=.5*h*(db0*B0+db1*B1)
   min_gap=min(min_gap,float(min(np.diff(np.r_[0,r]))))
  Ef,_=energy(r,v,1.);Eeq,_=energy(eq[1.],np.zeros(N),1.)
  rows.append(dict(N=N,dt=h,duration=duration,equilibrium_residuals=residuals,force_derivative_error=force_error,work_residual=Ef-E0-work,excitation_energy=Ef-Eeq,kinetic_energy=float(.5*np.sum(w*v*v)),relative_position_rms=float(np.sqrt(np.sum(w*(r-eq[1.])**2)/np.sum(w*eq[1.]**2))),minimum_gap=min_gap,final_edge=float(r[-1]),equilibrium_edge=float(eq[1.][-1])))
checks=dict(force_derivative=all(r['force_derivative_error']<1e-3 for r in rows),work=all(abs(r['work_residual'])<1e-5 for r in rows),ordered=all(r['minimum_gap']>0 for r in rows),slower_less_excitation=all(all(y<x for x,y in zip([r['excitation_energy'] for r in rows if r['N']==n],[r['excitation_energy'] for r in rows if r['N']==n][1:])) for n in [64,128]))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='cold spherical discrete shell dynamics, beta .1 to1, externally prescribed work; no primordial formation or nonspherical stability')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
