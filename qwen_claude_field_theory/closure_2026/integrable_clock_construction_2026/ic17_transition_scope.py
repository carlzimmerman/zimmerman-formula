#!/usr/bin/env python3
"""Exact L35 identity and a counterexample only to its variable-coefficient extension.

This constructs no auxiliary-constraint solution and certifies no physical cone.
"""
import argparse
from functools import lru_cache
import json
import sympy as s


@lru_cache(None)
def fixed_q_checks():
    r, rho, E, G, B = s.symbols('r rho E G B', nonzero=True, real=True)
    eta = s.Function('eta')
    rr = -E*rho/3
    h = -E*rho**2/3 + eta(rr)*(-E*G*rho**2/3-B)
    A = 1+G*eta(rr)
    actual = (E*A/6+s.diff(h,rho,2)/4).subs(rho,-3*r/E).doit()
    b = E*G*r**2/12+B*E**2/36
    target = -E*G*r*s.diff(eta(r),r)/3-b*s.diff(eta(r),r,2)
    return dict(hessian=s.simplify(actual-target),
                total_derivative=s.simplify(target+s.diff(b*b*s.diff(eta(r),r),r)/b))


@lru_cache(None)
def counterexample():
    r = s.symbols('r',real=True)
    t = r-1
    eta = 10*t**3-15*t**4+6*t**5
    ep,epp = s.diff(eta,r),s.diff(eta,r,2)
    E = s.exp(r+2)
    G = -3/(E*r)
    B = (9*r-s.Rational(36,100)*epp)/E**2
    alpha = s.simplify(E*G*r/3)
    b = s.simplify(E*G*r**2/12+B*E**2/36)
    aUV = s.factor(-alpha*ep-b*epp)
    critical = [1,2]+s.solve(s.diff(epp,r),r)
    bound = s.simplify(max(abs(epp.subs(r,x)) for x in critical))
    return dict(r=r,eta=eta,eta_prime=s.factor(ep),eta_second=s.factor(epp),
                E=E,G=G,B=B,alpha=alpha,b=s.factor(b),aUV=aUV,
                second_derivative_bound=bound,
                B_numerator_lower_bound=9-s.Rational(36,100)*bound,
                integrating_factor_residue=s.limit((r-s.Rational(3,2))*alpha/b,r,s.Rational(3,2)))


def chart_checks():
    """Bounded 101-point checks, not a constraint solve or interval certificate."""
    c=counterexample()
    r=c['r']
    E,G=c['E'],c['G']
    w=s.log(1+G)/2-s.Rational(1,12)
    xi=s.log(E)+3*w
    u=1+w/xi
    S=xi-w
    out=dict(E_positive=True,G_in_chart=True,B_positive=True,
             xi_positive=True,u_in_chart=True,S_monotone=True)
    for i in range(101):
        values=[s.N(e.subs(r,1+s.Rational(i,100)),40)
                for e in (E,G,c['B'],xi,u,s.diff(S,r))]
        tests=(values[0]>0,-1<values[1]<0,values[2]>0,
               values[3]>0,0<values[4]<1,values[5]>0)
        out={k:old and bool(test) for (k,old),test in zip(out.items(),tests)}
    return out


def exit_status(checks, require_full_closure=False):
    if not checks or not all(checks.values()):
        return 1
    return 2 if require_full_closure else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    c=counterexample()
    r=c['r']
    checks={k:v==0 for k,v in fixed_q_checks().items()}
    checks.update(chart_checks())
    checks.update(positive_decomposition=s.simplify(c['aUV']-c['eta_prime']-c['eta_second']**2/100)==0,
                  rising_factor=s.factor(c['eta_prime'])==30*(r-1)**2*(r-2)**2,
                  isolated_zeros=s.solve(c['b'],r)==[1,s.Rational(3,2),2],
                  positive_B_bound=bool(c['B_numerator_lower_bound']>0),
                  singular_weight=c['integrating_factor_residue']==-s.Rational(10,3))
    print(json.dumps(dict(full_theory='OPEN',checks=checks,
                         counterexample={k:str(v) for k,v in c.items()},
                         scope='C2 variable-coefficient ODE counterexample; not an IC solution'),indent=2))
    return exit_status(checks,args.require_full_closure)


if __name__=='__main__':
    raise SystemExit(main())
