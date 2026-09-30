"""Conditional matched-background coefficient; no parameter-selection law."""
import argparse
import json
import math
import sympy as s
from scipy.optimize import brentq

G,K,A,B,q,D,x=s.symbols('G K A B q D x',positive=True)
ell=4*(A-B*q**4)/(3*q*(3*B*q**4-A))
S=2+3*ell*q
U=A/q**2+B*q**2
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
check('vacuum coupling solution',s.simplify(s.diff(U,q)+3*ell*U/S)==0)
check('vacuum S identity',s.simplify(S-2*(A+B*q**4)/(3*B*q**4-A))==0)
Lambda=16*s.pi*G*U/S
a0=1/(12*s.pi*G*K*q)
Dcube=(12*s.pi*G)**3*2*A*K*K
Cbare=Lambda/a0**2
check('bare matched coefficient',s.simplify(Cbare-Dcube*(3*B*q**4/A-1)/3)==0)
mu=D/(1+D)
check('conditional relaxed Newton coefficient',s.simplify((D**3*(3*x**4-1)/3)/mu**2-D*(1+D)**2*(3*x**4-1)/3)==0)
qs=brentq(lambda q:-2/q**3+2*q+30*(q**-2+q*q)/(2+30*q),3**(-0.25),1)
cb=12**3*(3*qs**4-1)/3
cn=12*13**2*(3*qs**4-1)/3
result={'passed':all(c['passed'] for c in checks),'checks':checks,'illustrative_qstar':qs,'illustrative_D':12,'illustrative_ell':10,'coefficient_if_G_N_equals_bare_G':cb,'coefficient_if_local_relaxation_Newton_calibration_holds':cn,'target_32pi_for_comparison_only':32*math.pi}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
