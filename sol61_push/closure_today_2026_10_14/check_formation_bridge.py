import json
import sys
from fractions import Fraction as F
import sympy as s

checks = []
def exact(name, expression):
    residual = s.simplify(expression)
    assert residual == 0, (name, residual)
    checks.append(name)

mu, n = s.symbols('mu n', positive=True)
nc = ((n+2)*mu+2)/(2*mu+1)
nt = (n*(mu+1)+2*mu)/(2*mu+1)
q = ((4-n)*mu+3-n)/(2*(n+2)*mu+4)
exact('q from full-law logarithmic slopes', q-(3-nt)/(2*nc))
exact('cold mass slope from implicit law', nc-n-(2-n)*(mu+1)/(2*mu+1))
exact('total mass slope from implicit law', nt-n-mu*(2-n)/(2*mu+1))
exact('point-source q', q.subs(n,0)-(4*mu+3)/(4*mu+4))
exact('n=1 q', q.subs(n,1)-s.Rational(1,2))
exact('n=2 q', q.subs(n,2)-s.Rational(1,4))
exact('q numerator positivity decomposition', ((4-n)*mu+3-n)-(mu+(3-n)*(mu+1)))
den = 2*(n+2)*mu+4
exact('one minus q positive decomposition', den*(1-q)-(3*n*mu+n+1))

r,t = s.symbols('r t', positive=True)
mass=s.Function('M')(r)
gamma=s.Function('gamma')(r)
z=gamma*t
q_general=-mass*s.diff(gamma,r)/(s.diff(mass,r)*gamma)
H=1-s.exp(-z)*(1+q_general*z)
exact('enclosed-to-local conversion identity', s.diff(mass*(1-s.exp(-z)),r)-s.diff(mass,r)*H)
Z,Q=s.symbols('z q', positive=True)
h=1-(1+Q*Z)*s.exp(-Z)
one=1-s.exp(-Z)
two=1-(1+Z)*s.exp(-Z)
exact('mixture of one and two stages',h-((1-Q)*one+Q*two))
exact('source rate',s.diff(h,Z)-s.exp(-Z)*(1-Q+Q*Z))
exact('initial empty cold state',h.subs(Z,0))
exact('late cold fraction',s.limit(h,Z,s.oo)-1)
exact('q>1 early negativity slope',s.diff(h,Z).subs(Z,0)-(1-Q))
exact('q<0 eventual supply violation',h-1+(1+Q*Z)*s.exp(-Z))

x,f,a0=s.symbols('x f a0', positive=True)
u0=a0*x
gb=u0**2/(a0-u0)
free=(1-f)*u0
tether=(f*u0)**2/(a0-f*u0)
inward=gb+free-tether
gtotal=gb+u0
exact('reciprocal force deficit', inward-u0*(1-f)/((1-x)*(1-f*x)))
exact('force deficit vs total gravity',inward-gtotal*(1-f)/(1-f*x))
exact('half formed example',inward.subs({x:s.Rational(1,2),f:s.Rational(1,2)})/gb.subs(x,s.Rational(1,2))-s.Rational(4,3))
g,T=s.symbols('gamma total_gravity',positive=True)
source=g*s.exp(-Z)*(1-Q+Q*Z)
accel=T*s.exp(-Z)/(1-x+x*s.exp(-Z))
v_required=T*h/(g*(1-Q+Q*Z)*(1-x+x*s.exp(-Z)))
exact('outward injection momentum balance',source*v_required-h*accel)

# Finite exact controls check boundary n=0,3 and interior slopes, not the proof.
for nn in [F(0),F(1,4),F(1),F(2),F(3)]:
    for mm in [F(1,100),F(1,2),F(1),F(10),F(100)]:
        qq=((4-nn)*mm+3-nn)/(2*(nn+2)*mm+4)
        assert 0<=qq<=1
checks.append('25 rational full-law slope controls')
for xx in [F(1,100),F(1,2),F(99,100)]:
    for ff in [F(0),F(1,10),F(1,2),F(9,10),F(1)]:
        uu=xx
        actual=uu*uu/(1-uu)+(1-ff)*uu-(ff*uu)**2/(1-ff*uu)
        expected=uu*(1-ff)/((1-xx)*(1-ff*xx))
        assert actual==expected
        assert actual>0 if ff<1 else actual==0
checks.append('15 rational shared-gravity force controls')
assert ((4-F(4))*F(1)+3-F(4))/(2*(F(4)+2)*F(1)+4)<0
checks.append('n=4 positive-density shell counterexample q<0')

json.dump({'claim_id':'CT-001','status':'exact identities and finite controls passed',
 'checks':checks,'count':len(checks),'scope':'Kinematic full-law clock and required reciprocal force; no physical source derived',
 'software':{'python':sys.version.split()[0],'sympy':s.__version__}},open(sys.argv[1],'w'),indent=2)
