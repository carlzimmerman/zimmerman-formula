# AC11 frozen criteria: the moving Sun in AC2q's clock frame

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. No dark-matter particle. Analogue of astra's
AZ37 (astra_goal_2026_11_05/AZ37_moving_sun, criteria 80a14d9d9c), which is read
and reproduced, never edited.

AC2q: AC2 (../AC2_single_clock/ACTION.md) with the stiffness
-(gamma/2){[max(D.P + 2X, 0)]^2 - (2X)^2} (AC7, d063cd6e5f). The clock is the
canonical dark-energy scalar phi; s^2 = phidot^2 <= 2 rho_DE = 8 a0^2 (geometric
units, framework-native). Both footings, never pooled: canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2.

## Verdict lines (AZ37's definitions)

- Full PASS needs the physical moving branch on a Galactic charged background, a
  regular solution over the claimed region and its metric response.
- FAIL needs a physical inconsistency: here, Omega^2 < 0 (exponential charge
  growth) on any physical on-region cell of the B2 grid, or X <= 0 forced by
  the linear moving response on that grid, or a measured exclusion.
- Otherwise NO VERDICT on the complete moving-Sun prediction. An exact
  alternative branch, its absence, or a linear local response alone gives
  NO VERDICT. A static potential divided into a gravitomagnetic coefficient is
  not alpha_1, and no alpha_1/alpha_2 is reported unless derived on the moving
  equations.

## B1. Does AZ37's exact P = 0 GR branch exist in AC2q? (sympy)

At P = 0 derive the P equation of AC2q. Prediction to test: it reads
A_i + 2 gamma D_i X = 0 (spatial), and with A_i = -D_i X/(2X) for a scalar clock,
it forces D_i X = 0: a geodesic clock, phi = f(tau) with |d tau| = 1. Then phi's
own Klein-Gordon equation, -f'' - f' theta = V'(f) (theta = div n), requires
theta to be constant on each leaf unless f' = s = 0.
- B1a: derive the P equation and the scalar-clock acceleration identity.
- B1b: on AZ37's Schwarzschild congruence family tau = E t + T(r),
  T' = sqrt(E^2 - f)/f (symbolic E; E = 1, 13/12, 5/3), compute theta(r) and test
  whether it is constant on a leaf (d theta/dr at fixed tau = 0).
- Label BRANCH ABSENT (for s != 0, on the tested family) if theta varies on the
  leaf; BRANCH PRESENT otherwise. This is not a theorem about every congruence.
- Size: the branch's failure sources P through 2 gamma D X; report the relative
  size gamma s^2 (it bounds how far the approximate GR branch is from exact).
- Known answer: s = 0 removes the Klein-Gordon obstruction (AZ37's branch).

## B2. Forced oscillator on AC2q's own linear system (sympy + numbers)

AC7 q2()'s hand-built on-region system (validated there against an automatic
linearisation), isotropic Hessian K M_theta, with a baryon source
-K delta rho_b added to the Poisson equation. Solve for the charge response
drt per unit delta rho_b: the transfer T(omega, k).
- B2a known answer: at s = 0, T = K rho0/(Omega^2 - omega^2) with
  Omega^2 = K rho0 [M_theta - 1 + Lstar^2 k^2/2], AZ37's oscillator, identically.
- B2b: AZ37's grid (rho0 0.0447 / 0.0514 Msun/pc^3, x_e 1.15 / 2.6,
  M_theta = (1+x_e)^2, Lstar 21.68/24/27 pc canonical and 22.85/24/24.60 alt,
  v 220 / 369 km/s, k = 1/r for r = 1 and 9.58 AU) at s^2 = 0 must reproduce
  AZ37's phase-speed ranges 753.5-938.4 m/s (canonical), 851.6-916.9 m/s (alt)
  to 4 significant figures, and with s^2 = 8 a0^2 give AC2q's Omega'^2, phase
  speeds and pole cosines. Resonance SURVIVES if every cell has 0 < pole <= 1.
- B2c: finite-time response: AZ37's exact zero-initial-data solution with
  AC2q's coefficients (any instantaneous part of T kept separately), at 1 and 10
  crossing times, transverse / resonant / parallel directions. s = 0 must
  reproduce AZ37's maximum |rho_tau/rho_source| 5.384e-15 / 6.191e-15 to 1e-6
  relative. Report the AC2q maximum and its relative change.
- B2d (X > 0 and the khronon velocity): from the same linear solution, the
  clock-velocity transfer |k dsigma| and the relative X change |dC2|/s^2 per unit
  delta rho_b. Line for FAIL: X <= 0 would need |dC2|/s^2 >= 1 at the source
  amplitude; report the amplitude at which that would happen.
- B2e (linearity diagnostic, information): the linear static response of the
  Sun's own charge is q_sun(r) = Phi_N/gamma (from T at omega = 0 and the
  Lstar^2 k^2 term). Report q_sun/rho0 at 1 and 9.58 AU and the radius where it
  equals rho0. Where q_sun >> rho0 the frozen Galactic coefficients are not the
  local background and the B2 test is outside its own validity.
- Off-region (D.P + 2X < 0): report its oscillator and phase speed (not graded:
  the Galactic background at the Sun is on-region).

## Tolerances and controls

- Symbolic identities exact (simplify to 0). DOP853 pairs 1e-9/1e-11 against the
  exact solution: relative error <= 1e-7. 50-digit convolution check <= 1e-30.
- MUTATE (separate outputs, AC11_MUTATE=1): gamma -> -gamma in B2. On the grid
  Omega'^2 must turn negative (no real phase speed) in every cell; if it does
  not, B2 has no power and no verdict stands on it.
- One thread per job, <= 2 GB, minutes, no downloads.
