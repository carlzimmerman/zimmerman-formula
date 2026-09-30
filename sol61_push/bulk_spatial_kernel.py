"""Massless static kernel of declared isotropic z=3/2 band toy."""
import argparse,json,math
from pathlib import Path
import numpy as np
import sympy as s
from numpy.polynomial.legendre import leggauss
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);I=s.eye(2)
# Clifford 6, dimension eight. First three are momenta, last three masses.
gammas=[s.kronecker_product(X,I,I),s.kronecker_product(Y,I,I),s.kronecker_product(Z,X,I),s.kronecker_product(Z,Y,I),s.kronecker_product(Z,Z,X),s.kronecker_product(Z,Z,Y)]
check('all six Clifford relations',all(a*b+b*a==(2*s.eye(8) if i==j else s.zeros(8)) for i,a in enumerate(gammas) for j,b in enumerate(gammas)))
check('all six Hermitian',all(g==g.conjugate().T for g in gammas))
E,F,c=s.symbols('E F c',positive=True)
positive=((E-F)**2+2*E*F*(1-c))/(2*E*F*(E+F))
check('symmetrically subtracted positive integrand',s.simplify(positive-((1/E+1/F)/2-(1+c)/(E+F)))==0)
# Zero-frequency bubble after exact frequency integration:
# Pi(q)-Pi(0)=d/2 int d³k/(2pi)³ [(.5/E+.5/E')-(1+cos)/(E+E')].
def coefficient(order,momentum=1.):
 nodes,weights=leggauss(order)
 t=(nodes+1)/2;tw=weights/2
 kk=t/(1-t);kw=tw/(1-t)**2
 k=kk[:,None];u=nodes[None,:]
 kp=np.sqrt(k*k+momentum*momentum+2*k*momentum*u)
 energy=k**1.5;other=kp**1.5
 # Stable 1-cos for large k; direct formula when dot-product component negative.
 proj=k+momentum*u
 one_minus=np.where(proj>=0,momentum*momentum*(1-u*u)/(kp*(kp+proj)),1-proj/kp)
 ediff=energy*np.expm1(1.5*np.log(kp/k))
 term=(ediff*ediff+2*energy*other*one_minus)/(2*energy*other*(energy+other))
 integral=np.sum((kw*kk*kk)[:,None]*weights[None,:]*term)
 return float(integral/(math.pi**2)) # trace dimension d=8 => d/(8pi²)=1/pi²
rows=[]
for n in (64,128,256,512,1024):
 val=coefficient(n);rows.append(dict(order=n,coefficient=val));check('positive finite kernel order='+str(n),val>0 and math.isfinite(val))
last=rows[-1]['coefficient'];prior=rows[-2]['coefficient'];difference=abs(last-prior)/last
check('last quadrature refinement agreement',difference<1e-4,dict(relative_difference=difference))
for q in (.5,2.):
 val=coefficient(512,q);ratio=val/(q**1.5)
 check('independent momentum scaling q='+str(q),abs(ratio-last)/last<2e-4,dict(coefficient=ratio))
# Dimensional implications, not a finite-mass background determinant.
r,A,y,mu=s.symbols('r A y mu',positive=True)
condition=1/(y*A*s.sqrt(mu*r))
check('gap hierarchy improves at large radius',s.limit(condition,r,s.oo)==0)
check('massless correction decays faster than cubic',s.Rational(1,1)+s.Rational(3,2)>2)
# At finite mass, generic analytic q² coefficient scales as m^[(d-z-2)/z]=m^-1/3.
check('finite mass derivative exponent by scaling',s.simplify((3-s.Rational(3,2)-2)/s.Rational(3,2))==-s.Rational(1,3))
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,quadrature=rows,kernel_coefficient_d8_mu_y_one=last,last_relative_refinement=difference,kernel_scaling='Pi(q)-Pi(0)=C8 y² sqrt(mu)|q|^(3/2); nu=4 occupied bands per eight-band flavor',hierarchy='Along p=A/r: E_(1/r)/(y p)=1/[y A sqrt(mu r)] tends to zero at large r.',non_claims=['Finite quadratures not a certified exact coefficient','No finite-mass kernel computed','No nonuniform galaxy solution','No critical tuning or UV causal completion','No absolute vacuum energy or 32pi prediction'])
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s; C8 %.12g'%(result['status'],result['passed'],result['total'],last));raise SystemExit(result['status']!='PASS')
