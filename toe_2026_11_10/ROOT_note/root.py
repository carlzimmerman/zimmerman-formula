#!/usr/bin/env python3
"""ROOT note: one cause for TOE0's T2 and T3 failures, for every MOND interpolating function, not only (A)'s.

Khronometric form (QX17 (A), HZ1): GR + (a0^2/K) J(u), u = |A|/a0, gives the static law mu(x) = 1 - J'(x)/x
(HZ1 KA3 for J = u - ln(1+u)). Deep MOND (v^4 = G M a0) needs mu(x) = x + O(x^2) as x -> 0.
Claim: then J = u^2/2 - u^3/3 + O(u^4) for ANY such mu, so
  (1) alpha(0) = 4 J''(0)/2 = 2: the khronon scalar speed^2 (beta+lambda)(2-alpha)/[...] is 0 for every beta, lambda;
  (2) the next term is -|A|^3/3: odd in |A| = (A.A)^(1/2), so not a polynomial in A_i.
A note, not a graded lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import sympy as sp

x, u = sp.symbols("x u", positive=True)
al, be, la = sp.symbols("alpha beta lambda", real=True)
out = []


def say(s):
    out.append(s)
    print(s)


# KA: (A)'s own J gives the simple mu
J_A = u - sp.log(1 + u)
mu_A = sp.simplify(1 - sp.diff(J_A, u).subs(u, x) / x)
say(f"KA  J = u - ln(1+u) -> mu = {mu_A}   (simple mu: {sp.simplify(mu_A - x/(1+x)) == 0})")

# General: J analytic in u near 0 up to order 5 with free coefficients; impose mu(x) = x + m2 x^2 + m3 x^3 + ...
c = sp.symbols("c0:6")
m2, m3 = sp.symbols("m2 m3")
J = sum(c[n] * u**n for n in range(6))
mu = sp.expand(1 - sp.diff(J, u).subs(u, x) / x)
target = x + m2 * x**2 + m3 * x**3
eqs = [sp.Eq(sp.expand(mu * x).coeff(x, k), sp.expand(target * x).coeff(x, k)) for k in range(0, 5)]
sol = sp.solve(eqs, [c[1], c[2], c[3], c[4], c[5]], dict=True)[0]
say(f"any mu = x + m2 x^2 + m3 x^3 + ...  forces  c1 = {sol[c[1]]}, c2 = {sol[c[2]]}, c3 = {sol[c[3]]}, "
    f"c4 = {sol[c[4]]}, c5 = {sol[c[5]]}")
alpha0 = 4 * sol[c[2]]          # HZ1: alpha(u) = 4 J(u)/u^2 -> 4 c2 at u = 0
say(f"(1) alpha(0) = 4 c2 = {alpha0}  (independent of m2, m3: {alpha0.free_symbols == set()})")
cs2 = (be + la) * (2 - al) / (al * (1 - be) * (2 + be + 3 * la))
say(f"    BPS khronon speed^2 at alpha = alpha(0): {sp.simplify(cs2.subs(al, alpha0))}  for all beta, lambda")
say(f"    Newtonian G_N/G = 1/(1 - alpha/2) at alpha(0): {sp.limit(1/(1 - al/2), al, alpha0, '-')} (from below)")
say(f"(2) cubic coefficient c3 = {sol[c[3]]} (nonzero for every m2): the term c3 |A|^3/a0 = c3 (A.A)^(3/2)/a0")
a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
cubic = (a1**2 + a2**2 + a3**2) ** sp.Rational(3, 2)
say(f"    (A.A)^(3/2) polynomial in A_i: {cubic.is_polynomial(a1, a2, a3)}")
# MUTATE: a non-MOND mu with mu(0) = 1/2 (no deep regime) does not force alpha(0) = 2
mu_bad = sp.Rational(1, 2) + x / 2
eqs_b = [sp.Eq(sp.expand(mu * x).coeff(x, k), sp.expand(mu_bad * x).coeff(x, k)) for k in range(0, 5)]
sol_b = sp.solve(eqs_b, [c[1], c[2], c[3], c[4], c[5]], dict=True)[0]
say(f"MUTATE mu(0) = 1/2 (not MOND): c2 = {sol_b[c[2]]}, alpha(0) = {4*sol_b[c[2]]}, c3 = {sol_b[c[3]]}: "
    f"{'bites (alpha != 2)' if 4*sol_b[c[2]] != 2 else 'does NOT bite'}")

open(__file__.replace("root.py", "root.out"), "w").write("\n".join(out) + "\n")
