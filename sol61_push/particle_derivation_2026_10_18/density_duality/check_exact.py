#!/usr/bin/env python3
"""Bounded exact algebra checks; see contract.json for non-claims."""
import json
import pathlib
import platform
import sys
import sympy as s

checks = []

def zero(label, expression):
    reduced = s.simplify(s.expand(expression))
    if reduced != 0:
        raise AssertionError((label, reduced))
    checks.append({"label": label, "residual": "0"})

f, h, v, d, aux = s.symbols("f h v d aux", real=True)
A = f**2 + 4*h**2
a = 2*h**2*d/A
original = f**2*v**2 + h**2*(2*v+d)**2
completed = A*(v+a)**2 + f**2*h**2*d**2/A
zero("two-phase square completion (one independent metric component)", original-completed)
first_order = -aux**2/(4*A)+aux*(v+a)+f**2*h**2*d**2/A
zero("relativistic auxiliary-current elimination", first_order.subs(aux, 2*A*(v+a))-original)

m, M = s.symbols("m M", positive=True)
np, nm, xp, xm = s.symbols("np nm xp xm", nonnegative=True)
charge = np-nm+2*(xp-xm)
mass = m*(np+nm)+M*(xp+xm)
zero("rest-minus-charge dictionary", mass-m*charge-(2*m*nm+(M-2*m)*xp+(M+2*m)*xm))
R = s.symbols("R", real=True)
zero("conversion conserves weighted charge", 2*R+2*(-R))
zero("conversion rest-energy release", m*(2*R)+M*(-R)-(2*m-M)*R)

t, x, y, z = s.symbols("t x y z", real=True)
coords = (t, x, y, z)
B = s.zeros(4,4)
for mu in range(4):
    for nu in range(mu+1,4):
        B[mu,nu] = s.Function("B%d%d"%(mu,nu))(*coords)
        B[nu,mu] = -B[mu,nu]
def dual_current(matrix):
    return s.Matrix([s.Rational(1,2)*sum(
        s.LeviCivita(mu,nu,rho,sigma)*s.diff(matrix[rho,sigma],coords[nu])
        for nu in range(4) for rho in range(4) for sigma in range(4)
    ) for mu in range(4)])
def curl(vec):
    return s.Matrix([s.diff(vec[2],y)-s.diff(vec[1],z),
                     s.diff(vec[0],z)-s.diff(vec[2],x),
                     s.diff(vec[1],x)-s.diff(vec[0],y)])
def div(vec):
    return sum(s.diff(vec[i],coords[i+1]) for i in range(3))
Q = s.Matrix([B[2,3],B[3,1],B[1,2]])
C = s.Matrix([B[0,1],B[0,2],B[0,3]])
J = dual_current(B)
zero("dual density component", J[0]-div(Q))
spatial = -Q.diff(t)+curl(C)
for i in range(3):
    zero("dual spatial current sign component %d"%i, J[i+1]-spatial[i])
zero("identical continuity", sum(s.diff(J[mu],coords[mu]) for mu in range(4)))
Lam = [s.Function("Lambda%d"%i)(*coords) for i in range(4)]
dLam = s.Matrix(4,4,lambda mu,nu: s.diff(Lam[nu],coords[mu])-s.diff(Lam[mu],coords[nu]))
deltaJ = dual_current(dLam)
for mu in range(4):
    zero("dual gauge invariance component %d"%mu, deltaJ[mu])
zero("spatial dual potential gauge transformation x", dLam[2,3]-curl(s.Matrix(Lam[1:]))[0])
zero("spatial dual potential gauge transformation y", dLam[3,1]-curl(s.Matrix(Lam[1:]))[1])
zero("spatial dual potential gauge transformation z", dLam[1,2]-curl(s.Matrix(Lam[1:]))[2])

n = s.symbols("n", positive=True)
j, grad = s.symbols("j grad", real=True)
nr_aux = -j*grad+m*j**2/(2*n)
zero("Schrodinger auxiliary number flux elimination", nr_aux.subs(j,n*grad/m)+n*grad**2/(2*m))
rho, kinetic = s.symbols("rho kinetic", positive=True)
zero("mass-current kinetic normalization", (m*j**2/(2*n)).subs({j:kinetic/m,n:rho/m})-kinetic**2/(2*rho))

a0,K,p,E = s.symbols("a0 K p E", positive=True)
W = (-a0*K*p-a0**2*s.log(1-K*p/a0))/K
Wp = a0*K*p/(a0-K*p)
F = (a0*E-a0**2*s.log(1+E/a0))/K
p_of_E = a0*E/(K*(a0+E))
zero("rational W derivative", s.diff(W,p)-Wp)
zero("Legendre inverse gradient", Wp.subs(p,p_of_E)-E)
zero("Legendre F derivative", s.diff(F,E)-p_of_E)
# Parameterize the actual domain p<a0/K: p=p(E), E>0.  Positivity of p
# alone does not tell SymPy the logarithmic gap a0-K*p is positive.
zero("Legendre value on positive below-saturation branch",
     s.expand_log(s.factor(p_of_E*E-W.subs(p,p_of_E)-F),force=False))
zero("W quadratic coefficient", s.limit(W/p**2,p,0)-K/2)
zero("W cubic coefficient", s.limit((W-K*p**2/2)/p**3,p,0)-K**2/(3*a0))

c = s.symbols("c", real=True)
gauge_parameter = s.Matrix([0,0,c*y/m])
pure_P = m*curl(gauge_parameter)
zero("pure gauge can change local P at zero charge x", pure_P[0]-c)
zero("pure gauge y", pure_P[1])
zero("pure gauge z", pure_P[2])
zero("pure gauge has zero density", div(pure_P))
zero("pure gauge changes positive quadratic W", K*pure_P.dot(pure_P)/2-K*c**2/2)

result = {
    "status": "all_exact_residuals_zero",
    "assertions": len(checks),
    "checks": checks,
    "software": {"python": platform.python_version(), "sympy": s.__version__},
    "interpretation": "Finite formal algebra checks only; analytic gauge/topology/mass arguments and restrictions are in DENSITY_DUALITY.md.",
}
out = pathlib.Path(sys.argv[1])
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":result["status"],"assertions":len(checks),"output":str(out)}))
