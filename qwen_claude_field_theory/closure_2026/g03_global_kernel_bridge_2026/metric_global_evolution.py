"""Constraint-reduced GLOBAL linear vacuum evolution of the same CMC action.

Full curved spatial operators; no prescribed eigenvalues, inertia or ranks.
Finite matrix evolution is not nonlinear existence or a three-dimensional
stability certificate. Fixed-wall global modes are not local scalar waves.
"""
import argparse
from functools import lru_cache
from itertools import permutations
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.linalg import expm
import sympy as s

from metric_static_background import derive, solve_background
from metric_initial_response import operators


@lru_cache(maxsize=1)
def derive_reduction():
    N,A,pbar,C,P,w,adot,Ddot=s.symbols('N A pbar C P w adot Ddot', real=True)
    PA,PB=s.symbols('PA PB')
    H=N*(-PA*PB/(4*A)+PB**2/(8*A**2))
    replacement={PA:s.Rational(4,3)*A*pbar-P/A,PB:s.Rational(2,3)*A**2*pbar+P}
    da=s.diff(H,PA)/A+w; db=s.diff(H,PB)+w
    anisotropy=s.factor((db-da).subs(replacement))
    volume=s.factor((2*da+db).subs(replacement))
    kinetic=s.factor(H.subs(replacement).subs(P,C/A))
    theta=(PA*A*adot+PB*(adot+Ddot)).subs(replacement)
    z=s.symbols('z',real=True); af=s.Function('A')(z); pf=s.Function('P')(z)
    paf=s.Rational(4,3)*af*pbar-pf/af
    pbf=s.Rational(2,3)*af**2*pbar+pf
    momentum=s.factor(s.diff(af,z)*paf-s.diff(pbf,z))
    Ap,Np,EA,EB,EN,d=s.symbols('Ap Np EA EB EN d')
    force_derivative=Ap*EB+A*(Ap*EA+Np*EN)-2*A**2*Ap*d
    force_res=s.factor(force_derivative.subs(EA,(2*A**2*d-EB)/A).subs(EN,0))
    residuals=dict(anisotropy=s.factor(anisotropy-3*N*P/(4*A**2)),
        volume=s.factor(volume+N*pbar/2-3*w),
        canonical_one_form=s.factor(theta-s.Rational(2,3)*A**2*pbar*(3*adot+Ddot)-P*Ddot),
        momentum_antiderivative=s.factor(momentum+s.diff(af*pf,z)/af),
        kinetic_diagonalization=s.factor(kinetic-3*N*C**2/(8*A**4)+N*A**2*pbar**2/6),
        on_shell_force_constancy=force_res)
    return dict(identity_residuals={k:str(v) for k,v in residuals.items()},
        reduced_kinetic_density=str(kinetic),global_trace_kinetic_coefficient=str(s.expand(kinetic).coeff(pbar,2)),
        anisotropy_velocity=str(anisotropy),volume_velocity=str(volume),
        scope='Vacuum plane sector, linear perturbations about a static background; global trace retained.')


@lru_cache(maxsize=1)
def spatial_operators():
    d, J, _=operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    aa,ap,app,bb,bp1,bpp,v,vp,vpp=s.symbols('aa ap app bb bp1 bpp v vp vpp')
    vars=[aa,ap,app,bb,bp1,bpp,v,vp,vpp]
    qs=[N,A,B,Nd,Ad,Bd,Ndd,Add,Bdd]
    dq=[N*v,A*aa,B*bb,Nd*v+N*vp,Ad*aa+A*ap,Bd*bb+B*bp1,
        Ndd*v+2*Nd*vp+N*vpp,Add*aa+2*Ad*ap+A*app,Bdd*bb+2*Bd*bp1+B*bpp]
    gauge={B:1,Bd:0,Bdd:0,Nd:N*u,Ad:A*b,Ndd:N*(up+u**2),Add:A*(bp+b**2)}
    eq=[d['EL'][0]/(A**2*B),(A*d['EL'][1]+B*d['EL'][2])/(N*A**2*B),d['EL'][2]]
    lin=[s.factor(sum(s.diff(e,q)*x for q,x in zip(qs,dq)).subs(gauge,simultaneous=True)) for e in eq]
    full=s.Matrix([[s.factor(s.diff(e,q)) for q in vars] for e in lin])
    cross=(full[:2,:3]+full[:2,3:6]).row_join(full[:2,6:])-J
    if any(s.factor(e)!=0 for e in cross):
        raise RuntimeError('General spatial variation does not match previous conformal operator')
    return d,J,full


