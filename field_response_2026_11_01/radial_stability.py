#!/usr/bin/env python3
"""FR01 radial energy screen; finite Ritz signs, not full kinetic stability."""
import importlib.util
import json
import math
import resource
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss, legval, legder
from scipy.integrate import solve_bvp
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent


def local_energy(n, s):
    return 1.5*np.asarray(n)**(5./3)*np.exp(-2*np.asarray(s)) + np.expm1(3*np.asarray(s))-3*np.asarray(s)


def local_hessian(n, s):
    n, s = np.asarray(n), np.asarray(s)
    z = np.exp(-2*s)
    return (5./3*n**(-1./3)*z, -5*n**(2./3)*z,
            6*n**(5./3)*z+9*np.exp(3*s))


def source_module():
    spec=importlib.util.spec_from_file_location('frozen_gradient', HERE/'inputs/check_gradient.py')
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def quadrature(lo, hi, count):
    x,w=leggauss(count)
    r=lo+(x+1)*(hi-lo)/2
    return r,w*(hi-lo)/2


def state(sol,r):
    psi,dp,s,ds=sol.sol(r)
    p=np.maximum(psi,0.)
    z=np.exp(3*s)
    n=p**1.5*z
    dn=z*(1.5*np.sqrt(p)*dp+3*p**1.5*ds)
    return psi,dp,s,ds,n,dn


def displacement(j,r,radius):
    co=np.zeros(j+1);co[j]=1.
    z=2*(r/radius)**2-1
    poly=legval(z,co)
    dpoly=legval(z,legder(co)) if j else np.zeros_like(r)
    return r*poly,poly+4*(r/radius)**2*dpoly,poly


def perturbation(j,sol,r,radius):
    psi,dp,s,ds,n,dn=state(sol,r)
    xi,dxi,xir=displacement(j,r,radius)
    inside=(r<radius)
    q=-(dn*xi+n*(dxi+2*xir))
    return np.where(inside,xi,0.),np.where(inside,q,0.)


def scalar_response(j, sol, radius, eps, tol):
    outer=sol.x[-1]
    tail=math.sqrt(3/eps)+1/outer
    grid=np.unique(np.r_[sol.x,np.linspace(.9*radius,1.01*radius,100)])
    grid=grid[(grid>=0)&(grid<=outer)]
    def rhs(r,y):
        psi,dp,s,ds,n,dn=state(sol,r)
        _,q=perturbation(j,sol,r,radius)
        b=-5*np.maximum(psi,0.)
        c=6*n*np.maximum(psi,0.)+9*np.exp(3*s)
        return np.array([y[1],(c*y[0]+b*q)/(3*eps)])
    def jac(r,y):
        psi,dp,s,ds,n,dn=state(sol,r)
        c=6*n*np.maximum(psi,0.)+9*np.exp(3*s)
        a=np.zeros((2,2,r.size));a[0,1]=1;a[1,0]=c/(3*eps)
        return a
    def bc(a,b):
        return np.array([a[1],b[1]+tail*b[0]])
    out=solve_bvp(rhs,bc,grid,np.zeros((2,grid.size)),S=np.diag([0.,-2.]),
                  fun_jac=jac,tol=tol,max_nodes=24000)
    if not out.success:
        raise RuntimeError('scalar BVP failed j=%d: %s'%(j,out.message))
    return out


