import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
fb=1/6.364;fc=1-fb;ai=1/1101
def growth(ell,method='DOP853',tol=1e-11):
 def f(N,Y):
  a=np.exp(N);b,bp,c,cp=Y;S=1/(1+(.1*ell/a)**2)
  return [bp,1.5*(fb*b+fc*c)-.5*bp,cp,1.5*(fb*b+fc*S*c)-.5*cp]
 sol=solve_ivp(f,(np.log(ai),0),[ai]*4,method=method,rtol=tol,atol=tol*1e-4)
 assert sol.success
 return float(fb*sol.y[0,-1]+fc*sol.y[2,-1])
checks=[]
def ck(name,ok,value):
 checks.append(dict(name=name,passed=bool(ok),value=str(value)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))
rows=[]
for radius in [10,100,500]:
 ell=radius/(1000*np.pi);amp=growth(ell);other=growth(ell,'RK45',1e-9)
 ck('repeat_radius_'+str(radius),abs(amp-other)<1e-7,abs(amp-other))
 rows.append(dict(radius_kpc=radius,minimum_ell_kpc=ell*1000,amplitude=amp))
ck('monotone',all(rows[i]['amplitude']>rows[i+1]['amplitude'] for i in range(2)),rows)
inversions=[]
for target in [.99,.95,.90]:
 ell=brentq(lambda e:growth(e)-target,0,.2,xtol=1e-13)
 value=growth(ell)
 ck('inverse_'+str(target),abs(value-target)<1e-8,value)
 inversions.append(dict(amplitude_retention=target,ell_upper_kpc=ell*1000,radius_upper_kpc=np.pi*ell*1000))
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',checks=checks,radius_cases=rows,retention_cases=inversions),indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
