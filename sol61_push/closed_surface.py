import argparse
import json
import math
import numpy as np
import sympy as s
from scipy.special import polygamma

checks=[]
def check(name,condition): checks.append({'name':name,'passed':bool(condition)})
n,x=s.symbols('n x',positive=True)
raw=n*n+x*x/2-n*s.sqrt(n*n+x*x)
stable=x**4/(2*(s.sqrt(n*n+x*x)+n)**2)
check('stable summand identity',s.simplify(raw-stable)==0)
series=s.series(raw,x,0,8).removeO()
check('quartic coefficient',s.expand(series).coeff(x,4)==1/(8*n*n))
check('sixth coefficient',s.expand(series).coeff(x,6)==-1/(16*n**4))
u=s.symbols('u',nonnegative=True)
continuum=s.integrate(s.exp(-2*u)*s.cosh(u)/2,(u,0,s.oo))
check('continuum integral one third',continuum==s.Rational(1,3))
N=30000
ns=np.arange(1,N+1,dtype=float)
rows=[]
for value in (0.01,0.1,1.,10.,100.,300.):
    finite=float(np.sum(value**4/(2*(np.sqrt(ns*ns+value*value)+ns)**2)))
    upper=finite+value**4*float(polygamma(1,N+1))/8
    error=value**6/(48*N**3)
    lower=upper-error
    check('positive response x='+str(value),lower>0)
    if value<=0.1:
        lead=math.pi**2*value**4/48
        remainder=math.pi**4*value**6/1440
        check('small-x quartic bounds x='+str(value),lower<=lead and upper>=lead-remainder)
    if value>=100:
        check('planar cubic approached x='+str(value),abs(upper/(value**3/3)-1)<0.008)
    rows.append({'x':value,'F_upper_estimate':upper,'tail_error_bound':error,'F_over_x4':upper/value**4,'F_over_planar':upper/(value**3/3)})
short=np.arange(1,101,dtype=float)
direct=float(np.sum(short**2+0.5-short*np.sqrt(short**2+1)))
independent=float(np.sum(1/(2*(np.sqrt(short**2+1)+short)**2)))
check('independent raw truncated sum',abs(direct-independent)<1e-10)
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'rows':rows,'N':N}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if result['passed'] else 1)
