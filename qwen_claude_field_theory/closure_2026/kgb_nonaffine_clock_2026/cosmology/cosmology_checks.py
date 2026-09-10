#!/usr/bin/env python3
"""Same-action FLRW/mapped-matter and fixed-quadratic-F exclusion diagnostics.

No P/G high-X continuation or CMB likelihood is supplied. Q=2X is a clock norm,
not H/a0. A single global constant a0 is retained throughout.
"""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sympy as s


def flrw_map(H,Xdot,X,C,C1):
    """Physical proper time dot; EF proper time d tau=sqrt(C) dt."""
    return dict(dtau_dt=s.sqrt(C),H_EF=(H+C1*Xdot/(2*C))/s.sqrt(C),
        chi=X/C,chi_dot_EF=(C-X*C1)*Xdot/C**s.Rational(5,2),Q_clock=2*X)


def matter_map(X,C,C1,C2,rho,p,u):
    D=C-X*C1;chi=X/C;T=-rho+3*p;kappa=C*C1/D
    kappa_chi=C*C*C1*C1/D**2+C**4*C2/D**3
    # Homogeneous kinetic addition below is the dust specialization only.
    return dict(Dfield=D,chi=chi,kappa=kappa,kappa_chi=kappa_chi,
        rho_EF=(rho-kappa*chi*T)/C**2,p_EF=p/C**2,
        current_EF=-u*kappa*T/(2*C**2),
        homogeneous_matter_kinetic=rho*(C1*D+2*X*C*C2)/(2*D**3) if p==0 else None)


@lru_cache(None)
def fluid_variation():
    N,a,v,rho0,x,u=s.symbols('N a v rho0 x u',positive=True)
    w,H,acc=s.symbols('w H acc',real=True)
    C=s.Function('C');chi=v*v/(2*N*N);n=(3*w-1)/2
    fbar=rho0*a**(-3*(1+w))*C(x)**n
    f=fbar.subs(x,chi);L=-N*a**3*f
    kap=(s.diff(C(x),x)/C(x)).subs(x,chi)
    rhoEF=-s.diff(L,N)/a**3
    pEF=s.diff(L,a)/(3*N*a*a)
    current=s.diff(L,v)/a**3
    rho_expected=f*(1-chi*kap*(3*w-1))
    current_expected=-v/N*kap*(3*w-1)*f/2
    # Ward/energy exchange identity on physical-fluid conservation, using its
    # conserved comoving-density Routhian rather than EF-minimal dust.
    fu=fbar.subs(x,u*u/2)
    rho_u=fu-u*s.diff(fu,u);J=-s.diff(fu,u)
    Dt=lambda e:s.diff(e,a)*a*H+s.diff(e,u)*acc
    ward=Dt(rho_u)+3*H*(rho_u+w*fu)-u*(Dt(J)+3*H*J)
    return dict(mapped_fluid_Routhian=L,
        residuals={
            'lapse_energy':s.simplify(rhoEF-rho_expected),
            'spatial_pressure':s.simplify(pEF-w*f),
            'shift_current':s.simplify(current-current_expected),
            'mapped_energy_exchange':s.simplify(ward),
            'radiation_trace_free':s.simplify(s.diff(fbar.subs(w,s.Rational(1,3)),x))})


@lru_cache(None)
def homogeneous_action():
    N,a,v,ad,m=s.symbols('N a v ad m',positive=True)
    H,acc=s.symbols('H acc',real=True)
    P,P1,P2,G1,G2,f1,f2=s.symbols('P P1 P2 G1 G2 f1 f2')
    Pu,B,fu=[s.Function(n) for n in ('Pu','B','fu')]
    scalar=N*a**3*Pu(v/N)+3*a*a*ad*B(v/N)
    L=-3*m*a*ad*ad/N+scalar-N*a**3*fu(v/N)
    repl={Pu(v):P,s.diff(Pu(v),v):v*P1,s.diff(Pu(v),v,2):P1+v*v*P2,
        s.diff(B(v),v):v*v*G1,s.diff(B(v),v,2):2*v*G1+v**3*G2,
        s.diff(fu(v),v):v*f1,s.diff(fu(v),v,2):f1+v*v*f2}
    reduce=lambda e:s.expand(e.subs(N,1).doit()).subs(repl).subs(ad,a*H).simplify()
    rho=reduce(-s.diff(scalar,N)/a**3)
    current=reduce(s.diff(scalar,v)/a**3)
    momentum_a=s.diff(scalar.subs(N,1),ad)
    pressure=reduce((s.diff(scalar.subs(N,1),a)
        -s.diff(momentum_a,a)*ad-s.diff(momentum_a,v)*acc)/(3*a*a))
    W=s.hessian(L,(ad,v));S=reduce((W[1,1]-W[0,1]**2/W[0,0])/a**3)
    chi=v*v/2
    expected_S=P1+2*chi*P2+6*H*v*(G1+chi*G2)+6*chi*chi*G1*G1/m-f1-2*chi*f2
    return dict(minisuperspace=L,velocity_Hessian=W,
        homogeneous_clock_coefficient=S,
        residuals={
            'KGB_energy':s.factor(rho-(2*chi*P1-P+6*H*v*chi*G1)),
            'KGB_current':s.factor(current-(v*P1+6*H*chi*G1)),
            'KGB_pressure':s.factor(pressure-(P-2*chi*G1*acc)),
            'actual_Schur_coefficient':s.factor(S-expected_S)})


