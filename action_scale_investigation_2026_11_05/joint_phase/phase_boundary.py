"""Dynamical phase wall: fluid equilibria and moving-boundary radial modes."""
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

EPS2=1.e-6

def moving_rhs(z,N,gamma,Sigma,DV,wrong_sign=False):
    radius=np.exp(z[-2]);W=z[-1];faces=np.linspace(0,radius,N+1);r=(faces[:-1]+faces[1:])/2;vol=np.diff(faces**3)/3;dr=radius/N
    n=np.exp(z[:N]);T=np.exp(z[N:2*N]);u=np.r_[0.,z[2*N:-2],W];uc=(u[:-1]+u[1:])/2;gridw=faces/radius*W;wc=r/radius*W
    nf=(n[:-1]+n[1:])/2;J=source(r,1.)
    numflux=np.r_[0.,nf*(u[1:-1]-gridw[1:-1]),0.]
    ndot=-np.diff(faces**2*numflux)/vol+J-K*n*n-3*W/radius*n
    mass=np.r_[0.,np.cumsum(n*vol)]
    du=(uc[1:]-uc[:-1])/dr
    udot=-(u[1:-1]-gridw[1:-1])*du-np.diff(n*T)/(dr*nf)-gamma*mass[1:-1]/faces[1:-1]**2-(J[:-1]+J[1:])/(2*nf)*u[1:-1]
    F=np.r_[0.,-kap0*np.sqrt((T[:-1]+T[1:])/2)*np.diff(T)/dr,0.]
    dT=(np.r_[T[1:],T[-1]]-np.r_[T[0],T[:-1]])/(2*dr)
    divu=np.diff(faces**2*u)/vol;divF=np.diff(faces**2*F)/vol
    Tdot=-(uc-wc)*dT-T*divu/cv+(J*(ein+uc*uc/2-cv*T)-n*n*cool(T)-divF)/(cv*n)
    pressure=n[-1]*T[-1] # same boundary-cell pressure used in compression work
    inertia=Sigma*EPS2
    force=pressure+(-DV if wrong_sign else DV)-2*Sigma/radius
    Wdot=force/inertia-W*W/radius
    return np.r_[ndot/n,Tdot/T,udot,W/radius,Wdot]

def solve_moving(sol,radius,N,gamma,Sigma,DV):
    faces=np.linspace(0,radius,N+1);r=(faces[:-1]+faces[1:])/2;ys=sol.sol(r)
    z0=np.r_[ys[0],ys[2],sol.sol(faces[1:-1])[1],np.log(radius),0.]
    def residual(z):
        v=moving_rhs(z,N,gamma,Sigma,DV);v[-1]*=Sigma*EPS2
        return v
    ans=root(residual,z0,tol=1.e-10);z=ans.x;res=float(np.max(abs(residual(z))))
    if not np.all(np.isfinite(z)) or res>1.e-7:return {'N':N,'success':False,'residual':res,'message':str(ans.message)}
    def jac(step):
        eye=np.eye(len(z))*step
        return np.column_stack([(moving_rhs(z+e,N,gamma,Sigma,DV)-moving_rhs(z-e,N,gamma,Sigma,DV))/(2*step) for e in eye])
    ev=eigvals(jac(1.e-6));ev=ev[np.argsort(ev.real)[::-1]]
    change=None
    if N==48:
        ev2=eigvals(jac(5.e-7));change=float(abs(np.max(ev2.real)-ev[0].real))
    radius=np.exp(z[-2]);faces=np.linspace(0,radius,N+1);r=(faces[:-1]+faces[1:])/2;vol=np.diff(faces**3)/3
    n=np.exp(z[:N]);T=np.exp(z[N:2*N]);uf=np.r_[0.,z[2*N:-2],z[-1]];uc=(uf[:-1]+uf[1:])/2
    mass=np.r_[0.,np.cumsum(n*vol)];mc=mass[:-1]+n*(r**3-faces[:-1]**3)/3;v2=gamma*mc/r
    slopes=np.gradient(np.log(v2)/2,np.log(r));src=float(np.sum(source(r,1.)*vol));loss=float(np.sum(K*n*n*vol))
    # Moving-volume number conservation with a nonzero wall-velocity perturbation.
    pert=z+1.e-5*np.cos(np.arange(len(z)));pn=np.exp(pert[:N]);pr=np.exp(pert[-2]);pw=pert[-1];pf=np.linspace(0,pr,N+1);pv=np.diff(pf**3)/3;pc=(pf[:-1]+pf[1:])/2
    pd=moving_rhs(pert,N,gamma,Sigma,DV)[:N]*pn
    budget=float(abs(np.sum((pd+3*pw/pr*pn)*pv)-np.sum((source(pc,1.)-K*pn*pn)*pv)))
    # Per 4pi wall+vacuum mechanical energy, arbitrary off-equilibrium state.
    wr=radius*1.01;wv=.001;pp=float(n[-1]*T[-1]);I=Sigma*EPS2;acc=(pp+DV-2*Sigma/wr)/I-wv*wv/wr
    edot=2*Sigma*wr*wv+I*wr*wv**3+I*wr**2*wv*acc-DV*wr**2*wv
    wall_error=float(abs(edot-pp*wr**2*wv)/(1+abs(pp*wr**2*wv)))
    negative=float(abs(moving_rhs(z,N,gamma,Sigma,DV,True)[-1]*I))
    return {'N':N,'success':True,'residual_scaled':res,'R':float(radius),'R_relative_to_bvp':float(radius/radius_seed-1),'density_range':[float(n.min()),float(n.max())],'temperature_range':[float(T.min()),float(T.max())],'pressure':pp,'force_residual':float(pp+DV-2*Sigma/radius),'max_eigen_real':float(ev[0].real),'eigen_step_change':change,'top_eigenvalues':[[float(e.real),float(e.imag)] for e in ev[:10]],'source_integral':src,'relative_number_balance':abs(src-loss)/src,'moving_number_budget_error':budget,'wall_work_error':wall_error,'wrong_vacuum_sign_force':negative,'max_mach':float(np.max(abs(uc)/np.sqrt(T))),'mass_integral':float(mass[-1]),'edge_v2':float(gamma*mass[-1]/radius),'edge_v4_over_source':float((gamma*mass[-1]/radius)**2/src),'slope_half_R':float(np.interp(radius*.5,r,slopes)),'slope_08_R':float(np.interp(radius*.8,r,slopes)),'profile':{'r':r.tolist(),'n':n.tolist(),'T':T.tolist(),'u':uc.tolist(),'v2':v2.tolist()}}

