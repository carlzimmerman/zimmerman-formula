"""Bounded quadratic state-preparation and interaction-response checks."""
import argparse,json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
CHI=11.220184543019636

def prepare(N,T,dt,ti,mi,protocol,ef=.01):
    u,w=np.polynomial.legendre.leggauss(N);u=(u+1)/2;w=CHI*u*w/2
    b0=np.column_stack((u,np.full(N,mi),np.zeros(N)));r0=np.linalg.norm(b0,axis=1)
    L=np.ones(N) if ti==0 else np.tanh(r0/(2*ti))
    r=-L[:,None]*b0/r0[:,None]
    initial=w@np.sum(b0*r,axis=1);work=0.;maxledger=0.;maxnorm=0.
    count=round(T/dt);assert abs(count*dt-T)<1e-12
    for j in range(count):
        s=np.sin(np.pi*np.array([j,j+.5,j+1])/(2*count))**2
        m=mi*(1-s) if protocol=='linear' else ef*np.tan(np.arctan(mi/ef)*(1-s))
        e=ef*s
        before=(m[1]-m[0])*r[:,1]-(e[1]-e[0])*r[:,2]
        b=np.column_stack((u,np.full(N,m[1]),np.full(N,-e[1])))
        mag=np.linalg.norm(b,axis=1);axis=b/mag[:,None];angle=2*mag*dt
        c=np.cos(angle)[:,None];sine=np.sin(angle)[:,None]
        r=r*c+np.cross(axis,r)*sine+axis*np.sum(axis*r,axis=1)[:,None]*(1-c)
        work+=w@(before+(m[2]-m[1])*r[:,1]-(e[2]-e[1])*r[:,2])
        energy=w@(u*r[:,0]+m[2]*r[:,1]-e[2]*r[:,2])
        maxledger=max(maxledger,abs(energy-initial-work))
        maxnorm=max(maxnorm,float(np.max(abs(np.linalg.norm(r,axis=1)-L))))
    axis=np.column_stack((u,np.zeros(N),np.full(N,-ef)))/np.hypot(u,ef)[:,None]
    Pdiag=w@(np.sum(r*axis,axis=1)*axis[:,2]);P0=CHI*ef/(np.hypot(1,ef)+ef)
    Pbest=w@(L*ef/np.hypot(u,ef));S0=CHI*ef-P0
    return dict(N=N,T=T,dt=dt,initial_temperature=ti,initial_mass=mi,protocol=protocol,
        final_field=ef,source_relative_error=float((P0-Pdiag)/S0),
        eigenvalue_lower_bound_error=float((P0-Pbest)/S0),
        initial_energy=float(initial),final_energy=float(energy),work_on_medium=float(work),
        maximum_energy_work_residual=float(maxledger),maximum_length_error=maxnorm,
        final_instantaneous_P=float(w@r[:,2]),final_diagonal_P=float(Pdiag),ground_P=float(P0))

def floor(ti,mi,e):
    def L(u):return np.tanh(np.hypot(u,mi)/(2*ti)) if ti else 1.
    Pbest=CHI*e*quad(lambda u:u*L(u)/np.hypot(u,e),0,1,epsabs=1e-12,epsrel=1e-12)[0]
    P0=CHI*e/(np.hypot(1,e)+e)
    return dict(temperature=ti,initial_mass=mi,final_field=e,
        source_relative_error_lower_bound=float((P0-Pbest)/(CHI*e-P0)))

def response(lam,chi,x):
    delta=1-lam;f=chi/(1+chi);e=delta*delta*x/f
    lo=e.copy();hi=e+lam/2
    for _ in range(72):
        h=(lo+hi)/2;p=h/(np.hypot(1,h)+h)
        lo=np.where(h-lam*p<e,h,lo);hi=np.where(h-lam*p>=e,h,hi)
    h=(lo+hi)/2;p=h/(np.hypot(1,h)+h)
    residual=np.max(abs(h-lam*p-e)/np.maximum(e,1e-15))
    y=f*x*(1-delta*p/e);assert np.all(y>0)
    target=(y+np.sqrt(y*y+4*y))/2
    return np.log10(x/target),float(residual)

