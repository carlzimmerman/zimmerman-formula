#!/usr/bin/env python3
"""p01_exact_reductions.py -- what is exactly true about  A * Lambda = 32 pi^2  with  A = pi/a0^2  (c = G = 1).

Everything here is computed, not assumed: the Euler (Gauss-Bonnet) density E4 = Riem^2 - 4 Ric^2 + R^2 is obtained from the
Riemann tensor of each metric (sympy), then integrated.  Checks:
  R1  the algebra: AL = 32 pi^2  <=>  Lambda = 32 pi a0^2  <=>  a0 = (1/2) sqrt(rho_Lambda)  <=>  rho_Lambda r_s^2 = 1  <=>  K_Sigma = rho_Lambda
  R2  32 pi^2 = (8 pi)(4 pi) = 2 (4 pi)^2 = 12 Vol(S^4_unit) = the unit-S^4 Einstein-Hilbert integral
  G1  Euclidean de Sitter S^4(L): E4 = 24/L^4, integral 64 pi^2 = 32 pi^2 chi (chi = 2), for EVERY L
  G2  Euclidean Schwarzschild: E4 = 48 M^2/r^6, integral 64 pi^2 for EVERY M  (chi = 2)
  G3  Euclidean Nariai S^2 x S^2: E4 = 8 Lambda^2, integral 128 pi^2 = 32 pi^2 * 4
  G4  product formula E4(S^2 x S^2) = 2 R1 R2, which is where 32 pi^2 = 2 (4 pi)^2 comes from
  S1  the static-slice Euler charge  Q = int E4 dV3  equals 32 pi kappa for BOTH Schwarzschild (8 pi/M) and de Sitter (32 pi/L)
  S2  on-shell Einstein-Hilbert: S_dS = (1/32 pi) int R dV over S^4(L) = pi L^2
  M1  Milgrom's a0 = cH/2pi would give A*Lambda = 12 pi^3, not 32 pi^2
Exit 0 = all checks (and the controls) behave.
"""
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

pi = sp.pi
# ------------------------------------------------------------------ R1  algebra
a0, Lam, rho, rs, KS = sp.symbols('a0 Lambda rho r_s K_Sigma', positive=True)
A = pi / a0**2
print("\nR1  the equivalent forms of the puzzle's relation")
rel = sp.Eq(A * Lam, 32 * pi**2)
sol_Lam = sp.solve(rel, Lam)[0]
check("AL = 32 pi^2  <=>  Lambda = 32 pi a0^2", sp.simplify(sol_Lam - 32 * pi * a0**2) == 0)
rho_L = Lam / (8 * pi)                                  # G = 1
check("Lambda = 32 pi a0^2  <=>  a0 = (1/2) sqrt(rho_Lambda), rho_Lambda = Lambda/8pi",
      sp.simplify((sp.sqrt(rho_L) / 2).subs(Lam, 32 * pi * a0**2) - a0) == 0)
rs_expr = 1 / (2 * a0)                                  # Schwarzschild: kappa = 1/(4M) = a0, r_s = 2M = 1/(2 a0)
check("Schwarzschild with kappa = a0: r_s = 1/(2 a0), A = 4 pi r_s^2 = pi/a0^2", sp.simplify(4 * pi * rs_expr**2 - A) == 0)
check("Lambda = 32 pi a0^2  <=>  rho_Lambda r_s^2 = 1  (a dimensionless O(1) relation)", sp.simplify(rho_L.subs(Lam, 32 * pi * a0**2) * rs_expr**2 - 1) == 0)
check("... <=>  K_Sigma = rho_Lambda, K_Sigma = 1/r_s^2 the Gauss curvature of the horizon 2-sphere", sp.simplify(1 / rs_expr**2 - rho_L.subs(Lam, 32 * pi * a0**2)) == 0)
Lds = sp.symbols('L', positive=True)
Z = sp.sqrt(32 * pi / 3)
check("Rindler length 1/a0 = Z L with L = sqrt(3/Lambda), Z = sqrt(32 pi/3)", sp.simplify((1 / a0).subs(a0, sp.sqrt(Lam / (32 * pi))).subs(Lam, 3 / Lds**2) / Lds - Z) == 0)

