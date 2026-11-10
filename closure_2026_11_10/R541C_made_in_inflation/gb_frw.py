"""R541C part 1 (sympy): Gauss-Bonnet in FRW and Schwarzschild, the charge equation of action (A) + gamma*tau*G_GB.
Units c = 1, K = 4 pi G. Prints to gb_frw.out (run: python gb_frw.py > gb_frw.out)."""
import sympy as sp


def curvature(g, X):
    n = len(X); gi = g.inv()
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                             for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]
    Riem = sp.MutableDenseNDimArray.zeros(n, n, n, n)  # R^a_{bcd}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d])
                    e += sum(Gam[a][c][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][c] for k in range(n))
                    Riem[a, b, c, d] = sp.simplify(e)
    Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(Riem[a, b, a, d] for a in range(n))))
    Rs = sp.simplify(sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n)))
    # lower first index, raise all
    Rl = sp.MutableDenseNDimArray.zeros(n, n, n, n)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rl[a, b, c, d] = sum(g[a, e] * Riem[e, b, c, d] for e in range(n))
    # metrics here are diagonal: raising is multiplication by gi diagonal
    diag = [gi[i, i] for i in range(n)]
    assert all(gi[i, j] == 0 for i in range(n) for j in range(n) if i != j)
    Kr = sp.simplify(sum(Rl[a, b, c, d] ** 2 * diag[a] * diag[b] * diag[c] * diag[d]
                         for a in range(n) for b in range(n) for c in range(n) for d in range(n)))
    RicSq = sp.simplify(sum(Ric[a, b] ** 2 * diag[a] * diag[b] for a in range(n) for b in range(n)))
    GB = sp.simplify(Rs ** 2 - 4 * RicSq + Kr)
    return Rs, RicSq, Kr, GB


t, r, th, ph, x, y, z = sp.symbols('t r theta phi x y z')
a = sp.Function('a')(t); N = sp.Function('N')(t)
H, Hd = sp.symbols('H Hdot')

print("=== KA1: FRW with lapse ===")
gF = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2)
Rs, RicSq, Kr, GB = curvature(gF, [t, x, y, z])
sqg = N * a ** 3
CS = 8 * sp.diff(a, t) ** 3 / N ** 3
print("sqrt(-g) G_GB - 8 d/dt(adot^3/N^3) =", sp.simplify(sqg * GB - sp.diff(CS, t)))
GB1 = sp.simplify(GB.subs(N, 1).doit())
# express with H = adot/a
ad = sp.diff(a, t); add = sp.diff(a, t, 2)
GBH = sp.simplify(GB1.subs(add, (Hd + H ** 2) * a).subs(ad, H * a))
print("G_GB (N=1) in H, Hdot:", sp.factor(GBH), " (target 24 H^2 (Hdot + H^2))")
print("  de Sitter (Hdot=0):", sp.factor(GBH.subs(Hd, 0)))
print("  radiation (Hdot=-2H^2):", sp.factor(GBH.subs(Hd, -2 * H ** 2)))
print("  matter (Hdot=-3/2 H^2):", sp.factor(GBH.subs(Hd, -sp.Rational(3, 2) * H ** 2)))
print("  w-era general, Hdot = -(3/2)(1+w)H^2:", sp.factor(GBH.subs(Hd, -sp.Rational(3, 2) * (1 + sp.Symbol('w')) * H ** 2)))

print("\n=== KA2: Schwarzschild ===")
M = sp.symbols('M', positive=True)
f = 1 - 2 * M / r
gS = sp.diag(-f, 1 / f, r ** 2, r ** 2 * sp.sin(th) ** 2)
RsS, RicSqS, KrS, GBS = curvature(gS, [t, r, th, ph])
print("R =", RsS, " Ric^2 =", RicSqS, " G_GB =", sp.simplify(GBS), " (target 48 M^2/r^6)")

