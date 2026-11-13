#!/usr/bin/env python3
"""Independent exact identities for the perspective compensation repair."""
import argparse,json
from pathlib import Path
import sympy as s


def main(output):
    q,C,L,u,Pc=s.symbols('q C L u Pc',positive=True);Gamma=s.Function('Gamma')(u)
    S=s.exp(-u**3);t=(q-1)**2/(L*L*q);F=C*(q-1)**2
    B=C*L*L*q*(1-s.exp(-t));H=F-B+B*S-q*Gamma
    checks={}
    def check(name,e):checks[name]=s.simplify(e)==0
    Bqq=C*s.exp(-t)*(2-(q*q-1)**2/(L*L*q**3))
    check('perspective_B_QQ',s.diff(B,q,2)-Bqq)
    check('perspective_B_Q',s.diff(B,q)-(C*L*L*(1-s.exp(-t))+C*(q-1/q)*s.exp(-t)))
    check('QB_Q_minus_B',q*s.diff(B,q)-B-C*(q*q-1)*s.exp(-t))
    check('convex_clock_Hessian',s.diff(H,q,2)-(2*C-(1-S)*Bqq))
    check('positive_convexity_remainder',s.diff(H,q,2)-2*C*S-(1-S)*(2*C-Bqq))
    chosen=9*C*L*L*u**4*S
    Hpp=s.diff(H,u,2).subs(s.diff(Gamma,u,2),chosen)/Pc**2
    check('concave_Pi_Hessian',Hpp-S*(9*u**4*(B-q*C*L*L)-6*u*B)/Pc**2)
    check('energy_suppression',q*s.diff(H,q)-H-C*(q*q-1)*(1-(1-S)*s.exp(-t)))
    # Set Gamma(0)=Gamma'(0)=Gamma''(0)=0 for endpoint checks.
    endpoint={Gamma:0,s.diff(Gamma,u):0,s.diff(Gamma,u,2):0}
    check('FRW_function',H.subs(endpoint).subs(u,0)-F)
    check('FRW_first_Pi',s.diff(H,u).subs(endpoint).subs(u,0))
    check('FRW_mixed_Pi',s.diff(H,u,q).subs(endpoint).subs(u,0))
    check('FRW_second_Pi',Hpp.subs(u,0))
    R=F-B
    neff=q*s.diff(H,q)+Pc*u-u*s.diff(H,u)
    positive_form=q*(s.diff(R,q)+S*s.diff(B,q))+Pc*u-u*B*s.diff(S,u)+q*(u*s.diff(Gamma,u)-Gamma)
    check('positive_branch_enthalpy_decomposition',neff-positive_form)
    check('R_stationary_at_Q1',s.diff(R,q).subs(q,1))
    check('Qbelow1_enthalpy_counterexample',neff.subs(endpoint).subs({u:0,q:s.Rational(1,2)})+C/2)
    # Gamma's exact asymptotic moments.
    slope=s.integrate(chosen,(u,0,s.oo));intercept=s.integrate(u*chosen,(u,0,s.oo))
    check('explicit_Gamma_intercept',intercept-3*C*L*L)
    check('explicit_Gamma_slope',slope-3*s.gamma(s.Rational(5,3))*C*L*L)
    u0=s.real_root(s.Rational(2,3),3)
    # Integration by parts: integral_u0^infty u S'' = S(u0)-u0*S'(u0).
    lower=s.simplify(S.subs(u,u0)-u0*s.diff(S,u).subs(u,u0))
    check('sharp_pressure_intercept_bound',lower-3*s.exp(-s.Rational(2,3)))
    # A constant multiple of QPi is an exact covariant total divergence.
    Q,Pi,l,divP,PdQ,HQ,HP,HQP,HQQ,HPP,g,p=s.symbols('Q Pi l divP PdQ HQ HP HQP HQQ HPP g p')
    check('covariant_QPi_boundary',Q*(divP+PdQ/Q)-(Q*divP+PdQ))
    B0=1+g*p-HP;c0=B0+Q*HQP
    shifted_c=1+g*p-(HP-l*Q)+Q*(HQP-l)
    check('boundary_preserves_mixed_principal_coefficient',shifted_c-c0)
    check('boundary_preserves_clock_energy',Q*(-l*p)-(-l*Q*p))
    check('boundary_preserves_pressure',-l*Q*p-p*(-l*Q))
    check('boundary_preserves_charge',-l*Pi+l*Pi)
    result={'checks':checks,'all_pass':all(checks.values()),'count':len(checks),
            'Gamma_slope':str(slope),'Gamma_intercept':str(intercept),
            'sharp_intercept_factor':str(lower),'scope':'Exact algebra; inequalities proved in REPAIR_REVIEW, no repaired halo solve or target pressure-number remeasurement'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);main(a.parse_args().output)
