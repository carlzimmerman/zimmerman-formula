"""Step 4: linearised Hamiltonian + trace equations in the conformal gauge.
N = 1 + Phi, f = 1 - 2 Psi, P = p rhat.  Read off the P-source structure.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
K, gam = sp.symbols('K gamma', positive=True)
Phi = sp.Function('Phi')(r)
Psi = sp.Function('Psi')(r)
p = sp.Function('p')(r)
e = sp.symbols('e')          # order parameter for the expansion

N = 1 + e*Phi
f = 1 - e*2*Psi
pe = e*p


def R3(fe):
    L = sp.log(fe)
    return -(1/fe)*(2*sp.diff(L, r, 2) + 4*sp.diff(L, r)/r + sp.Rational(1, 2)*sp.diff(L, r)**2)


sqh = f**sp.Rational(3, 2)
q = sp.sqrt(f)*pe
DP = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)
W2 = K*pe**2/(2*f)
clock = pe*sp.diff(N, r)/(f*N)
L = sp.expand(r**2*sqh*N*(R3(f)/(4*K) + clock - W2 - (gam/2)*DP**2))


def euler(L, v):
    ee = sp.diff(L, v)
    for d in L.atoms(sp.Derivative):
        if d.expr == v:
            n = d.variable_count[0][1]
            ee = ee + (-1)**n*sp.diff(sp.diff(L, d), r, n)
    return sp.expand(ee)


Qs = [Phi, Psi, p]
E = {v: sp.expand(sp.diff(euler(L, v), e).subs(e, 0)) for v in Qs}
for v in Qs:
    print('--- euler wrt', v, '---')
    print(sp.simplify(E[v]/r**2))
    print()
