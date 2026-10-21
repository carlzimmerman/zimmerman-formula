"""Step 2b: correct Euler-Lagrange for higher derivatives; verify isotropic Schwarzschild."""
import sympy as sp

r = sp.symbols('r', positive=True)
K, beta, eta, gam, a0, mu = sp.symbols('K beta eta gamma a0 mu', positive=True)
N = sp.Function('N')(r)
f = sp.Function('f')(r)
p = sp.Function('p')(r)


def R3(fe):
    L = sp.log(fe)
    return -(1/fe)*(2*sp.diff(L, r, 2) + 4*sp.diff(L, r)/r + sp.Rational(1, 2)*sp.diff(L, r)**2)


def euler(L, v):
    e = sp.diff(L, v)
    for d in L.atoms(sp.Derivative):
        if d.expr == v:
            n = d.variables[0][1]
            e = e + (-1)**n*sp.diff(sp.diff(L, d), r, n)
    return sp.simplify(e)


sqh = f**sp.Rational(3, 2)
q = sp.sqrt(f)*p
DP = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)
u = K*p/sp.sqrt(f)
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
clock = p*sp.diff(N, r)/(f*N)
L = r**2*sqh*N*(R3(f)/(4*K) + clock - W - (gam/2)*DP**2)

print("R3[isotropic Schwarzschild] =", sp.simplify(R3((1+mu/(2*r))**4)))

L0 = L.subs({p: 0}).subs(sp.Derivative(p, r), 0)
eN0 = euler(L0, N)
ef0 = euler(L0, f)
fs = (1 + mu/(2*r))**4
Ns = (1 - mu/(2*r))/(1 + mu/(2*r))
sub = {f: fs, N: Ns}
for g in (f, N):
    for n in (1, 2):
        sub[sp.Derivative(g, r, n)] = sp.diff(fs if g == f else Ns, r, n)
print("GR eN residual:", sp.simplify(eN0.subs(sub)))
print("GR ef residual:", sp.simplify(ef0.subs(sub)))
