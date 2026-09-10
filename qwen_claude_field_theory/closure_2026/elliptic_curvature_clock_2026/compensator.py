#!/usr/bin/env python3
"""Constructive elliptic-curvature/clock gate, not a completed gravity theory.

S/m = int N sqrt(h) [ exp(2chi)/2 (R3+KijKij-K^2)-Lambda+f(a)
    +2(Dchi)^2+4 Dchi.a+2chi a^2+2exp(2chi)/3(K-Kbar_NF)^2+nu(t)chi ] + Sm/m.
Kbar_NF uses the weight N sqrt(h) exp(2chi); local kinetic ratio stays d=2.
Variation of the GLOBAL nu imposes int N sqrt(h) chi=0, not chi(x)=0.
Principal calculations are at leading weak-field order chi_bar=0, Kbar=0,
with arbitrary finite acceleration y. The homogeneous calculation is exact.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import sympy as s

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('dirac_engine',BASE/'g03_global_kernel_bridge_2026/metric_constraint.py')
engine=importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


def pb(f,g,qs,ps):
    return s.simplify(sum(s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q) for q,p in zip(qs,ps)))


def scalar():
    m,k=s.symbols('m k',positive=True)
    alpha=s.symbols('alpha',real=True)
    z,E,n,B,chi,zd,Ed,pz,pE,pn,pB,pc=s.symbols('z E n B chi zd Ed pz pE pn pB pc',real=True)
    K=s.diag(zd+k*k*(B-Ed),zd,zd)
    kin=m*(s.trace(K*K)-s.trace(K)**2)/2+2*m*s.trace(K)**2/3
    pot=m*k*k*(z*z+2*n*z+alpha*n*n+2*chi*chi+4*chi*(z+n))
    L=s.expand(kin+pot)
    vel=s.solve([s.diff(L,zd)-pz,s.diff(L,Ed)-pE],[zd,Ed])
    H=s.factor((pz*zd+pE*Ed-L).subs(vel))
    qs,ps=[z,E,n,B,chi],[pz,pE,pn,pB,pc]
    dc={name:engine.linear_dirac(H.subs(alpha,av),qs,ps,[pn,pB,pc])
        for name,av in [('generic',alpha),('zero_field',s.S.One),('radial_turnover',s.S.Zero)]}
    # Eliminate action-derived auxiliaries; gauge coordinate retained above.
    Lg=L.subs(Ed,0)
    aux=s.solve([s.diff(Lg,x) for x in (B,n,chi)],[B,n,chi])
    red=s.factor(Lg.subs(aux))
    A=s.factor(s.diff(red,zd,2)/2)
    cs2=s.factor(-s.diff(red,z,2)/(2*k*k*A))
    lapse_aux_hessian=s.hessian(pot,[n,chi])
    y=s.symbols('y',positive=True)
    return dict(L=L,H=H,auxiliaries=aux,reduced_L=red,kinetic=A,
                kinetic_m1=A.subs(m,1),speed_squared=cs2,
                radial_cs2_y2=cs2.subs(alpha,-s.exp(-2)),
                zero_field_cs2=cs2.subs(alpha,1),
                lapse_aux_hessian=lapse_aux_hessian,
                lapse_aux_determinant=s.factor(lapse_aux_hessian.det())),dc


def homogeneous():
    m,A,N=s.symbols('m A N',positive=True)
    Lam,chi,nu,T,adot,pA,pN,pc,pnu,pT=s.symbols('Lambda chi nu T adot pA pN pc pnu pT',real=True)
    F=s.exp(2*chi)
    L=-3*m*F*A*adot**2/N-m*Lam*N*A**3+m*N*A**3*nu*chi
    vel=s.solve(s.diff(L,adot)-pA,adot)[0]
    H=s.factor((pA*adot-L).subs(adot,vel))+N*pT
    qs,ps=[A,N,chi,nu,T],[pA,pN,pc,pnu,pT]
    primary=[pN,pc,pnu]
    generated=[pb(c,H,qs,ps) for c in primary]
    surface={chi:0,nu:pA**2/(6*m*m*A**4),pT:pA**2/(12*m*A)-m*Lam*A**3}
    weak=lambda f:s.factor(f.subs(surface,simultaneous=True))
    # Equivalent normalized secondaries are derived from the raw equations.
    C=-generated[0]
    D=s.factor(generated[1]/(m*N*A**3))
    Z=s.factor(generated[2]/(m*N*A**3))
    cons=primary+[C,D,Z]
    bracket=s.Matrix([[weak(pb(c,e,qs,ps)) for e in cons] for c in cons])
    multipliers=s.symbols('uN uc unu')
    HT=H+sum(u*c for u,c in zip(multipliers,primary))
    preserved=[weak(pb(c,HT,qs,ps)) for c in cons]
    solved=s.solve(preserved,multipliers,dict=True)[0]
    residuals=[s.factor(e.subs(solved)) for e in preserved]
    rank=bracket.rank();fc=len(cons)-rank
    return dict(L=L,H=H,primaries=primary,raw_secondaries=generated,
                normalized_secondaries=[C,D,Z],constraint_residuals=[weak(c) for c in (C,D,Z)],
                poisson_matrix_on_surface=bracket,bracket_rank=rank,first_class=fc,second_class=rank,
                matter_inclusive_pairs=len(qs)-fc-s.Rational(rank,2),
                primary_multiplier_solution=solved,preservation_residuals=residuals,
                H_squared=s.factor((vel**2/(N*N*A*A)).subs(chi,0).subs(pA**2,12*m*A*(pT+m*Lam*A**3))),
                global_multiplier_on_branch=surface[nu])


def response():
    """Vary conserved-source scalar action and compute Ricci, not just lapse.
    All amplitudes may be complex; source convention exp(-i omega t).
    Source L=-n rho+z S+B rho_dot+E rho_ddot. E is gauge-fixed only here,
    following the independent momentum/Dirac audit. TT has zero Ricci-00
    contribution; transverse vector sources do not enter this contraction.
    """
    m,k=s.symbols('m k',positive=True)
    alpha,w=s.symbols('alpha omega',real=True)
    z,n,B,chi,zd,rho,S=s.symbols('z n B chi zd rho stress')
    K=s.diag(zd+k*k*B,zd,zd)
    L=m*(s.trace(K*K)-s.trace(K)**2)/2+2*m*s.trace(K)**2/3
    L+=m*k*k*(z*z+2*n*z+alpha*n*n+2*chi*chi+4*chi*(z+n))-n*rho+z*S-s.I*w*B*rho
    eq=[s.diff(L,z)+s.I*w*s.diff(L,zd)]+[s.diff(L,q) for q in (n,B,chi)]
    eq=[s.expand(e.subs(zd,-s.I*w*z)) for e in eq]
    sol=s.solve(eq,[z,n,B,chi])
    R=s.factor((-k*k*n+s.I*w*k*k*B+3*w*w*z).subs(sol))
    mu=s.symbols('mu',positive=True)
    Rmu=s.factor(R.subs(alpha,1-mu))
    high=s.simplify(s.limit(R,w,s.oo))
    # Expose angular dependence with alpha=1-D/q; no assumption of isotropy.
    q,D=s.symbols('q D',positive=True)
    aniso=s.factor(Rmu.subs({mu:D/q,k*k:q}))
    return dict(equation_residuals=[s.simplify(e.subs(sol)) for e in eq],
                metric_solution=sol,R00=R,R00_mu=Rmu,high_frequency_R00=high,
                anisotropic_R00=aniso,
                source_convention='rho_dot+k Jz=0, Jz_dot-k Szz=0; S is stress trace, not assumed zero',
                warning='A real subluminal mode is not a finite-domain-of-dependence proof.')


def causal_initial_data(sc):
    """Source-free compact initial data of the constant-coefficient principal
    system. An explicit Green-kernel derivative tests curvature support.
    This is not a construction of finite-amplitude globally curved solutions.
    """
    q,D,F=s.symbols('q D test_profile',positive=True)
    z0=(q+D)*F; n0=-q*F; c0=-D*F
    alpha=1-D/q
    constraints=[s.simplify(alpha*n0+z0+2*c0),s.simplify(n0+z0+c0)]
    keys={str(v):v for v in sc['auxiliaries']}
    za=s.Symbol('z',real=True);zd=s.Symbol('zd',real=True);k=s.Symbol('k',positive=True)
    zdd=-sc['speed_squared']*k*k*za
    R=-k*k*sc['auxiliaries'][keys['n']]-k*k*s.diff(sc['auxiliaries'][keys['B']],zd)*zdd-3*zdd
    Ridentity=s.simplify(R-k*k*za)
    Omega2=s.Rational(2,3)*D*q/(q+D)
    R0=q*z0
    R2=s.factor(-Omega2*R0)
    R4=s.factor(Omega2**2*R0/F)
    transverse,longitudinal,X,Z=s.symbols('mu_t mu_l k_perp_squared k_parallel_squared',positive=True)
    denom=(1+transverse)*X+(1+longitudinal)*Z
    numerator=s.Rational(4,9)*(transverse*X+longitudinal*Z)**2*(X+Z)**3
    quotient,remainder=s.div(numerator,denom,X)
    remainder=s.factor(remainder)
    radius,z=s.symbols('R z',positive=True)
    # Green function of E=-(1+mu_t)Delta_perp-(1+mu_l)partial_z^2.
    green=1/(4*s.pi*(1+transverse)*s.sqrt(1+longitudinal)*
             s.sqrt(radius**2/(1+transverse)+z*z/(1+longitudinal)))
    # Z^5 is (-partial_z^2)^5; evaluate on transverse axis outside source.
    tail=s.factor(-(remainder/Z**5)*s.diff(green,z,10).subs(z,0))
    mutation=s.simplify(tail.subs(longitudinal,transverse))
    y=s.symbols('y',positive=True)
    row={transverse:1-s.exp(-2),longitudinal:1+s.exp(-2),radius:1}
    return dict(initial_z=z0,initial_n=n0,initial_chi=c0,initial_velocities='zero',
                initial_constraint_residuals=constraints,vacuum_R00_identity_residual=Ridentity,
                R00_initial=R0,R00_second_time_derivative=R2,
                R00_fourth_time_derivative_symbol=R4,
                polynomial_division_residual=s.factor(numerator-denom*quotient-remainder),
                spatial_remainder=remainder,isotropic_remainder=s.simplify(remainder.subs(longitudinal,transverse)),
                elliptic_Green=green,exterior_fourth_derivative_kernel=tail,
                isotropic_tail=mutation,tail_at_y2_R1=tail.subs(row),
                exponential_anisotropy=s.simplify((1+(y-1)*s.exp(-y))-(1-s.exp(-y))),
                verdict='Principal causal FAIL: compact constrained vacuum data can develop exterior curvature at fourth time-derivative order.',
                limitation='Frozen weak-field principal system; nonlinear background and global mean/boundary lift remain open.')


def auxiliary_variation():
    x=s.symbols('x',real=True)
    N,c=[s.Function(name)(x) for name in ('N','chi')]
    T,nu=s.symbols('ADM_curvature_plus_kinetic nu',real=True)
    a=s.diff(N,x)/N
    L=N*(s.exp(2*c)*T/2+2*s.diff(c,x)**2+4*s.diff(c,x)*a+2*c*a*a+nu*c)
    equation=s.simplify((s.diff(L,c)-s.diff(s.diff(L,s.diff(c,x)),x))/N)
    expected=s.exp(2*c)*T+nu-4*(s.diff(c,x,2)+a*s.diff(c,x)+s.diff(a,x))-2*a*a
    return dict(one_dimensional_EL=equation,variation_identity=s.simplify(equation-expected),
                note='The full 3D equation replaces derivatives by D; add (4F/3)(K-Kbar_NF)^2 from variance variation.')


@lru_cache(maxsize=1)
def derive():
    sc,dc=scalar(); hm=homogeneous(); re=response()
    causal=causal_initial_data(sc);auxvar=auxiliary_variation()
    m,a0,p=s.symbols('m a0 Phi_gradient',positive=True)
    q,cg=s.symbols('Psi_gradient chi_gradient',real=True)
    f=2*a0*a0*(1-(1+p/a0)*s.exp(-p/a0))
    # chi R3 integrates to -4 grad(chi).grad(Psi); 4 Dchi.a is explicit.
    Lstat=m*(q*q-2*p*q+f+2*cg*cg+4*cg*(p-q))
    flux=[s.factor(s.diff(Lstat,x)/(2*m)) for x in (p,q,cg)]
    sol=s.solve([flux[1],flux[2]],[q,cg])
    physical=s.simplify(-flux[0].subs(sol))
    hp,hc,vp,vc,k,ch=s.symbols('hp hc vp vc k chi_bar',real=True)
    hh=s.Matrix([[hp,hc,0],[hc,-hp,0],[0,0,0]])
    hd=hh.subs({hp:vp,hc:vc})
    Ltt=m*s.exp(2*ch)*(s.trace(hd*hd)-k*k*s.trace(hh*hh))/8
    KT=s.hessian(Ltt,[vp,vc]); VT=-s.hessian(Ltt,[hp,hc]); w2=s.symbols('w2')
    roots=s.solve(s.det(w2*KT-VT),w2)
    mu=s.symbols('mu',positive=True)
    cs_mu=sc['speed_squared'].subs(s.Symbol('alpha',real=True),1-mu)
    checks={
        'static_compensator_has_no_extra_force_on_branch':sol[cg]==0,
        'static_Psi_derived_equal_Phi':sol[q]==p,
        'same_exponential_MOND_flux':s.simplify(physical-p*(1-s.exp(-p/a0)))==0,
        'scalar_kinetic_positive':sc['kinetic_m1']>0,
        'scalar_speed_identity':s.simplify(cs_mu-2*mu/(3*(1+mu)))==0,
        'scalar_speed_positive':s.simplify(cs_mu).is_positive,
        'scalar_speed_below_two_thirds':s.simplify(s.Rational(2,3)-cs_mu).is_positive,
        'local_primary_preservation':all(v['preservation_closed'] for v in dc.values()),
        'global_constraint_preservation':all(x==0 for x in hm['preservation_residuals']),
        'global_constraints_on_expanding_branch':all(x==0 for x in hm['constraint_residuals']),
        'tensor_positive_for_every_real_chi':all(v.is_positive for v in KT.eigenvals()),
        'tensor_luminal':all(s.simplify(v-k*k)==0 for v in roots),
        'source_equations_all_satisfied':all(x==0 for x in re['equation_residuals']),
        'auxiliary_equation_varied':auxvar['variation_identity']==0,
        'compact_initial_data_satisfy_constraints':all(x==0 for x in causal['initial_constraint_residuals']),
        'vacuum_physical_Ricci_derived':causal['vacuum_R00_identity_residual']==0,
        'tail_not_polynomial_division_error':causal['polynomial_division_residual']==0,
        'isotropic_control_has_no_displayed_tail':causal['isotropic_tail']==0,
        'anisotropic_exterior_tail_nonzero':float(causal['tail_at_y2_R1'])<0,
    }
    return dict(checks={name:bool(value) for name,value in checks.items()},scalar=sc,dirac=dc,homogeneous=hm,response=re,
                static=dict(L=Lstat,independent_fluxes=flux,spatial_solution=sol,physical_flux=physical,
                            G_measured=1/(8*s.pi*m)),
                tensor=dict(kinetic=KT,frequency_squared=roots),
                causal_initial_data=causal,auxiliary_variation=auxvar,
                status='OPEN full completion: constructive health/FLRW gates pass; frozen principal causal gate FAILS')


def serializable(value):
    if isinstance(value,dict):
        return {str(k):serializable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [serializable(v) for v in value]
    return value


def main():
    p=argparse.ArgumentParser();p.add_argument('--require-closure',action='store_true');args=p.parse_args()
    r=derive();print(json.dumps(serializable(r),default=str,indent=2))
    return 1 if not all(r['checks'].values()) else (2 if args.require_closure else 0)


if __name__=='__main__':
    raise SystemExit(main())
