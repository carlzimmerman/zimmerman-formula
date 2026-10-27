import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();p=Path('sol61_push/moving_core_population_2026_10_22');r=json.loads((p/'run/result.json').read_text());n0=r['inventory']['n_if_all_cores_Mpc3'];rc=.0003214846542759978;phi0=n0*4*np.pi/3*rc**3
fb=1/6.364;fc=1-fb;ell=.0004404221297174536;N0=-np.log(1101)
def calc(z,k,beta,matching,tol):
 nf=-np.log(1+z);ai=np.exp(N0)
 def pre(N,Y):
  b,bp,c,cp=Y;S=1/(1+(k*ell/np.exp(N))**2)
  return [bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*S*c)]
 def post(N,Y):
  b,bp,c,cp=Y;grav=1.5*(fb*b+fc*c)
  return [bp,-.5*bp+grav,cp,-.5*cp+beta*grav]
 sol=solve_ivp(pre,(N0,nf),[ai]*4,rtol=tol,atol=tol*1e-5,method='DOP853');assert sol.success
 Y=sol.y[:,-1].copy();before=(fb*Y[0]+fc*Y[2])/np.exp(nf)
 if matching=='momentum':Y[3]*=beta
 sol=solve_ivp(post,(nf,0),Y,rtol=tol,atol=tol*1e-5,method='DOP853');assert sol.success
 return float(fb*sol.y[0,-1]+fc*sol.y[2,-1]),float(before)
rows=[];checks=[]
for z in [10,30,100]:
 for k in [.1,1]:
  for beta in [1,.997]:
   for matching in ['velocity','momentum']:
    v,before=calc(z,k,beta,matching,1e-11);v2,_=calc(z,k,beta,matching,1e-9);rows.append(dict(z_form=z,k=k,beta=beta,matching=matching,amplitude=v,before_relative=before,filling_at_formation=phi0*(1+z)**3,repeat=abs(v-v2)))
checks.append(dict(name='convergence24',passed=max(v['repeat'] for v in rows)<1e-7));checks.append(dict(name='beta1_matching_identity',passed=all(abs(calc(z,k,1,'velocity',1e-10)[0]-calc(z,k,1,'momentum',1e-10)[0])<1e-12 for z in [10,30,100] for k in [.1,1])));checks.append(dict(name='dilute_early_assumption_fails',passed=phi0*1101**3>1))
out=dict(checks=checks,present_filling=phi0,filling_z1100=phi0*1101**3,z_filling_one=(1/phi0)**(1/3)-1,z_filling_001=(.01/phi0)**(1/3)-1,rows=rows)
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
