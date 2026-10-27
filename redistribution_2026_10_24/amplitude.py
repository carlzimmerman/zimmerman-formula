import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from global_density import Global,RESERVOIR
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[]}
for L in [1,3,10]:
 r=json.loads(Path(f'redistribution_2026_10_24/run_global/checkpoint_{L}.json').read_text());n=r['n'];m=Global(n=n,domain=12,beta=2,K=30,charge=0,L=L);m.ell2=(10/m.rm)**2;y=np.r_[np.sqrt(r['mass']),r['v'][n:]]
 def v(y):return np.r_[y[:n]**2,y[n:]]
 def fg(y):
  E,g=m.direct(v(y));return E,g*np.r_[2*y[:n],np.ones(n)]
 cons=[dict(type='eq',fun=lambda y:sum(y[:n]**2)-RESERVOIR,jac=lambda y:np.r_[2*y[:n],np.zeros(n)]),dict(type='ineq',fun=lambda y:m.cap(v(y)),jac=lambda y:m.capjac(v(y))*np.r_[2*y[:n],np.ones(n)])]
 op=minimize(fg,y,jac=True,method='SLSQP',bounds=[(1e-6,np.sqrt(RESERVOIR))]*n+[(0,1)]*n,constraints=cons,options=dict(ftol=1e-14,maxiter=2400));val=v(op.x);r=m.report(np.r_[np.log(val[:n]),val[n:]]);E,g=m.direct(val);active=val[:n]>1e-7;mu=g[:n]-np.median(g[:n][active]);mu=np.where((~active)&(mu>0),0,mu);r.update(density_KKT_max=float(max(abs(mu))),optimizer=dict(success=bool(op.success),message=str(op.message),iterations=int(op.nit)),ell_kpc=10);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['density_stiffness_length_kpc','law_endpoint_error_dex','density_KKT_max','empty_transition_cells','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
