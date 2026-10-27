"""LD-16: feasible cold-control initialization for compatible quadrature."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from compatible import Compatible
from joint import RESERVOIR
from conservative_radius import transfer_species
from pressure_refine import extended

def checks():
    m=Compatible(n=32,k=0,tau=0,beta=20,K=3);v=m.start(scale=8);v[m.n:]=np.linspace(.8,.1,m.n);E,g=m.direct(v);d=np.sin(np.arange(2*m.n)+.4);d[:m.n]*=1e-6;eps=1e-6
    fd=(m.direct(v+eps*d)[0]-m.direct(v-eps*d)[0])/(2*eps);err=abs(fd-g@d)/max(abs(fd),1);assert err<1e-6
    u=m.A.numpy()@v[:m.n];assert max(u)<1
    core=m.A.numpy().T@((m.vol.numpy()*(1/(1-u)**2-1))[:,None]*m.A.numpy());ev=float(np.linalg.eigvalsh(core)[0]);assert ev>0
    return dict(energy_directional_error=err,cold_bulk_core_Hessian_min=ev,cold_test_max_u=float(max(u)))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out=dict(checks=checks(),bulk=[],joint=[])
    for n in [64,128]:
        m=Compatible(n=n,domain=4,beta=0,k=0,tau=0,K=0);x=np.ones(n)
        def fg(mass):
            E,g=m.direct(np.r_[mass,x]);return E,g[:n]
        cons=[dict(type='eq',fun=lambda v:sum(v)-RESERVOIR,jac=lambda v:np.ones(n)),dict(type='ineq',fun=lambda v:.9997-m.A.numpy()@v,jac=lambda v:-m.A.numpy())]
        initial=m.start(scale=8)[:n];assert min(.9997-m.A.numpy()@initial)>0
        op=minimize(fg,initial,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*n,constraints=cons,options=dict(maxiter=1500,ftol=1e-12))
        r=extended(m.report(np.r_[np.log(op.x),x]));r['optimizer']=dict(success=bool(op.success),message=str(op.message),iterations=int(op.nit));out['bulk'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n')
    old=json.loads(Path(__file__).with_name('run_pressure').joinpath('results.json').read_text())['runs'][0]
    for start in ['front','seed']:
        m=Compatible(n=96,domain=4,beta=20,k=0,tau=0,K=3)
        if start=='front':v,info=transfer_species(m,old)
        else:v=m.start(scale=4);v[m.n:]=.01*np.exp(-m.r.numpy()/(4*m.b));info={}
        assert min(m.cap(v))>0
        r=extended(m.solve_checkpointed(v,dest.with_name(start+'_checkpoint.json'),maxiter=1500));r.update(start=start,transfer=info);out['joint'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:[{k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']} for r in rows] if isinstance(rows,list) else rows for key,rows in out.items()},indent=2))