@lru_cache(maxsize=1)
def gauge_covariance():
    d,_,full=spatial_operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    xi,xip,xipp,xippp=s.symbols('xi xip xipp xippp')
    upp=s.diff(d['rhs'][0],u)*up+s.diff(d['rhs'][0],b)*bp
    bpp=s.diff(d['rhs'][1],u)*up+s.diff(d['rhs'][1],b)*bp
    gauge=s.Matrix([b*xi,bp*xi+b*xip,bpp*xi+2*bp*xip+b*xipp,
                    xip,xipp,xippp,u*xi,up*xi+u*xip,upp*xi+2*up*xip+u*xipp])
    # Differentiate background equations with Lambda held constant BEFORE
    # imposing the radial constraint at the selected point.
    radial=s.solve(d['C'],Lam)[0]
    raw=full*gauge
    residuals=[s.factor(e.subs({up:d['rhs'][0],bp:d['rhs'][1]},simultaneous=True)
                          .subs(Lam,radial)) for e in raw]
    return dict(on_shell_gauge_EL_residuals=[str(e) for e in residuals],
        gauge='delta a=b_background*xi, delta b=xi_prime, delta v=u*xi; xi=0 at both walls',
        scope='All three varied spatial equations on the constrained static vacuum background.')


@lru_cache(maxsize=1)
def boundary_charge():
    d=derive()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    PA,PB,hm=s.symbols('PA PB hm')
    density=N*(-PA*PB/(4*A)+B*PB**2/(8*A**2)+hm)-d['L']
    charge=s.factor(N*s.diff(density,Nd))
    expected=-4*N*A*Ad/B-4*A**2*s.exp(-Nd/(N*B*a0))*Nd/B
    return dict(lapse_homogeneity_residual=str(s.factor(density-N*s.diff(density,N)-Nd*s.diff(density,Nd))),
        boundary_charge=str(charge),boundary_charge_identity_residual=str(s.factor(charge-expected)),
        charge_normal_metric_derivative=str(s.factor(s.diff(charge,Ad))),
        scope='Multiplier constraints vanish on shell. Fixed wall N,A do not fix normal '
              'derivatives; no additional zero-boundary-energy condition is imposed.')


def growth_gate(matrix,refined_from):
    """A resolved growing root falsifies spectral stability; no-growth is not
    a proof (Jordan blocks and untested sectors remain). No expected roots.
    """
    eigen,vectors=np.linalg.eig(matrix)
    other=np.linalg.eigvals(refined_from)
    matching=min(max(abs(eigen[i]-other[j]) for i,j in enumerate(order))
                 for order in permutations(range(len(eigen))))
    condition=float(np.linalg.cond(vectors))
    matrix_error=float(np.linalg.norm(matrix-refined_from,2))
    numerical_scale=condition*(matrix_error+20*np.finfo(float).eps*(1+np.linalg.norm(matrix,2)))
    uncertainty=max(float(matching),float(numerical_scale),1e-14)
    growth=float(max(eigen.real))
    ratio=growth/uncertainty
    return dict(status='FAIL' if ratio>100 else 'UNRESOLVED',
        maximum_real_eigenvalue=growth,matched_eigenvalue_refinement=float(matching),
        eigenvector_condition=condition,perturbation_sensitivity_scale=uncertainty,
        resolution_ratio=ratio,
        caveat='Refinement plus eigenvector conditioning is a numerical sensitivity check, not an interval enclosure.')