# ------------------------------------------------------------------ R2
print("\nR2  where the number 32 pi^2 comes from")
check("32 pi^2 = (8 pi)(4 pi) = 2 (4 pi)^2", sp.simplify(32 * pi**2 - 8 * pi * 4 * pi) == 0 and sp.simplify(32 * pi**2 - 2 * (4 * pi)**2) == 0)
volS4 = 8 * pi**2 / 3
check("32 pi^2 = 12 Vol(S^4_unit) = int_{S^4(1)} R dV  (R = 12)", sp.simplify(32 * pi**2 - 12 * volS4) == 0)

# ------------------------------------------------------------------ curvature machinery
def christoffel(g, x):
    ginv = g.inv(); n = len(x)
    return [[[sum(ginv[i, l] * (sp.diff(g[l, j], x[k]) + sp.diff(g[l, k], x[j]) - sp.diff(g[j, k], x[l])) for l in range(n)) / 2
              for k in range(n)] for j in range(n)] for i in range(n)]

def riemann(g, x):
    n = len(x); G = christoffel(g, x)
    R = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    R[i][j][k][l] = sp.simplify(sp.diff(G[i][j][l], x[k]) - sp.diff(G[i][j][k], x[l])
                                                + sum(G[i][k][m] * G[m][j][l] - G[i][l][m] * G[m][j][k] for m in range(n)))
    return R

def euler_density(g, x):
    n = len(x); ginv = g.inv(); R = riemann(g, x)
    Ric = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(R[i][j][i][l] for i in range(n))))
    Rs = sp.simplify(sum(ginv[j, l] * Ric[j, l] for j in range(n) for l in range(n)))
    # all-lower Riemann, then contractions with a diagonal inverse metric
    Rl = [[[[sum(g[i, m] * R[m][j][k][l] for m in range(n)) for l in range(n)] for k in range(n)] for j in range(n)] for i in range(n)]
    riem2 = sp.simplify(sum(ginv[i, i] * ginv[j, j] * ginv[k, k] * ginv[l, l] * Rl[i][j][k][l]**2
                            for i in range(n) for j in range(n) for k in range(n) for l in range(n)))
    ric2 = sp.simplify(sum(ginv[i, i] * ginv[j, j] * Ric[i, j]**2 for i in range(n) for j in range(n)))
    return sp.simplify(riem2 - 4 * ric2 + Rs**2), Rs

t, r, th, ph = sp.symbols('tau r theta phi', real=True)
L, M, Lm = sp.symbols('L M Lambda_', positive=True)
xs = [t, r, th, ph]

# ------------------------------------------------------------------ G1  Euclidean de Sitter
print("\nG1  Euclidean de Sitter (static form of S^4(L))")
f = 1 - r**2 / L**2
g = sp.diag(f, 1 / f, r**2, r**2 * sp.sin(th)**2)
E4_dS, R_dS = euler_density(g, xs)
check("E4 = 24/L^4 and R = 12/L^2", sp.simplify(E4_dS - 24 / L**4) == 0 and sp.simplify(R_dS - 12 / L**2) == 0)
I_dS = sp.integrate(E4_dS * r**2 * sp.sin(th), (ph, 0, 2 * pi), (th, 0, pi), (r, 0, L), (t, 0, 2 * pi * L))
check("int E4 = 64 pi^2 = 32 pi^2 * chi(S^4), independent of L", sp.simplify(I_dS - 64 * pi**2) == 0)
Q_dS = sp.integrate(E4_dS * r**2 * sp.sin(th), (ph, 0, 2 * pi), (th, 0, pi), (r, 0, L))
check("static-slice Euler charge Q_dS = int E4 dV3 = 32 pi / L = 32 pi kappa_dS  (kappa_dS = 1/L)", sp.simplify(Q_dS - 32 * pi / L) == 0)

