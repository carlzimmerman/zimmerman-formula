"""Explicit 2D band mass triplet and its massless nonlocal kernel."""
import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
checks=[]
def check(name,ok,detail=''):
 checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS ' if ok else 'FAIL ')+name)
X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);I2=s.eye(2);I4=s.eye(4)
gamma=[s.kronecker_product(X,I2),s.kronecker_product(Y,I2),s.kronecker_product(Z,X),s.kronecker_product(Z,Y),s.kronecker_product(Z,Z)]
for a in range(5):
 for b in range(a,5): check('Clifford %s %s'%(a,b),gamma[a]*gamma[b]+gamma[b]*gamma[a]==(2*I4 if a==b else s.zeros(4)))
kx,ky,y=s.symbols('kx ky y',real=True);px,py,pz=s.symbols('px py pz',real=True)
H=kx*gamma[0]+ky*gamma[1]+y*(px*gamma[2]+py*gamma[3]+pz*gamma[4])
energy2=kx*kx+ky*ky+y*y*(px*px+py*py+pz*pz)
check('Hermitian band Hamiltonian',H==H.conjugate().T)
check('isotropic mass magnitude spectrum',s.simplify(H*H-energy2*I4)==s.zeros(4))
check('two positive and two negative bands',s.trace(H)==0)
for a,b in ((2,3),(3,4),(4,2)):
 J=gamma[a]*gamma[b]/2
 check('internal rotation leaves both momenta unchanged %s%s'%(a,b),J*gamma[0]-gamma[0]*J==s.zeros(4) and J*gamma[1]-gamma[1]*J==s.zeros(4))
 check('internal rotation rotates mass %s%s'%(a,b),J*gamma[a]-gamma[a]*J==-gamma[b] and J*gamma[b]-gamma[b]*J==gamma[a])
# I(q)=int d³l/(2pi)³ 1/[l²(l+q)²]
# Feynman parametrization: int d³l/(2pi)³ 1/(l²+D)² = 1/(8pi sqrt(D)).
x=s.symbols('x',positive=True);q=s.symbols('q',positive=True)
param=quad(lambda t:1/math.sqrt(t*(1-t)),0,1,epsabs=1e-11,epsrel=1e-11)[0]
check('bubble Feynman parameter quadrature',abs(param-math.pi)<1e-10,param)
radial=quad(lambda t:t*t/(t*t+1)**2,0,math.inf,epsabs=1e-11,epsrel=1e-11)[0]/(2*math.pi**2)
check('bubble radial quadrature',abs(radial-1/(8*math.pi))<1e-12,radial)
# One four-band flavor has trace dimension d=4 and occupied band count nu=2.
bubble=1/(8*q);kernel=s.simplify(4*y*y*q*q*bubble/2)
check('massless four-band kernel',kernel==y*y*q/4)
G,nu,ell,p=s.symbols('G nu ell p',positive=True)
alpha=2*G*nu*y**3/(3*ell);a0=ell/(2*G*nu*y**3)
beta=s.pi*G*nu*y*y/(2*ell)
check('normalized nonlocal to cubic ratio',s.simplify(beta*q*p/(3*alpha*p*p)-s.pi*q/(4*y*p))==0)
check('condition scales with mass gap',s.simplify(beta*a0-s.pi/(4*y))==0)
rows=[]
for v in (50,100,200,300):
 mr=(v/299792.458)**2
 rows.append(dict(speed_km_s=v,mass_gap_times_radius_at_y_one=mr,y_for_mass_gap_times_radius_one=1/mr,nonlocal_to_cubic_estimate_y_one=math.pi/(4*mr)))
# This is dimensional derivative-scale estimate k~1/r, not exact |grad| action on 1/r.
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,band_multiplicity=2,massless_kernel='nu y² |q|/8 per sheet',normalized_kernel='beta |q|; beta=pi G nu y²/(2ell)',derivative_expansion_condition='q << y|p|; exactly massless vacuum has nonanalytic |q| kernel',galaxy_scale_estimates=rows,non_claims=['No sheet formation or bulk isotropy dynamics','No exact finite-mass nonuniform determinant','Massless kernel not asserted valid at q much smaller than nonzero mass','k~1/r comparison is dimensional estimate, not fractional derivative evaluation','No covariant stability or vacuum energy prediction','No 32pi solution'])
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print('%s %s/%s'%(result['status'],result['passed'],result['total']));raise SystemExit(result['status']!='PASS')
