# AC20 iter_3 frozen criteria: spline contact, exact v3s / AC2q form for Pi >= b

Frozen after iter_1/iter_2 (afa3c5035c) and before any iter_3 number. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing.

Why: iter_2 missed C-c on resolution (the jump was halving toward 0 but the ladder was too short). It missed C-e
structurally: smoothing on the charge's own scale puts AC2q's FRW background (Pi = 2X) inside the smoothing zone.
The fix moves the smoothing strictly below the background.

## The form

F(Pi) = 0 for Pi <= 0; F = (gamma/2) Pi^2 for Pi >= b; on [0, b], F = Pi^m (c_0 + ... ) is the unique polynomial
with contact order m at 0 (F = F' = ... = F^(m-1) = 0) that matches F, F', F'', F''' of (gamma/2) Pi^2 at b
(C^3 at the knot). m = 4 (graded, 1D) and m = 6 (degree 9; the 3D Sobolev count needs it; S-a/S-b only).
b: AC2q b = X (half its FRW charge 2X, so FRW lies in the exact region for any b < 2X); v3s b = rho_DE (from the
a0 law). Not a new constant. The choice b = X versus another b in (0, 2X) is a shape choice that no gate is
tuned on; numerics use two b values to show the results do not depend on it.

## Checks

- S-a (sympy, m = 4 and 6): the coefficients exist and are unique; F'' >= 0 on [0, b] (so c^2 = Pi F'' >= 0
  everywhere); F in C^3.
- S-b: F = v3s exactly for Pi >= b; max over [0, b] of |F' - gamma Pi| / (gamma b) is reported, and
  |F' - gamma Pi| <= gamma b.
- S-c (numerics, harness, gamma = 1, Pi_0 = tanh q, N = 800 / 1600 / 3200 / 6400 / 12800, t_meas = 0.05):
  - spline m = 4, b = 0.4 and 0.1: finest-N |Delta v_x| <= 0.1 x 0.1005, and the last-two-rung ratio
    |Delta(N/2)| / |Delta(N)| in [1.6, 2.4] (first-order convergence to zero, the C1 signature); t_inv converged
    (last-two-rung ratio [0.9, 1.1]).
  - iter_2's contact form, a = 0.4 and 0.1, on the same extended ladder and the same lines (a regrade of
    iter_2's C-c, labelled as such).
  - discrimination controls on the same ladder: iter_1's n = 3 must give a ratio in [0.9, 1.1] with |Delta|
    about 0.1 (a finite kink that is not C1); v3s (n = 2) must give a ratio < 0.9 (growing). If either control
    falls in [1.6, 2.4], the test has no power and no verdict stands.
- S-d (statics, both footings): change only on 0 < Pi < b; relative <= b/Pi at Cassini (0.0055 / 0.0062) and
  inside Lstar (0.084); scaled floor shift (b/1.5e-4) x 0.042 % <= 0.01 %; SPARC (Lstar/1 kpc)^2 b/rho_ph <= 1e-4.
- S-e (AC2q FRW, AC7 Q1 method, b = X): g1 = F''(2X) = gamma, g2 = d/dX F'(2X) = 2 gamma; integrated factor
  (1 - 2 gamma s^2)^2, = 1 at s = 0; 72/72 physical fixtures healthy.
- S-f: soft side identical (AC10's fold unchanged).

## Labels

- REPAIR (1D) for v3s if S-a, S-b, S-c (spline rows and both controls), S-d pass; for AC2q also S-e.
- iter_2's regrade label is reported separately (C-c on the extended ladder); its C-e failure stands.
- 3D: only the m = 6 existence and convexity (S-a) are graded; 3D well-posedness itself is not tested.
- MUTATE (AC20_MUTATE=1): the spline with m = 2 (no contact: the v3s kink) through S-c must FAIL.

## Lean (added to AC20_smooth_switch.lean)

L6: the m = 4 spline's F''/gamma on [0, b] (scaled q = Pi/b in [0, 1]) is >= 0
[MUTATE twin: the same polynomial with a sign error is claimed >= 0 and must fail].
