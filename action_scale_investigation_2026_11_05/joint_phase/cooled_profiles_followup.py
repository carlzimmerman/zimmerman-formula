"""Conditional finite halo BVP and staggered radial linear stability experiment."""
import argparse,json,warnings
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import root,brentq
from scipy.special import kve
from scipy.linalg import eigvals
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
R=3.;rmin=1.e-3;K=1.e-3;C=1.e-3;kap0=.2;gap=.5;ein=3.;cv=1.5

def cool(T):
    x=gap/(2*T)
    return C*gap/(2*np.sqrt(T))*np.exp(-2*x)*kve(1,x)
def source(r,scale):return scale*1.e-3*np.exp(-r/5)/(1+r*r)

def bvp(gamma,scale,old=None):
    r=np.linspace(rmin,R,160)
    temp=brentq(lambda T:cv*T+cool(T)/K-ein,.01,3.)
    rr=np.linspace(0,R,1000);nm=np.sqrt(np.trapz(source(rr,scale)*rr**2,rr)/(K*R**3/3))
    guess=np.array([np.full_like(r,np.log(nm)),np.zeros_like(r),np.full_like(r,np.log(temp)),np.zeros_like(r),nm*r**3/3]) if old is None else old.sol(r)
    def fun(r,y):
        n=np.exp(y[0]);u=y[1];T=np.exp(y[2]);F=y[3];M=y[4]
        J=source(r,scale);q=J/n;Tp=-F/(kap0*np.sqrt(T))
        dlogn=(-u*(q-K*n-2*u/r)-gamma*M/r**2-q*u-Tp)/(T-u*u)
        up=q-K*n-2*u/r-u*dlogn
        Fp=J*(ein+u*u/2-cv*T)-n*cv*u*Tp-n*T*(up+2*u/r)-n*n*cool(T)-2*F/r
        return np.array([dlogn,up,Tp/T,Fp,r*r*n])
    def bc(a,b):
        n=np.exp(a[0]);T=np.exp(a[2]);J=source(rmin,scale)
        return np.array([a[1]-(J/n-K*n)*rmin/3,a[3]-(J*(ein-2.5*T)+K*n*n*T-n*n*cool(T))*rmin/3,a[4]-n*rmin**3/3,b[1],b[3]])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        sol=solve_bvp(fun,bc,r,guess,tol=2.e-7,max_nodes=6000)
    return sol

def grid(N):
    faces=np.linspace(0,R,N+1);r=(faces[:-1]+faces[1:])/2;vol=(faces[1:]**3-faces[:-1]**3)/3
    return faces,r,vol,R/N

def rhs(z,N,gamma,scale,disable_cooling=False):
    faces,r,vol,dr=grid(N);n=np.exp(z[:N]);T=np.exp(z[N:2*N]);u=np.r_[0.,z[2*N:],0.]
    uc=(u[:-1]+u[1:])/2;nf=(n[:-1]+n[1:])/2;J=source(r,scale)
    numflux=np.r_[0.,nf*u[1:-1],0.]
    ndot=-np.diff(faces**2*numflux)/vol+J-K*n*n
    M=np.r_[0.,np.cumsum(n*vol)]
    up=(uc[1:]-uc[:-1])/dr
    udot=-u[1:-1]*up-np.diff(n*T)/(dr*nf)-gamma*M[1:-1]/faces[1:-1]**2-(J[:-1]+J[1:])/(2*nf)*u[1:-1]
    F=np.r_[0.,-kap0*np.sqrt((T[:-1]+T[1:])/2)*np.diff(T)/dr,0.]
    gradT=(np.r_[T[1:],T[-1]]-np.r_[T[0],T[:-1]])/(2*dr)
    divu=np.diff(faces**2*u)/vol;divF=np.diff(faces**2*F)/vol
    cooling=0. if disable_cooling else n*n*cool(T)
    Tdot=-uc*gradT-T*divu/cv+(J*(ein+uc*uc/2-cv*T)-cooling-divF)/(cv*n)
    return np.r_[ndot/n,Tdot/T,udot]

def jacobian(z,N,gamma,scale,step=2.e-6):
    eye=np.eye(len(z))*step
    return np.column_stack([(rhs(z+e,N,gamma,scale)-rhs(z-e,N,gamma,scale))/(2*step) for e in eye])

