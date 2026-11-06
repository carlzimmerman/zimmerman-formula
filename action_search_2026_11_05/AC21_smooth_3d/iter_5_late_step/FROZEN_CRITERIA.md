# AC21 iter_5 frozen criteria: structural blend with a late step (after iter_4's sign pattern)

Frozen after iter_4 ran and before any iter_5 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Why

In iter_4 all 15 (tau, n) pairs solved, and every one had A > 0 with B < 0, or A < 0 with B > 0. That NO-GO
stands for the iter_4 family.

The reason, read after the run, is this. Write h = f - q^2/2 on [0, 1]. Then h'' has zero mass and zero first
moment. Near 0, h'' is about -1 on [0, tau]. So the positive part of h'' must sit at the mean of the negative part,
and that mean is at most tau unless f'' also drops below 1 somewhere to the right.

iter_4's step S(x) reaches 1 too early, so there is no negative region on the right. This iteration starts the
step late at x0, which opens that region. Nothing else changes.

## Family

On [tau, 1], with x = (q - tau)/(1 - tau) and y = max(x - x0, 0)/(1 - x0):

    f'' = A q^4 (1 - S(x)) + B x^5 (1 - x)^n + S(y)

where S is iter_4's C^4 smoothstep. f'' = A q^4 on (0, tau] and f'' = 1 for q >= 1.

- C^4 at both knots holds by construction: S(y) = 0 near x = 0, and S(y) -> 1 with flat derivatives at x = 1.
- A and B come from the two moments, f'(1) = 1 and f(1) = 1/2, solved exactly in rationals.
- f'' > 0 on (0, 1] if A > 0 and B >= 0, since every term is >= 0.
- Search order, fixed now: tau = 1/2, 1/3, 1/4 (outer); x0 = 1/2, 2/3, 4/5 (middle); n = 5, 10 (inner).
  The first triple with A > 0 and B >= 0 wins.

## Checks and labels

The checks are iter_4's, unchanged: T4'' exact, plus T5, T6 and T7.

- EXISTS if a triple qualifies. Then iter_2's numerics use this winner: rows b = 0.4 and 0.8, with the statistic,
  lines and controls frozen in ../FROZEN_CRITERIA.md.
- NO-GO for this family if no triple qualifies. The 3D label then stays FAIL as frozen, and the README says so.
