import argparse
import json
import math
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erfc

checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
gamma,k,sym_s=s.symbols('gamma k s',positive=True)
check('zero-speed Laplace partial fraction',s.simplify(1/(sym_s*(sym_s+gamma*k*k))-(1/sym_s-1/(sym_s+gamma*k*k))/(gamma*k*k))==0)
def average(freq,kappa,v):
    return quad(lambda mu:math.sqrt(freq*freq-v*v*kappa*kappa*(1-mu*mu)),0,1,epsabs=1e-11,epsrel=1e-12)[0]
def closed(freq,kappa,v):
    a=freq*freq-v*v*kappa*kappa
    return (freq+a/(v*kappa)*math.asinh(v*kappa/math.sqrt(a)))/2
rows=[]
for v in (0.2,1.):
    for kap in (3.,10.,30.):
        g=1.
        lo=g*kap*kap/2
        hi=g*kap*kap
        def denominator(freq): return freq*freq-g*kap*kap*average(freq,kap,v)
        check('analytic sign bracket '+str((v,kap)),lo>v*kap and denominator(lo)<0 and denominator(hi)>0)
        pole=brentq(denominator,lo,hi,xtol=1e-12,rtol=1e-14)
        residual=abs(denominator(pole))/(pole*pole)
        check('complex-momentum pole '+str((v,kap)),lo<pole<hi and residual<1e-10)
        check('independent angular integral '+str((v,kap)),abs(average(pole,kap,v)/closed(pole,kap,v)-1)<1e-10)
        rows.append({'v':v,'kappa':kap,'s_pole':pole,'s_over_kappa':pole/kap,'s_over_gamma_kappa_squared':pole/(g*kap*kap),'relative_denominator_residual':residual})
for v in (0.2,1.):
    kap=4.
    pole=brentq(lambda freq:freq*freq-kap*kap*average(freq,kap,v),8,16)
    check('pole inside unit-speed analytic tube v='+str(v),pole>kap and pole>v*kap)
heat_rows=[]
for radius in (1.,3.,10.):
    response=float(erfc(radius/2)/(4*math.pi*radius))
    check('heat benchmark off-cone positive radius='+str(radius),response>0)
    heat_rows.append({'r':radius,'t':1.,'gamma':1.,'response':response})
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'complex_momentum_poles':rows,'formal_zero_speed_heat_benchmark':heat_rows}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if result['passed'] else 1)
