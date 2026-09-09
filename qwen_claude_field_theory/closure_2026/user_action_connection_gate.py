"""Exact static spatial contraction and its quadratic background expansion.

Clock normal to static slices, zero shift, h_ij=exp(-2 Psi) delta_ij,
phi depending on x only. This computes the coherence term, not the full action.
"""
import json
import sympy as s
x,y,z=s.symbols('x y z',real=True);coordinates=(x,y,z)
p=s.Function('Psi')(x);f=s.Function('phi')(x)
h=s.exp(-2*p)*s.eye(3);inv=h.inv()
Gamma=[[[sum(inv[i,l]*(s.diff(h[l,k],coordinates[j])+s.diff(h[l,j],coordinates[k])-s.diff(h[j,k],coordinates[l])) for l in range(3))/2 for k in range(3)] for j in range(3)] for i in range(3)]
V=s.Matrix([s.diff(f,c) for c in coordinates])
DV=s.Matrix(3,3,lambda i,j:s.diff(V[j],coordinates[i])-sum(Gamma[k][i][j]*V[k] for k in range(3)))
norm=s.simplify(sum(inv[i,k]*inv[j,l]*DV[i,j]*DV[k,l] for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
eps,s0,b,j,xi=s.symbols('eps s0 b j xi',real=True)
P=s.Function('p')(x);F=s.Function('f')(x)
expanded=norm.subs({p:eps*P,f:s0*x+eps*F},simultaneous=True).doit()
quadratic=s.simplify(s.diff(expanded,eps,2).subs(eps,0)/2)
expected=(s.diff(F,x,2)+s0*s.diff(P,x))**2+2*s0**2*s.diff(P,x)**2
assert s.simplify(quadratic-expected)==0
L=-b*j*xi**2*quadratic
metric_EL=s.simplify(s.diff(L,P)-s.diff(s.diff(L,s.diff(P,x)),x))
scalar_EL=s.simplify(s.diff(L,F)-s.diff(s.diff(L,s.diff(F,x)),x)+s.diff(s.diff(L,s.diff(F,x,2)),x,2))
assert s.simplify(quadratic.subs(s0,0)-s.diff(F,x,2)**2)==0
print(json.dumps(dict(spatial_covariant_derivative=str(DV),exact_contraction=str(norm),
    quadratic_contraction=str(quadratic),coherence_metric_EL=str(metric_EL),
    coherence_scalar_EL=str(scalar_EL),full_theory='OPEN',scope=__doc__),indent=2))
