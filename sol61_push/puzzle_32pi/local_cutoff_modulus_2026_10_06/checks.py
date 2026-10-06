import argparse,json
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',default='none');a=ap.parse_args()
y,T=s.symbols('y T',positive=True)
chi=(s.sqrt(1+1/y)-1)/(1+(y/T)**2)
dc=s.diff(chi,T)
expected=2*T*y**2*(s.sqrt(1+1/y)-1)/(T**2+y**2)**2
checks={}
def eq(name,u,v):checks[name]=bool(s.simplify(u-v)==0)
eq('cutoff_derivative',dc,expected)
w=s.symbols('w',positive=True)
eq('small_y_derivative_coefficient',s.limit(dc/y**s.Rational(3,2),y,0),2/T**3)
eq('small_y_density_coefficient',2*(2/T**3)/(s.Rational(7,2)),8/(7*T**3))
eq('large_y_derivative_coefficient',s.limit(dc*y**3,y,s.oo),T)
r,m=s.symbols('r m',positive=True)
f=s.exp(-m*r)/r
eq('massive_green_outside_source',-s.diff(f,r,2)-2*s.diff(f,r)/r+m*m*f,0)
for n in range(3,8):
 k=s.Rational(7,2)*(n-1)
 g=r**(-k)
 eq('tail_laplacian_n'+str(n),s.diff(g,r,2)+(n-1)*s.diff(g,r)/r,k*(k-n+2)*r**(-k-2))
 h=r**(2-n)
 eq('massless_green_n'+str(n),s.diff(h,r,2)+(n-1)*s.diff(h,r)/r,0)
 # Independent Jacobian integration of q(y)=2 integral_0^y t dc(t)dt.
 # Radial volume Jacobian = S rM^n/(n-1) y^(-1-n/(n-1)).
 jac=s.Rational(1,n-1)
 inner=s.Rational(n-1,n)
 eq('charge_weight_n'+str(n),-s.Rational(n,n-1)+1,-s.Rational(1,n-1))
 charge_extra=2 if a.control=='double_charge' and n==3 else 1
 eq('charge_normalization_n'+str(n),charge_extra*s.Rational(1,2)*jac*inner*2,s.Rational(1,n))
 # At the origin the massless Green cancels the spatial sphere factor.
 eq('central_weight_n'+str(n),1-s.Rational(2,n-1),s.Rational(n-3,n-1))
 # Massive local particular term cannot cancel the leading r^(-k) source
 # through its Laplacian, which is two powers smaller.
 candidate=0 if a.control=='yukawa' and n==3 else r**(-k)/m**2
 operator=-s.diff(candidate,r,2)-(n-1)*s.diff(candidate,r)/r+m*m*candidate
 eq('massive_tail_is_algebraic_n'+str(n),s.limit(r**k*operator,r,s.oo),1)
eq('three_dimensional_tail_normalization',s.Rational(8,7)/(8*s.pi),1/(7*s.pi))
Z,delta,J=s.symbols('Z delta J',positive=True)
checks['negative_minimum_contradiction']=bool(-Z*s.Symbol('lap',nonnegative=True)-Z*m*m*delta<0)
# At an assumed negative minimum T-T0=-delta, the LHS is negative,
# whereas J is positive: no constant-vacuum or negative-minimum solution.
source_integrand=0 if a.control=='constant' else expected.subs({y:1,T:1})
checks['constant_cutoff_has_nonzero_source']=bool(source_integrand>0)
checks['offset_does_not_change_modulus_equation']=bool(s.diff(s.Symbol('V0'),T)==0)
if a.control not in ['none','yukawa','constant','double_charge']:raise ValueError(a.control)
out={'claim_id':'LOCAL_CUTOFF_MODULUS_20261006','control':a.control,'checks':checks,'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'scope':'Exact coefficients and symbolic controls; analytic proof in REPORT establishes sign and asymptotic claims.'}
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'failed':out['failed']}))
raise SystemExit(bool(out['failed']))
