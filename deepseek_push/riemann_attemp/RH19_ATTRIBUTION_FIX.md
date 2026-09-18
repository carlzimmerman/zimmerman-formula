# ATTRIBUTION CORRECTION -- 2026-09-17, deepseek lane (the honesty fix)

**Applies to RH16L/RH16, RH17, RH18.  Veredict of the referee review of
these lanes' framing: the mathematics is LEGIT (certified, measured,
zero fabrication) but the NOVELTY claims must be corrected to name the
classical sources.  Nothing in these lanes is new mathematics about the
zeta; what is new is (a) the Lean certificates as artifacts, (b) the
specific empirical numbers at these budgets, (c) the framing in the
framework's vocabulary.**

## The corrections (one line each)

- **RH16 / RH16L (the 'zeta's RAR' per-pair flip)**: the algebraic fact
  that the axis-excess of |xi|^2 per paired Hadamard factor
  E(u) = u^2(u^2+2w-2d^2) goes negative exactly when a zero leaves the
  critical line is the per-factor face of **Titchmarsh's monotonicity
  criterion** (RH  <->  |xi(sigma+it)| non-decreasing in sigma >= 1/2
  for all t; Titchmarsh, The Theory of the Riemann Zeta-Function,
  1930s/1951 chapter on the critical strip).  The Lean certificate is
  algebra, classically understood; the framework-RAR vocabulary is a
  presentation, not a discovery.

- **RH17 (the dark component |psi(x)-x| ~ sqrt-law)**: the identity
  psi(x) - x = - sum_rho x^rho/rho - ... and the bound
  |psi(x)-x| <= C sqrt(x) ln^2 x  <->  RH  is the classical explicit
  formula (von Mangoldt 1895; Titchmarsh ch. 3 & 12).  A measured alpha
  = 0.528 on a finite grid CONFIRMS the classical envelope on the
  sampled range; it does not add a new law.

- **RH18 (the S-function / Selberg RAR)**: the distribution of
  S(t) = (1/pi) Im log zeta(1/2+it) with variance ~ (1/2) ln ln t and
  the Gaussian limit is **Selberg's central limit theorem** (1942,
  published 1946).  The measured bounded envelope
  |S|_max/sqrt(ln t ln ln t) ~ 0.5-1.8 over t < 2000 is consistent
  with that classical theorem.  The deep-MOND vocabulary is a framing;
  the theorem is 80 years old.

## What stands as genuinely new (the narrow ledger)

  1. Lean-certified artifacts: the Lomax-ladder reflection
     M_l(s) = M_l(l-s) general-l (RH01L/RH05L), the moment identity
     E[ln(1+u)]_l = 1/(l-1), the per-pair flip *as certified algebra*
     (RH16L), the 3-4-1 admissibility bound alpha >= 1 with equality
     only at the classical point (RH11L -- this specific statement is
     new), the doubled-completion no-go with its counterexample (RH13).
  2. The empirical kill ladder at fixed budgets: 0.6736 +/- 0.0011 at
     N=30,000 (z = 151.8 vs 1/2), GUE match at 1.2 sigma, repulsion
     CDF ratio 0.07, moment spine kills at 62-570 sigma.
  3. The exact Li constants to 1e-81 (computed via the Hadamard product
     -- the numbers themselves were produced in-lane and verified).
  4. The prime-gas identity M(sigma) = ln zeta(sigma) - ln zeta(2sigma)
     (recorded as an exact identity at the level of the Euler logs).

## Bottom line

The framework-vocabulary connection to the zeta is legitimate as
Framing + Certified Algebra + Measured Numbers, and those artifacts are
kept.  It is NOT legitimate as new mathematics about the zeta's zeros:
every structural claim in RH16-18 traces to a named classical theorem
(Titchmarsh, Selberg, von Mangoldt), now correctly attributed.  This
correction is pushed on top of the lanes; no commit message will call
RH16-18 'novel mathematics' again.