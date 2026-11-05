# AC8: AC2q's static limit equals v3s's at mu_K = 0 — TRANSFERS (corrections proportional to phidot^2)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (bc4a81ee47).
Script: ac8.py (sympy, exact).

- With sigma = 0 and static fields, the Euler-Lagrange equations of AC2q (AC7, on-region) minus those of
  v3s (H4's A1 Lagrangian at mu_K = 0) are, exactly:
  - Poisson: + s^2 (1 - 2 gamma div P)/(1 + phi)^3, the clock's own gravitating density, at most 2 rho_DE
    (framework-native 8.6e-8 / 1.3e-7 Msun/pc^3); the same role v3s's Lambda plays inside J;
  - P equation: + 2 gamma s^2 grad(phi)/(1 + phi)^3, a relative correction 2 gamma s^2 <= 2.2e-10 (AC7 Q3).
- Every difference vanishes identically at s = 0, and sigma = 0 solves AC2q's sigma equation exactly in statics.
- Control (W sign flipped in AC2q only): a difference survives at s = 0. Bites.

**Consequence.** v3s's static results carry to AC2q with corrections far below every tolerance on record:
the simple-mu law S (SPARC rms 0.054 dex), the Cassini hedgehog (margin 4.8e7; AC7 Q4 static shift <= 1.1e-5),
the outer-globular Lstar floor. Not carried: anything dynamical (moving Sun, caustics, nonlinear evolution),
lensing beyond the static potential, and anything that used v3s's dust (AC2q has none).
