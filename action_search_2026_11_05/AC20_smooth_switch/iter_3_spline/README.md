# AC20 iter_3: spline contact (exact v3s/AC2q form for Pi >= b). NOT A REPAIR as frozen (resolution line missed again)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (a13f5eb1f5). Script ac20_i3.py
(about 2 min, one thread).

The form: F = 0 for Pi <= 0. On [0, b], F = gamma b^2 (5q^4 - 10q^5 + 15q^6/2 - 2q^7) with q = Pi/b (contact order 4, C^3 at
the knot). For Pi >= b, F = (gamma/2) Pi^2 exactly. b = X for AC2q (FRW sits at Pi = 2X, inside the exact region);
b = rho_DE for v3s.

| check | result |
|---|---|
| S-a, m = 4 | PASS. Unique polynomial; F''/gamma = -q^2 (84q^3 - 225q^2 + 200q - 60) >= 0 on [0, 1] (Lean `L6_spline_convex`) |
| S-a, m = 6 (3D-ready) | **FAIL.** The C^3, degree-9 polynomial is not convex on [0, 1]; F'' < 0 near q = 0.83 |
| S-b | PASS. max over [0, b] of |F' - gamma Pi| = 0.108 gamma b (m = 4) |
| S-c, spline rows | **FAIL as frozen.** The jump halves per doubling: ratio 1.976 / 1.966, and t_inv converges (1.005 / 1.017). But the finest-N jump is 0.035 / 0.56 against the 0.01005 line |
| S-c, controls | Both discriminate. n = 3: the jump stays at 0.0955, ratio 1.000 (a finite kink). v3s: 0.08, 0.34, 1.5, 8.0, 29 (ratio 0.276, growing) |
| iter_2 regrade (C-c) | a = 0.4 PASS: 0.00346, ratio 1.971. a = 0.1 misses: 0.053, ratio 1.893 |
| S-d | PASS, both footings. b = rho_DE = 8.6e-8 / 1.3e-7 Msun/pc^3; Cassini 1.6e-5 / 2.0e-5, inside Lstar 1.0e-6 / 1.5e-6 |
| S-e (AC2q FRW) | PASS. g1 = gamma, g2 = 2 gamma, factor (1 - 2 gamma s^2)^2 (AC7's exactly); 72/72 healthy |
| MUTATE (m = 2 spline = v3s) | S-c FAILs, so the control bites (exit 1) |

- **Reading (post-run).** Every smoothed row shows first-order convergence of the jump to zero, which is the C1
  signature, while the n = 3 kink stays fixed and the v3s jump grows. The absolute line is the wrong statistic:
  the stencil error delta x v_xx is large wherever the force bends, over the width b, so no finite ladder clears a
  fixed line for small b. iter_4 tests this with a Richardson statistic on fresh initial data, frozen before it
  was run.
- **Bug fix (kept on the record).** In the first run, the spline's F' below b was identically 0: `sympify` of the
  stored polynomial made a fresh symbol q, so its derivative was 0, which put a jump in F' at b. That output is
  kept as ac20_i3_BUGGY_first_run.out. The fix passes `locals={"q": q}`. All other rows were unaffected and
  reproduced to the last digit.
