#!/usr/bin/env python3
"""Exact frozen scalar-action response, NOT nonlinear gravity certification.

Variables: physical spatial perturbation z=u-b*n, lapse n, scalar shift B.
q=|k|^2>0, Fourier time convention exp(-i*w*t), physical Psi=-z.
The E=0 scalar spatial gauge follows the previous principal Dirac analysis;
this script does not purport to redo a nonlinear constraint count.
"""
import argparse
import json
from functools import lru_cache
import sympy as s


@lru_cache(None)
def derive():
    m,q,mu=s.symbols('m q mu',positive=True)
    b,d,r,w=s.symbols('b d r omega',real=True)
    u,n,B,ud,rho,S=s.symbols('u n B ud rho stress')
    z=u-b*n
    K=s.diag(ud+q*B,ud,ud)
    kinetic=m*(s.trace(K*K)-s.trace(K)**2)/2+m*d*s.trace(K)**2/3
    potential=m*q*(r*(z+n)**2-mu*n*n)
    source=-n*rho+z*S-s.I*w*B*rho
    L=kinetic+potential+source
    eq=[s.diff(L,u)+s.I*w*s.diff(L,ud),s.diff(L,n),s.diff(L,B)]
    eq=[s.expand(e.subs(ud,-s.I*w*u)) for e in eq]
    sol=s.solve(eq,[u,n,B])
    R=s.factor((-q*n+s.I*w*q*B+3*w*w*z).subs(sol))
    residuals=[s.simplify(s.factor(e.subs(sol))) for e in eq]
    # Vacuum action reduction derives, rather than supplies, dispersion.
    vacuum=kinetic+potential
    aux=s.solve([s.diff(vacuum,n),s.diff(vacuum,B)],[n,B])
    reduced=s.factor(vacuum.subs(aux))
    A=s.factor(s.diff(reduced,ud,2)/2)
    speed2=s.factor(-s.diff(reduced,u,2)/(2*q*A))
    contact=s.factor(s.limit(R/w**2,w,s.oo))
    tuned=s.factor(R.subs({b:0,r:-1,d:1+mu}))
    tuned_contact=s.factor(s.limit(tuned,w,s.oo))
    static={w:0,S:0}
    # Both potentials independently extracted from the varied equations.
    static_n=s.factor(sol[n].subs(static))
    static_z=s.factor(z.subs(sol).subs(static))
    unbraided=s.factor(s.limit(R.subs(b,0),w,s.oo))
    # Necessary zero-order contact-locality conditions: allow r(mu), fix d.
    h=s.symbols('h',real=True)
    density_contact=s.factor(2*m*s.diff(unbraided,rho))
    r_family=s.solve(density_contact-h,r)[0]
    recovered_speed=s.factor(speed2.subs(b,0).subs(r,r_family).subs(h,1))
    # A compact divergence-free source with T00=T0i=0:
    # Txx=partial_y^2 f, Tyy=partial_x^2 f, Txy=-partial_x partial_y f.
    # In Fourier space its trace is -X*f and its divergence vanishes exactly.
    kx,ky,kz,mt,ml=s.symbols('kx ky kz mu_t mu_l',real=True)
    X=kx*kx+ky*ky; Z=kz*kz; D=mt*X+ml*Z
    T=s.Matrix([[-ky*ky,kx*ky,0],[kx*ky,-kx*kx,0],[0,0,0]])
    divergence=T*s.Matrix([kx,ky,kz])
    tuned_transverse=s.factor(tuned_contact.subs({rho:0,S:-X,mu:D/(X+Z)}))
    # Extend the compact vacuum-data obstruction to every constant d>1
    # with density-contact matching r=1-d, without inserting a remainder.
    matched={b:0,r:1-d}
    udd=-speed2.subs(matched)*q*u
    Rvac=-q*aux[n].subs(matched)-q*s.diff(aux[B],ud)*udd-3*udd
    Rvac_residual=s.factor(Rvac-q*u)
    mtp,mlp,Xp,Zp=s.symbols('mu_t mu_l X Z',positive=True)
    qp=Xp+Zp; Dp=mtp*Xp+mlp*Zp; Ep=(d-1)*qp+Dp
    omega2=s.factor((speed2.subs(matched)*q).subs({mu:Dp/qp,q:qp}))
    fourth=s.factor(omega2**2*qp*Ep)
    numerator=s.factor(fourth*Ep)
    quotient,remainder=s.div(s.expand(numerator),Ep,Xp)
    return dict(symbols=(m,q,mu,b,d,r,w,rho,S),L=L,equations=eq,
                solution=sol,residuals=residuals,R00=R,reduced_L=reduced,
                kinetic=A,speed2=speed2,omega2_contact=contact,
                static_n=static_n,static_z=static_z,tuned_R00=tuned,
                tuned_contact=tuned_contact,unbraided_contact=unbraided,
                constant_density_contact_r=r_family,
                GR_contact_matched_speed2=recovered_speed,
                transverse_source_divergence=divergence,
                tuned_transverse_source_contact=tuned_transverse,
                matched_vacuum_R00_residual=Rvac_residual,
                matched_initial_u=Ep,matched_initial_n=-(d-1)*qp,
                matched_fourth_derivative=fourth,
                matched_vacuum_remainder=s.factor(remainder),
                matched_division_residual=s.factor(numerator-quotient*Ep-remainder))


def serial(value):
    if isinstance(value,dict):
        return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [serial(v) for v in value]
    return str(value)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-closure',action='store_true')
    args=parser.parse_args()
    a=derive()
    if any(e!=0 for e in a['residuals']):
        raise ArithmeticError('action variation residual failed')
    print(json.dumps(serial(a),indent=2,sort_keys=True))
    print('STATUS=OPEN: exact principal response only; no full theory certificate')
    return 2 if args.require_closure else 0


if __name__=='__main__':
    raise SystemExit(main())
