# QX7 iter_7 (door B): switch retention + a remnant tracing the hot gas. SHAPE FAIL (groups); X-COP on the line; a shape clue

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria c302aa5804 + Amendment A1, both pushed before any number.
Script: qx7_iter7.py (seconds). Outputs: qx7_iter7.json/.out, run_main.txt.

**Scope (A1):** iter_4's retention rule is the idealisation QX10 iter_2 refuted, so the galaxy gates here pass BY ASSUMPTION.
No global label is possible. The graded output is the SHAPE test: X-COP AND groups (strict) on both footings, AND ellipticals
inside G7, at a lambda_0 in iter_4's growth window. The test is also CONDITIONAL on a pressureless phase-mixed remnant.

## Result: SHAPE FAIL, both footings (every window lambda_0, 1.47-8.25 Mpc)

| lambda_0 | ellipticals keeping dust | G7 shift (0.15) | X-COP gas-traced (mean/rms; HO1 0.05/0.10) | groups strict fst0 / fst1 (need 16) |
|---|---|---|---|---|
| 1.47 | 7/7 | -0.59 / -0.58 FAIL | +0.019/0.1003, -0.006/0.0996 | 2/0, 2/0 |
| 2.61 | 2/7 | -0.17 / -0.17 FAIL | same | 2/0 |
| 3.16-8.25 | 0/7 | 0 PASS | same (retention unchanged in X-COP) | at most 2/0 |

- **X-COP sits on the line.** Canonical rms 0.1003 misses the 0.100 line by 0.0003; alt 0.0996 passes. The mean is +0.019 / -0.006.
  As frozen, X-COP does not pass on canonical.
- **Tracing all baryons instead (reported):** X-COP passes, -0.003/0.082 and -0.027/0.087, which reproduces QX29 B1 (K2).
- **Ellipticals:** for lambda_0 >= 3.16 the switch empties all seven, so they keep the plain law and G7 is clean.
- **Groups are the killer, and their miss has a shape.** At lambda_0 3.16 (canonical, fst 0), every group is short at R2500
  (+0.01 to +0.26 dex) and over-massed at R500 (-0.06 to -0.27). With fst 1, everything is over. The group gas profile is steep
  (gas fraction rising outward), so a remnant that traces the gas sits too far out.

## The clue

Every profile tried for the missing mass in hot systems, from QX7 iter_4 to iter_7, misses the same way: too little in the
centre, too much outside.
- iter_4: the isolated core.
- iter_5: the host-hydrostatic profile.
- iter_7: the gas-traced remnant, in groups.

Only profiles that trace all baryons, including the stars, fit X-COP (QX29 B1, the reported row here). So the extra mass hot
systems need is **more concentrated than their hot gas, and is closer to the total (stars + gas) or the HSE mass profile**.
That is a target for any mechanism, not a mechanism.

## Controls (all hold)

- K1, iter_4's core: +0.0012/0.2346 vs +0.0014/0.2346 (alt -0.0228/0.2337 vs -0.0227/0.2337). PASS.
- K2, QX29 B1 reproduction: -0.0029/0.082, -0.0269/0.087 vs -0.003/0.082, -0.027/0.087. PASS.
- MUTATE A, f_cap 0: +0.4675 / +0.4345 = QX2. PASS.
- MUTATE B, lambda_0 1e-3: G5, G6 and G7 all fail. BITES.
- MUTATE C, f_cap x0.3: X-COP moves +0.239 / +0.234. BITES.
