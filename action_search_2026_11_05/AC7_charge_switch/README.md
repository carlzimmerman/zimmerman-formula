# AC7: AC2 with the stiffness switched on the khronon charge (AC2q) — SURVIVES Q1-Q4

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (b0d44a6952),
frozen before any graded number. Scripts: ac7.py, mb_knife_edge.py.

## The candidate

    S = Int sqrt(-g) [ Mpl^2 R/2 + X - V(phi) + P.A - W(p, a0)
                       - (gamma/2) { [max(D.P + 2X, 0)]^2 - (2X)^2 } + lambda_P n.P ] + S_b[g],

with AC2's definitions (one canonical scalar is both dark energy and the clock; a0^2 = xi G V;
gamma = K Lstar^2/2). The switch sits on D.P + 2X, which is the khronon charge AC6 derived
(div P + phidot^2). Where it is on, the term is AC2's plus -2 gamma X D.P; where off, +2 gamma X^2.
C^1 across the switch, convex in P at fixed X.

## Results

- **Q1 (FRW, exact).** Integrating the longitudinal polarization out multiplies AC2's lapse term
  Mpl^2 cY k^2 alpha^2 by **(1 - 2 gamma phidot^2)^2**. The frozen prediction said (1 + 2 gamma s^2)^2:
  the sign of that prediction was wrong; the derived factor is still a perfect square, = 1 at s = 0.
  All 72 physical fixtures (gamma s^2 = 0 and 1e-11) and all 72 stress fixtures (0.1, 1) have positive
  kinetic and gradient terms and phase and group speeds in (0, 1]. Known answer: factor 1 gives AC2's
  analytic dispersion identically. Physically gamma phidot^2 ~ G Lstar^2 rho_DE / c^2 ~ 1e-11 [erratum, AC9: 1e-11 is the fixture value, a conservative upper bound; the computed value at s^2 = 2 rho_DE is 2.4e-17 canonical / 4.0e-17 alt].
- **Q2 (galaxies, PN WKB).** The hand-built linear system equals an automatic linearisation of the
  Euler-Lagrange equations (isotropic W) identically. On-region UV limit
  omega^2/k^2 -> gamma (d0 + s^2 - 2 gamma d0 s^2)/(1 - 3 gamma s^2 + 4 gamma^2 s^4 - 2 gamma^2 d0 s^2):
  positive on the whole on-region (d0 >= -s^2, |2 gamma d0| < 1); 0 negative grid points. Off-region:
  omega^2 -> K rho_q (M_theta - 1), k-independent (bounded). So: no Gamma ~ k anywhere.
- **Q3.** |2 gamma D.P| <= 2.2e-10 on every record value (Solar System 0.045 Msun/pc^3, H4 medians),
  Lstar 21.7-90 pc; a 1e3 Msun/pc^3 stress value gives 4.9e-6.
- **Q4.** The new term shifts screened statics by at most 2 phidot^2/D.P = 7.7e-6 (canonical),
  1.1e-5 (alt) at the Solar-System value, against Cassini's 4.8e7 margin.

## Controls

- M-a (gamma -> -gamma): Q2b fails on 34 grid points. Bites.
- M-b (switch on D.P alone, as v3s): on FRW, where D.P = 0, the two sides integrate to different lapse
  coefficients, alpha^2 k^2/(4(K + gamma k^2)) vs alpha^2 k^2/(4K): non-analytic, and the D.P < 0 side
  is AC3's singular Lstar = 0 branch. So the v3s placement cannot work with a dark-energy clock.

## What it does not show

No nonlinear evolution, no sourced inhomogeneous background solved on its own equations, no
Solar-System, galaxy, lensing or tensor regrade on AC2q's own equations, no X > 0 preservation, and
no fixing of xi or kappa. Those are the next obligations. AC5's slow-mode question stays NO VERDICT.
