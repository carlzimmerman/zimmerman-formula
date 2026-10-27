import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import eigh,cho_factor,cho_solve
from tension_charge import TensionCharge,h
from refine import polish

def diagnostic(m,x):
    q=h(x);E,g=m.energy_grad(x);inner=(m.r>=.5*m.b)&(m.r<=min(5*m.b,.4*m.R));outer=m.r>=.8*m.R
    at=-np.gradient(m.tpotential(x),m.r,edge_order=2);af=-np.gradient(m.fpotential(x),m.r,edge_order=2)
    ps=[]
    for frac,acc in [(q,at),(1-q,af)]:
        f=np.where(frac>1e-9,m.m*frac/m.vol*(m.g0-acc),0)
        P=-cumulative_trapezoid(f[::-1],m.r[::-1],initial=0)[::-1]
        ps.append(dict(min=float(min(P)),max=float(max(P))))
    cross=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0]
    return dict(n=m.n,delta=m.delta,energy=E,qinner=float(m.m[inner]@q[inner]/sum(m.m[inner])),qouter=float(m.m[outer]@q[outer]/sum(m.m[outer])),speed=float(max(abs(cho_solve(cho_factor(m.metric),g)))),eigenvalue=float(eigh(m.hessian(x),m.metric,subset_by_index=[0,0],eigvals_only=True)[0]),force_error=float(max(abs((at[inner]-m.g0[inner])/m.g0[inner]))),crossings_kpc=(m.r[cross]*m.rm).tolist(),pressures=ps,x=x.tolist(),r=(m.r*m.rm).tolist(),force_T=at.tolist(),force_F=af.tolist())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    rows=json.loads(Path(__file__).with_name('run_tension').joinpath('results.json').read_text())['runs'];prev=next(r for r in rows if r['beta']==1000 and r['k']==100 and r['tau']==.1)
    out=dict(runs=[])
    for n,delta in [(128,1e-5),(256,1e-5),(512,1e-5),(512,1e-6)]:
        m=TensionCharge(6e10,3,n,100,delta,beta=1000,tau=.1);x0=np.interp(m.r*m.rm,prev['r'],prev['x']);x,opt=polish(m,x0)
        r=diagnostic(m,x);r['optimizer']=opt;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force_T','force_F','optimizer']},flush=True);prev=r
