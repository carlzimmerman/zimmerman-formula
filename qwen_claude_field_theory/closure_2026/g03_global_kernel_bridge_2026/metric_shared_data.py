"""Analytic small-slab limit and nonlinear common KG/gravity constraint data.

Same Hamiltonian and normalized matter convention as metric_initial_response.
This does not assert a full nonlinear evolution or import a Dirac DOF count.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import root
import sympy as s

from metric_static_background import derive, solve_background, curved_matter_jets
from metric_initial_response import operators


def matter_sources():
    eps,sigma,K,N=s.symbols('epsilon sigma K N',real=True)
    r=s.Matrix([1,s.Rational(1,2),s.Rational(1,3)])
    v=s.ones(3,1); U=s.Matrix([1,-2,1]); mass=s.diag(1,4,9)
    rho=[]; trace=[]; trace_dot=[]; rho_dot=[]; kinetics=[]; momenta=[]
    for sign in [-1,1]:
        phi=eps*r; vel=eps*(v+sign*U*sigma)
        acceleration=-K*vel-mass*phi  # normal KG derivative at D_i phi=0
        kinetic=vel.dot(vel); potential=(phi.T*mass*phi)[0]
        kinetics.append(s.expand(kinetic))
        # Each phi_i is spatially constant on the initial slice.
        z=s.symbols('z',real=True)
        momenta.append(s.expand(sum(vel[i]*s.diff(phi[i],z) for i in range(3))))
        rho.append(s.expand((kinetic+potential)/2))
        trace.append(s.expand(3*(kinetic-potential)/2))
        rho_dot.append(s.expand(vel.dot(acceleration)+(phi.T*mass*vel)[0]))
        trace_dot.append(s.expand(3*(vel.dot(acceleration)-(phi.T*mass*vel)[0])))
    return dict(rho=str(rho[0]),trace=str(trace[0]),
        rho_difference=str(s.simplify(rho[1]-rho[0])),
        trace_difference=str(s.simplify(trace[1]-trace[0])),
        momentum_difference=str(s.simplify(momenta[1]-momenta[0])),
        kinetic=str(kinetics[0]),kinetic_difference=str(s.simplify(kinetics[1]-kinetics[0])),
        first_stress_derivatives_agree=all(s.simplify(rows[1]-rows[0])==0
                                         for rows in [rho_dot,trace_dot]),
        rho_dot=str(rho_dot[0]),trace_dot=str(trace_dot[0]))


def small_slab_limit():
    d,coeff,_=operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    chi=s.symbols('chi',real=True); y=s.symbols('y',positive=True)
    physical=coeff[:,[2,5]].subs({u:y,a0:1}).applyfunc(s.factor)
    H=physical.applyfunc(lambda e:s.factor(e.subs(s.exp(-y),chi/(1-y))))
    reconstruct=(H.subs(chi,(1-y)*s.exp(-y))-physical).applyfunc(s.simplify)
    x,a,beta,c=s.symbols('x a beta c',real=True)
    acc=(H.inv()*s.Matrix([0,2*c])).applyfunc(s.factor)
    W=a*(x+1)+acc[0]*(x+1)**2/2
    V=beta*(x+1)+acc[1]*(x+1)**2/2
    endpoint=s.Matrix([W.subs(x,1),V.subs(x,1),s.integrate(W,(x,-1,1))])
    matching=endpoint.jacobian([a,beta,c])
    det=s.factor(matching.det())
    # P=(-d_xx with Dirichlet data)^-1 sigma, integral P=M/2.
    M,M0=s.symbols('M M0',positive=True); P=s.Function('P')(x)
    forcing=-s.sympify(curved_matter_jets()['proper_time_stress_acceleration_coefficient'])
    mu=1-chi
    forced_V=(forcing*P+c*(1-x**2))/(4*mu)
    mean_V=(forcing*M/2+c*s.integrate(1-x**2,(x,-1,1)))/(4*mu)
    csol=s.solve(mean_V,c)[0]
    forced_W=s.factor(-chi*forced_V.subs(c,csol))
    outside=s.factor(forced_W.subs(P,(1-x)*M0/2)) # even source, x>support
    tail_res=s.factor(s.diff(outside,x,2)-chi*csol/(2*mu))
    bound=s.factor((outside.subs(x,s.Rational(3,4))*mu/(chi*M0))
                   .subs(M,s.Rational(8,9)*M0))
    return dict(principal_matrix=str(H),boundary_matching_matrix=str(matching),
        computed_determinant=str(det),chi_zero_boundary_rank=matching.subs(chi,0).rank(),
        derived_principal_matrix_agrees=all(v==0 for v in reconstruct),
        global_c=str(csol),exterior_W=str(outside),
        exterior_solution_identity_residual=str(tail_res),
        mean_constraint_residual=str(s.factor(mean_V.subs(c,csol))),
        uniform_exterior_bound_coefficient=str(bound),
        scope='chi!=0, 1-chi>0; even nonnegative smooth sigma supported in |x|<1/3. '
              'For sufficiently small L the full variable-coefficient shooting map is invertible '
              'by continuous dependence. This does not specify a certified numerical L threshold.')


@lru_cache(maxsize=1)
def nonlinear_operator():
    d,old,_=operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    nb,ab=s.symbols('Nbar Abar',positive=True)
    W,Wp,Wpp,V,Vp,Vpp=s.symbols('W Wp Wpp V Vp Vpp',real=True)
    nn=nb*s.exp(V); aa=ab*s.exp(W); bb=s.exp(W)
    substitution={N:nn,A:aa,B:bb,Nd:nn*(u+Vp),Ad:aa*(b+Wp),Bd:bb*Wp,
        Ndd:nn*(up+(u+Vp)**2+Vpp),Add:aa*(bp+(b+Wp)**2+Wpp),Bdd:bb*(Wp**2+Wpp)}
    raw=[d['EL'][0]/(A**2*B),(A*d['EL'][1]+B*d['EL'][2])/(N*A**2*B)]
    eq=s.Matrix([s.factor(e.subs(substitution,simultaneous=True)) for e in raw])
    highest=eq.jacobian([Wpp,Vpp]); low=eq.subs({Wpp:0,Vpp:0})
    zero={q:0 for q in [W,Wp,Wpp,V,Vp,Vpp]}
    linear=eq.jacobian([W,Wp,Wpp,V,Vp,Vpp]).subs(zero)
    residual=(linear-old.subs({N:nb,A:ab})).applyfunc(s.simplify)
    args=(nb,ab,u,b,up,bp,Lam,W,Wp,V,Vp)
    return d,highest,low,args,[str(v) for v in residual]


@lru_cache(maxsize=1)
def preservation_operator():
    """Differentiate constraints with canonical KG p_phi held fixed, not velocities."""
    d,H,low,args,_=nonlinear_operator()
    W,Wp,V,Vp=args[-4:]
    Wpp,Vpp=s.symbols('Wpp Vpp',real=True)
    kinetic,potential,bar_pi_dot=s.symbols('kinetic potential bar_pi_dot',real=True)
    w,v=s.symbols('w v',real=True)
    eq=H*s.Matrix([Wpp,Vpp])+low
    J=eq.jacobian([W,Wp,Wpp,V,Vp,Vpp])
    # sqrt(h) -> exp(3w)*sqrt(h); p_phi/sqrt(h) -> exp(-3w)*velocity.
    rho=(s.exp(-6*w)*kinetic+potential)/2
    trace=3*(s.exp(-6*w)*kinetic-potential)/2
    nn=args[0]*s.exp(V)
    correction=s.Matrix([-rho,trace-2*bar_pi_dot/(nn*s.exp(v))]).jacobian([w,v])
    correction=correction.subs({w:0,v:0})
    for i in range(2):
        J[i,0]+=correction[i,0]
        J[i,3]+=correction[i,1]
    return J,args+(Wpp,Vpp,kinetic,bar_pi_dot),correction


def common_data(y0,ratio,span,epsilon):
    d,H,low,args,_=nonlinear_operator()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    seed=solve_background(y0,ratio,span)['seed']
    bg_rhs=s.lambdify((u,b),d['rhs'].subs({a0:1,Lam:ratio}),'numpy')
    def bgflow(z,Y):
        return [Y[2],Y[3],*np.asarray(bg_rhs(*Y[2:]),float).reshape(2)]
    bg=[solve_ivp(bgflow,(0,sign*span),seed,method='DOP853',rtol=1e-12,
        atol=1e-14,dense_output=True,max_step=span/32) for sign in [-1,1]]
    if not all(sol.success for sol in bg):
        raise RuntimeError('Background integration failed')
    hf=s.lambdify(args,H.subs(a0,1),'numpy')
    lf=s.lambdify(args,low.subs(a0,1),'numpy')
    chi=(1-y0)*np.exp(-y0)
    if chi==0:
        raise ValueError('The common-data volume-fixed shooting chart is singular at chi=0')
    ms=matter_sources(); eps,profile=s.symbols('epsilon sigma',real=True)
    rhof=s.lambdify(profile,s.sympify(ms['rho'],locals={'epsilon':eps,'sigma':profile})
                   .subs(eps,epsilon),'numpy')
    sf=s.lambdify(profile,s.sympify(ms['trace'],locals={'epsilon':eps,'sigma':profile})
                 .subs(eps,epsilon),'numpy')
    def geometry(x,Y):
        z=span*x
        lnN,lnA,uu,bb=bg[0 if z<0 else 1].sol(z)
        upp,bpp=np.asarray(bg_rhs(uu,bb),float).reshape(2)
        nb,ab=np.exp(lnN),np.exp(lnA)
        W,Wp,V,Vp=span**2*Y[0],span*Y[1],span**2*Y[2]/chi,span*Y[3]/chi
        arguments=(nb,ab,uu,bb,upp,bpp,ratio,W,Wp,V,Vp)
        M=np.asarray(hf(*arguments),float); q=np.asarray(lf(*arguments),float).reshape(2)
        return nb,ab,uu,W,V,M,q
    def source(x):
        z=3*x
        return np.exp(1-1/(1-z*z)) if abs(z)<1 else 0.
    def flow(x,Y,scaled_d):
        nb,ab,uu,W,V,M,q=geometry(x,Y)
        sigma=source(x); nn=nb*np.exp(V)
        target=np.array([rhof(sigma),-sf(sigma)+2*scaled_d/(chi*nn)])
        M[:,1]/=chi; M[1,:]*=chi
        rhs=target-q; rhs[1]*=chi
        Wxx,Vxx=np.linalg.solve(M,rhs)
        volume=ab**2*np.expm1(3*W)/(3*span**2)
        return [Y[1],Wxx,Y[3],Vxx,volume]
    def shoot(guess,method,rtol,atol):
        def integrate(p,dense=False):
            return solve_ivp(lambda x,Y:flow(x,Y,p[2]),(-1,1),[0,p[0],0,p[1],0],
                method=method,rtol=rtol,atol=atol,max_step=1/32,dense_output=dense)
        def residual(p):
            sol=integrate(p)
            if not sol.success:
                raise RuntimeError('Nonlinear shooting integration failed')
            return sol.y[[0,2,4],-1]
        fit=root(residual,guess,tol=1e-8)
        error=float(max(abs(residual(fit.x))))
        if error>1e-8:
            raise RuntimeError('Nonlinear boundary solve failed: '+str(fit.message))
        return integrate(fit.x,True),fit.x,error,bool(fit.success)
    coarse,p0,_,_=shoot(np.zeros(3),'RK45',2e-9,1e-11)
    fine,p,error,root_success=shoot(p0,'DOP853',1e-11,1e-13)
    grid=np.linspace(-1,1,1001); Y=fine.sol(grid)
    geometry_rows=[geometry(x,Y[:,i]) for i,x in enumerate(grid)]
    volume=np.array([r[1]**2*np.expm1(3*r[3]) for r in geometry_rows])
    baseline=np.array([r[1]**2 for r in geometry_rows])
    constraint_res=[]; dx=1e-4
    for x in np.linspace(-.99,.99,81):
        q=fine.sol(x); nb,ab,uu,W,V,M,lo=geometry(x,q)
        dq=(fine.sol(x+dx)-fine.sol(x-dx))/(2*dx)
        values=M@np.array([dq[1],dq[3]/chi])+lo
        sigma=source(x)
        target=np.array([rhof(sigma),-sf(sigma)+2*p[2]/(chi*nb*np.exp(V))])
        constraint_res.append(max(abs(values-target))/(1+max(abs(target))))

    # First preservation of the lapse and projected trace equations at pi=0.
    J,jargs,correction=preservation_operator()
    jf=s.lambdify(jargs,J.subs(a0,1),'numpy')
    kineticf=s.lambdify(profile,s.sympify(ms['kinetic'],locals={'epsilon':eps,'sigma':profile})
                       .subs(eps,epsilon),'numpy')
    free_trace=s.sympify(ms['trace_dot'],locals={
        'epsilon':eps,'sigma':profile,'K':s.Symbol('K',real=True)}).subs({
            eps:epsilon,s.Symbol('K',real=True):0})
    trace_dotf=s.lambdify(profile,free_trace,'numpy')
    def preservation_values(x):
        q=fine.sol(x); nb,ab,uu,W,V,_,_=geometry(x,q)
        z=span*x; _,_,_,bb=bg[0 if z<0 else 1].sol(z)
        upp,bpp=np.asarray(bg_rhs(uu,bb),float).reshape(2)
        dq=flow(x,q,p[2]); nn=nb*np.exp(V)
        C=np.asarray(jf(nb,ab,uu,bb,upp,bpp,ratio,W,span*q[1],V,span*q[3]/chi,
            dq[1],dq[3]/chi,kineticf(source(x)),p[2]/chi),float)
        # w=L^2 Z0, v=L^2 Z2/chi, derivatives below are in x=z/L.
        C*=np.array([span**2,span,1,span**2/chi,span/chi,1/chi])
        C[1,:]*=chi
        return nn,ab**2*np.exp(3*W),C
    def preserve_flow(x,Z,scaled_c,forcing):
        nn,volume_weight,C=preservation_values(x)
        target=np.array([0.,chi*(-nn*trace_dotf(source(x))*forcing)+2*scaled_c/nn])
        lower=C[:,[0,1,3,4]]@Z[[0,1,2,3]]
        wxx,vxx=np.linalg.solve(C[:,[2,5]],target-lower)
        return np.array([Z[1],wxx,Z[3],vxx,volume_weight*Z[0]])
    def preserve_solve(method,rtol,atol):
        columns=[]
        for initial,c,forcing in [([0,0,0,0,0],0.,1.),([0,1,0,0,0],0.,0.),
                                   ([0,0,0,1,0],0.,0.),([0,0,0,0,0],1.,0.)]:
            sol=solve_ivp(lambda x,Z:preserve_flow(x,Z,c,forcing),(-1,1),initial,
                method=method,rtol=rtol,atol=atol,max_step=1/32,dense_output=True)
            if not sol.success:
                raise RuntimeError('Multiplier preservation integration failed')
            columns.append(sol)
        matrix=np.column_stack([col.y[[0,2,4],-1] for col in columns[1:]])
        weights=np.linalg.solve(matrix,-columns[0].y[[0,2,4],-1])
        def dense(x):
            return columns[0].sol(x)+sum(wt*col.sol(x) for wt,col in zip(weights,columns[1:]))
        return dense,weights[2],matrix
    coarse_p,_,_=preserve_solve('RK45',2e-9,1e-11)
    fine_p,scaled_c,matrix=preserve_solve('DOP853',1e-11,1e-13)
    Z=fine_p(grid); residuals=[]
    for x in np.linspace(-.99,.99,81):
        derivative=(fine_p(x+dx)-fine_p(x-dx))/(2*dx)
        predicted=preserve_flow(x,fine_p(x),scaled_c,1.)
        residuals.append(np.max(abs(derivative-predicted)/(1+abs(predicted))))
    weight=np.array([r[1]**2*np.exp(3*r[3]) for r in geometry_rows])
    singular=np.linalg.svd(matrix,compute_uv=False)
    # Independent local directional differentiation of the nonlinear residual,
    # holding p_phi fixed. This catches missing matter/2d-v terms in J.
    directional=[]; step=2e-6
    direction=np.array([.7,-.2,.11,-.3,.13,.2])
    for x in [-.6,.1,.7]:
        q=fine.sol(x); nb,ab,uu,W,V,_,_=geometry(x,q)
        _,_,_,bb=bg[0 if x<0 else 1].sol(span*x)
        upp,bpp=np.asarray(bg_rhs(uu,bb),float).reshape(2)
        dq=flow(x,q,p[2]); jets=np.array([W,span*q[1],dq[1],V,span*q[3]/chi,dq[3]/chi])
        kin=kineticf(source(x)); pot=2*rhof(source(x))-kin; dd=p[2]/chi
        def residual_at(displacement):
            wj,wpj,wppj,vj,vpj,vppj=jets+displacement*direction
            aa=(nb,ab,uu,bb,upp,bpp,ratio,wj,wpj,vj,vpj)
            raw=np.asarray(hf(*aa),float)@np.array([wppj,vppj])+np.asarray(lf(*aa),float).reshape(2)
            shifted_kin=kin*np.exp(-6*displacement*direction[0])
            return raw+np.array([-(shifted_kin+pot)/2,
                3*(shifted_kin-pot)/2-2*dd/(nb*np.exp(vj))])
        numeric=(residual_at(step)-residual_at(-step))/(2*step)
        exact=np.asarray(jf(nb,ab,uu,bb,upp,bpp,ratio,W,span*q[1],V,span*q[3]/chi,
                            dq[1],dq[3]/chi,kin,dd),float)@direction
        directional.append(np.max(abs(numeric-exact)/(1+abs(exact))))
    preservation=dict(computed_boundary_rank=int(np.linalg.matrix_rank(matrix)),
        boundary_matrix=matrix.tolist(),singular_values=singular.tolist(),
        boundary_residual=float(np.max(abs(Z[[0,2,4]][:,[0,-1]]))),
        current_volume_mean_residual=float(abs(simpson(weight*Z[0],x=grid))
            /(1+np.max(abs(Z[0])))),
        finite_difference_ODE_residual=float(max(residuals)),
        refinement_difference=float(np.max(abs(Z-coarse_p(grid))/(1+abs(Z)))),
        fixed_p_directional_derivative_residual=float(max(directional)),
        same_for_both_matter_states=ms['kinetic_difference']=='0'
            and ms['first_stress_derivatives_agree'],
        fixed_canonical_matter_correction=str(correction),
        maximum_lambda_eff=float(2*span**2*np.max(abs(Z[0]))),
        maximum_log_lapse_time_derivative=float(span**2*np.max(abs(Z[2]))/abs(chi)),
        bar_pi_second_time_derivative=float(scaled_c/chi))
    return dict(y0=y0,Lambda_over_a0_squared=ratio,span=span,epsilon=epsilon,
        success=error<1e-8,root_reported_success=root_success,
        boundary_residual=error,volume_relative_residual=float(abs(simpson(volume,x=grid))
            /simpson(baseline,x=grid)),max_constraint_residual=float(max(constraint_res)),
        refinement_difference=float(np.max(abs(Y-coarse.sol(grid))/(1+abs(Y)))),
        minimum_y=float(min((r[2]+span*Y[3,i]/chi)/np.exp(r[3])
                            for i,r in enumerate(geometry_rows))),
        minimum_N=float(min(r[0]*np.exp(r[4]) for r in geometry_rows)),
        maximum_conformal_change=float(max(abs(r[3]) for r in geometry_rows)),
        maximum_log_lapse_change=float(max(abs(r[4]) for r in geometry_rows)),
        bar_pi_dot=float(p[2]/chi),shooting_parameters=p.tolist(),preservation=preservation,
        methods=['RK45','DOP853'],rtols=[2e-9,1e-11],atols=[1e-11,1e-13])


def audit():
    start=time.monotonic()
    limit=small_slab_limit(); matter=matter_sources(); _,_,_,_,linear=nonlinear_operator()
    rows=[common_data(.5,0.,.02,.02),common_data(.5,0.,.02,.01),
          common_data(10.5,float(32*s.pi),.002,.05),
          common_data(10.5,float(32*s.pi),.002,.025)]
    checks=dict(principal_matrix_from_action=limit['derived_principal_matrix_agrees'],
        exact_tail_and_mean=limit['exterior_solution_identity_residual']=='0'
            and limit['mean_constraint_residual']=='0',
        same_positive_matter_sources=all(matter[k]=='0' for k in
            ['rho_difference','trace_difference','momentum_difference']),
        first_matter_jets_agree=matter['first_stress_derivatives_agree'],
        nonlinear_linearization_agrees=all(v=='0' for v in linear),
        nonlinear_constraint_data=all(r['success'] and r['max_constraint_residual']<1e-6
            and r['volume_relative_residual']<1e-7 and r['refinement_difference']<1e-6 for r in rows),
        common_first_preservation=all(r['preservation']['same_for_both_matter_states']
            and r['preservation']['finite_difference_ODE_residual']<1e-6
            and r['preservation']['refinement_difference']<1e-6
            and r['preservation']['boundary_residual']<1e-9
            and r['preservation']['fixed_p_directional_derivative_residual']<1e-6
            and r['preservation']['current_volume_mean_residual']<1e-7 for r in rows))
    return dict(limit=limit,matter=matter,linearization_residuals=linear,common_data=rows,
        checks=checks,runtime_seconds=time.monotonic()-start,
        verdict='Small-slab inverse and common nonlinear lapse/trace constraint data established; '
            'evolution and full boundary/Dirac interpretation must follow the separate proof contract.')


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',type=Path)
    args=p.parse_args(); r=audit()
    if args.output:
        args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    for i,(name,passed) in enumerate(r['checks'].items(),1):
        print('[%s] %02d %s'%('ok' if passed else 'FAIL',i,name))
    print('Computed limiting determinant:',r['limit']['computed_determinant'])
    for row in r['common_data']:
        print('y0',row['y0'],'epsilon',row['epsilon'],'constraint residual',
              row['max_constraint_residual'],'bar pi dot',row['bar_pi_dot'])
    return 0 if all(r['checks'].values()) else 1


if __name__=='__main__':
    raise SystemExit(main())
