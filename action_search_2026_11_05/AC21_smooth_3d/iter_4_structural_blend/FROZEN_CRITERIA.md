# AC21 iter_4 frozen criteria: a structurally positive blend (after iter_3's LP family failed)

Frozen after iter_3 ran and before any iter_4 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Why

- iter_3's LP polynomial family, with D up to 20, certified no member. The best minimum Bernstein coefficient was
  -1.28, at tau = 1/3 and D = 20. It improved with D and with smaller tau, but the frozen search stopped at D = 20.
  That NO-GO stands for the iter_3 family.
- The obstruction is soft. f'' / 1 must be a unit-mass density on [0, 1] with mean exactly 1/2, equal to 1 at q = 1,
  and suppressed as A q^4 near 0. That forces compensating mass just right of tau. Polynomials with positive
  Bernstein coefficients need very high degree to place it.
- This iteration builds f'' as a sum of terms that are nonnegative by construction, so positivity needs no
  certificate beyond the signs of two scalars.

## Family

- **Pieces.** x = (q - tau)/(1 - tau) on the layer. S(x) is the C^4 smoothstep,
  x^5 (126 - 420 x + 540 x^2 - 315 x^3 + 70 x^4), which is monotone from 0 to 1.
  - f'' = A q^4 for 0 < q <= tau.
  - f'' = A q^4 (1 - S(x)) + S(x) + B x^5 (1 - x)^n for tau <= q <= 1.
  - f'' = 1 for q >= 1.
  - F = gamma b^2 f(q), so F = (gamma/2) Pi^2 exactly for Pi >= b.
- **C^4 at both knots is automatic.** S - 0 vanishes to order 5 at x = 0, and 1 - S vanishes to order 5 at x = 1.
  The bump vanishes to order 5 at x = 0 and to order n >= 5 at x = 1.
- **Unknowns.** A and B, from the two linear moment equations f'(1) = 1 and f(1) = 1/2.
- **Positivity.** If A > 0 and B >= 0, then f'' > 0 on (0, 1] (each term is >= 0 and S > 0 for x > 0).
  Lean certifies this structurally.
- **Search order, fixed now.** tau = 1/2, 1/3, 1/4 (outer), then n = 5, 10, 15, 20, 30 (inner). The first pair
  with A > 0 and B >= 0, solved exactly in rationals, wins.

## Checks and labels

- **T4''.** Exact rational A > 0 and B >= 0. Re-verify C^4 matching at both knots and both moments exactly
  with sympy.
- **T5, T6, T7.** As in iter_3: the statics bounds, max |f' - q| <= 1, AC2q FRW exact, and F' >= 0 with
  F'' > 0 on the layer.
- **Labels.**
  - If T4'' passes: 3D-admissible smoothing EXISTS (v3s with b = rho_DE, AC2q with b = X). The 3D PASS label
    then waits on iter_2's numerics on this form: rows b = 0.4 and 0.8, with the statistic, lines and controls
    frozen in ../FROZEN_CRITERIA.md.
  - If no pair qualifies: NO-GO for this family too, and the 3D label stays FAIL as frozen.
- **iter_2 amendment, before any iter_2 number.** "The T4 form" in iter_2 means the iter_4 winner. iter_1 and
  iter_3 produced no form.
