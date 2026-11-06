# AC21 iter_3 frozen criteria: a wider blend family for the 3D-admissible smoothing (after iter_1's T4 fail)

Frozen after iter_1 ran and before any iter_3 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Why

iter_1's T4 found no convex member in the declared family, which used the minimal-degree blends with
tau in {1/2, 1/3, 2/3} and C^4 / C^3 knots. Each of those blends is uniquely fixed by its matching conditions,
and each one dips negative. That failure stays on the record as iter_1's T4 label.

The class itself is not empty: f'' >= 0 on [0, 1] with unit mass, mean 1/2, f''(1) = 1 and q^4 vanishing at 0
is a nonempty convex set (for example, a bump left of 1/2 plus a sliver at 1). So the question is whether a
polynomial blend with free parameters can realize it, certified exactly.

## Family and rule

- **Form.** f'' = A q^4 on (0, tau], f'' = p(q) on [tau, 1] (degree D), and f'' = 1 on [1, inf). This is
  F = gamma b^2 f(q) with q = Pi / b, so F = (gamma / 2) Pi^2 exactly for Pi >= b.
- **Constraints.** Same as iter_1: C^4 matching at tau (to A q^4) and at 1 (to 1), f'(1) = 1, f(1) = 1/2.
- **Free directions.** For D > 10 there are D - 10 of them. Pick them by linear programming: maximize the minimum
  Bernstein coefficient of p on [tau, 1] (scipy linprog, highs), with every coordinate in [-1e6, 1e6].
- **Exact rounding.** Round the LP point to rationals (denominators <= 10^6). Re-solve the equality constraints
  exactly with sympy, using the rounded free coordinates.
- **Strict positivity.** It must be certified exactly: every Bernstein coefficient > 0, plus A > 0.
- **Search order, fixed now.** D = 12, 14, 16, 18, 20, then tau = 1/2 before tau = 1/3. The first certified
  member wins.

## Checks on the winner

- T4': all Bernstein coefficients > 0 and A > 0 (exact). The matching identities are certified in Lean
  (fable_independent_2026/lean_2026/AC21_smooth_3d.lean), and so is Bernstein positivity => f'' >= 0 on the layer.
- T5: iter_1's statics bounds, which depend only on b, plus max |f'(q) - q| <= 1 on [0, 1].
- T6: AC2q FRW exact, unchanged from iter_1, since the background sits at Pi = 2X > b = X.
- T7: F' >= 0 and F'' > 0 on the layer. This follows from f'' > 0 and f'(0) = 0, and the README states it with
  iter_1's general PN theorem.

## Labels (replace iter_1's T4 label only if a member is certified)

- 3D-admissible smoothing EXISTS (v3s with b = rho_DE, AC2q with b = X): T4', T5 and T6 pass.
- With iter_2's numerics on this form (rows b = 0.4 and 0.8, same statistic, lines and controls as frozen in
  ../FROZEN_CRITERIA.md), the label is **3D PASS (classical H^s local well-posedness across a transverse switch,
  d <= 3, PN charge-velocity system)** for v3s and AC2q.
- If no member is certified: NO-GO for this family too, and the label stays FAIL as frozen.

**iter_2 amendment, before any iter_2 number.** The rows "T4 form b = 0.4 / 0.8" mean the iter_3 winner. iter_1's
T4 form does not exist.