def quadratic_F(X,j):
    X0=s.Rational(1,2);F0=s.Rational(21,40);f0=s.Rational(1,20)
    F=F0+f0*(X-X0)+j*(X-X0)**2/2
    f=f0+j*(X-X0);C=2*F;C1=2*f
    return dict(F=s.expand(F),C=s.expand(C),f=f,C1=C1,C2=2*j,
                Dfield=s.expand(C-X*C1),tensor_G_ratio=s.Rational(21,20)/C)


def first_upper_barrier(j):
    if j>0:X=s.sqrt(s.Rational(1,4)+1/j);kind='field_map_zero'
    elif j<0:
        X=s.Rational(1,2)+(-s.Rational(1,20)-s.sqrt(s.Rational(1,400)-s.Rational(21,20)*j))/j
        kind='F_zero'
    else:return dict(kind='no_finite_F_or_map_barrier',X=None,Q=None)
    return dict(kind=kind,X=X,Q=2*X)


def quadratic_scan():
    result=[]
    for j in map(s.Integer,(-100000,-10000,0,10000,100000)):
        barrier=first_upper_barrier(j);rows=[]
        for Q in (s.Integer(1),s.Rational(1001,1000),s.Rational(101,100),s.Integer(10),s.Integer(1000000)):
            a=quadratic_F(Q/2,j)
            rows.append(dict(Q=Q,**a,positive_F=bool(a['F']>0),nonzero_map=bool(a['Dfield']!=0),
                connected_to_seed=bool(barrier['Q'] is None or Q<barrier['Q'])))
        result.append(dict(j=j,first_barrier=barrier,rows=rows))
    return result


@lru_cache(None)
def jet_ambiguity():
    X,lam=s.symbols('X lambda');X0=s.Rational(1,2)
    deltaP=lam*(X-X0)**3;C=1+X/10;chi=X/C
    Pt=deltaP/C**2;Pt1=s.diff(Pt,X)/s.diff(chi,X)
    rho=2*chi*Pt1-Pt
    return dict(same_seed_2jet=[s.diff(deltaP,X,n).subs(X,X0) for n in range(3)],
                early_EF_energy_lambda_coefficient=s.factor(s.diff(rho,lam).subs(X,2)))


def l121_recheck():
    c=2.998e8;H0=67.4e3/3.0857e22;a0=9.3619e-11;z=1090.
    E=math.sqrt(9.2e-5*(1+z)**4+.315*(1+z)**3+.685)
    ratio0=a0/(c*H0);ratio=a0/(c*H0*E)
    examples=[dict(mode_amplitude=A,ck_over_aH=k,g_over_global_a0=k*A/ratio)
              for A,k in ((1e-5,1),(1e-6,1),(1e-5,10))]
    return dict(benchmark='L121 LCDM expansion arithmetic, NOT this action cosmology',
        Hrec_over_H0=E,ratio_today=ratio0,ratio_constant=ratio,
        ratio_H_tracking_hypothesis=ratio0,global_a0_parameter=a0,
        z_equality_baryon_only=.049/9.2e-5-1,z_equality_LCDM=.315/9.2e-5-1,
        mode_examples=examples,scope='No CMB on/off switch, no likelihood or clustering theorem')


def serial(value):
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(v) for v in value]
    if isinstance(value,s.MatrixBase):return [[serial(v) for v in row] for row in value.tolist()]
    if isinstance(value,s.Basic):return dict(exact=str(value),numeric=str(s.N(value,30))) if not value.free_symbols else str(value)
    return value


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    result=dict(fluid=fluid_variation(),homogeneous=homogeneous_action(),
        quadratic_F_only=quadratic_scan(),jet_ambiguity=jet_ambiguity(),L121=l121_recheck())
    output=json.dumps(serial(result),indent=2)+'\n'
    if args.result_file:args.result_file.write_text(output)
    else:print(output)
    return 0


if __name__=='__main__':raise SystemExit(main())
