import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,cho_factor,cho_solve
from scipy.integrate import solve_ivp
from alignment import Align,h

def evolve(m,x0,duration=100000):
    factor=cho_factor(m.metric);E0,_=m.energy_grad(x0)
    def rhs(t,y):
        _,g=m.energy_grad(y[:-1]);dx=-cho_solve(factor,g);return np.r_[dx,-g@dx]
    def jac(t,y):
        _,g=m.energy_grad(y[:-1]);H=m.hessian(y[:-1]);J=np.zeros((m.n+1,m.n+1));J[:-1,:-1]=-cho_solve(factor,H);J[-1,:-1]=2*cho_solve(factor,g)@H;return J
    sol=solve_ivp(rhs,(0,duration),np.r_[x0,0],method='BDF',jac=jac,rtol=1e-8,atol=1e-10,t_eval=np.r_[0,np.geomspace(1,duration,50)]);assert sol.success
    inner=(m.r>=.5*m.b)&(m.r<=5*m.b);outer=m.r>=.8*m.R;hist=[];errors=[]
    for j,t in enumerate(sol.t):
        x=sol.y[:-1,j];q=h(x);E,g=m.energy_grad(x);errors.append(abs(E+sol.y[-1,j]-E0)/max(abs(E0),1e-30));hist.append(dict(t=float(t),qinner=float(np.dot(m.m[inner],q[inner])/sum(m.m[inner])),qouter=float(np.dot(m.m[outer],q[outer])/sum(m.m[outer])),energy=float(E),speed=float(max(abs(cho_solve(factor,g))))))
    x=sol.y[:-1,-1];q=h(x);force=-np.gradient(m.tpotential(x),m.r,edge_order=2);res=(force-m.g0)/m.g0;ix=np.where((q[:-1]>=.5)&(q[1:]<.5))[0];rfront=float(np.interp(.5,[q[ix[-1]+1],q[ix[-1]]],[m.r[ix[-1]+1],m.r[ix[-1]]])*m.rm) if len(ix) else None
    return dict(n=m.n,Rjb=m.Rjb,eta=m.eta,duration=duration,final=hist[-1],front_kpc=rfront,max_energy_error=max(errors),eigenvalue=float(eigh(m.hessian(x),m.metric,subset_by_index=[0,0],eigvals_only=True)[0]),T_force_max_relative=float(max(abs(res[inner]))),T_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),phase_min=float(min(x)),phase_max=float(max(x)),history=hist,x=x.tolist(),r=(m.r*m.rm).tolist(),force=force.tolist(),gravity=m.g0.tolist())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_instability').joinpath('results.json').read_text())['runs'];prev=next(r for r in rows if r['Rjb']==8);out=dict(runs=[])
    for n in [256,512]:
        m=Align(6e10,3,n,8,30);x0=np.interp(m.r*m.rm,prev['r'],prev['x']);r=evolve(m,x0);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','history','force','gravity']},flush=True);prev=r
