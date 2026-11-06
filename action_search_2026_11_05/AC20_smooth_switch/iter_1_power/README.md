# AC20 iter_1: pure-power stiffness, n = 3 and n = 4. NOT A REPAIR (statics change)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (e6d1ad6114). Script ac20_i1.py
(sympy plus the shared harness ../harness.py, about 7 s, one thread).

| n | (a) across-switch classical well-posedness (1D) | (b) statics | repair |
|---|---|---|---|
| 3 | FAIL: Lipschitz only | CHANGED (L_eff off by up to 4.5x) | no |
| 4 | PASS (C1) | CHANGED (up to 29x) | no |

- **P-a, P-b (sympy).** For n >= 3 the force -d_x F' is continuous at a transverse zero; for n = 2 it jumps by
  -gamma c1, AC16's control. The stiff side is a polytropic gas with gamma_poly = n:
  - c^2 = gamma_n (n - 1) Pi^(n-1);
  - in (v, w), with w = 2c/(n - 1), the system is [[v, k w], [k w, v]] with k = (n - 1)/2, exactly;
  - at n = 3, k = 1, so the Riemann invariants v +- w are decoupled Burgers equations.
- **P-c (numerics, N = 400-3200; the n = 2 control falls by 1.417 / 1.413 / 1.418 per doubling).**
  - n = 3: the velocity-slope jump at the switch label converges to -0.0955 (prediction -0.1005;
    N-to-N change 0.02 %). First crossing at t_inv = 0.712 (prediction 1/sqrt 2 = 0.707). A Lipschitz solution
    exists to the gradient catastrophe, but it is not C1 for t > 0: the max(Pi, 0)-kink of w_0 travels with the
    label.
  - n = 4: the jump falls 0.0090, 0.0045, 0.0023, 0.0011, halving per doubling, so C1. t_inv converges to
    about 0.92.
- **P-d (statics).** The stiffness stays ONE constant, gamma_n, with no new constant, but its dimension changes,
  and the linearised screening length becomes charge-dependent: L_eff^2 proportional to Pi^(n-2). Fixed to the
  record floor at the globulars' 0.084 Msun/pc^3, L_eff moves by 4.5x (n = 3) or 29x (n = 4) at NGC 2419's
  2.5 and the Cassini minimum. So the D10 floor and the C6 / Cassini solves would all have to be redone.
  Statics are not preserved.
- **MUTATE** (n = 2 through the n = 4 smoothness test): (a) FAILs, so the control bites (exit 1).
- **Bookkeeping fix.** On the first run the sympy symbols x, x_s were declared positive. Sympy then dropped the
  Heaviside jump, and the n = 2 control check failed. They are now declared real, as in AC16, and the rerun
  passes. No numerical result changed.

**Reading.** Contact order 4 or more restores C1 in 1D, but a pure power changes how screening scales with
charge. The next step, iter_2, keeps v3s's quadratic form away from the switch and raises the contact order
only within a charge scale a = s^2 of it.
