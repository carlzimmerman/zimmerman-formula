#!/usr/bin/env python3
"""EQ1 check: the closed forms quoted in EQUATIONS.md for the cold dark energy around a point mass (the law, mu_K = 0,
gamma_L = 0). A note's arithmetic, not a graded lane. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import sympy as sp, os
HERE = os.path.dirname(os.path.abspath(__file__)); LOG = open(os.path.join(HERE, "eq1_check.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n")
x, a0, G, Mb, Xs = sp.symbols("x a0 G M_b X_s", positive=True)
rM = sp.sqrt(G * Mb / a0); r = x * rM
gN = G * Mb / r**2                                   # = a0 / x^2
nu = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + a0 / gN)
g = sp.simplify(gN * nu)
ok = True
def chk(name, expr, pts=((sp.Rational(3, 10),), (2,), (40,))):
    global ok
    vals = [abs(sp.N(expr.subs({x: p[0], a0: sp.Rational(7, 5), G: sp.Rational(3, 2), Mb: sp.Rational(11, 4), Xs: 59}), 40)) for p in pts]
    good = max(vals) < 1e-30; ok &= good
    P(f"[{'PASS' if good else 'FAIL'}] {name}: max residual {float(max(vals)):.1e}")
chk("the law: g_N = g^2 / (g + a0)", gN - g**2 / (g + a0))
gc = g - gN
chk("cold pull: g_c = a0 g / (g + a0)", gc - a0 * g / (g + a0))
chk("g_c g = a0 g_N", gc * g - a0 * gN)
X = (sp.sqrt(1 + 4 * x**2) - 1) / 2
chk("enclosed cold mass / M_b = nu - 1 = X(x) = (sqrt(1 + 4x^2) - 1)/2", (nu - 1) - X)
chk("enclosed cold mass / M_b = a0 / g", a0 / g - X)
rho = Mb * sp.diff(X, x) / (4 * sp.pi * rM**3 * x**2)        # (1/4 pi r^2) dM_c/dr
chk("density: rho_c = (M_b / (4 pi r_M^3)) 2 / (x sqrt(1 + 4x^2))", rho - Mb / (4 * sp.pi * rM**3) * 2 / (x * sp.sqrt(1 + 4 * x**2)))
P("   strong field (x -> 0): rho_c r ->", sp.simplify(sp.limit(rho * r, x, 0)), "  (= a0 / (2 pi G))")
P("   weak field (x -> oo): rho_c r^2 ->", sp.simplify(sp.limit(rho * r**2, x, sp.oo)), "  (= sqrt(G M_b a0) / (4 pi G))")
K = 4 * sp.pi * G; u = g / a0
J = (a0**2 / K) * (u - sp.log(1 + u))
chk("hydrostatic, isotropic: dJ/dr = -rho_c g", sp.diff(J, x) / rM + rho * g)
P("   deep field: J / (rho_c sigma^2) with sigma^2 = sqrt(G M_b a0)/2 ->", sp.limit(J / (rho * sp.sqrt(G * Mb * a0) / 2), x, sp.oo))
xt = sp.sqrt(Xs * (Xs + 1))
chk("cap: X(x_t) = X_s at x_t^2 = X_s (X_s + 1)", X.subs(x, xt) - Xs, pts=((1,),))
P("   flat speed: v^4 = (g r)^2 -> G M_b a0 as x -> oo:", sp.simplify(sp.limit((g * r)**2 / (G * Mb * a0), x, sp.oo)))
kap = sp.Rational(1, 2); rhoDE, c = sp.symbols("rho_DE c", positive=True)
a0r = kap * c * sp.sqrt(G * rhoDE)
P("   with a0 = (1/2) c sqrt(G rho_DE): a0^2 / (8 pi G) =", sp.simplify(a0r**2 / (8 * sp.pi * G)), " ; column a0/(2 pi G) =", sp.simplify(a0r / (2 * sp.pi * G)))
P(f"\nall checks pass: {bool(ok)}")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