def matrices(sol, radius, eps, scalar, nq):
    r,w=quadrature(0.,radius,nq)
    re,we=quadrature(radius,sol.x[-1],nq)
    allr=np.r_[r,re]; weights=np.r_[w*r*r,we*re*re]
    psi,dp,s,ds,n,dn=state(sol,allr)
    p=np.maximum(psi,0.)
    aa=np.zeros_like(n)
    aa[:nq]=5./3*np.exp(-3*s[:nq])/np.sqrt(p[:nq])
    bb=-5*p;cc=6*n*p+9*np.exp(3*s)
    xis=[];qs=[];ss=[];dss=[]
    for j,sc in enumerate(scalar):
        xi,q=perturbation(j,sol,allr,radius)
        sig,dsg=sc.sol(allr)
        xis.append(xi);qs.append(q);ss.append(sig);dss.append(dsg)
    xi,q,sig,dsg=map(np.array,(xis,qs,ss,dss))
    def gram(a,b,coef): return (a*(weights*coef))@b.T
    pieces={
        'density':gram(q,q,aa),
        'mixed':gram(q,sig,bb)+gram(sig,q,bb),
        'scalar':gram(sig,sig,cc),
        'gradient':gram(dsg,dsg,np.full_like(n,3*eps)),
        'gravity':gram(xi,xi,-2.5*n*n)}
    # Robin exterior tail contributes its exact quadratic boundary energy.
    end=np.array([sc.sol(sol.x[-1])[0] for sc in scalar])
    tail=3*eps*sol.x[-1]**2*(math.sqrt(3/eps)+1/sol.x[-1])*np.outer(end,end)
    pieces['tail']=tail
    Q=sum(pieces.values());Q=(Q+Q.T)/2
    matter=gram(xi,xi,2.5*n)
    adv=sig+ds*xi
    inertia=matter+gram(adv,adv,np.full_like(n,3*eps))
    inertia=(inertia+inertia.T)/2
    scalar_work=gram(sig,sig,cc)+gram(dsg,dsg,np.full_like(n,3*eps))+tail
    source_work=gram(sig,q,-bb)
    stationarity=float(np.max(np.abs(scalar_work-source_work))/max(1.,np.max(np.abs(scalar_work))))
    mass_variations=q@weights
    # Quadrature error at a free edge is independently controlled by refinement.
    mass_error=float(np.max(np.abs(mass_variations))/max(1.,np.sum(weights*n)))
    return Q,inertia,pieces,{'scalar_response_identity':stationarity,'mass_variation':mass_error},(allr,weights,xi,q,sig,dsg)


def independent_homology(sol,radius,eps,nq=500):
    r,w=quadrature(0,radius,nq);re,we=quadrature(radius,sol.x[-1],nq)
    rr=np.r_[r,re];ww=np.r_[w*r*r,we*re*re]
    p,dp,s,ds,n,dn=state(sol,rr);pp=np.maximum(p,0.)
    er=1.5*n*pp
    A=float(ww@er);U=float(ww@(np.expm1(3*s)-3*s))
    D=float(ww@(1.5*eps*ds**2));W=float(ww@(2.5*n*dp*rr))
    I=float(ww@(s*er))
    Hll=6*A+6*U+2*W;Hla=10*I-4*D
    Haa=float(ww@(4*s*s*er+9*s*s*np.exp(3*s)))+2*D
    beta=-Hla/Haa
    xi=np.where(rr<radius,rr,0.)
    q=-(dn*rr+3*n)
    sig=-rr*ds+beta*s
    d2=sol.sol(rr,1)[3]
    dsg=-ds-rr*d2+beta*ds
    a=np.zeros_like(n);a[:nq]=(5./3)*pp[:nq]/n[:nq]
    b=-5*pp;c=6*n*pp+9*np.exp(3*s)
    direct=float(ww@(a*q*q+2*b*q*sig+c*sig*sig+3*eps*dsg*dsg-2.5*n*n*xi*xi))
    exact=Hll-Hla*Hla/Haa
    def energy(lam,alpha):
        return float(ww@(1.5*n*pp*np.exp(-2*(alpha-1)*s)/lam**2+
                         lam**3*(np.expm1(3*alpha*s)-3*alpha*s)))+alpha*alpha*lam*D+W/lam
    # Actual mass-preserving dilation and scalar-amplitude deformation.
    fd=[]
    for h in [1e-3,5e-4,2.5e-4]:
        fd.append((energy(1+h,1+beta*h)-2*energy(1,1)+energy(1-h,1-beta*h))/h**2)
    return {'A':A,'U':U,'D':D,'W':W,'virial':2*A-3*U-D+W,
            'H_lambda_lambda':Hll,'H_lambda_alpha':Hla,'H_alpha_alpha':Haa,
            'alpha_direction':beta,'optimized_curvature':exact,'direct_quadratic':direct,
            'finite_energy_second_differences':fd,
            'direct_scaled_error':abs(direct-exact)/max(1.,abs(Hll),abs(exact)),
            'finite_difference_scaled_error':abs(fd[-1]-exact)/max(1.,abs(Hll),abs(exact))}


