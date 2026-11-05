# AC8 frozen criteria: AC2q's static limit against v3s's

Frozen before any graded output. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Question

Can v3s's static results (AQUAL law S, SPARC, the Cassini hedgehog and the Lstar floor) be carried
to AC2q (AC7, d063cd6e5f), and with which corrections?

## Method (sympy, exact)

PN Lagrangians: v3s = H4's A1 Lagrangian at mu_K = 0 (the dust's mass term off, as in galaxies);
AC2q = AC7's Lagrangian in its on-region (D.P + 2X >= 0). Static ansatz: sigma = 0, all fields
time-independent. Derive both sets of Euler-Lagrange equations and print their difference.

## Lines

- TRANSFERS (with stated corrections) if every difference term is proportional to s^2 = phidot^2,
  i.e. vanishes identically at s = 0, and sigma = 0 solves AC2q's sigma equation exactly in statics.
  The corrections are then bounded with AC6/AC7 numbers: P equation relative 2 gamma s^2 (<= 1e-10),
  Poisson source s^2 (<= 2 rho_DE, framework-native).
- DOES NOT TRANSFER if any difference survives at s = 0, or sigma = 0 is not a static solution.

## Control

MUTATE (separate output): flip the sign of the W term in the AC2q Lagrangian only. A difference
must then survive at s = 0. If it does not, the comparison is not sensitive and no verdict stands.
