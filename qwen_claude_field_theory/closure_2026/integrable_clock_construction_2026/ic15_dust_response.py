#!/usr/bin/env python3
"""IC15: covariant dust response and a separate pure-source potential repair."""
import argparse
import json
import mpmath as mp
import sympy as sp
import ic14_matter_square as clock


def potential(z, q, t, kind='repaired'):
    if kind == 'square':
        return (z-q)**2/(2*t)
    if kind != 'repaired':
        raise ValueError('Unknown auxiliary potential')
    return (z*z/2+q**3/z-3*q*q/2)/(3*t)


def raw(S, z, b=0, Y=0, t='0.1', kind='repaired'):
    j = clock.branch_jets(S)
    z, b, Y, t = map(mp.mpf, (z,b,Y,t))
    if z <= 0 or b < 0 or Y < 0 or t <= 0:
        raise ValueError('Require z,t>0 and b,Y>=0')
    return j['F']-potential(z,j['z0'],t,kind)+z*Y-b*mp.sqrt(z)


def response(S, z, b=0, Y=0, t='0.1', kind='repaired', at_velocity_fold=False):
    j = clock.branch_jets(S)
    z, b, Y, t = map(mp.mpf, (z,b,Y,t))
    if z <= 0 or b < 0 or Y < 0 or t <= 0:
        raise ValueError('Require z,t>0 and b,Y>=0')
    q, qx, qxx, X = (j[k] for k in ('z0','z0X','z0XX','X'))
    if kind == 'square':
        Vz, Vzz = (z-q)/t, 1/t
        LX = j['FX']+(z-q)*qx/t
        LXX = j['FXX']-qx*qx/t+(z-q)*qxx/t
        LXz = qx/t
    elif kind == 'repaired':
        Vz, Vzz = (z-q**3/z**2)/(3*t), (1+2*q**3/z**3)/(3*t)
        LX = j['FX']+(q-q*q/z)*qx/t
        LXX = j['FXX']+((1-2*q/z)*qx*qx+(q-q*q/z)*qxx)/t
        LXz = q*q*qx/(t*z*z)
    else:
        raise ValueError('Unknown auxiliary potential')
    Lz, Lzz = -Vz+Y-b/(2*mp.sqrt(z)), -Vzz+b/(4*z**mp.mpf('1.5'))
    M = mp.diag([LX+2*X*LXX,z])
    cross = mp.matrix([mp.sqrt(2*X)*LXz,mp.sqrt(2*Y)])
    D = mp.diag([LX,z])
    K = None if at_velocity_fold else M-cross*cross.T/Lzz
    A = Lzz-(cross.T*M**-1*cross)[0] if mp.det(M) else mp.nan
    bracket = mp.matrix([[0,A],[-A,0]])
    if mp.isfinite(A):
        _,singular,_ = mp.svd(bracket)
        rank = sum(value > mp.mpf('1e-35') for value in singular)
    else:
        rank = None
    Hpp = M**-1+(M**-1*cross*cross.T*M**-1)/A if A and mp.isfinite(A) else None
    healthy = bool(K is not None and D[0,0] > 0 and K[0,0] >= D[0,0] and K[0,0] > 0)
    chart = bool(mp.exp(-mp.mpf(S)) < z < 1)
    return dict(**j, z=z, b=b, Y=Y, t=t, potential=kind,
                pressure=j['F']-potential(z,q,t,kind)+z*Y-b*mp.sqrt(z),
                constraint=Lz,Lzz=Lzz,M=M,K=K,D=D,
                canonical_auxiliary_schur_z=A,canonical_auxiliary_bracket=bracket,
                computed_auxiliary_rank=rank,
                reduced_clock_momentum_hessian=Hpp[0,0] if Hpp is not None else mp.nan,
                clock_probe_speed_squared=D[0,0]/K[0,0] if K is not None else mp.nan,
                healthy_clock_probe=healthy, inside_original_chart=chart,
                physical_activation_checked=False,full_dust_characteristics_checked=False)


def square_dust_fold(S,t='0.1'):
    q = clock.branch_jets(S)['z0']
    t = mp.mpf(t)
    z = q/3
    b = 4*q**mp.mpf('1.5')/(3*mp.sqrt(3)*t)
    return response(S,z,b=b,t=t,kind='square',at_velocity_fold=True)