@lru_cache(maxsize=8)
def global_response(y0,ratio,L):
    chi=(1-y0)*np.exp(-y0)
    if y0<=0 or chi==0:
        raise ValueError('Positive-field, nonzero-chi scaling required')
    d,J,full=spatial_operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    seed=solve_background(y0,ratio,L)['seed']
    rhs=s.lambdify((u,b),d['rhs'].subs({a0:1,Lam:ratio}),'numpy')
    def bgflow(x,Y):
        return L*np.array([Y[2],Y[3],*np.asarray(rhs(*Y[2:]),float).reshape(2)])
    bg=[solve_ivp(bgflow,(0,sign),seed,method='DOP853',rtol=2e-13,atol=2e-15,
                  max_step=1/64,dense_output=True) for sign in [-1,1]]
    if not all(sol.success for sol in bg):
        raise RuntimeError('Static background integration failed')
    jf=s.lambdify((N,A,u,b,up,bp),J.subs({a0:1,Lam:ratio}),'numpy')
    ff=s.lambdify((N,A,u,b,up,bp),full.subs({a0:1,Lam:ratio}),'numpy')
    def values(x):
        lnN,lnA,uu,bb=bg[0 if x<0 else 1].sol(x)
        upp,bpp=np.asarray(rhs(uu,bb),float).reshape(2)
        nn,aa=np.exp(lnN),np.exp(lnA)
        j=np.asarray(jf(nn,aa,uu,bb,upp,bpp),float)
        f=np.asarray(ff(nn,aa,uu,bb,upp,bpp),float)
        j*=np.array([L**2,L,1,L**2/chi,L/chi,1/chi]);j[1]*=chi
        shape=3*nn/(4*aa**3)
        D=np.array([shape,shape*(uu-3*bb),shape*((uu-3*bb)**2+upp-3*bpp)])
        return nn,aa,j,f,D
    integ=lambda fun:quad(fun,-1,1,epsabs=2e-13,epsrel=2e-13)[0]
    Vx=integ(lambda x:values(x)[1]**2)
    V=L*Vx
    Nmean=integ(lambda x:values(x)[0]*values(x)[1]**2)/Vx
    kappa=L*integ(lambda x:values(x)[4][0]/values(x)[1])
    mean_targets=np.array([-integ(lambda x:values(x)[1]**2*values(x)[4][0])/3,Vx/3])

    def solve(method,rtol,atol,step):
        count=2; columns=5
        initial=np.zeros((5,columns));initial[1,2]=1;initial[3,3]=1
        global_c=np.zeros(columns);global_c[4]=1
        def flow(x,flat):
            Y=flat.reshape(5,columns)
            nn,aa,j,f,D=values(x)
            target=np.zeros((2,columns))
            target[:,0]=-L**2*(f[:2,3:6]@D)*np.array([1,chi])
            target[1]+=2*global_c/nn
            second=np.linalg.solve(j[:,[2,5]],target-j[:,[0,1,3,4]]@Y[[0,1,2,3]])
            return np.vstack([Y[1],second[0],Y[3],second[1],aa**2*Y[0]]).reshape(-1)
        sol=solve_ivp(flow,(-1,1),initial.reshape(-1),method=method,rtol=rtol,
                      atol=atol,max_step=step,dense_output=True)
        if not sol.success:
            raise RuntimeError('Augmented spatial solve failed: '+sol.message)
        end=sol.y[:,-1].reshape(5,columns)
        match=end[[0,2,4],2:]
        target=-end[[0,2,4],:2];target[2]+=mean_targets
        weights=np.linalg.solve(match,target)
        def dense(x):
            Y=sol.sol(x).reshape((5,columns)+np.shape(x))
            return Y[:,:2]+np.einsum('ij...,jk->ik...',Y[:,2:],weights)
        dscaled=weights[2]/chi
        def jet(x):
            nn,aa,j,f,D=values(x);Y=dense(x)
            target=np.zeros((2,2));target[:,0]=-L**2*(f[:2,3:6]@D)*np.array([1,chi])
            target[1]+=2*weights[2]/nn
            second=np.linalg.solve(j[:,[2,5]],target-j[:,[0,1,3,4]]@Y[[0,1,2,3]])
            alljets=np.vstack([Y[0],Y[1],second[0],Y[0],Y[1],second[0],Y[2]/chi,Y[3]/chi,second[1]/chi])
            alljets[3:6,0]+=D*np.array([1,L,L**2])
            EBscaled=(f[2]*np.array([L**2,L,1,L**2,L,1,L**2,L,1]))@alljets
            force=aa*EBscaled-s.Rational(2,3)*aa**3*dscaled
            return np.asarray(force,float),np.vstack([Y[1],second[0],Y[3],second[1],aa**2*Y[0]])
        force=jet(0.)[0]
        M=np.zeros((4,4));M[0,1]=1;M[2,3]=-Nmean/2
        M[1,[0,2]]=force;M[3,[0,2]]=dscaled
        return dense,jet,M,match
    coarse=solve('RK45',2e-10,2e-12,1/64)
    fine,jet,M,matching=solve('DOP853',2e-13,3e-15,1/96)
    grid=np.linspace(-1,1,201);Y=fine(grid)
    forces=np.array([jet(x)[0] for x in grid])
    force_error=float(np.max(abs(forces-forces[100])))
    dx=1e-5;ode=[]
    for x in np.linspace(-.99,.99,81):
        numeric=(fine(x+dx)-fine(x-dx))/(2*dx);predicted=jet(x)[1]
        ode.append(np.max(abs(numeric-predicted)/(1+abs(predicted))))
    boundary=float(np.max(abs(Y[[0,2]][:,:,[0,-1]])))
    mean_error=float(np.max(abs(Y[4,:,-1]-mean_targets)))
    refine=float(max(np.max(abs(M-coarse[2]))/(1+np.max(abs(M))),
        np.max(abs(Y-coarse[0](grid)))/(1+np.max(abs(Y)))))
    O=np.zeros((4,4));O[0,1]=-kappa;O[1,0]=kappa;O[2,3]=-2*V/3;O[3,2]=2*V/3
    hessian=O@M
    symp=float(np.linalg.norm(M.T@O+O@M)/(1+np.linalg.norm(hessian)))
    eigen=np.linalg.eigvals(M)
    growth=growth_gate(M,coarse[2])
    # Independent determinant reduction of the 4-by-4 block form gives this
    # quadratic in lambda^2. Compare against numpy's characteristic polynomial.
    # Exact rational arithmetic on the computed binary matrix avoids subtracting
    # O(1e7) float products to obtain an O(1) quartic constant at high field.
    # This certifies the matrix identity, NOT the continuum BVP coefficients.
    R=s.Matrix([[s.Rational(float(x)) for x in row] for row in M])
    lam=s.symbols('lambda');h=-R[2,3];fx,fq=R[1,0],R[1,2];dx0,dq0=R[3,0],R[3,2]
    q2=h*dq0-fx;q0=h*(fq*dx0-fx*dq0)
    formula=lam**4+q2*lam**2+q0
    quartic_error=float(s.expand(R.charpoly(lam).as_expr()-formula))
    quartic=np.array([1.,0.,float(q2),0.,float(q0)])
    numpy_quartic_error=float(np.max(abs(np.poly(M)-quartic))/(1+np.max(abs(quartic))))
    sq=[(-q2+sign*s.sqrt(q2**2-4*q0))/2 for sign in [-1,1]]
    precise=np.array([complex(sign*s.sqrt(z).evalf(50)) for z in sq for sign in [-1,1]])
    root_difference=float(min(max(abs(eigen[i]-precise[j]) for i,j in enumerate(order))
                              for order in permutations(range(4))))
    # Independent time integrator versus exact matrix exponential. No selected
    # eigenvalue or assumed oscillation frequency enters either evolution.
    initial=np.array([.1,-.2,.15,.25]);ts=np.linspace(0,1,101)
    timed=solve_ivp(lambda t,X:M@X,(0,1),initial,method='DOP853',rtol=2e-12,atol=2e-14,t_eval=ts)
    if not timed.success:
        raise RuntimeError('Reduced time evolution failed')
    exact=np.array([expm(t*M)@initial for t in ts]).T
    time_error=float(np.max(abs(exact-timed.y))/(1+np.max(abs(exact))))
    Hsym=(hessian+hessian.T)/2
    energies=np.einsum('it,ij,jt->t',exact,Hsym,exact)/2
    energy_drift=float(np.max(abs(energies-energies[0]))/(1+abs(energies[0])))
    checks=dict(symbolic=all(v=='0' for v in derive_reduction()['identity_residuals'].values()),
        spatial_force_constant=force_error<1e-7,ODE=max(ode)<1e-5,boundary=boundary<1e-9,
        mean=mean_error<1e-9,refinement=refine<1e-6,symplectic=symp<1e-7,
        time_evolution=time_error<1e-7,quadratic_invariant=energy_drift<1e-7)
    checks['quartic_identity']=quartic_error<1e-10
    checks['independent_high_precision_roots']=root_difference<growth['perturbation_sensitivity_scale']
    return dict(y0=y0,Lambda_over_a0_squared=ratio,L=L,volume=V,kappa=kappa,mean_lapse=Nmean,
        generator=M.tolist(),state_order=['X','L*C','Q','L*pbar'],time_coordinate='tau=t/L',
        eigenvalues=[[float(e.real),float(e.imag)] for e in eigen],
        maximum_real_eigenvalue=float(max(eigen.real)),
        growth_gate=growth,characteristic_polynomial=quartic.tolist(),quartic_identity_residual=quartic_error,
        numpy_characteristic_discrepancy=numpy_quartic_error,
        exact_binary_matrix_quartic_coefficients=[str(x) for x in [s.S.One,s.S.Zero,q2,s.S.Zero,q0]],
        high_precision_root_difference=root_difference,
        symplectic_matrix=O.tolist(),computed_symplectic_rank=int(np.linalg.matrix_rank(O)),
        reduced_Hessian=hessian.tolist(),Hessian_eigenvalues=np.linalg.eigvalsh(Hsym).tolist(),
        force_constancy_absolute=force_error,ODE_residual=float(max(ode)),
        boundary_residual=boundary,mean_residual=mean_error,refinement_relative=refine,
        symplectic_residual=symp,evolution_refinement_relative=time_error,quadratic_invariant_drift=energy_drift,
        matching_matrix=matching.tolist(),computed_matching_rank=int(np.linalg.matrix_rank(matching)),
        matching_condition_number=float(np.linalg.cond(matching)),
        checks={k:bool(v) for k,v in checks.items()},audit_pass=bool(all(checks.values())),
        scope='Two global vacuum response bases on a fixed-wall plane patch; no tensor, '
              'nonlinear, infinite-volume, matter-driven, or zero-field stability certification.')


