# interp_0037 -- the golden-Koide-Yukawa shared number X

Seed 0037 is a random collision. Read charitably, all three bullets point at ONE
dimensionless number X that is the "shadow" binding them:

  * bullet 1 (geometry): the golden-ratio point of the a0-bump cluster response
    R (peaked at a0) sits at normalized value 1/phi ~= 0.618 (the golden section of
    the bump), and its shadow is the top Yukawa y_t ~= 0.70.
  * bullet 2 (renorm): an entropy partition of the Koide ratio Q = 2/3 ~= 0.667
    renormalizes onto the a0-line g^2 - g_b^2 = a0 * g_b.
  * wildcard: the single number both bullets share, if true, is X.

## Hypothesis (one sentence)
The three candidates collapse to one number X ~= 0.618-0.70 that is simultaneously
(a) the golden-section value of the a0-bump response, (b) the top Yukawa y_t, and
(c) the Koide 2/3 entropy-partition value that lands on the a0-line; i.e. X ~= 1/phi
~= 2/3 ~= y_t within the kappa-scale tolerance, and that X satisfies
g^2 - g_b^2 = a0*g_b.

## Exact quantities
- X_geo  = R(a*/a0) / R_peak  read at the golden section  (a*/a0 = 1/phi); target ~= 0.618.
- y_t    = top-quark Yukawa, quoted ~0.70 (note ambiguity: y_t at a high scale vs y_t^2;
           test uses the seed's 0.70, flag the convention in the ref report).
- Q      = 2/3 = 0.66667 (Koide ideal ratio).
- a0-line: g^2 - g_b^2 = a0 * g_b, solved for the X-point (dimensional step uses BOTH
           footings a0 = 9.3619e-11 and a0 = 1.1279e-10 m/s^2).

## Exact test
1. X_geo: build the a0-bump response R (the cluster-response peaked at a0), take its
   value at the golden section. Falsifiable number in [0,1].
2. Collapse check: |X_geo - 1/phi|, |X_geo - 2/3|, |X_geo - y_t| each < tol,
   with tol = 0.043 (the kappa fit uncertainty 0.551 +/- 0.043).
3. a0-line check: at the X-point the identity g^2 - g_b^2 = a0*g_b holds on BOTH
   footings; if it holds on only one footing, record NULL (footing-sensitive, not dead).

## Kill conditions (any one => REFUTED / DISCARD)
- The three candidates do NOT collapse to a single X within tol = 0.043
  (i.e. they stay separated at 0.618 / 0.667 / 0.70 with no common X).
- No single X satisfies g^2 - g_b^2 = a0*g_b on both footings.
- y_t convention resolves to ~0.93 (m_Z value), not ~0.70, killing bullet 1's target.
- X equals a pure CONVENTION match (unit/normalization artifact): CONVENTION is not a hit.

## What it is NOT
This is a hypothesis, not a derivation. X ~= 2/3 is NOT claimed derived; if the numbers
collapse it is a coincidence to be chased, not a proof. Do not count kappa = 1/2 here.
