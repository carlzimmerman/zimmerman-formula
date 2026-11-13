#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import sympy as s

p,K,a0,D,p2,p3,r=s.symbols('p K a0 D p2 p3 r',nonzero=True)
v=p*r/3
candidate=p+p2*r*r+p3*r**3
residual=s.series(s.diff(candidate,r)+K*v/(1-K*v/a0)/D,r,0,3).removeO()
sol=s.solve([residual.coeff(r,1),residual.coeff(r,2)],(p2,p3),dict=True)[0]
checks={'quadratic_coefficient':s.simplify(sol[p2]+K*p/(6*D))==0,
        'cubic_coefficient':s.simplify(sol[p3]+K*K*p*p/(27*a0*D))==0,
        'old_cubic_omission_is_not_O_r4':s.simplify(residual.subs({p2:-K*p/(6*D),p3:0}).coeff(r,2))!=0}
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
result={'checks':checks,'all_pass':all(checks.values()),'Pi_r2':str(sol[p2]),'Pi_r3':str(sol[p3]),
        'scope':'First radial series terms; omitted v O(r³), D−D0 O(r²),psi−1 O(r⁴) do not affect these two coefficients'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']
