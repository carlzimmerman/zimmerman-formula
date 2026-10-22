import sympy as sp
from gr_tools import ricci_scalar

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
beta = sp.symbols('beta', real=True)
Lam = sp.symbols('Lambda', real=True)
Kc = sp.Symbol('K', positive=True)
cs = [x, y, z]
E = sp.Symbol('E', positive=True)

def avg(expr):
    e = expr.subs(sp.cos(kk*z), (E + 1/E)/2).subs(sp.sin(kk*z), (E - 1/E)/(2*sp.I))
    e = sp.expand(sp.expand(sp.simplify(e)))
    return sp.simplify(e.coeff(E, 0))

f = eps*sig*sp.cos(kk*z)
m = sp.diag(1+f, 1-f, 1)
minv = m.inv()
R3m, _, _ = ricci_scalar(m, cs)
R3 = sp.expand(sp.series(R3m/a**2, eps, 0, 3).removeO())

h = a**2*m
Kij = sp.Matrix(3, 3, lambda i, j: sp.diff(h[i, j], t)/2)
theta = sp.expand(sum(minv[i, j]*Kij[i, j] for i in range(3) for j in range(3))/a**2)
Ksq = sp.expand(sum(minv[i, k]*minv[j, l]*Kij[i, j]*Kij[k, l]
                   for i in range(3) for j in range(3) for k in range(3) for l in range(3))/a**4)
sqrth = a**3*sp.sqrt(sp.det(m))

L = sp.simplify((R3 + Ksq - (1+beta)*theta**2 - 2*Lam)*sqrth/(4*Kc))
Lser = sp.expand(sp.series(sp.simplify(L), eps, 0, 3).removeO())
L2 = sp.expand(Lser.coeff(eps, 2))

print("theta =", sp.simplify(theta))
print("theta - 3H =", sp.simplify(theta - 3*sp.diff(a,t)/a))
print("Ksq - 9H^2 =", sp.simplify(Ksq - 9*(sp.diff(a,t)/a)**2))
L2av = avg(L2)
print("\n<L2> =", L2av)
sd = sp.Symbol('sd')
L2s = sp.expand(L2av.subs(sp.diff(sig, t), sd))
A = sp.simplify(sp.diff(L2s, sd, 2)/2)
B = sp.simplify(L2s.subs(sd, 0).subs(sig, sp.Symbol('s0')))
print("\nA (coeff sigma_dot^2) =", A)
print("B (coeff sigma^2, no sd) =", sp.simplify(L2s.subs(sd, 0)))
print("ratio -B/(A k^2) =", sp.simplify(-sp.expand(L2s.subs(sd,0))/(A*kk**2)))
