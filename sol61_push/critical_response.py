"""Static critical polarization and scoped gapless-mode integrals, not 32pi proof."""
import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
p=s.symbols('p',positive=True);g,h,alpha,delta=s.symbols('g h alpha delta',positive=True)
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
V=p*p/4-h*p/2-h*h*s.log(1-p/h)/2
force=p*(2*h-p)/(2*(h-p))
check('exact auxiliary potential derivative',s.simplify(s.diff(V,p)-force)==0)
check('radial internal stiffness',s.simplify(s.diff(V,p,2)-(s.Rational(1,2)+h*h/(2*(h-p)**2)))==0)
check('deep potential cubic term',s.limit((V-p*p/2)/p**3,p,0)==1/(6*h))
b=s.sqrt(g*g+h*h)-h;chosen=g-b
check('P2 selected polarization solves stationarity',s.simplify(force.subs(p,chosen)-g)==0)
check('bounded polarization at Newton limit',s.limit(chosen,g,s.oo)==h)
W=(g*s.sqrt(g*g+h*h)+h*h*s.asinh(g/h))/2-h*g
# Equality of derivatives and zero values avoids log/asinh branch simplification.
check('eliminated action derivative equals P2',s.simplify(g-chosen-b)==0)
check('eliminated action zero constant',s.limit(V,p,0)==0 and s.limit(W,g,0)==0)
check('deep induction',s.limit(b/g**2,g,0)==1/(2*h))
check('Newton normalized induction',s.limit(b/g,g,s.oo)==1)
# General radial critical potential; alignment follows from minimizing -g dot p.
Vc=p*p/2+alpha*p**3
check('critical radial equation',s.diff(Vc,p)==p+3*alpha*p*p)
check('orientation follows energy minimum',s.diff(-g*p*s.cos(s.Symbol('theta',real=True)),s.Symbol('theta',real=True),2).subs(s.Symbol('theta',real=True),0)==g*p)
root=2*g/(1+s.sqrt(1+12*alpha*g))
check('critical positive branch exact',s.simplify(root+3*alpha*root**2-g)==0)
check('critical response coefficient',s.limit((g-root)/g**2,g,0)==3*alpha)
check('critical response approaches Newton',s.limit((g-root)/g,g,s.oo)==1)
check('critical response static radial ellipticity',s.simplify(s.diff(g-root,g)-(1-1/s.sqrt(1+12*alpha*g)))==0)
check('analytic quartic gives wrong radial order',s.diff(p*p/2+alpha*p**4,p)-p==4*alpha*p**3)
# Generic delta, positive-detuning branch only.
pr=2*g/(1+delta+s.sqrt((1+delta)**2+12*alpha*g))
check('detuned branch exact',s.simplify((1+delta)*pr+3*alpha*pr**2-g)==0)
check('positive detuning returns linear deep response',s.limit((g-pr)/g,g,0)==delta/(1+delta))
q=s.symbols('q',positive=True)
check('constant vacuum term has no constitutive effect',s.diff(Vc+q,p)==s.diff(Vc,p))
# Two-dimensional occupied fermion bands: E=-nu int d²k/(2pi)² sqrt(k²+m²).
m,K,nu=s.symbols('m K nu',positive=True)
ren=-nu*((K*K+m*m)**s.Rational(3,2)-K**3-m**3)/(6*s.pi)+nu*K*m*m/(4*s.pi)
check('fermion finite nonanalytic term',s.limit(ren,K,s.oo)==nu*m**3/(6*s.pi))
# Thermal real scalar zero-mode: T/2 int d³k/(2pi)³ log(1+m²/k²).
# Differentiate in m, subtract analytic K term, then integrate from m=0.
T=s.symbols('T',positive=True)
boson_derivative=-T*m*m*s.atan(K/m)/(2*s.pi**2)
check('thermal boson cubic derivative sign',s.limit(boson_derivative,K,s.oo)==-T*m*m/(4*s.pi))
check('thermal boson finite cubic term',s.integrate(-T*m*m/(4*s.pi),(m,0,m))==-T*m**3/(12*s.pi))
rows=[]
for ratio in (2.,10.,100.):
 for mass in (.3,1.,2.):
  cutoff=ratio*mass
  integral,err=quad(lambda k:k*(math.sqrt(k*k+mass*mass)-k),0,cutoff,epsabs=1e-11,epsrel=1e-11)
  num=-integral/(2*math.pi)+cutoff*mass*mass/(4*math.pi)
  exact=float(ren.subs({nu:1,K:cutoff,m:mass}))
  error=abs(num-exact)/mass**3
  check('fermion cutoff quadrature ratio=%s mass=%s'%(ratio,mass),error<1e-8,dict(normalized_error=error))
  rows.append(dict(cutoff_over_mass=ratio,mass=mass,finite_coefficient=num/mass**3,continuum_coefficient=1/(6*math.pi)))
G,y,ell,rho=s.symbols('G y ell rho',positive=True)
alphaf=2*G*nu*y**3/(3*ell);a0=1/(3*alphaf)
check('hypothetical sheet to bulk response dictionary',s.simplify(a0-ell/(2*G*nu*y**3))==0)
C=s.simplify(8*s.pi*G*rho/a0**2)
check('vacuum density remains independent',s.diff(C,rho)!=0)
check('target requires extra density condition',s.solve(s.Eq(C,32*s.pi),rho)==[ell**2/(G**3*nu**2*y**6)])
result=dict(status='PASS' if all(x['passed'] for x in checks) else 'FAIL',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,fermion_quadratures=rows,auxiliary_potential=str(V),critical_a0='1/(3alpha)',hypothetical_fermion_a0=str(a0),hypothetical_C=str(C),non_claims=['No microscopic vector mass representation','No stream sheet generation or density selection','No covariant completion','Critical quadratic cancellation imposed','Exact P2 potential inverse designed','No absolute vacuum energy prediction','Not a 32pi solution'])
a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
