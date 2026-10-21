"""Step 2: verify the reduced static system reproduces isotropic Schwarzschild (p=0),
then extract the exact P equation on a fixed GR background.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
K, beta, eta, gam, a0, mu = sp.symbols('K beta eta gamma a0 mu', positive=True)
N = sp.Function('N')(r)
f = sp.Function('f')(r)
p = sp.Function('p')(r)


def R3(fe):
    L = sp.log(fe)
    return -(1/fe)*(2*sp.diff(L, r, 2) + 4*sp.diff(L, r)/r + sp.Rational(1, 2)*sp.diff(L, r)**2)


def eqs_of(Lexpr, dep):
    out = []
    for v in dep:
        e = sp.diff(Lexpr, v)
        for d in sorted(Lexpr.atoms(sp.Derivative), key=str):
            if d.expr == v:
                e -= sp.diff(sp.diff(Lexpr, d), r, d.variables[0])
                # second derivatives
        out.append(sp.simplify(e))
    return out


sqh = f**sp.Rational(3, 2)
q = sp.sqrt(f)*p
DP = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)
u = K*p/sp.sqrt(f)
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
clock = p*sp.diff(N, r)/(f*N)
L = r**2*sqh*N*(R3(f)/(4*K) + clock - W - (gam/2)*DP**2)


def euler(L, v):
    e = sp.diff(L, v)
    for d in L.atoms(sp.Derivative):
        if d.expr == v:
            e = e - sp.diff(sp.diff(L, d), r)
    return sp.simplify(e)


L0 = L.subs({p: 0}).subs(sp.Derivative(p, r), 0)
eN0 = euler(L0, N)
ef0 = euler(L0, f)

# isotropic Schwarzschild: f = (1+mu/(2r))^4, N = (1-mu/(2r))/(1+mu/(2r))
fs = (1 + mu/(2*r))**4
Ns = (1 - mu/(2*r))/(1 + mu/(2*r))
sub = {f: fs, N: Ns, sp.Derivative(f, r): sp.diff(fs, r), sp.Derivative(f, r, 2): sp.diff(fs, r, 2),
       sp.Derivative(N, r): sp.diff(Ns, r), sp.Derivative(N, r, 2): sp.diff(Ns, r, 2)}
print("GR eN residual:", sp.simplify(eN0.subs(sub)))
print("GR ef residual:", sp.simplify(ef0.subs(sub)))
print("g00 check:", sp.simplify(-Ns**2 - (-(1-mu/(2*r))**2/(1+mu/(2*r))**2)))