# ------------------------------------------------------------------ G2  Euclidean Schwarzschild
print("\nG2  Euclidean Schwarzschild")
f = 1 - 2 * M / r
g = sp.diag(f, 1 / f, r**2, r**2 * sp.sin(th)**2)
E4_S, R_S = euler_density(g, xs)
check("E4 = 48 M^2/r^6 (Ricci flat)", sp.simplify(E4_S - 48 * M**2 / r**6) == 0 and sp.simplify(R_S) == 0)
Q_S = sp.integrate(E4_S * r**2 * sp.sin(th), (ph, 0, 2 * pi), (th, 0, pi), (r, 2 * M, sp.oo))
kap = 1 / (4 * M)
check("static-slice Euler charge Q_S = 8 pi/M = 32 pi kappa  (kappa = 1/(4M))", sp.simplify(Q_S - 8 * pi / M) == 0 and sp.simplify(Q_S - 32 * pi * kap) == 0)
I_S = sp.simplify(Q_S * (2 * pi / kap))
check("int E4 = beta Q = 64 pi^2 = 32 pi^2 * chi(R^2 x S^2), independent of M", sp.simplify(I_S - 64 * pi**2) == 0)

# ------------------------------------------------------------------ G3, G4
print("\nG3/G4  S^2 x S^2 (Euclidean Nariai) and the product formula")
c = sp.symbols('c', positive=True)
g = sp.diag(1 / c, sp.sin(th)**2 / c, 1 / c, sp.sin(r)**2 / c)         # coordinates (th1, ph1, th2, ph2): S^2 x S^2 of Gauss curvature c
th1, ph1, th2, ph2 = sp.symbols('th1 ph1 th2 ph2', real=True)
g = sp.diag(1 / c, sp.sin(th1)**2 / c, 1 / c, sp.sin(th2)**2 / c)
E4_N, R_N = euler_density(g, [th1, ph1, th2, ph2])
check("E4(S^2 x S^2) = 2 R1 R2 = 8 c^2  with R1 = R2 = 2c", sp.simplify(E4_N - 2 * (2 * c) * (2 * c)) == 0)
I_N = sp.integrate(E4_N * sp.sin(th1) * sp.sin(th2) / c**2, (ph1, 0, 2 * pi), (th1, 0, pi), (ph2, 0, 2 * pi), (th2, 0, pi))
check("int E4 = 128 pi^2 = 32 pi^2 * chi(S^2 x S^2), chi = 4, independent of c", sp.simplify(I_N - 128 * pi**2) == 0)
check("two unit-S^2 integrals: 2 (int R)(int R)/... : int_{S^2} R dA = 8 pi so 2 (4 pi)(4 pi) = 32 pi^2 per unit Euler number", sp.simplify(2 * (4 * pi)**2 - 32 * pi**2) == 0)

# ------------------------------------------------------------------ S2  on-shell EH
print("\nS2  on-shell Einstein-Hilbert action of S^4(L) and the 32 pi")
Lamdef = 3 / L**2
Vol = sp.simplify(sp.integrate(r**2 * sp.sin(th), (ph, 0, 2 * pi), (th, 0, pi), (r, 0, L), (t, 0, 2 * pi * L)))
check("Vol(S^4(L)) = (8 pi^2/3) L^4", sp.simplify(Vol - 8 * pi**2 * L**4 / 3) == 0)
IEH = -(1 / (16 * pi)) * (R_dS - 2 * Lamdef) * Vol
check("I_E = -(1/16pi) int (R - 2 Lambda) = -pi L^2 = -S_dS = -3 pi/Lambda", sp.simplify(IEH + pi * L**2) == 0)
check("S_dS = (1/(32 pi)) int_{S^4} R dV : the 32 pi is 16 pi x 2 from the on-shell Lambda term", sp.simplify(R_dS * Vol / (32 * pi) - pi * L**2) == 0)

# ------------------------------------------------------------------ M1  Milgrom
print("\nM1  the Unruh-2pi version")
a0M = sp.sqrt(Lam / 3) / (2 * pi)
check("Milgrom a0 = cH/2pi gives Lambda = 12 pi^2 a0^2 and A Lambda = 12 pi^3 (an extra pi from the thermal period)",
      sp.simplify(sp.solve(sp.Eq(a0, a0M), Lam)[0] - 12 * pi**2 * a0**2) == 0 and sp.simplify((pi / a0**2) * 12 * pi**2 * a0**2 - 12 * pi**3) == 0)

# ------------------------------------------------------------------ controls
print("\nControls (must be caught)")
check("C1  a wrong Gauss-Bonnet constant 30 pi^2 is rejected", sp.simplify(I_dS - 30 * pi**2 * 2) != 0)
check("C2  a wrong charge 16 pi kappa is rejected for Schwarzschild", sp.simplify(Q_S - 16 * pi * kap) != 0)
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
