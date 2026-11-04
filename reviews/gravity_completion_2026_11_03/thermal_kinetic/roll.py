"""Bounded first collisionless roll, expanding explicit initial xi=.02 bath."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from stationary import frozen
HERE=Path(__file__).resolve().parent
def main(out):
 start=time.monotonic();stationary=json.loads((HERE/'run_stationary_002/result.json').read_text());spins=json.loads((HERE.parent/'thermal/run_static_001/result.json').read_text());rows=[]
 for point in stationary['points']:
  kind=point['kind'];mu=point['mu_GeV'];spin=next(p for p in spins['points'] if p['kind']==kind)['spins'][0];t0=spin['TD_over_mu'];x0=spin['X_over_mu'];w0=math.sqrt(-point['origin_curvature']/62)
  grid=np.array(point['grid']);vv=np.array(point['T0_potential_mu4']);v=CubicSpline(grid,vv,bc_type=((1,point['origin_force']),(2,0)))
  def Hbar(t):return math.sqrt(math.pi**2*106.75/90)*(t*mu/.02)**2/2.435e18/(mu*w0)
  def deriv(u,y):
   x,vel,t,diss=y;rho,f,p=frozen(x,t);h=Hbar(t)
   return [vel,-3*h*vel-(float(v(x,1))+f)/(62*w0*w0),-h*t,3*h*(62*w0*w0*vel*vel+rho+p)]
  result=[]
  for rtol in (1e-8,1e-10):
   sol=solve_ivp(deriv,[0,250],[x0,0,t0,0],rtol=rtol,atol=rtol*1e-3,max_step=.1,dense_output=True)
   uu=np.linspace(0,250,5001);yy=sol.sol(uu);ener=[]
   for x,vel,t,diss in yy.T:ener.append(31*w0*w0*vel*vel+float(v(x))+frozen(x,t)[0]+diss)
   initial=ener[0];energy_scale=max(abs(float(v(x0))),frozen(x0,t0)[0],1e-20);error=max(abs(e-initial) for e in ener)/energy_scale
   result.append(dict(rtol=rtol,success=bool(sol.success),nfev=sol.nfev,min_x=float(min(yy[0])),max_x=float(max(yy[0])),final_x=float(yy[0,-1]),fractional_cooling=1-float(yy[2,-1]/t0),energy_plus_integrated_damping_error_relative_to_initial_particle_energy=error))
  rows.append(dict(kind=kind,mu_GeV=mu,initial_x=x0,initial_Tc_over_mu=t0,initial_xi=.02,initial_velocity=0,origin_roll_rate_GeV=w0*mu,initial_H_over_roll=Hbar(t0),duration_GeV_inverse=250/(mu*w0),controls=result,trajectory=[dict(u=float(u),x=float(x),dx_du=float(vel),Tc_over_mu=float(t)) for u,(x,vel,t,diss) in zip(uu[::25],yy.T[::25])]))
 checks={'integrations_completed':all(q['success'] for p in rows for q in p['controls']),'first_roll_stays_positive_and_bounded':all(q['min_x']>0 and q['max_x']<10 for p in rows for q in p['controls']),'particle_field_energy_exchange':all(q['energy_plus_integrated_damping_error_relative_to_initial_particle_energy']<1e-6 for p in rows for q in p['controls']),'integration_tolerance_repeat':all(abs(p['controls'][0]['max_x']-p['controls'][1]['max_x'])<1e-5 for p in rows)}
 result=dict(claim_id='TK08_FIRST_COLLISIONLESS_ROLL',checks=checks,points=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Conditional collisionless homogeneous first 250 origin-roll times, initial field position chosen from equilibrium spinodal, zero initial velocity, frozen charged FD population and explicit expanding visible radiation xi=.02. Other massive hidden species omitted. This does not reach outer-vacuum reappearance over a Hubble cooling interval, solve collisions or derive the initial distribution.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
