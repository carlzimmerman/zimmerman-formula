# T2 -- is `alpha^-1 + a1*alpha + a2*alpha^2 = c` with (a1, a2) = (1, -12 pi) a genuine QED loop series? (pre-registration)

Written 2026-09-29 BEFORE `t2_series_class.py` was run. The question came from the user: why was the 'two-loop thing' (alpha^-1 + alpha - 12 pi alpha^2 = 4 Z^2 + 3) so close?
The existing audit (real_research/reviews/alpha_12pi_identity_audit_2026.py, Lean AH8) established that its 1.8e-8 closeness is a 0.12% coefficient match magnified ~70,000x. This lane asks the
structural question that audit did not: does the identity have the SHAPE of a loop expansion, i.e. are its coefficients in the class real QED produces?

## The class (declared)
In QED every order-n coefficient of a series in alpha has the form (1/pi)^n x (an element of the Q-span of {1, zeta(3), pi^2, pi^2 ln 2, ln-of-mass-ratio terms, ...}); the first-order coefficient is rational/pi; the second-order one is
(rational + rational*zeta(3) + rational*pi^2 + rational*pi^2 ln 2)/pi^2. Checked against three published closed forms (recalled, and checked against their published decimals): the electron g-2 coefficients
A1 = 1/2 and A2 = 197/144 + pi^2/12 - (pi^2/2) ln 2 + (3/4) zeta(3) = -0.3284789655791938... (in units of (alpha/pi)^n), and the QED beta function beta(alpha) = (2 alpha^2/(3 pi)) [1 + (3/4)(alpha/pi) + ...].

## Declared tests and criteria
* T-A (class): with high-precision integer-relation search (PSLQ, 100 digits, coefficient bound 10^6), decide whether a1 = 1 equals r1/pi for a rational r1 (i.e. whether pi is rational: expected NO) and whether a2 = -12 pi lies in the class
  {(r + s zeta(3) + t pi^2 + u pi^2 ln 2)/pi^2} (expected NO: it would require pi^3 to be in the Q-span of {1, zeta(3), pi^2, pi^2 ln 2}). Report 'no relation found up to the bound' (not a proof).
* T-B (freedom): enumerate class-restricted series alpha^-1 + (r1/pi) alpha + (r2/pi^2) alpha^2 = 4 Z^2 + 3 with r1, r2 small rationals (numerator <= 64 and <= 4096, denominator <= 12) and count how many land within
  1e-8 and within 5e-10 of the residual; report the expected chance count from the density. This shows how much freedom two rational slots have.
* T-C (control): the same enumerations applied to a RANDOM target residual of the same size must give comparable hit counts (if it does, a hit means nothing).
* MUTATE control: replacing pi in the class test by a rational must make T-A report a relation (the control must fail T-A's 'no relation' expectation).
* Expected (declared before running): T-A: no relation, so the identity's coefficients are NOT in the QED class (it is not a QED loop series); T-B: a few class-restricted rational pairs hit within 1e-8 by chance; T-C: comparable counts for random targets.

## Reading rules
This tests the SHAPE of the series only. It does not test whether alpha^-1 = 4 Z^2 + 3 at some scale; it is silent on that. alpha stays an INPUT; kappa = 1/2 FITTED.
