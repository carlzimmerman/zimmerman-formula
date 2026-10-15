"""Exact n=5 neutral atmosphere and finite controlled potential/gate checks."""
import json
from pathlib import Path
import sys
import sympy as s
import mpmath as mp

checks=[]
def exact(name,expr):
    v=s.simplify(expr)
    assert v==0,(name,v)
    checks.append(name)

r,b,G,M,f=s.symbols('r b G M f',positive=True)
rho=3*f*M*b**2/(4*s.pi*(r*r+b*b)**s.Rational(5,2))
ms=f*M*r**3/(r*r+b*b)**s.Rational(3,2)
psi=G*M*(1+f)/s.sqrt(r*r+b*b)
pressure=rho*psi/6
exact('enclosed support mass',s.diff(ms,r)-4*s.pi*r*r*rho)
exact('total potential Poisson',s.diff(r*r*s.diff(psi,r),r)/r**2+4*s.pi*G*rho*(1+f)/f)
exact('hydrostatic with support selfgravity',s.diff(pressure,r)+rho*G*M*(1+f)*r/(r*r+b*b)**s.Rational(3,2))
exact('EOS logarithmic slope',s.diff(pressure,r)*rho-s.Rational(6,5)*s.diff(rho,r)*pressure)
exact('Newtonian sound',s.Rational(6,5)*pressure/rho-psi/5)
exact('Schur coefficient', (f*psi/(1+f))/rho-s.Rational(5)*f/(1+f)*(psi/(5*rho)))
Kstar=G*M*(1+f)/(6*b)*(4*s.pi*b**3/(3*f*M))**s.Rational(1,5)
exact('EOS normalization identity',(6*Kstar)**5*rho-psi**5)
mu=f/(1+f)**5
exact('normalization turning derivative',s.diff(mu,f)-(1-4*f)/(1+f)**6)
exact('turning value',mu.subs(f,s.Rational(1,4))-s.Rational(256,3125))
exact('weak branch Hessian margin',1-5*f/(1+f)-(1-4*f)/(1+f))
t,q=s.symbols('t q',positive=True)
x=q*t/(1+t*t)**s.Rational(3,2)
exact('charge maximum squared bound',s.Rational(4,27)*q*q-x*x-q*q*(2*t*t-1)**2*(t*t+4)/(27*(1+t*t)**3))
exact('profile envelope derivative',s.diff(t**3/(1+t*t)**2,t)-t*t*(3-t*t)/(1+t*t)**3)
exact('profile envelope value',(t**3/(1+t*t)**2).subs(t,s.sqrt(3))-3*s.sqrt(3)/16)
exact('rational envelope', (1+t*t)**2-2*t**3-(t*t*(t-1)**2+t*t+1))
c=s.symbols('c',positive=True)
h=rho*c*c+6*pressure
sound=s.Rational(6,5)*pressure/h
exact('support effective inertia',h*(1-sound)-rho*c*c-s.Rational(24,5)*pressure)
exact('relativistic sound bound',sound-psi/(5*(c*c+psi)))
a0,MQ=s.symbols('a0 MQ',positive=True)
xphys=G*MQ/(a0*b*b)*t/(1+t*t)**s.Rational(3,2)
rhophys=rho.subs(r,b*t)
rawgate=a0*a0/(4*s.pi*G)*xphys**3/(1-xphys)**2/(rhophys*c*c)
normalized=(G*M/(b*c*c))*(MQ/M)**2*(G*MQ/(a0*b*b))/(3*f)*t**3/((1+t*t)**2*(1-xphys)**2)
exact('gate normalization from dimensional definitions',rawgate-normalized)
eps=s.Rational(1,1000000); fw=s.Rational(1,1000); gamma=s.Rational(1,2); qv=s.Rational(1,2)
ratio_bound=eps*gamma**2*qv/(3*fw)*s.Rational(1,2)*s.Rational(25,16)
exact('rational gate witness',ratio_bound-s.Rational(25,768000))
exact('Hessian witness',5*fw/(1+fw)-s.Rational(5,1001))
assert ratio_bound<1 and s.Rational(5,1001)<1 and s.Rational(1,27)<s.Rational(1,25)

mp.mp.dps=60
fv=mp.mpf('0.001')
def density(z): return 3*fv/(4*mp.pi)*(1+z*z)**mp.mpf('-2.5')
potential_checks=[]
for rv in [mp.mpf('0.1'),mp.mpf(1),mp.mpf(10)]:
    direct=4*mp.pi*(mp.quad(lambda z:z*z*density(z),[0,rv])/rv+mp.quad(lambda y:density(1/y)/(y**3),[0,1/rv]))
    target=fv/mp.sqrt(1+rv*rv)
    err=abs(direct-target)
    assert err<mp.mpf('1e-45')
    potential_checks.append({'r_over_b':str(rv),'potential':mp.nstr(target,24),'absolute_error':mp.nstr(err,12)})
grid=[]
for tv in [s.Rational(1,100),s.Rational(1,10),s.Rational(1,2),s.Integer(1),s.Integer(2),s.Integer(10),s.Integer(100)]:
    xv=x.subs({q:qv,t:tv})
    rr=eps*gamma**2*qv/(3*fw)*tv**3/((1+tv*tv)**2*(1-xv)**2)
    assert rr.evalf(50)<ratio_bound and rr>0
    grid.append({'r_over_b':str(tv),'hc_over_rho_c2':str(rr),'decimal':str(rr.evalf(22))})
result={'claim_id':'AS2-CORE-001','exact_identity_count':len(checks),'identities':checks,'potential_quadratures':potential_checks,'gate_samples':grid,
 'scope':'Exact neutral Euler-Poisson profile for fixed regular central sources; no live charged-core or full Einstein solution.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities, {len(potential_checks)} potential quadratures, {len(grid)} local-gate samples.')
