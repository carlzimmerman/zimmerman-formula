#!/usr/bin/env python3
"""FINAL-10 (LEAN-STRESS): verify whether 2(u - log(1+u)) = u^2/(1+u) holds
on the deep-law branch u^2 = x^2 (1+u).

If it fails (expected), report the honest residual
    R(x) = 2(u - log(1+u)) - u^2/(1+u)
and the true ratio Pi_rr/Pi_tt.
"""
import mpmath
import sympy as sp

x, u, s, t = sp.symbols('x u s t', positive=True)

# ---------------- 1. The claimed identity on the branch ---------------------
# u(x) = positive root of u^2 - x^2 (1+u) = 0
usol = sp.solve(sp.Eq(u**2, x**2 * (1 + u)), u)
print("roots of u^2 = x^2 (1+u):", usol)
u_of_x = sp.simplify(max(usol, key=lambda r: sp.limit(r, x, sp.oo)))  # growing root
# explicitly the positive root
u_of_x = (x**2 + sp.sqrt(x**4 + 4 * x**2)) / 2
# verify it satisfies the branch equation
branch_check = sp.simplify(u_of_x**2 - x**2 * (1 + u_of_x))
print("u(x) =", u_of_x)
print("branch residual u^2 - x^2(1+u) =", branch_check)

# claimed identity LHS - RHS
claim = 2 * (u - sp.log(1 + u)) - u**2 / (1 + u)
print("\nclaim LHS-RHS as function of u:", sp.simplify(claim))

# Series about u=0 -> shows it fails at cubic order
print("series of claim about u=0:", sp.series(claim, u, 0, 6))

# exact: u^2/(1+u) = x^2 on the branch, so R(x) = 2(u-log(1+u)) - x^2
R_of_x = sp.simplify(2 * (u_of_x - sp.log(1 + u_of_x)) - x**2)
print("\nR(x) = 2(u-log(1+u)) - x^2 =", R_of_x)
print("series small x:", sp.series(R_of_x, x, 0, 8))
print("series large x (x->oo):", sp.series(R_of_x.subs(x, 1 / t), t, 0, 2))

# closed form via s = log(1+u): R = 2(sinh s - s)
R_sinh = sp.simplify(2 * (sp.exp(s) - 1 - s) - (sp.exp(s) - 1) ** 2 / sp.exp(s))
print("\nR in terms of s=log(1+u):", sp.simplify(R_sinh),
      " == 2(sinh s - s)?", sp.simplify(R_sinh - 2 * (sp.sinh(s) - s)) == 0)
print("d/ds of 2(sinh s - s):", sp.simplify(sp.diff(2 * (sp.sinh(s) - s), s)))

# ---------------- 2. Numbers over x in [0.1, 100] ---------------------------
print("\n%-8s %-14s %-14s %-14s %-14s %-14s" %
      ("x", "u(x)", "2(u-ln(1+u))", "u^2/(1+u)=x^2", "R(x)", "Pi_rr/Pi_tt"))
print("-" * 84)
grid = [0.1, 0.2, 0.5, 1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100]
f = sp.lambdify(x, R_of_x, 'mpmath')
gu = sp.lambdify(x, u_of_x, 'mpmath')
mpmath.mp.dps = 30
rows = []
for xv in grid:
    uv = mpmath.mpf(gu(xv))
    F = 2 * (uv - mpmath.log(1 + uv))           # 2(u - log(1+u))
    Q = uv**2 / (1 + uv)                        # = x^2 on branch
    R = F - Q
    ratio = 1 - Q / (F / 2)                     # Pi_rr/Pi_tt
    rows.append((xv, uv, F, Q, R, ratio))
    print("%-8s %-14.8g %-14.8g %-14.8g %-14.8g %-14.8g" %
          (xv, uv, F, Q, R, ratio))

print("\nsign of R over the grid:", "all > 0" if all(r[4] > 0 for r in rows)
      else "MIXED")
print("min R = %.6e at x = %s" % (min(r[4] for r in rows),
                                  min(rows, key=lambda r: r[4])[0]))
print("max R = %.6e at x = %s" % (max(r[4] for r in rows),
                                  max(rows, key=lambda r: r[4])[0]))

# ---------------- 3. Asymptotics confirmed by limit ------------------------
print("\nR/x^3 as x->0 :", sp.limit(R_of_x / x**3, x, 0))
print("R/x^2 as x->oo:", sp.limit(R_of_x / x**2, x, sp.oo))
print("R - (x^2 - 4 log x + 2) at large x:",
      sp.limit(sp.simplify(R_of_x - (x**2 - 4 * sp.log(x) + 2)), x, sp.oo))

# ratio asymptotics
ratio_expr = 1 - x**2 / (u_of_x - sp.log(1 + u_of_x))
print("\nPi_rr/Pi_tt at x->0   :", sp.simplify(sp.limit(ratio_expr, x, 0)))
print("Pi_rr/Pi_tt at x->oo  :", sp.limit(ratio_expr, x, sp.oo))
print("(Pi_rr/Pi_tt)*x^2/(2 log x) at x->oo:",
      sp.limit(ratio_expr * x**2 / (2 * sp.log(x)), x, sp.oo))

# ---------------- 4. Small-u isotropic limit --------------------------------
F_expr = u - sp.log(1 + u)
print("\nseries u - log(1+u):", sp.series(F_expr, u, 0, 6))
print("F(u) - u^2/2  ~ ", sp.series(F_expr - u**2 / 2, u, 0, 5))
# J = (a0^2/K) F ; g^2/(2K) = a0^2 u^2 /(2K)
print("=> J = g^2/(2K) - (a0^2/K) u^3/3 + ...  (deficit is O(u^3), negative)")