def audit():
    start=time.monotonic()
    cases=[global_response(.5,0.,.02),global_response(.5,0.,.01),
           global_response(10.5,float(32*s.pi),.002),global_response(10.5,float(32*s.pi),.001)]
    gauge=gauge_covariance();charge=boundary_charge()
    return dict(symbolic=derive_reduction(),gauge=gauge,boundary_charge=charge,cases=cases,runtime_seconds=time.monotonic()-start,
        audit_pass=all(r['audit_pass'] for r in cases) and all(v=='0' for v in gauge['on_shell_gauge_EL_residuals'])
            and charge['lapse_homogeneity_residual']=='0' and charge['boundary_charge_identity_residual']=='0',
        scope='A finite-dimensional constrained linear vacuum evolution is not a complete theory.')


def exit_status(result,require_stable):
    if not result['audit_pass']:
        return 1
    if require_stable and any(r['growth_gate']['status']!='PASS' for r in result['cases']):
        return 2
    return 0


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path)
    p.add_argument('--require-no-growing-global-mode',action='store_true')
    args=p.parse_args();r=audit()
    if args.output:
        args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    for case in r['cases']:
        print('y0',case['y0'],'L',case['L'],'eigenvalues',case['eigenvalues'],
              'growth gate',case['growth_gate'],'checks',case['checks'])
    return exit_status(r,args.require_no_growing_global_mode)


if __name__=='__main__':
    raise SystemExit(main())