print("\n=== Charge equation from the minisuperspace of (A) + gamma tau G_GB, P = 0 ===")
K, mu, Lam, gam, rb0 = sp.symbols('K mu_K Lambda gamma rho_b0', positive=True)
tau = sp.Function('tau')(t)
Q = sp.diff(tau, t) / N
L_grav = (-6 * a * sp.diff(a, t) ** 2 / N - 2 * Lam * N * a ** 3) / (4 * K)
L_K = N * a ** 3 * mu ** 2 * (Q - 1) ** 2 / (2 * K)
L_m = -N * rb0
L_GB = gam * tau * sp.diff(CS, t)          # sqrt(-g) gamma tau G_GB, exact
L_GBp = -gam * sp.diff(tau, t) * CS        # same up to a total derivative
print("L_GB - L_GBp is a total derivative:", sp.simplify(L_GB - L_GBp - sp.diff(gam * tau * CS, t)) == 0)
L = L_grav + L_K + L_m + L_GB
EL_tau = sp.simplify(sp.diff(sp.diff(L, sp.diff(tau, t)), t) - sp.diff(L, tau))
n_expr = mu ** 2 * (Q - 1) / K
print("tau equation: d/dt[a^3 n] - gamma sqrt(-g) G_GB =",
      sp.simplify(EL_tau - (sp.diff(a ** 3 * n_expr, t) - gam * sp.diff(CS, t))))
print("  => d/dt[ a^3 n - 8 gamma adot^3/N^3 ] = 0 exactly: a^3 n = C + 8 gamma (a H)^3 (N = 1)")
print("  covariant: nabla_m J^m = gamma G_GB with J^m = n n^m (P = 0); KA3: gamma = 0 gives a^3 mu^2 (Q-1)/K = C")
p_tau = sp.simplify(sp.diff(L_grav + L_K + L_m + L_GBp, sp.diff(tau, t)))
print("  Noether momentum (by-parts form):", p_tau)

print("\n=== Friedmann constraint with the term ===")
L2 = L_grav + L_K + L_m + L_GBp
Ham = sp.diff(L2, N)
qq = sp.symbols('q')
HamN1 = sp.simplify(Ham.subs(sp.diff(tau, t), qq * N).subs(N, 1))
HamH = sp.expand(sp.simplify(HamN1.subs(sp.diff(a, t), H * a) / a ** 3))
print("dL/dN / a^3 (N=1, tau_dot=q):", HamH)
print("  => 3H^2/(2K) = rho_b + Lambda/(2K) + mu^2 (q^2-1)/(2K) - 24 gamma q H^3")
print("  with n = C/a^3 + 8 gamma H^3 and q ~ 1: rho_K + rho_GB ~ C/a^3 + 8 gamma H^3 - 24 gamma H^3 = C/a^3 - 16 gamma H^3")

print("\n=== KA4: Chamseddine-Mukhanov integral (PROVISIONAL source) ===")
HI, af, beta = sp.symbols('H_I a_f beta', positive=True)
aa = af * sp.exp(HI * (t))
integrand = sp.diff(aa, t) * sp.diff(sp.diff(aa, t) ** 2 * beta * 27 * HI ** 3, t)
I = sp.simplify(sp.integrate(integrand, (t, -sp.oo, 0)))
print("int adot d/dt(adot^2 beta 27 H^3) dt over de Sitter up to a_f:", I, " (paper: 18 beta H_I^6 a_f^3)")
integrand1 = sp.diff(aa, t) * sp.diff(sp.diff(aa, t) ** 2 * beta, t)
print("same with g = 1 (the plain linear term):", sp.simplify(sp.integrate(integrand1, (t, -sp.oo, 0))),
      " = (2/3) beta adot^3: tracks adot^3, i.e. reversible")
print("generic a(t): int adot d/dt(adot^2) dt = (2/3) adot^3 identically:",
      sp.simplify(sp.diff(sp.Rational(2, 3) * sp.diff(a, t) ** 3, t) - sp.diff(a, t) * sp.diff(sp.diff(a, t) ** 2, t)) == 0)

print("\n=== MU1a: replace G_GB by R^2 (not a total derivative) ===")
R1 = sp.simplify(Rs.subs(N, 1).doit())
src = sp.simplify(a ** 3 * R1 ** 2)
test = sp.simplify(src - sp.diff(8 * sp.diff(a, t) ** 3, t))
print("a^3 R^2 - 8 d/dt(adot^3) =", sp.factor(test), " (nonzero: R^2 source does not track adot^3)")
RH = sp.simplify(R1.subs(add, (Hd + H ** 2) * a).subs(ad, H * a))
print("R in H, Hdot:", sp.factor(RH), "; in radiation era:", sp.simplify(RH.subs(Hd, -2 * H ** 2)),
      "-> R^2 source vanishes in radiation, so a charge made in inflation by an R^2 coupling would survive")
