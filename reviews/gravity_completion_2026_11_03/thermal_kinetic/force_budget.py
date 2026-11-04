"""Necessary charged number for stationary trapping in prescribed force family."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource,numpy as np
from scipy.interpolate import CubicSpline
from stationary import E,G,A0,DG,thermal_force,eq_light_force
HERE=Path(__file__).resolve().parent
def perparticle_bound(x):
 k=E/2;m=k*x;q=-E*A0/2;gg=5*G;split=E/62
 pp=np.array([[m*m+q*q+split,-m*q],[-m*q,q*q]])+np.outer([gg*A0,-gg*x],[gg*A0,-gg*x])
 dp=np.array([[2*m*k,-k*q-gg*gg*A0],[-k*q-gg*gg*A0,2*gg*gg*x]])
 # The remaining physical minus-block eigenvalue is m^2+q^2; its zero is Goldstone.
 mp=math.sqrt(np.linalg.eigvalsh(pp).min());pm=math.sqrt(m*m+q*q)
 ppbound=np.linalg.norm(dp,2)/(2*mp);pmbound=abs(m*k)/pm
 fbound=np.linalg.norm(DG,2);vbound=gg*x/math.sqrt(A0*A0+x*x)
 return max(ppbound,pmbound,fbound,vbound)
def main(out):
 start=time.monotonic();stat=json.loads((HERE/'run_stationary_002/result.json').read_text());charged=json.loads((HERE.parent/'run_charged/result.json').read_text());rows=[];t=.002;xi=.02;entropy=2*math.pi**2*106.75/45*(t/xi)**3
 grid=np.unique(np.r_[0,np.geomspace(1e-10,1,150),np.linspace(1,200,1001)])
 for point in stat['points']:
  spline=CubicSpline(point['grid'],point['T0_potential_mu4'],bc_type=((1,point['origin_force']),(2,0)))
  ff=np.array([float(spline(x,1))+thermal_force(x,t,n=256)-eq_light_force(x,t) for x in grid]);bounds=np.array([perparticle_bound(x) for x in grid]);need=np.maximum(-ff,0)/bounds/entropy;i=int(np.argmin(need));charge=next(q for q in charged['cases'] if q['name']==point['kind']);gate=.1*.44e-9/charge['lightest_charged_GeV']
  rows.append(dict(kind=point['kind'],Tc_over_mu=t,grid_count=len(grid),all_baseline_forces_outward=bool(np.all(ff<0)),smallest_required_Y=float(need[i]),at_x=float(grid[i]),force_mu3=float(ff[i]),per_particle_mass_slope_bound=float(bounds[i]),charged_relic_10percent_Y_gate=gate,required_Y_over_10percent_gate=float(need[i]/gate),maximum_baseline_force=float(ff.max()),minimum_slope_bound=float(bounds.min()),maximum_slope_bound=float(bounds.max())))
 checks={'baseline_outward_on_grid':all(q['all_baseline_forces_outward'] for q in rows),'force_required_Y_exceeds_gate':all(q['required_Y_over_10percent_gate']>1e4 for q in rows)}
 result=dict(claim_id='TK08_TRAPPING_CHARGED_NUMBER_BUDGET',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Necessary charged number for a stationary point at Tc=.002mu, leadingglobalT0+ideal-equilibriumother-species force, finite grid0<=x<=200. All charged scalar/fermion/vector particles bounded bypointwise mass-slope norms, independent of momentum or statistics. Neutralfrozen daughters and nonstationary capture excluded; noallhistoryexclusion. TheDMgate rhoDM/s=.44e-9GeV is an explicit comparisonbenchmark.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
