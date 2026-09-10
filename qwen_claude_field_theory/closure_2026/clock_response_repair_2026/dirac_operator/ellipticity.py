#!/usr/bin/env python3
"""Exact all-domain principal-sign reduction, not global lapse invertibility."""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    U,d,ell,Y,r,Q2 = s.symbols('U d ell Y r Q2', positive=True)
    X = s.symbols('X', real=True)
    W = U+2*d*ell*(s.sqrt(1+Y/ell)-1)
    WY,WYY = s.diff(W,Y),s.diff(W,Y,2)
    transverse = W-2*Q2*WY
    longitudinal = transverse-(2*WY+4*Q2*WYY)*Y
    # Exact variable substitution; r is positive, so sqrt(r^2)=r.
    def transform(v):
        return s.simplify(v.subs(Q2,X+Y).subs(Y,ell*(r*r-1)))
    D=U-2*d*X;W0=U-2*d*ell
    pperp=W0*(1-1/r)+D/r
    ppara=W0*(1-1/r**3)+D/r**3
    assert s.simplify(transform(transverse)-pperp)==0
    assert s.simplify(transform(longitudinal)-ppara)==0
    A,q,m=s.symbols('A q m',positive=True)
    sub={U:m*q*A,d:A*(m*q*A)/(2*q*(q*A+m*q*A)),ell:q*q*m/2}
    margin=s.factor(W0.subs(sub,simultaneous=True))
    assert s.factor(margin-m*q*A*(2+m)/(2*(1+m)))==0
    # Independent boundary and failure controls: positivity needs the stated domain.
    assert s.simplify(pperp.subs(r,1)-D)==0
    assert s.simplify(ppara.subs(r,1)-D)==0
    outside={U:1,d:1,ell:s.Rational(1,4),X:1,r:1}
    assert pperp.subs(outside)<0 and ppara.subs(outside)<0
    inside={U:1,d:1,ell:s.Rational(1,4),X:s.Rational(1,4),r:2}
    assert pperp.subs(inside)>0 and ppara.subs(inside)>0
    return dict(principal_tensor='(W-2 Q^2 W_Y) h^ij - (2 W_Y+4 Q^2 W_YY) chi^i chi^j',
        transverse=str(pperp),longitudinal=str(ppara),stationary_margin=str(margin),
        assumptions=['timelike foliation','ell>0','Y>=0','U-2*d*X>0','U-2*d*ell>=0'],
        symbolic_eigenvalue_bridge=True,negative_domain_control=True,
        conclusion='Pointwise positive principal tensor throughout this regular action domain; not uniform positivity at its boundary',
        full_theory_status='OPEN')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result=main()
    if a.result_file:a.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
