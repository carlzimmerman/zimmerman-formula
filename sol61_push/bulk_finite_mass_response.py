"""Finite uniform-mass static response of 3D z=3/2 eight-band toy."""
import argparse,json,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.special import beta as beta_function
from numpy.polynomial.legendre import leggauss
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
E,F,m=s.symbols('E F m',positive=True)
Jdiff=1/(E*F*(E+F))-(1/E**3+1/F**3)/4
stable=-(E-F)**2*(E*E+3*E*F+F*F)/(4*E**3*F**3*(E+F))
check('longitudinal stable subtraction identity',s.simplify(Jdiff-stable)==0)
beta1=beta_function(4/3,1/6);beta2=beta_function(7/3,7/6)
check('Euler beta recurrence',abs(beta2/beta1-8/135)<1e-14)
# Trace d=8. Common mu^(1/3) m^(-1/3) y² factored out.
CT=17*8*beta1/(576*math.pi**2)
CL=CT-5*8*beta2/(64*math.pi**2)
check('exact stiffness ratio',abs(CL/CT-43/51)<1e-14)
check('both analytic stiffness coefficients positive',0<CL<CT,dict(longitudinal=CL,transverse=CT))
rad1,err1=quad(lambda k:k**3/(1+k**3)**1.5,0,math.inf,epsabs=1e-11,epsrel=1e-11)
rad2,err2=quad(lambda k:k**6/(1+k**3)**3.5,0,math.inf,epsabs=1e-11,epsrel=1e-11)
check('independent transverse radial integral',abs(rad1-beta1/3)<1e-10,dict(value=rad1,error=err1))
check('independent longitudinal radial integral',abs(rad2-beta2/3)<1e-10,dict(value=rad2,error=err2))
D,Q=s.symbols('D Q',positive=True)
check('transverse coefficient prefactor',s.Rational(17,576)*D-s.Rational(1,16)*s.Rational(17,12)*D/3==0)
check('longitudinal ratio exact rational reduction',s.Rational(17,576)-s.Rational(5,64)*s.Rational(8,135)==s.Rational(43,1728))
cache={}
def kernels(order,q,mass=1.,mu=1.):
 if order not in cache:cache[order]=leggauss(order)
 nodes,w=cache[order];t=(nodes+1)/2;tw=w/2
 kk=(t/(1-t))**2;kw=tw*2*t/(1-t)**3
 k=kk[:,None];u=nodes[None,:]
 logratio=.5*np.log1p(2*q*u/k+(q/k)**2)
 kp=np.sqrt(k*k+q*q+2*k*q*u)
 ek=k**1.5/math.sqrt(mu);fk=kp**1.5/math.sqrt(mu)
 energy=np.sqrt(ek*ek+mass*mass);other=np.sqrt(fk*fk+mass*mass)
 proj=k+q*u
 one_minus=np.where(proj>=0,q*q*(1-u*u)/(kp*(kp+proj)),1-proj/kp)
 kd=ek*np.expm1(1.5*logratio)
 dsq=kd*kd+2*ek*fk*one_minus
 transverse=dsq/(2*energy*other*(energy+other))
 gapdiff=(ek*ek*np.expm1(3*logratio))/(energy+other)
 correction=mass*mass*gapdiff*gapdiff*(energy*energy+3*energy*other+other*other)/(2*energy**3*other**3*(energy+other))
 long=transverse-correction
 weight=(kw*kk*kk)[:,None]*w[None,:]/math.pi**2
 return float(np.sum(weight*long)),float(np.sum(weight*transverse))
rows=[]
for q in (.03,.1,.3,1.,3.,10.):
 vals=[]
 for order in (256,512,1024):
  l,tt=kernels(order,q);vals.append(dict(order=order,longitudinal=l,transverse=tt))
 last=vals[-1];previous=vals[-2]
 diff=max(abs(last[key]-previous[key])/abs(last[key]) for key in ('longitudinal','transverse'))
 check('finite-momentum refinement q='+str(q),diff<2e-4,diff)
 check('finite-momentum signs q='+str(q),last['longitudinal']>0 and last['transverse']>0)
 rows.append(dict(q=q,refinement=diff,values=vals))
 if q==.03:
  dl=abs(last['longitudinal']/q**2-CL)/CL;dt=abs(last['transverse']/q**2-CT)/CT
  check('low-momentum matches exact stiffness',max(dl,dt)<1e-3,dict(longitudinal_relative_error=dl,transverse_relative_error=dt))
# Full kernel scales as mu*m times function q/(mu*m²)^(1/3), y² separately.
base=kernels(1024,1.)
scale=[]
for mass in (.25,4.):
 q=mass**(2/3);v=kernels(1024,q,mass)
 error=max(abs(v[i]/mass-base[i])/base[i] for i in (0,1))
 check('independent mass scaling m='+str(mass),error<2e-4,error)
 scale.append(dict(mass=mass,q=q,kernels=v,normalized_error=error))
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,small_q_coefficients=dict(longitudinal=CL,transverse=CT,exact_ratio='43/51',common_factor='mu^(1/3) m^(-1/3) y²',CT_exact='17d B(4/3,1/6)/(576pi²)',CL_exact='43d B(4/3,1/6)/(1728pi²)',d=8),finite_momentum=rows,mass_scaling=scale,scope='Uniform nonzero mass, zero temperature, static q, subtracted q=0 curvature. Full nonuniform determinant uncomputed.',non_claims=['No full dynamic or covariant stability','No critical cancellation protection','No vacuum energy prediction','No causal UV completion','No 32pi derivation'])
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s; CL %.12g CT %.12g'%(result['status'],result['passed'],result['total'],CL,CT));raise SystemExit(result['status']!='PASS')
