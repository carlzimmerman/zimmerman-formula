"""Algebraic obstruction and additive-vacuum cancellation diagnostic."""
import argparse
import json
import math
import sympy as s

d,r=s.symbols('d r',positive=True)
lam=(1+2*d/((1+d)*r))/3
c=4*d*(1+d)**2/(3*(3*lam-1))
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
check('eliminate lambda',s.simplify(c-s.Rational(2,3)*r*(1+d)**3)==0)
lower=s.Rational(2,3)*r/(1-r)**3
check('endpoint expression',s.simplify(c.subs(d,r/(1-r))-lower)==0)
check('coefficient lower bound increases for 0<r<1',s.simplify(s.diff(lower,r)-s.Rational(2,3)*(1+2*r)/(1-r)**4)==0)
check('lambda branch inequality',s.simplify((lam-1)-2*(d*(1-r)-r)/(3*r*(1+d)))==0)
rows=[]
for ratio in (0.92,0.95,0.99):
    cbound=(2/3)*ratio/(1-ratio)**3
    cancellation=1-32*math.pi/cbound
    for multiplier in (1.01,2,10):
        D=multiplier*ratio/(1-ratio)
        L=(1+2*D/((1+D)*ratio))/3
        C=4*D*(1+D)**2/(3*(3*L-1))
        check('admissible sample '+str((ratio,multiplier)),L>1 and C>cbound)
    rows.append({'R':ratio,'C_infimum':cbound,'C_infimum_over_32pi':cbound/(32*math.pi),'required_negative_vacuum_fraction_lower_bound':cancellation})
result={'passed':all(x['passed'] for x in checks),'checks':checks,'bounds':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