def run_case(pc,eps,src):
    loc,guess=src.local_solution(pc)
    rec,sol=src.solve_case(pc,eps,loc,guess,refine=True)
    if not rec.get('passed',False):
        raise RuntimeError('frozen baseline failed '+str(rec))
    R=rec['radius'] if 'radius' in rec else rec['matter_radius']
    scalars=[scalar_response(j,sol,R,eps,2e-6) for j in range(12)]
    Q,I,parts,errors,samples=matrices(sol,R,eps,scalars,256)
    sub=[]
    for nb in [4,8,12]:
        vals,vec=eigh(Q[:nb,:nb],I[:nb,:nb])
        v=vec[:,0]
        comp={k:float(v@a[:nb,:nb]@v) for k,a in parts.items()}
        sub.append({'basis_size':nb,'lowest_omega2_ritz':float(vals[0]),
                    'next_omega2_ritz':float(vals[1]),'curvature_terms':comp,
                    'negative_scaled_margin':float(vals[0])/sum(abs(x) for x in comp.values()),
                    'eigenvector':v.tolist()})
    vals,vec=eigh(Q,I);v=vec[:,0]
    tight=[scalar_response(j,sol,R,eps,3e-7) for j in range(12)]
    Q2,I2,parts2,errors2,samples2=matrices(sol,R,eps,tight,512)
    val2,vec2=eigh(Q2,I2);vv=vec2[:,0]
    comp2={k:float(vv@a@vv) for k,a in parts2.items()}
    scale=sum(abs(x) for x in comp2.values())
    nongrav=Q2-parts2['gravity']
    checks={
        'baseline':bool(rec['passed']),
        'positive_inertia':bool(np.linalg.eigvalsh(I2)[0]>0),
        'positive_nongravitational_quadratic':bool(eigh(nongrav,I2,eigvals_only=True)[0]>0),
        'scalar_response_identity':errors2['scalar_response_identity']<3e-5,
        'mass_variation':errors2['mass_variation']<3e-5,
        'refined_lowest_sign_and_value':abs(val2[0]-vals[0])/max(1.,abs(val2[0]))<3e-4,
        'nested_ritz_nonincrease':all(sub[j+1]['lowest_omega2_ritz']<=sub[j]['lowest_omega2_ritz']+1e-8 for j in range(2))}
    hom=independent_homology(sol,R,eps)
    checks['homology_direct_energy']=hom['direct_scaled_error']<3e-5 and hom['finite_difference_scaled_error']<3e-5
    adverse=bool(val2[0]/scale < -1e-5)
    if not all(checks.values()): verdict='NUMERICAL_CONTROL_FAILURE'
    elif adverse: verdict='NEGATIVE_RADIAL_ENERGY_DIRECTION_IN_REDUCED_FLUID_COMPLETION'
    else: verdict='NO_NEGATIVE_DIRECTION_IN_TESTED_RITZ_SPACE'
    rr,ww,xi,q,sig,dsg=samples2
    saved={'r':rr,'weight':ww,'xi':vv@xi,'density_perturbation':vv@q,
           'scalar_perturbation':vv@sig,'scalar_derivative':vv@dsg,
           'background':np.array(state(sol,rr))}
    out={'psi_c':pc,'epsilon':eps,'baseline':rec,'nested_ritz':sub,
         'refined_lowest_omega2_ritz':float(val2[0]),'refined_curvature_terms':comp2,
         'refined_scaled_margin':float(val2[0]/scale),'refined_eigenvector':vv.tolist(),
         'errors_initial':errors,'errors_refined':errors2,'homology':hom,'checks':checks,
         'verdict':verdict,'scalar_speed_squared_over_h_star':1.,
         'reduced_mode_efolding_time':float(1/math.sqrt(-val2[0])) if adverse else None}
    return out,saved


def main():
    target=Path(sys.argv[1]);target.parent.mkdir(parents=True,exist_ok=True)
    result={'assertion_tested':'Six PN28 fixed-mass radial variational screens with nested Ritz spaces and refined witnesses; fluid completion only.',
            'cases':[],'non_claims':['No full kinetic stability theorem','No nonlinear vacuum-crossing completion','No observed galaxy mass mapping','Positive Ritz values do not prove continuum stability']}
    profiles={};src=source_module()
    try:
        for pc in [.8,.95,.99]:
            for eps in [.0001,.01]:
                row,arr=run_case(pc,eps,src);result['cases'].append(row)
                tag='pc%s_eps%s'%(pc,eps)
                profiles.update({tag+'_'+k:v for k,v in arr.items()})
                print(pc,eps,row['verdict'],row['refined_lowest_omega2_ritz'],flush=True)
        result['all_controls_pass']=all(all(c['checks'].values()) for c in result['cases'])
    except Exception as exc:
        import traceback
        result['exception']=repr(exc);result['traceback']=traceback.format_exc();result['all_controls_pass']=False
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    target.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(target.with_name('profiles.npz'),**profiles)
    if not result['all_controls_pass']:
        print(result.get('traceback','control failure'),file=sys.stderr)
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
