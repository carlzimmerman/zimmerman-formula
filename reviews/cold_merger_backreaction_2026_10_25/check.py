import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 B=1e-4;turn=math.sqrt(24)
 # X=turn*sin(theta) removes the turning-point quadrature singularity.
 def integrand(theta):
  x=turn*math.sin(theta);return turn*math.cos(theta)/math.sqrt(2*(-.2+1/math.sqrt(1+x*x)))
 P=4*quad(integrand,0,math.pi/2,epsabs=1e-10)[0]
 def potential(q,d):
  s=np.sin(q/2)**2;f=1-s;am1=s/(np.sqrt(f)*(1+np.sqrt(f)))
  return (-4*s+14*s*s)/f**2+d*am1
 def force(q,d):
  x=1/np.cos(q/2);return (40*x**3-48*x+d)*(.5*x*np.tan(q/2))
 def run(T,tol,seed=1e-6,cycles=30):
  M=B*T*T
  def fun(t,z):
   q,p,x,v=z;d=40+16*(1+x*x)**(-2.5);dp=-80*x*(1+x*x)**(-3.5)
   s=math.sin(q/2)**2;am1=s/(math.sqrt(1-s)*(1+math.sqrt(1-s)))
   feedback=dp*am1*(-1 if a.mutate else 1)
   return [p,-force(q,d),v,(-B*x/(1+x*x)**1.5-feedback)/M]
  ts=np.linspace(0,cycles*P*T,12001)
  sol=solve_ivp(fun,[0,ts[-1]],[seed,0,turn,0],t_eval=ts,rtol=tol,atol=tol*1e-3,method='DOP853')
  assert sol.success
  q,p,x,v=sol.y;d=40+16*(1+x*x)**(-2.5)
  ef=.5*p*p+potential(q,d);eo=.5*M*v*v-B/np.sqrt(1+x*x);h=ef+eo
  err=float(max(abs(h-h[0])))
  assert err<2e-10,('total energy / backreaction sign',T,seed,err)
  assert max(ef)<=h[0]+B+2e-10
  return dict(T=T,cycles=cycles,seed=seed,initial_field_energy=float(ef[0]),final_field_energy=float(ef[-1]),peak_field_energy=float(max(ef)),orbital_energy_loss=float(eo[0]-eo[-1]),energy_error=err,field_budget=float(h[0]+B),max_abs_q=float(max(abs(q))))
 control=run(.3,2e-11,.01,2)
 runs=[]
 for T in [.03,.1,.3,1.,3.,10.]:
  base=run(T,2e-10);tight=run(T,2e-12)
  assert abs(base['final_field_energy']-tight['final_field_energy'])<max(1e-12,1e-3*abs(tight['final_field_energy']))
  runs.append(dict(base=base,tight=tight))
 zero=run(.3,2e-10,0.,2);assert zero['peak_field_energy']==0
 gas=json.load(open('reviews/cold_filter_reality_2026_10_25/run_fixed/result.json'))['cluster_rows']
 retention=[]
 for r in gas:
  if r['HJ']!=1.8e-18:continue
  ratio=math.sqrt(23.04/(r['d']-8))
  assert ratio<1
  retention.append(dict(name=r['name'],inner_X=r['inner_X'],d=r['d'],outer_over_inner_mass=ratio,necessary_lapse_ratio_below=ratio,escape_speed_over_c=math.sqrt(1-ratio*ratio),escape_energy_fraction=1-ratio,required_log_lapse_depth=-math.log(ratio)))
 assert len(retention)==35
 summary=dict(uncoupled_period_over_T=P,retention_cases=35,required_log_lapse_range=[min(r['required_log_lapse_depth'] for r in retention),max(r['required_log_lapse_depth'] for r in retention)],escape_speed_range=[min(r['escape_speed_over_c'] for r in retention),max(r['escape_speed_over_c'] for r in retention)],escape_energy_fraction_range=[min(r['escape_energy_fraction'] for r in retention),max(r['escape_energy_fraction'] for r in retention)])
 result=dict(summary=summary,control=control,runs=runs,zero=zero,retention=retention)
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['summary','control','runs']},indent=2))
if __name__=='__main__':main()