cases=[]
configs=[(1.,.6,.03)] if args.mutate else [(1.,.6,.03),(1.,.6,.05),(8.,.4,.03)]
for gamma,Sigma,DV in configs:
    cache={};scan=[]
    def evaluate(rad):
        global R
        key=round(float(rad),12)
        if key in cache:return cache[key]
        R=float(rad);sol=None
        for grav in ([1.,2.,4.,8.] if gamma==8. else [gamma]):
            sol=bvp(grav,1.,sol)
            if not sol.success:break
        if sol.success:
            yw=sol.sol(R);pressure=float(np.exp(yw[0]+yw[2]));force=pressure+DV-2*Sigma/R
        else:force=None
        cache[key]=(force,sol)
        return force,sol
    for rad in np.geomspace(.5,40,20):
        force,sol=evaluate(rad);scan.append({'R':float(rad),'force':force,'success':bool(sol.success)})
        print(json.dumps({'gamma':gamma,'Sigma':Sigma,'DV':DV,'scan':scan[-1]}),flush=True)
    roots=[]
    for left,right in zip(scan[:-1],scan[1:]):
        if left['force'] is None or right['force'] is None or left['force']*right['force']>=0:continue
        try:
            radius_seed=brentq(lambda x:evaluate(x)[0],left['R'],right['R'],xtol=1.e-9)
            force,sol=evaluate(radius_seed)
            hrad=radius_seed*1.e-4;df=(evaluate(radius_seed+hrad)[0]-evaluate(radius_seed-hrad)[0])/(2*hrad)
            rec={'bvp_R':float(radius_seed),'equilibrium_force':force,'quasistatic_force_slope':float(df),'runs':[]}
            for N in ([24] if args.mutate else [24,48,72]):
                run=solve_moving(sol,radius_seed,N,gamma,Sigma,DV);rec['runs'].append(run)
                print(json.dumps({'gamma':gamma,'Sigma':Sigma,'DV':DV,'root':radius_seed,**{k:v for k,v in run.items() if k not in ['profile','top_eigenvalues']}}),flush=True)
            roots.append(rec)
        except Exception as exc:roots.append({'bracket':[left['R'],right['R']],'error':repr(exc),'runs':[]})
    cases.append({'gamma':gamma,'Sigma':Sigma,'DeltaV':DV,'scan':scan,'roots':roots})
valid=[r for c in cases for rt in c['roots'] for r in rt['runs'] if r.get('success')]
checks={'at least one free boundary solved':bool(valid),'reported steady force residuals':all(r['residual_scaled']<1.e-7 for r in valid),'moving number budget':all(r['moving_number_budget_error']<1.e-10 and r['relative_number_balance']<1.e-7 for r in valid),'wall work identity':all(r['wall_work_error']<1.e-12 for r in valid),'vacuum pressure sign in equilibrium':all((r['wrong_vacuum_sign_force'] if args.mutate else abs(r['force_residual']))<1.e-7 for r in valid)}
result={'parameters':{'wall_inertia_ratio':EPS2,'cooling_C':C,'K':K,'kappa0':kap0,'gap':gap,'ein':ein},'cases':cases,'checks':checks,'mutation':args.mutate,'scope':'Prescribed phase parameters; thin wall; dynamic spherical boundary; no nonspherical or microscopic feasibility proof.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(checks),flush=True);raise SystemExit(0 if all(checks.values()) else 1)
