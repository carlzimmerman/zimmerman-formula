"""Local static-background tensor principal term of the submitted action.

Wave along a nonzero scalar gradient, clock normal to the static slices.
Spatial background Hessian phi=0 at the evaluated point; coefficients frozen
for the principal symbol. No global flat-background solution is assumed.
"""
import json
import sympy as s
eps,h,hx,hxx,ht,v,F,c13,b,j,xi=s.symbols('eps h hx hxx ht v F c13 b j xi',real=True)
metric=s.diag(1,1+eps*h,1-eps*h);inv=metric.inv()
def dx(expr):return s.diff(expr,h)*hx+s.diff(expr,hx)*hxx
def partial(expr,i):return dx(expr) if i==0 else 0
Gamma=[[[s.simplify(sum(inv[k,l]*(partial(metric[l,z],i)+partial(metric[l,i],z)-partial(metric[i,z],l)) for l in range(3))/2) for z in range(3)] for i in range(3)] for k in range(3)]
Ric=s.Matrix(3,3,lambda i,z:sum(partial(Gamma[k][i][z],k)-partial(Gamma[k][i][k],z)+sum(Gamma[k][k][l]*Gamma[l][i][z]-Gamma[k][z][l]*Gamma[l][i][k] for l in range(3)) for k in range(3)))
measure=s.sqrt(metric.det())
curvature=s.simplify(s.trace(inv*Ric))
DV=s.Matrix(3,3,lambda i,z:-Gamma[0][i][z]*v)
coherence=s.trace(inv*DV*inv*DV)
K=s.diff(metric,h)*ht/2
extrinsic=s.trace(inv*K*inv*K)
def quadratic(expr):return s.simplify(s.diff(expr,eps,2).subs(eps,0)/2)
R2=quadratic(measure*curvature)
boundary=s.diff(R2,hxx)*hx
R2ibp=s.simplify(R2-dx(boundary))
L2=s.simplify((F-c13)*quadratic(measure*extrinsic)+F*R2ibp-b*j*xi**2*quadratic(measure*coherence))
kinetic=s.diff(L2,ht,2);gradient=-s.diff(L2,hx,2)
speed2=s.factor(gradient/kinetic)
assert s.simplify(R2-dx(boundary)-R2ibp)==0
assert quadratic(s.trace(inv*K)**2)==0
assert s.simplify(speed2.subs({xi:0,c13:0})-1)==0
assert s.simplify(speed2.subs(v,0)-F/(F-c13))==0
print(json.dumps(dict(scope=__doc__,quadratic_density=str(L2),
    tensor_time_coefficient=str(kinetic),tensor_space_coefficient=str(gradient),
    squared_speed=str(speed2),luminal_c13=s.solve(gradient-kinetic,c13)[0].__str__(),
    full_theory='OPEN',non_claims=['No bound on observed travel time','No full perturbation spectrum','No claim for all background geometries']),indent=2))