def interactions():
    gaps=[]
    for lam in [.25,.5,.9,1.,1.01,1.1,1.5,1+np.sqrt(2),3.]:
        exact=0. if lam<=1 else (lam*lam-1)/(2*lam)
        def energy(m):
            # Stable difference (1+m*m)^1.5-1; absolute m^3 term is separate.
            return m*m/(2*lam)-(np.expm1(1.5*np.log1p(m*m))-abs(m)**3)/3
        fit=minimize_scalar(energy,bounds=(0,5),method='bounded',options={'xatol':1e-13})
        chosen=fit.x if fit.fun<energy(0) else 0.
        gaps.append(dict(coupling=lam,analytic_gap=exact,numeric_gap=float(chosen),
            energy_at_analytic=float(energy(exact)),numeric_energy=float(min(fit.fun,0))))
    x=np.logspace(-4,4,501);fits=[]
    for lam in [0,.01,.05,.1,.25,.5,.75,.9,.99]:
        opt=minimize_scalar(lambda z:float(max(abs(response(lam,np.exp(z),x)[0]))),
            bounds=(-3,20),method='bounded',options={'xatol':1e-8})
        fitted=np.exp(opt.x);err,res=response(lam,fitted,x)
        fits.append(dict(coupling=lam,chi_effective=float(fitted),maximum_acceleration_residual_dex=float(max(abs(err))),
            upper_chi_boundary=bool(opt.x>19.99),maximum_root_relative_residual=res,
            fixed_chi_residual_dex=float(max(abs(response(lam,CHI,x)[0])))))
    # Finite illustrative grid, not global optimality or a first-principles prediction.
    candidates=[]
    for lam in np.linspace(.25,.5,101):
        opt=minimize_scalar(lambda z:float(max(abs(response(lam,np.exp(z),x)[0]))),bounds=(-3,20),method='bounded')
        candidates.append((float(opt.fun),float(lam),float(np.exp(opt.x))))
    best=min(candidates);dense=np.logspace(-4,4,4001)
    derr,res=response(best[1],best[2],dense)
    return dict(gaps=gaps,fits=fits,grid_best=dict(coarse_residual_dex=best[0],coupling=best[1],chi_effective=best[2],
        dense_residual_dex=float(max(abs(derr))),dense_root_relative_residual=res),
        bounds=dict(x_min=1e-4,x_max=1e4,fit_nodes=501,check_nodes=4001,lambda_grid=[.25,.5,101],log_chi_bounds=[-3,20]))

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    rows=[]
    for protocol in ['linear','angular']:
        for ti in [0.,.1,.2]:
            for T in [100.,1000.]:rows.append(prepare(96,T,.1,ti,1.,protocol))
    refinement=[prepare(N,1000.,dt,.1,1.,'angular') for N,dt in [(96,.05),(192,.1),(192,.05)]]
    floors=[floor(ti,mi,.01) for ti in [.01,.05,.1,.2] for mi in [0.,1.]]
    data=dict(runs=rows,refinement=refinement,occupation_bounds=floors,interactions=interactions())
    assert max(r['maximum_energy_work_residual'] for r in rows+refinement)<1e-10
    assert max(r['maximum_length_error'] for r in rows+refinement)<1e-10
    assert all(r['source_relative_error']+1e-9>=r['eigenvalue_lower_bound_error'] for r in rows+refinement)
    with open(args.output,'w') as f:json.dump(data,f,indent=2,allow_nan=False)
    print(json.dumps(dict(refinement=refinement,occupation_bounds=floors,interaction_best=data['interactions']['grid_best'])))
if __name__=='__main__':main()
