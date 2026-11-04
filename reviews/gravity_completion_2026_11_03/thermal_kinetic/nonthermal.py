"""Frozen FD pair -> actual on-shell neutral scalars, maximum absorption."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource,numpy as np
from scipy.special import kv
from numpy.polynomial.legendre import leggauss
from neutral_rates import one
HERE=Path(__file__).resolve().parent
def phase_integral(M,m,t,n=96,MB=False):
 z,w=leggauss(n);u=40*(z+1);wu=40*w;ct,wt=leggauss(n);rm=M/t;r=m/t;en=np.sqrt(u*u+rm*rm);beta=math.sqrt(max(0,1-4*m*m/(M*M)))
 if MB:avg=np.exp(-en)
 else:
  e1=en[:,None]/2+u[:,None]*beta*ct[None,:]/2;e2=en[:,None]-e1
  p1=np.sqrt(np.maximum(0,e1*e1-r*r));p2=np.sqrt(np.maximum(0,e2*e2-r*r));f1=np.exp(-p1)/(1+np.exp(-p1));f2=np.exp(-p2)/(1+np.exp(-p2));avg=(f1*f2)@wt/2
 return float((wu*u*u/en)@avg)
def main(out):
 start=time.monotonic();stat=json.loads((HERE/'run_stationary_002/result.json').read_text());checks={};controls=[]
 for M in (1,10,100):
  ref=M*kv(1,M);got=phase_integral(M,.1,1,128,True);controls.append(dict(M_over_t=M,relative_MB_error=abs(got/ref-1)))
 checks['MB_detailed_balance_limit']=max(q['relative_MB_error'] for q in controls)<1e-10
 rows=[]
 for point in stat['points']:
  kind=point['kind'];mu=point['mu_GeV']
  for t in (.004,.003,.002,.001,.00064):
   branch=next(q for q in point['branches'] if q['mode']=='frozen_only' and q['t']==t);x=next(q['x'] for q in branch['extrema'] if q['minimum']);data=one(x,[t],{kind:mu});m=data['light_mass_over_mu'];totals={};parents=[]
   for n in (64,128):
    gamma=0
    for p in data['neutral_scalar_partial_widths']:
     M=p['mass_over_mu'];width=p['width_over_mu'];value=width*M*t*t/(2*math.pi**2)*phase_integral(M,m,t,n);gamma+=value
     if n==128:parents.append(dict(mass_over_mu=M,width_to_light_over_mu=width,inverse_reaction_density_mu4=value))
    totals[n]=gamma
   number=24*3*1.202056903159594/(4*math.pi**2)*t**3;loss=2*totals[128]/number;H=math.sqrt(math.pi**2*106.75/90)*(t*mu/.02)**2/2.435e18
   rows.append(dict(kind=kind,t=t,x=x,m_over_t=m/t,scalar_parent_count=len(parents),max_absorbing_loss_rate_GeV=loss*mu,max_absorbing_loss_over_H=loss*mu/H,quadrature_repeat_relative_error=abs(totals[64]/totals[128]-1) if totals[128]>1e-100 else 0,parents=parents))
 checks['quadrature_repeat']=max(q['quadrature_repeat_relative_error'] for q in rows)<.01
 result=dict(claim_id='TK08_NONTHERMAL_SCALAR_RESONANT_LOSS',checks={k:bool(v) for k,v in checks.items()},MB_controls=controls,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Frozen FD nonthermal pair->on-shell neutral-scalar inverse rates; every parent assumed irreversibly absorbed, so a maximum for this channel set only. Zero parent occupation, no stimulated parent factors, tree narrow widths, prescribed fixed-number minima. No all-channel loss bound, no field/abundance backreaction or actual neutral cascade completion.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
