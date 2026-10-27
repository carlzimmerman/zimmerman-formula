"""Independent cold-bulk benchmark: recover law from mobile mass alone."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from constrained import Constrained
from joint import RESERVOIR

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(runs=[])
    for n in [64,128,256]:
        m=Constrained(n=n,k=0,tau=0,K=0,beta=0);x=np.ones(n)
        def fg(mass):
            E,g=m.direct(np.r_[mass,x]);return E,g[:n]
        cons=[dict(type='eq',fun=lambda y:sum(y)-RESERVOIR,jac=lambda y:np.ones(n)),dict(type='ineq',fun=lambda y:.97-m.A.numpy()@y,jac=lambda y:-m.A.numpy())]
        opt=minimize(fg,m.start(scale=4)[:n],jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*n,constraints=cons,options=dict(maxiter=3000,ftol=1e-12))
        r=m.report(np.r_[np.log(opt.x),x]);r['optimizer']=dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit));out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
