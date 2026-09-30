import argparse
import json
import math
from scipy.integrate import quad
from scipy.special import beta as beta_function, binom, zeta

checks=[]
def check(name, condition): checks.append({'name':name,'passed':bool(condition)})
def integral(beta):
    def f(t): return t**(-beta)/(math.hypot(1,t)+1)**2
    return quad(f,0,1,epsabs=1e-11,epsrel=1e-11)[0]+quad(f,1,math.inf,epsabs=1e-11,epsrel=1e-11)[0]
def beta_integral(beta):
    return 2**(-beta-2)*(beta_function((1-beta)/2,beta+1)+beta_function((3-beta)/2,beta+1))
rows=[]
for b in (0.25,0.5,0.75):
    numeric=integral(b)
    exact=beta_integral(b)
    check('independent Mellin integral beta='+str(b),abs(numeric-exact)<1e-9)
    J=1.5*zeta(1+b,1)*exact
    for delta in (1e-2,1e-4,1e-6):
        correction=0.0
        for k in range(2,8):
            ak=-binom(0.5,k)*zeta(2*k-2,1)
            correction+=3*ak*delta**(2*k-3-b)/(2*k-3-b)
        k=8
        omitted=abs(3*(-binom(0.5,k)*zeta(2*k-2,1))*delta**(2*k-3-b)/(2*k-3-b))
        Q=b*delta**b*(J-correction)
        leading=b*delta**b*J
        check('positive finite ensemble response beta='+str(b)+' delta='+str(delta),0<Q<1)
        first_correction=b*math.pi**2*delta/(16*(1-b))
        remainder_bound=b*math.pi**4*delta**3/(480*(3-b))
        check('derived heavy-tail correction beta='+str(b)+' delta='+str(delta),abs(Q-(leading-first_correction))<=remainder_bound+1e-13*leading)
        rows.append({'beta':b,'delta':delta,'normalized_cubic_response':Q,'leading_prediction':leading,'analytic_series_error_bound':b*delta**b*omitted})

for n in (1,2,7):
    b=0.5
    def f(x): return 1.5*x**(-b)/(math.hypot(n,x)+n)**2
    numeric=quad(f,0,1,epsabs=1e-11,epsrel=1e-11)[0]+quad(f,1,math.inf,epsabs=1e-11,epsrel=1e-11)[0]
    predicted=1.5*n**(-1-b)*beta_integral(b)
    check('individual mode Mellin scaling n='+str(n),abs(numeric-predicted)<1e-9)

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'rows':rows}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if result['passed'] else 1)
