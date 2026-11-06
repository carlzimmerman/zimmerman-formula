# AC20 iter_4: fresh-data Richardson C1 test. v3s with the contact form: REPAIR (1D); the spline: NOT A REPAIR as frozen

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (054b3bdec4), frozen before this run.
Script ac20_i4.py (about 3 min, one thread). New data: Pi_0 = tanh 2q, v_0 = 0.2 sin q, t_meas = 0.03, N = 800-12800.
Line: |Delta_inf| <= 0.1 x |Delta_n3| = 0.0226.

| row | Delta(12800) | Richardson Delta_inf | ratio | t_inv ratio | C1 |
|---|---|---|---|---|---|
| contact a = 0.4 | -0.0161 | -0.0009 | 1.94 | 1.018 | PASS |
| contact a = 0.2 | -0.0625 | -0.0068 | 1.89 | 1.023 | PASS |
| spline b = 0.4 | -0.162 | -0.0071 | 1.96 | 1.020 | PASS |
| spline b = 0.2 | -0.646 | **-0.0399** | 1.94 | 1.024 | **FAIL** (line 0.0226) |
| control n = 3 | -0.2256 | -0.2256 | 1.000 | 1.003 | finite kink (bites) |
| control v3s | +37.4 | +69.0 | 0.154 | 1.416 | grows (bites) |

- **Labels, as frozen.**
  - v3s with the contact form (a = 2 rho_DE): REPAIR (1D).
  - v3s and AC2q with the spline: NOT A REPAIR. The b = 0.2 row misses. Its jump still halves per doubling
    (ratio 1.94), but at b = 0.2 the ladder is pre-asymptotic: the jump grew from N = 800 to 1600.
  - AC2q with the contact form: NOT A REPAIR (iter_2's C-e stands).
- **S-a' (contact order 6, C^2 knot, degree 8): FAIL.** F''/gamma = q^4 (280q^2 - 504q + 225) has two roots in
  (0, 1), so it is negative between them. With iter_3's C^3 failure, no convex polynomial spline of this kind
  reaches the contact order 6 that the 3D Sobolev count asks for.
- **MUTATE** (v3s's F through the statistic): FAILs, so the control bites (exit 1).
