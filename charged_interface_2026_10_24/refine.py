import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh,cho_factor,cho_solve,solve
from scipy.integrate import cumulative_trapezoid
from protected import Protected,h
from angular_gate import s,Fp

def polish(m,x):
    sd=np.sqrt(m.mobility_denom)
    def fg(v):
        E,g=m.energy_grad(v/sd);return E/m.normalization,g/sd/m.normalization
    opt=minimize(fg,x*sd,jac=True,method='L-BFGS-B',options=dict(maxiter=8000,ftol=1e-15,gtol=1e-11,maxls=50,maxcor=30));x=opt.x/sd;trace=[]
    for it in range(30):
        E,g=m.energy_grad(x);H=m.hessian(x);speed=float(max(abs(cho_solve(cho_factor(m.metric),g))));trace.append(dict(energy=E,speed=speed))
        if speed<1e-10:break
        try:step=cho_solve(cho_factor(H),-g)
        except np.linalg.LinAlgError:break
        rate=min(1,.2/max(abs(step)));accepted=False
        for j in range(30):
            xn=x+rate*step;en,gn=m.energy_grad(xn)
            if en<=E+1e-13*max(abs(E),1) and np.linalg.norm(gn)<np.linalg.norm(g):x=xn;accepted=True;break
            rate*=.5
        if not accepted:break
    return x,dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),newton=trace)

def diagnostics(m,x):
    q=h(x);E,g=m.energy_grad(x);inner=(m.r>=.5*m.b)&(m.r<=min(5*m.b,.4*m.R));outer=m.r>=.8*m.R
    mut=m.tpotential(x)
    # At nonzero populations, muF=muT-E_x/(m h'). Use stable q/h' ratio.
    u=m.u(q);M=m.m@q;terms=m.a*(u/(1-u)+m.beta*m.C*s(x)*Fp(u));mu=np.cumsum(terms[::-1])[::-1]-(1-m.own)*terms+m.tail_mu(M)
    mu+=m.Amid.T@(.5*m.links*Fp(m.Amid@q)*np.diff(x)**2)/m.m+.5*m.ell2*m.gamma(M)[1]*x[-1]**2
    rf=np.divide(np.sin(np.pi*x/2),np.pi*np.cos(np.pi*x/2),out=np.zeros_like(x),where=abs(np.cos(np.pi*x/2))>1e-10)
    muf=q*mu-rf*g/m.m
    at=-np.gradient(mut,m.r,edge_order=2);af=-np.gradient(muf,m.r,edge_order=2);res=(at-m.g0)/m.g0
    pressures=[]
    for frac,acc in [(q,at),(1-q,af)]:
        density=m.m*frac/m.vol;integrand=density*(m.g0-acc);integrand=np.where(frac>1e-9,integrand,0.)
        P=-cumulative_trapezoid(integrand[::-1],m.r[::-1],initial=0)[::-1]
        pressures.append(dict(min=float(min(P)),max=float(max(P)),negative_to_max=float(min(P)/max(max(abs(P)),1e-30))))
    cross=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0];front=[float(np.interp(.5,[q[j+1],q[j]],[m.r[j+1],m.r[j]])*m.rm) if q[j]>.5 else float(np.interp(.5,[q[j],q[j+1]],[m.r[j],m.r[j+1]])*m.rm) for j in cross]
    return dict(n=m.n,delta=m.delta,beta=m.beta,k=m.k,energy=float(E),capacity=m.charge(x,False)[2],qinner=float(m.m[inner]@q[inner]/sum(m.m[inner])),qouter=float(m.m[outer]@q[outer]/sum(m.m[outer])),qinner_min=float(min(q[inner])),speed=float(max(abs(cho_solve(cho_factor(m.metric),g)))),eigenvalue=float(eigh(m.hessian(x),m.metric,subset_by_index=[0,0],eigvals_only=True)[0]),T_force_max_relative=float(max(abs(res[inner]))),T_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),crossings_kpc=front,isotropic_pressure_T=pressures[0],isotropic_pressure_F=pressures[1],x=x.tolist(),r=(m.r*m.rm).tolist(),force_T=at.tolist(),force_F=af.tolist(),gravity=m.g0.tolist())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_protection').joinpath('results.json').read_text())['runs'];prev=next(r for r in rows if r['beta']==1000 and r['k']==100 and r['start_fraction']==.4);out=dict(runs=[])
    for n,delta in [(256,1e-5),(512,1e-5),(512,1e-6)]:
        m=Protected(6e10,3,n,100,delta,1000);x0=np.interp(m.r*m.rm,prev['r'],prev['x']);x,op=polish(m,x0);r=diagnostics(m,x);r['optimizer']=op;out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','force_T','force_F','gravity','optimizer']},flush=True);prev=r
