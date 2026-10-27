#!/usr/bin/env python3
"""Same C-H action: canonical branch admission, not full geometric closure.

The flux identity is pointwise; smooth function-space equivalence and a
nonlinear continuum Dirac count are NOT inferred from its scalar Hessian.
"""
import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shlex
import subprocess
import time

import numpy as np
import scipy
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PARENT=HERE.parent/'g03_flrw_scalar_2026'/'flrw_gate.py'
spec=importlib.util.spec_from_file_location('parent_flrw_constraint',PARENT)
parent=importlib.util.module_from_spec(spec); spec.loader.exec_module(parent)


@lru_cache(None)
def legendre_identity():
    y,s=sp.symbols('y s',positive=True)
    G=y*y+2*(1+y)*sp.exp(-y)-2
    mu=1-sp.exp(-y); w=y*mu
    q=2-2*(1+y)*sp.exp(-y)-y*y*sp.exp(-2*y)
    lifted=4*s*y-2*G-2*s*s
    dqds=sp.diff(q,y)/sp.diff(w,y)
    return dict(primitive=G,lifted_density=lifted,stationarity=sp.diff(lifted,y),
        stationarity_residual=sp.simplify(sp.diff(lifted,y)-4*(s-w)),
        on_shell_identity_residual=sp.simplify(lifted.subs(s,w)-2*q),
        primitive_hessian_zero=sp.limit(sp.diff(G,y,2),y,0,dir='+'),
        eliminated_hessian_limit=sp.limit(sp.diff(dqds,y)/sp.diff(w,y),y,0,dir='+'),
        inverse_holder_limit=sp.limit(y/sp.sqrt(w),y,0,dir='+'),
        transverse_constitutive_eigenvalue=mu,
        longitudinal_constitutive_eigenvalue=sp.diff(w,y),
        nonzero_inverse_condition='mu>0 and d(y*mu)/dy>0 for y>0; not at y=0')


@lru_cache(None)
def adm_kinetic():
    V,N,R,Lambda=sp.symbols('sqrt_h N R3 Lambda',positive=True)
    d=sp.symbols('r1_dot r2_dot r3_dot',real=True)
    p=sp.symbols('p1 p2 p3',real=True)
    Nd=sp.symbols('N_dot',real=True)
    K=[v/N for v in d]; trace=sum(K)
    L=N*V*(sum(v*v for v in K)-trace**2+R-2*Lambda)
    momenta=[sp.diff(L,v) for v in d]
    velocities=sp.solve([a-b for a,b in zip(p,momenta)],d,dict=True)[0]
    hc=sp.factor((sum(a*b for a,b in zip(p,d))-L).subs(velocities))
    invariant=(sum(v*v for v in p)-sum(p)**2/2)/(4*V)-V*(R-2*Lambda)
    x=sp.symbols('x',real=True)
    lapse=sp.Function('N')(x); U=sp.Function('U')(x); volume=sp.Function('sqrt_h')(x)
    alpha,q=sp.symbols('alpha q',positive=True)
    acc=sp.diff(lapse,x)/lapse; v=sp.diff(U,x)-acc
    density=lapse*volume*(2*v*v+2*alpha*alpha*q)
    en=sp.diff(density,lapse)-sp.diff(sp.diff(density,sp.diff(lapse,x)),x)
    derived=2*v*v+4*v*acc+4*sp.diff(volume*v,x)/volume+2*alpha*alpha*q
    return dict(momentum_equations=momenta,Hamiltonian=hc,
        momentum_residuals=[sp.simplify(m-2*V*(ki-trace)) for m,ki in zip(momenta,K)],
        Hamiltonian_residual=sp.simplify(hc-N*invariant),lapse_primary=sp.diff(L,Nd),
        lapse_equation=en/volume,lapse_equation_residual=sp.simplify(en/volume-derived))


def poisson(f,g,qs,ps):
    return sp.factor(sum(sp.diff(f,q)*sp.diff(g,p)-sp.diff(f,p)*sp.diff(g,q) for q,p in zip(qs,ps)))


