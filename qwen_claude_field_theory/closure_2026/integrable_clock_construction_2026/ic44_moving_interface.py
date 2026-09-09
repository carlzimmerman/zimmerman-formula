"""Necessary moving-interface equations from the actual IC30 radial action.

No full gravitational DOF count, global variational completion, or existence
claim. The split-domain action is a candidate completion of IC39, not an
invertible redefinition of its multiplier at eta=0.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sympy as s
import ic30_radial_bridge as radial


@lru_cache(None)
def derive():
    d=radial.radial_action();r=d['r'];old=d['fields'][:-1];ell=d['fields'][-1]
    fields=s.symbols('S w Q q z shear beta',real=True)
    grads=s.symbols('S_r w_r Q_r q_r z_r shear_r beta_r',real=True)
    seconds=s.symbols('S_rr w_rr Q_rr q_rr z_rr shear_rr beta_rr',real=True)
    S,w,Q,q,z,sh,beta=fields;Sr,wr,Qr,qr,zr,shr,br=grads
    Qt=s.Symbol('Q_t',real=True)
    mapping={**dict(zip(old,fields)),**dict(zip([s.diff(f,r) for f in old],grads)),
             **dict(zip([s.diff(f,r,2) for f in old],seconds)),d['Qdot']:Qt}
    raw=d['L'].subs(ell,0);L=raw.xreplace(mapping);J=d['J'].xreplace(mapping)
    speed,a,db,dq,dh=s.symbols('Rdot a db dq dshear',real=True)
    # Minus-side gradient minus plus-side gradient. Hadamard compatibility
    # at continuous S,w,Q gives [f_t]=-Rdot [f_r]. Only Q_t occurs in L.
    derivative_jump={Sr:Sr-a,wr:wr+a,Qr:Qr-a,br:br+db,Qt:Qt+speed*a}
    full_jump={**derivative_jump,q:q+dq,sh:sh+dh}
    change=lambda expr,sub:s.simplify(expr.subs(sub,simultaneous=True)-expr)
    momenta=[s.diff(L,g) for g in grads]
    momenta[2]-=speed*s.diff(L,Qt)
    normal=[change(p,full_jump)/J for p in momenta]
    normal=[s.simplify(p) for p in normal]
    flux_matrix=s.Matrix([normal[2],normal[6]]).jacobian([dq,dh])
    # First solve the normal metric/shift flux conditions at Rdot+beta !=0.
    flux_solution=s.solve([normal[2],normal[6]],[dq,dh],dict=True)[0]
    # On the strictly monotone z branch, equal q implies equal z. Prove the
    # finite-difference factorization separately; no assumed mode count.
    zz=s.Symbol('z_minus',real=True);D=d['D'].xreplace(mapping);E=d['E4'].xreplace(mapping)
    z_eq=s.diff(L,z)/J
    factor=(zz-z)*(2*D+4*E*(zz**2+zz*z+z**2))
    auxiliary_error=s.simplify(z_eq.subs(z,zz)-z_eq-factor)
    q_jump=change(s.diff(L,q)/J,full_jump).subs(flux_solution)
    shear_jump=change(s.diff(L,sh)/J,full_jump).subs(flux_solution)
    q_jump=s.simplify(q_jump);shear_jump=s.simplify(shear_jump)
    transmission=s.Matrix([q_jump,shear_jump]).jacobian([a,db])
    solution=s.solve([q_jump,shear_jump],[a,db],dict=True)[0]
    residual=s.Matrix([q_jump,shear_jump]).subs(solution).applyfunc(s.simplify)
    # Moving-boundary shape coefficient, with common field traces fixed
    # when R varies: [L - sum(p_normal f_r)]. The fluxes agree after dq=ds=0.
    legendre=L-s.Add(*[p*g for p,g in zip(momenta,grads)])
    shape=change(legendre,derivative_jump)
    # Independent jet-chain derivative of the inactive clock EL expression.
    def dr(expr):
        return s.diff(expr,r)+sum(s.diff(expr,f)*g for f,g in zip(fields,grads))\
             +sum(s.diff(expr,g)*gg for g,gg in zip(grads,seconds))
    inactive=s.diff(L,w)-dr(s.diff(L,wr))
    direct=radial.euler(raw,old[1],r).xreplace(mapping)
    return dict(speed=speed,beta=beta,amplitude=a,db=db,dq=dq,dh=dh,
        normal_flux_jumps=normal,normal_Q_jump=normal[2],normal_beta_jump=normal[6],
        momentum_flux_matrix=flux_matrix,momentum_flux_determinant=s.factor(flux_matrix.det()),
        momentum_flux_generic_rank=flux_matrix.rank(),momentum_flux_solution=flux_solution,
        auxiliary_factor=factor,auxiliary_factorization_error=auxiliary_error,
        q_equation_jump=q_jump,shear_equation_jump=shear_jump,
        transmission_matrix=transmission,transmission_determinant=s.factor(transmission.det()),
        transmission_generic_rank=transmission.rank(),
        transmission_shift_characteristic_rank=transmission.subs(speed,-beta).rank(),
        transmission_solution=solution,transmission_residual=residual,
        shape_jump=shape,inactive_clock_equation=s.factor(inactive/J),
        inactive_clock_direct_identity=s.simplify(inactive-direct),
        phase_action_density=L,scope='Radial split-domain necessary conditions; not full field-theory closure')


def selected_interface():
    """Recompute speed from recorded IC41 jets, not an assigned PPN/speed gate."""
    import mpmath as mp
    import ic37_local_taylor as local
    source=Path(__file__).parent/'ic41_run_001/response80/stdout.txt'
    record=json.loads(source.read_text())
    with mp.workdps(80):
        initial=local.LocalJet().initial
        beta=initial[5]
        speed=-mp.mpf(record['x_t'])/mp.mpf(record['a'])
        relative=speed+beta
        return dict(input=str(source.relative_to(Path(__file__).parent)),
            beta=mp.nstr(beta,60),Rdot=mp.nstr(speed,60),
            relative_to_shift=mp.nstr(relative,60),
            q_jump_coefficient=mp.nstr(2*relative,60),
            implication='Nonzero relative speed forces zero auxiliary first-gradient jump in the stated smooth-metric, monotone-z class',
            exact_interface_solution=False)


if __name__=='__main__':
    from ic43_weighted_multiplier import serial
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');p.add_argument('--selected',action='store_true')
    args=p.parse_args();out=dict(derivation=derive(),full_theory='OPEN')
    if args.selected:out['selected_interface']=selected_interface()
    print(json.dumps(serial(out),indent=2))
    raise SystemExit(2 if args.strict else 0)
