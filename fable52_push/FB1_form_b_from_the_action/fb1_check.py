#!/usr/bin/env python3
"""FB1 check (a note's arithmetic, not a graded lane): the law sector's own stress holds its own charge, in any geometry.

Statement checked. For any static potential Phi (no symmetry assumed), with g = -grad Phi, u = |g| / a0,
  J(g)   = (a0^2 / K) [u - ln(1 + u)]                       (the law's Lagrangian after P is eliminated; K = 4 pi G)
  P      = -g / (K (1 + u))                                 (from A = K W'(K|P|) P_hat with the record's W)
  rho_Pi = -div[g / (1 + u)] / K  = div P                   (the polarization part of the clock charge)
  Pi_ij  = J delta_ij - g_i g_j / (K (1 + u))               (the canonical stress of J)
the identity   d_j Pi_ij = rho_Pi g_i   holds pointwise: the stress of the law sector balances the weight of its own charge.
Then Poisson with source rho_b + rho_Pi is the law's equation div[(u / (1 + u)) g] = -K rho_b.

Checks: (1) Legendre: W'(p) = p / (K (1 - p / a0)) gives K|P| = g / (1 + u), and J = P.A - W on that solution;
        (2) the identity at random points for three potentials with no symmetry (exact derivatives, 50-digit arithmetic);
        (3) spherical: with rho_c = rho_Pi the isotropic form dP/dr = -rho_c g integrates to P = J(g) for a point mass.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import sympy as sp, random, os
HERE = os.path.dirname(os.path.abspath(__file__)); LOG = open(os.path.join(HERE, "fb1_check.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n")
x, y, z, a0, K = sp.symbols("x y z a0 K", positive=True)
ok_all = True

# (1) Legendre pair
p, A = sp.symbols("p A", positive=True)
W = (a0 ** 2 / K) * (-p / a0 - sp.log(1 - p / a0))
sol = sp.solve(sp.Eq(K * sp.diff(W, p), A), p)
psol = sp.simplify(sol[0]); c1 = sp.simplify(psol - A / (1 + A / a0)) == 0
Jleg = sp.simplify((psol / K) * A - W.subs(p, psol)); Jdir = (a0 ** 2 / K) * (A / a0 - sp.log(1 + A / a0))
c1b = abs(sp.N((Jleg - Jdir).subs({A: sp.Rational(7, 3), a0: sp.Rational(11, 10), K: sp.Rational(13, 7)}), 40)) < 1e-30
P(f"(1) Legendre: K|P| = A / (1 + A / a0): {c1};  J = P.A - W equals (a0^2/K)[u - ln(1 + u)]: {c1b}"); ok_all &= bool(c1 and c1b)

# (2) the identity, no symmetry
X = (x, y, z)
pots = {"three unequal masses plus a tide": -1 / sp.sqrt((x - 1) ** 2 + y ** 2 + z ** 2 + sp.Rational(1, 50)) - sp.Rational(3, 5) / sp.sqrt(x ** 2 + (y + 2) ** 2 + (z - 1) ** 2 + sp.Rational(1, 30))
        - sp.Rational(2, 7) / sp.sqrt((x + 2) ** 2 + (y - 1) ** 2 + (z + 3) ** 2 + sp.Rational(1, 20)) + sp.Rational(1, 9) * (x ** 2 - z ** 2) + sp.Rational(1, 11) * x * y,
        "polynomial and trigonometric": sp.sin(x + 2 * y) * sp.cos(z / 2) + sp.Rational(1, 3) * x * y * z + sp.Rational(1, 5) * (x ** 2 + 2 * y ** 2 - z) ** 2 / 10,
        "exponential disc-like": -sp.exp(-sp.sqrt(x ** 2 + 2 * y ** 2 + sp.Rational(1, 10))) / (1 + z ** 2) + sp.Rational(1, 4) * sp.log(1 + x ** 2 + y ** 2 + 3 * z ** 2)}
random.seed(52)
for name, Phi in pots.items():
    g = [-sp.diff(Phi, v) for v in X]; gn = sp.sqrt(sum(c ** 2 for c in g)); u = gn / a0
    J = (a0 ** 2 / K) * (u - sp.log(1 + u))
    rhoPi = -sum(sp.diff(g[i] / (1 + u), X[i]) for i in range(3)) / K
    worst = 0
    for i in range(3):
        lhs = sum(sp.diff((J if i == j else 0) - g[i] * g[j] / (K * (1 + u)), X[j]) for j in range(3))
        res = lhs - rhoPi * g[i]; scale = rhoPi * g[i]
        for _ in range(6):
            pt = {x: sp.Rational(random.randint(-300, 300), 100), y: sp.Rational(random.randint(-300, 300), 100), z: sp.Rational(random.randint(-300, 300), 100),
                  a0: sp.Rational(random.randint(5, 400), 100), K: sp.Rational(random.randint(50, 900), 100)}
            r = abs(sp.N(res.subs(pt), 50)); s = abs(sp.N(scale.subs(pt), 50)) + sp.Float("1e-40")
            worst = max(worst, float(r / s))
    okk = worst < 1e-30
    P(f"(2) {name}: max |d_j Pi_ij - rho_Pi g_i| / |rho_Pi g_i| over 18 random points = {worst:.1e}  -> {'PASS' if okk else 'FAIL'}"); ok_all &= okk

# (3) spherical, point mass: g(r) from the law, rho_c = phantom, isotropic pressure
r, GM = sp.symbols("r GM", positive=True)
yv = GM / (a0 * r ** 2); gs = a0 * (yv / 2 + sp.sqrt(yv ** 2 / 4 + yv))            # g = g_N nu(g_N / a0), the law
Mt = gs * r ** 2                                                                  # G M_tot
rho_c = sp.diff(Mt, r) / (K * r ** 2)                                             # K rho = (1/r^2) d(G M)/dr with K = 4 pi G
Jg = (a0 ** 2 / K) * (gs / a0 - sp.log(1 + gs / a0))
res3 = sp.diff(Jg, r) + rho_c * gs
vals = [abs(sp.N(res3.subs({r: sp.Rational(k, 7), GM: sp.Rational(9, 4), a0: sp.Rational(3, 5), K: sp.Rational(11, 3)}), 40)) for k in (1, 5, 30, 400, 9000)]
c3 = max(vals) < 1e-30
P(f"(3) spherical point mass: d/dr J(g) = -rho_c g with rho_c the phantom density, at five radii: max residual {float(max(vals)):.1e}  -> {'PASS' if c3 else 'FAIL'}"); ok_all &= bool(c3)
P(f"\nall checks pass: {bool(ok_all)}")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
