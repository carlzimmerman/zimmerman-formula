"""Conservative moving-minimum loading followed by charged-source preparation."""
import json
from pathlib import Path
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
J=10.;d=.01;release=.0001

def ramp(z):return z**3*(10+z*(-15+6*z)),30*z*z*(1-z)**2

def drive(s,R):
 if s<=-R-release or s>=0:return 0.,0.
 if s<-release:
  z=(s+R+release)/R;v,dv=ramp(z);return v,dv/R
 v,dv=ramp((s+release)/release);return 1-v,-dv/release

def window(s,D):
 if s<=0 or s>=D+d:return 0.,0.
 if s<d:v,dv=ramp(s/d);return v,dv/d
 if s<=D:return 1.,0.
 v,dv=ramp((s-D)/d);return 1-v,-dv/d

def integrate(z,edges,R,D,tol=1e-11):
 hist=[];t=0.
 def rhs(t,z):
  x,y,vx,vy,s,v=z;f,df=drive(s,R);w,dw=window(s,D)
  return [vx,vy,-x+f,-y+f-3*w*y,v,((x+y-2*f)*df-1.5*dw*y*y)/J]
 for edge,step in edges:
  def event(t,z):return z[4]-edge
  event.terminal=True;event.direction=1
  sol=solve_ivp(rhs,(t,t+500),z,events=event,method='DOP853',rtol=tol,atol=tol*.05,max_step=step)
  if len(sol.t_events[0])!=1:raise RuntimeError('no crossing')
  z=sol.y[:,-1];t=sol.t[-1];hist.append(sol)
 return z,t,hist

def prep(R,tol=1e-11):
 z=np.array([0.,0.,0.,0.,-R-release,math.sqrt(12/J)])
 return integrate(z,[(-release,.1),(0.,release/12)],R,1.31,tol)

def pulse(z,R,D,tol=1e-11):return integrate(z,[(d,d/12),(D,.025),(D+d,d/12)],R,D,tol)

p=Path(__file__).parent
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def audit(hists,R,D):
 errors=[];symmetry=[];speed=[]
 for h in hists:
  for z in h.y.T:
   x,y,vx,vy,s,v=z;f,df=drive(s,R);w,dw=window(s,D)
   E=.5*(vx*vx+vy*vy+(x-f)**2+(y-f)**2+J*v*v)+1.5*w*y*y
   errors.append(abs(E-6));speed.append(v)
   if s<=0:symmetry.append(max(abs(x-y),abs(vx-vy)))
 return dict(total_energy_absolute_drift=max(errors),loading_symmetry_error=max(symmetry),minimum_clock_speed=min(speed))
rows=[]
for R in [50.,100.,200.]:
 z,t,h=prep(R)
 def obj(D):
  q,tt,hh=pulse(z,R,D)
  return (q[2]-q[1])**2+(q[3]+q[0])**2
 opt=minimize_scalar(obj,bounds=(1.25,1.38),method='bounded',options={'xatol':1e-13})
 check('width optimization success',opt.success)
 cases=[]
 for tol in [1e-11,2e-13]:
  z,t,h=prep(R,tol);q,tt,hh=pulse(z,R,float(opt.x),tol)
  E=.5*np.dot(q[:4],q[:4]);Q=2*(q[1]*q[2]-q[0]*q[3]);clock=.5*J*q[-1]**2
  a=audit(h+hh,R,float(opt.x))
  eta=1-Q/(2*E*math.sqrt(1+1e-6))
  check('source loaded from initially zero field',E>.99 and E<1.01)
  check('cold source',eta<5.001e-7)
  check('closed energy accounting',a['total_energy_absolute_drift']<2e-8)
  check('clock provides source energy',abs((6-clock)-E)<2e-8)
  check('symmetric loading fixes phase',a['loading_symmetry_error']<1e-12)
  check('clock crosses',a['minimum_clock_speed']>0)
  cases.append(dict(rtol=tol,release_state=z.tolist(),endpoint=q.tolist(),duration=t+tt,source_energy=E,clock_energy=clock,charge=Q,eta=eta,circular_residual=float(np.linalg.norm([q[2]-q[1],q[3]+q[0]])),**a))
 check('tolerance convergence',max(abs(np.array(cases[0]['endpoint'])-np.array(cases[1]['endpoint'])))<2e-7)
 rows.append(dict(rise_width=R,pulse_width=float(opt.x),runs=cases))
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,
         initial_state=dict(source_fields=[0,0],source_velocities=[0,0],clock_energy=6),
         non_claims=['Clock kinetic energy, displacement scale and coupling profiles supplied',
                     'No full-chain quantum fluctuation audit',
                     'No nonlinear spatial stability, cosmological abundance or halo selection'])
(p/'clock_loading_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_pass=out['all_pass'],checks=len(checks),rows=[dict(rise_width=r['rise_width'],pulse_width=r['pulse_width'],duration=r['runs'][-1]['duration'],source_energy=r['runs'][-1]['source_energy'],clock_energy=r['runs'][-1]['clock_energy'],eta=r['runs'][-1]['eta'],energy_error=r['runs'][-1]['total_energy_absolute_drift'],circular_residual=r['runs'][-1]['circular_residual']) for r in rows]),indent=2));assert out['all_pass']
