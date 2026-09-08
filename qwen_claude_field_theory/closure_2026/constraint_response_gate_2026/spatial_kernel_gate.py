"""Same trace-constraint action plus a general spatial slip kernel.

Full additional term: (m/2) int dT <sqrt(N) I, F_T(-Delta_h)sqrt(N) I>_h,
I=R[h]-4 D_i a^i-2 a_i a^i, a_i=D_i ln N, m=M^2.
F is real self-adjoint on specified mean-zero spatial modes, local in time.
No time derivatives are added. Spectral inverse/boundary prescriptions are
part of the candidate, not proved healthy by this quadratic calculation.
The homogeneous I=0 background equations are unchanged. A flat-FLRW
quadratic coefficient Q=m*kappa^2+8*m*kappa^4 F is then varied exactly.
Positive/unbounded Q fails; a negative bounded Q can pass the matter gate.
No full nonlinear gravitational count or causal certificate is claimed.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys
import sympy as s

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'vcdm_flrw_gate_2026'))
sys.path.insert(0, str(BASE/'lapse_braiding_gate_2026'))
import vcdm_flrw
import conformal_action


def pb(f,g,q,p):
    return s.expand(sum(s.diff(f,x)*s.diff(g,y)-s.diff(f,y)*s.diff(g,x)
                        for x,y in zip(q,p)))


def constant_potential_counterexample(kinetic, symbols):
    """Exact nonunit-lapse P=X-V0 background, not an off-shell sign fixture."""
    Q,Z,D,q,M=symbols
    t,V0=s.symbols('T V0',positive=True)
    m=M*M
    rho=m/(3*t*t)
    lapse_factor=1-3*V0*t*t/m
    N=1/lapse_factor
    a=t**s.Rational(1,3)*lapse_factor**(-s.Rational(1,6))
    q2=2*(rho-V0)
    qbg=s.sqrt(q2)
    phi=-1/t
    H=s.factor(s.diff(a,t)/(a*N))
    charge_drift=s.factor(s.diff(a**3*qbg,t))
    residuals=[s.factor(3*m*H**2-rho),s.factor(3*H+phi),
        s.factor(s.diff(phi,t)/N-3*q2/(2*m)),charge_drift,
        s.factor(s.diff(rho,t)/N+3*H*q2)]
    base={Z:1,D:1,q*q:q2}
    fixed=s.factor(kinetic.subs(Q,-rho/2).subs(base))
    tracked=s.factor(kinetic.subs(Q,-m/(6*t*t*N)).subs(base))
    fixture={M:s.sqrt(3),t:1,V0:s.Rational(1,2)}
    return dict(domain='T,M>0; 0<V0<M^2/(3T^2), ensuring q^2,N>0',
        rho=rho,N=N,a=a,q_squared=q2,phi=phi,H=H,
        background_residuals=residuals,
        fixed_kinetic=fixed,adaptive_kinetic=tracked,
        fixed_fixture_kinetic=s.simplify(fixed.subs(fixture)),
        adaptive_fixture_kinetic=s.simplify(tracked.subs(fixture)))


def canonical_zero(L,u,ud,aux,a):
    """Rebuild at Q=0; a vanishing potential Hessian is not a Dirac rank."""
    coords=[u,*aux]
    pu,pn,pz,pv=mom=list(s.symbols('pu pn pz pv', real=True))
    primary=[pn,pz,pv]
    L=a**3*L
    vel=s.solve(pu-s.diff(L,ud),ud)[0]
    H=s.factor((pu*ud-L).subs(ud,vel))
    secondary=[s.factor(pb(c,H,coords,mom)) for c in primary]
    cons=primary+secondary
    Omega=s.Matrix([[pb(c,b,coords,mom) for b in cons] for c in cons])
    rank=Omega.rank()
    multiplier_matrix=s.Matrix([[pb(c,b,coords,mom) for b in primary]
                                for c in secondary])
    explicit_time=s.Matrix(s.symbols('Ct_n Ct_z Ct_v'))
    drift=s.Matrix([pb(c,H,coords,mom) for c in secondary])+explicit_time
    multipliers=-multiplier_matrix.inv()*drift
    residuals=list((multiplier_matrix*multipliers+drift).applyfunc(s.simplify))
    solution=s.solve(cons,[*aux,pn,pz,pv],dict=True)[0]
    Hred=s.factor(H.subs(solution))
    return dict(primary=primary,secondary=secondary,matrix=Omega,rank=rank,
                first_class=len(cons)-rank,second_class=rank,
                matter_pairs=s.Rational(2*len(coords)-2*(len(cons)-rank)-rank,2),
                Hred=Hred,matter_velocity=s.diff(Hred,pu),
                explicit_constraint_time_derivatives=list(explicit_time),
                preservation_residuals=residuals,
                scope='Gauge-fixed quadratic scalar-plus-matter model, not full gravity')


@lru_cache(None)
def derive():
    raw=vcdm_flrw.derive_nonzero_mode()
    a,M,k,q,Z,D,alpha,u,ud=[raw[x] for x in ('a','M','k','q','Z','D','alpha','u','ud')]
    n,z,v=raw['auxiliaries']
    Q=s.Symbol('Q', real=True, nonzero=True)
    cross,lapse=s.symbols('cross lapse', real=True)
    kp2=k**2/a**2
    static=Q*z*z+2*cross*n*z+lapse*n*n
    # Independently require z=-n and the measured fixed static coefficient.
    relation=s.solve(s.diff(static,z),z)[0]
    cross_solution=s.solve(relation+n,cross)[0]
    reduced_static=static.subs(z,-n).subs(cross,cross_solution)
    lapse_solution=s.solve(reduced_static-M**2*kp2*(alpha-1)*n*n,lapse)[0]
    static_fixed=s.factor(static.subs({cross:cross_solution,lapse:lapse_solution}))
    old_spatial=M**2*kp2*(z*z+2*z*n+alpha*n*n)
    L=s.expand(raw['L']-old_spatial+static_fixed)
    control=s.factor(L.subs(Q,M**2*kp2)-raw['L'])
    mond=L.subs(alpha,1)
    aux=[n,z,v]
    equations=[s.diff(mond,x) for x in aux]
    solution=s.solve(equations,aux,dict=True)[0]
    reduced=s.factor(mond.subs(solution))
    kinetic=s.factor(s.diff(reduced,ud,2))
    gradient=s.factor(-s.diff(reduced,u,2))
    omega2=s.factor(gradient/kinetic)
    canonical={Z:1,D:1,Q:-q*q/4}
    fixed_kinetic=s.factor(kinetic.subs(canonical))
    fixed_omega=s.factor(omega2.subs(canonical))

    # Derive the geometric realizer using actual Christoffels of h.
    x,y,w,eps=s.symbols('x y w epsilon',real=True)
    mode=s.cos(k*x)
    h=s.eye(3)*a*a*s.exp(2*eps*z*mode)
    R,_,_=conformal_action._ricci_scalar(h,(x,y,w))
    N=1+eps*n*mode
    volume=a**3*s.exp(3*eps*z*mode)
    gradlog=s.diff(s.log(N),x)
    divacc=s.diff(volume*h.inv()[0,0]*gradlog,x)/volume
    I=R-4*divacc-2*h.inv()[0,0]*gradlog**2
    Ilinear=s.simplify(s.diff(I,eps).subs(eps,0)/mode)
    F=s.Symbol('F',real=True)
    extra=M**2*Ilinear**2*F/2
    Q_from_F=s.factor(s.diff(old_spatial+extra,z,2)/2)
    F_solution=s.solve(Q_from_F-Q,F)[0]
    Q_check=s.factor(Q_from_F.subs(F,F_solution))
    # Different, explicit clock-dependent action: its quadratic coefficient
    # is derived with the physical background lapse retained. The two terms
    # are -m/16 <sqrtN I,K^-1 sqrtN I> and
    # -tau_T/96 <K^-1 I,K^-1 I>, K=-Delta_h on specified nonzero modes.
    Nbar,taudot=s.symbols('Nbar tau_T',positive=True)
    proper_correction=(-M**2*Nbar*Ilinear**2/(16*kp2)
                       -taudot*Ilinear**2/(96*kp2**2))/Nbar
    proper_Q=s.factor(s.diff(old_spatial+proper_correction,z,2)/2)
    source_coefficient_residual=s.factor(proper_Q+taudot/(6*Nbar))
    background_taudot=s.Rational(3,2)*Nbar*q*q*Z
    adaptive_Q=s.factor(proper_Q.subs(taudot,background_taudot))
    adaptive_K=s.factor(kinetic.subs(Q,adaptive_Q))
    adaptive_speed=s.factor(s.limit((gradient/adaptive_K)/kp2,k,s.oo))
    b=s.Symbol('b',positive=True)
    family_correction=(-M**2*Nbar*Ilinear**2/(16*kp2)
                       -b*taudot*Ilinear**2/(24*kp2**2))/Nbar
    family_Q=s.factor(s.diff(old_spatial+family_correction,z,2)/2)
    family_bg_Q=s.factor(family_Q.subs(taudot,background_taudot))
    family_K=s.factor(kinetic.subs(Q,family_bg_Q))
    family_speed=s.factor(s.limit((gradient/family_K)/kp2,k,s.oo))
    # Rebuild the exact zero-enthalpy canonical-matter action BEFORE solving
    # any 1/q auxiliary equation. This diagnoses a nonuniform branch limit;
    # it is not a nonlinear gravitational degree-of-freedom certificate.
    vacuum_L=s.expand(mond.subs({Z:1,D:1}).subs({q:0,Q:0}))
    vacuum_v=s.solve(s.diff(vacuum_L,v),v)[0]
    vacuum_reduced=s.expand(vacuum_L.subs(v,vacuum_v))
    vacuum_speed=s.factor(-s.diff(vacuum_reduced,u,2)
                           /(kp2*s.diff(vacuum_reduced,ud,2)))
    zero_enthalpy=dict(L=vacuum_L,matter_speed2=vacuum_speed,
        lapse_variation=s.diff(vacuum_L,n),trace_variation=s.diff(vacuum_L,z),
        speed_matching_b=s.solve(family_speed.subs({Z:1,D:1})-vacuum_speed,b),
        scope='Exact q=Q=0 canonical quadratic action; not a full nonlinear rank count')
    density=s.factor((q*D*(ud-q*n)).subs(solution))
    matter_background=constant_potential_counterexample(kinetic,(Q,Z,D,q,M))
    zero=canonical_zero(mond.subs(Q,0),u,ud,aux,a)
    residuals=[s.factor(e.subs(solution)) for e in equations]
    residuals += [control,raw['boundary_residual'],raw['background_tadpole_residual']]
    residuals += zero['preservation_residuals']
    residuals += [source_coefficient_residual]+matter_background['background_residuals']
    t=s.Symbol('t',positive=True)
    stiff={a:t**s.Rational(1,3),q:s.sqrt(s.Rational(2,3))*M/t,Z:1,D:1,
           Q:-M**2/(6*t*t)}
    stiffK=s.factor(kinetic.subs(stiff))
    stiffB=s.factor(gradient.subs(stiff))
    return dict(a=a,M=M,k=k,q=q,Z=Z,D=D,alpha=alpha,u=u,ud=ud,n=n,z=z,Q=Q,
                static=dict(cross=cross_solution,lapse=lapse_solution,L=static_fixed),
                L=mond,solution=solution,reduced_L=reduced,kinetic=kinetic,
                gradient=gradient,omega2=omega2,
                large_positive_Q_kinetic=s.limit(kinetic,Q,s.oo),
                large_negative_Q_kinetic=s.limit(kinetic,Q,-s.oo),
                negative_Q_healthy_boundary=s.solve(kinetic,Q)[0],
                canonical_negative=dict(kinetic=fixed_kinetic,
                    UV_speed2=s.limit(fixed_omega/kp2,k,s.oo),
                    gradient=s.factor(gradient.subs(canonical)),
                    gravity_scalar_pairs_claimed=None),
                stiff_example=dict(kinetic=stiffK,gradient=stiffB,
                    friction=s.factor(s.diff(t*stiffK,t)/(t*stiffK)),
                    frequency2=s.factor(stiffB/stiffK),Q_of_T=-M**2/(6*t*t)),
                realizer=dict(I_linear=Ilinear,Q_from_F=Q_from_F,
                    F_symbol=F_solution,reconstructed_Q=Q_check),
                constant_potential=matter_background,
                adaptive=dict(proper_Q=proper_Q,Q_on_background=adaptive_Q,
                    kinetic=adaptive_K,UV_speed2=adaptive_speed,density=density,
                    source_coefficient_residual=source_coefficient_residual,
                    domain='q!=0,Z,D>0 and 0<Z/D<=1; background tau_T/N=(3/2)q^2Z; nonzero spatial mode',
                    zero_enthalpy_warning='The q=0 system must be rebuilt; none of the 1/q auxiliary solutions is inherited'),
                adaptive_family=dict(b=b,Nbar=Nbar,tau_T=taudot,proper_Q=family_Q,
                    Q_on_background=family_bg_Q,kinetic=family_K,UV_speed2=family_speed,
                    n=solution[n],z=s.factor(solution[z].subs(Q,family_bg_Q)),v=solution[v]),
                zero_enthalpy=zero_enthalpy,
                zero_stiffness=zero,old_action_residual=control,residuals=residuals)


def encode(obj):
    if isinstance(obj,dict): return {str(k):encode(v) for k,v in obj.items()}
    if isinstance(obj,s.MatrixBase): return encode(obj.tolist())
    if isinstance(obj,(tuple,list)): return [encode(x) for x in obj]
    if isinstance(obj,s.Integer): return int(obj)
    if isinstance(obj,s.Basic): return str(obj)
    return obj


def run():
    d=derive()
    checks=all(s.simplify(r)==0 for r in d['residuals'])
    if not checks: raise AssertionError('Variational or preservation residual failed')
    fixture=d['canonical_negative']
    healthy=bool(fixture['kinetic']>0 and fixture['UV_speed2']>0
                 and fixture['UV_speed2']<=1)
    return encode(dict(algebra_checks_passed=checks,matter_gate=healthy,result=d,
        full_theory_status='OPEN',
        limitations=['No full nonlinear Dirac count','No physical causal certificate',
                     'Mean-zero inverse operators require a separate k=0 theory',
                     'One healthy expanding canonical-matter branch is not viable cosmology',
                     'Negative spatial stiffness is not certified healthy in all other sectors']))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--require-matter-gate',action='store_true')
    args=ap.parse_args()
    result=run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result,stream,indent=2,sort_keys=True); stream.write('\n')
    print('General reduced kinetic:',result['result']['kinetic'])
    print('Negative-kernel canonical matter gate:',result['matter_gate'])
    print('Full theory:',result['full_theory_status'])
    raise SystemExit(2 if args.require_matter_gate and not result['matter_gate'] else 0)


if __name__=='__main__': main()
