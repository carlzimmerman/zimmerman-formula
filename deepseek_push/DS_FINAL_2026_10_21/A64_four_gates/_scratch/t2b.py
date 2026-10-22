import sympy as sp
r, K, a0, gam = sp.symbols('r K a0 gamma', positive=True)
m = sp.Symbol('m', positive=True)
N = sp.Function('N')(r); f = sp.Function('f')(r); P = sp.Function('P')(r)
R3 = -2*sp.diff(f, r, 2)/f**2 + sp.Rational(3, 2)*sp.diff(f, r)**2/f**3 - 4*sp.diff(f, r)/(r*f**2)
u = K*P
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
d = f**sp.Rational(-3, 2)*(1/r**2)*sp.diff(r**2*sp.sqrt(f)*P, r)
rho = sp.Function('rho')(r)
L = 4*sp.pi*r**2*(N*f**sp.Rational(3, 2)*(R3/(4*K) - W - gam*d**2/2) + sp.sqrt(f)*P*sp.diff(N, r) - rho*N*f**sp.Rational(3, 2))
EN = sp.diff(L, N) - sp.diff(sp.diff(L, sp.diff(N, r)), r)
EP = sp.diff(L, P) - sp.diff(sp.diff(L, sp.diff(P, r)), r)
Ef = sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r) + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)

def num(expr, subs_fn, vals):
    e = expr
    for fn, val in subs_fn.items():
        e = e.subs(fn, val)
    e = e.subs(vals)
    return complex(sp.N(e, 40))

KV, a0V, gV = sp.Rational(8387, 10**13), sp.Rational(936, 10**12), sp.Rational(23, 10**25)
print("--- Schwarzschild (P=0, rho=0): EL_N, EL_f should vanish; EL_P should not")
for rv in (3, 5, 10, 50):
    subs_fn = {N: (1 - m/r)/(1 + m/r), f: (1 + m/r)**4, P: sp.Integer(0), rho: sp.Integer(0)}
    vals = {r: sp.Integer(rv), m: sp.Integer(1), K: KV, a0: a0V, gam: gV}
    print(f" r={rv:3d}  EL_N={num(EN, subs_fn, vals): .3e}   EL_f={num(Ef, subs_fn, vals): .3e}   EL_P={num(EP, subs_fn, vals): .3e}")
print("\n--- a nontrivial P, N, f: the lapse EL should equal 4pi r^2 f^(3/2)*(R3/(4K)-W-gam d^2/2-rho-d)")
subs_fn = {N: 1 + sp.Rational(1, 100)*sp.exp(-r), f: 1 + sp.Rational(1, 50)*sp.exp(-r), P: sp.Rational(1, 10**30)*sp.exp(-r), rho: sp.Rational(1, 10**22)}
for rv in (1, 3, 7):
    vals = {r: sp.Integer(rv), K: KV, a0: a0V, gam: gV}
    e1 = num(EN, subs_fn, vals)
    e2 = num(4*sp.pi*r**2*f**sp.Rational(3, 2)*(R3/(4*K) - W - gam*d**2/2 - rho - d), subs_fn, vals)
    print(f" r={rv}  EL_N={e1:.6e}   4pi r^2 f^3/2(...)={e2:.6e}   ratio={e1/e2:.12f}")