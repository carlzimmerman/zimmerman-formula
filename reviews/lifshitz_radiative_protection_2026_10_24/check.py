"""Finite-shell formal one-loop background calculation, not full quantum RG."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args()
g,D,K,h,kL,kU,amp,k,n=s.symbols('gamma D K hbar kL kU amp k n',positive=True)
mu=s.symbols('mu',real=True)
checks=[]
def ck(name,e):
 r=s.factor(s.simplify(e));checks.append(dict(name=name,passed=r==0,residual=str(r)))
x,y,z=s.symbols('x y z',real=True)
V=g*(x*x+y*y+z*z)**s.Rational(3,2)/3
H=s.hessian(V,(x,y,z)).subs({x:0,y:0,z:amp})
ck('transverse_hessian',H[0,0]-g*amp)
ck('longitudinal_hessian',H[2,2]-2*g*amp)
afactor=1 if a.mutate else 1+mu**2
ck('projected_hessian',g*amp*afactor-(g*amp*(1-mu**2)+H[2,2]*mu**2))
omega=s.sqrt((D*k**4+g*amp*k*k*afactor)/K)
# d^3k/(2pi)^3 = k^2 dk dmu/(4pi^2); E=hbar omega/2.
coeff=[]
for j in range(3):
 integrand=h*k*k*s.diff(omega,amp,j).subs(amp,0)/(8*s.pi**2*s.factorial(j))
 coeff.append(s.simplify(s.integrate(s.integrate(integrand,(mu,-1,1)),(k,kL,kU))))
expected=[h*s.sqrt(D/K)*(kU**5-kL**5)/(20*s.pi**2),h*g*(kU**3-kL**3)/(18*s.pi**2*s.sqrt(K*D)),-7*h*g*g*(kU-kL)/(120*s.pi**2*s.sqrt(K)*D**s.Rational(3,2))]
for j in range(3):ck('shell_coefficient_'+str(j),coeff[j]-expected[j])
ck('angular_first_moment',s.integrate(afactor,(mu,-1,1))/2-s.Rational(4,3))
ck('angular_second_moment',s.integrate(afactor**2,(mu,-1,1))/2-s.Rational(28,15))
ck('general_n_first_moment',(1+1/n).subs(n,3)-s.Rational(4,3))
ck('general_n_second_moment',(1+2/n+3/(n*(n+2))).subs(n,3)-s.Rational(28,15))
# Positive-gradient 1D branch E=d/dx(g phi'^2).
u,curv,eps=s.symbols('u curvature eps',positive=True)
E=2*g*u*curv
ck('linear_shift_changes_euler_equation',E.subs(u,u+eps)-E-2*g*eps*curv)
ck('hbar_order',h*s.diff(coeff[2],h)-coeff[2])
r=dict(mutated=a.mutate,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,shell_coefficients=[str(c) for c in coeff],scope='finite preferred-frame shell; expansion gamma amp/(D kL^2) small; one-loop only, not uniform full quantum zero-gradient limit')
Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
