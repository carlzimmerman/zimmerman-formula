"""Finite-regulator amplitude branch, not a full UV stability calculation."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
u,a,L,x,b,q,MP,alpha=s.symbols('u a Lambda x absY q Mpl alpha',positive=True)
Y=-b
sigma=-1 if args.mutate else 1
lag=u*Y/2+sigma*L**4*u**3*Y**3/(6*(a+u)**6)
station=(a+u)**7/(u**2*(u-a))
F=(1+x)**7/(x*x*(x-1))
xstar=1+1/s.sqrt(2)
checks=[]
def ck(name,e):
 z=s.factor(s.simplify(e));checks.append(dict(name=name,passed=z==0,residual=str(z)))
ck('stationary_branch',s.diff(lag,u).subs(L**4,station/b**2))
ck('dimensionless_branch',station.subs(u,a*x)-a**4*F)
ck('threshold_stationarity',s.diff(F,x).subs(x,xstar))
ck('global_minimum_derivative_sign',s.diff(F,x)/F-(4*x*x-8*x+2)/(x*(x-1)*(x+1)))
# Both endpoints x=1+ and infinity diverge; this is the only zero for x>1.
ck('threshold_polynomial',4*xstar*xstar-8*xstar+2)
hess=s.diff(lag,u,2).subs(L**4,station/b**2)
ck('amplitude_hessian',hess-Y*(2*u*u-4*a*u+a*a)/(u*(u-a)*(a+u)))
kin=s.Rational(1,2)+sigma*L**4*u*u*b*b/(2*(a+u)**6)
ck('amplitude_gradient_coefficient',kin.subs(L**4,station/b**2)-u/(u-a))
ck('unregulated_stationary_amplitude',s.diff(lag,u).subs(a,0).subs(u,L*s.sqrt(b)))
ck('unregulated_cubic_action',lag.subs(a,0).subs(u,L*s.sqrt(b))+2*L*b**s.Rational(3,2)/3)
Fstar=s.simplify(F.subs(x,xstar))
gmin=q*a/L*Fstar**s.Rational(1,4)
a0=q**3*MP**2/L
ck('minimum_acceleration_ratio',s.simplify((gmin/a0).subs(q,alpha*L/MP))-a/(alpha*L)**2*Fstar**s.Rational(1,4))
result=dict(mutated=args.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,scope='amplitude equation with gradients neglected; threshold gap closes; no full coupled mode or UV health claim')
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
