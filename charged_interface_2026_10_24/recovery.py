import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from scipy.integrate import solve_ivp
from pinning import Pin,h
from forces import potential

def tpotential(m,x):
    _,g=m.energy_grad(x)
    ratio=np.divide(np.cos(np.pi*x/2),np.pi*np.sin(np.pi*x/2),out=np.zeros_like(x),where=abs(np.sin(np.pi*x/2))>1e-10)
    return potential(m,x)+ratio*g/m.m

def check():
    m=Pin(6e10,3,64,5,1e5,.03);x=np.linspace(.8,.2,64);mu=tpotential(m,x);old=m.m.copy();A=m.A.copy();Am=m.Amid.copy();q=h(x);d=old*np.sin(np.arange(64)+.3);eps=1e-5;es=[]
    for sign in [1,-1]:
        new=old+sign*eps*d;ratio=new/old;m.m=new;m.A=A*ratio;m.Amid=Am*ratio
        xn=2/np.pi*np.arcsin(np.sqrt((old*q+sign*eps*d)/new));es.append(m.energy_grad(xn)[0])
    err=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1);assert err<1e-6
    return dict(T_mass_variation_fd_error=err)

def run(m,xstar,shift):
    q=h(xstar);j=np.where((q[:-1]>=.5)&(q[1:]<.5))[0][-1];R=(m.r[j]+m.r[j+1])/2
    v=-np.gradient(xstar,m.r)*np.exp(-((m.r-R)/(.15*m.R))**4)
    x0=xstar+shift/m.rm*v;E0,_=m.energy_grad(x0);factor=cho_factor(m.metric)
    def rhs(t,y):
        _,g=m.energy_grad(y[:-1]);dx=-cho_solve(factor,g);return np.r_[dx,-g@dx]
    def jac(t,y):
        _,g=m.energy_grad(y[:-1]);H=m.hessian(y[:-1]);J=np.zeros((m.n+1,m.n+1));J[:-1,:-1]=-cho_solve(factor,H);J[-1,:-1]=2*cho_solve(factor,g)@H;return J
    sol=solve_ivp(rhs,(0,100),np.r_[x0,0],method='BDF',jac=jac,rtol=1e-8,atol=1e-10,t_eval=np.linspace(0,100,21));assert sol.success
    errors=[abs(m.energy_grad(sol.y[:-1,i])[0]+sol.y[-1,i]-E0)/abs(E0) for i in range(len(sol.t))]
    x=sol.y[:-1,-1];inner=(m.r>=.5*m.b)&(m.r<=5*m.b);outer=m.r>=.8*m.R
    force=-np.gradient(tpotential(m,x),m.r,edge_order=2);res=(force-m.g0)/m.g0
    return dict(shift_kpc=shift,max_energy_error=max(errors),phase_initial_distance=float(np.linalg.norm(x0-xstar)),phase_final_distance=float(np.linalg.norm(x-xstar)),qinner=float(np.dot(m.m[inner],h(x)[inner])/sum(m.m[inner])),qouter=float(np.dot(m.m[outer],h(x)[outer])/sum(m.m[outer])),T_force_max_relative=float(max(abs(res[inner]))),T_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),x=x.tolist())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_forces').joinpath('results.json').read_text())['runs'];row=next(r for r in rows if r['n']==256 and r['Rjb']==5);m=Pin(6e10,3,256,5,1e5,.03);x=np.array(row['x']);out=dict(checks=check(),runs=[])
    for shift in [-.2,.2]:
        r=run(m,x,shift);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k!='x'},flush=True)
