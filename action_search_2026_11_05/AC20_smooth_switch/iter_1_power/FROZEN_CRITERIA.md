# AC20 iter_1 frozen criteria: pure-power stiffness F = (gamma_n/n) max(Pi, 0)^n, n = 3, 4

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Analysis to be checked (sympy)

Stiff side is a polytropic gas: pressure p = Pi F' - F = gamma_n (n-1)/n Pi^n, sound speed
c^2 = Pi F'' = gamma_n (n-1) Pi^(n-1), Riemann invariants v +- w, w = 2c/(n-1), and in (v, w) the system
is [[v, k w], [k w, v]] with k = (n-1)/2 (exact; linear in w). Across a transverse zero
(Pi_0 = c1 (x - x*)), the data w_0 is proportional to max(Pi_0, 0)^((n-1)/2).
- n = 3: w_0 is Lipschitz with a kink (slope jump d = sqrt(2 gamma_3) c1). The invariants are decoupled
  Burgers equations, so a Lipschitz solution exists to t = 1/d, but the velocity slope jumps at the label:
  Delta v_x(t) = -d^2 t / (1 - d^2 t^2) (v_0 = 0). Prediction: no C1 solution for t > 0 -> classical FAIL,
  but no immediate shell crossing.
- n = 4: w_0 ~ max^(3/2) is C1 and the speeds v +- (3/2) w are C1 in (v, w), so 1D C1 local well-posedness
  holds (diagonal-system theory) -> classical PASS (1D).

## Checks

- P-a (sympy): force -d_x F' is continuous at a transverse zero for n = 3, 4; jump -gamma c1 for n = 2
  (control).
- P-b (sympy): pressure, c^2, w and the (v, w) system as stated; Burgers decoupling for n = 3.
- P-c (numerics, AC16's Lagrangian scheme with force -d_x F'(Pi), gamma_n = 1, Pi_0 = tanh q,
  N = 400/800/1600/3200, v_0 = 0):
  - n = 3: velocity-slope jump at the interface label at t = 0.05 (one-sided least-squares slopes over
    4 cells) converges to -d^2 t/(1 - d^2 t^2) = -0.1005 within 15 % (finest N), last-two-N change <= 5 %;
    first crossing time t_inv converges (last-two-N ratio in [0.9, 1.1]) to 1/d = 0.7071 within
    [0.6, 0.85].
  - n = 4: |Delta v_x| at finest N <= 0.1 x 0.1005 and decreasing with N; t_inv converges (ratio
    [0.9, 1.1]).
  - control n = 2 (AC16): t_inv falls by a ratio in [1.2, 1.7] per doubling (must bite).
- P-d (statics): gamma_n has dimension gamma x [charge]^(2-n): the single stiffness constant changes
  dimension; it is still ONE constant bounded below by the globular floor (no extra constant). But the
  linearised screening length becomes charge-dependent, L_eff^2 = L_n^2 (n-1) (Pi_bar/Pi_ref)^(n-2).
  Graded line for "statics preserved": with gamma_n fixed so that L_eff equals the record floor at the
  floor-setting charge (the record's min D.P inside Lstar for the outer globulars, 0.084 Msun/pc^3,
  X3 D4), L_eff must stay within 1e-3 relative of the v3s value at every other graded static charge:
  Cassini minimum 0.0055 / 0.0062 Msun/pc^3 (X3 D2), the Sun's 0.0447 / 0.0514, NGC 2419's 2.5.
  Otherwise statics are CHANGED (re-derivation of the floor and C6/D10 re-solves needed) = (b) FAIL.

## Labels

- per n: (a) classical across-switch well-posedness PASS / FAIL (1D), (b) statics PRESERVED / CHANGED.
- A candidate counts as a repair only with (a) PASS and (b) PRESERVED.
- MUTATE (separate outputs, AC20_MUTATE=1): run n = 2 through the same grader; (a) must FAIL.