@lru_cache(None)
def lifted_scalar():
    old=parent.scalar_action()
    A,H,k,z,n,b,d=[old[key] for key in ('A','H','k','z','n','b','d')]
    E,u,v,ed,nd,bd,ud,vd=sp.symbols('E u v E_dot n_dot b_dot u_dot v_dot',real=True)
    sig,eta=sp.symbols('sigma eta',positive=True)
    p,pn,pb,pE,pu,pv=sp.symbols('p_z p_n p_b p_E p_u p_v',real=True)
    lns,lbs,lus,lvs=sp.symbols('lambda_n lambda_b lambda_u lambda_v',real=True)
    # v_x=-v sin(kx); average sin^2=cos^2=1/2. G has no quadratic term.
    aux=A*(k*k*(u-n)**2-k*k*sig*sig*u*u+2*k*sig*u*v)
    L=(old['L']-old['aux_L']+aux).subs(b,b-ed)
    qs=[z,n,b,E,u,v]; ps=[p,pn,pb,pE,pu,pv]; velocities=[d,nd,bd,ed,ud,vd]
    vh=sp.hessian(L,velocities)
    primary=[mom-sp.diff(L,vel) for mom,vel in zip(ps,velocities) if sp.diff(L,vel)==0]
    legendre=sp.solve([p-sp.diff(L,d),pE-sp.diff(L,ed)],[d,ed],dict=True)[0]
    hc=sp.factor((p*d+pE*ed-L).subs(legendre))
    secondary=[poisson(c,hc,qs,ps) for c in primary]
    constraints=primary+secondary
    surface=sp.solve(secondary,[n,pE,u,v],dict=True)[0]
    surface.update(dict.fromkeys(primary,0))
    rawPB=sp.Matrix([[poisson(f,g,qs,ps) for g in constraints] for f in constraints])
    matrix=rawPB.subs(surface)
    pairing=matrix.extract([0,2,3],[4,6,7])
    sc=int(matrix.rank()); fc=len(constraints)-sc
    mults=[lns,lbs,lus,lvs]
    total=hc+sum(m*c for m,c in zip(mults,primary))
    # sigma=exp[-xi^2 k^2/(2A^2)], eta=xi^2 k^2/A^2, so sigma_dot=H eta sigma.
    partial_t=lambda f: sp.diff(f,A)*H*A+sp.diff(f,sig)*H*eta*sig
    preservation=[sp.factor((partial_t(c)+poisson(c,total,qs,ps)).subs(surface)) for c in constraints]
    solved=sp.solve(preservation,mults,dict=True)[0]
    residuals=[sp.simplify(e.subs(solved)) for e in preservation]
    lag_aux=sp.solve([sp.diff(L,u),sp.diff(L,v)],[u,v],dict=True)[0]
    eliminated=sp.simplify(L.subs(lag_aux))
    # Independently compare the Lagrangian reduction, not assigned DOF integers.
    parent_dirac=parent.dirac_sector()
    checks=[sp.simplify(lag_aux[u]),sp.simplify(lag_aux[v]-k*n/sig)]
    # Time derivative of the solved algebraic surface must agree with Hamilton flow.
    flow={z:sp.diff(hc,p),p: -sp.diff(hc,z),E:sp.diff(hc,pE),pE:-sp.diff(hc,E)}
    tangent=[]
    for q,mult in ((n,lns),(u,lus),(v,lvs)):
        f=surface[q]
        dt=partial_t(f)+sum(sp.diff(f,var)*rhs for var,rhs in flow.items())
        tangent.append(sp.simplify((dt-mult).subs(surface).subs(solved)))
    return dict(L=L,auxiliary_L=aux,velocity_hessian=vh,velocity_rank=int(vh.rank()),
        Hamiltonian=hc,primary=primary,secondary=secondary,constraints=constraints,
        PB=matrix,first_class=fc,second_class=sc,
        constraint_pairing=pairing,constraint_pairing_det=sp.factor(pairing.det()),
        scalar_dof=sp.Rational(2*len(qs)-2*fc-sc,2),parent_scalar_dof=parent_dirac['dof'],
        algebraic_surface=surface,multipliers=solved,preservation_residuals=residuals,
        multiplier_substitution_residuals=tangent,
        zero_gain_PB_rank=int(rawPB.subs(sig,0).rank()),
        reduced_action_residual=sp.simplify(eliminated-old['L'].subs(b,b-ed)),
        u_constraint_residual=checks[0],v_constraint_residual=checks[1],
        flux_solution_residual=sp.simplify(sp.diff(L,u).subs({u:0,v:k*n/sig})),
        reduced_scalar_action=parent_dirac['reduced_action'],
        scope='one fixed nonzero scalar Fourier mode, quadratic zero-field action; not full nonlinear vector/continuum count')


