import sys,json,math
import sympy as s
r,t,A,b=s.symbols('r t A b',positive=True);z=b*t/r
M=A*r*(1-s.exp(-z));D=1-(1+z)*s.exp(-z)
checks=0
def ck(expr):
 global checks
 assert s.simplify(expr)==0;checks+=1
ck(s.diff(M,r)-A*D)
ck(s.diff(M,t)-A*b*s.exp(-z))
ck(s.diff(M,r,t)-A*b*b*t*s.exp(-z)/r**2)
assert s.limit(M,r,s.oo)==A*b*t;checks+=1
assert s.limit(M,r,0)==0;checks+=1
v=-b*s.exp(-z)/D
ck(s.diff(M,t)+v*s.diff(M,r))
assert s.limit(v/r**2,r,s.oo)==-2/(b*t*t);checks+=1
assert s.limit(s.diff(M,t),r,s.oo)==A*b;checks+=1
Z=s.symbols('Z',positive=True)
DD=1-(1+Z)*s.exp(-Z)
ck(s.diff(DD,Z)-Z*s.exp(-Z))
assert DD.subs(Z,0)==0;checks+=1
for zz in [.001,.01,.1,1,10,100]:
 dd=-math.expm1(-zz)-zz*math.exp(-zz)
 assert 0<dd<1;checks+=1
json.dump(dict(checks=checks,total_mass='A beta t',required_source='A beta^2 t exp(-beta t/r)/(4 pi r^4)',transport_only_asymptotic_v='-2 r^2/(beta t^2)',scope='Deep isolated flat-speed kinematics, supplied clock, no action-derived production'),open(sys.argv[1],'w'),indent=2)
