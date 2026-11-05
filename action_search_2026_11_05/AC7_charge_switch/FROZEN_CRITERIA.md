# AC7 frozen criteria: AC2 with the switch on the khronon charge (candidate AC2q)

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. No dark-matter particle.

## Why

AC6 (777a7b62f5): AC2's smooth stiffness is Hadamard ill-posed wherever the
khronon charge rho_eff = D.P + phidot^2 < 0, which happens in 6 of 7 H4 systems.
Switching on D.P alone (as v3s) leaves a knife edge on FRW (D.P = 0 there).
AC7 tests the switch on the charge itself, with the clock's X^2 piece removed
so that the clock's own kinetic function is unchanged where the switch is on:

    S_stiff = -(gamma/2) Int sqrt(-g) { [max(D.P + 2X, 0)]^2 - (2X)^2 },

all else as AC2 (../AC2_single_clock/ACTION.md). Where D.P + 2X >= 0 this is
AC2's term plus -2 gamma X D.P; where D.P + 2X < 0 it is +2 gamma X^2 (no P
stiffness). The function is C^1 across the switch and convex in P at fixed X.

## Tests

Q1 (FRW, exact, sympy). Longitudinal P integrated out on FRW in unitary gauge
with the new term. Prediction to test: AC2's lapse term Mpl^2 cY k^2 alpha^2 is
multiplied by (1 + 2 gamma s^2)^2, s^2 = phidot^2, nothing else changes at
quadratic order. Then AC2's 36 fixtures (3 eps x 3 ell x 4 x) rerun with that
factor at gamma s^2 in {0, 1e-11, 0.1, 1}: kinetic > 0, gradient > 0,
phase and group speeds in (0, 1]. Known answer: gamma s^2 = 0 reproduces AC2's
analytic dispersion identically.

Q2 (galaxies, PN WKB, sympy). H4/AC6 frozen-background system with the new
term (P equation gets +i gamma k khat dC2, continuity and Poisson get the
(1 - 2 gamma D0) and (1 - 2 gamma s^2) factors). Validation: the hand-built
linear system must equal an automatic linearisation of the Euler-Lagrange
equations for an isotropic quadratic W (residual 0). Graded: the sign of
lim_{k->inf} omega^2/k^2 in the on-region (rho_eff >= 0) must be >= 0 for all
D0 with |2 gamma D0| < 1; in the off-region the limit omega^2(k->inf) must be
finite (bounded rate).

Q3 (sizes). 2 gamma D.P on the record's systems: H4/AC6 maxima and the
Solar-System screened value 0.045 Msun/pc^3, at Lstar 21.7 / 22.9 / 90 pc.
Line: |2 gamma D.P| < 1e-3 everywhere tabulated.

Q4 (screened statics). Relative shift of screened D.P from the -2 gamma X D.P
term, bounded by 2 phidot^2 / D.P with phidot^2 <= 2 rho_DE (framework-native,
AC6 values): must be < 1e-3 at the Solar-System value, i.e. far inside
Cassini's 4.8e7 margin.

## Lines

- AC2q SURVIVES Q1-Q4 if every graded item passes.
- FAIL if Q1 positivity/speeds fail at any gamma s^2 <= 1e-11 (physical), or
  Q2's on-region UV limit can be negative with rho_eff >= 0 and |2 gamma D0| < 1.
- Larger gamma s^2 (0.1, 1) are stress values, reported, not graded.
- A pass is not full health: no nonlinear, sourced-background, Solar-System
  solve or lensing regrade is done here.

## Negative controls (separate outputs)

- M-a: gamma -> -gamma in Q2. The on-region UV limit must turn negative.
- M-b: switch on D.P alone on FRW: show the quadratic action is not analytic
  in the longitudinal P mode at D.P = 0 (one-sided coefficients differ).
