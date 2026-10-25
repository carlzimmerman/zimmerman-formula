import argparse,json,math
from pathlib import Path
import numpy as np
import sympy as S
from scipy.integrate import solve_ivp

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 rows=json.load(open('reviews/cold_local_production_2026_10_25/run/result.json'))['rows']
 wave=json.load(open('reviews/cold_wave_relaxation_2026_10_25/run/result.json'))['rows']
 speed={(r['name'],r['model'],r['footing'],r['shell']):r['sigma_kms'] for r in wave if r['sigma_factor']==1}
 groups={}
 for r in rows:groups.setdefault((r['name'],r['model'],r['footing']),[]).append(r)
 X=[.1,.2,.3,.5,.7,1.];budgets=[]
 for key,rs in groups.items():
  if len(rs)!=5:continue
  vals=dict(required=0.,sudden=0.,slow=0.,gas_kinetic=0.)
  for r in rs:
   j=r['shell'];vol=X[j+1]**3-X[j]**3;d=r['gas_d'];v=speed[(*key,j)]
   vals['required']+=vol*r['required_source_over_D']
   vals['sudden']+=vol*(-.4+d*(math.sqrt(6/5)-1))
   vals['slow']+=vol*r['produced_energy_over_D']
   vals['gas_kinetic']+=vol*.5*d*(v/299792.458)**2
  budgets.append(dict(name=key[0],model=key[1],footing=key[2],**vals,sudden_fraction=vals['sudden']/vals['required'],slow_fraction=vals['slow']/vals['required'],kinetic_fraction=vals['gas_kinetic']/vals['required']))
 assert len(budgets)==28
 def mat(w,phase):return np.array([[math.cos(phase),math.sin(phase)/w],[-w*math.sin(phase),math.cos(phase)]])
 wl,wh=2.,math.sqrt(12)
 quarter=mat(wl,math.pi/2)@mat(wh,math.pi/2)
 half=mat(wl,math.pi)@mat(wh,math.pi)
 assert np.allclose(quarter,np.diag([-wh/wl,-wl/wh]),atol=1e-14)
 assert np.allclose(half,np.eye(2),atol=1e-14)
 w0=math.sqrt(8);floquet=[]
 for ratio in [.1,.5,1.,2.,3.]:
  om=ratio*w0;period=2*math.pi/om
  def fun(t,z):return (np.array([[0.,1.],[-(8+4*math.sin(om*t)),0.]])@z.reshape(2,2)).ravel()
  sol=solve_ivp(fun,[0,period],np.eye(2).ravel(),rtol=2e-11,atol=1e-12,method='DOP853')
  assert sol.success
  M=sol.y[:,-1].reshape(2,2);det=float(np.linalg.det(M));assert abs(det-1)<1e-7
  floquet.append(dict(frequency_ratio=ratio,determinant=det,spectral_radius=float(max(abs(np.linalg.eigvals(M))))))
 q,d=S.symbols('q d',real=True);f=S.cos(q/2)**2;y=4*S.sin(q/2)**2
 V=(1+(y-1)**2)/f**2+d/S.sqrt(f)
 force=S.lambdify((q,d),S.diff(V,q),'numpy')
 # Stable expression for A-1 near zero; W-2 evaluated algebraically.
 def excess(q,d):
  s=np.sin(q/2)**2;return ((1+(4*s-1)**2)-2*(1-s)**2)/(1-s)**2+d*s/(np.sqrt(1-s)*(1+np.sqrt(1-s)))
 def run(ratio,tol,seed=1e-6):
  om=ratio*w0;period=2*math.pi/om
  def fun(t,z):
   q,p,work=z;dd=40+16*math.sin(om*t);ds=16*om*math.cos(om*t);s=math.sin(q/2)**2
   am1=s/(math.sqrt(1-s)*(1+math.sqrt(1-s)))
   return [p,-force(q,dd),(-1 if a.mutate else 1)*ds*am1]
  t=np.linspace(0,80*period,16001)
  sol=solve_ivp(fun,[0,t[-1]],[seed,0,0],t_eval=t,method='DOP853',rtol=tol,atol=tol*.01)
  assert sol.success
  q,p,work=sol.y;energy=.5*p*p+excess(q,40+16*np.sin(om*t));res=float(max(abs(energy-energy[0]-work)))
  assert res<1e-7,('energy ledger',ratio,res)
  return dict(frequency_ratio=ratio,initial_energy=float(energy[0]),final_energy=float(energy[-1]),peak_energy=float(max(energy)),max_abs_q=float(max(abs(q))),ledger_error=res)
 nonlinear=[]
 for ratio in [1.,2.,3.]:
  base=run(ratio,2e-10);tight=run(ratio,2e-12)
  assert abs(base['final_energy']-tight['final_energy'])<max(1e-10,1e-4*abs(tight['final_energy']))
  nonlinear.append(dict(base=base,tight=tight))
 zero=run(2.,2e-10,0.);assert zero['max_abs_q']==0
 PC=3.085677581491367e16;omegaunit=299792458.**2/(1500*PC*1000)/(2.4*math.sqrt(5/6))
 summary=dict(complete_profiles=len(budgets),sudden_fraction_range=[min(r['sudden_fraction'] for r in budgets),max(r['sudden_fraction'] for r in budgets)],slow_fraction_range=[min(r['slow_fraction'] for r in budgets),max(r['slow_fraction'] for r in budgets)],kinetic_fraction_range=[min(r['kinetic_fraction'] for r in budgets),max(r['kinetic_fraction'] for r in budgets)],quarter_cycle_energy_gain=3.,half_cycle_energy_gain=1.,resonant_period_days=math.pi/w0/omegaunit/86400)
 result=dict(summary=summary,budgets=budgets,floquet=floquet,nonlinear=nonlinear,zero_seed=zero)
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['summary','floquet','nonlinear']},indent=2))
if __name__=='__main__':main()