@lru_cache(None)
def homogeneous_flux():
    v=sp.symbols('v',positive=True)
    G=v*v+2*(1+v)*sp.exp(-v)-2
    constraint=sp.diff(G,v)/2
    return dict(exact_radial_constraint=constraint,
        constraint_jacobian_at_zero=sp.limit(sp.diff(constraint,v),v,0,dir='+'),
        constraint_over_v2_limit=sp.limit(constraint/v**2,v,0,dir='+'),
        primitive_over_v3_limit=sp.limit(G/v**3,v,0,dir='+'),
        nonlinear_solution='v=0 only, since (1-exp(-r/alpha))*v=0 and mu(r/alpha)>0 for r>0',
        GR_homogeneous_dof=parent.homogeneous_sector()['dof'],
        full_homogeneous_flux_Dirac_count=None,
        reason='irregular nonlinear algebraic constraint; zero linearized Jacobian is not a gauge generator')


@lru_cache(None)
def branch_admission():
    A,H,J=sp.symbols('A H J',positive=True)
    P,P1,P2,J1,J2=sp.symbols('P P_prime P_second J_q J_qq',real=True)
    gamma=sp.sqrt(1+P*P/A**2)
    def ds(f):
        return sp.diff(f,A)*H*A*gamma+sp.diff(f,J)*P1/(A*A*gamma**2)
    def dq(f):
        return (sp.diff(f,A)*H*A*P*gamma*J+sp.diff(f,P)*P1+sp.diff(f,P1)*P2+
                sp.diff(f,J)*J1+sp.diff(f,J1)*J2)
    def derivative(f,i): return dq(f) if i==0 else sp.Integer(0)
    h=sp.diag(A*A*gamma**2*J*J,A*A,A*A); hi=h.inv()
    ch=[[[sp.simplify(sum(hi[i,l]*(derivative(h[l,j],k)+derivative(h[l,k],j)-derivative(h[j,k],l))
        for l in range(3))/2) for k in range(3)] for j in range(3)] for i in range(3)]
    ric=sp.Matrix(3,3,lambda i,j:sp.simplify(sum(derivative(ch[l][i][j],l)-derivative(ch[l][i][l],j)+
        sum(ch[l][l][m]*ch[m][i][j]-ch[l][j][m]*ch[m][i][l] for m in range(3)) for l in range(3))))
    R=sp.simplify(sp.trace(hi*ric))
    Kcov=h.applyfunc(ds)/2; Kmix=hi*Kcov; K=sp.simplify(sp.trace(Kmix))
    K2=sp.simplify(sp.trace(Kmix*Kmix))
    constraint=sp.simplify(R+K*K-K2-6*H*H)
    # D_j K^j_i-D_i K, evaluated as a genuine tensor divergence.
    mom=[]
    for i in range(3):
        mom.append(sp.simplify(sum(derivative(Kmix[j,i],j)+
            sum(ch[j][j][m]*Kmix[m,i]-ch[m][j][i]*Kmix[j,m] for m in range(3))
            for j in range(3))-derivative(K,i)))
    evolution=Kcov.applyfunc(ds)+ric-2*Kcov*hi*Kcov+K*Kcov-3*H*H*h
    # Aux fields are constants/zero BEFORE evaluating their differential equations.
    zero=sp.Integer(0); U=sp.Integer(1); W=U; multiplier=zero
    heat=lambda f: sp.simplify(dq(A*gamma**(-1)*J**(-1)*dq(f))/(A**3*gamma*J))
    auxiliary=[zero-heat(W),W-U,zero+heat(multiplier),multiplier,
               multiplier-multiplier,zero-multiplier]
    return dict(clock_adapted_metric=h,extrinsic_eigenvalues=list(Kmix.diagonal()),
        expansion=K,leaf_R=R,momenta_mixed=sp.simplify(sp.sqrt(h.det())*(Kmix-sp.eye(3)*K)),
        Hamiltonian_constraint=constraint,Hamiltonian_preservation=sp.simplify(ds(constraint)),
        momentum_constraint=sp.simplify(sum(v*v for v in mom)),momentum_components=mom,
        ADM_evolution_residuals=[sp.simplify(v) for v in evolution],
        auxiliary_equation_residuals=auxiliary,
        domain='all smooth pre-caustic clock leaves with J>0; arbitrary smooth periodic admissible P(q)')


