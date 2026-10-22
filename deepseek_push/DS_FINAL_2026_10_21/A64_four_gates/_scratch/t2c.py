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

def sub_all(expr, fns):
    e = expr
    for fn, val in fns.items():
        for k in (3, 2, 1):
            e = e.subs(sp.Derivative(fn, (r, k)), sp.diff(val, r, k))
        e = e.subs(fn, val)
    return e

def num(expr, fns, vals):
    e = sub_all(expr, fns).subs(vals)
    v = sp.N(e, 40)
    return float(sp.re(v)), float(sp.im(v))

KV, a0V, gV = sp.Rational(8387, 10**13), sp.Rational(936, 10**12), sp.Rational(23, 10**25)
print("--- Schwarzschild (P=0, rho=0): EL_N, EL_f should vanish; EL_P should not")
for rv in (3, 5, 10, 50):
    fns = {N: (1 - m/r)/(1 + m/r), f: (1 + m/r)**4, P: sp.Integer(0), rho: sp.Integer(0)}
    vals = {r: sp.Integer(rv), m: sp.Integer(1), K: KV, a0: a0V, gam: gV}
    a = num(EN, fns, vals); b = num(Ef, fns, vals); c = num(EP, fns, vals)
    print(f" r={rv:3d}  EL_N={a[0]: .3e}   EL_f={b[0]: .3e}   EL_P={c[0]: .3e}")
print("\n--- nontrivial N,f,P: EL_N vs 4pi r^2 f^(3/2)(R3/(4K)-W-gam d^2/2-rho-d)")
fns = {N: 1 + sp.Rational(1, 100)*sp.exp(-r), f: 1 + sp.Rational(1, 50)*sp.exp(-r),
       P: sp.Rational(1, 10**30)*sp.exp(-r), rho: sp.Rational(1, 10**22)}
for rv in (1, 3, 7):
    vals = {r: sp.Integer(rv), K: KV, a0: a0V, gam: gV}
    e1 = num(EN, fns, vals)[0]
    e2 = num(4*sp.pi*r**2*f**sp.Rational(3, 2)*(R3/(4*K) - W - gam*d**2/2 - rho - d), fns, vals)[0]
    print(f" r={rv}  EL_N={e1:.6e}  rhs={e2:.6e}  ratio={e1/e2:.12f}")