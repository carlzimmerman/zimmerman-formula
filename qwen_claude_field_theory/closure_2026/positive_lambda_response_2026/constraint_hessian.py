"""Exact homogeneous Dirac closure and the nonlinear functional obligation.

Base c759c46ac02e6c09cd0c7c3cb206b8c31bbc1b97. This is NOT a full field
constraint calculation. Delta S_b is identically zero on homogeneous fields.
The time-dependent canonical shift exposes a mixed lapse/conformal Hessian;
every homogeneous bracket below is calculated from canonical functions.
"""
import argparse
from functools import lru_cache
import json
import sympy as s


def pb(f,g,coordinates,momenta):
    return s.expand(sum(s.diff(f,x)*s.diff(g,p)-s.diff(f,p)*s.diff(g,x)
                        for x,p in zip(coordinates,momenta)))


@lru_cache(None)
def derive():
    N,m,ps,td=s.symbols('N m p_sigma tau_dot',positive=True)
    chi,sigma,pc,pn,tau,tdd,Lam=s.symbols('chi sigma p_chi p_N tau tau_ddot Lambda',real=True)
    volume=s.exp(3*chi/2)
    generator=2*tau*volume/3
    correction=s.diff(generator,tau)*td
    old_pchi=s.diff(generator,chi)+pc
    # Original trace is p_chi_old. Terms proportional to the new primary
    # pc are absorbed in its multiplier, never discarded as new equations.
    original_shifted=N*(-old_pchi**2/(3*m*volume)+m*Lam*volume+ps**2/(2*volume))
    H=s.factor(original_shifted.subs(pc,0)+correction)
    removed=s.factor(original_shifted+correction-H)
    rho=ps**2/(2*volume**2)
    coordinates=[N,chi,sigma]
    momenta=[pn,pc,ps]
    primary=[pn,pc]
    secondary=[s.factor(pb(c,H,coordinates,momenta)) for c in primary]
    constraints=primary+secondary
    Omega=s.Matrix([[pb(a,b,coordinates,momenta) for b in constraints] for a in constraints])
    # Solve the actual secondary equations; solve for Lambda merely to
    # parameterize the weak surface, after all Poisson derivatives are taken.
    weak_Lambda=s.solve(secondary[0],Lam)[0]
    weak_N=s.solve(secondary[1].subs(Lam,weak_Lambda),N)[0]
    weak={Lam:weak_Lambda,N:weak_N,pn:0,pc:0}
    apply_weak=lambda expression:s.simplify(expression.subs(weak,simultaneous=True))
    hessian=s.hessian(H,(N,chi))
    weak_hessian=hessian.applyfunc(apply_weak)
    weak_Omega=Omega.applyfunc(apply_weak)
    rank=weak_Omega.rank()
    multiplier_block=s.Matrix([[pb(c,p,coordinates,momenta) for p in primary] for c in secondary])
    explicit_time=lambda expr:s.diff(expr,tau)*td+s.diff(expr,td)*tdd
    drift=s.Matrix([pb(c,H,coordinates,momenta)+explicit_time(c) for c in secondary])
    solved=-(multiplier_block.applyfunc(apply_weak)).inv()*drift.applyfunc(apply_weak)
    solved=solved.applyfunc(s.factor)
    residuals=(multiplier_block.applyfunc(apply_weak)*solved+drift.applyfunc(apply_weak)).applyfunc(s.simplify)
    Hubble=s.factor(solved[1]/(2*weak_N))
    # Exact fixed positive-Lambda member, not its stiff limit.
    t,Hd=s.symbols('t H_d',positive=True)
    vbg=s.sinh(3*Hd*t)
    taubg=-3*m*Hd*s.coth(3*Hd*t)
    substitute={chi:s.Rational(2,3)*s.log(vbg),tau:taubg,
        td:s.diff(taubg,t),tdd:s.diff(taubg,t,2),Lam:3*Hd**2,
        ps:s.sqrt(6*m)*Hd,N:1,pn:0,pc:0}
    # Normalize hyperbolic identities as exact rational functions of exp.
    # Expanding multiple-angle tanh first can leave an identically-zero
    # residual in a form SymPy's generic simplify does not recognize.
    clean=lambda x:s.factor(s.together(x.rewrite(s.exp)))
    background_residuals=[clean(c.subs(substitute,simultaneous=True)) for c in constraints]
    background_residuals += [clean(Hubble.subs(substitute,simultaneous=True)-Hd*s.coth(3*Hd*t)),
        clean(solved[1].subs(substitute,simultaneous=True)-s.diff(s.Rational(2,3)*s.log(vbg),t))]
    lapse_drift=clean(solved[0].subs(substitute,simultaneous=True))
    # At rho=0 the regular inverse must not be inherited. The surface is
    # irregular in matter momentum, so no count follows from these zeros.
    vacuum_sub={ps:0,td:0,Lam:tau**2/(3*m*m)}
    return dict(m=m,N=N,chi=chi,tau=tau,tau_dot=td,tau_ddot=tdd,
        volume=volume,rho=rho,p_sigma=ps,generator=generator,
        clock_correction=correction,H=H,primary_multiple_removed=removed,
        canonical_primary_residual=s.simplify(old_pchi-tau*volume-pc),
        primary_constraints=primary,secondary_constraints=secondary,
        poisson_matrix=Omega,weak_poisson_matrix=weak_Omega,
        weak_hessian=weak_hessian,poisson_rank=rank,
        first_class=len(constraints)-rank,second_class=rank,
        homogeneous_pairs=s.Rational(2*len(coordinates)-2*(len(constraints)-rank)-rank,2),
        multiplier_block=multiplier_block,multipliers=solved,
        explicit_secondary_time_derivatives=[explicit_time(c) for c in secondary],
        preservation_residuals=list(residuals),lapse=weak_N,Hubble=Hubble,
        background_residuals=background_residuals,positive_lambda_lapse_drift=lapse_drift,
        vacuum=dict(raw_constraints=[s.simplify(c.subs(vacuum_sub)) for c in secondary],
            count_claimed=None,reason='Irregular vacuum surface; regular inverse rho is unavailable'),
        scope='Exact nonlinear homogeneous canonical system, not the full nonlocal field-theory operator',
        functional_obligation='Compute the full (N,chi) functional Hessian at fixed canonical shape/matter, including variation of inverse Laplacians, measures, zero-mode projectors and the clock-volume term. Its invertibility on an admissible surface would close the regular scalar multiplier system.')


def encode(value):
    if isinstance(value,dict): return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,s.MatrixBase): return encode(value.tolist())
    if isinstance(value,(list,tuple)): return [encode(x) for x in value]
    if isinstance(value,s.Integer): return int(value)
    if isinstance(value,s.Basic): return str(value)
    return value


def run():
    d=derive()
    residuals=d['preservation_residuals']+d['background_residuals']
    residuals += [d['canonical_primary_residual'],d['positive_lambda_lapse_drift']]
    if not all(s.simplify(x)==0 for x in residuals):
        raise AssertionError('Constraint preservation or background residual is nonzero')
    return encode(dict(checks_passed=True,derivation=d,full_field_count_proved=False))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-field-count',action='store_true')
    args=parser.parse_args(argv)
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
    return 2 if args.require_full_field_count and not result['full_field_count_proved'] else 0


if __name__=='__main__': raise SystemExit(main())
