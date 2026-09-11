#!/usr/bin/env python3
"""Same-action constraint propagation with on-shell minimally coupled dust.

This is a continuum residual identity, not a gravitational mode count.
The existing action Noether identities are rederived first. Matter identities
are independently checked using its continuity and geodesic equations.
"""
import argparse
import json
import re
from pathlib import Path
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
from equations import derive


def calculate():
    action=derive()
    assert action['checks']['radial_noether_identity']
    assert action['checks']['time_noether_identity_shift_zero']
    t,r=s.symbols('t r',real=True)
    N,A,R,rho,w=[s.Function(z)(t,r) for z in ('N','A','R','rho','w')]
    V=A*R**2;U=s.sqrt(1+w*w/A**2)
    k,h=s.symbols('k h',real=True)
    at=N*A*k;rt=N*R*h;wt=s.diff(N*U,r)
    Ut=s.diff(U,t).subs({s.diff(A,t):at,s.diff(w,t):wt})
    rhot=(s.diff(N*V*rho*w/A**2,r)-V*rho*Ut
          -N*(k+2*h)*V*rho*U)/(V*U)
    on_dust={s.diff(A,t):at,s.diff(R,t):rt,s.diff(w,t):wt,s.diff(rho,t):rhot}
    EN=-V*rho*U**2;EA=N*R**2*rho*w**2/A**2;Ev=-V*rho*U*w
    checks={}
    def check(name,e):
        checks[name]=s.simplify(s.cancel(e))==0
        if not checks[name]:raise AssertionError(name+': '+str(s.simplify(e)))
    check('dust_radial_Ward',
          (s.diff(N,r)*EN+s.diff(A,r)*EA-s.diff(A*EA,r)-s.diff(Ev,t)).subs(on_dust))
    check('dust_temporal_Ward',
          (-N*s.diff(EN,t)+at*EA+s.diff(N*N*Ev/A**2,r)).subs(on_dust))

    C,M,T=[s.Function(z)(t,r) for z in ('C_H','C_M','C_tau')]
    eta=s.symbols('eta',real=True)
    # On the constraint-added spatial equations and E_chi=0, total EL residual
    # densities. The chi EL terms in both Noether identities are zero only
    # under this scalar-evolution hypothesis, not by dust conservation alone.
    EN=V*C;Ev=V*M;EA=-eta*N*R**2*C;ER=-2*eta*N*A*R*C
    radial=s.diff(N,r)*EN+s.diff(A,r)*EA+s.diff(R,r)*ER-s.diff(A*EA,r)-s.diff(Ev,t)
    temporal=-N*s.diff(EN,t)+at*EA+rt*ER-N*V*T+s.diff(N*N*Ev/A**2,r)
    residuals=[e.subs({s.diff(A,t):at,s.diff(R,t):rt}) for e in (temporal,radial)]
    rates=s.solve(residuals,[s.diff(C,t),s.diff(M,t)])
    theta=N*(k+2*h)
    expected_C=-(1+eta)*theta*C+N/A**2*s.diff(M,r)+(2*s.diff(N,r)+N*(2*s.diff(R,r)/R-s.diff(A,r)/A))/A**2*M-T
    expected_M=eta*N*s.diff(C,r)+(1+eta)*s.diff(N,r)*C-theta*M
    check('Hamiltonian_rate',rates[s.diff(C,t)]-expected_C)
    check('momentum_rate',rates[s.diff(M,t)]-expected_M)
    energy=eta*C**2+M**2/A**2
    flux=2*eta*V*N*C*M/A**2
    balance=(s.diff(V*energy,t)-s.diff(flux,r)).subs(rates).subs({s.diff(A,t):at,s.diff(R,t):rt})/V
    expected=-eta*(1+2*eta)*theta*C**2-(theta+2*N*k)*M**2/A**2+2*(1+2*eta)*s.diff(N,r)*C*M/A**2-2*eta*T*C
    check('weighted_energy_balance',balance-expected)
    principal=s.Matrix([[0,N/A**2],[eta*N,0]])
    lam=s.symbols('lambda')
    determinant=s.factor((lam*s.eye(2)-principal).det())
    check('principal_polynomial',determinant-(lam**2-eta*N**2/A**2))
    flrw=s.factor(expected.subs({eta:1,k:h,s.diff(N,r):0,T:0}))
    check('expanding_FLRW_damping',flrw+N*h*(9*C**2+5*M**2/A**2))
    nn,aa,kk,hh,gg,cc,zz,tt=s.symbols('N A k h g C Z T')
    plain=expected.subs({eta:1,s.diff(N,r):A*gg,M:A*zz,C:cc,T:tt})
    plain=plain.subs({N:nn,A:aa,k:kk,h:hh})
    lean=(HERE/'ConstraintEnergy.lean').read_text()
    body=re.search(r'def balance .*? :=\s*(.*?)\n\n',lean,re.S).group(1)
    lean_expr=s.sympify(body.replace('^','**'),locals={str(x):x for x in (nn,kk,hh,gg,cc,zz,tt)})
    check('actual_Lean_balance_definition',plain-lean_expr)
    check('actual_Lean_energy_definition',
          s.sympify(re.search(r'def energy .*? :=\s*(.*?)\n',lean).group(1).replace('^','**'),
                    locals={'C':cc,'Z':zz})-(cc**2+zz**2))
    return dict(checks=checks,action_checks=action['checks'],
                inherited_action_checks=action['inherited_check_count'],
                Hamiltonian_rate=str(s.factor(rates[s.diff(C,t)])),
                momentum_rate=str(s.factor(rates[s.diff(M,t)])),
                energy_density=str(energy),flux_density=str(flux),
                balance_per_volume=str(expected),principal_matrix=str(principal),
                characteristic_polynomial=str(determinant),FLRW_balance=str(flrw),
                normalized_eta_one_balance=str(s.factor(plain)),
                assumptions=['on-shell dust continuity and geodesic equations',
                             'on-shell chi Euler-Lagrange equation',
                             'constraint-added spatial metric equations',
                             'regular spherical patch N,A,R nonzero',
                             'constant eta; C_tau is retained as a source'],
                scope='Constraint residual evolution, not physical tensor/scalar perturbations',
                full_theory_status='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();result=calculate()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
