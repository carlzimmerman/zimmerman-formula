import argparse,json,math
from pathlib import Path
import numpy as np
import sympy as S
from scipy.integrate import solve_ivp

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args()
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 q,d=S.symbols('q d',real=True);f=S.cos(q/2)**2;y=4*S.sin(q/2)**2
 V=(1+(y-1)**2)/f**2+d/S.sqrt(f)
 assert S.simplify(S.diff(V,q,2).subs(q,0)-(d-8)/4)==0
 g=S.Rational(9,4)*(2 if a.mutate else 1)
 assert S.simplify(S.diff(V,q,4).subs({q:0,d:8})/6-g)==0,'quartic mutation'
 runs=[]
 grid=np.linspace(80,160,16001)
 for L in [40.,80.,160.]:
  sol=solve_ivp(lambda t,z:[z[1],-t*z[0]-z[0]**3],[-L,160],
      [math.sqrt(L),-1/(2*math.sqrt(L))],method='DOP853',rtol=2e-11,atol=1e-12,dense_output=True)
  assert sol.success
  Q,P=sol.sol(grid)
  energy=.5*P*P+.5*grid*Q*Q+.25*Q**4
  action=energy/np.sqrt(grid)
  means=[float(np.mean(action[grid<120])),float(np.mean(action[grid>=120]))]
  assert abs(means[0]/means[1]-1)<.02
  runs.append(dict(initial_cutoff=L,action_windows=means))
 I=runs[-1]['action_windows'][-1]
 assert max(abs(r['action_windows'][-1]/I-1) for r in runs)<.02
 # Inputs already computed and provenance recorded in preceding audits.
 gas=json.load(open('reviews/cold_filter_reality_2026_10_25/run_fixed/result.json'))['cluster_rows']
 gas=[x for x in gas if x['HJ']==1.8e-18]
 lookup={(x['name'],round(x['inner_X'],6)):x['d'] for x in gas}
 wave=json.load(open('reviews/cold_wave_relaxation_2026_10_25/run/result.json'))['rows']
 PC=3.085677581491367e16;MSUN=1.98847e30;G=6.67430e-11
 omegaJ=299792458.**2/(1500*PC*1000);fout=5/6
 omegaunit=omegaJ/(2.4*math.sqrt(fout))
 Dmass=.75*3*(1.8e-18)**2/(8*math.pi*G)
 X=[.1,.2,.3,.5,.7,1.];rows=[]
 for z in wave:
  if z['sigma_factor']!=1.:continue
  df=lookup[z['name'],X[z['shell']]]
  tc=z['r_pc']*PC/(z['sigma_kms']*1000)
  gamma=2/(omegaunit*tc)
  wf=math.sqrt((df-8)/4)
  produced_D=gamma/float(g)*I*wf
  required=z['rho_Msun_pc3']*MSUN/PC**3/Dmass
  rows.append(dict(name=z['name'],footing=z['footing'],model=z['model'],shell=z['shell'],
    t_cross_Gyr=tc/(1e9*365.25*86400),gas_d=df,gamma=gamma,
    produced_energy_over_D=produced_D,required_source_over_D=required,ratio_produced_required=produced_D/required,
    critical_time_years=gamma**(-1/3)/omegaunit/(365.25*86400)))
 assert len(rows)==303
 result=dict(scope='conditional homogeneous slow-restoration production; no fitted conversion efficiency',
     quartic=float(g),universal_runs=runs,action_I=I,rows=rows,
     summary=dict(cases=len(rows),gamma_range=[min(r['gamma'] for r in rows),max(r['gamma'] for r in rows)],
       produced_over_D_range=[min(r['produced_energy_over_D'] for r in rows),max(r['produced_energy_over_D'] for r in rows)],
       best_ratio=max(r['ratio_produced_required'] for r in rows),worst_ratio=min(r['ratio_produced_required'] for r in rows),
       critical_years_range=[min(r['critical_time_years'] for r in rows),max(r['critical_time_years'] for r in rows)]))
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['universal_runs','action_I','summary']},indent=2))
if __name__=='__main__':main()
