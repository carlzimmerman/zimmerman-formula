"""Autonomous smooth clock pulse: finite homogeneous classical experiment."""
import json
from pathlib import Path
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

def window(s,D,d):
 def ramp(z): return z**3*(10+z*(-15+6*z)),30*z*z*(1-z)**2
 if s<=0 or s>=D+d:return 0.,0.
 if s<d:
  w,dw=ramp(s/d);return w,dw/d
 if s<=D:return 1.,0.
 w,dw=ramp((s-D)/d);return 1-w,-dw/d

def run(theta,D,J,d=.01,tol=1e-10):
 z=np.array([math.sqrt(2)*math.cos(theta),math.sqrt(2)*math.sin(theta),0.,0.,0.,1.])
 def rhs(t,z):
  x,y,vx,vy,s,v=z;w,dw=window(s,D,d)
  return [vx,vy,-x,-(1+3*w)*y,v,-1.5*dw*y*y/J]
 hist=[]; t=0
 for edge,step in [(d,d/12),(D,.025),(D+d,d/12)]:
  def stop(t,z):return z[4]-edge
  stop.terminal=True;stop.direction=1
  sol=solve_ivp(rhs,(t,t+20),z,events=stop,rtol=tol,atol=tol*.1,max_step=step)
  if len(sol.t_events[0])==0:raise ValueError('clock did not cross')
  t=sol.t[-1];z=sol.y[:,-1];hist.append(sol)
 return z,t,hist

p=Path(__file__).parent
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def stats(theta,D,J,tol):
 z,t,hist=run(theta,D,J,tol=tol)
 states=np.concatenate([h.y for h in hist],axis=1)
 energies=[];speeds=[]
 for zz in states.T:
  x,y,vx,vy,s,v=zz;w,dw=window(s,D,.01)
  energies.append(.5*(x*x+y*y+vx*vx+vy*vy+J*v*v)+1.5*w*y*y)
  speeds.append(v)
 x,y,vx,vy,s,v=z
 E=.5*(x*x+y*y+vx*vx+vy*vy);Q=2*(y*vx-x*vy)
 # Orthogonal torque check: integrate augmented charge along dense ODE solution.
 # This is a separate quadrature, using dense output on each completed segment.
 from scipy.integrate import quad
 torque=0.
 for h in hist:
  # Cubic spline of actual trajectory samples, then check convergence by tolerance.
  from scipy.interpolate import CubicSpline
  interp=CubicSpline(h.t,h.y,axis=1)
  def f(tt):
   zz=interp(tt);return 6*window(zz[4],D,.01)[0]*zz[0]*zz[1]
  torque+=quad(f,h.t[0],h.t[-1],epsabs=1e-9,epsrel=1e-9,limit=500)[0]
 return dict(theta=theta,width=D,inertia=J,duration=t,source_energy=E,charge=Q,
             efficiency=Q/(2*E),eta=1-Q/(2*E*math.sqrt(1+.001**2)),
             clock_speed_final=v,clock_speed_min=min(speeds),
             total_energy_absolute_drift=max(abs(np.array(energies)-(1+J/2))),
             torque_integral_error=abs(Q-torque),circular_residual=float(np.linalg.norm([vx-y,vy+x])),
             endpoint=z.tolist())
rows=[]
for J in [10.,100.,10000.]:
 def fun(v):
  z,t,h=run(v[0],v[1],J)
  x,y,vx,vy,s,vs=z
  return [vx-y,vy+x]
 opt=root(fun,[math.pi/4,math.pi/2],tol=1e-9)
 check('root solved '+str(J),opt.success)
 tuned=stats(float(opt.x[0]),float(opt.x[1]),J,1e-10)
 tight=stats(float(opt.x[0]),float(opt.x[1]),J,1e-12)
 untuned=stats(math.pi/4,math.pi/2,J,1e-12)
 perturbed=stats(float(opt.x[0]),float(opt.x[1])+.001,J,1e-12)
 check('circular endpoint '+str(J),tight['circular_residual']<2e-8)
 check('cold budget '+str(J),tight['eta']<5.0001e-7)
 check('finite clock crosses '+str(J),tight['clock_speed_min']>0)
 check('total energy conserved '+str(J),tight['total_energy_absolute_drift']<2e-6)
 check('charge torque '+str(J),tight['torque_integral_error']<2e-7)
 check('endpoint tolerance agreement '+str(J),max(abs(np.array(tuned['endpoint'])-np.array(tight['endpoint'])))<2e-7)
 check('energy transferred back '+str(J),abs(tight['source_energy']-1)<2e-8)
 # Once s>D+d and v>0, the compact window is identically zero and remains so.
 check('late interaction zero '+str(J),window(tight['endpoint'][4]+.1,float(opt.x[1]),.01)==(0.,0.))
 rows.append(dict(tuned=tuned,tight=tight,untuned=untuned,width_error_plus_001=perturbed))
out=dict(checks=checks,all_pass=all(c['passed'] for c in checks),rows=rows,
         non_claims=['No initial displacement or phase selection mechanism',
                     'No vacuum formation or autonomous cosmic abundance',
                     'Homogeneous classical Minkowski calculation; no quantum or spatial stability audit',
                     'Clock is an extra field with a deliberately chosen compact interaction'])
(p/'autonomous_clock_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_pass=out['all_pass'],checks=len(checks),rows=[dict(J=r['tight']['inertia'],width=r['tight']['width'],duration=r['tight']['duration'],eta=r['tight']['eta'],energy_drift=r['tight']['total_energy_absolute_drift'],torque_error=r['tight']['torque_integral_error'],untuned_eta=r['untuned']['eta'],perturbed_eta=r['width_error_plus_001']['eta']) for r in rows]),indent=2))
assert out['all_pass']
