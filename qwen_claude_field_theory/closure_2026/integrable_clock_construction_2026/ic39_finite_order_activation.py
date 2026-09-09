"""An explicit pin-potential variant, with a conditional finite second response."""
from functools import lru_cache
from pathlib import Path
import argparse
import json
import mpmath as mp
import sympy as s


@lru_cache(None)
def derive():
    x=s.Symbol('x',real=True);b=s.Rational(1,4)
    eta=x**4/(x**4+(b-x)**4)
    left=[s.limit(s.diff(eta,x,n),x,0,dir='+') for n in range(5)]
    right=[s.limit(s.diff(eta,x,n),x,b,dir='-') for n in range(5)]
    delta,a=s.symbols('delta a',positive=True);E4,S0=s.symbols('E4 S0',real=True)
    response=-E4*delta**4/(24*s.exp(S0)*eta.subs(x,a*delta))
    limit=s.limit(response,delta,0,dir='+')
    q,z,w,wc,S,ell=s.symbols('q z w wc S ell',real=True)
    m,h0=s.symbols('m h0',positive=True)
    activation=eta.subs(x,(s.exp(-3*w)*q/(3*m*h0))**2-s.Rational(1,2))
    pin=s.exp(S)*ell*(w-wc)*activation
    # Differentiate before imposing the pin. This is per unit J in the radial action.
    variation={k:s.diff(pin,v) for k,v in dict(S=S,w=w,q=q,ell=ell).items()}
    expected=s.exp(S)*ell*activation.subs(w,wc)
    checks=dict(w_equation=s.simplify(variation['w'].subs(w,wc)-expected),
                q_equation=s.simplify(variation['q'].subs(w,wc)),
                S_equation=s.simplify(variation['S'].subs(w,wc)),
                multiplier_equation=s.simplify(variation['ell']-s.exp(S)*(w-wc)*activation))
    t,A,D,E=s.symbols('t A D E',positive=True)
    h=-t*q*q/6-A*q*z-D*z*z-E*z**4-pin
    hqq=s.diff(h,q,2).subs(w,wc);hqz=s.diff(h,q,z).subs(w,wc);hzz=s.diff(h,z,2).subs(w,wc)
    uv=s.simplify(t/6+(hqq-hqz*hqz/hzz)/2)
    checks['pinned_schur_coefficient']=s.simplify(uv-A*A/(4*D+24*E*z*z))
    return dict(left_jets=left,right_jets=right,limit=limit,
                limit_identity=s.simplify(limit+E4*b**4/(24*s.exp(S0)*a**4)),
                quadratic_leak_limit=s.limit(-x*x/eta,x,0,dir='+'),
                quartic_example_limit=s.limit(-x**4/eta,x,0,dir='+'),
                monotonicity_identity=s.factor(s.diff(eta,x)-4*b*x**3*(b-x)**3/(x**4+(b-x)**4)**2),
                variation_checks=checks,pinned_schur_coefficient=uv)


def selected_limits(path):
    data=json.loads(Path(path).read_text());rows=[]
    # This is a reported CONDITIONAL limit, never an assertion that rounded roots are exact.
    with mp.workdps(80):
        # S0 is an exactly lifted input of the existing local construction, not a fitted value.
        import ic37_local_taylor as local
        S0=mp.mpf(float(local.reference().initial[0]));b=mp.mpf(1)/4
        for branch in data['joint']:
            if 'audits' not in branch:continue
            source=max(branch['audits'],key=lambda row:row['dps'])
            E4=mp.mpf(source['edge_jets'][4]);a=mp.mpf(source['activation_radial_derivative'])
            limit=-E4*b**4/(24*mp.exp(S0)*a**4)
            rows.append(dict(U0=branch['U0'],U1=branch['U1'],E4=str(E4),
                             conditional_ell_tt_limit=mp.nstr(limit,50),
                             unresolved_lower_jets=source['edge_jets'][:4],
                             exact_zero_jet_certificate=False))
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True)
    parser.add_argument('--strict',action='store_true');args=parser.parse_args()
    out=derive();checks={k:v==0 for k,v in out['variation_checks'].items()}
    checks.update(limit_identity=out['limit_identity']==0,monotonicity_identity=out['monotonicity_identity']==0)
    symbolic={k:([str(v) for v in value] if isinstance(value,list) else str(value))
              for k,value in out.items() if k!='variation_checks'}
    print(json.dumps(dict(checks=checks,symbolic=symbolic,selected=selected_limits(args.input),
                         full_theory='OPEN',variant='quartic pin activation, not a change of MOND mu'),indent=2))
    raise SystemExit(1 if not all(checks.values()) else 2 if args.strict else 0)
