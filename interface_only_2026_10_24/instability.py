import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,cho_factor,cho_solve
from scipy.integrate import solve_ivp
from alignment import Align,h

def run(row):
    m=Align(6e10,3,256,row['Rjb'],30);xstar=np.array(row['x']);H=m.hessian(xstar);evals,evecs=eigh(H,m.metric,subset_by_index=[0,0]);v=evecs[:,0];v/=max(abs(v));amp=.01
    E0,g=m.energy_grad(xstar);ep=m.energy_grad(xstar+amp*v)[0];em=m.energy_grad(xstar-amp*v)[0];x0=xstar+(amp if ep<em else -amp)*v;Ein=m.energy_grad(x0)[0]
    factor=cho_factor(m.metric)
    def rhs(t,y):
        _,g=m.energy_grad(y[:-1]);dx=-cho_solve(factor,g);return np.r_[dx,-g@dx]
    def jac(t,y):
        _,g=m.energy_grad(y[:-1]);H=m.hessian(y[:-1]);J=np.zeros((m.n+1,m.n+1));J[:-1,:-1]=-cho_solve(factor,H);J[-1,:-1]=2*cho_solve(factor,g)@H;return J
    sol=solve_ivp(rhs,(0,3000),np.r_[x0,0],method='BDF',jac=jac,rtol=1e-8,atol=1e-10,t_eval=np.r_[0,np.geomspace(.01,3000,60)]);assert sol.success
    inner=(m.r>=.5*m.b)&(m.r<=5*m.b);outer=m.r>=.8*m.R;hist=[];errors=[]
    for j,t in enumerate(sol.t):
        x=sol.y[:-1,j];q=h(x);E,g=m.energy_grad(x);errors.append(abs(E+sol.y[-1,j]-Ein)/max(abs(Ein),1e-30));hist.append(dict(t=float(t),qinner=float(np.dot(m.m[inner],q[inner])/sum(m.m[inner])),qouter=float(np.dot(m.m[outer],q[outer])/sum(m.m[outer])),energy=float(E)))
    x=sol.y[:-1,-1];_,g=m.energy_grad(x);force=-np.gradient(m.tpotential(x),m.r,edge_order=2);res=(force-m.g0)/m.g0
    return dict(Rjb=m.Rjb,n=m.n,eta=m.eta,initial_eigenvalue=float(evals[0]),mode_curvature=float(v@H@v),energy_second_difference=float((ep+em-2*E0)/amp**2),energy_change_plus=ep-E0,energy_change_minus=em-E0,mode_peak_radius_kpc=float(m.r[np.argmax(abs(v))]*m.rm),final=hist[-1],max_energy_error=max(errors),max_speed=float(max(abs(cho_solve(factor,g)))),endpoint_eigenvalue=float(eigh(m.hessian(x),m.metric,subset_by_index=[0,0],eigvals_only=True)[0]),T_force_max_relative=float(max(abs(res[inner]))),history=hist,x=x.tolist(),r=(m.r*m.rm).tolist(),phase_min=float(min(x)),phase_max=float(max(x)))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_refine').joinpath('results.json').read_text())['runs'];out=dict(runs=[])
    for row in rows:
        if row['profile']==2 and row['eta']==30:
            r=run(row);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','history']},flush=True)
