import json,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from carrier_checked import Carrier
from joint import RESERVOIR,outer

def polish(m,v,path,maxiter=1600):
 count=[0]
 def report(a):
  r=m.report(np.r_[np.log(a[:m.n]),a[m.n:]]);E,g=m.direct(a);act=a[:m.n]>1e-7;mu=g[:m.n]-np.median(g[:m.n][act]);mu=np.where((~act)&(mu>0),0,mu)
  r.update(density_KKT_max=float(max(abs(mu))),mass_constraint_error=float(abs(sum(a[:m.n])-RESERVOIR)),cap_slack_min=float(min(m.cap(a))),ell_kpc=float(np.sqrt(m.ell2)*m.rm));return r
 def cb(v):
  count[0]+=1
  if count[0]%100==0:
   r=report(v);r['iterations']=count[0];Path(path).write_text(json.dumps(r,indent=2)+'\n')
 cons=[dict(type='eq',fun=lambda a:sum(a[:m.n])-RESERVOIR,jac=lambda a:np.r_[np.ones(m.n),np.zeros(m.n)]),dict(type='ineq',fun=m.cap,jac=m.capjac)]
 op=minimize(m.direct,v,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*m.n+[(0,1)]*m.n,constraints=cons,callback=cb,options=dict(maxiter=maxiter,ftol=1e-14))
 r=report(op.x);r['optimizer']=dict(success=bool(op.success),message=str(op.message),iterations=int(op.nit));Path(path).write_text(json.dumps(r,indent=2)+'\n');return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output);old=json.loads(Path('material_interface_2026_10_24/run_pressure/results.json').read_text());out={'runs':[]}
 for i,r in enumerate(old['runs']):
  m=Carrier(n=r['n'],domain=16,beta=r['beta'],K=r['K'],charge=r['charge']);m.ell2=(r['ell_kpc']/m.rm)**2;v=np.r_[r['mass'],r['v'][m.n:]]
  r=polish(m,v,dest.with_name(f'checkpoint_{i}.json'));out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['K','law_windows_dex','density_KKT_max','qouter','interpolated_crossings_kpc','optimizer']},flush=True)
