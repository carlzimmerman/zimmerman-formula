"""Homogeneous scalar-dependent preferred-time coupling diagnostic."""
import argparse
import json
import math
import sympy as s
from scipy.optimize import brentq

q,N,adot,a,qdot,M2,Z=s.symbols('q N adot a qdot M2 Z',positive=True)
S=s.Function('S')(q)
U=s.Function('U')(q)
L=-s.Rational(3,2)*M2*S*a*adot**2/N+a**3*Z*qdot**2/(2*N)-N*a**3*U
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
check('lapse constraint',s.simplify(s.diff(L,N)/a**3-(s.Rational(3,2)*M2*S*(adot/(a*N))**2-Z*qdot**2/(2*N**2)-U))==0)
check('scalar curvature force sign',s.simplify(-s.diff(L,q)/(N*a**3)-(s.diff(U,q)+s.Rational(3,2)*M2*s.diff(S,q)*(adot/(a*N))**2))==0)
F=s.diff(U,q)+s.diff(S,q)*U/S
check('de Sitter stationary function',s.simplify(F-s.diff(S*U,q)/S)==0)
stationary={s.diff(U,q):-s.diff(S,q)*U/S}
mass=s.diff(F,q).subs(stationary)
check('constraint-reduced homogeneous mass',s.simplify(mass-s.diff(S*U,q,2).subs(stationary)/S)==0)
rows=[]
# Dimensionless illustrative units A=B=M²=Z=1; S=2+3 ell q.
for ell in (0.1,1.,10.):
    def pot(x): return x**-2+x*x
    def dp(x): return -2*x**-3+2*x
    def ds_force(x): return dp(x)+3*ell*pot(x)/(2+3*ell*x)
    qs=brentq(ds_force,3**(-0.25),1,xtol=1e-14)
    h2=2*pot(qs)/(3*(2+3*ell*qs))
    wpp=12/qs**4+4+6*ell/qs**3+18*ell*qs
    m2=wpp/(2+3*ell*qs)
    check('unique vacuum bracket '+str(ell),3**(-0.25)<qs<1 and abs(ds_force(qs))<1e-10)
    check('positive homogeneous mass '+str(ell),m2>0 and h2>0)
    check('old potential minimum not a vacuum '+str(ell),ds_force(1)>0)
    # Fixed radiation density, zero q velocity: instantaneous zero force,
    # not a time-dependent solution or a tracking proof.
    rho=1e8
    def early_force(x): return dp(x)+3*ell*(rho+pot(x))/(2+3*ell*x)
    qe=brentq(early_force,1e-8,1,xtol=1e-14)
    check('high density instantaneous force zero '+str(ell),abs(early_force(qe))/(3*ell*rho)<1e-8 and qe<qs)
    rows.append({'ell':ell,'q_de_Sitter':qs,'lambda_de_Sitter':1+ell*qs,'H_squared':h2,'homogeneous_mass_squared':m2,'rho_diagnostic':rho,'q_instantaneous_early':qe,'lambda_instantaneous_early':1+ell*qe})
result={'passed':all(c['passed'] for c in checks),'checks':checks,'samples':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
