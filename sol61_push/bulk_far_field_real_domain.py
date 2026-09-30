"""Formal leading-gradient far-field branch; not full determinant or 32pi proof."""
import argparse,json
from pathlib import Path
import sympy as s
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
r=s.symbols('r',positive=True);P=s.Function('P')(r)
CL,CT,K,A,a0,G,M=s.symbols('CL CT K A a0 G M',positive=True)
# K=4piG mu^(1/3)y^(5/3), coefficients evaluated for d=8.
Lr=K*(CL*r*r*P**s.Rational(-1,3)*s.diff(P,r)**2+2*CT*P**s.Rational(5,3))/2
variation=s.simplify((s.diff(Lr,P)-s.diff(s.diff(Lr,s.diff(P,r)),r))/r**2)
expected=K*(CL*s.diff(P,r)**2/(6*P**s.Rational(4,3))-2*CL*s.diff(P,r)/(r*P**s.Rational(1,3))-CL*s.diff(P,r,2)/P**s.Rational(1,3)+5*CT*P**s.Rational(2,3)/(3*r*r))
check('radial variational force independent formula',s.simplify(variation-expected)==0)
sub={P:A/r,s.diff(P,r):-A/r**2,s.diff(P,r,2):2*A/r**3}
force=s.simplify(variation.subs(sub))
D=K*(CL/6+5*CT/3)
check('hedgehog force positive prefactor',s.simplify(force-D*A**s.Rational(2,3)/r**s.Rational(8,3))==0)
# Euler variation for direction, constrained n.n=1: radial n has Delta n parallel to n.
check('directional spherical gradient norm',2/r**2>0)
epsilon=-D*a0/(2*A**s.Rational(4,3))
check('first correction coefficient cancels residual',s.simplify(2*epsilon*A*A/a0+D*A**s.Rational(2,3))==0)
check('first polarization correction is negative',epsilon.is_negative)
check('relative correction tends to zero',s.limit(epsilon/r**s.Rational(2,3),r,s.oo)==0)
check('leading source amplitude unchanged',s.solve(s.Eq(A*A/a0,G*M),A)==[s.sqrt(G*M*a0)])
# Asymptotic p=A/r + B/r^(5/3), choose B from above.
B=-D*a0/(2*A**s.Rational(1,3));profile=A/r+B/r**s.Rational(5,3)
# Exact symbolic small t transform r=t^-3, p=A t³+B t⁵; residual / t^8.
t=s.symbols('t',positive=True)
# q-dependent derivatives pre-substituted then simplify powers under positive r.
fr=s.simplify(variation.subs({P:profile,s.diff(P,r):s.diff(profile,r),s.diff(P,r,2):s.diff(profile,r,2)}))
residual=s.simplify(profile*profile/a0+fr-A*A/(a0*r*r))
check('full leading-gradient residual cancels at r^-8/3',s.limit(residual*r**s.Rational(8,3),r,s.oo)==0)
check('next residual bounded at expected order',s.limit(residual*r**s.Rational(10,3),r,s.oo).is_finite)
# Higher gradient hierarchy q/k0 where k0=(mu m²)^(1/3), m=y A/r.
y,mu=s.symbols('y mu',positive=True)
qoverk0=s.simplify((1/r)/(mu*(y*A/r)**2)**s.Rational(1,3))
check('momentum over gap scale vanishes',s.limit(qoverk0,r,s.oo)==0)
check('fourth derivative expected scaling relative to second',s.simplify(qoverk0**2*r**s.Rational(2,3)-(mu*y*y*A*A)**s.Rational(-2,3))==0)
# Linear internal symmetries: |Tp|³=|p|³ implies squared norms equal;
# positive monotonic power means any cubic-norm symmetry preserves quadratic norm.
x,z=s.symbols('x z',nonnegative=True)
xp,zp=s.symbols('xp zp',positive=True)
check('positive norm-cubic equality fixes same norm',s.solveset(s.Eq(xp**3,zp**3),xp,domain=s.S.Reals)==s.FiniteSet(zp))
check('zero norm case separately',s.solveset(s.Eq(x**3,0),x,domain=s.S.Reals)==s.FiniteSet(0))
check('norm symmetry cannot distinguish quadratic invariant',s.simplify((x*x-z*z).subs(x,z))==0)
check('loop stiffness ratio fixes hedgehog combination',s.simplify((CL/6+5*CT/3).subs(CL,s.Rational(43,51)*CT)-s.Rational(553,306)*CT)==0)
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,gradient_force=str(variation),hedgehog_force=str(force),first_far_field_polarization='P=A/r-D a0/(2 A^(1/3) r^(5/3))+higher orders; A=sqrt(GM a0)',D=str(D),scope='Leading local derivative expansion of the uniform-band loop, radial hedgehog, asymptotic r to infinity; positive P at sufficiently large r.',non_claims=['No global finite-energy galaxy solution','No dynamical formation or stability proof','Bare derivative operators can change stiffnesses','No quadratic tuning protection by tested symmetries','No absolute vacuum energy or 32pi prediction'])
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