@lru_cache(None)
def refoliation_check():
    t,x,eps,k=sp.symbols('t x eps k',real=True)
    f=sp.Function('f')(t)
    tau=t+eps*f*sp.cos(k*x)
    X=sp.diff(tau,t)**2-sp.diff(tau,x)**2
    # Exact normalized vector, expanded only after differentiation.
    nup=[sp.diff(tau,t)/sp.sqrt(X),-sp.diff(tau,x)/sp.sqrt(X)]
    ax=nup[0]*sp.diff(nup[1],t)+nup[1]*sp.diff(nup[1],x)
    first=sp.simplify(sp.diff(ax,eps).subs(eps,0))
    averaged=sp.simplify(2*first**2).subs(sp.sin(k*x)**2,sp.Rational(1,2))
    # A smooth compact-support f with f' nonzero makes the integrated coefficient positive.
    return dict(first_acceleration=first,quadratic_average=averaged,
        acceleration_residual=sp.simplify(first-k*sp.diff(f,t)*sp.sin(k*x)),
        action_coefficient_residual=sp.simplify(averaged-k*k*sp.diff(f,t)**2),
        stationary_refoliation_coefficient=averaged.subs(sp.diff(f,t),0),
        time_varying_refoliation_example=averaged.subs({k:2,sp.diff(f,t):3}),
        scope='off-shell fixed-metric clock refoliation is not a gauge symmetry; extra branch-only identification not decided')


