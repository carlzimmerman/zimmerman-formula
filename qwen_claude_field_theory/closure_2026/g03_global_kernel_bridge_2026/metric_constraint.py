"""Constraint-first metric MOND Hamiltonian: static, FLRW and principal gates.

H = H_GR - 2 int N sqrt(h) a0^2 F(a_i a^i/a0^2)
    + int lambda [pi - sqrt(h) int(pi)/int(sqrt(h))],
F(z)=2[1-(1+sqrt(z))exp(-sqrt(z))]. Matter couples to the ADM metric.
The mean-subtracted trace constraint is absent on homogeneous configurations.
This is an explicitly preferred-foliation Hamiltonian, not an established
covariant completion. Generic nonlinear Dirac closure is NOT inferred from
the complete finite-mode algorithm below. The causal calculation retains
the anisotropic highest-spatial-derivative quadratic block, not all terms
on a solved finite-gradient curved background. See METRIC_CONSTRAINT.md.
"""
import argparse
import json
from pathlib import Path
import platform
import time

import sympy as s


def linear_dirac(H,qs,ps,primary):
    """Preserve all linear constraints, computing PB ranks, never supplying them."""
    phase=qs+ps
    def pb(f,g):
        return s.expand(sum(s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q)
                            for q,p in zip(qs,ps)))
    constraints=list(primary)
    generations=[list(map(str,constraints))]
    def remainder(expr):
        rows,pivots=s.Matrix(constraints).jacobian(phase).rref()
        for i,pivot in enumerate(pivots):
            expr=s.expand(expr-s.diff(expr,phase[pivot])*(rows.row(i)*s.Matrix(phase))[0])
        return s.cancel(expr)
    for _ in range(12):
        A=s.Matrix([[pb(c,p) for p in primary] for c in constraints])
        b=s.Matrix([pb(c,H) for c in constraints])
        added=[]
        for left in A.T.nullspace():
            expr=remainder((left.T*b)[0])
            if expr!=0:
                coefficient=next(s.diff(expr,v) for v in phase if s.diff(expr,v)!=0)
                expr=s.cancel(expr/coefficient)
                constraints.append(expr)
                added.append(str(expr))
        if not added:
            break
        generations.append(added)
    else:
        raise RuntimeError('Iteration cap reached, not closure')
    multipliers=s.symbols('mult0:'+str(len(primary)))
    solution=s.linsolve(list(A*s.Matrix(multipliers)+b.applyfunc(remainder)),multipliers)
    if not solution:
        raise RuntimeError('Inconsistent preservation')
    multipliers=list(solution)[0]
    closed=all(remainder(pb(c,H)+sum(pb(c,p)*v for p,v in zip(primary,multipliers)))==0
               for c in constraints)
    bracket=s.Matrix([[pb(c,d) for d in constraints] for c in constraints])
    rank=bracket.rank()
    FC=len(constraints)-rank
    return {'generations':generations,'constraints':list(map(str,constraints)),
            'phase_basis':list(map(str,phase)),
            'poisson_matrix':[[str(v) for v in row] for row in bracket.tolist()],
            'bracket_rank':rank,'first_class':FC,'second_class':rank,
            'scalar_mode_count':int(len(qs)-FC-s.Rational(rank,2)),
            'multipliers':list(map(str,multipliers)),'preservation_closed':closed}


