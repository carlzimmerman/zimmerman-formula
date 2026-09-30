"""Isotropic 3D z=3/2 spectral toy, no local/covariant completion."""
import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
m,K,mu,nu=s.symbols('m K mu nu',positive=True);checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
# Change t=k^(3/2)/sqrt(mu): k²dk=(2mu/3)t dt.
t,k=s.symbols('t k',positive=True)
kt=mu**s.Rational(1,3)*t**s.Rational(2,3)
check('three dimensional radial Jacobian',s.simplify(kt**2*s.diff(kt,t)-2*mu*t/3)==0)
ren=-nu*mu*((K*K+m*m)**s.Rational(3,2)-K**3-m**3)/(9*s.pi**2)+nu*mu*K*m*m/(6*s.pi**2)
check('finite positive bulk cubic',s.limit(ren,K,s.oo)==nu*mu*m**3/(9*s.pi**2))
# K is energy cutoff t, physical momentum cutoff (mu K²)^(1/3).
rows=[]
for ratio in (2,10,100):
 for mass in (.5,1.,2.):
  cutoff=ratio*mass;momentum=(cutoff*cutoff)**(1/3)
  value,error=quad(lambda kk:kk*kk*(math.sqrt(kk**3+mass*mass)-kk**1.5),0,momentum,epsabs=1e-11,epsrel=1e-11)
  numeric=-value/(2*math.pi**2)+cutoff*mass*mass/(6*math.pi**2)
  exact=float(ren.subs({nu:1,mu:1,K:cutoff,m:mass}));relative=abs(numeric-exact)/mass**3
  check('direct physical momentum quadrature ratio=%s mass=%s'%(ratio,mass),relative<1e-8,relative)
  rows.append(dict(cutoff_over_mass=ratio,mass=mass,finite_cubic_coefficient=numeric/mass**3,continuum=1/(9*math.pi**2)))
z,d=s.symbols('z d',positive=True)
check('cubic energy power selects z=3/2 in d=3',s.solve(s.Eq(1+3/z,3),z)==[s.Rational(3,2)])
check('ordinary relativistic bulk has fourth power',1+3/s.Integer(1)==4)
G,y,rho=s.symbols('G y rho',positive=True)
alpha=4*G*nu*mu*y**3/(9*s.pi);a0=1/(3*alpha)
check('bulk response scale',s.simplify(a0-3*s.pi/(4*G*nu*mu*y**3))==0)
C=s.simplify(8*s.pi*G*rho/a0**2)
check('vacuum density still free',s.diff(C,rho)!=0)
check('target is extra vacuum density relation',s.solve(s.Eq(C,32*s.pi),rho)==[9*s.pi**2/(4*G**3*mu**2*nu**2*y**6)])
# massless group velocity for declared dispersion.
check('UV velocity grows without bound',s.limit(s.diff(k**s.Rational(3,2)/s.sqrt(mu),k),k,s.oo)==s.oo)
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,rows=rows,dispersion='sqrt(k³/mu+m²)',hypothetical_a0=str(a0),non_claims=['Nonanalytic spatial operator, not a local covariant theory','No UV causal completion','No dynamical origin of z=3/2 or mu','Critical quadratic cancellation imposed','No absolute vacuum energy prediction','No 32pi solution'])
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