def serial(value):
    if isinstance(value,dict): return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [serial(v) for v in value]
    if isinstance(value,sp.MatrixBase): return [[str(v) for v in row] for row in value.tolist()]
    if isinstance(value,sp.Basic): return str(value)
    return value


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=HERE)
    parser.add_argument('--require-closed',action='store_true')
    args=parser.parse_args(); started=time.time(); checks=[]
    def check(name,passed):
        checks.append(dict(name=name,passed=bool(passed)))
        print(f'[{"PASS" if passed else "FAIL"}] {name}',flush=True)
    leg=legendre_identity(); adm=adm_kinetic(); scalar=lifted_scalar()
    homogeneous=homogeneous_flux(); branch=branch_admission(); gauge=refoliation_check()
    check('exact stationary flux identity preserves exponential kernel',leg['stationarity_residual']==0 and leg['on_shell_identity_residual']==0)
    check('finite lifted Hessian does not create an invertible origin',leg['primitive_hessian_zero']==0 and leg['eliminated_hessian_limit']==sp.oo and leg['inverse_holder_limit']==1)
    check('ADM momenta Hamiltonian and lapse variation derived',all(v==0 for v in adm['momentum_residuals']) and adm['Hamiltonian_residual']==adm['lapse_equation_residual']==0)
    check('all fixed-k scalar constraints preserved',all(v==0 for v in scalar['preservation_residuals']+scalar['multiplier_substitution_residuals']))
    check('independent scalar reduction agrees with original variables',scalar['reduced_action_residual']==0 and scalar['scalar_dof']==scalar['parent_scalar_dof'] and scalar['flux_solution_residual']==0)
    check('exact zero gain changes PB rank',scalar['zero_gain_PB_rank']<scalar['second_class'])
    check('homogeneous nonlinear flux constraint is irregular',homogeneous['constraint_jacobian_at_zero']==0 and homogeneous['constraint_over_v2_limit']==1 and homogeneous['full_homogeneous_flux_Dirac_count'] is None)
    check('exact tilted clock satisfies canonical constraints',branch['Hamiltonian_constraint']==branch['momentum_constraint']==0)
    check('canonical branch is preserved by full ADM evolution',branch['Hamiltonian_preservation']==0 and all(v==0 for v in branch['ADM_evolution_residuals']+branch['auxiliary_equation_residuals']))
    check('arbitrary fixed-metric refoliation is not gauge',gauge['acceleration_residual']==gauge['action_coefficient_residual']==0 and gauge['time_varying_refoliation_example']>0)
    failed=any(not c['passed'] for c in checks); rc=1 if failed else (2 if args.require_closed else 0)
    data=dict(theory_status='OPEN',branch_status='CANONICALLY_ADMITTED_AND_PRESERVED',
        legendre=serial(leg),ADM=serial(adm),fixed_k_scalar=serial(scalar),
        homogeneous=serial(homogeneous),branch=serial(branch),refoliation=serial(gauge),checks=checks)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    output=args.output_dir/'results.json'; output.write_text(json.dumps(data,indent=2)+'\n')
    dependencies=[HERE/'constraint_gate.py',HERE/'test_constraint_gate.py',HERE/'CONTRACT.md',HERE/'REPORT.md',
        PARENT,HERE.parent/'two_body_frequency_2026'/'binary_frequency.py',
        HERE.parent/'g03_covariant_action_2026'/'ACTION.md',
        HERE.parent/'g03_covariant_action_2026'/'FULL_VARIATION.md',
        HERE.parent/'g03_clock_caustic_2026'/'REPORT.md']
    sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    command=['python3','-B',str((HERE/'constraint_gate.py').relative_to(ROOT))]
    if args.require_closed: command.append('--require-closed')
    if args.output_dir!=HERE: command.extend(['--output-dir',str(args.output_dir)])
    manifest=dict(schema_version=1,claim_id='C-H-clock-canonical-admission-not-geometric-closure',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))),
        command=shlex.join(command),
        environment=dict(software=['Python '+platform.python_version(),'sympy '+sp.__version__,
            'numpy '+np.__version__,'scipy '+scipy.__version__],hardware=platform.machine()),
        mathematics=dict(assertion_tested='exact canonical admission of caustic branch; derived fixed-k quadratic scalar PB with flux lift',
            coefficient_domain='SymPy exact real expressions',conventions='c=1; ADM K=+h_dot/(2N); prefactor c^3/(16piG) suppressed; scalar cosine average 1/2',
            inputs=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in dependencies],
            bounds=dict(branch='all smooth J>0,A>0,H>0 with stated exact coordinate identities',
                scalar='one arbitrary fixed k>0, sigma>0; sigma_dot=H eta sigma',
                excluded='nonlinear or continuum DOF, generic lifted smooth-field equivalence, all vector modes'),
            non_claims=['full geometric closure','post-caustic continuation','generic Dirac count','primordial origin','new empirical law','global novelty']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=datetime.fromtimestamp(started,timezone.utc).isoformat(),runtime_seconds=time.time()-started,exit_status=rc),
        outputs=[dict(path=str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else output.name,sha256=sha(output))],
        checks=checks,result='FAILED_DIAGNOSTIC' if failed else 'CANONICAL_ADMISSION_FULL_THEORY_OPEN',
        residual_risks=['irregular zero-field constraint surface','unbounded inverse heat response','extra branch gauge identification unproved','generic nonlinear Dirac closure unfinished'])
    (args.output_dir/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Scalar subsector:',scalar['first_class'],'first class,',scalar['second_class'],'second class,',scalar['scalar_dof'],'DOF; full theory OPEN; exit',rc)
    return rc


if __name__=='__main__':
    raise SystemExit(main())