def derive():
    start=time.monotonic()
    a0,u,v,y,z=s.symbols('a0 u v y z',positive=True)
    F=2*(1-(1+s.sqrt(z))*s.exp(-s.sqrt(z)))
    # Independent variation of the two static metric potentials.
    Lstatic=2*v**2-4*u*v+2*a0**2*F.subs(z,u**2/a0**2)
    spatial_flux=s.factor(s.diff(Lstatic,v)/4)
    lapse_flux=s.factor(-s.diff(Lstatic,u)/4)
    mu=s.simplify((lapse_flux.subs(v,u))/u)
    gx,gy,gz=s.symbols('gx gy gz',real=True)
    Lextra=2*a0**2*F.subs(z,(gx**2+gy**2+gz**2)/a0**2)
    lapse_tensor=(s.hessian(Lextra,[gx,gy,gz])/4).subs({gx:0,gy:0,gz:a0*y}).applyfunc(s.simplify)
    checks={'exponential_flux_derived':s.simplify(mu-(1-s.exp(-u/a0)))==0,
            'spatial_metric_equation_independent':spatial_flux==v-u,
            'Newtonian_limit':s.limit(mu,u,s.oo)==1,
            'deep_MOND_limit':s.limit(mu/u,u,0)==1/a0,
            'anisotropic_lapse_Hessian':lapse_tensor==s.diag(s.exp(-y),s.exp(-y),(1-y)*s.exp(-y))}
    energy=s.simplify(y**2-F.subs(z,y**2))
    mu_y=mu.subs(u,a0*y)
    longitudinal=s.diff(y*mu_y,y)
    checks['static_energy_generates_mu']=s.simplify(s.diff(energy,y)/(2*y)-mu_y)==0
    checks['static_energy_quadratic_lower_bound']=s.simplify(energy-y**2+2).is_positive
    checks['longitudinal_eigenvalue_exceeds_transverse']=s.simplify(longitudinal-mu_y).is_positive

    n,B,lam,P,E,pn,pB,pl,pP,pE=s.symbols('n B lam P E pn pB pl pP pE',real=True)
    vp,ve,alpha=s.symbols('vp ve alpha',real=True)
    q=s.symbols('q',positive=True)
    L=-6*vp**2+4*q*vp*(B-ve)+2*q*P**2-4*q*n*P+2*alpha*q*n**2
    velocities=s.solve([s.diff(L,vp)-pP,s.diff(L,ve)-pE],[vp,ve])
    H=s.factor((pP*vp+pE*ve-L).subs(velocities))+lam*pP
    expected=-pP*pE/(4*q)+3*pE**2/(8*q**2)+B*pE-2*q*P**2+4*q*n*P-2*alpha*q*n**2+lam*pP
    checks['Legendre_transform_with_spatial_gauge_retained']=s.cancel(H-expected)==0
    dirac={}
    for label,aval in [('generic',s.Rational(1,2)),('GR',s.S.Zero),('zero_field',s.S.One)]:
        branch=H.subs(alpha,aval)
        if label=='generic':
            branch=branch.subs(q,1)
        dirac[label]=linear_dirac(branch,[n,B,lam,P,E],[pn,pB,pl,pP,pE],[pn,pB,pl])
    # Rational-function field: q != 0 and generic alpha; exceptional alpha=0,1
    # were recomputed above, rather than specializing a generic inverse.
    dirac['generic_symbolic']=linear_dirac(H,[n,B,lam,P,E],[pn,pB,pl,pP,pE],[pn,pB,pl])
    checks['all_linear_preservation_closed']=all(v['preservation_closed'] for v in dirac.values())

    # Time-dependent conserved matter sources; no source is inserted into an EOM.
    rho,stress,rdot,rddot=s.symbols('rho stress rhodot rhoddot',real=True)
    Hsource=H+n*rho+P*stress-B*rdot-E*rddot
    equations=[s.diff(Hsource,n),s.diff(Hsource,B),s.diff(Hsource,lam),
               s.diff(Hsource,P),s.diff(Hsource,pE)]  # E=0, Edot=0 gauge in final equation only
    solved=s.solve(equations,[n,P,pE,pP,B])
    dP=s.factor(solved[P]-solved[P].subs(alpha,0))
    dn=s.factor(solved[n]-solved[n].subs(alpha,0))
    checks['equal_metric_corrections_derived']=s.cancel(dP-dn)==0
    checks['shift_response_unchanged']=s.diff(solved[B],alpha)==0
    checks['momentum_constraint_preserved_by_conservation']=s.diff(Hsource,E)+rddot==0
    static_slip=s.cancel((solved[P]-solved[n]).subs({stress:0,rdot:0,rddot:0}))

    # Mean subtraction: weighted projector, never apply the local CMC constraint at k=0.
    w1,w2=s.symbols('volume1 volume2',positive=True)
    projector=s.eye(2)-s.ones(2,1)*s.Matrix([[w1,w2]])/(w1+w2)
    checks['homogeneous_trace_not_constrained']=(projector*s.ones(2,1)).applyfunc(s.cancel)==s.zeros(2,1)
    checks['weighted_projector_idempotent']=(projector*projector-projector).applyfunc(s.cancel).is_zero_matrix
    scale,adot,N,Lambda,M=s.symbols('scale adot N Lambda M_dust',positive=True)
    L0=-6*scale*adot**2/N-2*Lambda*N*scale**3-N*M
    lapse0=s.diff(L0,N)
    Hubble2=s.factor(s.solve(lapse0,adot**2)[0]/(N**2*scale**2))
    checks['FLRW_Friedmann_from_lapse']=s.cancel(Hubble2-(Lambda/3+M/(6*scale**3)))==0

    # k=0 exact minisuperspace, with minimally coupled irrotational dust clock.
    # Dust reduces to p_T dot(T)-N p_T on its future-directed homogeneous branch.
    # The homogeneous mean-subtracted trace term vanishes identically. Its
    # multiplier is a spectator primary, not an equation setting p_scale=0.
    pscale,pN0,lambda0,plambda0,clock,pclock=s.symbols('p_scale p_N0 lambda0 p_lambda0 clock p_clock',real=True)
    Lgravity0=L0+N*M
    velocity0=s.solve(s.diff(Lgravity0,adot)-pscale,adot)[0]
    Hgravity0=s.factor((pscale*adot-Lgravity0).subs(adot,velocity0))
    Htotal0=Hgravity0+N*pclock
    qs0=[scale,N,lambda0,clock]; ps0=[pscale,pN0,plambda0,pclock]
    def pb0(f,g):
        return s.simplify(sum(s.diff(f,x)*s.diff(g,p)-s.diff(f,p)*s.diff(g,x)
                              for x,p in zip(qs0,ps0)))
    prim0=[pN0,plambda0]
    secondary0=[s.factor(pb0(c,Htotal0)) for c in prim0 if pb0(c,Htotal0)!=0]
    cons0=prim0+secondary0
    matrix0=s.Matrix([[pb0(c,d) for d in cons0] for c in cons0])
    closed0=all(pb0(c,Htotal0)==0 for c in secondary0)
    rank0=matrix0.rank(); fc0=len(cons0)-rank0
    pscale2=s.solve(secondary0[0],pscale**2)[0]
    zero_dirac={'Hamiltonian':str(Htotal0),'primaries':list(map(str,prim0)),
                'secondaries':list(map(str,secondary0)),
                'poisson_matrix':[[str(v) for v in row] for row in matrix0.tolist()],
                'preservation_closed':closed0,'first_class':fc0,'second_class':rank0,
                'physical_pairs_including_dust_clock':int(len(qs0)-fc0-s.Rational(rank0,2)),
                'expanding_momentum_squared':str(pscale2),
                'clock_rate':str(s.diff(Htotal0,pclock)),
                'scope':'Exact homogeneous isotropic sector only; the physical global pair includes the matter clock, not a local scalar graviton.'}
    checks['homogeneous_canonical_preservation_closed']=closed0
    checks['homogeneous_canonical_matches_lapse']=s.cancel(
        (velocity0**2/(N**2*scale**2)).subs(pscale**2,pscale2)-Hubble2.subs(M,pclock))==0

    # Tensor principal action from the traceless metric kinetic/spatial blocks.
    hp,hc,dp,dc,frequency=s.symbols('hp hc dp dc frequency',real=True)
    tensor=s.Matrix([[hp,hc,0],[hc,-hp,0],[0,0,0]])
    tensor_dot=tensor.subs({hp:dp,hc:dc})
    Ltt=(s.trace(tensor_dot*tensor_dot)-q*s.trace(tensor*tensor))/4
    Ktt=s.hessian(Ltt,[dp,dc]); Vtt=-s.hessian(Ltt.subs({dp:0,dc:0}),[hp,hc])
    tensor_roots=s.solve(s.det(frequency*Ktt-Vtt),frequency)
    checks['tensor_principal_positive_kinetic']=all(v.is_positive for v in Ktt.eigenvals())
    checks['tensor_principal_luminal']=bool(tensor_roots) and all(s.simplify(v/q-1)==0 for v in tensor_roots)

    # Anisotropic principal response, retaining the actual exponential Hessian.
    mt,ml,X,Y,Z,R,t=s.symbols('mu_t mu_l X Y Z R t',positive=True)
    GA=-1/(4*s.pi*mt*s.sqrt(ml)*s.sqrt((X**2+Y**2)/mt+Z**2/ml))
    GI=-1/(4*s.pi*s.sqrt(X**2+Y**2+Z**2))
    diff=GA-GI
    f=t**6  # for t>0; continued as zero for t<0 (C5 at activation)
    deltaP=(f*s.diff(diff,Z,2)+s.diff(f,t,2)*diff)/4
    tidal=(s.diff(deltaP,X,2)+s.diff(deltaP,t,2)).subs({X:R,Y:0,Z:0})
    tidal=s.simplify(tidal)
    witness=tidal.subs({mt:s.Rational(1,2),ml:(1+s.log(2))/2,R:1,t:s.Rational(1,10)})
    # Conservation of an explicitly constructed smooth spatial probe.
    tt,xx,yy,zz=s.symbols('time x y zcoord',real=True)
    ft=s.Function('f')(tt); profile=s.Function('profile')(xx,yy,zz)
    T00=ft*s.diff(profile,zz,2); T0z=-s.diff(ft,tt)*s.diff(profile,zz)
    Tzz=s.diff(ft,tt,2)*profile
    checks['probe_conserved']=s.simplify(s.diff(T00,tt)+s.diff(T0z,zz))==0 and s.simplify(s.diff(T0z,tt)+s.diff(Tzz,zz))==0
    checks['anisotropic_Green_off_source']=s.simplify(mt*(s.diff(GA,X,2)+s.diff(GA,Y,2))+ml*s.diff(GA,Z,2))==0
    return {'checks':{k:bool(v) for k,v in checks.items()},'python':platform.python_version(),'sympy':s.__version__,
            'F':str(F),'static_flux':str(lapse_flux),'mu':str(mu),'static_slip_residual':str(static_slip),
            'static_energy_primitive':str(energy),'static_energy_zero_field_series':str(s.series(energy,y,0,5)),
            'lapse_gradient_Hessian':[[str(v) for v in row] for row in lapse_tensor.tolist()],
            'quadratic_Hamiltonian':str(H),'sourced_Hamiltonian':str(Hsource),
            'sourced_solution':{str(k):str(v) for k,v in solved.items()},
            'dirac':dirac,'homogeneous_dirac':zero_dirac,'homogeneous_Friedmann_H_squared':str(Hubble2),
            'homogeneous_expanding_H_squared':float(Hubble2.subs({Lambda:3,M:6,scale:1})),
            'tensor_kinetic_eigenvalues':{str(k):v for k,v in Ktt.eigenvals().items()},
            'tensor_frequency_squared':list(map(str,tensor_roots)),
            'principal_tidal_formula':str(tidal),'principal_tidal_probe':float(witness),
            'GR_tidal_difference':str(s.simplify(tidal.subs({mt:1,ml:1}))),
            'nonlinear_DOF_certified':False,
            'scope':'Exact static leading weak-field and homogeneous reductions of stated preferred-foliation Hamiltonian; complete fixed-mode quadratic constraints; anisotropic frozen principal causal probe, not complete finite-background perturbations.',
            'runtime_seconds':round(time.monotonic()-start,3)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--require-clean-principal-causality',action='store_true')
    args=p.parse_args(); result=derive()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    for i,(name,ok) in enumerate(result['checks'].items(),1):
        print('[{}] {} {}'.format('ok' if ok else 'FAIL',i,name))
    print('Quadratic scalar counts:',{k:v['scalar_mode_count'] for k,v in result['dirac'].items()})
    print('Poisson ranks:',{k:v['bracket_rank'] for k,v in result['dirac'].items()})
    print('FLRW H^2:',result['homogeneous_Friedmann_H_squared'])
    print('Principal tidal probe outside GR cone:',result['principal_tidal_probe'])
    print('Full nonlinear/covariant theory: NOT CERTIFIED')
    raise SystemExit(1 if not all(result['checks'].values()) else
                     2 if args.require_clean_principal_causality and result['principal_tidal_probe']!=0 else 0)