def discrete(sol,N,gamma,scale):
    faces,r,vol,dr=grid(N);ys=sol.sol(r)
    z0=np.r_[ys[0],ys[2],sol.sol(faces[1:-1])[1]]
    ans=root(lambda z:rhs(z,N,gamma,scale),z0,tol=1.e-10)
    z=ans.x;res=float(np.max(np.abs(rhs(z,N,gamma,scale))))
    if not np.all(np.isfinite(z)) or res>1.e-7:return {'N':N,'success':False,'message':str(ans.message),'residual':res}
    n=np.exp(z[:N]);T=np.exp(z[N:2*N]);uf=np.r_[0,z[2*N:],0];uc=(uf[:-1]+uf[1:])/2
    eig=eigvals(jacobian(z,N,gamma,scale));idx=np.argsort(eig.real)[::-1];eig=eig[idx]
    Mcent=np.r_[0,np.cumsum(n*vol)[:-1]]+n*(r**3-faces[:-1]**3)/3
    v2=gamma*Mcent/r
    slopes=np.gradient(np.log(np.maximum(v2,1.e-300))/2,np.log(r)) if gamma else np.zeros(N)
    src=float(np.sum(source(r,scale)*vol));loss=float(np.sum(K*n*n*vol));Lrad=float(np.sum(n*n*cool(T)*vol))
    perturb=z+1.e-4*np.cos(np.arange(len(z)))
    np_=np.exp(perturb[:N]);d=rhs(perturb,N,gamma,scale)[:N]*np_
    budget=float(abs(np.sum(d*vol)-np.sum((source(r,scale)-K*np_**2)*vol)))
    evchange=None
    if N==48 and gamma==1. and scale==1.:
        e2=eigvals(jacobian(z,N,gamma,scale,1.e-6));evchange=float(abs(np.max(e2.real)-eig[0].real))
    return {'N':N,'success':True,'root_success_flag':bool(ans.success),'residual':res,'source_integral':src,'annihilation_integral':loss,'relative_number_balance':abs(src-loss)/src,'perturbed_number_budget_error':budget,'radiative_integral':Lrad,'max_mach':float(np.max(abs(uc)/np.sqrt(T))),'n_range':[float(n.min()),float(n.max())],'T_range':[float(T.min()),float(T.max())],'outer_pressure':float(n[-1]*T[-1]),'mass_integral':float(np.sum(n*vol)),'max_v2':float(v2.max()),'vmax4_over_source_scale':float(v2.max()**2/scale),'rotation_slope_at_half_R':float(np.interp(R*.5,r,slopes)),'rotation_slope_at_08_R':float(np.interp(R*.8,r,slopes)),'bvp_log_n_error':float(np.max(abs(z[:N]-ys[0]))),'bvp_log_T_error':float(np.max(abs(z[N:2*N]-ys[2]))),'max_eigen_real':float(eig[0].real),'top_eigenvalues':[[float(e.real),float(e.imag)] for e in eig[:8]],'eigen_step_change':evchange,'no_cooling_residual':float(np.max(abs(rhs(z,N,gamma,scale,True)))),'profile':{'r':r.tolist(),'n':n.tolist(),'T':T.tolist(),'u':uc.tolist(),'v2':v2.tolist()}}


cases=[]
configs=[('strong_gravity',3.,3.,8.,[48,72,96]),('smaller_boundary',2.,3.,1.,[48,72]),('larger_boundary',4.,3.,1.,[48,72]),('hotter_injection',3.,6.,1.,[48,72])]
for label,radius,energy,gamma,grids in configs:
    R=radius;ein=energy
    sol=None
    for grav in ([1.,2.,4.,8.] if gamma==8. else [gamma]):sol=bvp(grav,1.,sol)
    rec={'label':label,'R':R,'ein':ein,'gamma':gamma,'bvp_success':bool(sol.success),'runs':[]}
    if sol.success:
        for N in grids:
            run=discrete(sol,N,gamma,1.)
            if run['success']:
                faces,r,vol,dr=grid(N);pr=run['profile'];n=np.array(pr['n']);T=np.array(pr['T']);u=np.array(pr['u'])
                mass=np.r_[0.,np.cumsum(n*vol)];gf=np.r_[0.,gamma*mass[1:]/faces[1:]**2];gc=(gf[:-1]+gf[1:])/2
                injection=float(np.sum(source(r,1.)*ein*vol));ann=float(np.sum(K*n*n*(cv*T+u*u/2)*vol));cooling=run['radiative_integral'];gravwork=float(-np.sum(n*u*gc*vol))
                err=injection+gravwork-ann-cooling
                run['kinetic_budget']={'injection':injection,'annihilation':ann,'radiation':cooling,'gravitational_work':gravwork,'residual':err,'relative_error':abs(err)/(abs(injection)+abs(gravwork)+abs(ann)+abs(cooling))}
                run['edge_v2']=gamma*run['mass_integral']/R
                run['edge_v4_over_total_source']=run['edge_v2']**2/run['source_integral']
                run['flow_range']=[float(u.min()),float(u.max())]
            rec['runs'].append(run)
    cases.append(rec)
    print(json.dumps({k:v for k,v in rec.items() if k!='runs'}),flush=True)
    for run in rec['runs']:print(json.dumps({k:v for k,v in run.items() if k not in ['profile','top_eigenvalues']}),flush=True)
checks={'all requested BVPs converge':all(c['bvp_success'] for c in cases),'all requested discrete solutions converge':all(len(c['runs'])>=2 and all(r['success'] for r in c['runs']) for c in cases)}
valid=[r for c in cases for r in c['runs'] if r['success']]
checks['steady residuals below tolerance']=all(r['residual']<1.e-7 for r in valid)
checks['number budgets']=all(r['relative_number_balance']<1.e-7 and r['perturbed_number_budget_error']<1.e-11 for r in valid)
checks['energy budget errors decrease on refinement']=all(c['runs'][-1]['kinetic_budget']['relative_error']<c['runs'][0]['kinetic_budget']['relative_error'] for c in cases if len(c['runs'])>=2)
checks['fine grid energy budget relative error below 0.001']=all(c['runs'][-1]['kinetic_budget']['relative_error']<.001 for c in cases if c['runs'])
result={'cases':cases,'checks':checks,'scope':'Conditional parameter sensitivity and refinement; prescribed rigid boundary; stationary kinetic-energy budget includes gravitational work.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(checks));raise SystemExit(0 if all(checks.values()) else 1)
