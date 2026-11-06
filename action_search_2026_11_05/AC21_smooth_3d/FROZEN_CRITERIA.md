# AC21 frozen criteria: is the smoothed switch well-posed in 3D, and is there an AC2q smoothing that keeps FRW exact?

Frozen before any AC21 script exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Lane rules:
closure_2026_11_06/SWARM_BRIEF.md. Builds on AC16 (6d5faba9bd) and AC20 (3384fe50b6), both read only.

## What is asked

AC20 left two things open:
1. AC20 iter_2 found a contact form that repairs the v3s switch in 1D. Does it also give a well-posed theory in 3D?
2. For AC2q, no smoothing passed every frozen line. The open request is a smoothing of max(D.P + 2X, 0)^2 - (2X)^2
   that is C2 across zero charge and still gives AC2q's exact FRW lapse factor, (1 - 2 gamma s^2)^2.

The system is AC16's PN charge-velocity system in d dimensions, with general stiffness F(Pi), where F = 0 for
Pi <= 0 and F = (gamma/2) Pi^2 is v3s:

    Pi_t + div(Pi v) = 0,    v_t + (v.grad) v = -grad F'(Pi) + (order-zero terms).

The sign of Pi is carried by the labels (AC16 C1 and the AC20 harness), so the switch surface is a material surface.

## Method (iter_1: analytic, sympy plus Lean)

- **T1 (symmetrizer, d = 3).** Use the variable w(Pi) = int_0^Pi sqrt(F''(u)/u) du on the stiff side, w = 0 on the
  soft side. Then c = Pi w' = sqrt(Pi F''), and the system is w_t + v.grad w + c div v = 0,
  v_t + v.grad v + c grad w = 0. Its principal symbol is symmetric with the identity as symmetrizer, and its speeds
  are v.k (multiplicity 2) and v.k +- c|k|. sympy must confirm the symbol and the reduction exactly.
- **T2 (smooth coefficients).** The standard classical theorem (Kato 1975; Majda 1984) needs c to be a smooth
  function of w across w = 0 (Makino's 1986 vacuum symmetrization).
  - For a pure power F = Pi^m (m > 1), sympy must give c = ((m-1)/2) w exactly.
  - For AC20's contact form, gamma/2 Pi^4/(Pi+a)^2, and AC20's m = 4 spline, compute the series of c(w) at w = 0.
    A non-integer power after the linear term means c is not C2 in w, and the theorem does not apply.
- **T3 (data regularity).** If the data cross the switch transversally and F behaves as Pi^m near 0, then
  w_0 ~ (x_n)_+^((m-1)/2), which lies in H^s locally iff s < m/2 (standard). The theorem needs s > d/2 + 1, which
  holds iff m > d + 2. Lean certifies the exponent algebra. Cross-check against AC20's 1D numerics, which are
  already on record: m = 3 was a finite kink and m = 4 was C1. That matches m > 3 in d = 1.
- **T4 (existence of a 3D-admissible smoothing).** The form below is fixed now. With q = Pi/b and F = gamma b^2 f(q):
  - f = 0 for q <= 0; f = A q^6/30 on (0, tau]; a polynomial blend on [tau, 1]; f = q^2/2 for q >= 1.
  - f'' is C^4 at tau and at 1, and the blend's degree is fixed by those matching conditions plus the two
    moments f'(1) = 1 and f(1) = 1/2.
  - Search order, declared now (first convex member wins; this is a construction choice, not a gate tuning):
    tau = 1/2, 1/3, 2/3, with C^4 knots, then the same three tau with C^3 knots.
  - PASS T4 needs A > 0 and f'' > 0 on (0, 1], by exact real-root isolation. Lean certifies the matching identities.
- **T5 (statics).** F equals the v3s/AC2q form exactly for Pi >= b. Reuse AC20 S-d's bounds, which depend only on b,
  both footings (b = rho_DE for v3s, b = X for AC2q). Also require max over [0, 1] of |f'(q) - q| <= 1 (AC20 S-b).
- **T6 (AC2q FRW).** The FRW background has Pi = 2X > b = X, so it lies inside the exact region. Recheck AC20 S-e's
  g1 = gamma, g2 = 2 gamma and the factor (1 - 2 gamma s^2)^2 with sympy, on a neighbourhood of D.P = 0.
- **T7 (PN sign inside the layer).** Where Pi >= b the form is v3s's, so AC17's symbol carries over unchanged.
  For 0 < Pi < b, rerun AC17's v3s Lagrangian with the stiffness replaced by its local quadratic,
  -(gamma/2)(beta s + C s^2/2), with beta = F'(s0) - s0 F''(s0) and C = F''(s0). Report B and A_eff. PASS T7 if both
  stay positive for the T4 form on the whole layer (exact sign analysis). If the sign cannot be fixed, report it
  as UNDECIDED for the layer.

## Numerics (iter_2: a curved switch surface in 2D)

- A radial (axisymmetric 2D) Lagrangian annulus scheme: the AC20 harness transcribed to r, with area-weighted charge.
- The switch is the circle r = 1. Data: Pi_0 = tanh(2(r - 1)), v_0 = 0.2 sin(r - 1); labels r in [0.25, 3.25];
  gamma = 1; t_meas = 0.03; N = 800 / 1600 / 3200 / 6400 / 12800.
- Statistic and lines are AC20 iter_4's: Richardson Delta_inf = 2 Delta(12800) - Delta(6400), and ratio
  r = |Delta(6400)|/|Delta(12800)|.
  - C1 PASS for a row: |Delta_inf| <= 0.1 |Delta_n3(12800)|, r in [1.6, 2.4], and t_inv converged (last-two ratio in
    [0.9, 1.1]) or no crossing before t_max.
  - Rows: the T4 form with b = 0.4 and b = 0.8.
  - Controls, which must hold or the label is NO VERDICT:
    - n = 3 pure power: r in [0.9, 1.1] and |Delta_inf| >= 0.5 |Delta(12800)|;
    - v3s max form: r < 0.9;
    - compatible data under v3s's form (Pi_0 = tanh^3(2(r-1))): |Delta(12800)| <= 0.1 |Delta_v3s(12800)|.
- This tests that curvature does not spoil the C1 property. It cannot see the dimension count of T3, and the
  README will say so.

## Labels

- **3D, AC20 contact form:** NOT A 3D REPAIR if T2 or T3 fail for it; otherwise PASS.
- **3D, T4 form (v3s and AC2q):** PASS (classical H^s local well-posedness across a transverse switch in d <= 3,
  PN charge-velocity system) if T1, T2 (pure power near 0), T3 (m = 6 > 5), T4, T5 and T7 pass and iter_2's rows
  pass with discriminating controls. UNDECIDED if T7 is undecided. FAIL if T4 finds no convex member.
- **AC2q smoothing:** EXISTS if the T4 form passes T4, T5 and T6. That is also the AC2q REPAIR label in d <= 3 when
  the 3D line passes. Otherwise NO-GO for the declared family.

Out of scope, and said in the README: shocks and lifespan (the stiff side still forms ordinary gas shocks, as in
AC20), the soft-side folds (unchanged), the full covariant system, and data that are not transverse.

## Controls

- MUTATE (AC21_MUTATE=1, separate outputs): gamma -> -gamma must break T1 (c^2 < 0). The pure max form must fail
  T3 (m = 2) and fail iter_2's C1 statistic.
