import sympy as s
import json
A,S,R,B,v,k,w,c=s.symbols('A S R B v k w c',positive=True)
d=A-S
C=S*(1-c*c)+R*c*c
D=(A*w-C*k*k)*(B*k*k*w-B*k**4+d*v*v*k*k*c*c)-d*d*v*v*k*k*c*c*w
reduced=(A*w-C*k*k)*(B*w-B*k*k+d*v*v*c*c)-d*d*v*v*c*c*w
checks={}
def check(n,x):
 x=s.simplify(x)
 assert x==0,(n,x)
 checks[n]='exact zero'
check('clock_determinant_reduction',D-k*k*reduced)
check('long_wavelength_limit',reduced.subs(k,0)-w*(A*B*w+d*S*v*v*c*c))
check('constant_term',reduced.subs(w,0)-C*k*k*(B*k*k-d*v*v*c*c))
check('parallel_band',reduced.subs({w:0,c:1})-R*k*k*(B*k*k-d*v*v))
check('perpendicular_decoupling',reduced.subs(c,0)-(A*w-S*k*k)*(B*w-B*k*k))
# For t=3/4: mu=3/5, F=123/125. Exact k=1/2 parallel witness.
case=s.factor(reduced.subs({A:s.Rational(9,8),S:s.Rational(3,5),R:s.Rational(123,125),B:1,v:1,k:s.Rational(1,2),c:1}))
assert case.subs(w,0)<0
checks['finite_parallel_negative_product']='exact negative rational'
print(json.dumps({'count':len(checks),'checks':checks,'finite_parallel_witness':str(case)},indent=2))
