# AC20 iter_2 frozen criteria: contact form F = (gamma/2) Pi_+^4 / (Pi_+ + a)^2, a = s^2

Frozen before any graded number (same commit as iter_1). Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

The form equals v3s's (gamma/2) Pi^2 for Pi >> a, has contact order 4 at Pi = 0, and is 0 for Pi <= 0.
a is not a new constant: AC2q's own 2X (= s^2 <= 2 rho_DE); for v3s, a = 2 rho_DE with
rho_DE = a0^2/(kappa^2 c^2 G) (the a0 law), per footing. AC2q's term becomes -[F(D.P + 2X) - F(2X)]
(zero on FRW at P = 0, as AC7's subtraction).

## Checks

- C-a (sympy + Lean): F' = gamma Pi^3 (Pi + 2a)/(Pi + a)^3; F'' = gamma f'(u), u = Pi/a,
  f'(u) = u^2 (u^2 + 4u + 6)/(u + 1)^4 >= 0, so c^2 = Pi F'' >= 0 for every Pi (soft side 0); F'' -> gamma.
- C-b (sympy + Lean): 0 <= gamma Pi - F'(Pi) <= gamma a for Pi >= 0 (absolute force deviation from v3s
  bounded by gamma a; relative by a/Pi).
- C-c (well-posedness, 1D): Riemann invariants v +- w, w(Pi) = int_0^Pi sqrt(F''/q) dq; near 0,
  w ~ Pi^(3/2), so w_0 is C1 across a transverse zero and the speeds v +- c(w) are C1 in w (c = (3/2) w +
  O(w^(5/3))). Prediction: 1D C1 local well-posedness PASS. Classical lifespan scales as sqrt(a/gamma)/c1
  (gradient catastrophe of the compressive invariant), then ordinary gas shocks.
  Numerics (gamma = 1, a = 0.4, 0.1, 0.025, same harness as iter_1):
  - |Delta v_x| at t = 0.05, finest N, <= 0.1 x 0.1005 and decreasing with N, for every a;
  - t_inv converges in N (last-two-N ratio in [0.9, 1.1]) for every a;
  - T(a) = t_inv(finest N) ~ a^p with fitted p in [0.35, 0.65] (prediction 1/2).
- C-d (statics, bounds; both footings): relative stiffness-force change <= a/Pi at
  Cassini minimum D.P (0.0055 / 0.0062 Msun/pc^3) and inside Lstar for the outer globulars
  (>= 0.084, X3 D4): each <= 1e-3. Floor shift by scaling X3 D4 (a 100 % stiffness change on lobes
  >= 1.5e-4 Msun/pc^3 deep moved the floor <= 0.042 %): bound (a / 1.5e-4) x 0.042 % <= 0.01 %.
  SPARC: stiffness enters the law at O((Lstar/R)^2); bound (Lstar/1 kpc)^2 x a/Pi_ph with Pi_ph the deep-MOND
  phantom density at 30 kpc for 1e9 Msun: <= 1e-4.
- C-e (AC2q FRW, AC7 Q1 method): quadratic coefficients g1 = F''(2X; a = 2X), g2 = d/dX F'(2X; 2X);
  integrated longitudinal-P lapse factor positive, = 1 at s = 0; all 72 physical fixtures healthy
  (gamma s^2 in {0, 1e-11}).
- C-f (caustics): F = 0 for Pi <= 0, so the soft-side PN equations, hence AC10's fold, are identical
  (sympy: soft-side Euler-Lagrange equations equal). Reported, not required.

## Labels

- REPAIR (1D) if C-a, C-b, C-c (all numerics), C-d and C-e pass. Scope: 1D planar PN; 3D needs data in H^s,
  s > 5/2, which this contact order does not give (w ~ Pi^(3/2) is in H^s only for s < 2): 3D classical
  well-posedness would need contact order >= 6; stated, not graded.
- NOT A REPAIR if any of C-a..C-e fails.
- MUTATE (AC20_MUTATE=1): replace the contact form by v3s's F (exponent 2, a = 0): C-c must FAIL
  (Delta v_x stays finite, t_inv falls like N^-1/2).

## Lean claims (AC20_smooth_switch.lean; the MUTATE twin states the four bracketed false variants)

L1 symmetrizer: H A - A^T H = 0 for A = [[v, Pi], [g, v]], H = diag(g, Pi) [false variant: H = diag(Pi, g)].
L2 force continuity core: |max(c h, 0)^m| <= |c|^m |h|^m (m >= 2 gives a zero one-sided derivative);
   m = 1 one-sided quotients c and 0.
L3 convexity numerator: (4u^3 + 6u^2)(u + 1) - 3u^3(u + 2) = u^2 (u^2 + 4u + 6) >= 0
   [false variant: = u^2 (u^2 + 4u + 5)].
L4 deviation: Q^3 (Q + 2a) = Q (Q + a)^3 - a Q (Q^2 + 3aQ + a^2) and Q (Q^2 + 3aQ + a^2) <= (Q + a)^3,
   Q, a >= 0 [false variant: <= Q^3].
L5 n = 3 kink growth: d/(1 + d t) + (-d)/(1 - d t) = -2 d^2 t/(1 - d^2 t^2) [false variant: = 0].
