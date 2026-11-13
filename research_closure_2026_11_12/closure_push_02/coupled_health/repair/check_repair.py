#!/usr/bin/env python3
"""Convex/concave repair identities and its conditional physical pressure cost."""
import argparse
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as s


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start=time.time(); here=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=here/'run_001')
    args=parser.parse_args()
    source=here.parents[1]/'static_gate'/'matching'/'run01'/'results.json'
    data=json.loads(source.read_text())
    q,C,L,u,Pc,N,qt,lam=s.symbols('q C L u Pc N qt lam',positive=True)
    x=q-1;t=x*x/(L*L*q);F=C*x*x;B=C*L*L*q*(1-s.exp(-t));S=s.exp(-u**3)
    Bqq=C*s.exp(-t)*(2-(q*q-1)**2/(L*L*q**3))
    Hgate=F-B+B*S
    gamma_uu=9*C*L*L*u**4*S
    D=(B*s.diff(S,u,2)-q*gamma_uu)/Pc**2
    Dclosed=S/Pc**2*(9*u**4*(B-q*C*L*L)-6*u*B)
    target_energy=C*(q*q-1)*(1-(1-S)*s.exp(-t))
    checks={
        'perspective_second_derivative':s.simplify(s.diff(B,q,2)-Bqq)==0,
        'energy_of_gated_piece':s.simplify(q*s.diff(B,q)-B-C*(q*q-1)*s.exp(-t))==0,
        'exact_clock_energy_fraction':s.simplify(q*s.diff(Hgate,q)-Hgate-target_energy)==0,
        'concavity_identity':s.simplify(D-Dclosed)==0,
        'FRW_value':s.simplify(Hgate.subs(u,0)-F)==0,
        'FRW_first_Pi':s.simplify(s.diff(Hgate,u).subs(u,0))==0,
        'FRW_mixed_QPi':s.simplify(s.diff(Hgate,u,q).subs(u,0))==0,
        'FRW_second_Pi':s.simplify(s.diff(Hgate,u,2).subs(u,0))==0,
        'QPi_lapse_independence':s.diff(N*(-lam*qt/N)*u,N)==0,
    }
    # A Q-linear Gamma has zero energy, but nonzero pressure.
    G,Gp=s.symbols('Gamma Gamma_prime',real=True)
    checks['QGamma_zero_energy']=s.simplify(q*(-G)-(-q*G))==0
    checks['QGamma_pressure']=s.simplify((-q*G)-u*(-q*Gp)-q*(u*Gp-G))==0
    pressure=3*C*L*L*(1-(u**3+1)*S)
    checks['explicit_pressure_moment']=s.simplify(s.diff(pressure,u)-u*gamma_uu)==0
    u0=(s.Rational(2,3))**s.Rational(1,3)
    lower=3*s.exp(-s.Rational(2,3))-(3*u**3+1)*S
    checks['minimum_pressure_moment_derivative']=s.simplify(s.diff(lower,u)-u*s.diff(S,u,2))==0
    checks['minimum_pressure_moment_lower_endpoint']=s.simplify(lower.subs(u,u0))==0
    # Direct diagonal spatial-metric variation at fixed vector density J.
    s1,s2,s3,v,pp,h0,hp,w0,wv,ga=s.symbols('s1 s2 s3 v pp h0 hp w0 wv ga',real=True)
    volume=s.exp(s1+s2+s3);localPi=pp/volume;localP=v*s.exp(-s2-s3)
    matter=volume*(h0+hp*(localPi-pp)-localPi-ga*localPi**2/2-w0-wv*(localP-v))
    zero={s1:0,s2:0,s3:0}
    pr=h0-pp*hp+ga*pp**2/2-w0
    checks['radial_stress_fixed_J']=s.simplify(s.diff(matter,s1).subs(zero)-pr)==0
    checks['tangential_stress_fixed_J']=s.simplify(s.diff(matter,s2).subs(zero)-(pr+v*wv))==0
    Z=s.symbols('Z',positive=True)
    Wmargin=Z*Z/(1-Z)+2*Z+2*s.log(1-Z)
    checks['W_pressure_margin_derivative']=s.simplify(s.diff(Wmargin,Z)-Z*Z/(1-Z)**2)==0
    # Wrong boundary choice and omitted pressure are explicit counterchecks.
    controls={
        'Pi_only_is_not_lapse_boundary':s.diff(N*(-lam*u),N)!=0,
        'zero_pressure_mutation_rejected':s.simplify(q*(u*Gp-G))!=0,
    }
    assert all(checks.values()) and all(controls.values())
    # Finite diagnostic of the analytically proved inequalities, including Q<1.
    Cn,Ln=2.,.05
    minimumQQ=math.inf; maximumPP=-math.inf
    for Q in np.r_[np.geomspace(.001,1000,301),1.]:
        T=(Q-1)**2/(Ln*Ln*Q);E=math.exp(-T)
        bv=Cn*Ln*Ln*Q*(-math.expm1(-T))
        bqq=Cn*E*(2-(Q*Q-1)**2/(Ln*Ln*Q**3))
        for U in np.linspace(0,4,101):
            sv=math.exp(-U**3)
            # Stable positive form: the subtractive form rounds to zero at Q=1,u=4.
            hqq=2*Cn*sv+(1-sv)*(2*Cn-bqq)
            hpp=sv*(-9*U**4*Q*Cn*Ln*Ln*E-6*U*bv)
            minimumQQ=min(minimumQQ,hqq); maximumPP=max(maximumPP,hpp)
    assert minimumQQ>0 and maximumPP<=1e-15
    mp.mp.dps=70
    floor=3*mp.exp(-mp.mpf(2)/3)
    I=3*mp.gamma(mp.mpf(5)/3)
    rows=[]
    for mu in sorted({r['mu_Mpc_inverse'] for r in data['rows']}):
        inputs=[r for r in data['rows'] if r['mu_Mpc_inverse']==mu]
        bounds=[]
        for r in inputs:
            X=mp.mpf(str(abs(r['phi_geo'])));Q=1+X
            U=mp.mpf(str(r['Pi_over_Pic']));delta=mp.mpf(str(r['dust_fraction_ceiling_delta']))
            su=mp.exp(-U**3)
            bound=X*X/(Q*(mp.log1p(-su)-mp.log1p(-delta)))
            bounds.append(bound)
        L2=max(bounds);KB=mp.mpf(str(mu))**2*L2/2
        for r in inputs:
            X=mp.mpf(str(abs(r['phi_geo'])));Q=1+X
            U=mp.mpf(str(r['Pi_over_Pic']));delta=mp.mpf(str(r['dust_fraction_ceiling_delta']))
            su=mp.exp(-U**3);T=X*X/(L2*Q)
            fraction=-mp.expm1(-T)+su*mp.exp(-T)
            assert fraction<=delta*(1+mp.mpf('1e-60'))
            finitefloor=floor-(3*U**3+1)*su
            Kpmin=Q*KB*finitefloor
            Kpexplicit=Q*KB*3*(1-(U**3+1)*su)
            rows.append(dict(mu_Mpc_inverse=mu,r_Mpc=r['r_Mpc'],Q=float(Q),u=float(U),
                target_delta=float(delta),energy_fraction=float(fraction),
                required_L_squared=float(L2),K_Bstar_Mpc_inverse2=float(KB),
                minimum_K_clock_pressure_Mpc_inverse2=float(Kpmin),
                explicit_K_clock_pressure_Mpc_inverse2=float(Kpexplicit),
                minimum_pressure_over_Pi=float(Kpmin/mp.mpf(str(r['KPi_Mpc_inverse2']))),
                minimum_pressure_curvature_length_Mpc=float(1/mp.sqrt(Kpmin)),
                three_Kp_r_squared=float(3*Kpmin*mp.mpf(str(r['r_Mpc']))**2),
                omitted_pressure_moment_tail=float((3*U**3+1)*su)))
    result=dict(status='PASS; exact repair identities and conditional target-cost calculation',
        checks=checks,mutation_controls=controls,
        diagnostics=dict(sampled_HQQ_min=minimumQQ,sampled_HPIPI_max=maximumPP,
                         grid='302 Q values including Q=1; 101 u values; cross-check only'),
        constants=dict(lambda_integral=float(I),minimum_pressure_factor=float(floor),explicit_pressure_factor=3),
        physical_assumptions=dict(input_path=str(source),
            clock_mapping='Q=1+abs(phi_geo), the supplied weak-potential reference mapping',
            target='same supplied annulus and clock-energy fraction ceiling; not a new fit or repaired-background solution',
            candidate='perspective B with QGamma; separate from original bounded-B derivative bound'),rows=rows)
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    dest=out/'result.json';dest.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    manifest=dict(state='COMPLETED',exit_code=0,elapsed_seconds=time.time()-start,
        command=sys.argv,
        environment=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__,numpy=np.__version__),
        inputs={str(p):sha(p) for p in [Path(__file__).resolve(),here/'DERIVATION.md',source]},
        outputs={'result.json':sha(dest)},scope=result['status'])
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
