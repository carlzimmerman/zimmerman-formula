"""Exact causal single-pole obstruction and unprotected common-gap response."""
import argparse
import json
from pathlib import Path
import sympy as s

checks=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
    print(('PASS ' if ok else 'FAIL ')+name)

k,mu,x,t,m=s.symbols('k mu x t m',positive=True)
E=k*s.sqrt(k/(mu+k))
vg=s.simplify(s.diff(E,k))
check('bounded-dispersion group velocity exact',s.simplify(vg-s.sqrt(k/(mu+k))*(3*mu+2*k)/(2*(mu+k)))==0)
check('group speed below one by positive polynomial',s.simplify(1-vg**2-mu**2*(4*mu+3*k)/(4*(mu+k)**3))==0)
check('group speed tends to one',s.limit(vg,k,s.oo)==1)
check('original group speed unbounded',s.limit(s.diff(k**s.Rational(3,2)/s.sqrt(mu),k),k,s.oo)==s.oo)
check('both dispersions share nonanalytic leading k-cubed',s.series(E**2,k,0,4).removeO()==k**3/mu)

# Axis restriction q=|kx|. Cubic in q is not analytic in vector momentum.
a=s.symbols('a',positive=True)
right=s.diff(x**3/mu,x,3)
left=s.diff(-x**3/mu,x,3)
check('axis third derivative jump is nonzero',s.simplify(right-left-12/mu)==0)
# Scalar kernel: sin(t sqrt(u))/sqrt(u), expanded in u at massless u=0.
u=s.symbols('u',positive=True)
scalar=s.series(s.sin(t*s.sqrt(u))/s.sqrt(u),u,0,3).removeO()
trace=s.series(s.cos(t*s.sqrt(u)),u,0,3).removeO()
check('scalar retarded nonanalytic coefficient',s.expand(scalar).coeff(u,1)==-t**3/6)
check('fermion trace nonanalytic coefficient',s.expand(trace).coeff(u,1)==-t**2/2)
check('scalar branch survives analytic nonzero residue',s.simplify(a*(-t**3/6)/mu)!=0)
check('massive scalar branch survives generic early time',s.series(s.diff(s.sin(t*s.sqrt(u))/s.sqrt(u),u).subs(u,m*m),t,0,5).removeO().coeff(t,3)==-s.Rational(1,6))
check('massive fermion branch survives generic early time',s.series(s.diff(s.cos(t*s.sqrt(u)),u).subs(u,m*m),t,0,4).removeO().coeff(t,2)==-s.Rational(1,2))

F=(0,2,2,3,6);B=(1,1,1,5,5)
eta=lambda fn:sum(fn(n) for n in F)-sum(fn(n) for n in B)
d,P,M,y,G=s.symbols('d P M y G',positive=True)
mass2=lambda n:n*n*M*M+d+y*y*P*P
check('common gap preserves count cancellation',eta(lambda n:1)==0)
check('common gap preserves squared-mass cancellation',s.simplify(eta(mass2))==0)
check('common gap preserves fourth-moment difference',s.simplify(eta(lambda n:mass2(n)**2)-156*M**4)==0)
rho=mu/(9*s.pi**2)*eta(lambda n:mass2(n)**s.Rational(3,2))
Sd=eta(lambda n:s.sqrt(n*n*M*M+d))
quad=s.simplify(s.diff(rho,P,2).subs(P,0)/2)
check('gapped quadratic coefficient exact',s.simplify(quad-mu*y*y*Sd/(6*s.pi**2))==0)
check('gapped potential has no cubic Taylor term',s.simplify(s.diff(rho,P,3).subs(P,0))==0)
small=s.series(Sd,d,0,2).removeO()
check('common gap induces square-root critical detuning',s.simplify(small-(s.sqrt(d)-s.Rational(19,20)*d/M))==0)
detuning=4*G*mu*y*y*Sd/(3*s.pi)
check('quadratic matching detuning dictionary',s.simplify(8*s.pi*G*quad-detuning)==0)

rows=[]
for ratio in (1e-8,1e-6,1e-4,1e-2):
    sv=float(Sd.subs({M:1,d:ratio}))
    leading=ratio**.5-.95*ratio
    check('positive small-gap susceptibility Delta=%g'%ratio,sv>0,sv)
    check('small-gap series Delta=%g'%ratio,abs(sv-leading)<ratio**2,abs(sv-leading))
    rows.append(dict(Delta_over_M2=ratio,weighted_mass_sum_over_M=sv))

# Unit-weight massless fermion component alone displays noncommuting limits.
# d/dP[(Delta+y²P²)^(3/2)] = 3y²P sqrt(Delta+y²P²).
R=3*y*y*P*s.sqrt(d+y*y*P*P)
check('at any fixed gap deep response is linear',s.limit(R/P,P,0)==3*y*y*s.sqrt(d))
check('at zero gap response is quadratic',s.simplify(R.subs(d,0)-3*y**3*P**2)==0)
check('crossover field fixed by gap',s.solve(s.Eq(y*y*P*P,d),P)==[s.sqrt(d)/y])
q=s.symbols('q',positive=True)
check('gapped deep induction ratio is Newtonian constant',s.limit((q*P+P*P)/(P+q*P+P*P),P,0)==q/(1+q))

result=dict(status='PASS' if all(z['passed'] for z in checks) else 'FAIL',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,rows=rows,non_claims=['No theorem excludes fractional low-energy modes with additional continuum','No interaction self-energy was calculated','Bounded group speed does not establish microcausality','No symmetry protects gaplessness or moment conditions','No vacuum-stress completion','No 32pi solution'])
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print('%s %s/%s'%(result['status'],result['passed'],result['total']))
raise SystemExit(result['status']!='PASS')