def axis_state(S,b=0,Y=0,t='0.1'):
    b,Y,t = map(mp.mpf,(b,Y,t))
    if b < 0 or Y < 0 or t <= 0 or (b > 0 and Y > 0):
        raise ValueError('Require a pure b>=0 or Y>=0 source and t>0')
    q = clock.branch_jets(S)['z0']
    if b:
        d = 3*t*b/4
        r = q**3/(mp.sqrt(q**3+d*d)+d)
        z = r**(mp.mpf(2)/3)
    elif Y:
        y = 3*t*Y/q
        h = mp.findroot(lambda h:h**3-y*h*h-1,(1,1+y),solver='bisect',
                        tol=mp.power(10,-mp.mp.dps+8),maxsteps=5*mp.mp.dps)
        z = q*h
    else:
        z = q
    return response(S,z,b=b,Y=Y,t=t)


def mixed_degeneracy(S,t='0.1'):
    q = clock.branch_jets(S)['z0']
    t = mp.mpf(t)
    return response(S,q,b=4*q**mp.mpf('1.5')/t,Y=2*q/t,t=t,at_velocity_fold=True)


def identities():
    z,q,t,n,b = sp.symbols('z q t n b',positive=True)
    V = potential(z,q,t)
    Vz,Vzz = sp.diff(V,z),sp.diff(V,z,2)
    critical_b = 4*q**sp.Rational(3,2)/(3*sp.sqrt(3)*t)
    square_constraint = -(z-q)/t-b/(2*sp.sqrt(z))
    return dict(dust_conformal_density=sp.simplify(z**2*n*z**sp.Rational(-3,2)-n*sp.sqrt(z)),
                radiation_conformal_density=sp.simplify(z**2*(n*z**sp.Rational(-3,2))**sp.Rational(4,3)-n**sp.Rational(4,3)),
                square_fold_constraint=sp.simplify(square_constraint.subs({z:q/3,b:critical_b})),
                square_fold_curvature=sp.simplify(sp.diff(square_constraint,z).subs({z:q/3,b:critical_b})),
                repair_vacuum_value=sp.simplify(V.subs(z,q)),
                repair_vacuum_stationarity=sp.simplify(Vz.subs(z,q)),
                repair_vacuum_curvature=sp.simplify(Vzz.subs(z,q)-1/t),
                dust_monotonicity=sp.simplify(Vz+2*z*Vzz-(z+q**3/z**2)/t))


def report():
    mp.mp.dps=50
    fields=('S','z','b','Y','constraint','Lzz','canonical_auxiliary_schur_z',
            'computed_auxiliary_rank','clock_probe_speed_squared','healthy_clock_probe',
            'inside_original_chart','physical_activation_checked','full_dust_characteristics_checked')
    compact=lambda bg:{**{k:bg[k] for k in fields},'bare_clock_kinetic':bg['M'][0,0],
                       'clock_gradient':bg['D'][0,0],
                       'clock_kinetic':bg['K'][0,0] if bg['K'] is not None else None}
    return dict(candidate='IC15 separate pure-source potential repair',full_theory='OPEN',
                exact_checks={k:v == 0 for k,v in identities().items()},
                square_dust_folds=[compact(square_dust_fold(S)) for S in ('.03','.1','.2')],
                repaired_axes=[compact(axis_state('.1',**{source:density}))
                               for source in ('b','Y') for density in ('0','.001','.01','.1','1','100','1000000')],
                mixed_raw_degeneracy=compact(mixed_degeneracy('.1')),
                nonclaims=['Pure-axis root regularity does not prove all-density clock health',
                           'Mixed-source statement concerns fixed-X raw auxiliary-root regularity only',
                           'Dust velocity and density perturbations and radiation cosmology are not calculated here',
                           'Original chart, activation, global action, and phenomenology require separate control'])


def completion_status(result, require_full_closure=False):
    """Identity failures are errors; documented physical controls are results."""
    if not result['exact_checks'] or not all(result['exact_checks'].values()):
        return 1
    return 2 if require_full_closure else 0


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args(argv)
    result=report()
    print(json.dumps(result,indent=2,default=lambda value:mp.nstr(value,24)))
    return completion_status(result,args.require_full_closure)


if __name__=='__main__':
    raise SystemExit(main())
