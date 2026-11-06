# AC20 iter_2: contact form F = (gamma/2) Pi_+^4/(Pi_+ + a)^2, a = s^2. NOT A REPAIR as frozen (two lines missed)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (e6d1ad6114). Script ac20_i2.py
(about 10 s, one thread).

| check | result |
|---|---|
| C-a | PASS. F' = gamma Pi^3 (Pi + 2a)/(Pi + a)^3; F'' = gamma u^2 (u^2 + 4u + 6)/(u + 1)^4 >= 0, which tends to gamma; c^2 = Pi F'' >= 0 everywhere |
| C-b | PASS. 0 <= gamma Pi - F' = gamma a Pi (Pi^2 + 3a Pi + a^2)/(Pi + a)^3 <= gamma a |
| C-c, t_inv | PASS. Converges for a = 0.4 / 0.1 / 0.025: t_inv(a) proportional to a^0.450, predicted 1/2, line [0.35, 0.65] |
| C-c, smoothness | **FAIL as frozen.** At the finest N the velocity-slope jump is 0.0133 / 0.181 / 1.71, against a line of 0.0101 |
| C-d | PASS, both footings. a = 2 rho_DE = 1.73e-7 / 2.52e-7 Msun/pc^3. Relative change 3.1e-5 / 4.1e-5 at Cassini, 2.1e-6 / 3.0e-6 inside Lstar; scaled floor shift <= 7.1e-5 %; SPARC <= 1.7e-6 |
| C-e | **FAIL as frozen (= 1 at s = 0 missed).** AC2q's FRW background sits at Pi = 2X = a, i.e. u = 1, where the form differs from v3s's: the FRW stiffness is g1 = 11 gamma/16 and the linear coupling is 3 gamma/4 (AC2q: gamma and 2 gamma). The integrated lapse factor relative to AC2 at stiffness g1 is (1 - 3 gamma s^2/4)^2 > 0, and 72/72 fixtures are healthy, but it no longer reduces to AC2 at s = 0 |
| C-f | Soft side identical (F = 0 for Pi <= 0): AC10's fold is unchanged |

- **The C-c miss is a resolution miss, not a C1 failure (post-run reading).** The jump at a = 0.4 falls 0.0717,
  0.0446, 0.0250, 0.0133: ratios 1.61, 1.78, 1.89 per doubling, tending to 2. That is first-order convergence to
  zero, the C1 signature, which would cross the line at about N = 4,200. At a = 0.1 the ratios are 1.04, 1.36 and
  1.62. a = 0.025 is unresolved, because the 4-cell stencil (0.0075 at N = 3200) is not much smaller than the
  smoothing width (about a). The frozen ladder was too short; iter_3 extends it, under new frozen criteria.
- **The C-e miss is structural for AC2q, not a resolution miss.** Smoothing on the charge's own scale puts AC2q's
  FRW background inside the smoothing zone. iter_3 moves the smoothing below the background (an exact v3s/AC2q
  form for Pi >= b, with b < 2X).
- **MUTATE** (v3s's F through C-c): the jump grows 0.022, 0.080, 0.336, 1.52, so C-c FAILs and the control
  bites (exit 1).
- **Crash fix.** The first run crashed in C-e's fixture loop because the gamma-relative factor depends on k and
  K. The fixtures now use the factor relative to AC2 at stiffness g1, and the frozen "= 1 at s = 0" line is still
  graded on the gamma-relative factor (FAIL).
