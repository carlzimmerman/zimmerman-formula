# AC21 iter_6 frozen criteria: fast-decaying left piece (after iter_5's sign pattern)

Frozen after iter_5 ran and before any iter_6 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Why

iter_5 found no qualifying triple, and its NO-GO stands for the iter_5 family. All 18 triples again gave A and B of
opposite sign.

The cause, read after the run: f'' is a positive combination of three shapes,
- L = A q^4 (1 - S(x)),
- the bump B x^5 (1 - x)^n,
- the fixed late step S(y).

A positive (A, B) exists only if the target mean, (1/2 - M1_step)/(1 - m_step), lies between the means of L and of
the bump. In iters 4 and 5, L = A q^4 (1 - S(x)) decays over the whole layer. That puts its mean above the target,
so no positive pair can exist.

This iteration makes L decay within a short fraction x1 of the layer.

## Family

On [tau, 1], with x = (q - tau)/(1 - tau), z = min(x/x1, 1) and y = max(x - x0, 0)/(1 - x0):

    f'' = A q^4 (1 - S(z)) + B x^5 (1 - x)^n + S(y)

with iter_4's C^4 smoothstep S. As before, f'' = A q^4 on (0, tau] and f'' = 1 for q >= 1.

- C^4 holds at every knot (tau, the end of L's decay at x = x1, the step start at x0, and 1), because S is flat at
  both of its ends.
- A and B come from the two moments, solved exactly in rationals.
- Positivity: A > 0 and B >= 0 together give f'' > 0 on (0, 1].
- Search order, fixed now: tau = 1/2, 1/3; then x1 = 1/4, 1/8; then x0 = 1/2, 4/5; then n = 5, 10.
  The first quadruple with A > 0 and B >= 0 wins.

## Checks and labels

- The checks are iter_4/5's: exact C^4 at all knots, exact moments, positivity, T5, T6 and T7.
- EXISTS if a quadruple qualifies. Then iter_2's numerics use this winner, with rows b = 0.4 and 0.8 and the lines
  frozen in ../FROZEN_CRITERIA.md.
- NO-GO for this family otherwise.
- This is the last structural family this lane will try. If it fails, the README reports the smoothing as an
  unresolved construction (the class is nonempty, but none of the families tried here realizes it), and the 3D
  label stays FAIL as frozen.
