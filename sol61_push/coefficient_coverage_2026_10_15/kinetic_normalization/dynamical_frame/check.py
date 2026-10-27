import sympy as s
import json
A,S,B,v,k,w,eps=s.symbols('A S B v k w eps',positive=True)
p,h,b=s.symbols('p h b',real=True)
d=A-S
e0,j,ep=s.symbols('e0 j ep',real=True)
# chi=v*z+eps*pi, time derivative eps*p, transverse derivative eps*h.
# u=(sqrt(1+eps^2*b^2),0,0,eps*b): unit timelike exactly.
z=s.sqrt(1+eps**2*b**2)*eps*p+eps*b*v
X=v*v+eps**2*(h*h-p*p)
sp=s.sqrt(X+z*z)
dsp=s.series(sp,eps,0,3).removeO()-v
energy=e0+j*dsp+ep*dsp*dsp/2
L=A*z*z/2-energy
L2=s.expand(s.series(L,eps,0,3).removeO()).coeff(eps,2).subs(j,S*v)
target=A*p*p/2-S*h*h/2+d*v*b*p+d*v*v*b*b/2
checks={}
def check(name,value):
    value=s.simplify(value)
    assert value==0,(name,value)
    checks[name]='exact zero'
check('unit_constraint',-(1+eps**2*b*b)+eps**2*b*b+1)
check('quadratic_action',L2-target)
# omega^2 is w; off-diagonal product is d^2 v^2 w.
D=(A*w-S*k*k)*(B*w-B*k*k+d*v*v)-d*d*v*v*w
check('homogeneous_factor',D.subs(k,0)-w*(A*B*w+d*S*v*v))
root=-d*S*v*v/(A*B)
check('negative_branch_root',D.subs({k:0,w:root}))
check('constant_term',D.subs(w,0)-S*k*k*(B*k*k-d*v*v))
# Eliminate scalar conserved momentum p_chi=0 at k=0.
check('reduced_tilt_mass',target.subs({h:0,p:-d*v*b/A})-d*S*v*v*b*b/(2*A))
# Canonical Hamiltonian; P is scalar momentum and Q vector momentum.
P,Q=s.symbols('P Q',real=True)
H=(P-d*v*b)**2/(2*A)+Q*Q/(2*B)-d*v*v*b*b/2
check('hamiltonian_zero_momentum',H.subs({P:0,Q:0})+d*S*v*v*b*b/(2*A))
# Stable pinning is only a diagnostic: it invokes an external reference.
m=s.symbols('m',positive=True)
Dpin=(A*w-S*k*k)*(B*w-B*k*k+d*v*v-m)-d*d*v*v*w
check('pinned_constant',Dpin.subs(w,0)-S*k*k*(B*k*k+m-d*v*v))
t=s.symbols('t',positive=True)
mu=t/s.sqrt(1+t*t)
f=t*(t*t+2)/(1+t*t)**s.Rational(3,2)
check('radial_minus_transverse',f-mu-t/(1+t*t)**s.Rational(3,2))
check('equal_normalization_radial_speed',f/mu-(t*t+2)/(1+t*t))
# Analytic witness with rational stiffness S=3/5 (t=3/4), A=9/8, B=v=1.
witness=s.factor(D.subs({A:s.Rational(9,8),S:s.Rational(3,5),B:1,v:1,k:0}))
check('rational_growth_witness',root.subs({A:s.Rational(9,8),S:s.Rational(3,5),B:1,v:1})+s.Rational(7,25))
# Finite wave number witness: k^2=1/4 below threshold 21/40.
finite=s.factor(D.subs({A:s.Rational(9,8),S:s.Rational(3,5),B:1,v:1,k:s.Rational(1,2)}))
assert finite.subs(w,0)<0
checks['finite_wavelength_negative_product']='exact negative rational'
print(json.dumps({'count':len(checks),'checks':checks,'homogeneous_witness':str(witness),'finite_wavelength_witness':str(finite),'sympy':s.__version__},indent=2))
