#!/usr/bin/env python3
"""Finite independent Euler checks; universal proof is in the linked lemma."""
import argparse, json, sympy as s
parser=argparse.ArgumentParser()
parser.add_argument("--output",required=True)
parser.add_argument("--false-linear-exact",action="store_true")
args=parser.parse_args()
r=s.symbols('r', positive=True)
M,c,H,C=s.symbols('M c H C', positive=True)
N,B,V=[s.Function(t)(r) for t in ('N','B','V')]
d=lambda x:s.diff(x,r)
def el(L,x): return s.diff(L,x)-d(s.diff(L,d(x)))
checks=[]
for n in range(2,8):
    ve=n*(n-1)*M*H**2/2
    b=2*c/(n*H)
    D=d(V)+d(B)*V/B
    L=M*s.Rational(n-1,2)*((n-2)*N*r**(n-3)*(B+1/B)+2*d(N)*r**(n-2)/B-B/N*(2*r**(n-2)*V*D+(n-2)*r**(n-3)*V**2))+N*B*r**(n-1)*(2*c*s.log(N)-ve)-b*B*r**(n-1)*V*d(N)/N
    sub={N:1,B:1,d(N):0,d(B):0,d(N,):0,s.diff(N,r,2):0,s.diff(B,r,2):0}
    eb=s.simplify(el(L,B).subs(sub).doit())
    en=s.simplify(el(L,N).subs(sub).doit())
    want=M*s.Rational(n-1,2)*r**(n-3)*(2*r*V*d(V)+(n-2)*V**2)-ve*r**(n-1)
    assert s.simplify(eb-want)==0
    assert s.simplify(en-eb-r**(n-1)*(2*c+b*(d(V)+(n-1)*V/r)))==0
    residual=s.simplify(d(r**(n-2)*(-H*r+C/r**(n-1))**2)-n*H**2*r**(n-1))
    assert s.simplify(residual+n*C**2/r**(n+1))==0
    assert residual!=0  # Control: nonzero-C linear mode is not an exact solution.
    if args.false_linear_exact:
        assert residual==0, "Rejected false finite-mass exact geodesic mode"
    checks.append({'n':n,'EL_B':True,'EL_N_difference':True,'quadratic_obstruction':True,'false_exact_linear_claim_rejected':True})
result=json.dumps({'scope':'n=2..7 symbolic checks; general-n proof in GEODESIC_EXTERIOR_LEMMA.md','sympy':s.__version__,'checks':checks},indent=2)
from pathlib import Path
Path(args.output).write_text(result+'\n')
print(result)
