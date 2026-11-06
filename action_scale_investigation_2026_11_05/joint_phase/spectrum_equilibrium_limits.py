"""Supplement: chemical balance and long-lived opacity in the same model."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args()
checks={}
def eq(name,a,b):checks[name]=bool(s.simplify(a-b)==0)
m,T,z,q=s.symbols('m T z q',positive=True)
na=z/(2*s.pi**2)*s.integrate(q**2*s.exp(-q/T),(q,0,s.oo))
nchi=z*s.exp(-m/T)/(2*s.pi**2)*s.integrate(q**2*s.exp(-q*q/(2*m*T)),(q,0,s.oo))
eq('massless dilute density',na,z*T**3/s.pi**2)
eq('massive dilute density',nchi,z*(m*T/(2*s.pi))**s.Rational(3,2)*s.exp(-m/T))
eq('common fugacity chemical density ratio',nchi/na,s.sqrt(s.pi/8)*(m/T)**s.Rational(3,2)*s.exp(-m/T))
x=s.symbols('x',positive=True)
eq('cold equilibrium material energy disappears',s.limit(s.sqrt(s.pi/8)*x**s.Rational(5,2)*s.exp(-x)/3,x,s.oo),0)
n,K,R,v=s.symbols('n K R v',positive=True)
sig=4*K;tau=n*sig*R
eq('annihilation to dynamical time',1/(n*K)/(R/v),4*v/tau)
# independent Maxwell velocities: each component variance T/m;
# pair center of mass V=(v1+v2)/2.
eq('annihilation Doppler line variance',m*m*(T/m+T/m)/4,m*T/2)
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'scope':'Dilute common-chemical-potential limit, uniform cold opacity and leading source width.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
